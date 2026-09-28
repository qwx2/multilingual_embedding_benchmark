"""Everything written to results/: tables, chart, disagreement report, per-query dump."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import numpy as np

from .metrics import KS, bootstrap_ci, paired_diff, random_expectation, reciprocal_ranks, summarize

# Paired comparisons worth reporting, as (a, b): "how much better is b than a?"
PAIRS = [
    # Routing layer, embedder held fixed (MiniLM)
    ("minilm-direct", "minilm-router"),
    ("minilm-router", "minilm-llm-topic"),
    ("minilm-llm-topic", "minilm-llm-translation"),  # topic label vs question: same LLM call, one field
    ("minilm-llm-translation", "minilm-gold-en"),  # machine vs human translation
    # Embedding layer, full question held fixed
    ("minilm-llm-topic", "cohere-v4-direct"),  # LLM topic label vs multilingual embedder
    ("minilm-llm-translation", "cohere-v4-direct"),  # routing-layer fix vs embedding-layer fix
    ("minilm-gold-en", "cohere-v4-direct"),
    ("ml-minilm-direct", "cohere-v4-direct"),
    ("cohere-v4-direct", "cohere-v4-rerank"),
]

# The disagreement report files each question under the FIRST of these pairs that disagrees on it
# (hit@3 in one config, miss in the other); pairs whose configs were not run are skipped.
FOCUS_PAIRS = [
    ("minilm-llm-topic", "minilm-llm-translation"),  # topic label vs question, same LLM call
    ("minilm-router", "minilm-llm-topic"),  # keyword-map label vs LLM label
    ("minilm-llm-topic", "cohere-v4-direct"),  # LLM topic label vs multilingual embedder
    ("minilm-router", "cohere-v4-direct"),
]


def _by_config(records):
    out: dict[str, list[dict]] = {}
    for r in records:
        out.setdefault(r["config"], []).append(r)
    return out


def _fmt(x: float) -> str:
    return f"{x:.2f}"


def _pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def _hit(r: dict, k: int = 3) -> bool:
    return r["rank_section"] is not None and r["rank_section"] <= k


# --- results.md -----------------------------------------------------------------------------


def results_markdown(configs, questions, chunks, records, latency, cost, router_status, diag, env) -> str:
    by = _by_config(records)
    names = [c.name for c in configs]
    n_fb = sum(s.fell_back for s in router_status.values())
    n_q = len(questions)
    L = [
        "# Results",
        "",
        f"Generated {date.today().isoformat()} by `run_eval.py`. {len(chunks)} chunks, {n_q} Arabic questions.",
        "",
        "Recall@k = share of questions with at least one labelled relevant chunk in the top k. "
        "MRR uses the first relevant chunk. 95% CIs are percentile bootstraps over questions (10k resamples).",
        "",
        "## Section-level retrieval (headline)",
        "",
        "Rows are ordered by what text is embedded on the query side.",
        "",
        "| Config | Searched text | R@1 | R@3 | R@5 | MRR | MRR 95% CI | Median latency | Cost / 1k queries |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    def row(label, recs, lat=None, cst=None, searched=""):
        s = summarize([r["rank_section"] for r in recs])
        lo, hi = bootstrap_ci(reciprocal_ranks([r["rank_section"] for r in recs]))
        if not lat:
            lat_s = ""
        elif lat["median_ms"] is None:
            lat_s = "not measured"
        else:
            lat_s = f"{lat['median_ms']:.1f} ms (n={lat['n']})"
        cst_s = "" if cst is False else ("n/a" if cst is None else f"${cst:.4f}" if cst < 0.1 else f"${cst:.2f}")
        return (f"| {label} | {searched} | {_pct(s['R@1'])} | {_pct(s['R@3'])} | {_pct(s['R@5'])} | {_fmt(s['MRR'])} "
                f"| {_fmt(lo)}–{_fmt(hi)} | {lat_s} | {cst_s} |")

    for c in configs:
        L.append(row(f"`{c.name}`", by[c.name], latency[c.name], cost[c.name], c.searches))
        if c.name == "minilm-router":
            recs = by[c.name]
            L.append(row(f"&nbsp;&nbsp;↳ keyword matched (n={n_q - n_fb})",
                         [r for r in recs if not r["router_fell_back"]], cst=False))
            L.append(row(f"&nbsp;&nbsp;↳ no keyword → raw Arabic fallback (n={n_fb})",
                         [r for r in recs if r["router_fell_back"]], cst=False))
    rnd = random_expectation(len(chunks), [len(q["relevant"]) for q in questions])
    L.append(f"| *random ranking (expected)* | | {_pct(rnd['R@1'])} | {_pct(rnd['R@3'])} | {_pct(rnd['R@5'])} "
             f"| {_fmt(rnd['MRR'])} | | | |")
    L += [
        "",
        "Latency: local models are timed on CPU per single query after warm-up; Cohere is one "
        "single-query HTTPS call per sample (network round trip included), so the two are not "
        "like-for-like. The rerank row adds the rerank call to the embed call. LLM rows include the "
        "measured LLM call (Cohere command-a-03-2025) plus the local embed. "
        "Cost excludes local compute and the one-time corpus embedding.",
        "",
        "Configs:",
        "",
    ]
    L += [f"- `{c.name}` — {c.description}" for c in configs]

    # --- LLM routing diagnostics
    llm_cfgs = [c for c in configs if c.llm]
    if llm_cfgs:
        L += ["", "## LLM routing diagnostics", "",
              "| Config | LLM | Intents returned | Fell back to raw Arabic |",
              "|---|---|---|---|"]
        for c in llm_cfgs:
            metas = [r["prep_meta"] for r in by[c.name]]
            intents: dict[str, int] = {}
            for m in metas:
                intents[str(m["intent"])] = intents.get(str(m["intent"]), 0) + 1
            fb: dict[str, list[str]] = {}
            for r in by[c.name]:
                if r["prep_meta"]["llm_fallback"]:
                    fb.setdefault(r["prep_meta"]["llm_fallback"], []).append(r["qid"])
            models = ", ".join(sorted({f"`{m['llm_model']}`" for m in metas}))
            L.append(f"| `{c.name}` | {models} | {', '.join(f'{k}: {v}' for k, v in sorted(intents.items()))} "
                     f"| {'; '.join(f'{k}: {', '.join(v)}' for k, v in fb.items()) or 'none'} |")
        L += ["",
              "Fell back: `empty_field` = no topic/translation returned; `llm_error` = unparseable "
              "JSON or an unknown intent. In both cases the raw Arabic question is searched."]

    # --- router split across every config
    L += [
        "",
        "## Split by whether the keyword router matched a keyword",
        "",
        f"The router matched at least one keyword on {n_q - n_fb}/{n_q} questions and fell back to the "
        f"raw Arabic message on {n_fb}/{n_q}. Note: the eval set deliberately includes out-of-map "
        "vocabulary, so this fallback rate describes this eval set, not real-world traffic.",
        "",
        f"| Config | Matched R@1 | Matched R@3 | Matched MRR | Fallback R@1 | Fallback R@3 | Fallback MRR |",
        "|---|---|---|---|---|---|---|",
    ]
    for name in names:
        m = summarize([r["rank_section"] for r in by[name] if not r["router_fell_back"]])
        f = summarize([r["rank_section"] for r in by[name] if r["router_fell_back"]])
        L.append(f"| `{name}` | {_pct(m['R@1'])} | {_pct(m['R@3'])} | {_fmt(m['MRR'])} "
                 f"| {_pct(f['R@1'])} | {_pct(f['R@3'])} | {_fmt(f['MRR'])} |")

    fb_ids = [q["id"] for q in questions if router_status[q["id"]].fell_back]
    L += ["", f"Fallback questions: {', '.join(fb_ids)}"]

    # --- paired comparisons
    L += [
        "",
        "## Paired comparisons (section-level MRR, same questions)",
        "",
        "| A → B | ΔMRR (B − A) | 95% CI | B better / A better (questions) |",
        "|---|---|---|---|",
    ]
    for a, b in PAIRS:
        if a in by and b in by:
            ra = reciprocal_ranks([r["rank_section"] for r in by[a]])
            rb = reciprocal_ranks([r["rank_section"] for r in by[b]])
            d = paired_diff(ra, rb)
            L.append(f"| `{a}` → `{b}` | {d['diff']:+.2f} | {d['lo']:+.2f} to {d['hi']:+.2f} "
                     f"| {d['b_better']} / {d['a_better']} |")

    # --- by register
    regs = ["msa", "saudi", "terminology", "ambiguous"]
    counts = {g: sum(q["register"] == g for q in questions) for g in regs}
    L += ["", "## Section-level R@3 by register", "",
          "| Config | " + " | ".join(f"{g} (n={counts[g]})" for g in regs) + " |",
          "|---|" + "---|" * len(regs)]
    for name in names:
        cells = []
        for g in regs:
            recs = [r for r in by[name] if r["register"] == g]
            cells.append(_pct(summarize([r["rank_section"] for r in recs])["R@3"]))
        L.append(f"| `{name}` | " + " | ".join(cells) + " |")

    # --- document level
    L += ["", "## Document-level retrieval (secondary)", "",
          "Right *file* anywhere in the top k. With only 7 documents this saturates quickly.", "",
          "| Config | R@1 | R@3 | R@5 | MRR |", "|---|---|---|---|---|"]
    for name in names:
        s = summarize([r["rank_doc"] for r in by[name]])
        L.append(f"| `{name}` | {_pct(s['R@1'])} | {_pct(s['R@3'])} | {_pct(s['R@5'])} | {_fmt(s['MRR'])} |")

    # --- tokenizer diagnostics
    if diag:
        L += ["", "## What the local models' tokenizers see", "",
              "| Model | Vocab | Mean tokens / Arabic question | `[UNK]` rate | Chunks truncated (max_seq_length) |",
              "|---|---|---|---|---|"]
        for model, d in diag.items():
            L.append(f"| `{model}` | {d['vocab_size']:,} | {d['mean_tokens_per_question']:.1f} | "
                     f"{_pct(d['unk_rate'])} | {d['chunks_truncated']}/{len(chunks)} "
                     f"(limit {d['max_seq_length']}, longest {d['longest_chunk_tokens']}) |")
        L += ["", "Example tokenizations:", ""]
        qtext = {q["id"]: q["question_ar"] for q in questions}
        for model, d in diag.items():
            for qid, toks in d["examples"].items():
                L.append(f"- `{model}` · {qid} `{qtext[qid]}` → `{' '.join(toks)}`")

    L += ["", "## Run environment", "", f"- Python {env['python']}, {env['machine']}",
          f"- Cohere API calls made in the run that produced this file: {env['api_calls_made'] or 'none (all cached)'}"]
    return "\n".join(L) + "\n"


# --- chart ----------------------------------------------------------------------------------

# Reference data-viz palette (light surface), categorical slots 1-3 in fixed order.
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]


def write_chart(path: Path, configs, records) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    by = _by_config(records)
    names = [c.name for c in configs][::-1]  # top-to-bottom in config order
    y = np.arange(len(names))

    plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10})
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 0.55 * len(names) + 2.2), sharey=True,
                                 gridspec_kw={"wspace": 0.08})
    fig.patch.set_facecolor(SURFACE)

    def style(ax, title):
        ax.set_facecolor(SURFACE)
        ax.set_xlim(-0.02, 1.02)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0%", "25%", "50%", "75%", "100%"])
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(AXIS)
        ax.tick_params(colors=MUTED, length=0)
        ax.set_title(title, loc="left", color=INK, fontsize=11, pad=10)

    # Panel 1: R@1 / R@3 / R@5 per config
    for k, color in zip(KS, SERIES):
        vals = [summarize([r["rank_section"] for r in by[n]])[f"R@{k}"] for n in names]
        a1.scatter(vals, y, s=64, color=color, edgecolor=SURFACE, linewidth=2, zorder=3, label=f"Recall@{k}")
    for i, n in enumerate(names):
        s = summarize([r["rank_section"] for r in by[n]])
        a1.plot([s["R@1"], s["R@5"]], [i, i], color=GRID, linewidth=2, zorder=2)
    style(a1, "Section-level recall, all questions")
    a1.set_yticks(y, names, color=INK)

    # Hairline dividers between groups of rows that search the same kind of text.
    def group(n: str) -> str:
        s = next(c.searches for c in configs if c.name == n)
        return "floor" if n == "minilm-direct" else ("topic label" if "topic label" in s else "full question")

    for i in range(len(names) - 1):
        if group(names[i]) != group(names[i + 1]):
            for ax in (a1, a2):
                ax.axhline(i + 0.5, color=AXIS, linewidth=0.8, zorder=1)
    for i, n in enumerate(names):
        if i == len(names) - 1 or group(names[i + 1]) != group(n):  # topmost row of each group
            a1.text(-0.01, i + 0.44, f"searches: {group(n)}" if group(n) != "floor" else "floor",
                    color=MUTED, fontsize=8, va="top", ha="left")
    legend_below = dict(loc="upper left", bbox_to_anchor=(0, -0.07), frameon=False, labelcolor=INK2, fontsize=9)
    a1.legend(ncol=3, **legend_below)

    # Panel 2: R@3 on router-matched vs fallback questions
    for i, n in enumerate(names):
        m = summarize([r["rank_section"] for r in by[n] if not r["router_fell_back"]])["R@3"]
        f = summarize([r["rank_section"] for r in by[n] if r["router_fell_back"]])["R@3"]
        a2.plot([m, f], [i, i], color=GRID, linewidth=2, zorder=2)
        a2.scatter([m], [i], s=64, color=SERIES[0], edgecolor=SURFACE, linewidth=2, zorder=3,
                   label="router matched a keyword" if i == 0 else None)
        a2.scatter([f], [i], s=64, color=SERIES[1], edgecolor=SURFACE, linewidth=2, zorder=3,
                   label="no keyword (router fell back)" if i == 0 else None)
    n_fb = sum(r["router_fell_back"] for r in by[names[0]])
    style(a2, f"Recall@3: matched (n={len(by[names[0]]) - n_fb}) vs fallback (n={n_fb}) questions")
    a2.legend(ncol=2, **legend_below)

    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


# --- disagreements.md -----------------------------------------------------------------------


def disagreements_markdown(configs, questions, records, router_status) -> str:
    by_q: dict[str, dict[str, dict]] = {}
    for r in records:
        by_q.setdefault(r["qid"], {})[r["config"]] = r
    names = [c.name for c in configs]
    have = set(names)
    pairs = [p for p in FOCUS_PAIRS if set(p) <= have]

    buckets: dict[str, tuple[str, list]] = {}
    for a, b in pairs:
        buckets[f"{a}__miss__{b}__hit"] = (f"`{a}` misses @3, `{b}` hits @3", [])
        buckets[f"{b}__miss__{a}__hit"] = (f"`{b}` misses @3, `{a}` hits @3", [])
    buckets["other"] = ("Other disagreements @3", [])
    buckets["all_miss"] = ("Every configuration misses @3", [])
    for q in questions:
        rs = by_q[q["id"]]
        hits = {n: _hit(rs[n]) for n in names}
        if not any(hits.values()):
            buckets["all_miss"][1].append(q)
            continue
        if all(hits.values()):
            continue
        for a, b in pairs:
            if hits[a] != hits[b]:
                lose, win = (a, b) if hits[b] else (b, a)
                buckets[f"{lose}__miss__{win}__hit"][1].append(q)
                break
        else:
            buckets["other"][1].append(q)

    llm_labels = [(n, label) for n, label in (("minilm-llm-topic", "LLM topic_en"),
                                              ("minilm-llm-translation", "LLM translation")) if n in have]

    def llm_lines(qid: str) -> list[str]:
        out = []
        for n, label in llm_labels:
            r = by_q[qid][n]
            m = r["prep_meta"]
            note = f"intent {m['intent']}" + (f"; fell back: {m['llm_fallback']}" if m["llm_fallback"] else "")
            out.append(f"- **{label}:** `{r['query_text']}` ({note})")
        return out

    L = ["# Where the configurations disagree", "",
         "Every question where at least one configuration gets a relevant chunk into the top 3 and at "
         "least one does not, plus the questions every configuration misses. Ranks are of the first "
         "relevant chunk (38 chunks in total). Each question is filed under the first of these "
         "pairs that disagrees on it: " + "; ".join(f"`{a}` vs `{b}`" for a, b in pairs) + ".", ""]
    L += [f"- [{title}](#{key}) — {len(qs)}" for key, (title, qs) in buckets.items()]
    for key, (title, qs) in buckets.items():
        L += ["", f'<a id="{key}"></a>', f"## {title} ({len(qs)})", ""]
        for q in qs:
            st = router_status[q["id"]]
            route = (f"**fell back** → raw Arabic" if st.fell_back
                     else f"`{st.topic}` (matched {', '.join(st.matched_keys)})")
            L += [f"### {q['id']} · {q['register']}", "",
                  f"- **AR:** {q['question_ar']}",
                  f"- **EN (gold):** {q['gold_en']}",
                  f"- **Relevant:** {', '.join(f'`{r}`' for r in q['relevant'])}",
                  f"- **Keyword router:** {route}"]
            L += llm_lines(q["id"])
            if q.get("notes"):
                L.append(f"- **Note:** {q['notes']}")
            L += ["", "| Config | Rank | Top 3 retrieved |", "|---|---|---|"]
            for n in names:
                r = by_q[q["id"]][n]
                rank = r["rank_section"]
                mark = "✅" if _hit(r) else "❌"
                top3 = ", ".join(f"**{c}**" if c in q["relevant"] else c for c in r["top5"][:3])
                L.append(f"| `{n}` | {mark} {rank} | {top3} |")
            L.append("")
    return "\n".join(L) + "\n"


# --- entry point ----------------------------------------------------------------------------


def write_all(out: Path, configs, questions, chunks, records, latency, cost, router_status, diag, env) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.md").write_text(
        results_markdown(configs, questions, chunks, records, latency, cost, router_status, diag, env),
        encoding="utf-8")
    (out / "disagreements.md").write_text(
        disagreements_markdown(configs, questions, records, router_status), encoding="utf-8")
    with (out / "per_query.jsonl").open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = {c.name: {**summarize([r["rank_section"] for r in records if r["config"] == c.name]),
                        "latency": latency[c.name], "cost_per_1k": cost[c.name]} for c in configs}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_chart(out / "chart.png", configs, records)
