# Human adjudication of flagged Qwen response judgments

Review completed on 12 October 2026. All 14 cases flagged by the full AI judge were reviewed by the human user. Complete abstracts, Chinese translations, questions, Qwen responses, references and AI judgments were presented in the conversation. This was targeted, non-blinded adjudication with AI presentation assistance, not an independent random audit. Final user corrections supersede earlier choices. No additional human rationale is inferred where only a label was supplied.

Observed agreement on the flagged cases: 12/14 = 85.71%. This selected subset does not estimate overall judge accuracy.

## Human decisions

| QA ID | Original AI label | Final human label | Changed |
| --- | --- | --- | --- |
| all_050 | unsupported | unsupported | No |
| all_069 | supported | unsupported | Yes |
| all_070 | unsupported | unsupported | No |
| all_071 | unsupported | unsupported | No |
| all_090 | supported | supported | No |
| all_104 | unsupported | unsupported | No |
| all_111 | unsupported | unsupported | No |
| all_132 | unsupported | unsupported | No |
| all_152 | supported | supported | No |
| all_164 | unsupported | supported | Yes |
| all_186 | unsupported | unsupported | No |
| all_192 | unsupported | unsupported | No |
| all_228 | unsupported | unsupported | No |
| all_256 | correctly_abstained | correctly_abstained | No |

Two decisions changed: all_069 from supported to unsupported, and all_164 from unsupported to supported. The total counts therefore remain unchanged, despite these item-level corrections.

The reviewer identified ambiguity in all_152: the question does not distinguish the measured Hall conductivity from the calculated intrinsic conductivity. The response was nevertheless classified as supported. The question itself remains unchanged; this concern is retained separately and should be disclosed as a dataset limitation.

## Results after adjudication

| Classification | Count | Percentage of 300 |
| --- | ---: | ---: |
| supported | 215 | 71.67% |
| unsupported | 42 | 14.00% |
| correctly_abstained | 43 | 14.33% |

| Reference answerability | Total | Supported | Unsupported | Correctly abstained |
| --- | ---: | ---: | ---: | ---: |
| answerable | 240 | 215 | 25 | 0 |
| not_stated | 60 | 0 | 17 | 43 |

Supported answers plus correct semantic abstentions: 258/300 = 86.00%. This is a rubric-based result on the fixed dataset, not independently established scientific accuracy.

This report describes the 14 flagged-case adjudications. Subsequently, 30 of the 286 unflagged cases received a random human spot-check, documented in unflagged_spotcheck_report.md. The current full-set file incorporates both stages: 44 human-reviewed records and 256 AI-only records. The earlier 30-case calibration remains separate.

## Records

- codex_full_judgments.jsonl: unchanged original AI decisions. Its human-review flags describe the original run.
- full_human_review.jsonl: human decisions and question-ambiguity note.
- qwen_classifications_adjudicated.jsonl: 300 current classifications incorporating flagged adjudication and the subsequent spot-check, with original AI labels and reasons plus the basis of each current label. AI evidence and reasons remain AI-generated even on human-reviewed cases.

QA records and Qwen responses were not changed. This adjudication addresses the flagged decisions; it does not establish that every unflagged judgment is correct.

## Provenance

- codex_full_judgments.jsonl SHA-256: `2ebc7df4d9352b50077f941b4fdcaf815274eed20a9f8e60e9939f57ddd115df`
- full_human_review.jsonl SHA-256: `2667b704a9a6a7b43ff4f206f43c69233cb93444d9efcb944316c0c4de061523`
- qwen_classifications_adjudicated.jsonl SHA-256: `dbec8e9bdc70d5f595ca0b7e917869ba665185adb214aa9c15374b6673e6a592`
