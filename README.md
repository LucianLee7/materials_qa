# Evidence Grounded Materials Science QA Evaluation

This research internship project builds a QA dataset from materials-science abstracts and evaluates Qwen2.5-1.5B-Instruct using each abstract as context. It is **evaluation only; no fine-tuning was performed**.

The repository contains the data, prompts, collection and sampling code, Colab inference notebook, AI judgments and human review records. The accompanying write-up is [materials_qa_report.docx](materials_qa_report.docx), located in the project root. See [DataCard](DataCard.md) for the full processing rules, filter counts, audit findings and limitations.

## Results

| Stage | Result |
| --- | --- |
| arXiv collection | 1,500 abstracts from `cond-mat.mtrl-sci` |
| Deduplication and empty-abstract checks | 0 records removed |
| Materials-relevance screening | 1,479 retained; 21 excluded |
| QA generation | 300 pairs from 257 abstracts: 240 answerable and 60 not stated |
| Original human QA audit | 3 of 50 pairs had errors, all in chemical-formula annotations |
| Post-audit corrections | 11 non-chemical entries removed across 10 pairs; no QA pairs removed |
| Contextual Qwen inference | 300 responses; 0 empty responses; 2 token-limit flags |

The current response classifications, after human review, are:

| Reference question group | Supported | Unsupported | Correctly abstained |
| --- | ---: | ---: | ---: |
| All 300 | 215 (71.67%) | 42 (14.00%) | 43 (14.33%) |
| Answerable 240 | 215 (89.58%) | 25 (10.42%) | 0 |
| Not stated 60 | 0 | 17 (28.33%) | 43 (71.67%) |

Supported answers plus correct abstentions total **258/300 (86.00%)**. This is a rubric-based result on this fixed dataset, not independently verified scientific accuracy. Of the 300 current classifications, **44 have a human review basis and 256 remain AI-only**.

## Method

### Abstract screening

The collected abstracts span 12 August to 30 September 2026 (UTC). Deduplication uses arXiv IDs without version suffixes and keeps the highest collected version. Source abstract text is retained unchanged.

After a random 10-paper pilot, Gemini Pro and Sol independently classified the 1,500 abstracts as `keep`, `exclude` or `review`. The models agreed on 1,471 labels (98.07%); agreement does not establish accuracy. Human review covered all 29 disagreements, six jointly excluded/review-labelled records and 30 randomly selected joint keeps, for 65 distinct abstracts. Human decisions take precedence; other retained records require both models to label them `keep`.

### QA construction and audit

QA pairs cover material properties (129), synthesis conditions (81) and performance metrics (90), with at most two pairs per abstract. Each record includes the source arXiv ID, question, answer, supporting passage, answerability information and chemical-formula annotations. Answerable evidence must match the source abstract exactly. Not-stated cases have empty supporting passages and explain which information is absent. Original formula strings are retained; normalization is optional and unresolved issues can be recorded.

Error categories E1-E7 were defined before the random 50-pair human audit. Three pairs contained E6 errors: two watt symbols `W` and one English word `As` were misidentified as chemical formulas. The original sample error rate is 6%, with an approximate 95% Wilson interval of 2.06%-16.22%, without finite-population correction. This is not an error estimate for the corrected dataset. Final audit decisions were human judgments. Original candidates, audit findings and subsequent corrections are retained separately.

### Model inference and response judging

Qwen2.5-1.5B-Instruct ran on a Colab Tesla T4 with greedy decoding, seed 66, bfloat16 weights and a 128-new-token limit. The model received **only the full abstract and question**. Reference answers and evidence were saved in the output records but were not included in the inference prompt. The model revision and runtime details are in [run_manifest.json](data/evaluation/run_manifest.json).

The [response rubric](prompts/judge_model_responses.txt) defines:

- `supported`: sufficiently answers the question, with all substantive claims grounded in the abstract.
- `unsupported`: includes unsupported claims, contradictions, essential omissions, off-topic answers or unnecessary abstention.
- `correctly_abstained`: acknowledges that the requested information is absent without inventing details.

Semantic abstention is separate from exact compliance with the instructed string `not stated`. Reaching the token limit does not automatically determine a failure.

A 30-case Codex Sol calibration pilot was compared with human labels. A Codex Sol model then judged all 300 responses afresh. The exact full-run judge model snapshot is not established. Thirty of the 286 unflagged decisions were randomly sampled for a further human check. Initial agreement was **28/30 (93.33%)**. These review stages are separate from the original 50-pair QA audit.

## Main files

| File or directory | Purpose |
| --- | --- |
| [materials_qa_report.docx](materials_qa_report.docx) | Project write-up in Word format |
| [DataCard.md](DataCard.md) | Dataset methods, filter counts, audits and limitations |
| [data/raw/arxiv_sample.jsonl](data/raw/arxiv_sample.jsonl) | Original 1,500 collected abstracts |
| [data/processed/arxiv_deduplicated.jsonl](data/processed/arxiv_deduplicated.jsonl) | Deduplicated abstracts with arXiv ID/version fields |
| [data/processed/arxiv_materials_filtered.jsonl](data/processed/arxiv_materials_filtered.jsonl) | Final 1,479 retained abstracts |
| [data/processed/screening/](data/processed/screening/) | Gemini/Sol labels, human relevance decisions and final filtering records |
| [data/processed/qa/materials_qa_all.jsonl](data/processed/qa/materials_qa_all.jsonl) | Frozen original 300 QA candidates |
| [data/processed/qa/materials_qa_corrected.jsonl](data/processed/qa/materials_qa_corrected.jsonl) | Corrected QA set used for Qwen inference |
| [data/processed/qa/](data/processed/qa/) | QA audit manifest, human findings, audit summary and correction log |
| [data/evaluation/qwen_responses.jsonl](data/evaluation/qwen_responses.jsonl) | Unchanged model responses and reference fields |
| [data/evaluation/judge/codex_full_judgments.jsonl](data/evaluation/judge/codex_full_judgments.jsonl) | Original full-run AI judgments |
| [data/evaluation/judge/qwen_classifications_adjudicated.jsonl](data/evaluation/judge/qwen_classifications_adjudicated.jsonl) | Current 300 classifications, original AI labels/reasons and human review basis |
| [data/evaluation/judge/](data/evaluation/judge/) | Calibration, flagged-case adjudication, unflagged spot-check and their reports |
| [scripts/](scripts/) | All Python scripts for collection, preprocessing and sampling |
| [notebooks/materials_qa_evaluation.ipynb](notebooks/materials_qa_evaluation.ipynb) | Colab inference notebook |
| [prompts/](prompts/) | Relevance, QA-generation and judge prompts |

In the current classification file, `classification` is the applied label. `ai_classification` and `ai_reason` preserve the original AI decision. `classification_basis` distinguishes `human_adjudication`, `human_spotcheck` and `ai_judgment_unreviewed`. AI-generated evidence and explanations do not become human-written findings merely because a human reviewed the label.

## Reproduction

Run local commands from the project root using Python 3. Sampling and processing use the standard library; arXiv collection additionally requires `requests`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Reproduce preprocessing from the saved corpus

```bash
python3 scripts/deduplicate.py
python3 scripts/filter_abstracts.py
```

`scripts/deduplicate.py` writes the deduplicated corpus and recreates its count report. Historical filter counts are retained in DataCard. Despite its name, `scripts/filter_abstracts.py` **only checks missing or blank abstracts**; it does not perform materials-relevance screening or write the final relevance-filtered corpus. These commands use the saved raw data. Historical relevance decisions and their provenance are retained in the screening directory.

For a new collection, run `python3 scripts/fetch_arxiv.py` in a separate checkout or working copy. It requests the latest 1,500 records at execution time and overwrites `data/raw/arxiv_sample.jsonl`, so it will not recreate the historical snapshot. The exact original retrieval timestamp was not recorded.

### Reproduce historical random samples

`scripts/random_sample.py` fixes the seed at 66 and samples without replacement. It writes a sample and a manifest and refuses to overwrite existing output files; choose unused output paths.

```bash
python3 scripts/random_sample.py data/processed/arxiv_deduplicated.jsonl /tmp/pilot_10.jsonl --count 10
python3 scripts/random_sample.py data/processed/arxiv_deduplicated.jsonl /tmp/agreed_keep_30.jsonl --count 30 --agreed-keep
python3 scripts/random_sample.py data/processed/qa/materials_qa_all.jsonl /tmp/qa_audit_50.jsonl --count 50
python3 scripts/prepare_judge_sample.py
```

The agreed-keep sample uses the original deduplicated corpus and the two saved model classification files, not the final filtered corpus. The 50-pair audit uses the frozen original QA set, not its corrected copy. `scripts/prepare_judge_sample.py` reconstructs the 20-answerable/10-not-stated calibration inputs and manifest; generated inputs are not retained in the cleaned repository. It does not generate judge labels. The later unflagged sample is reproducible from the ordered source file, seed and method in [unflagged_spotcheck_manifest.json](data/evaluation/judge/unflagged_spotcheck_manifest.json).

### Run Qwen in Colab

1. Open [the notebook](notebooks/materials_qa_evaluation.ipynb) in Google Colab and select a GPU runtime.
2. Run its dependency installation cell, restart the runtime, and continue from the imports/settings cell as instructed.
3. Upload `materials_qa_corrected.jsonl` and `arxiv_materials_filtered.jsonl` from the canonical paths above.
4. Inspect the five-response execution pilot, run all 300 pairs and download the result archive before the session ends.

The notebook installs its own inference dependencies; local `requirements.txt` covers corpus collection only. Each full run starts from the beginning and overwrites the notebook's previous response file. Hardware availability and repeated model outputs may vary. Original settings are retained in the saved run manifest.

### Reproduce the judging workflow

Use [run_codex_judge.txt](prompts/run_codex_judge.txt) in a fresh conversation with access to the repository. It specifies the inputs, rubric, output files and coverage/evidence checks. Reference answers are fallible aids; complete abstracts are the sole evidence source. Preserve historical outputs separately before another run. The prompts make the method inspectable but do not guarantee identical AI labels or a fully blinded study.

## Limitations

The corpus covers one arXiv category and a short publication window. Most abstracts were retained through model agreement rather than individual human review. The QA set uses only 257 source abstracts, and the audited not-stated questions concentrate on missing durations. A Hall-conductivity question (`all_152`) remains ambiguous about measured versus calculated values; its response was classified as supported and the concern recorded separately.

Exact evidence matching checks quotation fidelity, not scientific truth or complete semantic support. Formula corrections were targeted, not a complete annotation audit. Human reviews were conducted by a single reviewer who is not a domain expert in materials science and relied on translation tools to understand some scientific content, which may have affected semantic interpretation and judgment accuracy. The 256 AI-only final labels may contain undetected errors. Detailed limitations and proposed improvements are discussed in the write-up and DataCard.

## References

- [DARWIN 1.5 paper](https://arxiv.org/abs/2412.11970)
- [DARWIN repository](https://github.com/MasterAI-EAM/Darwin)
- [Qwen2.5-1.5B-Instruct model](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)
- [arXiv API](https://export.arxiv.org/api/query)
