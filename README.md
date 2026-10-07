# Arabic questions over an English knowledge base: keyword routing, LLM rewriting and multilingual embeddings

A small, reproducible retrieval benchmark on a Saudi personal-finance knowledge base (7 English
Markdown documents).

The baseline retriever is `all-MiniLM-L6-v2`, an English-only embedding model. There are two
common ways to let Arabic questions reach an English-only retriever by rewriting the query into
English first:

- **Keyword router:** a substring dictionary maps Arabic keywords to English terms. The resulting
  topic string is searched on its own.
- **LLM router:** one JSON-mode LLM call classifies intent and returns `topic_en`, "3-8 ENGLISH
  keywords describing the topic". That topic string is searched on its own.

In both cases the question itself is discarded. If no topic is produced, the raw Arabic is
searched.

The alternatives are to translate the *full* question, or to embed the Arabic directly with a
multilingual model.

**The question:** where does retrieval quality go? Is it the English-only embedding model, or
rewriting the question into a topic label? And which fixes close the gap?

## TL;DR

Rows are grouped by *what text gets searched*. The embedder is MiniLM unless stated.

| Searched text | Config | R@1 | R@3 | MRR (95% CI) |
|---|---|---|---|---|
| raw Arabic (MiniLM can't read it) | `minilm-direct` — floor | 5% | 16% | 0.17 (0.11–0.23) |
| **topic label from keyword map** | `minilm-router` | 25% | 52% | **0.41** (0.32–0.51) |
| **topic label from LLM** | `minilm-llm-topic` | 70% | 93% | **0.81** (0.73–0.89) |
| full question, LLM translation | `minilm-llm-translation` | 71% | 95% | 0.82 (0.74–0.89) |
| full question, human translation | `minilm-gold-en` — ceiling | 77% | 93% | 0.85 (0.77–0.92) |
| full question, raw Arabic | `cohere-v4-direct` — Cohere embed-v4.0 | 77% | 88% | 0.84 (0.77–0.92) |
| full question, raw Arabic | **`cohere-v5-pro-direct` — Cohere embed-v5.0-pro** | 89% | 100% | **0.94** (0.90–0.98) |
| full question, raw Arabic | **`cohere-v5-fast-direct` — Cohere embed-v5.0-fast** | 88% | 98% | **0.93** (0.88–0.97) |
| full question, raw Arabic | `ml-minilm-direct` — free multilingual MiniLM | 45% | 64% | 0.58 (0.48–0.69) |
| full question, raw Arabic | `cohere-v4-rerank` — + rerank-v4.0-fast | 79% | 91% | 0.86 (0.78–0.93) |

1. **The large loss is in the keyword router.** Its MRR is 0.41 against about 0.81–0.85 for every
   configuration that searches a faithful English rendering of the question. It fails in two ways:
   - It silently degrades to the unreadable raw Arabic when no keyword matches.
   - When a keyword does match, it searches a generic label (`"loan debt"`). Even on the 32
     questions where it matched, the LLM's label beats it by +0.24 MRR (CI +0.11 to +0.37).
2. **LLM topic labels lose almost nothing on this set.** They score 0.81 against 0.85 for a human
   translation.
   - Replacing the LLM's topic label with an LLM translation, in the same call, changes MRR by
     **+0.01** (CI −0.07 to +0.08): the translation is better on 10 questions and worse on 9.
   - The model treats "3-8 keywords" as a short phrase that keeps the intent: `"debt repayment vs
     saving"`, `"is car insurance halal"`.
3. **The embedding model is not the bottleneck when the query text is good English.** MiniLM on a
   human translation (0.85) ties Cohere embed-v4.0 on raw Arabic (0.84). Embed-v4.0 on raw Arabic
   also ties the LLM-topic route (+0.03, CI −0.08 to +0.15). Embed 5 goes further; see finding 6.
4. **There are fixes at both layers.** With MiniLM and embed-v4.0 they reach the same level:
   - *Query-rewriting layer:* have an LLM produce an English label or translation. It doesn't
     matter much which.
   - *Embedding layer:* use a multilingual embedder that searches the Arabic directly. That also
     removes the keyword router's silent fallback, because the fallback query (the raw Arabic)
     becomes searchable.
5. **Rerank adds nothing measurable** (+0.01, CI −0.06 to +0.09).
6. **Cohere Embed 5 is the best setup tested.** Searching the raw Arabic directly, at the same 1024
   dimensions as v4:
   - `embed-v5.0-pro` scores 0.94 MRR and puts a correct section in the top 3 for **all 56
     questions**. `embed-v5.0-fast` scores 0.93, and the difference between them is negligible
     (+0.01, CI −0.03 to +0.06).
   - Both beat embed-v4.0: +0.10 for Pro (CI +0.03 to +0.17) and +0.09 for Fast (CI +0.01 to
     +0.16). They fix all 7 questions v4 missed in the top 3.
   - Pro also beats every query-rewriting route, including MiniLM on a human translation (+0.09,
     CI +0.01 to +0.18), so with Embed 5 the embedding layer is no longer tied with the rewriting
     layer.

The LLM rows use Cohere `command-a-03-2025`. Finding 2 depends on the model writing phrase-like
labels, so it may not hold for other LLMs; see [Limitations](#limitations).

The eval set is a stress test for the keyword router (it deliberately includes out-of-map
vocabulary), not a sample of real traffic.

---

## Setup

### Corpus and chunking

The corpus is 7 English Markdown documents (`knowledge/`): budgeting, car financing (murabaha vs
conventional), emergency fund, financial planning, Islamic finance contracts, saving strategies,
and zakat. Together they are about 21 KB.

The chunking is header-aware (`bench/chunking.py`):
- one chunk per `##` section, plus each document's preamble;
- each chunk is prefixed with its document title and section heading;
- chunk ids are readable (`zakat#the-nisab-threshold`) and serve directly as eval labels.

This gives 38 chunks of 31–313 words.

### Eval set: `eval/questions_ar.json`

56 Arabic questions, each labelled with the chunk(s) that answer it:

| Register | n | Examples |
|---|---|---|
| Modern Standard Arabic | 16 | ما هو الحد الأدنى من الثروة الذي تجب فيه الزكاة؟ |
| Everyday Saudi phrasing | 19 | كم تطلع زكاتي إذا عندي ربع مليون بالبنك؟ · أبي أحول جزء من معاشي أول ما ينزل لحساب ثاني |
| Religious / financial terms | 13 | زكاة، مرابحة، تورق، حول، نصاب، إجار منتهية بالتمليك، ميسر |
| Deliberately ambiguous | 8 | هل المرابحة أفضل؟ · أبي سيارة · الفلوس ما تكفي لآخر الشهر |

- 40 questions have one relevant chunk; 16 have 2–4.
- Each question also has a hand-written English translation (`gold_en`), used by the ceiling row.
- Many questions use vocabulary missing from the keyword map, or forms of mapped words that a
  substring match misses, such as زكاتي, الطوارى, قروض and اسلامي.
- تورق appears once in the corpus and not in the keyword map at all.

### Configurations (`bench/configs.py`)

| Config | Query text | Embedder |
|---|---|---|
| `minilm-direct` | raw Arabic | all-MiniLM-L6-v2 |
| `minilm-router` | keyword-map topic | all-MiniLM-L6-v2 |
| `minilm-llm-topic` | LLM `topic_en` | all-MiniLM-L6-v2 |
| `minilm-llm-translation` | same LLM call, `query_en` = faithful translation | all-MiniLM-L6-v2 |
| `minilm-gold-en` | human translation | all-MiniLM-L6-v2 |
| `ml-minilm-direct` | raw Arabic | paraphrase-multilingual-MiniLM-L12-v2 |
| `cohere-v4-direct` | raw Arabic | Cohere `embed-v4.0`, 1024 dims |
| `cohere-v5-pro-direct` | raw Arabic | Cohere `embed-v5.0-pro`, 1024 dims |
| `cohere-v5-fast-direct` | raw Arabic | Cohere `embed-v5.0-fast`, 1024 dims |
| `cohere-v4-rerank` | raw Arabic | `embed-v4.0` top-20 → `rerank-v4.0-fast` |

**The keyword router** (`bench/router.py`) is a 27-entry Arabic → English dictionary with
substring matching. The English terms of every matched key are joined and deduplicated. The topic
string is searched on its own, or the raw Arabic if nothing matched (`topic or message`). The
harness logs, per question, whether any keyword matched.

**The LLM router** (`bench/llm_router.py`) sends one call per question:
- **Model:** Cohere `command-a-03-2025`.
- **Prompt:** the system prompt is `CLASSIFY_SYSTEM` in `bench/llm_router.py`. It asks for intent,
  purchase details and `topic_en`, as JSON.
- **User turn:** `Conversation so far:\n(no prior messages)\n\nMessage to classify:\n{question}`.
- **Settings:** JSON mode, temperature 0.0, max_tokens 400.
- **What gets searched:** the returned `topic_en` string on its own. If it's empty, or the response
  isn't valid JSON with a known intent, the raw Arabic is searched instead. That never happened:
  all 56 calls returned valid JSON with a topic.

**The translation row** sends the exact same LLM prompt as the topic row, with one change: instead
of "3-8 English keywords describing the topic", it asks for "a faithful, complete English
translation; don't summarize or reduce it to keywords". Everything else is identical, so any
difference between the two rows comes only from *what* the LLM was asked to write.

### Metrics

- **Recall@k**: the share of questions with at least one labelled chunk in the top k. For
  multi-label questions this is the lenient "any hit" reading.
- **MRR**: the mean of 1/rank of the first relevant chunk.
- **Primary level**: section. **Secondary level**: document. With 7 documents, document-level
  recall saturates.
- **Uncertainty**: 95% percentile bootstrap CIs over questions, and paired bootstraps for
  differences.
- **Random baseline**: an exact random-ranking expectation is reported alongside.

## Results

![Recall@1, @3 and @5 per config, grouped by what text is searched](results/chart.png)

| Config | Searched text | R@1 | R@3 | R@5 | MRR | 95% CI |
|---|---|---|---|---|---|---|
| `minilm-direct` | raw Arabic | 5% | 16% | 23% | 0.17 | 0.11–0.23 |
| `minilm-router` | keyword-map topic | 25% | 52% | 64% | 0.41 | 0.32–0.51 |
| `minilm-llm-topic` | LLM topic label | 70% | 93% | 96% | 0.81 | 0.73–0.89 |
| `minilm-llm-translation` | LLM translation | 71% | 95% | 98% | 0.82 | 0.74–0.89 |
| `minilm-gold-en` | human translation | 77% | 93% | 98% | 0.85 | 0.77–0.92 |
| `ml-minilm-direct` | raw Arabic | 45% | 64% | 77% | 0.58 | 0.48–0.69 |
| `cohere-v4-direct` | raw Arabic | 77% | 88% | 96% | 0.84 | 0.77–0.92 |
| `cohere-v5-pro-direct` | raw Arabic | 89% | 100% | 100% | 0.94 | 0.90–0.98 |
| `cohere-v5-fast-direct` | raw Arabic | 88% | 98% | 100% | 0.93 | 0.88–0.97 |
| `cohere-v4-rerank` | raw Arabic | 79% | 91% | 95% | 0.86 | 0.78–0.93 |
| *random ranking (expected)* | | 4% | 11% | 18% | 0.14 | |

**Split by whether the keyword router matched (section R@3):**

| Config | Keyword matched (n=32) | No keyword → fallback (n=24) |
|---|---|---|
| `minilm-direct` | 12% | 21% |
| `minilm-router` | 75% | 21% |
| `minilm-llm-topic` | 91% | 96% |
| `minilm-llm-translation` | 94% | 96% |
| `minilm-gold-en` | 91% | 96% |
| `ml-minilm-direct` | 50% | 83% |
| `cohere-v4-direct` | 94% | 79% |
| `cohere-v5-pro-direct` | 100% | 100% |
| `cohere-v5-fast-direct` | 100% | 96% |
| `cohere-v4-rerank` | 94% | 88% |

## Implications

- **With an LLM rewriting the query, an English-only embedder reaches about the level of Cohere
  embed-v4.0.** Switching the topic label to a translation, or MiniLM to embed-v4.0, gives no
  measurable gain here. Switching to Cohere Embed 5 does: it beats every rewriting route and needs
  no LLM call.
- **A keyword router is the weak point.** Used as the only route or as a fallback, it drops Arabic
  retrieval from about 0.81 to 0.41 MRR. On questions the map can't parse, it drops to the floor,
  and nothing surfaces this. There are fixes at both layers:
  - *Rewriting layer:* normalize hamza, ta marbuta and common suffixes before the substring match.
    That would recover some misses (e.g. زكاتي, الطوارى, اسلامي), but the labels would stay generic.
  - *Embedding layer:* a multilingual embedder makes the fallback query, the raw Arabic, itself
    searchable. Cohere `embed-v4.0` scores 0.84 on raw Arabic here, and `embed-v5.0-pro` 0.94.
    It would also make query rewriting unnecessary. The local multilingual MiniLM (0.58) is a partial fix that needs no network.
- **Asking for a translation instead of a topic label** costs nothing extra in the same call. It's
  worth considering for multi-part or quantity questions (q26, q17, q31), but this benchmark doesn't
  show a net gain.
- **Rerank isn't worth adding at this corpus size.**

## Limitations

- **One LLM, one run.** The LLM rows use only `command-a-03-2025`, at temperature 0, with no
  repeated runs, so there's no estimate of run-to-run variation. The topic-label result depends on
  the model writing phrase-like labels rather than bare keyword lists; other LLMs may behave
  differently.
- **Few multi-part questions.** The set has few multi-part or comparison questions, which is exactly
  where a topic label is most likely to lose information. The topic-vs-translation comparison is
  weakly tested there.
- **Single-turn only.** Every question was sent with an empty conversation history, so follow-up
  questions that depend on context aren't tested.
- **Small and single-domain.** 56 questions over 38 chunks from 7 documents. MRR CIs are about
  ±0.04–0.10, which separates the keyword router from everything else but can't separate most of
  the top configurations from each other. Embed 5 vs embed-v4.0 is the exception.
- **The eval set is a stress test, not a traffic sample.** It deliberately includes vocabulary
  missing from the keyword map. The 24/56 fallback rate describes this set, not real-world traffic.
- **Gold translations are hand-written and clean**, so the human-translation row is an optimistic
  ceiling.
- **Lenient recall on multi-label questions.** For the 16 multi-label questions, any hit counts.
- **These are system comparisons, not ablations.** The embedders differ in size, training data and
  dimensionality, not only in language coverage.
- **Hosted models can change** behind the same name.

## Reproducing

```bash
python -m venv .venv
.venv\Scripts\activate                # Windows; source .venv/bin/activate elsewhere
pip install -r requirements.txt
# .env (gitignored): COHERE_API_KEY=...

python run_eval.py --dry-run          # prints every API call it would make; sends nothing
python run_eval.py                    # asks for confirmation above 20 uncached calls
python run_eval.py --configs minilm-direct,minilm-router,minilm-gold-en,ml-minilm-direct   # local only, free
```

- **Caching.** Embeddings, rerank results, LLM responses and API latency samples are cached under
  `cache/` (gitignored). LLM responses are keyed by model, prompt hash and question.
- **Call budget for a fresh run.** It needs 234 Cohere calls: 122 embed/rerank plus 112 chat.
  Trial keys allow 1,000 calls per month across all endpoints. After that, re-runs are free.
- **Rate limits.** 429 and 5xx responses are retried with exponential backoff. Calls are spaced to
  trial limits: rerank 10/min, chat 20/min.
- **Validation.** The eval file is checked on startup, and the translation prompt asserts it
  differs from the topic prompt by exactly one field.

### Adding a model

Any sentence-transformers checkpoint is one line in `bench/embedders.py`:

```python
EMBEDDERS["e5-large"] = lambda: SentenceTransformerEmbedder("intfloat/multilingual-e5-large")
```

and one entry in `bench/configs.py`:

```python
Config("e5-direct", "full question — raw Arabic", "Arabic -> multilingual-e5-large", "e5-large", arabic),
```

(E5 expects `query: ` / `passage: ` prefixes, which would be a small `Embedder` subclass.) A new
API provider is one `Embedder` subclass implementing `_embed(texts, role)`, and a new query rewrite
is one `prepare` function. Caching, call planning, latency measurement and reporting come with it.

## Layout

```
bench/chunking.py      header-aware Markdown splitter
bench/router.py        keyword router + fallback instrumentation
bench/llm_router.py    LLM router: topic_en call and its translation variant (command-a-03-2025)
bench/embedders.py     Embedder interface, MiniLM / Cohere backends, disk cache, retry/backoff
bench/rerank.py        Cohere Rerank with throttle + cache
bench/configs.py       the ten configurations
bench/metrics.py       Recall@k, MRR, bootstrap CIs, random baseline
bench/report.py        results.md, chart.png, disagreements.md, per_query.jsonl
eval/questions_ar.json
run_eval.py
results/               generated; committed so the numbers above can be checked
```
