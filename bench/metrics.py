"""Retrieval metrics.

Recall@k here is "success@k": a question counts as a hit if ANY of its labelled relevant chunks
is in the top k. With one gold chunk per question this equals standard Recall@k; for the
multi-label (ambiguous) questions it is the lenient reading. MRR uses the first relevant hit.
"""

from __future__ import annotations

import numpy as np

KS = (1, 3, 5)


def first_relevant_rank(ranked_ids: list[str], relevant: set[str]) -> int | None:
    for i, cid in enumerate(ranked_ids, start=1):
        if cid in relevant:
            return i
    return None


def collapse_to_docs(ranked_chunk_ids: list[str]) -> list[str]:
    """Chunk ranking -> document ranking (a doc's rank = its best chunk's rank)."""
    return list(dict.fromkeys(cid.split("#", 1)[0] for cid in ranked_chunk_ids))


def summarize(ranks: list[int | None]) -> dict:
    r = np.array([x if x is not None else np.inf for x in ranks], dtype=float)
    out = {f"R@{k}": float(np.mean(r <= k)) for k in KS}
    out["MRR"] = float(np.mean(1.0 / r))
    out["n"] = len(ranks)
    return out


def random_expectation(n_items: int, relevant_counts: list[int]) -> dict:
    """Exact expected metrics for a uniformly random ranking, averaged over questions."""
    from math import comb

    rows = []
    for m in relevant_counts:
        # P(first relevant at rank r) = C(N-r, m-1) / C(N, m)
        p = [comb(n_items - r, m - 1) / comb(n_items, m) for r in range(1, n_items + 1)]
        row = {f"R@{k}": sum(p[:k]) for k in KS}
        row["MRR"] = sum(pr / r for r, pr in enumerate(p, start=1))
        rows.append(row)
    return {key: float(np.mean([r[key] for r in rows])) for key in rows[0]}


def reciprocal_ranks(ranks: list[int | None]) -> np.ndarray:
    return np.array([1.0 / x if x else 0.0 for x in ranks])


def bootstrap_ci(values: np.ndarray, n_boot: int = 10_000, seed: int = 0) -> tuple[float, float]:
    """95% percentile bootstrap CI of the mean, resampling questions."""
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(values), size=(n_boot, len(values)))
    means = values[idx].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(lo), float(hi)


def paired_diff(a: np.ndarray, b: np.ndarray, n_boot: int = 10_000, seed: int = 0) -> dict:
    """Mean of (b - a) over the same questions, with a paired 95% bootstrap CI."""
    d = b - a
    lo, hi = bootstrap_ci(d, n_boot, seed)
    return {"diff": float(d.mean()), "lo": lo, "hi": hi, "b_better": int((d > 0).sum()), "a_better": int((d < 0).sum())}
