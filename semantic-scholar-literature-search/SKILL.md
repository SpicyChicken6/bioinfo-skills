---
name: semantic-scholar-literature-search
description: Plan and run literature searches using the Semantic Scholar API. Use when the user asks to find papers, build paper tables, discover related papers from seed papers, export metadata, or summarize literature search results. Prefer API-grounded results over free-form web search when Semantic Scholar coverage is appropriate.
---

# Semantic Scholar Literature Search

## Purpose

Use the Semantic Scholar API to perform fast, structured literature discovery and paper triage.

This skill is for API-assisted literature search, not for full systematic review automation or full-text paper reading.

Core workflow:

**Research question → query plan → Semantic Scholar API search → metadata table → paper triage → recommendations → literature summary**

## When to use this skill

Use this skill when the user asks to:

- search for scientific papers
- find recent papers on a research topic
- collect metadata for papers
- rank papers by relevance, year, citation count, or venue
- discover related papers from seed papers
- identify review papers, method papers, benchmark papers, or datasets
- export search results to JSONL, CSV, Markdown, or citation notes
- create a concise literature-search report

## When not to use this skill

Do not use this skill alone when the user needs:

- guaranteed full-text access
- formal systematic review screening with PRISMA-style audit trails
- PubMed/MEDLINE-only clinical literature search
- legal, medical, or regulatory advice
- full article summarization without available abstracts or PDFs

If full text is required, use Semantic Scholar metadata as discovery, then retrieve PDFs through user-approved sources such as open access links, institutional access, Zotero, PubMed Central, journal pages, or user-provided PDFs.

## API basics

Semantic Scholar exposes multiple APIs:

- Academic Graph API base URL: `https://api.semanticscholar.org/graph/v1`
- Recommendations API base URL: `https://api.semanticscholar.org/recommendations/v1`
- Datasets API base URL: `https://api.semanticscholar.org/datasets/v1`

Use an API key when available. Read it from the environment variable `S2_API_KEY`. Do not hard-code API keys.

## Preferred endpoints

### 1. Paper bulk search

Use for broad discovery in most cases.

Endpoint:

```text
GET /paper/search/bulk
```

Useful parameters:

- `query`
- `fields`
- `year`
- `publicationDateOrYear`
- `publicationTypes`
- `fieldsOfStudy`
- `venue`
- `minCitationCount`
- `openAccessPdf`
- `sort`
- `token` for pagination

Recommended fields:

```text
paperId,title,abstract,year,publicationDate,venue,publicationTypes,url,citationCount,influentialCitationCount,authors,externalIds,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy
```

### 2. Paper details

Use when the user provides a known paper ID, DOI, arXiv ID, PMID, or Semantic Scholar paper ID.

Endpoint:

```text
GET /paper/{paper_id}
```

Useful fields:

```text
title,abstract,year,venue,url,citationCount,influentialCitationCount,authors,externalIds,references,citations,openAccessPdf
```

### 3. Paper batch details

Use when enriching many selected paper IDs.

Endpoint:

```text
POST /paper/batch
```

Send paper IDs in the request body and request only the fields needed.

### 4. Recommendations from seed papers

Use after initial triage to find related work.

Endpoint:

```text
POST https://api.semanticscholar.org/recommendations/v1/papers
```

Use:

- `positivePaperIds` for papers that match the topic
- `negativePaperIds` for papers to avoid
- `limit` to control the number of recommended papers
- `fields` to request useful metadata

### 5. Author batch lookup

Use when author context matters.

Endpoint:

```text
POST /author/batch
```

Useful fields:

```text
name,url,paperCount,hIndex,papers
```

## Query planning rules

Before calling the API, make a compact query plan:

1. Identify the research topic.
2. Identify synonyms and related terms.
3. Identify inclusion criteria.
4. Identify exclusion criteria.
5. Decide date range.
6. Decide whether to include reviews, methods, benchmarks, datasets, preprints, or clinical studies.
7. Decide target fields.
8. Decide output format.

For bioinformatics topics, include method synonyms and biological synonyms.

Example:

```text
Topic: digenic disease prediction using knowledge graphs and protein language models
Queries:
- "digenic disease" prediction
- oligogenic disease knowledge graph
- gene pair prioritization rare disease
- protein language model variant prioritization
- knowledge graph rare disease diagnosis
Date range: 2020-
Include: method papers, benchmark papers, review papers
Exclude: unrelated general network biology papers without disease prediction
```

## Ranking rules

Rank papers using a transparent score rather than citation count alone.

Suggested criteria:

- topical relevance
- recency
- method relevance
- data/resource relevance
- citation count
- influential citation count
- venue credibility
- availability of abstract or open access PDF
- whether the paper is a review, method, benchmark, or application paper

Always explain why a paper is included.

## Output files

When working inside a project, prefer these outputs:

```text
literature/
  search_plan.md
  semantic_scholar_results.jsonl
  semantic_scholar_results.csv
  selected_papers.md
  seed_papers_for_recommendations.md
  recommendation_results.jsonl
  literature_summary.md
```

## Required literature summary structure

Use this structure unless the user asks otherwise:

```markdown
# Literature Search Summary

## Research Question

## Search Strategy

## Inclusion and Exclusion Criteria

## Query Set

## Results Overview

## Top Papers

| Title | Year | Venue | Type | Citation Count | URL | Why Relevant |
|---|---:|---|---|---:|---|---|

## Method Themes

## Evidence Gaps

## Seed Papers for Follow-Up Recommendations

## Suggested Next Searches

## Limitations
```

## API request rules

- Use `S2_API_KEY` from the environment when available.
- Do not print the API key.
- Use the `fields` parameter and request only needed fields.
- Prefer bulk or batch endpoints when collecting many papers.
- Handle pagination.
- Respect rate limits.
- Retry 429 responses with backoff.
- Save raw results before summarizing.
- Do not invent metadata.
- If abstracts are missing, say so.
- Do not claim full-text review unless full text was actually retrieved and read.

## Python implementation guidance

If writing helper scripts, use:

- `requests`
- `time.sleep` for rate limiting/backoff
- JSONL for raw results
- CSV for paper tables
- Markdown for summaries

Keep scripts small and transparent.

## Final response style

When finishing a search task, report:

- queries used
- number of records retrieved
- number of records selected
- output files created
- top papers or themes
- caveats about coverage and missing abstracts/full text
- suggested next query refinements
