# Literature Search Plan

## Research Question

State the research question or topic.

## Concepts and Synonyms

| Concept | Synonyms or related terms |
|---|---|
| Main topic | |
| Method | |
| Disease or biological context | |
| Data type | |

## Query Set

| Query | Purpose | Filters |
|---|---|---|
| example query | broad discovery | year range, field, publication type |

## Inclusion Criteria

- Include papers that directly match the topic.
- Include method, benchmark, review, or application papers as requested.
- Include recent papers if the user asks for current literature.

## Exclusion Criteria

- Exclude papers that match terms but are off-topic.
- Exclude papers without enough metadata if they cannot be evaluated.

## API Plan

1. Run paper bulk search for each query.
2. Save raw JSONL results.
3. Convert raw results to CSV.
4. Deduplicate by paperId or DOI.
5. Rank papers by relevance, year, citations, and topic fit.
6. Select seed papers.
7. Run recommendations from selected positive and negative seed papers if useful.
8. Write literature summary.

## Requested Fields

Use only the fields needed for the task.
