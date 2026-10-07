"""LLM query rewriting: one JSON-mode call that classifies intent and returns an English string.

Two variants of the same call:

- CLASSIFY_SYSTEM asks for `topic_en`, "3-8 ENGLISH keywords
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

from .embedders import CACHE_DIR, NO_SDK_RETRIES, cohere_client, text_key, with_backoff

# The exact system prompt used for the cached results. Editing it changes the cache key and
# means re-running the LLM calls.
CLASSIFY_SYSTEM = """You are the intent router for Twin, a Saudi personal-finance assistant.

Classify the user's message and extract any purchase details. Reply with JSON only:

{
  "intent": "purchase_simulation" | "financial_question" | "product_advice" | "chitchat",
  "item": string | null,            // what is being bought, 1-3 words, lowercase ("car", "iphone", "gym subscription")
  "price": number | null,           // amount in SAR, digits only. "120k" -> 120000
  "recurring": boolean,             // true if this is a per-month commitment, not a one-off
  "financing_option": string | null,// "cash" | "finance" | "wait" if the user named one
  "income_change_pct": number | null,// e.g. -20 for "what if my salary drops 20%"
  "topic_en": string                 // 3-8 ENGLISH keywords describing the topic, ALWAYS
                                     // in English even for Arabic messages. Used to search
                                     // an English knowledge base.
                                     // e.g. "buying a car cash vs murabaha financing"
}

Rules:
- purchase_simulation: the user is considering spending money, asking whether they can
  afford something, comparing paying cash vs financing, asking to delay a purchase, or
  asking what happens if their income changes. Anything with a price or an income change.
- financial_question: general advice with no specific transaction (zakat, budgeting,
  emergency funds, how murabaha works).
- product_advice: the user asks which bank/Alinma products suit them, or asks to see or
  compare Alinma's products (savings account, financing, credit cards), with no specific
  transaction to simulate. "What Alinma products are good for me?" is product_advice; a
  question with a price stays purchase_simulation.
- chitchat: greetings, thanks, "who are you", small talk.
- Resolve references against the conversation history. If the user says "what if I wait
  six months?" and a 120000 SAR car was just discussed, return that item and price with
  financing_option "wait".
- "300 SAR per month" / "monthly subscription" -> recurring: true, price: 300.
- Never guess a price that was not stated or previously discussed. Use null.

The message may be in English or Arabic. Classify Arabic exactly the same way, and return
`item` in the SAME language the user wrote in ("سيارة" for an Arabic message, "car" for an
English one)   it is shown back to them. Prices are always plain digits: "120 ألف" -> 120000.
"""

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
    raise RuntimeError("topic_en block not found verbatim in CLASSIFY_SYSTEM")
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
