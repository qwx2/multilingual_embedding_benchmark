"""The configurations under test. Adding one = adding an entry to CONFIGS.

A config is: how to turn an eval question into query text -> which embedder -> optional reranker.
Rows are ordered by *what text gets searched*, so the table separates the two questions
"which embedder?" and "search the question, or a topic label?".
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

from .llm_router import CLASSIFY_SYSTEM, TRANSLATE_SYSTEM, LLMRouter
from .rerank import CohereReranker
from .router import route_arabic


@dataclass(frozen=True)
class QueryPrep:
    text: str  # what gets embedded
    seconds: float = 0.0  # time spent producing it (routing / LLM call), counted in latency
    meta: dict = field(default_factory=dict)


def arabic(q: dict) -> QueryPrep:
    return QueryPrep(q["question_ar"])


def gold_english(q: dict) -> QueryPrep:
    # Ceiling for any translate-first approach: a human translation, free and instant.
    return QueryPrep(q["gold_en"])


def keyword_router(q: dict) -> QueryPrep:
    t0 = time.perf_counter()
    r = route_arabic(q["question_ar"])
    dt = time.perf_counter() - t0
    return QueryPrep(r.query, dt, {"topic": r.topic, "matched_keys": list(r.matched_keys), "fell_back": r.fell_back})


def via_llm(key: str) -> Callable[[dict], QueryPrep]:
    """Query text from an LLM routing call (cached; the first run makes one API call per question)."""

    def prep(q: dict) -> QueryPrep:
        llm = get_llm(key)
        r = llm.route(q["question_ar"])
        meta = {"llm_model": llm.model_id, "llm_value": r.value, "intent": r.intent, "llm_fallback": r.fallback}
        return QueryPrep(r.query, r.latency_s, meta)

    return prep


@dataclass(frozen=True)
class Config:
    name: str
    searches: str  # what text is embedded on the query side, for the results table
    description: str
    embedder: str  # key in embedders.EMBEDDERS
    prepare: Callable[[dict], QueryPrep]
    reranker: str | None = None  # key in RERANKERS
    rerank_candidates: int = 20
    llm: str | None = None  # key in LLMS, if prepare() makes an LLM call


CONFIGS: list[Config] = [
    Config("minilm-direct", "full question — raw Arabic (unreadable to this model)",
           "Baseline: Arabic query -> all-MiniLM-L6-v2 (English-only)", "minilm", arabic),
    Config("minilm-router", "topic label — keyword map",
           "Keyword router: Arabic -> keyword-map topic -> MiniLM", "minilm", keyword_router),
    Config("minilm-llm-topic", "topic label — LLM topic_en",
           "LLM router: command-a-03-2025 classify call -> topic_en -> MiniLM", "minilm",
           via_llm("llm-topic"), llm="llm-topic"),
    Config("minilm-llm-translation", "full question — LLM translation",
           "Same LLM call with topic_en swapped for a faithful translation -> MiniLM", "minilm",
           via_llm("llm-translation"), llm="llm-translation"),
    Config("minilm-gold-en", "full question — human translation",
           "Ceiling for translate-first: human English translation -> MiniLM", "minilm", gold_english),
    Config("ml-minilm-direct", "full question — raw Arabic",
           "Free multilingual: Arabic -> paraphrase-multilingual-MiniLM-L12-v2", "ml-minilm", arabic),
    Config("cohere-v4-direct", "full question — raw Arabic",
           "Cohere: Arabic -> embed-v4.0 (search_query) vs chunks (search_document)", "cohere-v4", arabic),
    Config("cohere-v5-pro-direct", "full question — raw Arabic",
           "Cohere: Arabic -> embed-v5.0-pro (search_query) vs chunks (search_document)", "cohere-v5-pro", arabic),
    Config("cohere-v5-fast-direct", "full question — raw Arabic",
           "Cohere: Arabic -> embed-v5.0-fast (search_query) vs chunks (search_document)", "cohere-v5-fast", arabic),
    Config("cohere-v4-rerank", "full question — raw Arabic",
           "Cohere embed-v4.0 top-20 -> rerank-v4.0-fast", "cohere-v4", arabic, reranker="rerank-fast"),
]

# Rerank 4 Fast: $2.00 / 1K searches (a search = 1 query + up to 100 docs); third-party pricing
# trackers, June 2026 -- verify. Trial keys allow 10 rerank calls/min, hence the 6.5 s throttle.
RERANKERS: dict[str, Callable[[], CohereReranker]] = {
    "rerank-fast": lambda: CohereReranker("rerank-v4.0-fast", price_per_1k_searches=2.00, min_interval_s=6.5),
}

# Cohere command-a-03-2025: $2.50 / 1M input, $10 / 1M output (third-party pricing trackers,
# 2026 -- verify). Trial keys allow 20 chat calls/min, hence the 3.2 s throttle.
LLMS: dict[str, Callable[[], LLMRouter]] = {
    "llm-topic": lambda: LLMRouter("llm-topic", CLASSIFY_SYSTEM, "topic_en", "command-a-03-2025",
                                   2.50, 10.00, min_interval_s=3.2),
    "llm-translation": lambda: LLMRouter("llm-translation", TRANSLATE_SYSTEM, "query_en", "command-a-03-2025",
                                         2.50, 10.00, min_interval_s=3.2),
}

_rerankers: dict[str, CohereReranker] = {}
_llms: dict[str, LLMRouter] = {}


def get_reranker(key: str) -> CohereReranker:
    if key not in _rerankers:
        _rerankers[key] = RERANKERS[key]()
    return _rerankers[key]


def get_llm(key: str) -> LLMRouter:
    if key not in _llms:
        _llms[key] = LLMS[key]()
    return _llms[key]
