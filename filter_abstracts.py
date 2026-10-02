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

    # 检查摘要是否为字符串，以及是否只包含空白
    if not isinstance(abstract, str) or not abstract.strip():
        missing_abstract_count += 1

print("Total records:", len(papers))
print("Missing or blank abstracts:", missing_abstract_count)
