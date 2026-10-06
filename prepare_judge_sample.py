"""Prepare a reproducible stratified sample for AI-judge calibration."""

import hashlib
import json
import random
from pathlib import Path

SEED = 66
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "data/evaluation/judge"
SOURCES = {
    "qa": ROOT / "data/processed/qa/materials_qa_corrected.jsonl",
    "abstracts": ROOT / "data/processed/arxiv_materials_filtered.jsonl",
    "responses": ROOT / "data/evaluation/qwen_responses.jsonl",
    "rubric": ROOT / "prompts/judge_model_responses.txt",
}


def read_jsonl(path):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return rows


def indexed(rows, key):
    result = {row[key]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"Duplicate {key} values")
    return result


def main():
    qa = indexed(read_jsonl(SOURCES["qa"]), "qa_id")
    abstracts = indexed(read_jsonl(SOURCES["abstracts"]), "arxiv_id")
    responses = read_jsonl(SOURCES["responses"])
    if set(indexed(responses, "qa_id")) != set(qa):
        raise ValueError("Response and QA IDs differ")
    rng = random.Random(SEED)
    selected = []
    for label, count in [("answerable", 20), ("not_stated", 10)]:
        pool = [row for row in responses if qa[row["qa_id"]]["answerability"] == label]
        selected.extend(rng.sample(pool, count))
    items = []
    for response in selected:
        candidate = qa[response["qa_id"]]
        for key in ["arxiv_id", "question"]:
            if response[key] != candidate[key]:
                raise ValueError(f"Mismatched {key}: {response['qa_id']}")
        items.append({
            "qa_id": response["qa_id"],
            "arxiv_id": response["arxiv_id"],
            "abstract": abstracts[response["arxiv_id"]]["abstract"],
            "question": response["question"],
            "model_response": response["model_response"],
            "reference_answer": candidate["answer"],
            "reference_answerability": candidate["answerability"],
            "reference_supporting_passage": candidate["supporting_passage"],
            "not_stated_reason": candidate["not_stated_reason"],
            "hit_token_limit": response["hit_token_limit"],
        })
    manifest = {
        "seed": SEED,
        "method": "Sequential random.Random(66).sample calls on answerable then not_stated pools in response-file order",
        "strata": {"answerable": 20, "not_stated": 10},
        "selected_qa_ids": [item["qa_id"] for item in items],
        "source_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in SOURCES.items()},
        "purpose": "AI-judge calibration, separate from the original 50-pair human QA audit",
        "limitations": "Stratified sample overrepresents not-stated cases; raw counts are not full-dataset performance estimates. Human labels are pending.",
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    outputs = {
        "calibration_inputs.jsonl": "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in items),
        "calibration_manifest.json": json.dumps(manifest, indent=2) + "\n",
    }
    for name, content in outputs.items():
        path = OUTPUT / name
        if path.exists() and path.read_text() != content:
            raise FileExistsError(f"Refusing to replace different content: {path}")
    for name, content in outputs.items():
        (OUTPUT / name).write_text(content)
    print(f"Prepared {len(items)} calibration inputs in {OUTPUT}")


if __name__ == "__main__":
    main()
