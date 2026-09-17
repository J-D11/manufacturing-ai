#!/usr/bin/env python3
"""Emit assessor-free prompts or validate score structure; no semantic scoring."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIMS = {"correctness", "evidence", "scope", "next_step", "clarity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prompt", "check-scores"])
    parser.add_argument("value", help="case ID or score JSON path")
    args = parser.parse_args()
    cases = json.loads((ROOT / "tests/scenarios.json").read_text())["cases"]
    indexed = {case["id"]: case for case in cases}
    if len(indexed) != len(cases):
        raise ValueError("Duplicate case IDs")
    if args.command == "prompt":
        if args.value not in indexed:
            raise ValueError("Unknown case ID; available: " + ", ".join(indexed))
        print(json.dumps({"case_id": args.value, **indexed[args.value]["input"]}, indent=2))
        return
    data = json.loads(Path(args.value).read_text())
    if not isinstance(data, dict):
        raise ValueError("Scores must be a JSON object")
    for field in ("run_id", "skill_fingerprint", "model"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError("Missing nonempty " + field)
    records = data.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("records must be a nonempty list")
    seen = set()
    for row in records:
        if not isinstance(row, dict):
            raise ValueError("Each record must be a JSON object")
        case_id, repeat = row.get("case_id"), row.get("repeat")
        if case_id not in indexed or type(repeat) is not int or repeat < 1:
            raise ValueError("Invalid case_id or repeat")
        key = (case_id, repeat)
        if key in seen:
            raise ValueError("Duplicate case/repeat")
        seen.add(key)
        scores = row.get("scores")
        if not isinstance(scores, dict) or set(scores) != DIMS:
            raise ValueError("Expected exactly five scoring dimensions")
        if any(type(v) is not int or v not in (0, 1, 2) for v in scores.values()):
            raise ValueError("Scores must be integers 0, 1, 2")
        failures = row.get("critical_failures")
        if not isinstance(failures, list) or any(not isinstance(v, str) or not v.strip() for v in failures):
            raise ValueError("critical_failures must be a list of nonempty descriptions")
        for field in ("response_path", "rationale", "assessor"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError("Missing nonempty " + field)
    missing = sorted(set(indexed) - {key[0] for key in seen})
    print(json.dumps({"schema_valid": True, "record_count": len(records), "unrecorded_cases": missing,
                      "note": "Structure only; artifact existence and semantic judgment are not verified."}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        raise SystemExit(str(exc))
