import json
import re
from pathlib import Path


input_path = Path("data/raw/arxiv_sample.jsonl")
output_path = Path("data/processed/arxiv_deduplicated.jsonl")
report_path = Path("data/processed/deduplication_report.json")

# Store papers using their arXiv IDs as keys.
unique_papers = {}
input_count = 0

with input_path.open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        # Stop on malformed input rather than silently dropping records.
        paper = json.loads(line)
        source_url = paper["source_url"]

        # Separate the arXiv ID from its version number.
        versioned_id = source_url.split("/abs/", 1)[1]
        match = re.fullmatch(r"(.+)v(\d+)", versioned_id)

        if match is None:
            raise ValueError(
                f"Missing or invalid arXiv version at line {line_number}"
            )

        arxiv_id = match.group(1)
        version = int(match.group(2))

        paper["arxiv_id"] = arxiv_id
        paper["arxiv_version"] = version
        input_count += 1

        # Keep the first record for each ID; replace it only with a higher version.
        if arxiv_id not in unique_papers:
            unique_papers[arxiv_id] = paper
        elif version > unique_papers[arxiv_id]["arxiv_version"]:
            unique_papers[arxiv_id] = paper

output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as file:
    for paper in unique_papers.values():
        file.write(json.dumps(paper, ensure_ascii=False) + "\n")

report = {
    "input_file": str(input_path),
    "output_file": str(output_path),
    "rule": "Deduplicate by arXiv ID; keep highest version; keep first on ties.",
    "input_records": input_count,
    "duplicates_removed": input_count - len(unique_papers),
    "output_records": len(unique_papers),
}

with report_path.open("w", encoding="utf-8") as file:
    json.dump(report, file, ensure_ascii=False, indent=2)

print(json.dumps(report, indent=2))