"""Deterministic Arabic keyword router: Arabic keywords -> an English topic string.

Matching is by substring (`if ar in text`). The English terms of every matched key are joined and
deduplicated in order, and that topic string is searched instead of the question. If nothing
matches, the raw Arabic message is searched (`topic or message`). `route_arabic` also reports
which keys matched, so the harness can separate queries the router handled from queries that
silently fell back to raw Arabic.
"""

from __future__ import annotations

from dataclasses import dataclass

_AR_TOPIC_HINTS = {
    "سيارة": "car vehicle",
    "سياره": "car vehicle",
    "تمويل": "financing loan",
    "مرابحة": "murabaha islamic financing",
    "قسط": "installment financing",
    "أقساط": "installment financing",
    "قرض": "loan debt",
    "زكاة": "zakat",
    "طوارئ": "emergency fund",
    "ادخار": "saving savings",
    "ادّخار": "saving savings",
    "مدخرات": "savings",
    "ميزانية": "budgeting budget",
    "راتب": "salary income",
    "دخل": "income salary",
    "اشتراك": "subscription recurring cost",
    "استثمار": "investing investment",
    "دين": "debt",
    "ديون": "debt",
    "تقاعد": "retirement planning",
    "حلال": "islamic finance halal",
    "ربا": "riba interest islamic finance",
    "إسلامي": "islamic finance",
    "عمرة": "goal saving umrah",
    "هدف": "goal planning",
    "بيت": "home property",
    "شقة": "apartment property",
}


def _topic_hints_ar(text: str) -> str:
    hits = [en for ar, en in _AR_TOPIC_HINTS.items() if ar in text]
    return " ".join(dict.fromkeys(" ".join(hits).split()))



@dataclass(frozen=True)
class RouteResult:
    query: str  # what gets sent to the retriever
    topic: str  # English topic string ("" if nothing matched)
    matched_keys: tuple[str, ...]  # Arabic keys that substring-matched

    @property
    def fell_back(self) -> bool:
        """True when no keyword matched and the raw Arabic went to MiniLM (== baseline)."""
        return not self.topic


def route_arabic(message: str) -> RouteResult:
    topic = _topic_hints_ar(message)
    matched = tuple(ar for ar in _AR_TOPIC_HINTS if ar in message)
    # Search the topic string alone; fall back to the raw Arabic if nothing matched.
    return RouteResult(query=topic or message, topic=topic, matched_keys=matched)
