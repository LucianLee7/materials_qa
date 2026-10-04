import json
from pathlib import Path

input_path = Path("data/processed/arxiv_deduplicated.jsonl")

papers = []

with input_path.open("r", encoding="utf-8") as file:
    for line in file:
        papers.append(json.loads(line))

missing_abstract_count = 0

for paper in papers:
    abstract = paper.get("abstract")

    # Check whether the abstract is a string containing non-whitespace text.
    if not isinstance(abstract, str) or not abstract.strip():
        missing_abstract_count += 1

print("Total records:", len(papers))
print("Missing or blank abstracts:", missing_abstract_count)
