# Human spot-check of unflagged full-run judgments

Review and clarification completed on 12 October 2026. Thirty cases were sampled uniformly without replacement from the 286 unflagged original AI judgments, using random.Random(66).sample in file order. Ordered IDs and source hash are retained in unflagged_spotcheck_manifest.json.

The user reviewed complete abstracts, Chinese translations, questions and Qwen responses one at a time. AI labels, AI reasons and reference answers were withheld during initial presentation. Earlier project discussion and exposure to some calibration cases mean this was not fully blinded or independent; translations and presentation remain AI assistance. Initial decisions were recorded before comparison. Two decisions were corrected after the assistant disclosed disagreements and explained rubric concerns.

## Initial comparison and subsequent clarification

Initial human labels: 22 supported, 3 unsupported and 5 correctly abstained. Initial observed agreement: 28/30 = 93.33%.

After clarification, final human labels: 21 supported, 5 unsupported and 4 correctly abstained. Final agreement: 30/30 = 100%. This final agreement incorporates discussion informed by the AI labels and must not be presented as independent judge accuracy. The initial 93.33% remains the relevant pre-clarification comparison. Neither percentage is whole-dataset response performance.

| Sample | QA ID | AI label | Initial human label | Final human label |
| ---: | --- | --- | --- | --- |
| 1 | all_037 | supported | supported | supported |
| 2 | all_170 | supported | supported | supported |
| 3 | all_236 | supported | supported | supported |
| 4 | all_135 | supported | supported | supported |
| 5 | all_242 | unsupported | unsupported | unsupported |
| 6 | all_160 | supported | supported | supported |
| 7 | all_140 | supported | supported | supported |
| 8 | all_049 | supported | supported | supported |
| 9 | all_268 | correctly_abstained | correctly_abstained | correctly_abstained |
| 10 | all_100 | supported | supported | supported |
| 11 | all_253 | unsupported | correctly_abstained | unsupported |
| 12 | all_282 | unsupported | unsupported | unsupported |
| 13 | all_067 | supported | supported | supported |
| 14 | all_036 | supported | supported | supported |
| 15 | all_199 | supported | supported | supported |
| 16 | all_091 | supported | supported | supported |
| 17 | all_221 | supported | supported | supported |
| 18 | all_248 | correctly_abstained | correctly_abstained | correctly_abstained |
| 19 | all_273 | correctly_abstained | correctly_abstained | correctly_abstained |
| 20 | all_016 | supported | supported | supported |
| 21 | all_285 | correctly_abstained | correctly_abstained | correctly_abstained |
| 22 | all_059 | supported | supported | supported |
| 23 | all_209 | supported | supported | supported |
| 24 | all_074 | supported | supported | supported |
| 25 | all_202 | unsupported | supported | unsupported |
| 26 | all_013 | supported | supported | supported |
| 27 | all_005 | supported | supported | supported |
| 28 | all_113 | supported | supported | supported |
| 29 | all_174 | supported | supported | supported |
| 30 | all_262 | unsupported | unsupported | unsupported |

## Resolved cases

- Sample 11, all_253: initially correctly_abstained, explicitly corrected by the user to unsupported after the unsupported approximately-one-step claim was highlighted.
- Sample 25, all_202: initially supported, explicitly corrected by the user to unsupported after the omission of domain-wall width and the earlier strict-completeness decision were highlighted.

Initial choices and correction notes are retained in unflagged_human_spotcheck.jsonl. No additional human rationale is inferred from a label-only correction. Prior calibration decisions and original AI records are unchanged.

## Current full-set results

All 30 final spot-check decisions have been applied to qwen_classifications_adjudicated.jsonl alongside the 14 flagged-case adjudications. There are 44 human-reviewed full-run records and 256 records whose current labels remain AI-only. The earlier 30-case calibration is separate and not added to this full-run review count.

| Classification | Count | Percentage of 300 |
| --- | ---: | ---: |
| supported | 215 | 71.67% |
| unsupported | 42 | 14.00% |
| correctly_abstained | 43 | 14.33% |

Supported answers plus correct abstentions: 258/300 = 86.00%. This is a rubric-based result on the fixed dataset, not independently verified scientific accuracy. The sample can miss disagreements, and human judgments and translations may themselves contain errors.

Original QA, Qwen responses and AI judgments are preserved. No question was removed. The ambiguity of all_152 remains separately documented.

## Provenance

- unflagged_spotcheck_manifest.json SHA-256: `6b40d87a778c58fa3783dfe33447713ddf5eeef7a4439494f6d88fa7b9dee5df`
- unflagged_human_spotcheck.jsonl SHA-256: `5a1fb5200c95208115e26bb60824294a6b716ff3c9ab47852b1ce98c0eb0d67b`
- codex_full_judgments.jsonl SHA-256: `2ebc7df4d9352b50077f941b4fdcaf815274eed20a9f8e60e9939f57ddd115df`
- qwen_classifications_adjudicated.jsonl SHA-256: `dbec8e9bdc70d5f595ca0b7e917869ba665185adb214aa9c15374b6673e6a592`
