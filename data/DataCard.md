Raw records: 1,500.

Deduplication rule: Deduplicate by arXiv ID without the version suffix.
For each ID, retain the highest version among the collected records.
If versions are identical, retain the first record.
Records removed: 0.
Records remaining: 1,500.

Abstract validation: Check whether abstracts are missing, are not strings,
or contain only whitespace.
Invalid abstracts found: 0.

Materials relevance screening: 
Status: Pilot completed; full screening not yet completed.

Method: AI-assisted classification based on paper titles and abstracts.
Labels: keep, exclude, review.
Prompt file: prompts/materials_relevance.txt
Model: Astra
Pilot date: 2026-10-01
Full screening date: Not yet run.

Planned validation:
Check JSON validity, ID coverage and uniqueness, allowed labels,
and exact evidence matching against the source abstracts.

Planned human review:
Review all records labelled exclude or review, and a random sample
of records labelled keep.

Final screening counts: Pending.