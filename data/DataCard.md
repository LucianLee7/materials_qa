# Materials Science Abstract Corpus Data Card

## Status

Abstract collection, deduplication, materials-relevance screening, human relevance review, and final relevance filtering are complete.

The final filtered corpus contains **1,479 abstracts**, with **21 abstracts excluded** from the original 1,500-record corpus.

A set of **300 candidate QA pairs** has been generated and mechanically validated. The random 50-pair human QA audit is complete: three pairs contain E6 errors (6% observed pair error rate). Confirmed QA errors have been corrected in a separate copy, and targeted chemical-formula checks are complete. Contextual model inference is complete for all 300 pairs; response classification and evaluation reporting remain pending.

This data card describes the abstract corpus, relevance-screening process, and current QA candidate set. It does not represent a fully audited final QA dataset.

---

## Collection

The corpus was collected from the arXiv API:

`https://export.arxiv.org/api/query`

using the query:

`cat:cond-mat.mtrl-sci`

The request retrieved the **1,500 most recent records** available under this category at the time of collection.

- Records retrieved: **1,500**
- Publication date range: **12 August to 30 September 2026 (UTC)**
- Exact API retrieval timestamp: not recorded
- Raw file: `data/raw/arxiv_sample.jsonl`

For each record, the following fields were stored:

- source URL;
- title;
- abstract;
- publication timestamp; and
- update timestamp.

Abstract text was preserved as returned by the API. No chemical-formula normalization was applied to the source abstracts.

---

## Preprocessing and Filter Counts

| Step | Rule | Input records | Removed | Remaining |
| --- | --- | ---: | ---: | ---: |
| Deduplication | Compare arXiv IDs without version suffixes; retain the highest collected version and the first record on ties | 1,500 | 0 | 1,500 |
| Abstract validation | Check for missing abstracts, non-string values, and whitespace-only strings | 1,500 | 0 | 1,500 |
| Materials relevance filtering | Human decisions override model labels; otherwise retain only records labelled `keep` by both models | 1,500 | 21 | 1,479 |

No duplicate records were removed.

No invalid abstracts were found.

The original 1,500-record source corpus remains unchanged. Relevance filtering was applied to create a separate **1,479-record filtered corpus**.

The deduplicated corpus is stored in:

`data/processed/arxiv_deduplicated.jsonl`

The final filtered corpus is stored in:

`data/processed/arxiv_materials_filtered.jsonl`

---

## Relevance Screening Rules

The screening models received only each paper's:

- arXiv ID;
- title; and
- abstract.

Scientific text was treated as data rather than as instructions.

The screening prompt is stored in:

`prompts/materials_relevance.txt`

The allowed labels were:

### `keep`

The paper clearly concerns materials composition, structure, properties, synthesis, processing, characterization, or performance in devices.

This includes theoretical and computational research, as well as methods explicitly intended to study or assess materials.

### `exclude`

The paper is clearly outside materials research and has no explicit connection to a materials-science problem.

### `review`

The available information is insufficient for a confident relevance decision.

The absence of experiments, numerical results, or the word *material* was not itself treated as a reason for exclusion.

The screening stage assessed **materials relevance**, not:

- scientific correctness;
- QA suitability; or
- overall paper quality.

Each model output contained:

- `arxiv_id`;
- `decision`;
- `reason`; and
- `evidence`.

For non-empty evidence, the passage was required to occur exactly and contiguously in the corresponding source abstract.

---

## Pilot

Ten abstracts were sampled without replacement from the deduplicated corpus using a fixed random seed.

Gemini Pro, Gemini 3.5 Flash-Lite, and Sol produced the same relevance labels for all ten abstracts:

- **9 `keep`**
- **1 `exclude`**

The pilot outputs checked at that stage passed exact evidence matching against the source abstracts.

The pilot was used to test the screening workflow and output format.

It was not an accuracy study based on independently prepared human reference labels and therefore does not establish classification accuracy.

---

## Full Corpus Classification

The full set of **1,500 deduplicated abstracts** was independently classified by Gemini Pro and Sol using the same materials-relevance criteria.

| Initial model label | Gemini Pro | Sol |
| --- | ---: | ---: |
| keep | 1,482 | 1,471 |
| exclude | 15 | 6 |
| review | 3 | 23 |
| Total | 1,500 | 1,500 |

The two models agreed on **1,471 records** and disagreed on **29 records**, corresponding to an inter-model agreement rate of:

**98.07%**

These counts describe model outputs only. They are not the final relevance-filtering results.

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

- Gemini: **1,500 / 1,500 exact evidence matches**
- Sol: **1,500 / 1,500 exact evidence matches**
- Remaining evidence mismatches: **0**

Exact evidence matching verifies that a cited passage occurs in the corresponding source abstract.

It does not establish that the relevance classification itself is correct.

---

## Human Adjudication of Model Disagreements

The **29 records** for which Gemini and Sol produced different relevance labels were manually reviewed.

The final human decisions were:

- **15 keep**
- **14 exclude**
- **0 review**

Human decisions override model labels in the final relevance-filtering process.

These reviews were adjudications because the model outputs were available during review.

They should therefore not be interpreted as:

- blinded reference-label annotations; or
- an independent classification-accuracy study.

---

## Human Review of Model-Agreed Exclude and Review Records

Six additional records for which both models returned either `exclude` or `review` were manually reviewed.

All six were assigned a final label of:

**exclude**

Together with the 29 model disagreements, this stage covered **35 unique abstracts**:

- **15 keep**
- **20 exclude**
- **0 review**

---

## Random Human Spot-Check of Model-Agreed Keep Records

Thirty records were sampled without replacement from the **1,465 abstracts jointly labelled `keep`** by both models.

Human review assigned:

- **29 keep**
- **1 exclude**
- **0 review**

One of the 30 sampled records therefore received a human decision that differed from the shared model `keep` label.

Because the sample is small and the review was not fully blinded, this result should not be interpreted as an estimate of the overall corpus classification error rate.

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

The filtered corpus is stored in:

`data/processed/arxiv_materials_filtered.jsonl`

Final relevance decisions for all 1,500 records are stored in:

`data/processed/screening/final_relevance_decisions.jsonl`

---

## Generated QA Candidates

The QA-generation stage produced **300 candidate QA pairs** from **257 source abstracts**.

The candidate set contains:

- **240 answerable pairs**
- **60 not-stated pairs**

The category distribution is:

| QA category | Count |
| --- | ---: |
| Material properties | 129 |
| Synthesis conditions | 81 |
| Performance metrics | 90 |
| Total | 300 |

A maximum of two QA pairs was generated from any single abstract.

The main candidate file is:

`data/processed/qa/materials_qa_all.jsonl`

All 300 candidates passed mechanical checks for:

- valid JSON;
- required fields;
- unique QA IDs;
- valid source IDs;
- unique question strings;
- membership in the filtered source corpus;
- exact evidence matching for answerable questions;
- required field rules for not-stated questions;
- valid QA categories; and
- preservation of original chemical-formula strings where checked.

Mechanical QA-filter counts are therefore:

| Step | Input | Removed | Remaining |
| --- | ---: | ---: | ---: |
| QA mechanical validation | 300 | 0 | 300 |

These checks do not establish:

- semantic correctness of an answer;
- whether the evidence fully supports the answer;
- correctness of not-stated judgments;
- scientific truth of the underlying paper; or
- adequacy of chemical-formula ambiguity handling.

---

## Predefined QA Audit Categories

The following audit categories were defined on **3 October 2026**, before manual review of the generated QA candidates.

They concern QA quality and are separate from the earlier abstract-relevance review.

For each reviewed pair, every applicable category should be marked.

A QA pair containing one or more errors counts once toward the overall **pair error rate**. Because one pair may contain multiple error types, category counts may sum to more than the total number of erroneous pairs.

Each finding should include a brief explanation and the relevant source text.

| Code | Category | Definition |
| --- | --- | --- |
| E1 | Source or record integrity | Wrong or missing arXiv ID, incorrect source abstract, missing required fields, invalid field values, or duplicate `qa_id`. |
| E2 | Question quality | Ambiguous, false-premise, multi-part, out-of-scope, or substantively duplicate question. |
| E3 | Answer support or correctness | The answer adds unstated facts, misreads the abstract, omits a necessary qualifier, or confuses prediction, observation, or causation. |
| E4 | Evidence passage | An answerable pair has empty evidence, evidence is not an exact contiguous source substring, or the passage does not support the entire answer. |
| E5 | Answerability or abstention | A not-stated question is actually answered in the abstract; an answerable question lacks a stated answer; or the not-stated answer, empty-evidence rule, or missing-information explanation is incorrect. |
| E6 | Chemical formula handling | A formula is altered in the QA text, the original form is not preserved, normalization is unjustified, or ambiguity is not recorded. |
| E7 | Numerical and experimental fidelity | Incorrect value, unit, sign, uncertainty, range, material assignment, or experimental or processing condition. This category may overlap with E3 or E6. |

---

## Completed 50-Pair Human QA Audit

On 3 October 2026, 50 pairs were sampled uniformly without replacement from the 300 original candidates using `random.Random(66).sample`. The candidate hash and ordered selected IDs were recorded before review in `qa_audit_manifest.json`; the sample can be reconstructed from the retained original candidates using these IDs. The sample contains 43 answerable and seven not-stated pairs. The original candidates remained unchanged throughout the audit.

All final audit judgments for the 50 sampled pairs were made manually by the human reviewer using categories E1–E7. No AI judge or automated scoring system assigned the audit labels, error categories or final decisions. AI assistance was used to organize the review materials, present source excerpts, and draw attention to some fields for inspection. Complete abstracts and all fields were available in the review materials during the audit; the separate display file was subsequently removed, and these records remain available from the original QA file and source corpus. The review therefore used human judgment with presentation assistance and was not a fully unaided or blinded audit.

| Category | Pairs with this error |
| --- | ---: |
| E1 | 0 |
| E2 | 0 |
| E3 | 0 |
| E4 | 0 |
| E5 | 0 |
| E6 | 3 |
| E7 | 0 |

**Three of 50 pairs had at least one error (6.0%); 47 had no errors detected by the reviewer.**

- Sample 25 (`all_070`): unit W was incorrectly recorded as a chemical formula.
- Sample 33 (`all_104`): unit W was incorrectly recorded as a chemical formula.
- Sample 40 (`all_159`): the English word As was incorrectly recorded as a chemical formula.

The two-sided 95% Wilson interval is **2.06%–16.22%**, a binomial approximation to sampling without replacement, without a finite-population correction. The sample gives limited precision for the full candidate-set error rate. This interval concerns sampling uncertainty and does not account for reviewer mistakes or attention influenced by model assistance. Zero findings in other categories do not establish zero errors there, and rare error types may be missed. The audit assesses agreement with supplied abstracts, not the scientific truth of the papers.

Not-stated questions showed template concentration around duration-related missing information: six of the seven not-stated questions in the audited sample ask about an unreported growth or deposition duration; the remaining question asks about numerical uncertainty. This limits coverage of different missing-information types and may make abstention evaluation less diverse. This is a dataset-level limitation, not an additional pair-level error assigned by the reviewer.

The original candidates remain unchanged. Post-audit corrections are recorded separately below and do not replace these original findings or the original error rate.

---

## Post-Audit QA Corrections

A separate corrected candidate file is stored in `data/processed/qa/materials_qa_corrected.jsonl`. It currently contains all 300 pairs, with 11 non-chemical entries removed from `chemical_formulas` across ten pairs. These include unit W, the English word As, and the magnetic B--H relationship. Questions, answers, evidence passages and original candidate records were not changed. No QA pairs were removed (300 input, 0 removed, 300 remaining).

The corrections are recorded in `data/processed/qa/qa_corrections.jsonl`. Three corrected pairs were identified in the original random audit; seven were confirmed in a targeted post-audit review. The original audit remains three errors in 50 pairs (6%). Post-audit findings do not retrospectively replace the original audit decisions. The targeted review of standalone W, As and B--H entries is complete; five W entries denoting tungsten were explicitly retained. This does not constitute a full semantic review of every formula annotation. Mechanical checks of the corrected file are recorded in `data/processed/qa/qa_corrected_checks.json`.

---

## Reproducing Random Samples

`random_sample.py` uses a fixed seed of 66 and samples without replacement in input file order. It writes a JSONL sample and a `.manifest.json` containing input hashes, sample IDs and sampling settings. The following commands reproduce the historical 10-paper pilot, 30-paper jointly kept sample, and 50-pair QA audit IDs in their original selected order. Existing outputs are not overwritten.

```bash
python3 random_sample.py data/processed/arxiv_deduplicated.jsonl /tmp/pilot_10.jsonl --count 10
python3 random_sample.py data/processed/arxiv_deduplicated.jsonl /tmp/agreed_keep_30.jsonl --count 30 --agreed-keep
python3 random_sample.py data/processed/qa/materials_qa_all.jsonl /tmp/qa_audit_50.jsonl --count 50
```

For the agreed-keep sample, the script joins the retained Gemini and Sol classification files by arXiv ID, filters to the 1,465 joint keep records, and preserves corpus order before sampling. The source is the original 1,500-record deduplicated corpus, not the final filtered corpus. The QA audit uses the original candidate file, not the corrected copy. Reproduction was verified against all three retained sample manifests.

---

## Contextual Model Inference

On 4 October 2026, Qwen2.5-1.5B-Instruct generated responses to all 300 corrected QA pairs on a Colab Tesla T4. Each model input contained the full source abstract and question; reference answers, answerability labels and supporting passages were stored only in the output, not supplied to the model.

The run used model revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, greedy decoding (`do_sample=false`), a limit of 128 new tokens, seed 66 and bfloat16 weights. Exact prompts, input hashes, software versions and GPU details are stored in `data/evaluation/run_manifest.json`.

All 300 QA IDs are present exactly once. Reference fields and input hashes match the repository files. Empty responses: 0; responses marked as hitting the token limit: 2. These checks do not measure answer correctness. All 300 response classifications remain pending.

- `data/evaluation/qwen_responses.jsonl`: the 300 model responses and reference fields.
- `data/evaluation/run_manifest.json`: model and run provenance.
- `data/evaluation/checkpoint_settings.json`: settings used to verify resumable inference.
- `data/evaluation/pilot_responses.jsonl`: five execution-pilot responses, separate from the formal denominator.
- `data/evaluation/response_checks.json`: ingestion checks and their limitations.

---

## Files and Provenance

The principal retained files are:

- `data/raw/arxiv_sample.jsonl`  
  Original 1,500-record arXiv corpus.

- `data/processed/arxiv_deduplicated.jsonl`  
  Deduplicated corpus with arXiv ID and version information.

- `data/processed/arxiv_materials_filtered.jsonl`  
  Final 1,479-record materials-relevance-filtered corpus.

- `data/processed/screening/gemini_classifications.jsonl`  
  Gemini relevance classifications.

- `data/processed/screening/sol_classifications.jsonl`  
  Sol relevance classifications.

- `data/processed/screening/human_relevance_review.jsonl`  
  Human relevance decisions.

- `data/processed/screening/final_relevance_decisions.jsonl`  
  Final decisions for all 1,500 abstracts.

- `data/processed/screening/final_filter_report.json`  
  Final filtering rules and counts.

- `data/processed/qa/materials_qa_all.jsonl`  
  The 300 generated QA candidates.

- `data/processed/qa/materials_qa_corrected.jsonl`  
  Corrected 300-pair candidate set for subsequent evaluation.

- `data/processed/qa/qa_corrections.jsonl`  
  Post-audit correction records.

- `data/processed/qa/qa_corrected_checks.json`  
  Mechanical checks and hash of the corrected candidates.

- `data/processed/qa/qa_ingestion_checks.json`  
  Mechanical QA validation results and limitations.

- `data/processed/qa/qa_audit_manifest.json`  
  Frozen candidate hash, sampling seed and selected IDs.

- `data/processed/qa/qa_human_audit.jsonl`  
  Individual human audit decisions and error categories.

- `data/processed/qa/qa_audit_summary.json`  
  Audit counts, confidence interval and limitations.

The original arXiv corpus, screening prompt, processed classification outputs, human decisions, final filtered corpus, and QA candidates are retained.

Intermediate execution files that are not necessary for interpretation of the final dataset are not part of the main data card.

---

## Limitations

Several limitations remain.

First, only **65 of the 1,500 abstracts** received individual human relevance review. The other retained abstracts depend on agreement between the two screening models.

Second, inter-model agreement does not establish classification accuracy, because both models may make the same mistake.

Third, the 30-record agreed-keep spot-check is too small to establish a precise relevance-classification error rate.

Fourth, mechanical QA validation verifies structure and source consistency but does not establish semantic correctness.

Fifth, all audit decisions were made by a single human reviewer, with AI assistance in presenting materials. The sample-based audit may miss rare errors or errors overlooked by the reviewer.

Finally, the dataset is grounded in the supplied arXiv abstracts. Neither the relevance review nor the QA audit verifies the scientific truth of claims made in the original papers.

---

## Pending Work

The following stages are complete:

- arXiv abstract collection;
- deduplication;
- abstract validation;
- materials-relevance classification;
- human adjudication of model disagreements;
- human review of model-agreed exclude/review records;
- random human spot-checking of model-agreed keep records;
- final materials-relevance filtering;
- generation of 300 QA candidates;
- mechanical validation of the QA candidates;
- the random 50-pair human QA audit;
- targeted chemical-formula review; and
- corrections recorded separately from the original audit.

The only remaining planned stage is:

### Contextual Open-Source Model Evaluation

Inference on all 300 corrected QA pairs is complete. Classify the saved responses as supported, unsupported, or correctly abstained using a documented method, and report results, failure examples and evaluation limitations.
