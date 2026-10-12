# Codex Sol Judge Calibration: Final Human Review Report

**Review date:** 12 October 2026 (review completion)  
**AI pilot date:** 6 October 2026  
**Task:** Evidence-grounded evaluation of Qwen responses to materials-science questions using supplied arXiv abstracts.  
**Status:** All 30 human review labels recorded.

## Executive summary

The 30-case stratified calibration sample consisted of 20 reference-answerable and 10 reference-not-stated questions, selected with seed 66. The provisional Codex Sol judge labels were compared with the subsequently recorded human semantic labels. All 30 labels matched (observed label agreement: **30/30 = 100%**). Both assessments assign **19 supported**, **4 unsupported**, and **7 correctly abstained**. These figures are *sample-specific label counts*, not performance estimates for the complete QA dataset.

Two semantically correct abstentions (**all_264** and **all_251**) were separately flagged by the human reviewer as exact-output-format violations. For **all_287**, capitalization-only variation was explicitly *not* flagged as a violation. The absence of a recorded format flag for other items should not be read as an exhaustive format audit.

**Interpretation caution:** This was not a blinded or isolated human–AI study. Earlier AI judge judgments existed within the same conversation, even when labels were withheld during individual review prompts. The 100% agreement is therefore descriptive, rather than an independently established accuracy rate or proof of judge reliability. No second independent human rater or adjudication is recorded.

## Method

1. The review set was drawn from `calibration_inputs.jsonl`. Each human review considered the complete abstract, question and Qwen response as the basis for classification.
2. The semantic rubric distinguished **supported** (sufficient, grounded and complete answer), **unsupported** (incorrect, ungrounded, off-topic or materially incomplete response), and **correctly_abstained** (appropriate acknowledgement that the abstract does not provide the requested answer).
3. Human labels were preserved separately from provisional Codex Sol labels. Format compliance was a separate dimension for explicitly reviewed cases.
4. Codex Sol was the reported display name; exact model identifier, snapshot and sampling parameters were unavailable. No outside sources were used for the original judgments.

## Results

| Semantic label | Human | Provisional AI |
|---|---:|---:|
| Supported | 19 | 19 |
| Unsupported | 4 | 4 |
| Correctly abstained | 7 | 7 |
| **Total** | **30** | **30** |

**Observed agreement:** 30 matching cases / 30 reviewed = **100%**.  
**Disagreements:** None.  
**Exact-output violations explicitly recorded:** 2 cases (`all_264`, `all_251`).

## Full item-level comparison

| # | QA ID | Human label | Codex Sol label | Agreement | Exact-output violation |
|---:|---|---|---|---|---|
| 1 | all_019 | supported | supported | Yes | Not separately recorded |
| 2 | all_080 | supported | supported | Yes | Not separately recorded |
| 3 | all_112 | supported | supported | Yes | Not separately recorded |
| 4 | all_237 | supported | supported | Yes | Not separately recorded |
| 5 | all_064 | supported | supported | Yes | Not separately recorded |
| 6 | all_202 | unsupported | unsupported | Yes | Not separately recorded |
| 7 | all_115 | supported | supported | Yes | Not separately recorded |
| 8 | all_076 | supported | supported | Yes | Not separately recorded |
| 9 | all_066 | supported | supported | Yes | Not separately recorded |
| 10 | all_221 | supported | supported | Yes | Not separately recorded |
| 11 | all_201 | supported | supported | Yes | Not separately recorded |
| 12 | all_144 | supported | supported | Yes | Not separately recorded |
| 13 | all_025 | supported | supported | Yes | Not separately recorded |
| 14 | all_191 | supported | supported | Yes | Not separately recorded |
| 15 | all_222 | supported | supported | Yes | Not separately recorded |
| 16 | all_238 | supported | supported | Yes | Not separately recorded |
| 17 | all_216 | supported | supported | Yes | Not separately recorded |
| 18 | all_127 | supported | supported | Yes | Not separately recorded |
| 19 | all_048 | supported | supported | Yes | Not separately recorded |
| 20 | all_120 | supported | supported | Yes | Not separately recorded |
| 21 | all_274 | unsupported | unsupported | Yes | Not separately recorded |
| 22 | all_249 | unsupported | unsupported | Yes | Not separately recorded |
| 23 | all_291 | correctly_abstained | correctly_abstained | Yes | Not separately recorded |
| 24 | all_286 | correctly_abstained | correctly_abstained | Yes | Not separately recorded |
| 25 | all_245 | correctly_abstained | correctly_abstained | Yes | Not separately recorded |
| 26 | all_297 | correctly_abstained | correctly_abstained | Yes | Not separately recorded |
| 27 | all_264 | correctly_abstained | correctly_abstained | Yes | Yes |
| 28 | all_287 | correctly_abstained | correctly_abstained | Yes | No |
| 29 | all_251 | correctly_abstained | correctly_abstained | Yes | Yes |
| 30 | all_267 | unsupported | unsupported | Yes | Not separately recorded |

## Notable qualitative cases

- **all_202 — incomplete yet factually grounded response.** Qwen named interfacial Dzyaloshinskii–Moriya interaction but omitted domain-wall width, which the question also required. The strict-completeness rubric classified this as unsupported rather than supported.
- **all_274 — unsupported extrapolation.** The abstract identifies substrates but supplies no deposition/growth duration. Qwen asserted substrate-dependent growth durations and tailored conditions not established by the abstract.
- **all_249 — quantity/unit confusion.** The stated **18 autonomous experiments** were incorrectly transformed into **18 seconds** of individual film deposition time.
- **all_267 — answer-type mismatch.** A question about how long CrN deposition lasted was answered with a temperature range of **400–800 °C**.
- **all_264 and all_251 — semantic abstention with format noncompliance.** Both clearly acknowledged absence of requested duration but did not output the exact instructed `not stated` string. Semantic and formatting results remain separated.
- **all_287 — capitalization variation accepted.** The reviewer recorded no exact-output violation for `Not stated`.

## Limitations and interpretation

- This stratified sample is small and intentionally oversamples not-stated questions relative to the full dataset (10/30 = 33.3% in the sample versus 60/300 = 20% in the full QA set); the label distribution and any derived response success proportion should **not** be extrapolated to the full dataset.
- Observed agreement is not a blind measure of Codex Sol accuracy. Prior discussion of provisional AI labels could influence human judgments, even though labels were not re-shown during per-item review.
- The source records do not establish the exact Codex Sol model ID, snapshot, sampling configuration or a reproducible isolated judge run.
- No independent second human annotator, inter-human agreement assessment or third-party adjudication was performed.
- Format flags were explicitly recorded for the final three relevant reviewed items; do not interpret unspecified cells as negative findings.

## Conclusion

For these 30 examined examples, Codex Sol's provisional semantic classifications and the recorded human classifications are identical. The audit also captures error distinctions hidden by a single three-way label, including answer incompleteness, fabricated time values, response-type mismatch and exact-output compliance. A larger **prospectively blinded** and independently annotated sample would be needed to make defensible claims about judge generalizability or accuracy.
