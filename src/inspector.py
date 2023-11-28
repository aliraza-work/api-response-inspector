#!/usr/bin/env python3
"""Inspect API response payloads against an expected field schema."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def inspect_payload(payload: dict[str, Any], required: list[str]) -> dict[str, Any]:
    missing = [field for field in required if field not in payload]
    unexpected = [key for key in payload.keys() if key not in required and not key.startswith("_")]
    empty = [field for field in required if field in payload and str(payload[field]).strip() == ""]
    return {
        "ok": not missing and not empty,
        "missing_fields": missing,
        "empty_fields": empty,
        "extra_fields": unexpected,
    }

def inspect_file(path: Path, required: list[str]) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else [data]
    rows = []
    for index, item in enumerate(items):
        result = inspect_payload(item, required)
        rows.append({"index": index, **result})
    return {
        "checked": len(rows),
        "passed": sum(1 for r in rows if r["ok"]),
        "failed": sum(1 for r in rows if not r["ok"]),
        "rows": rows,
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--required", nargs="+", required=True)
    parser.add_argument("--out", default="samples/inspect_report.json")
    args = parser.parse_args()
    report = inspect_file(Path(args.input), args.required)
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "failed": report["failed"]}))

if __name__ == "__main__":
    main()
