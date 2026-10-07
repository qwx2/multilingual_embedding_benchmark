"""Embedding backends behind one interface, with an on-disk vector cache.

To add a model: subclass `Embedder` (implement `_embed`), or for any sentence-transformers
checkpoint just add a line to `EMBEDDERS`. Then reference it from a config in `configs.py`.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal

import numpy as np

Role = Literal["query", "document"]
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"


def text_key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:32]


def normalize(m: np.ndarray) -> np.ndarray:
    return m / np.linalg.norm(m, axis=1, keepdims=True)


class ApiCallCounter:
    """Counts real network calls so each run can report what it actually spent."""

    calls: dict[str, int] = {}

    @classmethod
    def add(cls, what: str, n: int = 1) -> None:
        cls.calls[what] = cls.calls.get(what, 0) + n


class VectorCache:
    """text-hash -> vector for one (model, role). One .npz per pair."""

    def __init__(self, path: Path, read: bool = True):
        self.path = path
        self.store: dict[str, np.ndarray] = {}
        if read and path.exists():
            with np.load(path) as f:
                self.store = {k: f[k] for k in f.files}

    def missing(self, texts: list[str]) -> list[str]:
        seen, out = set(), []
        for t in texts:
            k = text_key(t)
            if k not in self.store and k not in seen:
                seen.add(k)
                out.append(t)
        return out

    def put(self, texts: list[str], vecs: np.ndarray) -> None:
        for t, v in zip(texts, vecs):
            self.store[text_key(t)] = v.astype(np.float32)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(self.path, **self.store)

    def get(self, texts: list[str]) -> np.ndarray:
        return np.stack([self.store[text_key(t)] for t in texts])


class Embedder(ABC):
    name: str  # used in cache paths and reports
    remote: bool = False
    batch_size: int = 64
    price_per_1m_tokens: float = 0.0  # USD; 0 for local models

    def __init__(self) -> None:
        self.refresh = False
        self._caches: dict[Role, VectorCache] = {}

    @abstractmethod
    def _embed(self, texts: list[str], role: Role) -> np.ndarray:
        """Embed one batch (len <= batch_size). Return raw vectors, one row per text."""

    def cache(self, role: Role) -> VectorCache:
        if role not in self._caches:
            path = CACHE_DIR / "vectors" / self.name.replace("/", "__") / f"{role}.npz"
            self._caches[role] = VectorCache(path, read=not self.refresh)
        return self._caches[role]

    def planned_calls(self, texts: list[str], role: Role) -> int:
        n = len(self.cache(role).missing(texts))
        return -(-n // self.batch_size) if self.remote else 0

    def embed(self, texts: list[str], role: Role) -> np.ndarray:
        """L2-normalised vectors for `texts`; only texts not already on disk are embedded."""
        cache = self.cache(role)
        todo = cache.missing(texts)
        for i in range(0, len(todo), self.batch_size):
            batch = todo[i : i + self.batch_size]
            cache.put(batch, self._embed(batch, role))
        return normalize(cache.get(texts))

    def time_one(self, text: str) -> float:
        """Wall-clock seconds to embed one query, bypassing the cache."""
        t0 = time.perf_counter()
        self._embed([text], "query")
        return time.perf_counter() - t0


# --- local models ---------------------------------------------------------------------------


class SentenceTransformerEmbedder(Embedder):
    """Any sentence-transformers checkpoint, run on CPU at its default max_seq_length."""

    def __init__(self, model_id: str):
        super().__init__()
        self.name = model_id
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.name, device="cpu")
        return self._model

    def _embed(self, texts: list[str], role: Role) -> np.ndarray:
        # The benchmark's MiniLM variants are symmetric models: no query/document prefix.
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

    def truncation_report(self, texts: list[str]) -> tuple[int, int, int]:
        """(n_truncated, max_tokens_seen, max_seq_length) for these texts."""
        tok, limit = self.model.tokenizer, self.model.max_seq_length
        lengths = [len(tok(t, add_special_tokens=True)["input_ids"]) for t in texts]
        return sum(n > limit for n in lengths), max(lengths), limit


# --- Cohere ---------------------------------------------------------------------------------

_RETRYABLE = {429, 500, 502, 503, 504}
# The SDK retries silently by default; disable that so `with_backoff` is the only retry path
# and ApiCallCounter reflects every request actually sent.
NO_SDK_RETRIES = {"max_retries": 0}


def with_backoff(fn, *, what: str, max_tries: int = 6, base: float = 2.0):
    """Call fn(); on rate-limit / transient errors retry with exponential backoff + jitter."""
    for attempt in range(1, max_tries + 1):
        try:
            ApiCallCounter.add(what)
            return fn()
        except Exception as e:  # cohere raises typed ApiError subclasses carrying status_code
            status = getattr(e, "status_code", None)
            transient = status in _RETRYABLE or type(e).__name__ in {
                "ConnectError",
                "ReadTimeout",
                "RemoteProtocolError",
            }
            if not transient or attempt == max_tries:
                raise
            delay = base * 2 ** (attempt - 1) + random.uniform(0, 1)
            print(f"  [{what}] HTTP {status or type(e).__name__}; retry {attempt} in {delay:.1f}s")
            time.sleep(delay)


def cohere_client():
    import cohere
    from dotenv import load_dotenv

    load_dotenv()
    key = os.environ.get("COHERE_API_KEY")
    if not key:
        raise RuntimeError("COHERE_API_KEY is not set (expected in .env)")
    return cohere.ClientV2(api_key=key)


class CohereEmbedder(Embedder):
    remote = True
    batch_size = 96  # API maximum texts per call

    # input_type differs by role; using the wrong one does not error, it just retrieves worse.
    INPUT_TYPE = {"query": "search_query", "document": "search_document"}

    def __init__(self, model_id: str, price_per_1m_tokens: float, output_dimension: int | None = None):
        super().__init__()
        self.model_id = model_id
        self.output_dimension = output_dimension
        self.name = f"{model_id}-d{output_dimension}" if output_dimension else model_id
        self.price_per_1m_tokens = price_per_1m_tokens
        self._client = None
        self.usage_path = CACHE_DIR / "vectors" / self.name / "usage.json"

    @property
    def client(self):
        if self._client is None:
            self._client = cohere_client()
        return self._client

    def _embed(self, texts: list[str], role: Role) -> np.ndarray:
        kwargs = dict(
            texts=texts,
            model=self.model_id,
            input_type=self.INPUT_TYPE[role],
            embedding_types=["float"],
            request_options=NO_SDK_RETRIES,
        )
        if self.output_dimension:
            kwargs["output_dimension"] = self.output_dimension
        resp = with_backoff(lambda: self.client.embed(**kwargs), what=f"embed:{self.model_id}")
        self._record_usage(role, len(texts), resp)
        return np.asarray(resp.embeddings.float_, dtype=np.float32)

    def _record_usage(self, role: Role, n_texts: int, resp) -> None:
        billed = getattr(getattr(resp.meta, "billed_units", None), "input_tokens", None)
        if billed is None:
            return
        usage = self.usage()
        u = usage.setdefault(role, {"texts": 0, "tokens": 0})
        u["texts"] += n_texts
        u["tokens"] += int(billed)
        self.usage_path.parent.mkdir(parents=True, exist_ok=True)
        self.usage_path.write_text(json.dumps(usage, indent=2))

    def usage(self) -> dict:
        return json.loads(self.usage_path.read_text()) if self.usage_path.exists() else {}

    def mean_query_tokens(self) -> float | None:
        u = self.usage().get("query")
        return u["tokens"] / u["texts"] if u and u["texts"] else None


# --- registry -------------------------------------------------------------------------------

# Prices: Embed v4 text input, $0.12 / 1M tokens (third-party pricing trackers, June 2026;
# cohere.com/pricing no longer lists per-token rates -- verify before quoting).
# Embed 5 (released 2026-09-30): Pro $0.12 / 1M, Fast $0.08 / 1M (third-party, Oct 2026 -- verify).
# Both v5 tiers run at 1024 dims, the same as v4, so differences come from the model, not the size.
EMBEDDERS: dict[str, callable] = {
    "minilm": lambda: SentenceTransformerEmbedder("sentence-transformers/all-MiniLM-L6-v2"),
    "ml-minilm": lambda: SentenceTransformerEmbedder(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ),
    "cohere-v4": lambda: CohereEmbedder("embed-v4.0", price_per_1m_tokens=0.12, output_dimension=1024),
    "cohere-v5-pro": lambda: CohereEmbedder("embed-v5.0-pro", price_per_1m_tokens=0.12, output_dimension=1024),
    "cohere-v5-fast": lambda: CohereEmbedder("embed-v5.0-fast", price_per_1m_tokens=0.08, output_dimension=1024),
}

_instances: dict[str, Embedder] = {}


def get_embedder(key: str) -> Embedder:
    if key not in _instances:
        _instances[key] = EMBEDDERS[key]()
    return _instances[key]
