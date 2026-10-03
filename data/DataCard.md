## Pilot

Ten abstracts were sampled without replacement from the deduplicated corpus using a fixed random seed.

Gemini Pro, Gemini 3.5 Flash-Lite, and Sol produced the same relevance labels for all ten abstracts:

- 9 `keep`
- 1 `exclude`

All retained pilot outputs passed exact evidence matching against the source abstracts.

The pilot was used to test the screening workflow and output format. It was not an accuracy study based on independently prepared human reference labels and therefore does not establish classification accuracy.

---

## Full Corpus Classification

The full set of 1,500 deduplicated abstracts was independently classified by Gemini Pro and Sol using the same materials-relevance criteria.

| Initial model label | Gemini Pro | Sol |
| --- | ---: | ---: |
| keep | 1,482 | 1,471 |
| exclude | 15 | 6 |
| review | 3 | 23 |
| Total | 1,500 | 1,500 |

The two models agreed on 1,471 records and disagreed on 29, corresponding to an inter-model agreement rate of **98.07%**.

These counts describe model outputs only and are not the final relevance-filtering results.

Model agreement is not equivalent to classification accuracy and does not rule out shared errors.

---

## Output Processing and Validation

Model outputs were normalized to UTF-8 JSONL and aligned with the deduplicated source corpus.

The final classification files passed checks for:

- valid JSON;
- required fields;
- allowed relevance labels;
- unique arXiv IDs;
- complete coverage of all 1,500 source records; and
- exact matching of non-empty evidence passages against the corresponding source abstracts.

Final evidence validation found:

- Gemini: **1,500/1,500 exact evidence matches**
- Sol: **1,500/1,500 exact evidence matches**
- Remaining evidence mismatches: **0**

Exact evidence matching verifies that the cited passage is present in the corresponding source abstract. It does not establish that the relevance label itself is correct.

---

## Files and Provenance

The principal retained screening files are:

- `data/processed/screening/gemini_classifications.jsonl`  
  Contains 1,500 Gemini classifications.

- `data/processed/screening/sol_classifications.jsonl`  
  Contains 1,500 Sol classifications.

- `data/processed/screening/human_relevance_review.jsonl`  
  Contains human relevance decisions.

- `data/processed/screening/final_relevance_decisions.jsonl`  
  Contains final relevance decisions for all 1,500 records.

- `data/processed/screening/final_filter_report.json`  
  Contains final filtering counts and decision rules.

The original arXiv corpus, screening prompt, processed model outputs, human-review decisions, and final filtering outputs are retained.

Some intermediate request, batching, and temporary processing files are not retained. Therefore, the exact execution history of every model request cannot be reconstructed from the current repository alone.

---

## Human Adjudication of Label Disagreements

The 29 records for which Gemini and Sol produced different relevance labels were manually reviewed.

The final human decisions were:

- **15 keep**
- **14 exclude**
- **0 review**

Human decisions override model labels in the final relevance filtering process.

These reviews were adjudications because the model outputs were available during review. They should therefore not be interpreted as blinded reference-label annotations or as an independent accuracy study.

---

## Human Review of Model-Agreed Exclude and Review Records

Six additional records for which both models returned either `exclude` or `review` were manually reviewed.

All six were assigned a final label of:

**exclude**

Together with the 29 model disagreements, this stage covered 35 unique abstracts:

- **15 keep**
- **20 exclude**
- **0 review**

---

## Random Human Spot-Check of Model-Agreed Keep Records

Thirty records were sampled without replacement from the 1,465 abstracts jointly labelled `keep` by both models.

Human review assigned:

- **29 keep**
- **1 exclude**
- **0 review**

Thus, one of the 30 sampled records received a human decision that differed from the shared `keep` label.

Because the sample is small and the review was not fully blinded, this result should not be interpreted as an estimate of the overall classification error rate.

Across all relevance-review stages, **65 unique abstracts** were manually reviewed:

- **44 keep**
- **21 exclude**
- **0 review**

---

## Final Materials Relevance Filter

Human relevance decisions were applied first and override model outputs.

For records without a human decision, an abstract was retained only when both Gemini and Sol labelled it `keep`.

The final corpus contains:

- **1,479 retained abstracts**
- **21 excluded abstracts**
- **0 unresolved decisions**

Of the 1,479 retained abstracts:

- **44** were individually reviewed by a human;
- **1,435** were retained based on agreement between both models.

A final relevance decision is a workflow outcome and should not be interpreted as proof that every retained abstract is relevant or suitable for QA generation.

The filtered materials-science corpus is stored in:

`data/processed/arxiv_materials_filtered.jsonl`

---

## Generated QA Candidates

The QA-generation stage produced **300 candidate QA pairs** from **257 source abstracts**:

- **240 answerable**
- **60 not stated**

The category distribution is:

- material properties: **129**
- synthesis conditions: **81**
- performance metrics: **90**

A maximum of two QA pairs was generated from any single abstract.

All 300 candidates passed mechanical checks for:

- valid JSON;
- required fields;
- unique QA IDs;
- valid source IDs;
- exact evidence matching for answerable questions;
- required fields for not-stated questions;
- valid categories; and
- preservation of original chemical-formula strings where checked.

No candidates were removed during these checks:

- Input: **300**
- Removed: **0**
- Remaining: **300**

These mechanical checks do not establish:

- semantic correctness of the answer;
- whether the evidence fully supports the answer;
- correctness of not-stated judgments; or
- adequacy of chemical-formula ambiguity handling.

---

## Pending Work

The following stages have been completed:

- abstract collection and deduplication;
- materials-relevance classification;
- human adjudication of model disagreements;
- human review of model-agreed exclude/review records;
- random human spot-checking of model-agreed keep records;
- final materials-relevance filtering;
- generation of 300 QA candidates; and
- mechanical validation of the QA candidates.

The remaining work includes:

### 1. Semantic Review of QA Candidates

Review the generated QA pairs for semantic and scientific correctness.

### 2. Review of Chemical Formula Handling

Further verify:

- preservation of chemical formulas;
- potential ambiguities; and
- whether additional ambiguity annotations are required.

### 3. Random 50-Pair Human QA Audit

Randomly sample **50 QA pairs** for manual quality review.

### 4. QA Correction or Filtering

Correct or remove QA pairs if issues are identified during the human audit.

### 5. Contextual Open-Source Model Evaluation

Evaluate an open-source model using the source abstracts as context.