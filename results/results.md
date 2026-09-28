# Results

Generated 2026-09-28 by `run_eval.py`. 38 chunks, 56 Arabic questions.

Recall@k = share of questions with at least one labelled relevant chunk in the top k. MRR uses the first relevant chunk. 95% CIs are percentile bootstraps over questions (10k resamples).

## Section-level retrieval (headline)

Rows are ordered by what text is embedded on the query side.

| Config | Searched text | R@1 | R@3 | R@5 | MRR | MRR 95% CI | Median latency | Cost / 1k queries |
|---|---|---|---|---|---|---|---|---|
| `minilm-direct` | full question — raw Arabic (unreadable to this model) | 5% | 16% | 23% | 0.17 | 0.11–0.23 | 11.6 ms (n=56) | $0.0000 |
| `minilm-router` | topic label — keyword map | 25% | 52% | 64% | 0.41 | 0.32–0.51 | 14.1 ms (n=56) | $0.0000 |
| &nbsp;&nbsp;↳ keyword matched (n=32) |  | 38% | 75% | 91% | 0.57 | 0.45–0.69 |  |  |
| &nbsp;&nbsp;↳ no keyword → raw Arabic fallback (n=24) |  | 8% | 21% | 29% | 0.21 | 0.11–0.32 |  |  |
| `minilm-llm-topic` | topic label — LLM topic_en | 70% | 93% | 96% | 0.81 | 0.73–0.89 | 1132.5 ms (n=56) | $2.28 |
| `minilm-llm-translation` | full question — LLM translation | 71% | 95% | 98% | 0.82 | 0.74–0.89 | 1256.2 ms (n=56) | $2.51 |
| `minilm-gold-en` | full question — human translation | 77% | 93% | 98% | 0.85 | 0.77–0.92 | 15.1 ms (n=56) | $0.0000 |
| `ml-minilm-direct` | full question — raw Arabic | 45% | 64% | 77% | 0.58 | 0.48–0.69 | 16.2 ms (n=56) | $0.0000 |
| `cohere-v4-direct` | full question — raw Arabic | 77% | 88% | 96% | 0.84 | 0.77–0.92 | 648.3 ms (n=20) | $0.0021 |
| `cohere-v4-rerank` | full question — raw Arabic | 79% | 91% | 95% | 0.86 | 0.78–0.93 | 1366.6 ms (n=20) | $2.00 |
| *random ranking (expected)* | | 4% | 11% | 18% | 0.14 | | | |

Latency: local models are timed on CPU per single query after warm-up; Cohere is one single-query HTTPS call per sample (network round trip included), so the two are not like-for-like. The rerank row adds the rerank call to the embed call. LLM rows include the measured LLM call (Cohere command-a-03-2025) plus the local embed. Cost excludes local compute and the one-time corpus embedding.

Configs:

- `minilm-direct` — Baseline: Arabic query -> all-MiniLM-L6-v2 (English-only)
- `minilm-router` — Keyword router: Arabic -> keyword-map topic -> MiniLM
- `minilm-llm-topic` — LLM router: command-a-03-2025 classify call -> topic_en -> MiniLM
- `minilm-llm-translation` — Same LLM call with topic_en swapped for a faithful translation -> MiniLM
- `minilm-gold-en` — Ceiling for translate-first: human English translation -> MiniLM
- `ml-minilm-direct` — Free multilingual: Arabic -> paraphrase-multilingual-MiniLM-L12-v2
- `cohere-v4-direct` — Cohere: Arabic -> embed-v4.0 (search_query) vs chunks (search_document)
- `cohere-v4-rerank` — Cohere embed-v4.0 top-20 -> rerank-v4.0-fast

## LLM routing diagnostics

| Config | LLM | Intents returned | Fell back to raw Arabic |
|---|---|---|---|
| `minilm-llm-topic` | `command-a-03-2025` | financial_question: 53, purchase_simulation: 3 | none |
| `minilm-llm-translation` | `command-a-03-2025` | financial_question: 53, purchase_simulation: 3 | none |

Fell back: `empty_field` = no topic/translation returned; `llm_error` = unparseable JSON or an unknown intent. In both cases the raw Arabic question is searched.

## Split by whether the keyword router matched a keyword

The router matched at least one keyword on 32/56 questions and fell back to the raw Arabic message on 24/56. Note: the eval set deliberately includes out-of-map vocabulary, so this fallback rate describes this eval set, not real-world traffic.

| Config | Matched R@1 | Matched R@3 | Matched MRR | Fallback R@1 | Fallback R@3 | Fallback MRR |
|---|---|---|---|---|---|---|
| `minilm-direct` | 3% | 12% | 0.14 | 8% | 21% | 0.21 |
| `minilm-router` | 38% | 75% | 0.57 | 8% | 21% | 0.21 |
| `minilm-llm-topic` | 72% | 91% | 0.81 | 67% | 96% | 0.81 |
| `minilm-llm-translation` | 66% | 94% | 0.79 | 79% | 96% | 0.86 |
| `minilm-gold-en` | 75% | 91% | 0.84 | 79% | 96% | 0.86 |
| `ml-minilm-direct` | 31% | 50% | 0.47 | 62% | 83% | 0.73 |
| `cohere-v4-direct` | 84% | 94% | 0.90 | 67% | 79% | 0.77 |
| `cohere-v4-rerank` | 81% | 94% | 0.88 | 75% | 88% | 0.83 |

Fallback questions: q08, q09, q11, q14, q16, q17, q18, q21, q24, q25, q27, q28, q29, q32, q33, q34, q38, q42, q43, q46, q49, q51, q52, q55

## Paired comparisons (section-level MRR, same questions)

| A → B | ΔMRR (B − A) | 95% CI | B better / A better (questions) |
|---|---|---|---|
| `minilm-direct` → `minilm-router` | +0.25 | +0.15 to +0.34 | 28 / 4 |
| `minilm-router` → `minilm-llm-topic` | +0.40 | +0.29 to +0.51 | 38 / 3 |
| `minilm-llm-topic` → `minilm-llm-translation` | +0.01 | -0.07 to +0.08 | 10 / 9 |
| `minilm-llm-translation` → `minilm-gold-en` | +0.03 | -0.02 to +0.08 | 5 / 4 |
| `minilm-llm-topic` → `cohere-v4-direct` | +0.03 | -0.08 to +0.15 | 15 / 13 |
| `minilm-llm-translation` → `cohere-v4-direct` | +0.03 | -0.07 to +0.13 | 12 / 10 |
| `minilm-gold-en` → `cohere-v4-direct` | -0.00 | -0.10 to +0.10 | 10 / 11 |
| `ml-minilm-direct` → `cohere-v4-direct` | +0.26 | +0.14 to +0.38 | 28 / 7 |
| `cohere-v4-direct` → `cohere-v4-rerank` | +0.01 | -0.06 to +0.09 | 9 / 8 |

## Section-level R@3 by register

| Config | msa (n=16) | saudi (n=19) | terminology (n=13) | ambiguous (n=8) |
|---|---|---|---|---|
| `minilm-direct` | 0% | 16% | 8% | 62% |
| `minilm-router` | 44% | 37% | 62% | 88% |
| `minilm-llm-topic` | 94% | 84% | 100% | 100% |
| `minilm-llm-translation` | 94% | 95% | 100% | 88% |
| `minilm-gold-en` | 88% | 95% | 100% | 88% |
| `ml-minilm-direct` | 75% | 68% | 38% | 75% |
| `cohere-v4-direct` | 94% | 79% | 92% | 88% |
| `cohere-v4-rerank` | 100% | 95% | 85% | 75% |

## Document-level retrieval (secondary)

Right *file* anywhere in the top k. With only 7 documents this saturates quickly.

| Config | R@1 | R@3 | R@5 | MRR |
|---|---|---|---|---|
| `minilm-direct` | 27% | 61% | 84% | 0.49 |
| `minilm-router` | 61% | 84% | 93% | 0.75 |
| `minilm-llm-topic` | 89% | 98% | 100% | 0.94 |
| `minilm-llm-translation` | 88% | 98% | 100% | 0.93 |
| `minilm-gold-en` | 89% | 98% | 98% | 0.93 |
| `ml-minilm-direct` | 61% | 91% | 96% | 0.75 |
| `cohere-v4-direct` | 88% | 98% | 100% | 0.93 |
| `cohere-v4-rerank` | 84% | 96% | 100% | 0.91 |

## What the local models' tokenizers see

| Model | Vocab | Mean tokens / Arabic question | `[UNK]` rate | Chunks truncated (max_seq_length) |
|---|---|---|---|---|
| `sentence-transformers/all-MiniLM-L6-v2` | 30,522 | 36.8 | 3% | 2/38 (limit 256, longest 480) |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 250,002 | 14.4 | 0% | 21/38 (limit 128, longest 471) |

Example tokenizations:

- `sentence-transformers/all-MiniLM-L6-v2` · q01 `ما هو الحد الأدنى من الثروة الذي تجب فيه الزكاة؟` → `م ##ا ه ##و ا ##ل ##ح ##د ا ##ل ##ا ##د ##ن ##ى م ##ن ا ##ل ##ث ##ر ##و ##ة ا ##ل ##ذ ##ي ت ##ج ##ب ف ##ي ##ه ا ##ل ##ز ##ك ##ا ##ة [UNK]`
- `sentence-transformers/all-MiniLM-L6-v2` · q27 `كم تطلع زكاتي إذا عندي ربع مليون بالبنك؟` → `ك ##م ت ##ط ##ل ##ع ز ##ك ##ا ##ت ##ي ا ##ذ ##ا ع ##ن ##د ##ي ر ##ب ##ع م ##ل ##ي ##و ##ن ب ##ا ##ل ##ب ##ن ##ك [UNK]`
- `sentence-transformers/all-MiniLM-L6-v2` · q38 `وش يعني تورق؟` → `و ##ش ي ##ع ##ن ##ي ت ##و ##ر ##ق [UNK]`
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` · q01 `ما هو الحد الأدنى من الثروة الذي تجب فيه الزكاة؟` → `▁ما ▁هو ▁الحد ▁الأ د نى ▁من ▁الث رو ة ▁الذي ▁ت جب ▁فيه ▁الز كا ة ؟`
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` · q27 `كم تطلع زكاتي إذا عندي ربع مليون بالبنك؟` → `▁كم ▁ تطلع ▁ز كات ي ▁إذا ▁عند ي ▁ ربع ▁مليون ▁بال بن ك ؟`
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` · q38 `وش يعني تورق؟` → `▁وش ▁يعني ▁تور ق ؟`

## Run environment

- Python 3.13.1, Windows 11, Intel64 Family 6 Model 140 Stepping 1, GenuineIntel
- Cohere API calls made in the run that produced this file: none (all cached)
