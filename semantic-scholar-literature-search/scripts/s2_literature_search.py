#!/usr/bin/env python3
"""Lightweight Semantic Scholar literature search helper.

Examples:
  python scripts/s2_literature_search.py search \
    --query '"digenic disease" prediction' \
    --year '2020-' \
    --limit 100 \
    --out literature/semantic_scholar_results.jsonl

  python scripts/s2_literature_search.py recommend \
    --positive 02138d6d094d1e7511c157f0b1a3dd4e5b20ebee \
    --negative 0045ad0c1e14a4d1f4b011c92eb36b8df63d65bc \
    --limit 50 \
    --out literature/recommendation_results.jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterable

import requests

GRAPH_BASE = "https://api.semanticscholar.org/graph/v1"
REC_BASE = "https://api.semanticscholar.org/recommendations/v1"
DEFAULT_FIELDS = (
    "paperId,title,abstract,year,publicationDate,venue,publicationTypes,url,"
    "citationCount,influentialCitationCount,authors,externalIds,openAccessPdf,"
    "fieldsOfStudy,s2FieldsOfStudy"
)


def get_headers() -> dict[str, str]:
    api_key = os.environ.get("S2_API_KEY")
    return {"x-api-key": api_key} if api_key else {}


def request_with_backoff(method: str, url: str, *, max_retries: int = 5, **kwargs: Any) -> dict[str, Any]:
    for attempt in range(max_retries):
        response = requests.request(method, url, timeout=60, **kwargs)
        if response.status_code == 429:
            sleep_seconds = min(60, 2 ** attempt)
            time.sleep(sleep_seconds)
            continue
        if response.status_code >= 400:
            raise RuntimeError(f"Semantic Scholar request failed: {response.status_code} {response.text[:500]}")
        return response.json()
    raise RuntimeError("Semantic Scholar request failed after repeated rate-limit retries")


def write_jsonl(records: Iterable[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def flatten_authors(paper: dict[str, Any]) -> str:
    authors = paper.get("authors") or []
    return "; ".join(a.get("name", "") for a in authors if isinstance(a, dict))


def jsonl_to_csv(jsonl_path: Path, csv_path: Path) -> None:
    rows = []
    with jsonl_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            paper = json.loads(line)
            rows.append(
                {
                    "paperId": paper.get("paperId", ""),
                    "title": paper.get("title", ""),
                    "year": paper.get("year", ""),
                    "publicationDate": paper.get("publicationDate", ""),
                    "venue": paper.get("venue", ""),
                    "citationCount": paper.get("citationCount", ""),
                    "influentialCitationCount": paper.get("influentialCitationCount", ""),
                    "url": paper.get("url", ""),
                    "authors": flatten_authors(paper),
                    "abstract": paper.get("abstract", ""),
                }
            )
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else ["paperId"])
        writer.writeheader()
        writer.writerows(rows)


def search(args: argparse.Namespace) -> None:
    url = f"{GRAPH_BASE}/paper/search/bulk"
    params: dict[str, Any] = {
        "query": args.query,
        "fields": args.fields,
    }
    if args.year:
        params["year"] = args.year
    if args.publication_date_or_year:
        params["publicationDateOrYear"] = args.publication_date_or_year
    if args.publication_types:
        params["publicationTypes"] = args.publication_types
    if args.fields_of_study:
        params["fieldsOfStudy"] = args.fields_of_study
    if args.min_citation_count is not None:
        params["minCitationCount"] = args.min_citation_count
    if args.sort:
        params["sort"] = args.sort

    headers = get_headers()
    records: list[dict[str, Any]] = []
    response = request_with_backoff("GET", url, params=params, headers=headers)

    while True:
        records.extend(response.get("data", []))
        if len(records) >= args.limit:
            records = records[: args.limit]
            break
        token = response.get("token")
        if not token:
            break
        params["token"] = token
        response = request_with_backoff("GET", url, params=params, headers=headers)

    out = Path(args.out)
    write_jsonl(records, out)
    if args.csv:
        jsonl_to_csv(out, Path(args.csv))
    print(f"Wrote {len(records)} papers to {out}")


def recommend(args: argparse.Namespace) -> None:
    url = f"{REC_BASE}/papers"
    params = {"fields": args.fields, "limit": args.limit}
    data = {
        "positivePaperIds": args.positive,
        "negativePaperIds": args.negative or [],
    }
    response = request_with_backoff("POST", url, params=params, json=data, headers=get_headers())
    papers = response.get("recommendedPapers", [])
    if args.sort_by_citations:
        papers.sort(key=lambda paper: paper.get("citationCount") or 0, reverse=True)
    out = Path(args.out)
    write_jsonl(papers, out)
    if args.csv:
        jsonl_to_csv(out, Path(args.csv))
    print(f"Wrote {len(papers)} recommended papers to {out}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Semantic Scholar literature search helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Run paper bulk search")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--year", default=None, help="Year range, e.g. 2020-")
    search_parser.add_argument("--publication-date-or-year", default=None)
    search_parser.add_argument("--publication-types", default=None)
    search_parser.add_argument("--fields-of-study", default=None)
    search_parser.add_argument("--min-citation-count", type=int, default=None)
    search_parser.add_argument("--sort", default=None)
    search_parser.add_argument("--fields", default=DEFAULT_FIELDS)
    search_parser.add_argument("--limit", type=int, default=100)
    search_parser.add_argument("--out", default="literature/semantic_scholar_results.jsonl")
    search_parser.add_argument("--csv", default=None)
    search_parser.set_defaults(func=search)

    rec_parser = subparsers.add_parser("recommend", help="Recommend papers from seed paper IDs")
    rec_parser.add_argument("--positive", nargs="+", required=True)
    rec_parser.add_argument("--negative", nargs="*", default=[])
    rec_parser.add_argument("--fields", default=DEFAULT_FIELDS)
    rec_parser.add_argument("--limit", type=int, default=100)
    rec_parser.add_argument("--out", default="literature/recommendation_results.jsonl")
    rec_parser.add_argument("--csv", default=None)
    rec_parser.add_argument("--sort-by-citations", action="store_true")
    rec_parser.set_defaults(func=recommend)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
