# bioinfo-skills

Lightweight, portable skills for bioinformatics and scientific data-analysis workflows.

## Included skills

### `bio-results-interpreter`

A compact Claude Code / Codex skill for turning existing research background, figures, tables, and result summaries into evidence-grounded Markdown or HTML interpretation reports.

It focuses on:

- research question and background
- analysis-module organization
- embedded figures and linked tables
- direct observations
- cautious biological/statistical interpretation
- plausible conclusions and hypotheses
- caveats, limitations, and validation ideas

The skill is intentionally small and fast. It does **not** run new analyses by default.

## Basic usage

Ask Claude Code or Codex something like:

```text
Use the bio-results-interpreter skill.

Create a concise Markdown interpretation report from this project.

Research question:
...

Background:
...

Results to interpret:
- figures/qc_summary.png
- tables/deseq2_results.csv
- tables/gsea_hallmark.csv
- figures/top_pathways.png

Do not run new analyses. Group results by analysis module. Embed figures and link tables. Separate direct observations from plausible hypotheses.
```
