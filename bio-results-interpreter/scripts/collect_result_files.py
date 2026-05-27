#!/usr/bin/env python3
"""Collect likely result files for a lightweight interpretation report.

Usage:
  python scripts/collect_result_files.py /path/to/project > result_inventory.md
"""

from __future__ import annotations

import sys
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".pdf"}
TABLE_EXTS = {".csv", ".tsv", ".xlsx", ".xls", ".txt"}
REPORT_EXTS = {".md", ".html", ".qmd", ".rmd", ".ipynb"}

SKIP_DIRS = {".git", ".nextflow", "node_modules", "__pycache__", ".venv", "venv"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def classify(path: Path) -> str | None:
    ext = path.suffix.lower()
    name = path.name.lower()
    if ext in IMAGE_EXTS:
        return "Figure"
    if ext in TABLE_EXTS:
        if any(k in name for k in ["result", "de", "marker", "enrich", "gsea", "pathway", "qc", "summary", "stats", "table"]):
            return "Table/Result"
        return "Possible table"
    if ext in REPORT_EXTS:
        return "Report/Notebook"
    return None


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        return 1

    records = []
    for path in sorted(root.rglob("*")):
        if should_skip(path) or not path.is_file():
            continue
        kind = classify(path)
        if kind:
            records.append((kind, path.relative_to(root)))

    print("# Result File Inventory\n")
    print(f"Project root: `{root}`\n")
    print("| Type | Relative Path |")
    print("|---|---|")
    for kind, rel in records:
        print(f"| {kind} | `{rel}` |")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
