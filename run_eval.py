"""Run every configuration over the same Arabic eval set and write results/.

    python run_eval.py --dry-run          # show what would hit the Cohere API, then stop
    python run_eval.py                    # run everything (asks before >20 uncached API calls)
    python run_eval.py --configs minilm-direct,minilm-router
    python run_eval.py --refresh          # ignore caches (re-embeds; costs API calls)
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import time
from pathlib import Path

import numpy as np

from bench import report
from bench.chunking import load_corpus
from bench.configs import CONFIGS, Config, get_llm, get_reranker
from bench.embedders import CACHE_DIR, ApiCallCounter, SentenceTransformerEmbedder, get_embedder, text_key
from bench.metrics import collapse_to_docs, first_relevant_rank
from bench.router import route_arabic

ROOT = Path(__file__).resolve().parent
REGISTERS = {"msa", "saudi", "terminology", "ambiguous"}
CONFIRM_ABOVE = 20  # uncached API calls


def load_questions(path: Path, chunk_ids: set[str]) -> list[dict]:
    qs = json.loads(path.read_text(encoding="utf-8"))["questions"]
    ids = [q["id"] for q in qs]
    problems = [f"duplicate id {i}" for i in {i for i in ids if ids.count(i) > 1}]
    for q in qs:
        if q["register"] not in REGISTERS:
            problems.append(f"{q['id']}: unknown register {q['register']!r}")
        if not q["relevant"]:
            problems.append(f"{q['id']}: no relevant chunks")
        problems += [f"{q['id']}: unknown chunk id {r!r}" for r in q["relevant"] if r not in chunk_ids]
    if problems:
        sys.exit("Invalid eval set:\n  " + "\n  ".join(problems))
    return qs


def latency_sample(questions: list[dict], n: int) -> list[dict]:
    """Evenly spaced subset, so the sample spans all registers."""
    if n <= 0:
        return []
    if n >= len(questions):
        return questions
    step = len(questions) / n
    return [questions[int(i * step)] for i in range(n)]


class LatencyCache:
    """Measured per-query API latencies, so re-runs do not re-spend calls on timing."""

    def __init__(self, name: str, read: bool):
        self.path = CACHE_DIR / "latency" / f"{name}.json"
        self.store = json.loads(self.path.read_text()) if read and self.path.exists() else {}

    def get(self, text: str) -> float | None:
        return self.store.get(text_key(text))

    def put(self, text: str, seconds: float) -> None:
        self.store[text_key(text)] = seconds
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.store, indent=1))


# --- planning -------------------------------------------------------------------------------


def plan_api_calls(configs: list[Config], chunks, questions, sample, refresh: bool) -> list[tuple[str, int]]:
    plan: dict[str, int] = {}
    for c in configs:
        if c.llm:
            llm = get_llm(c.llm)
            plan[f"{llm.model_id} ({llm.name}): one call per question (throttled {llm.min_interval_s}s)"] = (
                llm.planned_calls([q["question_ar"] for q in questions]))
    doc_texts = [c.text for c in chunks]
    for key in dict.fromkeys(c.embedder for c in configs):
        emb = get_embedder(key)
        if not emb.remote:
            continue
        users = [c for c in configs if c.embedder == key]
        if any(c.llm for c in users):
            # Planning would call prepare(), i.e. spend the LLM calls it is supposed to estimate.
            raise NotImplementedError("LLM-prepared queries with a remote embedder are not planned yet")
        q_texts = [c.prepare(q).text for c in users for q in questions]
        s_texts = [c.prepare(q).text for c in users for q in sample]
        lat = LatencyCache(emb.name, read=not refresh)
        plan[f"{emb.name}: embed corpus ({len(doc_texts)} chunks, batched)"] = emb.planned_calls(doc_texts, "document")
        plan[f"{emb.name}: embed queries (batched)"] = emb.planned_calls(q_texts, "query")
        plan[f"{emb.name}: single-query latency probes"] = len({text_key(t) for t in s_texts if lat.get(t) is None})
    for c in configs:
        if c.reranker:
            rr = get_reranker(c.reranker)
            plan[f"{rr.name}: one call per question (throttled {rr.min_interval_s}s)"] = rr.planned_calls(
                [c.prepare(q).text for q in questions]
            )
    return list(plan.items())


# --- running --------------------------------------------------------------------------------


def run_config(cfg: Config, chunks, questions, router_status) -> tuple[list[dict], dict[str, float]]:
    emb = get_embedder(cfg.embedder)
    D = emb.embed([c.text for c in chunks], "document")
    preps = [cfg.prepare(q) for q in questions]
    Q = emb.embed([p.text for p in preps], "query")
    order = np.argsort(-(Q @ D.T), axis=1, kind="stable")
    text_by_id = {c.id: c.text for c in chunks}

    records, rerank_latency = [], {}
    for i, (q, prep) in enumerate(zip(questions, preps)):
        ranked = [chunks[j].id for j in order[i]]
        if cfg.reranker:
            cand = ranked[: cfg.rerank_candidates]
            new, lat = get_reranker(cfg.reranker).rerank(prep.text, cand, [text_by_id[c] for c in cand])
            ranked = new + ranked[cfg.rerank_candidates :]
            rerank_latency[q["id"]] = lat
        relevant = set(q["relevant"])
        records.append(
            {
                "config": cfg.name,
                "qid": q["id"],
                "register": q["register"],
                "router_fell_back": router_status[q["id"]].fell_back,
                "query_text": prep.text,
                "prep_meta": prep.meta,
                "rank_section": first_relevant_rank(ranked, relevant),
                "rank_doc": first_relevant_rank(collapse_to_docs(ranked), {r.split("#")[0] for r in relevant}),
                "top5": ranked[:5],
            }
        )
    return records, rerank_latency


def measure_latency(cfg: Config, questions, sample, rerank_latency, refresh: bool) -> dict:
    """Median query-side latency: query prep + one single-query embed (+ rerank call)."""
    emb = get_embedder(cfg.embedder)
    if emb.remote:
        cache = LatencyCache(emb.name, read=not refresh)
        times = []
        for q in sample:
            prep = cfg.prepare(q)
            t = cache.get(prep.text)
            if t is None:
                t = emb.time_one(prep.text)
                cache.put(prep.text, t)
            times.append(prep.seconds + t + rerank_latency.get(q["id"], 0.0))
        where = "network round trip to Cohere, incl. TLS keep-alive reuse"
    else:
        # Full untimed pass first: torch/oneDNN on CPU takes tens of calls to reach steady state,
        # and without this whichever model runs first in the process looks ~2.5x slower.
        for q in questions:
            emb.time_one(cfg.prepare(q).text)
        times = []
        for q in questions:
            prep = cfg.prepare(q)
            times.append(prep.seconds + emb.time_one(prep.text))
        where = "local CPU"
    median = 1000 * statistics.median(times) if times else None
    return {"median_ms": median, "n": len(times), "where": where}


def cost_per_1k(cfg: Config) -> float | None:
    """Query-side API cost in USD per 1,000 queries (local compute not counted)."""
    cost = 0.0
    emb = get_embedder(cfg.embedder)
    if emb.remote:
        tokens = emb.mean_query_tokens()
        if tokens is None:
            return None
        cost += tokens * 1000 * emb.price_per_1m_tokens / 1e6
    if cfg.reranker:
        cost += get_reranker(cfg.reranker).price_per_1k_searches
    if cfg.llm:
        llm_cost = get_llm(cfg.llm).cost_per_1k()
        if llm_cost is None:
            return None
        cost += llm_cost
    return cost


def tokenizer_diagnostics(questions, chunks) -> dict:
    """Why English-only MiniLM fails on Arabic: what its tokenizer actually sees."""
    out = {}
    for key in ("minilm", "ml-minilm"):
        emb = get_embedder(key)
        if not isinstance(emb, SentenceTransformerEmbedder):
            continue
        tok = emb.model.tokenizer
        per_q = [tok.tokenize(q["question_ar"]) for q in questions]
        n_tok = sum(len(t) for t in per_q)
        unk = sum(t == tok.unk_token for ts in per_q for t in ts)
        truncated, longest, limit = emb.truncation_report([c.text for c in chunks])
        out[emb.name] = {
            "vocab_size": tok.vocab_size,
            "mean_tokens_per_question": n_tok / len(questions),
            "unk_rate": unk / n_tok,
            "examples": {q["id"]: tok.tokenize(q["question_ar"]) for q in questions if q["id"] in ("q01", "q27", "q38")},
            "chunks_truncated": truncated,
            "longest_chunk_tokens": longest,
            "max_seq_length": limit,
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--configs", help="comma-separated config names (default: all)")
    ap.add_argument("--latency-sample", type=int, default=20, help="single-query API calls per remote embedder")
    ap.add_argument("--dry-run", action="store_true", help="print the API call plan and exit")
    ap.add_argument("--yes", action="store_true", help="don't ask before spending API calls")
    ap.add_argument("--refresh", action="store_true", help="ignore all caches")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    chunks = load_corpus(ROOT / "knowledge")
    questions = load_questions(ROOT / "eval" / "questions_ar.json", {c.id for c in chunks})
    configs = CONFIGS
    if args.configs:
        wanted = args.configs.split(",")
        unknown = set(wanted) - {c.name for c in CONFIGS}
        if unknown:
            sys.exit(f"Unknown config(s): {sorted(unknown)}. Known: {[c.name for c in CONFIGS]}")
        configs = [c for c in CONFIGS if c.name in wanted]

    for c in configs:
        get_embedder(c.embedder).refresh = args.refresh
        if c.reranker:
            get_reranker(c.reranker).refresh = args.refresh
        if c.llm:
            get_llm(c.llm).refresh = args.refresh

    router_status = {q["id"]: route_arabic(q["question_ar"]) for q in questions}
    sample = latency_sample(questions, args.latency_sample)
    print(f"{len(chunks)} chunks, {len(questions)} questions, {len(configs)} configs")

    plan = plan_api_calls(configs, chunks, questions, sample, args.refresh)
    total = sum(n for _, n in plan)
    if plan:
        print("\nAPI calls this run would make (uncached only):")
        for what, n in plan:
            print(f"  {n:4d}  {what}")
        print(f"  {total:4d}  TOTAL  (Cohere trial keys: 1,000 calls/month across embed, rerank and chat)")
    if args.dry_run:
        return
    if total > CONFIRM_ABOVE and not args.yes:
        if input(f"\nThis will make {total} API calls. Continue? [y/N] ").strip().lower() != "y":
            sys.exit("Aborted; nothing was sent.")

    records, latency, cost = [], {}, {}
    for cfg in configs:
        t0 = time.perf_counter()
        print(f"\n== {cfg.name}: {cfg.description}")
        recs, rerank_latency = run_config(cfg, chunks, questions, router_status)
        records += recs
        latency[cfg.name] = measure_latency(cfg, questions, sample, rerank_latency, args.refresh)
        cost[cfg.name] = cost_per_1k(cfg)
        hits = sum(1 for r in recs if r["rank_section"] and r["rank_section"] <= 3)
        med = latency[cfg.name]["median_ms"]
        lat_s = f"{med:.1f} ms" if med is not None else "not measured"
        print(f"   R@3 {hits}/{len(recs)}   median latency {lat_s}   ({time.perf_counter() - t0:.0f}s)")

    diag = tokenizer_diagnostics(questions, chunks)
    env = {
        "python": platform.python_version(),
        "machine": f"{platform.system()} {platform.release()}, {platform.processor() or platform.machine()}",
        "api_calls_made": ApiCallCounter.calls,
    }
    out = ROOT / args.out
    report.write_all(out, configs, questions, chunks, records, latency, cost, router_status, diag, env)
    print(f"\nAPI calls made this run: {ApiCallCounter.calls or 'none (all cached)'}")
    print(f"Wrote {out}/results.md, chart.png, disagreements.md, per_query.jsonl")


if __name__ == "__main__":
    main()
