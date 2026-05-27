# Semantic Scholar Literature Search Skill

A lightweight Claude Code / Codex skill for planning and running literature searches through the Semantic Scholar API, then producing structured paper tables, seed-paper recommendations, and concise literature summaries.

This skill focuses on API-assisted search and triage. It is not a full systematic-review framework.

## What it does

- Turns a research question into Semantic Scholar search queries.
- Uses paper bulk search for broad literature discovery.
- Uses paper details for richer metadata on selected papers.
- Uses recommendations from positive and negative seed papers.
- Uses author batch lookup when author context matters.
- Exports results as JSONL, CSV, Markdown tables, or BibTeX-like citation notes.
- Produces a concise literature search summary with inclusion/exclusion notes.

## API sources

The skill is based on the official Semantic Scholar API tutorial and documentation patterns:

- Academic Graph API base URL: `https://api.semanticscholar.org/graph/v1`
- Recommendations API base URL: `https://api.semanticscholar.org/recommendations/v1`
- Datasets API base URL: `https://api.semanticscholar.org/datasets/v1`

## Recommended environment variable

Store your API key outside code:

```bash
export S2_API_KEY='your_api_key_here'
```

The API key is optional for some endpoints, but recommended for reliability and rate limiting.

## Basic usage

```text
Use the semantic-scholar-literature-search skill.

Search Semantic Scholar for papers about digenic disease prediction using knowledge graphs and protein language model embeddings.

Requirements:
- prioritize papers from 2020 onward
- include review papers and method papers
- export a Markdown table with title, year, venue, citation count, URL, abstract summary, and why it is relevant
- suggest 5 seed papers for follow-up recommendations
```

## Typical outputs

- `literature_search_plan.md`
- `semantic_scholar_results.jsonl`
- `semantic_scholar_results.csv`
- `literature_summary.md`
- `seed_papers_for_recommendations.md`
