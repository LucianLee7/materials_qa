# Predefined QA audit categories

Defined on 3 October 2026, before reviewing generated QA candidates. These categories concern QA quality, not the earlier abstract relevance audit. The 300-pair candidate target is 240 answerable and 60 not-stated pairs; these are design choices, not counts of an existing dataset.

For each reviewed pair, mark every applicable category. A pair with one or more errors counts once toward the overall pair error rate. Category counts may sum to more than the number of erroneous pairs. Record a brief explanation and the source text supporting each finding.

| Code | Category | Definition |
| --- | --- | --- |
| E1 | Source or record integrity | Wrong/missing arXiv ID, wrong source abstract, missing required fields, invalid field values or duplicate qa_id. |
| E2 | Question quality | Ambiguous, false-premise, multi-part, out-of-scope or substantively duplicate question. |
| E3 | Answer support or correctness | Answer adds unstated facts, misreads the abstract, omits a necessary qualifier, or confuses prediction, observation or causation. |
| E4 | Evidence passage | An answerable pair has empty evidence, evidence is not an exact contiguous source substring, or the passage does not support the entire answer. |
| E5 | Answerability or abstention | A not-stated question is actually answered in the abstract; an answerable question lacks a stated answer; or the not-stated answer, empty-passage rule or missing-information explanation is incorrect. |
| E6 | Chemical formula handling | Formula is altered in QA text, original is not preserved, normalization is unjustified, or ambiguity is not recorded. |
| E7 | Numerical and experimental fidelity | Wrong value, unit, sign, uncertainty, range, material assignment or experimental/processing condition. May overlap E3 or E6. |

Before human review, freeze the candidate version and record its hash. Select 50 pairs uniformly at random without replacement using a recorded seed and save their IDs. Audit the original candidates before repairing them, preserving the original findings. If repairs are made, report them separately rather than replacing the original audit error rate.

Report the number reviewed, counts by category, number of pairs with any error, and observed pair error rate. Give a 95% Wilson interval for the binary any-error rate and identify it as a binomial approximation to sampling without replacement; a finite-population interval can be used instead if its method is documented. Do not claim that zero observed errors proves zero dataset errors. Discuss the small sample, possible missed rare errors, reviewer judgement, and any model-generated translations or assistance. This audit measures agreement with the supplied abstracts, not the scientific truth of the papers.

Record every actual collection, preprocessing and QA filter in the data card with its rule, input count, removed count and remaining count. Do not report prompt targets or requested self-checks as completed filters. QA generation, filtering and the 50-pair audit have not yet been completed.
