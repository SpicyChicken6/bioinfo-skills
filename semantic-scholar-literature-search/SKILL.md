---
name: semantic-scholar-literature-search
description: Search Semantic Scholar, discover related papers from seeds, and export or summarize paper metadata. Use for literature discovery and triage; full-text review and formal systematic reviews need additional sources and methods.
---

# Semantic Scholar Literature Search

Translate the question into a compact query set with relevant biological/method synonyms, date range, and inclusion criteria. Choose retrieval depth and outputs to match the request; use the optional [search plan](report-templates/search_plan_template.md) only when useful.

## Retrieval

Academic Graph base: `https://api.semanticscholar.org/graph/v1`.

| Need | Endpoint | Details |
|---|---|---|
| Relevance-ranked shortlist or seeds | `GET /paper/search` | `offset`/`limit` pagination |
| Broad collection or sorted export | `GET /paper/search/bulk` | `token` pagination; supports `sort` |
| Known paper metadata | `GET /paper/{paper_id}` | Semantic Scholar ID or supported external ID such as `DOI:...`, `ARXIV:...`, `PMID:...` |
| Enrich selected papers | `POST /paper/batch` | Body: `{"ids": [...]}` |
| Author context, when relevant | `POST /author/batch` | Body: `{"ids": [...]}` |

For seed recommendations, use `POST https://api.semanticscholar.org/recommendations/v1/papers`: body fields `positivePaperIds` and optional `negativePaperIds`; query parameters `fields` and `limit`.

Request only needed `fields`; paginate to the requested scope. Use `S2_API_KEY` as the `x-api-key` header when available, without embedding or printing it. Back off on 429 responses and stop after bounded retries; report incomplete retrieval.

## Bundled helper

[scripts/s2_literature_search.py](scripts/s2_literature_search.py) requires Python and `requests`. Run it in the project's environment; use subcommand `--help` for filters and options.

- `relevance` and `search` require `--query`; `search` means **bulk** retrieval. `--limit` caps total records; relevance also supports `--offset` and `--page-size`.
- `recommend` requires one or more `--positive` IDs and accepts `--negative` IDs.
- All modes support `--fields`, `--out` (JSONL), and optional `--csv`. Choose paths within the project's existing layout; each run overwrites its output files.
- The helper handles pagination and up to five attempts on rate limits. Details/batch/author requests require direct API calls.

JSONL contains paper records. CSV columns are `paperId`, `title`, `year`, `publicationDate`, `venue`, `citationCount`, `influentialCitationCount`, `url`, `authors`, and `abstract`; an empty export contains only the `paperId` header.

## Selection and reporting

Save raw results and record queries, filters, endpoint modes, and retrieval date. Deduplicate by `paperId` or DOI before counting selected papers. Rank primarily by topical and methodological relevance, explaining inclusions; citation counts alone are insufficient.

Return the requested table or synthesis, with retrieved/selected counts, linked papers, and material coverage limitations. Distinguish metadata/abstract-based findings from full-text review; mark missing information and never infer full-text findings from metadata. Treat apparent gaps as gaps in the retrieved evidence.

Use the optional [summary template](report-templates/literature_summary_template.md) for longer reports, adapting its sections to the task. See the [example request](examples/example_prompt.md).
