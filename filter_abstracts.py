import json
import random
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

# 固定随机种子，使相同输入下的抽样结果可复现
rng = random.Random(66)
sample = rng.sample(papers, k=10)


for index, paper in enumerate(sample, start=1):
    print(f"\n--- Paper {index} ---")
    print("arXiv ID:", paper["arxiv_id"])
    print("Title:", paper["title"])
    print("Abstract:", paper["abstract"])