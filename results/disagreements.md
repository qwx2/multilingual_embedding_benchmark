# Where the configurations disagree

Every question where at least one configuration gets a relevant chunk into the top 3 and at least one does not, plus the questions every configuration misses. Ranks are of the first relevant chunk (38 chunks in total). Each question is filed under the first of these pairs that disagrees on it: `minilm-llm-topic` vs `minilm-llm-translation`; `minilm-router` vs `minilm-llm-topic`; `minilm-llm-topic` vs `cohere-v4-direct`; `minilm-router` vs `cohere-v4-direct`.

- [`minilm-llm-topic` misses @3, `minilm-llm-translation` hits @3](#minilm-llm-topic__miss__minilm-llm-translation__hit) — 2
- [`minilm-llm-translation` misses @3, `minilm-llm-topic` hits @3](#minilm-llm-translation__miss__minilm-llm-topic__hit) — 1
- [`minilm-router` misses @3, `minilm-llm-topic` hits @3](#minilm-router__miss__minilm-llm-topic__hit) — 24
- [`minilm-llm-topic` misses @3, `minilm-router` hits @3](#minilm-llm-topic__miss__minilm-router__hit) — 0
- [`minilm-llm-topic` misses @3, `cohere-v4-direct` hits @3](#minilm-llm-topic__miss__cohere-v4-direct__hit) — 2
- [`cohere-v4-direct` misses @3, `minilm-llm-topic` hits @3](#cohere-v4-direct__miss__minilm-llm-topic__hit) — 1
- [`minilm-router` misses @3, `cohere-v4-direct` hits @3](#minilm-router__miss__cohere-v4-direct__hit) — 0
- [`cohere-v4-direct` misses @3, `minilm-router` hits @3](#cohere-v4-direct__miss__minilm-router__hit) — 0
- [Other disagreements @3](#other) — 20
- [Every configuration misses @3](#all_miss) — 0

<a id="minilm-llm-topic__miss__minilm-llm-translation__hit"></a>
## `minilm-llm-topic` misses @3, `minilm-llm-translation` hits @3 (2)

### q17 · saudi

- **AR:** كم لازم يكون عندي فلوس احتياط عشان لو انفصلت من الشغل؟
- **EN (gold):** How much reserve money should I have in case I get laid off from work?
- **Relevant:** `emergency_fund#how-much-is-enough`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `emergency fund, job loss, savings` (intent financial_question)
- **LLM translation:** `How much emergency money should I have in case I lose my job?` (intent financial_question)
- **Note:** Dialect synonym (احتياط) for emergency fund.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 28 | budgeting#categories-that-quietly-leak-money, budgeting#build-the-budget-from-your-actual-cash-flow, budgeting#review-cadence |
| `minilm-router` | ❌ 28 | budgeting#categories-that-quietly-leak-money, budgeting#build-the-budget-from-your-actual-cash-flow, budgeting#review-cadence |
| `minilm-llm-topic` | ❌ 5 | emergency_fund#intro, emergency_fund#rebuilding-after-you-use-it, emergency_fund#the-rule-that-protects-everything-else |
| `minilm-llm-translation` | ✅ 1 | **emergency_fund#how-much-is-enough**, emergency_fund#intro, emergency_fund#the-rule-that-protects-everything-else |
| `minilm-gold-en` | ✅ 1 | **emergency_fund#how-much-is-enough**, financial_planning#know-your-four-numbers, saving_strategies#automate-then-forget |
| `ml-minilm-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, saving_strategies#the-waiting-test, saving_strategies#pay-yourself-first |
| `cohere-v4-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#intro |
| `cohere-v5-pro-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, saving_strategies#sinking-funds-for-lumpy-costs, saving_strategies#order-of-operations |
| `cohere-v5-fast-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, saving_strategies#sinking-funds-for-lumpy-costs |
| `cohere-v4-rerank` | ✅ 1 | **emergency_fund#how-much-is-enough**, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#intro |

### q31 · saudi

- **AR:** كم نسبة من راتبي المفروض أدخر كل شهر؟
- **EN (gold):** What percentage of my salary should I save each month?
- **Relevant:** `budgeting#the-50-30-20-rule-adapted-for-saudi-salaries`
- **Keyword router:** `salary income` (matched راتب)
- **LLM topic_en:** `savings rate from salary` (intent financial_question)
- **LLM translation:** `What percentage of my salary should I save each month?` (intent financial_question)
- **Note:** The verb أدخر does not contain the noun key ادخار.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 15 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, budgeting#intro |
| `minilm-router` | ✅ 2 | financial_planning#know-your-four-numbers, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, saving_strategies#automate-then-forget |
| `minilm-llm-topic` | ❌ 6 | financial_planning#know-your-four-numbers, saving_strategies#automate-then-forget, saving_strategies#intro |
| `minilm-llm-translation` | ✅ 3 | financial_planning#know-your-four-numbers, saving_strategies#automate-then-forget, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries** |
| `minilm-gold-en` | ✅ 3 | financial_planning#know-your-four-numbers, saving_strategies#automate-then-forget, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries** |
| `ml-minilm-direct` | ❌ 5 | financial_planning#know-your-four-numbers, emergency_fund#how-much-is-enough, saving_strategies#pay-yourself-first |
| `cohere-v4-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, saving_strategies#pay-yourself-first, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-pro-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, saving_strategies#pay-yourself-first, financial_planning#know-your-four-numbers |
| `cohere-v5-fast-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, saving_strategies#pay-yourself-first, financial_planning#know-your-four-numbers |
| `cohere-v4-rerank` | ✅ 2 | financial_planning#know-your-four-numbers, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, budgeting#build-the-budget-from-your-actual-cash-flow |


<a id="minilm-llm-translation__miss__minilm-llm-topic__hit"></a>
## `minilm-llm-translation` misses @3, `minilm-llm-topic` hits @3 (1)

### q52 · ambiguous

- **AR:** الفلوس ما تكفي لآخر الشهر
- **EN (gold):** The money doesn't last until the end of the month
- **Relevant:** `budgeting#build-the-budget-from-your-actual-cash-flow`, `budgeting#categories-that-quietly-leak-money`, `budgeting#intro`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `budgeting, money not lasting until end of month` (intent financial_question)
- **LLM translation:** `I don't have enough money to last until the end of the month` (intent financial_question)
- **Note:** A complaint, not a question.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, islamic_finance#murabaha-cost-plus-sale, **budgeting#intro** |
| `minilm-router` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, islamic_finance#murabaha-cost-plus-sale, **budgeting#intro** |
| `minilm-llm-topic` | ✅ 2 | budgeting#review-cadence, **budgeting#build-the-budget-from-your-actual-cash-flow**, **budgeting#intro** |
| `minilm-llm-translation` | ❌ 14 | emergency_fund#how-much-is-enough, emergency_fund#the-rule-that-protects-everything-else, saving_strategies#sinking-funds-for-lumpy-costs |
| `minilm-gold-en` | ❌ 17 | emergency_fund#how-much-is-enough, emergency_fund#the-rule-that-protects-everything-else, saving_strategies#sinking-funds-for-lumpy-costs |
| `ml-minilm-direct` | ❌ 7 | emergency_fund#how-much-is-enough, saving_strategies#the-waiting-test, financial_planning#know-your-four-numbers |
| `cohere-v4-direct` | ❌ 7 | zakat#the-nisab-threshold, emergency_fund#how-much-is-enough, emergency_fund#the-rule-that-protects-everything-else |
| `cohere-v5-pro-direct` | ✅ 2 | emergency_fund#how-much-is-enough, **budgeting#build-the-budget-from-your-actual-cash-flow**, saving_strategies#sinking-funds-for-lumpy-costs |
| `cohere-v5-fast-direct` | ✅ 2 | emergency_fund#how-much-is-enough, **budgeting#build-the-budget-from-your-actual-cash-flow**, emergency_fund#the-rule-that-protects-everything-else |
| `cohere-v4-rerank` | ❌ 13 | emergency_fund#how-much-is-enough, zakat#the-nisab-threshold, emergency_fund#the-rule-that-protects-everything-else |


<a id="minilm-router__miss__minilm-llm-topic__hit"></a>
## `minilm-router` misses @3, `minilm-llm-topic` hits @3 (24)

### q02 · msa

- **AR:** ما المحظورات الثلاثة الأساسية في التمويل الإسلامي؟
- **EN (gold):** What are the three basic prohibitions in Islamic finance?
- **Relevant:** `islamic_finance#the-three-prohibitions`
- **Keyword router:** `financing loan islamic finance` (matched تمويل, إسلامي)
- **LLM topic_en:** `islamic finance prohibitions` (intent financial_question)
- **LLM translation:** `What are the three main prohibitions in Islamic finance?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 17 | islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#murabaha-cost-plus-sale, budgeting#categories-that-quietly-leak-money |
| `minilm-router` | ❌ 4 | islamic_finance#practical-guidance, islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-llm-topic` | ✅ 2 | islamic_finance#intro, **islamic_finance#the-three-prohibitions**, islamic_finance#practical-guidance |
| `minilm-llm-translation` | ✅ 2 | islamic_finance#intro, **islamic_finance#the-three-prohibitions**, islamic_finance#practical-guidance |
| `minilm-gold-en` | ✅ 2 | islamic_finance#intro, **islamic_finance#the-three-prohibitions**, islamic_finance#practical-guidance |
| `ml-minilm-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#practical-guidance |
| `cohere-v4-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#intro |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#intro, islamic_finance#practical-guidance |
| `cohere-v4-rerank` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#intro, zakat#intro |

### q05 · msa

- **AR:** أين يجب أن أحتفظ بمدخرات الطوارئ؟
- **EN (gold):** Where should I keep my emergency savings?
- **Relevant:** `emergency_fund#where-to-keep-it`
- **Keyword router:** `emergency fund savings` (matched طوارئ, مدخرات)
- **LLM topic_en:** `emergency fund savings location` (intent financial_question)
- **LLM translation:** `Where should I keep my emergency savings?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 24 | islamic_finance#murabaha-cost-plus-sale, budgeting#categories-that-quietly-leak-money, islamic_finance#intro |
| `minilm-router` | ❌ 4 | emergency_fund#intro, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#rebuilding-after-you-use-it |
| `minilm-llm-topic` | ✅ 2 | emergency_fund#intro, **emergency_fund#where-to-keep-it**, emergency_fund#the-rule-that-protects-everything-else |
| `minilm-llm-translation` | ✅ 1 | **emergency_fund#where-to-keep-it**, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#rebuilding-after-you-use-it |
| `minilm-gold-en` | ✅ 1 | **emergency_fund#where-to-keep-it**, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#rebuilding-after-you-use-it |
| `ml-minilm-direct` | ❌ 4 | emergency_fund#intro, emergency_fund#how-much-is-enough, emergency_fund#rebuilding-after-you-use-it |
| `cohere-v4-direct` | ✅ 1 | **emergency_fund#where-to-keep-it**, emergency_fund#intro, emergency_fund#rebuilding-after-you-use-it |
| `cohere-v5-pro-direct` | ✅ 1 | **emergency_fund#where-to-keep-it**, emergency_fund#how-much-is-enough, emergency_fund#the-rule-that-protects-everything-else |
| `cohere-v5-fast-direct` | ✅ 1 | **emergency_fund#where-to-keep-it**, emergency_fund#intro, emergency_fund#how-much-is-enough |
| `cohere-v4-rerank` | ✅ 1 | **emergency_fund#where-to-keep-it**, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#intro |

### q08 · msa

- **AR:** ما هو التأمين التكافلي وكيف يتجنب الغرر؟
- **EN (gold):** What is takaful insurance and how does it avoid gharar?
- **Relevant:** `islamic_finance#takaful-cooperative-insurance`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `takaful insurance, avoiding gharar` (intent financial_question)
- **LLM translation:** `What is Takaful insurance and how does it avoid Gharar?` (intent financial_question)
- **Note:** Neither تأمين nor غرر is in the router map.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 6 | islamic_finance#murabaha-cost-plus-sale, budgeting#categories-that-quietly-leak-money, islamic_finance#intro |
| `minilm-router` | ❌ 6 | islamic_finance#murabaha-cost-plus-sale, budgeting#categories-that-quietly-leak-money, islamic_finance#intro |
| `minilm-llm-topic` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, saving_strategies#the-waiting-test, emergency_fund#how-much-is-enough |
| `minilm-llm-translation` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#mudaraba-and-musharaka-partnership, budgeting#categories-that-quietly-leak-money |
| `minilm-gold-en` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#mudaraba-and-musharaka-partnership, budgeting#categories-that-quietly-leak-money |
| `ml-minilm-direct` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, emergency_fund#the-rule-that-protects-everything-else, financial_planning#a-financial-health-score |
| `cohere-v4-direct` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#the-three-prohibitions, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#the-three-prohibitions, islamic_finance#mudaraba-and-musharaka-partnership |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#the-three-prohibitions, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v4-rerank` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#the-three-prohibitions, saving_strategies#sinking-funds-for-lumpy-costs |

### q09 · msa

- **AR:** ما نسبة ضريبة القيمة المضافة في المملكة وكيف تؤثر على سعر الشراء؟
- **EN (gold):** What is the VAT rate in the Kingdom and how does it affect the purchase price?
- **Relevant:** `financial_planning#vision-2030-context`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `VAT rate in Saudi Arabia, impact on purchase price` (intent financial_question)
- **LLM translation:** `What is the VAT rate in Saudi Arabia and how does it affect the purchase price?` (intent financial_question)
- **Note:** Tax vocabulary is not in the router map.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 6 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership, budgeting#intro |
| `minilm-router` | ❌ 6 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership, budgeting#intro |
| `minilm-llm-topic` | ✅ 1 | **financial_planning#vision-2030-context**, budgeting#categories-that-quietly-leak-money, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries |
| `minilm-llm-translation` | ✅ 1 | **financial_planning#vision-2030-context**, budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale |
| `minilm-gold-en` | ✅ 1 | **financial_planning#vision-2030-context**, islamic_finance#murabaha-cost-plus-sale, budgeting#categories-that-quietly-leak-money |
| `ml-minilm-direct` | ✅ 1 | **financial_planning#vision-2030-context**, car_financing#conventional-riba-based-auto-loans, zakat#the-calculation |
| `cohere-v4-direct` | ✅ 2 | islamic_finance#murabaha-cost-plus-sale, **financial_planning#vision-2030-context**, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries |
| `cohere-v5-pro-direct` | ✅ 1 | **financial_planning#vision-2030-context**, car_financing#murabaha-the-standard-islamic-auto-finance, car_financing#conventional-riba-based-auto-loans |
| `cohere-v5-fast-direct` | ✅ 1 | **financial_planning#vision-2030-context**, islamic_finance#murabaha-cost-plus-sale, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v4-rerank` | ✅ 1 | **financial_planning#vision-2030-context**, zakat#how-a-large-purchase-affects-your-zakat-base, car_financing#murabaha-the-standard-islamic-auto-finance |

### q11 · msa

- **AR:** ما الفرق بين عقد المضاربة والمشاركة المتناقصة؟
- **EN (gold):** What is the difference between a mudaraba contract and diminishing musharaka?
- **Relevant:** `islamic_finance#mudaraba-and-musharaka-partnership`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `mudarabah vs diminishing partnership contracts` (intent financial_question)
- **LLM translation:** `What is the difference between Mudarabah and Diminishing Partnership contracts?` (intent financial_question)
- **Note:** Contract names absent from router map.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 10 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, budgeting#review-cadence |
| `minilm-router` | ❌ 10 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, budgeting#review-cadence |
| `minilm-llm-topic` | ✅ 1 | **islamic_finance#mudaraba-and-musharaka-partnership**, islamic_finance#practical-guidance, islamic_finance#murabaha-cost-plus-sale |
| `minilm-llm-translation` | ✅ 1 | **islamic_finance#mudaraba-and-musharaka-partnership**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#practical-guidance |
| `minilm-gold-en` | ✅ 1 | **islamic_finance#mudaraba-and-musharaka-partnership**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#practical-guidance |
| `ml-minilm-direct` | ✅ 1 | **islamic_finance#mudaraba-and-musharaka-partnership**, islamic_finance#takaful-cooperative-insurance, islamic_finance#the-three-prohibitions |
| `cohere-v4-direct` | ✅ 1 | **islamic_finance#mudaraba-and-musharaka-partnership**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#takaful-cooperative-insurance |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#mudaraba-and-musharaka-partnership**, islamic_finance#takaful-cooperative-insurance, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#mudaraba-and-musharaka-partnership**, islamic_finance#the-three-prohibitions, islamic_finance#takaful-cooperative-insurance |
| `cohere-v4-rerank` | ✅ 1 | **islamic_finance#mudaraba-and-musharaka-partnership**, islamic_finance#the-three-prohibitions, islamic_finance#murabaha-cost-plus-sale |

### q14 · msa

- **AR:** ما مكونات مؤشر الصحة المالية وكيف يُستخدم؟
- **EN (gold):** What are the components of the financial health score and how is it used?
- **Relevant:** `financial_planning#a-financial-health-score`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `financial health index components and usage` (intent financial_question)
- **LLM translation:** `What are the components of the financial health index and how is it used?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 37 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, budgeting#intro |
| `minilm-router` | ❌ 37 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, budgeting#intro |
| `minilm-llm-topic` | ✅ 1 | **financial_planning#a-financial-health-score**, financial_planning#know-your-four-numbers, financial_planning#vision-2030-context |
| `minilm-llm-translation` | ✅ 1 | **financial_planning#a-financial-health-score**, financial_planning#know-your-four-numbers, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-gold-en` | ✅ 1 | **financial_planning#a-financial-health-score**, financial_planning#know-your-four-numbers, financial_planning#vision-2030-context |
| `ml-minilm-direct` | ✅ 1 | **financial_planning#a-financial-health-score**, financial_planning#know-your-four-numbers, emergency_fund#intro |
| `cohere-v4-direct` | ✅ 1 | **financial_planning#a-financial-health-score**, financial_planning#know-your-four-numbers, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-pro-direct` | ✅ 1 | **financial_planning#a-financial-health-score**, financial_planning#know-your-four-numbers, financial_planning#plan-around-goals-not-products |
| `cohere-v5-fast-direct` | ✅ 1 | **financial_planning#a-financial-health-score**, financial_planning#know-your-four-numbers, financial_planning#plan-around-goals-not-products |
| `cohere-v4-rerank` | ✅ 1 | **financial_planning#a-financial-health-score**, financial_planning#know-your-four-numbers, zakat#the-calculation |

### q15 · msa

- **AR:** هل يمكن الاعتماد على مكافأة نهاية الخدمة كمصدر للتقاعد؟
- **EN (gold):** Can end-of-service benefits be relied on as a source of retirement income?
- **Relevant:** `financial_planning#vision-2030-context`
- **Keyword router:** `retirement planning` (matched تقاعد)
- **LLM topic_en:** `end of service benefits as retirement source` (intent financial_question)
- **LLM translation:** `Can the end-of-service benefit be relied upon as a source of retirement income?` (intent financial_question)
- **Note:** Router matches تقاعد -> 'retirement planning', which has no dedicated section.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 6 | budgeting#build-the-budget-from-your-actual-cash-flow, budgeting#categories-that-quietly-leak-money, budgeting#review-cadence |
| `minilm-router` | ❌ 7 | financial_planning#plan-around-goals-not-products, saving_strategies#order-of-operations, financial_planning#know-your-four-numbers |
| `minilm-llm-topic` | ✅ 1 | **financial_planning#vision-2030-context**, emergency_fund#how-much-is-enough, financial_planning#know-your-four-numbers |
| `minilm-llm-translation` | ✅ 1 | **financial_planning#vision-2030-context**, emergency_fund#how-much-is-enough, financial_planning#know-your-four-numbers |
| `minilm-gold-en` | ✅ 1 | **financial_planning#vision-2030-context**, financial_planning#know-your-four-numbers, emergency_fund#how-much-is-enough |
| `ml-minilm-direct` | ❌ 4 | emergency_fund#how-much-is-enough, saving_strategies#automate-then-forget, saving_strategies#intro |
| `cohere-v4-direct` | ✅ 1 | **financial_planning#vision-2030-context**, emergency_fund#intro, car_financing#the-decision-rule |
| `cohere-v5-pro-direct` | ✅ 1 | **financial_planning#vision-2030-context**, emergency_fund#how-much-is-enough, saving_strategies#sinking-funds-for-lumpy-costs |
| `cohere-v5-fast-direct` | ✅ 1 | **financial_planning#vision-2030-context**, emergency_fund#how-much-is-enough, saving_strategies#pay-yourself-first |
| `cohere-v4-rerank` | ✅ 1 | **financial_planning#vision-2030-context**, emergency_fund#how-much-is-enough, emergency_fund#intro |

### q16 · msa

- **AR:** كيف أحدد أهدافي المالية بطريقة صحيحة؟
- **EN (gold):** How do I set my financial goals properly?
- **Relevant:** `financial_planning#plan-around-goals-not-products`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `setting financial goals` (intent financial_question)
- **LLM translation:** `How do I set my financial goals correctly?` (intent financial_question)
- **Note:** أهدافي (plural) does not contain the key هدف.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 37 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, saving_strategies#pay-yourself-first |
| `minilm-router` | ❌ 37 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, saving_strategies#pay-yourself-first |
| `minilm-llm-topic` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, financial_planning#a-financial-health-score, financial_planning#intro |
| `minilm-llm-translation` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, financial_planning#a-financial-health-score, financial_planning#intro |
| `minilm-gold-en` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, financial_planning#a-financial-health-score, saving_strategies#order-of-operations |
| `ml-minilm-direct` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, financial_planning#a-financial-health-score, financial_planning#know-your-four-numbers |
| `cohere-v4-direct` | ❌ 4 | financial_planning#know-your-four-numbers, financial_planning#a-financial-health-score, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-pro-direct` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, saving_strategies#order-of-operations, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-fast-direct` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, financial_planning#know-your-four-numbers, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v4-rerank` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, emergency_fund#the-rule-that-protects-everything-else, saving_strategies#automate-then-forget |

### q18 · saudi

- **AR:** المؤجر يبي الإيجار كامل مقدم، كيف أجهز له؟
- **EN (gold):** The landlord wants the full rent up front, how do I prepare for it?
- **Relevant:** `budgeting#the-50-30-20-rule-adapted-for-saudi-salaries`, `saving_strategies#sinking-funds-for-lumpy-costs`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `paying rent in advance, financial planning` (intent financial_question)
- **LLM translation:** `The landlord wants the full rent in advance, how can I prepare for it?` (intent financial_question)
- **Note:** Rent is not in the router map.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 8 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, budgeting#review-cadence |
| `minilm-router` | ❌ 8 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, budgeting#review-cadence |
| `minilm-llm-topic` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, financial_planning#know-your-four-numbers, islamic_finance#ijara-leasing |
| `minilm-llm-translation` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#ijara-leasing, saving_strategies#the-waiting-test |
| `minilm-gold-en` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#ijara-leasing, emergency_fund#rebuilding-after-you-use-it |
| `ml-minilm-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#ijara-leasing, saving_strategies#automate-then-forget |
| `cohere-v4-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, budgeting#build-the-budget-from-your-actual-cash-flow, islamic_finance#ijara-leasing |
| `cohere-v5-pro-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#ijara-leasing, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-fast-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#ijara-leasing, **saving_strategies#sinking-funds-for-lumpy-costs** |
| `cohere-v4-rerank` | ✅ 2 | islamic_finance#ijara-leasing, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, emergency_fund#where-to-keep-it |

### q24 · saudi

- **AR:** صرفت من فلوس الطوارى على تصليح المكيف، وش أسوي الحين؟
- **EN (gold):** I spent some of my emergency money fixing the air conditioner, what should I do now?
- **Relevant:** `emergency_fund#rebuilding-after-you-use-it`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `emergency fund replenishment` (intent financial_question)
- **LLM translation:** `I spent my emergency fund on fixing the air conditioner, what should I do now?` (intent financial_question)
- **Note:** Common hamza-less spelling الطوارى does not contain the key طوارئ.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 31 | budgeting#categories-that-quietly-leak-money, budgeting#intro, budgeting#build-the-budget-from-your-actual-cash-flow |
| `minilm-router` | ❌ 31 | budgeting#categories-that-quietly-leak-money, budgeting#intro, budgeting#build-the-budget-from-your-actual-cash-flow |
| `minilm-llm-topic` | ✅ 1 | **emergency_fund#rebuilding-after-you-use-it**, emergency_fund#intro, emergency_fund#the-rule-that-protects-everything-else |
| `minilm-llm-translation` | ✅ 1 | **emergency_fund#rebuilding-after-you-use-it**, emergency_fund#intro, emergency_fund#the-rule-that-protects-everything-else |
| `minilm-gold-en` | ✅ 1 | **emergency_fund#rebuilding-after-you-use-it**, emergency_fund#intro, emergency_fund#the-rule-that-protects-everything-else |
| `ml-minilm-direct` | ✅ 1 | **emergency_fund#rebuilding-after-you-use-it**, emergency_fund#the-rule-that-protects-everything-else, saving_strategies#the-waiting-test |
| `cohere-v4-direct` | ✅ 2 | financial_planning#plan-around-goals-not-products, **emergency_fund#rebuilding-after-you-use-it**, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-pro-direct` | ✅ 3 | emergency_fund#the-rule-that-protects-everything-else, saving_strategies#sinking-funds-for-lumpy-costs, **emergency_fund#rebuilding-after-you-use-it** |
| `cohere-v5-fast-direct` | ✅ 1 | **emergency_fund#rebuilding-after-you-use-it**, emergency_fund#how-much-is-enough, emergency_fund#the-rule-that-protects-everything-else |
| `cohere-v4-rerank` | ❌ 9 | budgeting#build-the-budget-from-your-actual-cash-flow, saving_strategies#the-waiting-test, saving_strategies#order-of-operations |

### q25 · saudi

- **AR:** أبي أحول جزء من معاشي أول ما ينزل لحساب ثاني، كيف أسويها؟
- **EN (gold):** I want to transfer part of my salary to another account as soon as it lands, how do I do that?
- **Relevant:** `saving_strategies#pay-yourself-first`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `transferring salary to another account` (intent financial_question)
- **LLM translation:** `I want to transfer part of my salary to another account as soon as it is deposited, how can I do that?` (intent financial_question)
- **Note:** معاش is everyday Saudi for salary; not in the map.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 9 | islamic_finance#intro, zakat#intro, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-router` | ❌ 9 | islamic_finance#intro, zakat#intro, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-llm-topic` | ✅ 3 | saving_strategies#automate-then-forget, financial_planning#know-your-four-numbers, **saving_strategies#pay-yourself-first** |
| `minilm-llm-translation` | ✅ 2 | saving_strategies#automate-then-forget, **saving_strategies#pay-yourself-first**, financial_planning#know-your-four-numbers |
| `minilm-gold-en` | ✅ 2 | saving_strategies#automate-then-forget, **saving_strategies#pay-yourself-first**, financial_planning#know-your-four-numbers |
| `ml-minilm-direct` | ✅ 1 | **saving_strategies#pay-yourself-first**, saving_strategies#automate-then-forget, zakat#intro |
| `cohere-v4-direct` | ❌ 14 | financial_planning#plan-around-goals-not-products, emergency_fund#rebuilding-after-you-use-it, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-pro-direct` | ✅ 1 | **saving_strategies#pay-yourself-first**, saving_strategies#sinking-funds-for-lumpy-costs, saving_strategies#automate-then-forget |
| `cohere-v5-fast-direct` | ❌ 4 | zakat#how-a-large-purchase-affects-your-zakat-base, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, zakat#the-calculation |
| `cohere-v4-rerank` | ✅ 1 | **saving_strategies#pay-yourself-first**, zakat#how-a-large-purchase-affects-your-zakat-base, budgeting#review-cadence |

### q27 · saudi

- **AR:** كم تطلع زكاتي إذا عندي ربع مليون بالبنك؟
- **EN (gold):** How much would my zakat be if I have a quarter of a million in the bank?
- **Relevant:** `zakat#the-calculation`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `zakat calculation bank balance` (intent financial_question)
- **LLM translation:** `How much zakat do I owe if I have 250,000 SAR in the bank?` (intent financial_question)
- **Note:** زكاتي (my zakat): the possessive turns ة into ت, so the key زكاة does not match.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 29 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#ijara-leasing |
| `minilm-router` | ❌ 29 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#ijara-leasing |
| `minilm-llm-topic` | ✅ 1 | **zakat#the-calculation**, zakat#intro, zakat#the-nisab-threshold |
| `minilm-llm-translation` | ✅ 1 | **zakat#the-calculation**, zakat#how-a-large-purchase-affects-your-zakat-base, zakat#what-you-pay-zakat-on |
| `minilm-gold-en` | ✅ 1 | **zakat#the-calculation**, zakat#the-nisab-threshold, zakat#what-you-pay-zakat-on |
| `ml-minilm-direct` | ✅ 1 | **zakat#the-calculation**, zakat#the-nisab-threshold, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v4-direct` | ✅ 1 | **zakat#the-calculation**, zakat#the-nisab-threshold, zakat#what-you-pay-zakat-on |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#the-calculation**, zakat#the-nisab-threshold, zakat#intro |
| `cohere-v5-fast-direct` | ✅ 1 | **zakat#the-calculation**, zakat#what-you-pay-zakat-on, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v4-rerank` | ✅ 1 | **zakat#the-calculation**, zakat#how-a-large-purchase-affects-your-zakat-base, zakat#intro |

### q28 · saudi

- **AR:** أنا مقيم وإقامتي مربوطة بالشغل، كم شهر لازم أحتاط؟
- **EN (gold):** I'm an expat and my residency is tied to my job, how many months should I keep in reserve?
- **Relevant:** `emergency_fund#how-much-is-enough`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `emergency fund for expat tied to work` (intent financial_question)
- **LLM translation:** `I am a resident and my residency is tied to my job, how many months should I save for as a precaution?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 31 | budgeting#categories-that-quietly-leak-money, islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-router` | ❌ 31 | budgeting#categories-that-quietly-leak-money, islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-llm-topic` | ✅ 2 | emergency_fund#intro, **emergency_fund#how-much-is-enough**, emergency_fund#where-to-keep-it |
| `minilm-llm-translation` | ✅ 1 | **emergency_fund#how-much-is-enough**, saving_strategies#the-waiting-test, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries |
| `minilm-gold-en` | ✅ 1 | **emergency_fund#how-much-is-enough**, saving_strategies#the-waiting-test, emergency_fund#where-to-keep-it |
| `ml-minilm-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, saving_strategies#the-waiting-test, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries |
| `cohere-v4-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, saving_strategies#the-waiting-test, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries |
| `cohere-v5-pro-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, saving_strategies#sinking-funds-for-lumpy-costs |
| `cohere-v5-fast-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, saving_strategies#sinking-funds-for-lumpy-costs |
| `cohere-v4-rerank` | ✅ 1 | **emergency_fund#how-much-is-enough**, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, saving_strategies#the-waiting-test |

### q30 · saudi

- **AR:** أسكن في المدينة وأبي أعرف كم المفروض أصرف على السكن من راتبي
- **EN (gold):** I live in Madinah and want to know how much of my salary I should spend on housing
- **Relevant:** `budgeting#intro`, `budgeting#the-50-30-20-rule-adapted-for-saudi-salaries`
- **Keyword router:** `salary income debt` (matched راتب, دين)
- **LLM topic_en:** `housing budget percentage of salary` (intent financial_question)
- **LLM translation:** `I live in the city and I want to know how much I should spend on housing from my salary.` (intent financial_question)
- **Note:** False positive: المدينة contains the key دين, so the router adds 'debt'.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 8 | islamic_finance#murabaha-cost-plus-sale, budgeting#categories-that-quietly-leak-money, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-router` | ❌ 5 | financial_planning#know-your-four-numbers, budgeting#build-the-budget-from-your-actual-cash-flow, zakat#what-you-pay-zakat-on |
| `minilm-llm-topic` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, financial_planning#know-your-four-numbers, budgeting#build-the-budget-from-your-actual-cash-flow |
| `minilm-llm-translation` | ✅ 2 | financial_planning#know-your-four-numbers, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, emergency_fund#how-much-is-enough |
| `minilm-gold-en` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, financial_planning#know-your-four-numbers, emergency_fund#how-much-is-enough |
| `ml-minilm-direct` | ✅ 2 | saving_strategies#automate-then-forget, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, saving_strategies#pay-yourself-first |
| `cohere-v4-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, financial_planning#know-your-four-numbers, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-pro-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, **budgeting#intro**, emergency_fund#how-much-is-enough |
| `cohere-v5-fast-direct` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, **budgeting#intro**, emergency_fund#how-much-is-enough |
| `cohere-v4-rerank` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, saving_strategies#sinking-funds-for-lumpy-costs, emergency_fund#how-much-is-enough |

### q32 · saudi

- **AR:** هل آخذ قروض شخصية عشان أدفع الإيجار؟
- **EN (gold):** Should I take personal loans to pay the rent?
- **Relevant:** `budgeting#the-50-30-20-rule-adapted-for-saudi-salaries`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `personal loans for rent payment` (intent financial_question)
- **LLM translation:** `Should I take out personal loans to pay my rent?` (intent financial_question)
- **Note:** Plural قروض does not contain the key قرض.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 24 | budgeting#categories-that-quietly-leak-money, budgeting#intro, islamic_finance#intro |
| `minilm-router` | ❌ 24 | budgeting#categories-that-quietly-leak-money, budgeting#intro, islamic_finance#intro |
| `minilm-llm-topic` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#ijara-leasing, islamic_finance#practical-guidance |
| `minilm-llm-translation` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#ijara-leasing, car_financing#paying-cash |
| `minilm-gold-en` | ✅ 1 | **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#ijara-leasing, car_financing#paying-cash |
| `ml-minilm-direct` | ✅ 3 | islamic_finance#ijara-leasing, car_financing#conventional-riba-based-auto-loans, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries** |
| `cohere-v4-direct` | ❌ 5 | islamic_finance#ijara-leasing, budgeting#build-the-budget-from-your-actual-cash-flow, saving_strategies#sinking-funds-for-lumpy-costs |
| `cohere-v5-pro-direct` | ✅ 2 | car_financing#the-decision-rule, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-fast-direct` | ✅ 2 | islamic_finance#ijara-leasing, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, islamic_finance#practical-guidance |
| `cohere-v4-rerank` | ✅ 2 | islamic_finance#ijara-leasing, **budgeting#the-50-30-20-rule-adapted-for-saudi-salaries**, zakat#what-you-pay-zakat-on |

### q33 · saudi

- **AR:** البنك قال لي نسبة الربح ٥٪ ثابتة، كيف أعرف كم بدفع بالمجموع؟
- **EN (gold):** The bank told me the profit rate is a flat 5%, how do I know how much I'll pay in total?
- **Relevant:** `car_financing#murabaha-the-standard-islamic-auto-finance`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `murabaha financing calculation fixed profit rate` (intent financial_question)
- **LLM translation:** `The bank told me the profit rate is 5% fixed, how do I know how much I will pay in total?` (intent financial_question)
- **Note:** Tests the flat-rate ambiguity paragraph; no router keyword.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 8 | islamic_finance#intro, islamic_finance#takaful-cooperative-insurance, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-router` | ❌ 8 | islamic_finance#intro, islamic_finance#takaful-cooperative-insurance, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-llm-topic` | ✅ 2 | islamic_finance#murabaha-cost-plus-sale, **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#practical-guidance |
| `minilm-llm-translation` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, financial_planning#intro |
| `minilm-gold-en` | ✅ 3 | financial_planning#intro, islamic_finance#murabaha-cost-plus-sale, **car_financing#murabaha-the-standard-islamic-auto-finance** |
| `ml-minilm-direct` | ❌ 27 | financial_planning#know-your-four-numbers, saving_strategies#pay-yourself-first, financial_planning#a-financial-health-score |
| `cohere-v4-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, car_financing#conventional-riba-based-auto-loans |
| `cohere-v5-pro-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, car_financing#conventional-riba-based-auto-loans |
| `cohere-v5-fast-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, car_financing#conventional-riba-based-auto-loans |
| `cohere-v4-rerank` | ✅ 2 | islamic_finance#murabaha-cost-plus-sale, **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans |

### q34 · saudi

- **AR:** هل أي منتج مكتوب عليه اسلامي يكون متوافق مع الشريعة؟
- **EN (gold):** Is any product labelled Islamic actually Shariah-compliant?
- **Relevant:** `islamic_finance#practical-guidance`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `sharia compliance of islamic financial products` (intent financial_question)
- **LLM translation:** `Is every product labeled as Islamic Sharia-compliant?` (intent financial_question)
- **Note:** Hamza-less اسلامي does not contain the key إسلامي.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 20 | budgeting#categories-that-quietly-leak-money, budgeting#intro, islamic_finance#intro |
| `minilm-router` | ❌ 20 | budgeting#categories-that-quietly-leak-money, budgeting#intro, islamic_finance#intro |
| `minilm-llm-topic` | ✅ 1 | **islamic_finance#practical-guidance**, islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-llm-translation` | ✅ 1 | **islamic_finance#practical-guidance**, islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-gold-en` | ✅ 1 | **islamic_finance#practical-guidance**, islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale |
| `ml-minilm-direct` | ✅ 1 | **islamic_finance#practical-guidance**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#intro |
| `cohere-v4-direct` | ✅ 1 | **islamic_finance#practical-guidance**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#the-three-prohibitions |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#practical-guidance**, islamic_finance#the-three-prohibitions, islamic_finance#takaful-cooperative-insurance |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#practical-guidance**, islamic_finance#the-three-prohibitions, islamic_finance#intro |
| `cohere-v4-rerank` | ✅ 1 | **islamic_finance#practical-guidance**, islamic_finance#ijara-leasing, car_financing#conventional-riba-based-auto-loans |

### q35 · saudi

- **AR:** التأمين على السيارة، هل هو حلال؟
- **EN (gold):** Is car insurance halal?
- **Relevant:** `islamic_finance#takaful-cooperative-insurance`
- **Keyword router:** `car vehicle islamic finance halal` (matched سيارة, حلال)
- **LLM topic_en:** `is car insurance halal` (intent financial_question)
- **LLM translation:** `Is car insurance halal?` (intent financial_question)
- **Note:** Router sends 'car vehicle islamic finance halal'; the answer is the takaful section.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 10 | budgeting#intro, budgeting#categories-that-quietly-leak-money, zakat#intro |
| `minilm-router` | ❌ 12 | car_financing#intro, car_financing#murabaha-the-standard-islamic-auto-finance, islamic_finance#murabaha-cost-plus-sale |
| `minilm-llm-topic` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#the-three-prohibitions, car_financing#the-decision-rule |
| `minilm-llm-translation` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#the-three-prohibitions, car_financing#the-decision-rule |
| `minilm-gold-en` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#the-three-prohibitions, car_financing#the-decision-rule |
| `ml-minilm-direct` | ❌ 7 | car_financing#conventional-riba-based-auto-loans, car_financing#the-decision-rule, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v4-direct` | ❌ 4 | islamic_finance#ijara-leasing, islamic_finance#the-three-prohibitions, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, islamic_finance#the-three-prohibitions, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#takaful-cooperative-insurance**, car_financing#murabaha-the-standard-islamic-auto-finance, islamic_finance#ijara-leasing |
| `cohere-v4-rerank` | ✅ 3 | zakat#what-you-pay-zakat-on, zakat#how-a-large-purchase-affects-your-zakat-base, **islamic_finance#takaful-cooperative-insurance** |

### q37 · terminology

- **AR:** هل التمويل الشخصي عن طريق التورق حلال؟
- **EN (gold):** Is personal financing through tawarruq halal?
- **Relevant:** `islamic_finance#murabaha-cost-plus-sale`
- **Keyword router:** `financing loan islamic finance halal` (matched تمويل, حلال)
- **LLM topic_en:** `is tawarruq financing halal` (intent financial_question)
- **LLM translation:** `Is personal financing through tawarruq halal?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 5 | zakat#intro, islamic_finance#intro, budgeting#intro |
| `minilm-router` | ❌ 4 | islamic_finance#practical-guidance, islamic_finance#intro, islamic_finance#the-three-prohibitions |
| `minilm-llm-topic` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#the-three-prohibitions, islamic_finance#practical-guidance |
| `minilm-llm-translation` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#the-three-prohibitions, islamic_finance#practical-guidance |
| `minilm-gold-en` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#the-three-prohibitions, islamic_finance#practical-guidance |
| `ml-minilm-direct` | ❌ 6 | islamic_finance#the-three-prohibitions, financial_planning#vision-2030-context, car_financing#paying-cash |
| `cohere-v4-direct` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#ijara-leasing, islamic_finance#the-three-prohibitions |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#the-three-prohibitions, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-fast-direct` | ✅ 2 | islamic_finance#the-three-prohibitions, **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#practical-guidance |
| `cohere-v4-rerank` | ❌ 9 | zakat#how-a-large-purchase-affects-your-zakat-base, zakat#what-you-pay-zakat-on, zakat#intro |

### q38 · terminology

- **AR:** وش يعني تورق؟
- **EN (gold):** What does tawarruq mean?
- **Relevant:** `islamic_finance#murabaha-cost-plus-sale`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `what is tawarruq financing` (intent financial_question)
- **LLM translation:** `What does Tawaruq mean?` (intent financial_question)
- **Note:** Hardest case: single rare term, absent from router map, one mention in corpus.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 5 | budgeting#intro, budgeting#categories-that-quietly-leak-money, islamic_finance#intro |
| `minilm-router` | ❌ 5 | budgeting#intro, budgeting#categories-that-quietly-leak-money, islamic_finance#intro |
| `minilm-llm-topic` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#takaful-cooperative-insurance, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-llm-translation` | ✅ 3 | islamic_finance#takaful-cooperative-insurance, islamic_finance#mudaraba-and-musharaka-partnership, **islamic_finance#murabaha-cost-plus-sale** |
| `minilm-gold-en` | ✅ 3 | islamic_finance#takaful-cooperative-insurance, islamic_finance#mudaraba-and-musharaka-partnership, **islamic_finance#murabaha-cost-plus-sale** |
| `ml-minilm-direct` | ✅ 2 | islamic_finance#ijara-leasing, **islamic_finance#murabaha-cost-plus-sale**, zakat#intro |
| `cohere-v4-direct` | ❌ 5 | islamic_finance#ijara-leasing, islamic_finance#the-three-prohibitions, islamic_finance#mudaraba-and-musharaka-partnership |
| `cohere-v5-pro-direct` | ✅ 2 | islamic_finance#takaful-cooperative-insurance, **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#ijara-leasing |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, islamic_finance#takaful-cooperative-insurance, islamic_finance#mudaraba-and-musharaka-partnership |
| `cohere-v4-rerank` | ❌ 4 | zakat#intro, islamic_finance#mudaraba-and-musharaka-partnership, emergency_fund#intro |

### q42 · terminology

- **AR:** هل ينقطع الحول إذا نزل مالي عن النصاب قبل تمام السنة؟
- **EN (gold):** Is the hawl interrupted if my wealth drops below nisab before the year is complete?
- **Relevant:** `zakat#the-nisab-threshold`, `zakat#intro`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `zakat nisab calculation` (intent financial_question)
- **LLM translation:** `Does the hawla (zakat year) break if my wealth falls below the nisab before the year is complete?` (intent financial_question)
- **Note:** Fiqh terms حول / نصاب, neither in the router map.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 9 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, islamic_finance#ijara-leasing |
| `minilm-router` | ❌ 9 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, islamic_finance#ijara-leasing |
| `minilm-llm-topic` | ✅ 1 | **zakat#the-nisab-threshold**, zakat#the-calculation, **zakat#intro** |
| `minilm-llm-translation` | ✅ 1 | **zakat#intro**, zakat#what-you-pay-zakat-on, **zakat#the-nisab-threshold** |
| `minilm-gold-en` | ✅ 1 | **zakat#the-nisab-threshold**, zakat#the-calculation, **zakat#intro** |
| `ml-minilm-direct` | ❌ 31 | financial_planning#vision-2030-context, car_financing#paying-cash, emergency_fund#where-to-keep-it |
| `cohere-v4-direct` | ✅ 2 | zakat#how-a-large-purchase-affects-your-zakat-base, **zakat#the-nisab-threshold**, **zakat#intro** |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#the-nisab-threshold**, **zakat#intro**, zakat#the-calculation |
| `cohere-v5-fast-direct` | ✅ 1 | **zakat#the-nisab-threshold**, **zakat#intro**, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v4-rerank` | ✅ 1 | **zakat#the-nisab-threshold**, zakat#how-a-large-purchase-affects-your-zakat-base, **zakat#intro** |

### q43 · terminology

- **AR:** ما المقصود بالغرر والميسر في المعاملات المالية؟
- **EN (gold):** What is meant by gharar and maysir in financial transactions?
- **Relevant:** `islamic_finance#the-three-prohibitions`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `gharar and maisir in financial transactions` (intent financial_question)
- **LLM translation:** `What is meant by Gharar and Maisir in financial transactions?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 23 | islamic_finance#murabaha-cost-plus-sale, budgeting#categories-that-quietly-leak-money, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-router` | ❌ 23 | islamic_finance#murabaha-cost-plus-sale, budgeting#categories-that-quietly-leak-money, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-llm-topic` | ✅ 2 | islamic_finance#takaful-cooperative-insurance, **islamic_finance#the-three-prohibitions**, islamic_finance#murabaha-cost-plus-sale |
| `minilm-llm-translation` | ✅ 3 | islamic_finance#takaful-cooperative-insurance, islamic_finance#mudaraba-and-musharaka-partnership, **islamic_finance#the-three-prohibitions** |
| `minilm-gold-en` | ✅ 3 | islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#takaful-cooperative-insurance, **islamic_finance#the-three-prohibitions** |
| `ml-minilm-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, emergency_fund#the-rule-that-protects-everything-else, financial_planning#vision-2030-context |
| `cohere-v4-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#takaful-cooperative-insurance, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership |
| `cohere-v4-rerank` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#murabaha-cost-plus-sale |

### q46 · terminology

- **AR:** ما هي الإجارة المنتهية بالتمليك؟
- **EN (gold):** What is ijara muntahia bittamleek (lease ending in ownership)?
- **Relevant:** `islamic_finance#ijara-leasing`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `ijara muntahia bi tamleek financing explanation` (intent financial_question)
- **LLM translation:** `What is Ijarah Muntahia bi Al-Tamlik?` (intent financial_question)
- **Note:** Absent from router map.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 7 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-router` | ❌ 7 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-llm-topic` | ✅ 2 | islamic_finance#murabaha-cost-plus-sale, **islamic_finance#ijara-leasing**, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-llm-translation` | ✅ 3 | islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#murabaha-cost-plus-sale, **islamic_finance#ijara-leasing** |
| `minilm-gold-en` | ✅ 1 | **islamic_finance#ijara-leasing**, islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#murabaha-cost-plus-sale |
| `ml-minilm-direct` | ❌ 4 | car_financing#conventional-riba-based-auto-loans, car_financing#murabaha-the-standard-islamic-auto-finance, emergency_fund#where-to-keep-it |
| `cohere-v4-direct` | ✅ 1 | **islamic_finance#ijara-leasing**, islamic_finance#murabaha-cost-plus-sale, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#ijara-leasing**, islamic_finance#murabaha-cost-plus-sale, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#ijara-leasing**, islamic_finance#murabaha-cost-plus-sale, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v4-rerank` | ✅ 1 | **islamic_finance#ijara-leasing**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership |

### q51 · ambiguous

- **AR:** من وين أبدأ عشان أرتب وضعي المالي؟
- **EN (gold):** Where do I start to get my finances in order?
- **Relevant:** `saving_strategies#order-of-operations`, `financial_planning#know-your-four-numbers`, `financial_planning#plan-around-goals-not-products`, `budgeting#build-the-budget-from-your-actual-cash-flow`
- **Keyword router:** **fell back** → raw Arabic
- **LLM topic_en:** `financial planning, budgeting, getting started` (intent financial_question)
- **LLM translation:** `Where should I start to organize my financial situation?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 5 | budgeting#categories-that-quietly-leak-money, budgeting#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-router` | ❌ 5 | budgeting#categories-that-quietly-leak-money, budgeting#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-llm-topic` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, financial_planning#intro, **financial_planning#know-your-four-numbers** |
| `minilm-llm-translation` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, financial_planning#intro, saving_strategies#automate-then-forget |
| `minilm-gold-en` | ✅ 1 | **financial_planning#plan-around-goals-not-products**, saving_strategies#automate-then-forget, **saving_strategies#order-of-operations** |
| `ml-minilm-direct` | ✅ 1 | **financial_planning#know-your-four-numbers**, financial_planning#a-financial-health-score, **financial_planning#plan-around-goals-not-products** |
| `cohere-v4-direct` | ✅ 1 | **budgeting#build-the-budget-from-your-actual-cash-flow**, **financial_planning#know-your-four-numbers**, **saving_strategies#order-of-operations** |
| `cohere-v5-pro-direct` | ✅ 1 | **saving_strategies#order-of-operations**, **financial_planning#plan-around-goals-not-products**, **budgeting#build-the-budget-from-your-actual-cash-flow** |
| `cohere-v5-fast-direct` | ✅ 1 | **saving_strategies#order-of-operations**, **financial_planning#plan-around-goals-not-products**, **budgeting#build-the-budget-from-your-actual-cash-flow** |
| `cohere-v4-rerank` | ✅ 1 | **budgeting#build-the-budget-from-your-actual-cash-flow**, saving_strategies#pay-yourself-first, **saving_strategies#order-of-operations** |


<a id="minilm-llm-topic__miss__minilm-router__hit"></a>
## `minilm-llm-topic` misses @3, `minilm-router` hits @3 (0)


<a id="minilm-llm-topic__miss__cohere-v4-direct__hit"></a>
## `minilm-llm-topic` misses @3, `cohere-v4-direct` hits @3 (2)

### q04 · msa

- **AR:** ما المبلغ الذي ينبغي الاحتفاظ به في صندوق الطوارئ؟
- **EN (gold):** How much money should be kept in an emergency fund?
- **Relevant:** `emergency_fund#how-much-is-enough`
- **Keyword router:** `emergency fund` (matched طوارئ)
- **LLM topic_en:** `emergency fund amount` (intent financial_question)
- **LLM translation:** `How much money should I keep in an emergency fund?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 32 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#practical-guidance |
| `minilm-router` | ❌ 5 | emergency_fund#intro, emergency_fund#rebuilding-after-you-use-it, emergency_fund#the-rule-that-protects-everything-else |
| `minilm-llm-topic` | ❌ 5 | emergency_fund#intro, emergency_fund#rebuilding-after-you-use-it, emergency_fund#the-rule-that-protects-everything-else |
| `minilm-llm-translation` | ❌ 5 | emergency_fund#intro, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#rebuilding-after-you-use-it |
| `minilm-gold-en` | ❌ 5 | emergency_fund#intro, emergency_fund#rebuilding-after-you-use-it, emergency_fund#the-rule-that-protects-everything-else |
| `ml-minilm-direct` | ✅ 2 | emergency_fund#intro, **emergency_fund#how-much-is-enough**, emergency_fund#the-rule-that-protects-everything-else |
| `cohere-v4-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, emergency_fund#where-to-keep-it, emergency_fund#intro |
| `cohere-v5-pro-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#intro |
| `cohere-v5-fast-direct` | ✅ 1 | **emergency_fund#how-much-is-enough**, emergency_fund#where-to-keep-it, emergency_fund#the-rule-that-protects-everything-else |
| `cohere-v4-rerank` | ✅ 1 | **emergency_fund#how-much-is-enough**, emergency_fund#the-rule-that-protects-everything-else, emergency_fund#where-to-keep-it |

### q26 · saudi

- **AR:** أسدد القرض الشخصي أول ولا أبدأ أحوش؟
- **EN (gold):** Should I pay off the personal loan first or start saving?
- **Relevant:** `saving_strategies#order-of-operations`
- **Keyword router:** `loan debt` (matched قرض)
- **LLM topic_en:** `debt repayment vs saving` (intent financial_question)
- **LLM translation:** `Should I pay off my personal loan first or start saving?` (intent financial_question)
- **Note:** أحوش (dialect: to save up) is not in the map; only قرض matches.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 11 | budgeting#categories-that-quietly-leak-money, budgeting#intro, budgeting#review-cadence |
| `minilm-router` | ❌ 27 | car_financing#conventional-riba-based-auto-loans, car_financing#murabaha-the-standard-islamic-auto-finance, islamic_finance#the-three-prohibitions |
| `minilm-llm-topic` | ❌ 13 | zakat#the-calculation, zakat#what-you-pay-zakat-on, car_financing#the-decision-rule |
| `minilm-llm-translation` | ❌ 4 | financial_planning#plan-around-goals-not-products, saving_strategies#the-waiting-test, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries |
| `minilm-gold-en` | ❌ 5 | financial_planning#plan-around-goals-not-products, saving_strategies#the-waiting-test, emergency_fund#the-rule-that-protects-everything-else |
| `ml-minilm-direct` | ❌ 8 | car_financing#paying-cash, emergency_fund#the-rule-that-protects-everything-else, saving_strategies#pay-yourself-first |
| `cohere-v4-direct` | ✅ 1 | **saving_strategies#order-of-operations**, budgeting#build-the-budget-from-your-actual-cash-flow, saving_strategies#sinking-funds-for-lumpy-costs |
| `cohere-v5-pro-direct` | ✅ 1 | **saving_strategies#order-of-operations**, car_financing#paying-cash, car_financing#the-decision-rule |
| `cohere-v5-fast-direct` | ✅ 1 | **saving_strategies#order-of-operations**, car_financing#the-decision-rule, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v4-rerank` | ✅ 1 | **saving_strategies#order-of-operations**, budgeting#build-the-budget-from-your-actual-cash-flow, islamic_finance#murabaha-cost-plus-sale |


<a id="cohere-v4-direct__miss__minilm-llm-topic__hit"></a>
## `cohere-v4-direct` misses @3, `minilm-llm-topic` hits @3 (1)

### q23 · saudi

- **AR:** كيف أجمع فلوس العمرة بدون ما أتسلف؟
- **EN (gold):** How do I save up money for Umrah without borrowing?
- **Relevant:** `saving_strategies#sinking-funds-for-lumpy-costs`
- **Keyword router:** `goal saving umrah` (matched عمرة)
- **LLM topic_en:** `saving for umrah without borrowing` (intent financial_question)
- **LLM translation:** `How can I save money for Umrah without borrowing?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 4 | budgeting#categories-that-quietly-leak-money, budgeting#review-cadence, islamic_finance#murabaha-cost-plus-sale |
| `minilm-router` | ✅ 1 | **saving_strategies#sinking-funds-for-lumpy-costs**, saving_strategies#order-of-operations, emergency_fund#rebuilding-after-you-use-it |
| `minilm-llm-topic` | ✅ 1 | **saving_strategies#sinking-funds-for-lumpy-costs**, saving_strategies#order-of-operations, saving_strategies#automate-then-forget |
| `minilm-llm-translation` | ✅ 1 | **saving_strategies#sinking-funds-for-lumpy-costs**, saving_strategies#order-of-operations, saving_strategies#automate-then-forget |
| `minilm-gold-en` | ✅ 1 | **saving_strategies#sinking-funds-for-lumpy-costs**, saving_strategies#order-of-operations, saving_strategies#automate-then-forget |
| `ml-minilm-direct` | ❌ 7 | saving_strategies#automate-then-forget, budgeting#intro, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v4-direct` | ❌ 5 | budgeting#build-the-budget-from-your-actual-cash-flow, saving_strategies#automate-then-forget, saving_strategies#order-of-operations |
| `cohere-v5-pro-direct` | ✅ 1 | **saving_strategies#sinking-funds-for-lumpy-costs**, saving_strategies#automate-then-forget, saving_strategies#order-of-operations |
| `cohere-v5-fast-direct` | ✅ 1 | **saving_strategies#sinking-funds-for-lumpy-costs**, saving_strategies#automate-then-forget, saving_strategies#pay-yourself-first |
| `cohere-v4-rerank` | ✅ 1 | **saving_strategies#sinking-funds-for-lumpy-costs**, zakat#the-calculation, zakat#what-you-pay-zakat-on |


<a id="minilm-router__miss__cohere-v4-direct__hit"></a>
## `minilm-router` misses @3, `cohere-v4-direct` hits @3 (0)


<a id="cohere-v4-direct__miss__minilm-router__hit"></a>
## `cohere-v4-direct` misses @3, `minilm-router` hits @3 (0)


<a id="other"></a>
## Other disagreements @3 (20)

### q01 · msa

- **AR:** ما هو الحد الأدنى من الثروة الذي تجب فيه الزكاة؟
- **EN (gold):** What is the minimum amount of wealth on which zakat becomes due?
- **Relevant:** `zakat#the-nisab-threshold`
- **Keyword router:** `zakat` (matched زكاة)
- **LLM topic_en:** `zakat minimum wealth threshold` (intent financial_question)
- **LLM translation:** `What is the minimum wealth threshold for zakat to be obligatory?` (intent financial_question)
- **Note:** Describes nisab without using the word.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 22 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-router` | ✅ 3 | zakat#intro, zakat#what-you-pay-zakat-on, **zakat#the-nisab-threshold** |
| `minilm-llm-topic` | ✅ 3 | zakat#intro, zakat#what-you-pay-zakat-on, **zakat#the-nisab-threshold** |
| `minilm-llm-translation` | ✅ 3 | zakat#intro, zakat#what-you-pay-zakat-on, **zakat#the-nisab-threshold** |
| `minilm-gold-en` | ❌ 4 | zakat#intro, zakat#what-you-pay-zakat-on, zakat#the-calculation |
| `ml-minilm-direct` | ✅ 1 | **zakat#the-nisab-threshold**, zakat#the-calculation, zakat#intro |
| `cohere-v4-direct` | ✅ 1 | **zakat#the-nisab-threshold**, zakat#what-you-pay-zakat-on, zakat#intro |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#the-nisab-threshold**, zakat#the-calculation, zakat#what-you-pay-zakat-on |
| `cohere-v5-fast-direct` | ✅ 2 | zakat#the-calculation, **zakat#the-nisab-threshold**, zakat#what-you-pay-zakat-on |
| `cohere-v4-rerank` | ✅ 1 | **zakat#the-nisab-threshold**, zakat#the-calculation, zakat#intro |

### q03 · msa

- **AR:** لماذا يُعد شراء السيارة نقداً الخيار الأرخص عادةً؟
- **EN (gold):** Why is buying a car in cash usually the cheapest option?
- **Relevant:** `car_financing#paying-cash`
- **Keyword router:** `car vehicle` (matched سيارة)
- **LLM topic_en:** `buying a car cash vs financing` (intent financial_question)
- **LLM translation:** `Why is buying a car in cash usually the cheapest option?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 20 | budgeting#intro, budgeting#categories-that-quietly-leak-money, budgeting#build-the-budget-from-your-actual-cash-flow |
| `minilm-router` | ✅ 2 | car_financing#intro, **car_financing#paying-cash**, zakat#how-a-large-purchase-affects-your-zakat-base |
| `minilm-llm-topic` | ✅ 1 | **car_financing#paying-cash**, car_financing#the-decision-rule, car_financing#murabaha-the-standard-islamic-auto-finance |
| `minilm-llm-translation` | ✅ 1 | **car_financing#paying-cash**, car_financing#the-decision-rule, car_financing#intro |
| `minilm-gold-en` | ✅ 1 | **car_financing#paying-cash**, car_financing#the-decision-rule, car_financing#intro |
| `ml-minilm-direct` | ✅ 1 | **car_financing#paying-cash**, car_financing#conventional-riba-based-auto-loans, car_financing#the-decision-rule |
| `cohere-v4-direct` | ✅ 1 | **car_financing#paying-cash**, car_financing#the-decision-rule, car_financing#conventional-riba-based-auto-loans |
| `cohere-v5-pro-direct` | ✅ 1 | **car_financing#paying-cash**, car_financing#the-decision-rule, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-fast-direct` | ✅ 1 | **car_financing#paying-cash**, car_financing#the-decision-rule, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v4-rerank` | ✅ 1 | **car_financing#paying-cash**, car_financing#the-decision-rule, saving_strategies#the-waiting-test |

### q06 · msa

- **AR:** هل تجب الزكاة على السيارة والمنزل المخصصين للاستعمال الشخصي؟
- **EN (gold):** Is zakat due on a car and a house kept for personal use?
- **Relevant:** `zakat#what-you-pay-zakat-on`, `zakat#how-a-large-purchase-affects-your-zakat-base`
- **Keyword router:** `car vehicle zakat` (matched سيارة, زكاة)
- **LLM topic_en:** `zakat on personal use car and house` (intent financial_question)
- **LLM translation:** `Is zakat obligatory on a car and a house that are for personal use?` (intent financial_question)
- **Note:** The exemption is stated in what-you-pay-zakat-on; the car example is in the purchase section.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 16 | budgeting#categories-that-quietly-leak-money, islamic_finance#takaful-cooperative-insurance, zakat#intro |
| `minilm-router` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, **zakat#what-you-pay-zakat-on** |
| `minilm-llm-topic` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, **zakat#what-you-pay-zakat-on** |
| `minilm-llm-translation` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, **zakat#what-you-pay-zakat-on** |
| `minilm-gold-en` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, **zakat#what-you-pay-zakat-on**, zakat#intro |
| `ml-minilm-direct` | ❌ 6 | car_financing#intro, car_financing#conventional-riba-based-auto-loans, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v4-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#the-calculation |
| `cohere-v5-fast-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#the-calculation |
| `cohere-v4-rerank` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro |

### q07 · msa

- **AR:** كيف يُحسب مقدار الزكاة الواجبة على المدخرات والاستثمارات؟
- **EN (gold):** How is the amount of zakat due on savings and investments calculated?
- **Relevant:** `zakat#the-calculation`
- **Keyword router:** `zakat savings investing investment` (matched زكاة, مدخرات, استثمار)
- **LLM topic_en:** `zakat calculation on savings and investments` (intent financial_question)
- **LLM translation:** `How is the amount of zakat due on savings and investments calculated?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 30 | budgeting#categories-that-quietly-leak-money, budgeting#build-the-budget-from-your-actual-cash-flow, saving_strategies#sinking-funds-for-lumpy-costs |
| `minilm-router` | ✅ 2 | zakat#intro, **zakat#the-calculation**, zakat#what-you-pay-zakat-on |
| `minilm-llm-topic` | ✅ 1 | **zakat#the-calculation**, zakat#intro, zakat#how-a-large-purchase-affects-your-zakat-base |
| `minilm-llm-translation` | ✅ 1 | **zakat#the-calculation**, zakat#intro, zakat#what-you-pay-zakat-on |
| `minilm-gold-en` | ✅ 1 | **zakat#the-calculation**, zakat#intro, zakat#what-you-pay-zakat-on |
| `ml-minilm-direct` | ✅ 1 | **zakat#the-calculation**, financial_planning#know-your-four-numbers, emergency_fund#how-much-is-enough |
| `cohere-v4-direct` | ✅ 1 | **zakat#the-calculation**, zakat#what-you-pay-zakat-on, zakat#intro |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#the-calculation**, zakat#what-you-pay-zakat-on, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v5-fast-direct` | ✅ 1 | **zakat#the-calculation**, zakat#what-you-pay-zakat-on, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v4-rerank` | ✅ 1 | **zakat#the-calculation**, zakat#intro, zakat#what-you-pay-zakat-on |

### q10 · msa

- **AR:** ما هي نسبة الدين إلى الدخل التي تُعد مقبولة؟
- **EN (gold):** What debt-to-income ratio is considered acceptable?
- **Relevant:** `financial_planning#know-your-four-numbers`
- **Keyword router:** `income salary debt` (matched دخل, دين)
- **LLM topic_en:** `debt to income ratio acceptable level` (intent financial_question)
- **LLM translation:** `What is the acceptable debt-to-income ratio?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 33 | budgeting#categories-that-quietly-leak-money, budgeting#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-router` | ✅ 1 | **financial_planning#know-your-four-numbers**, budgeting#build-the-budget-from-your-actual-cash-flow, saving_strategies#pay-yourself-first |
| `minilm-llm-topic` | ✅ 1 | **financial_planning#know-your-four-numbers**, budgeting#build-the-budget-from-your-actual-cash-flow, zakat#what-you-pay-zakat-on |
| `minilm-llm-translation` | ✅ 1 | **financial_planning#know-your-four-numbers**, zakat#what-you-pay-zakat-on, budgeting#build-the-budget-from-your-actual-cash-flow |
| `minilm-gold-en` | ✅ 1 | **financial_planning#know-your-four-numbers**, zakat#what-you-pay-zakat-on, budgeting#build-the-budget-from-your-actual-cash-flow |
| `ml-minilm-direct` | ✅ 3 | car_financing#conventional-riba-based-auto-loans, financial_planning#vision-2030-context, **financial_planning#know-your-four-numbers** |
| `cohere-v4-direct` | ✅ 2 | budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, **financial_planning#know-your-four-numbers**, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-pro-direct` | ✅ 1 | **financial_planning#know-your-four-numbers**, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, financial_planning#a-financial-health-score |
| `cohere-v5-fast-direct` | ✅ 1 | **financial_planning#know-your-four-numbers**, financial_planning#a-financial-health-score, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v4-rerank` | ✅ 1 | **financial_planning#know-your-four-numbers**, zakat#the-calculation, budgeting#build-the-budget-from-your-actual-cash-flow |

### q12 · msa

- **AR:** ما الرسوم الإدارية التي يسمح بها البنك المركزي على تمويل السيارات؟
- **EN (gold):** What administrative fees does the central bank allow on car financing?
- **Relevant:** `car_financing#murabaha-the-standard-islamic-auto-finance`
- **Keyword router:** `financing loan` (matched تمويل)
- **LLM topic_en:** `car financing administrative fees central bank regulations` (intent financial_question)
- **LLM translation:** `What are the administrative fees allowed by the central bank on car financing?` (intent financial_question)
- **Note:** Plural السيارات does not contain the key سيارة (ة vs ات), so only 'financing loan' is routed.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 16 | budgeting#categories-that-quietly-leak-money, islamic_finance#takaful-cooperative-insurance, islamic_finance#murabaha-cost-plus-sale |
| `minilm-router` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#practical-guidance, car_financing#conventional-riba-based-auto-loans |
| `minilm-llm-topic` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#the-decision-rule, car_financing#paying-cash |
| `minilm-llm-translation` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, car_financing#paying-cash |
| `minilm-gold-en` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, car_financing#paying-cash |
| `ml-minilm-direct` | ❌ 5 | car_financing#paying-cash, car_financing#conventional-riba-based-auto-loans, emergency_fund#the-rule-that-protects-everything-else |
| `cohere-v4-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, car_financing#paying-cash |
| `cohere-v5-pro-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-fast-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, car_financing#the-decision-rule |
| `cohere-v4-rerank` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#ijara-leasing, car_financing#paying-cash |

### q13 · msa

- **AR:** ما أهمية مراجعة الميزانية بشكل دوري ومتى يجب إعادة بنائها؟
- **EN (gold):** Why is it important to review the budget regularly, and when should it be rebuilt?
- **Relevant:** `budgeting#review-cadence`
- **Keyword router:** `budgeting budget` (matched ميزانية)
- **LLM topic_en:** `budget review importance and rebuilding` (intent financial_question)
- **LLM translation:** `What is the importance of reviewing the budget periodically and when should it be rebuilt?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 9 | budgeting#categories-that-quietly-leak-money, islamic_finance#mudaraba-and-musharaka-partnership, islamic_finance#murabaha-cost-plus-sale |
| `minilm-router` | ✅ 3 | budgeting#intro, budgeting#build-the-budget-from-your-actual-cash-flow, **budgeting#review-cadence** |
| `minilm-llm-topic` | ✅ 1 | **budgeting#review-cadence**, emergency_fund#rebuilding-after-you-use-it, budgeting#intro |
| `minilm-llm-translation` | ✅ 1 | **budgeting#review-cadence**, emergency_fund#rebuilding-after-you-use-it, budgeting#intro |
| `minilm-gold-en` | ✅ 1 | **budgeting#review-cadence**, budgeting#intro, emergency_fund#rebuilding-after-you-use-it |
| `ml-minilm-direct` | ✅ 1 | **budgeting#review-cadence**, emergency_fund#rebuilding-after-you-use-it, financial_planning#know-your-four-numbers |
| `cohere-v4-direct` | ✅ 1 | **budgeting#review-cadence**, emergency_fund#rebuilding-after-you-use-it, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v5-pro-direct` | ✅ 1 | **budgeting#review-cadence**, budgeting#build-the-budget-from-your-actual-cash-flow, emergency_fund#rebuilding-after-you-use-it |
| `cohere-v5-fast-direct` | ✅ 1 | **budgeting#review-cadence**, emergency_fund#rebuilding-after-you-use-it, budgeting#build-the-budget-from-your-actual-cash-flow |
| `cohere-v4-rerank` | ✅ 1 | **budgeting#review-cadence**, emergency_fund#rebuilding-after-you-use-it, budgeting#categories-that-quietly-leak-money |

### q19 · saudi

- **AR:** وش الأفضل أشتري السيارة كاش ولا بالأقساط؟
- **EN (gold):** Which is better, buying the car in cash or in installments?
- **Relevant:** `car_financing#paying-cash`, `car_financing#the-decision-rule`
- **Keyword router:** `car vehicle installment financing` (matched سيارة, أقساط)
- **LLM topic_en:** `buying a car cash vs financing` (intent purchase_simulation)
- **LLM translation:** `What is better, buying the car in cash or in installments?` (intent purchase_simulation)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 24 | budgeting#categories-that-quietly-leak-money, saving_strategies#pay-yourself-first, islamic_finance#murabaha-cost-plus-sale |
| `minilm-router` | ✅ 2 | car_financing#murabaha-the-standard-islamic-auto-finance, **car_financing#the-decision-rule**, **car_financing#paying-cash** |
| `minilm-llm-topic` | ✅ 1 | **car_financing#paying-cash**, **car_financing#the-decision-rule**, car_financing#murabaha-the-standard-islamic-auto-finance |
| `minilm-llm-translation` | ✅ 1 | **car_financing#paying-cash**, zakat#how-a-large-purchase-affects-your-zakat-base, **car_financing#the-decision-rule** |
| `minilm-gold-en` | ✅ 1 | **car_financing#paying-cash**, **car_financing#the-decision-rule**, zakat#how-a-large-purchase-affects-your-zakat-base |
| `ml-minilm-direct` | ✅ 1 | **car_financing#paying-cash**, car_financing#intro, **car_financing#the-decision-rule** |
| `cohere-v4-direct` | ✅ 1 | **car_financing#paying-cash**, **car_financing#the-decision-rule**, car_financing#conventional-riba-based-auto-loans |
| `cohere-v5-pro-direct` | ✅ 1 | **car_financing#paying-cash**, **car_financing#the-decision-rule**, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v5-fast-direct` | ✅ 1 | **car_financing#paying-cash**, **car_financing#the-decision-rule**, car_financing#murabaha-the-standard-islamic-auto-finance |
| `cohere-v4-rerank` | ✅ 1 | **car_financing#paying-cash**, **car_financing#the-decision-rule**, car_financing#murabaha-the-standard-islamic-auto-finance |

### q20 · saudi

- **AR:** اشتراكاتي في التطبيقات كثيرة، هل فعلاً تفرق بالميزانية؟
- **EN (gold):** I have a lot of app subscriptions, do they really make a difference to the budget?
- **Relevant:** `budgeting#categories-that-quietly-leak-money`
- **Keyword router:** `budgeting budget subscription recurring cost` (matched ميزانية, اشتراك)
- **LLM topic_en:** `budgeting for app subscriptions` (intent financial_question)
- **LLM translation:** `I have many app subscriptions, do they really make a difference in the budget?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale |
| `minilm-router` | ✅ 3 | budgeting#review-cadence, financial_planning#know-your-four-numbers, **budgeting#categories-that-quietly-leak-money** |
| `minilm-llm-topic` | ✅ 2 | financial_planning#know-your-four-numbers, **budgeting#categories-that-quietly-leak-money**, budgeting#review-cadence |
| `minilm-llm-translation` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, financial_planning#know-your-four-numbers, budgeting#review-cadence |
| `minilm-gold-en` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, financial_planning#know-your-four-numbers, budgeting#review-cadence |
| `ml-minilm-direct` | ❌ 5 | emergency_fund#the-rule-that-protects-everything-else, financial_planning#vision-2030-context, financial_planning#know-your-four-numbers |
| `cohere-v4-direct` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, budgeting#build-the-budget-from-your-actual-cash-flow, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries |
| `cohere-v5-pro-direct` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, budgeting#review-cadence, saving_strategies#sinking-funds-for-lumpy-costs |
| `cohere-v5-fast-direct` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, saving_strategies#sinking-funds-for-lumpy-costs, budgeting#intro |
| `cohere-v4-rerank` | ✅ 1 | **budgeting#categories-that-quietly-leak-money**, islamic_finance#practical-guidance, islamic_finance#murabaha-cost-plus-sale |

### q22 · saudi

- **AR:** راتبي زاد، وش أسوي بالزيادة عشان ما تروح على الكماليات؟
- **EN (gold):** My salary went up, what should I do with the raise so it doesn't go on luxuries?
- **Relevant:** `saving_strategies#automate-then-forget`
- **Keyword router:** `salary income` (matched راتب)
- **LLM topic_en:** `salary increase, budgeting, saving` (intent financial_question)
- **LLM translation:** `My salary has increased, what should I do with the increase so that it doesn't go towards luxuries?` (intent financial_question)
- **Note:** Router reduces this to 'salary income'.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 18 | islamic_finance#intro, islamic_finance#ijara-leasing, islamic_finance#takaful-cooperative-insurance |
| `minilm-router` | ✅ 3 | financial_planning#know-your-four-numbers, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, **saving_strategies#automate-then-forget** |
| `minilm-llm-topic` | ✅ 3 | financial_planning#know-your-four-numbers, saving_strategies#order-of-operations, **saving_strategies#automate-then-forget** |
| `minilm-llm-translation` | ✅ 1 | **saving_strategies#automate-then-forget**, financial_planning#know-your-four-numbers, saving_strategies#order-of-operations |
| `minilm-gold-en` | ✅ 1 | **saving_strategies#automate-then-forget**, saving_strategies#pay-yourself-first, financial_planning#know-your-four-numbers |
| `ml-minilm-direct` | ✅ 3 | financial_planning#vision-2030-context, financial_planning#a-financial-health-score, **saving_strategies#automate-then-forget** |
| `cohere-v4-direct` | ✅ 1 | **saving_strategies#automate-then-forget**, zakat#how-a-large-purchase-affects-your-zakat-base, financial_planning#plan-around-goals-not-products |
| `cohere-v5-pro-direct` | ✅ 1 | **saving_strategies#automate-then-forget**, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries, saving_strategies#pay-yourself-first |
| `cohere-v5-fast-direct` | ✅ 1 | **saving_strategies#automate-then-forget**, saving_strategies#pay-yourself-first, budgeting#the-50-30-20-rule-adapted-for-saudi-salaries |
| `cohere-v4-rerank` | ✅ 1 | **saving_strategies#automate-then-forget**, saving_strategies#pay-yourself-first, saving_strategies#order-of-operations |

### q39 · terminology

- **AR:** كيف تُحسب نسبة الربح في مرابحة السيارات؟
- **EN (gold):** How is the profit rate calculated in car murabaha?
- **Relevant:** `car_financing#murabaha-the-standard-islamic-auto-finance`
- **Keyword router:** `murabaha islamic financing` (matched مرابحة)
- **LLM topic_en:** `how murabaha car financing profit is calculated` (intent financial_question)
- **LLM translation:** `How is the profit rate calculated in car murabaha?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 14 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, saving_strategies#pay-yourself-first |
| `minilm-router` | ✅ 3 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#practical-guidance, **car_financing#murabaha-the-standard-islamic-auto-finance** |
| `minilm-llm-topic` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, car_financing#the-decision-rule |
| `minilm-llm-translation` | ✅ 2 | islamic_finance#murabaha-cost-plus-sale, **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans |
| `minilm-gold-en` | ✅ 2 | islamic_finance#murabaha-cost-plus-sale, **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans |
| `ml-minilm-direct` | ❌ 7 | car_financing#conventional-riba-based-auto-loans, zakat#how-a-large-purchase-affects-your-zakat-base, car_financing#the-decision-rule |
| `cohere-v4-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, car_financing#the-decision-rule |
| `cohere-v5-pro-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, car_financing#conventional-riba-based-auto-loans |
| `cohere-v5-fast-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, car_financing#conventional-riba-based-auto-loans |
| `cohere-v4-rerank` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, car_financing#conventional-riba-based-auto-loans |

### q40 · terminology

- **AR:** هل يحق لي تخفيض عند السداد المبكر لتمويل المرابحة؟
- **EN (gold):** Am I entitled to a rebate on early settlement of murabaha financing?
- **Relevant:** `car_financing#murabaha-the-standard-islamic-auto-finance`
- **Keyword router:** `financing loan murabaha islamic` (matched تمويل, مرابحة)
- **LLM topic_en:** `murabaha financing early repayment discount` (intent financial_question)
- **LLM translation:** `Am I entitled to a discount for early settlement of a Murabaha financing?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 13 | budgeting#categories-that-quietly-leak-money, budgeting#intro, budgeting#build-the-budget-from-your-actual-cash-flow |
| `minilm-router` | ✅ 3 | islamic_finance#practical-guidance, islamic_finance#murabaha-cost-plus-sale, **car_financing#murabaha-the-standard-islamic-auto-finance** |
| `minilm-llm-topic` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#practical-guidance |
| `minilm-llm-translation` | ✅ 3 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#practical-guidance, **car_financing#murabaha-the-standard-islamic-auto-finance** |
| `minilm-gold-en` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, islamic_finance#practical-guidance |
| `ml-minilm-direct` | ❌ 26 | emergency_fund#the-rule-that-protects-everything-else, financial_planning#plan-around-goals-not-products, financial_planning#know-your-four-numbers |
| `cohere-v4-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-pro-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-fast-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v4-rerank` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#conventional-riba-based-auto-loans, zakat#how-a-large-purchase-affects-your-zakat-base |

### q41 · terminology

- **AR:** ما الفرق بين هامش الربح الثابت في المرابحة ومعدل الفائدة السنوي في القرض التقليدي؟
- **EN (gold):** What is the difference between a flat murabaha profit margin and the annual interest rate on a conventional loan?
- **Relevant:** `car_financing#conventional-riba-based-auto-loans`, `car_financing#murabaha-the-standard-islamic-auto-finance`
- **Keyword router:** `murabaha islamic financing loan debt` (matched مرابحة, قرض)
- **LLM topic_en:** `murabaha vs conventional loan interest rate` (intent financial_question)
- **LLM translation:** `What is the difference between the fixed profit margin in Murabaha and the annual interest rate in a conventional loan?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 17 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, islamic_finance#intro |
| `minilm-router` | ✅ 3 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#practical-guidance, **car_financing#murabaha-the-standard-islamic-auto-finance** |
| `minilm-llm-topic` | ✅ 1 | **car_financing#conventional-riba-based-auto-loans**, **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#the-decision-rule |
| `minilm-llm-translation` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, **car_financing#conventional-riba-based-auto-loans**, islamic_finance#murabaha-cost-plus-sale |
| `minilm-gold-en` | ✅ 1 | **car_financing#conventional-riba-based-auto-loans**, **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale |
| `ml-minilm-direct` | ✅ 1 | **car_financing#conventional-riba-based-auto-loans**, financial_planning#vision-2030-context, car_financing#intro |
| `cohere-v4-direct` | ✅ 1 | **car_financing#conventional-riba-based-auto-loans**, **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-pro-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, **car_financing#conventional-riba-based-auto-loans** |
| `cohere-v5-fast-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, islamic_finance#murabaha-cost-plus-sale, **car_financing#conventional-riba-based-auto-loans** |
| `cohere-v4-rerank` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, **car_financing#conventional-riba-based-auto-loans**, islamic_finance#murabaha-cost-plus-sale |

### q44 · terminology

- **AR:** هل تجب الزكاة على الأسهم وصناديق الاستثمار؟
- **EN (gold):** Is zakat due on shares and investment funds?
- **Relevant:** `zakat#what-you-pay-zakat-on`
- **Keyword router:** `zakat investing investment` (matched زكاة, استثمار)
- **LLM topic_en:** `zakat on stocks and investment funds` (intent financial_question)
- **LLM translation:** `Is zakat obligatory on stocks and investment funds?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 30 | budgeting#categories-that-quietly-leak-money, zakat#intro, islamic_finance#takaful-cooperative-insurance |
| `minilm-router` | ✅ 2 | zakat#intro, **zakat#what-you-pay-zakat-on**, zakat#the-calculation |
| `minilm-llm-topic` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#intro, zakat#the-calculation |
| `minilm-llm-translation` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#intro, zakat#how-a-large-purchase-affects-your-zakat-base |
| `minilm-gold-en` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#the-calculation, zakat#intro |
| `ml-minilm-direct` | ❌ 6 | financial_planning#vision-2030-context, emergency_fund#the-rule-that-protects-everything-else, financial_planning#plan-around-goals-not-products |
| `cohere-v4-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#the-calculation, zakat#intro |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#the-calculation, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v5-fast-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#the-calculation, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v4-rerank` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#the-calculation, zakat#intro |

### q45 · terminology

- **AR:** هل تُخصم الديون المستحقة من وعاء الزكاة؟
- **EN (gold):** Are debts that are due deducted from the zakat base?
- **Relevant:** `zakat#what-you-pay-zakat-on`, `zakat#the-calculation`
- **Keyword router:** `zakat debt` (matched زكاة, ديون)
- **LLM topic_en:** `zakat calculation with outstanding debts` (intent financial_question)
- **LLM translation:** `Are outstanding debts deducted from the zakat base?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 23 | budgeting#categories-that-quietly-leak-money, islamic_finance#murabaha-cost-plus-sale, zakat#intro |
| `minilm-router` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#intro, **zakat#the-calculation** |
| `minilm-llm-topic` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#the-calculation**, zakat#intro |
| `minilm-llm-translation` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#how-a-large-purchase-affects-your-zakat-base, **zakat#the-calculation** |
| `minilm-gold-en` | ✅ 1 | **zakat#what-you-pay-zakat-on**, zakat#how-a-large-purchase-affects-your-zakat-base, **zakat#the-calculation** |
| `ml-minilm-direct` | ❌ 11 | car_financing#conventional-riba-based-auto-loans, car_financing#paying-cash, financial_planning#vision-2030-context |
| `cohere-v4-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#the-calculation**, zakat#the-nisab-threshold |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#the-calculation**, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v5-fast-direct` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#the-calculation**, zakat#how-a-large-purchase-affects-your-zakat-base |
| `cohere-v4-rerank` | ✅ 1 | **zakat#what-you-pay-zakat-on**, **zakat#the-calculation**, zakat#how-a-large-purchase-affects-your-zakat-base |

### q47 · terminology

- **AR:** هل تنقص الزكاة إذا اشتريت سيارة كاش؟
- **EN (gold):** Does my zakat go down if I buy a car in cash?
- **Relevant:** `zakat#how-a-large-purchase-affects-your-zakat-base`
- **Keyword router:** `car vehicle zakat` (matched سيارة, زكاة)
- **LLM topic_en:** `zakat and cash purchases` (intent financial_question)
- **LLM translation:** `Does zakat decrease if I buy a car in cash?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 27 | budgeting#categories-that-quietly-leak-money, budgeting#intro, saving_strategies#pay-yourself-first |
| `minilm-router` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, zakat#what-you-pay-zakat-on |
| `minilm-llm-topic` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, zakat#what-you-pay-zakat-on |
| `minilm-llm-translation` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#intro |
| `minilm-gold-en` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#intro |
| `ml-minilm-direct` | ❌ 7 | car_financing#paying-cash, car_financing#the-decision-rule, car_financing#intro |
| `cohere-v4-direct` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#the-calculation |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#the-calculation |
| `cohere-v5-fast-direct` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#the-calculation |
| `cohere-v4-rerank` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#the-calculation |

### q48 · terminology

- **AR:** المبلغ اللي أجمعه عشان أشتري سيارة، هل عليه زكاة؟
- **EN (gold):** Is zakat due on the money I'm saving up to buy a car?
- **Relevant:** `zakat#how-a-large-purchase-affects-your-zakat-base`
- **Keyword router:** `car vehicle zakat` (matched سيارة, زكاة)
- **LLM topic_en:** `zakat on savings for a car` (intent financial_question)
- **LLM translation:** `Is there zakat on the amount I'm saving to buy a car?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 27 | islamic_finance#intro, islamic_finance#murabaha-cost-plus-sale, islamic_finance#ijara-leasing |
| `minilm-router` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, zakat#what-you-pay-zakat-on |
| `minilm-llm-topic` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, zakat#what-you-pay-zakat-on |
| `minilm-llm-translation` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, zakat#what-you-pay-zakat-on |
| `minilm-gold-en` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#intro, zakat#what-you-pay-zakat-on |
| `ml-minilm-direct` | ✅ 3 | car_financing#paying-cash, car_financing#the-decision-rule, **zakat#how-a-large-purchase-affects-your-zakat-base** |
| `cohere-v4-direct` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#the-calculation |
| `cohere-v5-pro-direct` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#the-calculation |
| `cohere-v5-fast-direct` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#the-calculation |
| `cohere-v4-rerank` | ✅ 1 | **zakat#how-a-large-purchase-affects-your-zakat-base**, zakat#what-you-pay-zakat-on, zakat#intro |

### q50 · ambiguous

- **AR:** هل المرابحة أفضل؟
- **EN (gold):** Is murabaha better?
- **Relevant:** `car_financing#murabaha-the-standard-islamic-auto-finance`, `car_financing#conventional-riba-based-auto-loans`, `islamic_finance#murabaha-cost-plus-sale`, `islamic_finance#practical-guidance`
- **Keyword router:** `murabaha islamic financing` (matched مرابحة)
- **LLM topic_en:** `murabaha financing explanation` (intent financial_question)
- **LLM translation:** `Is murabaha better?` (intent financial_question)
- **Note:** Better than what? Underspecified.

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ✅ 3 | budgeting#intro, budgeting#categories-that-quietly-leak-money, **islamic_finance#murabaha-cost-plus-sale** |
| `minilm-router` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, **islamic_finance#practical-guidance**, **car_financing#murabaha-the-standard-islamic-auto-finance** |
| `minilm-llm-topic` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, **car_financing#murabaha-the-standard-islamic-auto-finance**, car_financing#the-decision-rule |
| `minilm-llm-translation` | ✅ 2 | car_financing#the-decision-rule, **islamic_finance#murabaha-cost-plus-sale**, car_financing#intro |
| `minilm-gold-en` | ✅ 2 | car_financing#the-decision-rule, **islamic_finance#murabaha-cost-plus-sale**, car_financing#intro |
| `ml-minilm-direct` | ❌ 5 | car_financing#the-decision-rule, car_financing#paying-cash, emergency_fund#the-rule-that-protects-everything-else |
| `cohere-v4-direct` | ✅ 2 | car_financing#the-decision-rule, **islamic_finance#practical-guidance**, **car_financing#conventional-riba-based-auto-loans** |
| `cohere-v5-pro-direct` | ✅ 1 | **car_financing#murabaha-the-standard-islamic-auto-finance**, **car_financing#conventional-riba-based-auto-loans**, **islamic_finance#murabaha-cost-plus-sale** |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#murabaha-cost-plus-sale**, **car_financing#conventional-riba-based-auto-loans**, **car_financing#murabaha-the-standard-islamic-auto-finance** |
| `cohere-v4-rerank` | ✅ 2 | car_financing#the-decision-rule, **car_financing#conventional-riba-based-auto-loans**, car_financing#paying-cash |

### q53 · ambiguous

- **AR:** هل القرض حرام؟
- **EN (gold):** Is a loan haram?
- **Relevant:** `islamic_finance#the-three-prohibitions`, `car_financing#conventional-riba-based-auto-loans`
- **Keyword router:** `loan debt` (matched قرض)
- **LLM topic_en:** `is loan haram in islam` (intent financial_question)
- **LLM translation:** `Is a loan haram?` (intent financial_question)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 21 | budgeting#intro, budgeting#review-cadence, budgeting#categories-that-quietly-leak-money |
| `minilm-router` | ✅ 1 | **car_financing#conventional-riba-based-auto-loans**, car_financing#murabaha-the-standard-islamic-auto-finance, **islamic_finance#the-three-prohibitions** |
| `minilm-llm-topic` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#practical-guidance, islamic_finance#intro |
| `minilm-llm-translation` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#ijara-leasing, islamic_finance#practical-guidance |
| `minilm-gold-en` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#ijara-leasing, islamic_finance#practical-guidance |
| `ml-minilm-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, car_financing#paying-cash, islamic_finance#ijara-leasing |
| `cohere-v4-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#ijara-leasing, islamic_finance#murabaha-cost-plus-sale |
| `cohere-v5-pro-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, **car_financing#conventional-riba-based-auto-loans**, islamic_finance#practical-guidance |
| `cohere-v5-fast-direct` | ✅ 1 | **islamic_finance#the-three-prohibitions**, islamic_finance#practical-guidance, **car_financing#conventional-riba-based-auto-loans** |
| `cohere-v4-rerank` | ✅ 2 | islamic_finance#ijara-leasing, **islamic_finance#the-three-prohibitions**, islamic_finance#practical-guidance |

### q54 · ambiguous

- **AR:** أبي سيارة
- **EN (gold):** I want a car
- **Relevant:** `car_financing#intro`, `car_financing#paying-cash`, `car_financing#the-decision-rule`
- **Keyword router:** `car vehicle` (matched سيارة)
- **LLM topic_en:** `buying a car` (intent purchase_simulation)
- **LLM translation:** `I want a car.` (intent purchase_simulation)

| Config | Rank | Top 3 retrieved |
|---|---|---|
| `minilm-direct` | ❌ 11 | islamic_finance#murabaha-cost-plus-sale, islamic_finance#ijara-leasing, islamic_finance#mudaraba-and-musharaka-partnership |
| `minilm-router` | ✅ 1 | **car_financing#intro**, **car_financing#paying-cash**, zakat#how-a-large-purchase-affects-your-zakat-base |
| `minilm-llm-topic` | ✅ 1 | **car_financing#intro**, financial_planning#plan-around-goals-not-products, **car_financing#paying-cash** |
| `minilm-llm-translation` | ✅ 2 | financial_planning#plan-around-goals-not-products, **car_financing#intro**, **car_financing#paying-cash** |
| `minilm-gold-en` | ✅ 1 | **car_financing#intro**, financial_planning#plan-around-goals-not-products, **car_financing#paying-cash** |
| `ml-minilm-direct` | ✅ 1 | **car_financing#intro**, car_financing#murabaha-the-standard-islamic-auto-finance, **car_financing#paying-cash** |
| `cohere-v4-direct` | ✅ 2 | car_financing#murabaha-the-standard-islamic-auto-finance, **car_financing#the-decision-rule**, **car_financing#intro** |
| `cohere-v5-pro-direct` | ✅ 2 | car_financing#murabaha-the-standard-islamic-auto-finance, **car_financing#paying-cash**, **car_financing#intro** |
| `cohere-v5-fast-direct` | ✅ 2 | car_financing#murabaha-the-standard-islamic-auto-finance, **car_financing#intro**, **car_financing#paying-cash** |
| `cohere-v4-rerank` | ❌ 5 | car_financing#murabaha-the-standard-islamic-auto-finance, saving_strategies#the-waiting-test, zakat#how-a-large-purchase-affects-your-zakat-base |


<a id="all_miss"></a>
## Every configuration misses @3 (0)

