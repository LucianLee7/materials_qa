# Materials Science Abstract Corpus Data Card

Status: Abstract collection and initial model-assisted relevance classification are complete. Final relevance decisions and human review are pending. This card describes the abstract corpus and screening outputs, not a completed QA dataset.

## Collection

- Source: arXiv API, https://export.arxiv.org/api/query.
- Query: `cat:cond-mat.mtrl-sci`.
- Request settings: `start=0`, `max_results=1500`, `sortBy=submittedDate`, `sortOrder=descending`.
- Returned records: 1,500.
- Publication date range: 12 August to 30 September 2026 (UTC).
- Exact API retrieval timestamp: not recorded.
- Raw file: `data/raw/arxiv_sample.jsonl`.
- Stored fields: source URL, title, abstract, publication timestamp and update timestamp.
- Abstract text is preserved as returned by the API; no chemical formula normalization has been applied.

## Preprocessing and Filter Counts

| Step | Rule | Input records | Records removed | Records remaining |
| --- | --- | ---: | ---: | ---: |
| Deduplication | Compare arXiv IDs without version suffixes; retain the highest collected version and the first record on ties | 1,500 | 0 | 1,500 |
| Abstract validation | Check for missing abstracts, non-string values and whitespace-only strings | 1,500 | 0 | 1,500 |
| Materials relevance filtering | Initial model labels collected; final human decisions pending | 1,500 | Pending | Pending |

The abstract validation script checks and reports invalid records. It does not remove records; none were invalid. The deduplicated corpus currently remains at 1,500 records. Model `exclude` labels have not been used to delete abstracts.

Deduplicated file: `data/processed/arxiv_deduplicated.jsonl`. This adds `arxiv_id` and `arxiv_version` while preserving the original abstract text. Deduplication counts are stored in `data/processed/deduplication_report.json`.

## Relevance Screening Rules

Models receive only each paper's arXiv ID, title and abstract. Scientific text is treated as data rather than instructions. The screening prompt is retained in `prompts/materials_relevance.txt`. Batch membership and request hashes remain in `data/screening_batches/batch_manifest.json`; the batch-specific input and request files were subsequently deleted.

- `keep`: Clearly concerns materials composition, structure, properties, synthesis, processing, characterization or performance in devices. This includes theoretical and computational research and methods explicitly intended to study or assess materials.
- `exclude`: Clearly outside materials research, with no explicit connection to a materials problem.
- `review`: Insufficient information for a confident relevance decision.

The absence of experiments, numerical results or the word material is not a reason for exclusion. Screening assesses relevance, not suitability for QA generation or scientific correctness. Each output contains `arxiv_id`, `decision`, `reason` and an exact contiguous abstract passage as `evidence`, or an empty evidence string when no passage supports the decision.

## Pilot

Ten abstracts were sampled without replacement using `random.Random(66).sample` from the deduplicated corpus. Sampling metadata, including the ten selected IDs, remains in `data/pilot/pilot_manifest.json`. The pilot sample and request files were subsequently deleted.

The user tested Gemini Pro and Gemini 3.5 Flash-Lite through a web interface, and Sol in a separate run. All three returned the same labels: nine `keep` and one `exclude`. Exported Gemini files and the supplied Sol response each passed exact evidence matching for all ten records. Earlier pasted Gemini responses had formatting and notation discrepancies; their cause was not established. The final exported outputs must not be treated as proof that the first responses were error-free.

This was an output and workflow pilot. It did not measure classification accuracy against independently prepared human reference labels. A formal 50-abstract reference-label study has not been recorded. The brief's separate requirement to hand-check 50 QA pairs also remains pending.

## Full Corpus Classification

Gemini was used through the Pro web interface, with the 1,500 abstracts divided in source order into 15 batches of 100. Batch 9 initially omitted `2609.03717`; a separate response supplied that classification as `keep`, with exact supporting evidence. After supplementation, all 1,500 IDs are present exactly once.

Sol classifications were supplied in `data/sol_screening_result.jsonl`, with an identical copy in `data/paper_classifications.jsonl`; these were counted as one run. Both input copies were subsequently deleted after checking that their records were preserved in `data/processed/screening/sol_classifications.jsonl`, which covers all 1,500 IDs exactly once. The precise Sol model version, reasoning setting and full-run request arrangement have not been documented. The precise Gemini backend version and per-run dates have also not been documented; Pro is the web-interface label reported by the user.

| Initial model label | Gemini Pro web | Sol |
| --- | ---: | ---: |
| keep | 1,482 | 1,471 |
| exclude | 15 | 6 |
| review | 3 | 23 |
| Total | 1,500 | 1,500 |

These are model classification counts, not final filter removal counts. No combined final label has been assigned.

## Output Processing and Validation

Outputs were normalized to UTF-8 JSONL and ordered to match the deduplicated corpus. JSON syntax was repaired in 74 Gemini records, addressing invalid backslash escapes and unescaped internal quotation marks. Classification labels and evidence content were not corrected. No model classifications were invented to fill missing records.

The final files passed JSON parsing, required-field and label checks, ID uniqueness and complete source-ID coverage checks.

Exact evidence validation uses `evidence in abstract` after JSON decoding, without whitespace or notation normalization:

| Check | Gemini | Sol |
| --- | ---: | ---: |
| Records with exact non-empty evidence matches | 1,309 | 1,500 |
| Records with evidence not matching an exact source substring | 191 | 0 |

The 191 Gemini evidence mismatches remain unresolved and are listed in `data/processed/screening/evidence_issues.jsonl`. Examples observed include changed chemical formula subscripts and changed whitespace. This is an exact text-matching result, not a count of wrong relevance labels. It does not establish whether a discrepancy originated in generation, web rendering or copying.

The two models agree on 1,471 labels and disagree on 29, giving 98.07% inter-model agreement. Agreement is not accuracy and does not rule out shared mistakes. The disagreements are listed in `data/processed/screening/label_disagreements.jsonl`.

## Files and Provenance

- `data/processed/screening/gemini_classifications.jsonl`: 1,500 Gemini classifications after JSON syntax repair and supplementation.
- `data/processed/screening/sol_classifications.jsonl`: 1,500 Sol classifications.
- `data/processed/screening/classifications_combined.jsonl`: 1,500 records containing both model outputs and label agreement; no final relevance decision.
- `data/processed/screening/evidence_issues.jsonl`: unresolved exact evidence mismatches.
- `data/processed/screening/label_disagreements.jsonl`: the 29 records with different model labels.
- `data/processed/screening/merge_report.json`: processing counts, syntax repair entries and input hashes. Historical paths in this report may refer to files subsequently deleted.

At the user's request, the Gemini raw batch responses, raw supplement, merge script, pilot sampling script and batch-generation script were removed from the workspace. The pilot sample and request files and the 15 batch input and request files were also subsequently deleted. The pilot and batch manifests, original arXiv corpus, screening prompt and processed outputs remain. As a result, the original Gemini replies and the exact normalization procedure cannot be fully reproduced from the current repository alone. Historical hashes and repair metadata remain but do not replace the deleted originals.

## Pending Work

Human adjudication of relevance labels, examination of evidence mismatches, and a final relevance-filter rule have not been completed. Final removal counts will be added after these decisions. QA generation, not-stated QA cases, chemical formula normalization policy, QA error categories, the random 50-pair human audit and contextual open-model evaluation are also pending.
