"""Sample records from a user-provided JSONL file using a fixed seed of 66."""

import argparse
import hashlib
import json
import random
from pathlib import Path


SEED = 66


def main():
    parser = argparse.ArgumentParser(description="Sample JSONL records without replacement using a fixed seed")
    parser.add_argument("input", type=Path, help="Input JSONL file")
    parser.add_argument("output", type=Path, help="Output sample JSONL file")
    parser.add_argument("--count", type=int, required=True, help="Number of records to sample, e.g. 10 or 50")
    parser.add_argument("--agreed-keep", action="store_true", help="Sample only records labelled keep by both Gemini and Sol")
    parser.add_argument("--gemini", type=Path, default=Path("data/processed/screening/gemini_classifications.jsonl"))
    parser.add_argument("--sol", type=Path, default=Path("data/processed/screening/sol_classifications.jsonl"))
    args = parser.parse_args()

    # Record the input hash to verify the data version when reproducing samples.
    input_bytes = args.input.read_bytes()
    records = []
    for line_number, line in enumerate(input_bytes.decode("utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError(f"Line {line_number} is empty; clean the input file first")
        record = json.loads(line)
        if not isinstance(record, dict):
            raise ValueError(f"Line {line_number} must contain a JSON object")
        records.append(record)

    input_count = len(records)
    model_sources = {}
    if args.agreed_keep:
        labels = {}
        for name, path in (("gemini", args.gemini), ("sol", args.sol)):
            raw = path.read_bytes()
            model_records = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
            labels[name] = {record["arxiv_id"]: record["decision"] for record in model_records}
            if len(labels[name]) != len(model_records):
                raise ValueError(f"{name} classification file contains duplicate arXiv IDs")
            if any(label not in ("keep", "exclude", "review") for label in labels[name].values()):
                raise ValueError(f"{name} classification file contains invalid labels")
            model_sources[name] = {"file": str(path), "sha256": hashlib.sha256(raw).hexdigest()}
        # Filter in source order, then randomly sample from eligible records.
        eligible = []
        for record in records:
            arxiv_id = record["arxiv_id"]
            if any(arxiv_id not in labels[name] for name in labels):
                raise ValueError(f"Classification files are missing {arxiv_id}")
            if all(labels[name][arxiv_id] == "keep" for name in labels):
                eligible.append(record)
        records = eligible

    if not 1 <= args.count <= len(records):
        raise ValueError(f"Sample count must be between 1 and {len(records)}")

    manifest_path = args.output.with_suffix(".manifest.json")
    if args.output.exists() or manifest_path.exists():
        raise FileExistsError("Output or manifest already exists; choose a new output path")

    # Sample record positions without replacement and preserve the selected order.
    indices = random.Random(SEED).sample(range(len(records)), args.count)
    sample = [records[index] for index in indices]
    manifest = {
        "input_file": str(args.input),
        "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
        "output_file": str(args.output),
        "input_records": input_count,
        "eligible_records": len(records),
        "filter": "Both Gemini and Sol label keep" if args.agreed_keep else None,
        "model_sources": model_sources,
        "sample_size": args.count,
        "random_seed": SEED,
        "sampling_method": "random.Random(66).sample without replacement; input file order",
        "selected_eligible_positions": [index + 1 for index in indices],
        "selected_ids": [
            {key: record[key] for key in ("qa_id", "arxiv_id") if key in record}
            for record in sample
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Use exclusive creation to avoid overwriting files; preserve original record fields.
    with args.output.open("x", encoding="utf-8") as file:
        for record in sample:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
    with manifest_path.open("x", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)
        file.write("\n")

    print(f"Sampled {args.count} of {len(records)} eligible records using seed {SEED}")
    print(f"Sample file: {args.output}")
    print(f"Manifest file: {manifest_path}")


if __name__ == "__main__":
    main()
