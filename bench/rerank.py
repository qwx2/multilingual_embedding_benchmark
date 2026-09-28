"""Cohere Rerank over a dense retriever's top-N candidates, cached per (query, candidate set)."""

from __future__ import annotations

import json
import time

from .embedders import CACHE_DIR, NO_SDK_RETRIES, cohere_client, text_key, with_backoff


class CohereReranker:
    remote = True

    def __init__(self, model_id: str, price_per_1k_searches: float, min_interval_s: float):
        self.model_id = model_id
        self.name = model_id
        self.price_per_1k_searches = price_per_1k_searches
        self.min_interval_s = min_interval_s  # client-side throttle for trial-key rate limits
        self.refresh = False
        self._client = None
        self._last_call = 0.0
        self.path = CACHE_DIR / "rerank" / f"{model_id}.json"
        self._store: dict | None = None

    @property
    def store(self) -> dict:
        if self._store is None:
            read = self.path.exists() and not self.refresh
            self._store = json.loads(self.path.read_text(encoding="utf-8")) if read else {}
        return self._store

    def planned_calls(self, queries: list[str]) -> int:
        return len({text_key(q) for q in queries} - set(self.store))

    def rerank(self, query: str, candidate_ids: list[str], candidate_texts: list[str]) -> tuple[list[str], float]:
        """Return (candidate ids reordered by relevance, API latency in seconds)."""
        k = text_key(query)
        hit = self.store.get(k)
        if hit and hit["candidates"] == candidate_ids:
            return hit["order"], hit["latency_s"]

        if self._client is None:
            self._client = cohere_client()
        wait = self.min_interval_s - (time.monotonic() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        t0 = time.perf_counter()
        resp = with_backoff(
            lambda: self._client.rerank(
                model=self.model_id,
                query=query,
                documents=candidate_texts,
                top_n=len(candidate_texts),
                request_options=NO_SDK_RETRIES,
            ),
            what=f"rerank:{self.model_id}",
        )
        latency = time.perf_counter() - t0
        self._last_call = time.monotonic()

        order = [candidate_ids[r.index] for r in resp.results]
        self.store[k] = {"candidates": candidate_ids, "order": order, "latency_s": latency}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.store, ensure_ascii=False, indent=1), encoding="utf-8")
        return order, latency
