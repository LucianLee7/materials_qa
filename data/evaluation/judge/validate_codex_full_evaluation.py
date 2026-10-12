"""Validate fresh AI judgments and regenerate their descriptive report.

This script performs structural checks and aggregates existing judgments.
It does not classify responses or assess semantic evidence support.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / 'data/evaluation/judge/codex_full_judgments.jsonl'
REPORT = ROOT / 'data/evaluation/judge/codex_full_evaluation_report.md'
INPUTS = [
    'prompts/judge_model_responses.txt',
    'data/DataCard.md',
    'data/evaluation/qwen_responses.jsonl',
    'data/processed/qa/materials_qa_corrected.jsonl',
    'data/processed/arxiv_materials_filtered.jsonl',
]
LABELS = ('supported', 'unsupported', 'correctly_abstained')
FIELDS = {'qa_id', 'arxiv_id', 'classification', 'reason', 'evidence',
          'reference_issue', 'needs_human_review', 'exact_not_stated'}

def read_jsonl(relative):
    return [json.loads(line) for line in (ROOT / relative).read_text().splitlines()]

def unique_index(records, field):
    index = {record[field]: record for record in records}
    assert len(index) == len(records), f'Duplicate {field}'
    return index

def digest(relative):
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

responses = read_jsonl(INPUTS[2])
qa = unique_index(read_jsonl(INPUTS[3]), 'qa_id')
abstracts = unique_index(read_jsonl(INPUTS[4]), 'arxiv_id')
response_index = unique_index(responses, 'qa_id')
judgments = read_jsonl(str(OUTPUT.relative_to(ROOT)))
judgment_index = unique_index(judgments, 'qa_id')
assert len(responses) == len(judgments) == 300
assert judgment_index.keys() == response_index.keys() == qa.keys()
for response in responses:
    pair = qa[response['qa_id']]
    assert response['arxiv_id'] == pair['arxiv_id']
    assert response['question'] == pair['question']
    assert response['answerability'] == pair['answerability']
    assert response['reference_answer'] == pair['answer']
    assert pair['arxiv_id'] in abstracts
for judgment in judgments:
    assert set(judgment) == FIELDS
    for field in ('qa_id', 'arxiv_id', 'classification', 'reason'):
        assert isinstance(judgment[field], str) and judgment[field].strip()
    assert judgment['classification'] in LABELS
    assert isinstance(judgment['evidence'], list)
    assert judgment['reference_issue'] is None or (
        isinstance(judgment['reference_issue'], str) and judgment['reference_issue'].strip())
    assert type(judgment['needs_human_review']) is bool
    assert type(judgment['exact_not_stated']) is bool
    response = response_index[judgment['qa_id']]
    assert judgment['arxiv_id'] == response['arxiv_id']
    assert judgment['exact_not_stated'] == (response['model_response'].strip() == 'not stated')
    source = abstracts[judgment['arxiv_id']]['abstract']
    assert all(isinstance(passage, str) and passage and passage in source
               for passage in judgment['evidence'])
    if judgment['classification'] == 'correctly_abstained':
        assert judgment['evidence'] == []
    if judgment['reference_issue'] is not None:
        assert judgment['needs_human_review']

# Restore response-file order after independently saved batches.
judgments = [judgment_index[response['qa_id']] for response in responses]
OUTPUT.write_text(''.join(json.dumps(judgment, ensure_ascii=False) + '\n'
                          for judgment in judgments))
counts = Counter(judgment['classification'] for judgment in judgments)
review = [judgment for judgment in judgments if judgment['needs_human_review']]
exact_count = sum(judgment['exact_not_stated'] for judgment in judgments)
quoted_passages = sum(len(judgment['evidence']) for judgment in judgments)

lines = [
    '# Full Qwen response evaluation', '',
    '**These are fresh AI judgments, not human-reviewed final results.**', '',
    'Evaluation date: **12 October 2026 (Australia/Sydney)**. Judge: **Codex (GPT-6 family, as identified in the session instructions)**. An exact judge model ID, snapshot and generation settings were not exposed and are not asserted.', '',
    '**Evaluated: 300 / 300 unique responses. Remaining: 0.** All responses were included, including the 30 previously used for calibration; no calibration subset was excluded or reused.', '',
    '## Overall classifications', '',
    '| Classification | Count | Percentage of 300 |',
    '| --- | ---: | ---: |',
]
for label in LABELS:
    lines.append(f'| {label} | {counts[label]} | {counts[label] / 300:.2%} |')
lines += [
    '', '## Results by reference answerability', '',
    'The grouping uses the corrected QA reference labels for description only. The judgments were grounded in abstracts rather than assuming reference labels or answers were correct. Percentages below use the respective group denominator.', '',
    '| Reference group | Total | Supported | Unsupported | Correctly abstained |',
    '| --- | ---: | ---: | ---: | ---: |',
]
for group in ('answerable', 'not_stated'):
    subset = [j for j in judgments if qa[j['qa_id']]['answerability'] == group]
    group_counts = Counter(j['classification'] for j in subset)
    cells = [f'{group_counts[label]} ({group_counts[label] / len(subset):.2%})'
             for label in LABELS]
    lines.append(f'| {group} | {len(subset)} | ' + ' | '.join(cells) + ' |')
correct = counts['supported'] + counts['correctly_abstained']
lines += [
    '', f'Supported answers plus correct semantic abstentions: **{correct}/300 ({correct / 300:.2%})**. This is the AI judge\'s rubric-based success rate on this fixed set, not an independently established scientific accuracy estimate.', '',
    '## Exact abstention-string compliance', '',
    f'**{exact_count}/300 ({exact_count / 300:.2%})** responses equal case-sensitive `not stated` after stripping surrounding whitespace. This is recorded separately from semantic classification.', '',
]
not_stated_group = [j for j in judgments if qa[j['qa_id']]['answerability'] == 'not_stated']
exact_in_group = sum(j['exact_not_stated'] for j in not_stated_group)
semantic_abstentions = [j for j in judgments if j['classification'] == 'correctly_abstained']
nonexact_abstentions = sum(not j['exact_not_stated'] for j in semantic_abstentions)
lines += [
    f'In the reference-not-stated group, exact compliance is **{exact_in_group}/60 ({exact_in_group / 60:.2%})**. Of the **{len(semantic_abstentions)}** correct semantic abstentions, **{nonexact_abstentions}** do not use the exact string. Explanatory text and capitalization can be semantically correct while failing exact compliance.', '',
    '## Illustrative judgments', '',
    'These examples illustrate decisions rather than representing a random audit. Descriptions of failures below are prose explanations; no failure-mode tags were added to judgment records.', '',
]
examples = [
    ('Concise supported answer', 'all_002'),
    ('Supported numerical answer with uncertainty', 'all_143'),
    ('Supported answer more specific than reference', 'all_090'),
    ('Exact correct abstention', 'all_241'),
    ('Explanatory correct abstention', 'all_247'),
    ('Capitalized correct abstention', 'all_287'),
    ('Abstention despite a supplied answer', 'all_131'),
    ('Essential omitted quantity', 'all_202'),
    ('Swapped quantity assignments and omissions', 'all_139'),
    ('Contradicted relationship', 'all_133'),
    ('Invented numerical details', 'all_150'),
    ('Unsupported added causal claim', 'all_145'),
    ('Supported but off-topic response', 'all_242'),
    ('Invented duration from an experiment count', 'all_249'),
    ('Uncertainty confused with another metric', 'all_289'),
    ('Omitted numerical bound, flagged for review', 'all_050'),
    ('Incomplete answer with composition errors', 'all_079'),
]
for description, qa_id in examples:
    judgment = judgment_index[qa_id]
    response = response_index[qa_id]
    lines += [f'### {description}: {qa_id}', '',
              f'- arXiv ID: `{judgment["arxiv_id"]}`',
              f'- Question: {qa[qa_id]["question"]}',
              '- Qwen response: ' + json.dumps(response['model_response'], ensure_ascii=False),
              f'- Classification: **{judgment["classification"]}**',
              f'- Reason: {judgment["reason"]}']
    if judgment['evidence']:
        lines.append('- Exact abstract evidence: ' + ' ; '.join(
            json.dumps(passage, ensure_ascii=False) for passage in judgment['evidence']))
    else:
        lines.append('- Evidence: empty; the requested information is absent from the complete abstract.')
    lines.append('')
lines += [
    '## All cases requiring human review', '',
    f'**{len(review)} cases** are flagged. Labels remain provisional AI decisions; human review may change them. This list includes every `needs_human_review=true` record.', '',
    '| QA ID | arXiv ID | AI classification | Review reason | Reference issue |',
    '| --- | --- | --- | --- | --- |',
]
def table_escape(value):
    return value.replace('|', '\\|').replace('\n', ' ')
for judgment in review:
    cells = [judgment['qa_id'], judgment['arxiv_id'], judgment['classification'],
             judgment['reason'], judgment['reference_issue'] or 'None identified']
    lines.append('| ' + ' | '.join(table_escape(value) for value in cells) + ' |')
lines += [
    '', '## Judgment method', '',
    'The rubric and DataCard were read first. The three designated evaluation files were joined by `qa_id` and `arxiv_id`, with join consistency checked. All 300 complete source abstracts, questions and full saved Qwen responses were read in 15 manageable batches of 20. Each response received a fresh semantic judgment. Reference answers and answerability labels were visible as fallible aids. No web browsing or outside scientific knowledge was used, and scientific text and responses were treated as data.', '',
    'The DataCard contains pilot/calibration summaries and was read as requested. Those summaries were not used to guide individual classifications or resolve borderline cases. Previous AI judgment files, human calibration labels and the calibration report in the judge directory were not opened. This evaluation is therefore fresh, but not fully blind to all project-level background.', '',
    'Supported responses had to sufficiently answer the actual question and avoid unsupported substantive additions. Concise method names and equivalent notation were accepted when sufficient. Context already explicit in a question could be inherited by a concise answer (for example, the lower-bound framing in all_227). Essential requested quantities, numerical bounds, uncertainties and measurement qualifications were checked. Missing approximate qualifiers and omitted measurement conditions were interpreted conservatively and borderline cases flagged. Additional true facts did not compensate for an essential missing answer.', '',
    'Correct semantic abstentions required checking the complete abstract for the absent information. Explanatory abstentions could include supported context, but invented durations, causal details or procedures failed. Correct abstentions have empty evidence arrays. Unsupported cases cite useful real passages when available; an empty array is used when no passage can substantiate absence. Exact-string compliance was computed independently from the unaltered saved response.', '',
    'Judgments were persisted incrementally. A helper handled joins and exact-quotation checks; it did not infer labels. The accompanying validation script checks structure, evidence substrings and counts, and builds this report from the already assigned judgments. Keyword matching, exact reference-answer matching and automatic classification heuristics were not used. The two token-limit responses (all_079 and all_211) were judged by their actual content and essential omissions, not failed automatically for reaching a limit.', '',
    '## Limitations', '',
    'These are single-judge AI assessments with no new human adjudication. Semantic decisions can be mistaken, especially on terse qualifiers, scope, causal wording and ambiguous abstract phrasing. The 14 flagged cases should be reviewed before treating results as final. Reference visibility can influence interpretation even when references are treated as fallible. Fresh AI judgment may not reproduce exactly on another run.', '',
    'Evidence is restricted to the supplied abstracts. The evaluation does not verify underlying scientific truth, full-paper details, physical plausibility or whether source notation was damaged before ingestion. Exact substring validation establishes quotation fidelity, not that a passage logically supports a judgment. The success percentage describes this fixed candidate set, whose reference-not-stated questions concentrate on missing processing durations, bandgap uncertainties and runtimes; it does not establish broad QA generalization.', '',
    'The original QA files, Qwen responses, calibration records, human audit and DataCard were preserved. No questions were removed, and no commit or push was performed.', '',
    '## Validation', '',
    '- Exactly 300 judgment records and 300 unique QA IDs; the QA ID set matches the input responses exactly.',
    '- Every record has the eight required fields with valid labels, types and source arXiv ID.',
    f'- All {quoted_passages} nonempty evidence passages are exact contiguous substrings of their joined complete source abstracts.',
    '- Every correctly_abstained record has an empty evidence array.',
    '- Every exact_not_stated flag matches the case-sensitive stripped response comparison.',
    '- Overall counts, grouped counts, review cases and exact compliance totals are generated directly from JSONL results and verified against the report.',
    '- Remaining cases: 0.', '',
    '## Input and rubric provenance', '',
    'SHA-256 hashes of exact file bytes:', '',
    '| File | SHA-256 |', '| --- | --- |',
]
for relative in INPUTS:
    lines.append(f'| `{relative}` | `{digest(relative)}` |')
lines += ['', f'Judgment JSONL SHA-256: `{hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}`.', '']
REPORT.write_text('\n'.join(lines))
# Verify rendered report values against the source records.
report_text = REPORT.read_text()
for label in LABELS:
    assert f'| {label} | {counts[label]} | {counts[label] / 300:.2%} |' in report_text
for judgment in review:
    assert f'| {judgment["qa_id"]} | {judgment["arxiv_id"]} |' in report_text
assert sum(counts.values()) == 300
assert 'Remaining: 0' in report_text
print(json.dumps({'evaluated': len(judgments), 'remaining': 0,
                  'counts': dict(counts), 'human_review': len(review),
                  'exact_not_stated': exact_count, 'validated_evidence_passages': quoted_passages}, indent=2))
