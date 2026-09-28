"""LLM query rewriting: one JSON-mode call that classifies intent and returns an English string.

Two variants of the same call:

- CLASSIFY_SYSTEM (prompts/classify_system.txt) asks for `topic_en`, "3-8 ENGLISH keywords
  describing the topic". The topic string alone is searched; the question is discarded.
- TRANSLATE_SYSTEM is the same prompt with exactly one field swapped: `topic_en` -> `query_en`, a
  faithful full translation.

Same model, settings and post-processing, so the difference between the two configs is only
"search a topic label" vs "search the question". Model: Cohere command-a-03-2025.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path

from .embedders import CACHE_DIR, NO_SDK_RETRIES, cohere_client, text_key, with_backoff

PROMPT_DIR = Path(__file__).resolve().parent / "prompts"
CLASSIFY_SYSTEM = (PROMPT_DIR / "classify_system.txt").read_text(encoding="utf-8")

_TOPIC_FIELD = """\
  "topic_en": string                 // 3-8 ENGLISH keywords describing the topic, ALWAYS
                                     // in English even for Arabic messages. Used to search
                                     // an English knowledge base.
                                     // e.g. "buying a car cash vs murabaha financing\""""

_TRANSLATION_FIELD = """\
  "query_en": string                 // a faithful, complete ENGLISH translation of the user's
                                     // message, ALWAYS in English even for Arabic messages.
                                     // Preserve everything that is asked, including
                                     // comparisons, conditions, amounts and every part of a
                                     // multi-part question. Do NOT summarize, do NOT answer,
                                     // and do NOT reduce it to keywords. Used to search an
                                     // English knowledge base.
                                     // e.g. "If I lose my job, how long will my savings last,
                                     // and should I stop paying my car installments?\""""

if CLASSIFY_SYSTEM.count(_TOPIC_FIELD) != 1:
    raise RuntimeError("topic_en block not found verbatim in prompts/classify_system.txt")
TRANSLATE_SYSTEM = CLASSIFY_SYSTEM.replace(_TOPIC_FIELD, _TRANSLATION_FIELD)

VALID_INTENTS = {"purchase_simulation", "financial_question", "product_advice", "chitchat"}


def classify_user_prompt(message: str) -> str:
    """The user turn: a single message with no conversation history."""
    return f"Conversation so far:\n(no prior messages)\n\nMessage to classify:\n{message}"


@dataclass(frozen=True)
class LLMRoute:
    query: str  # what gets searched
    value: str  # the returned topic_en / query_en ("" if missing)
    intent: str | None
    fallback: str | None  # None, or why the raw Arabic was searched instead: "empty_field" / "llm_error"
    latency_s: float


class LLMRouter:
    remote = True

    def __init__(self, name: str, system: str, field_name: str, model_id: str,
                 price_in_per_1m: float, price_out_per_1m: float, min_interval_s: float):
        self.name = name
        self.system = system
        self.field_name = field_name
        self.model_id = model_id
        self.price_in_per_1m = price_in_per_1m
        self.price_out_per_1m = price_out_per_1m
        self.min_interval_s = min_interval_s  # client-side throttle for trial-key rate limits
        self.prompt_hash = hashlib.sha256(system.encode("utf-8")).hexdigest()[:12]
        self.refresh = False
        self.path = CACHE_DIR / "llm" / model_id / f"{name}.json"
        self._store: dict | None = None
        self._client = None
        self._last_call = 0.0
        self._calls = 0

    @property
    def store(self) -> dict:
        if self._store is None:
            read = self.path.exists() and not self.refresh
            self._store = json.loads(self.path.read_text(encoding="utf-8")) if read else {}
        return self._store

    def _key(self, message: str) -> str:
        return text_key(f"{self.model_id}|{self.prompt_hash}|{message}")

    def planned_calls(self, messages: list[str]) -> int:
        return len({self._key(m) for m in messages} - set(self.store))

    def _request(self, message: str) -> tuple[str, int | None, int | None]:
        if self._client is None:
            self._client = cohere_client()
        resp = self._client.chat(
            model=self.model_id,
            messages=[{"role": "system", "content": self.system},
                      {"role": "user", "content": classify_user_prompt(message)}],
            response_format={"type": "json_object"},
            temperature=0.0,
            max_tokens=400,
            request_options=NO_SDK_RETRIES,
        )
        billed = resp.usage.billed_units if resp.usage else None
        raw = resp.message.content[0].text if resp.message.content else ""
        return raw, getattr(billed, "input_tokens", None), getattr(billed, "output_tokens", None)

    def _call(self, message: str) -> dict:
        wait = self.min_interval_s - (time.monotonic() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        timing = {}

        def attempt():  # time only the attempt that succeeds, not backoff sleeps
            t0 = time.perf_counter()
            out = self._request(message)
            timing["latency_s"] = time.perf_counter() - t0
            return out

        raw, tokens_in, tokens_out = with_backoff(attempt, what=f"chat:{self.model_id}")
        self._last_call = time.monotonic()
        self._calls += 1
        if self._calls % 10 == 0:
            print(f"   [{self.name}] {self._calls} LLM calls made", flush=True)
        return {"message": message, "raw": raw, "latency_s": timing["latency_s"],
                "input_tokens": tokens_in, "output_tokens": tokens_out}

    def route(self, message: str) -> LLMRoute:
        k = self._key(message)
        if k not in self.store:
            self.store[k] = self._call(message)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.store, ensure_ascii=False, indent=1), encoding="utf-8")
        rec = self.store[k]

        try:
            parsed = json.loads(rec["raw"])
        except json.JSONDecodeError:
            return LLMRoute(message, "", None, "llm_error", rec["latency_s"])
        intent = parsed.get("intent")
        value = str(parsed.get(self.field_name) or "").strip()
        if intent not in VALID_INTENTS:
            return LLMRoute(message, value, intent, "llm_error", rec["latency_s"])
        # Search the returned string alone; fall back to the raw Arabic if it is empty.
        return LLMRoute(value or message, value, intent, None if value else "empty_field", rec["latency_s"])

    def mean_tokens(self) -> tuple[float, float] | None:
        recs = [r for r in self.store.values() if r.get("input_tokens") is not None]
        if not recs:
            return None
        return (sum(r["input_tokens"] for r in recs) / len(recs),
                sum(r["output_tokens"] or 0 for r in recs) / len(recs))

    def cost_per_1k(self) -> float | None:
        t = self.mean_tokens()
        if t is None:
            return None
        return 1000 * (t[0] * self.price_in_per_1m + t[1] * self.price_out_per_1m) / 1e6
