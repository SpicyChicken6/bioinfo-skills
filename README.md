# bioinfo-skills

Lightweight, portable skills for bioinformatics and scientific data-analysis workflows.

These skills are designed to be small, focused, and usable by both Claude Code and Codex through `SKILL.md`-style instruction modules.

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

### `nextflow-step-converter`

A compact Claude Code / Codex skill for converting existing scripts, commands, notebooks, or manually described analysis steps into clean Nextflow DSL2 workflow components.

It focuses on:

- preserving existing analysis logic
- making inputs and outputs explicit
- wrapping steps as Nextflow processes
- creating step manifests
- organizing modules under `modules/local/`
- supporting `-resume`
- producing trace/report/timeline-friendly workflows

The skill is intentionally a packaging/conversion layer. It should not redesign statistical methods unless explicitly requested.

### `consensus-mcp`

A compact Claude Code / Codex skill for installing, verifying, repairing, and using the official Consensus MCP server for peer-reviewed literature search.

It focuses on:

- Claude Code, Claude Desktop, and Codex setup
- OAuth repair for expired tokens and failed reconnects
- correct use of the required `/mcp` endpoint
- practical search constraints for evidence-focused paper search
- avoiding accidental token/API-key exposure

## Basic usage

### Interpret existing results

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

### Convert existing steps to Nextflow

```text
Use the nextflow-step-converter skill.

Convert these existing analysis scripts into a minimal Nextflow DSL2 workflow. Do not change the statistical method or analysis logic. One process per logical step. Use explicit inputs and outputs. Add a step manifest and brief run instructions.

Scripts:
- scripts/run_deseq2.R
- scripts/run_gsea.R
- scripts/make_plots.R

Inputs:
- data/count_matrix.tsv
- data/metadata.tsv

Expected outputs:
- results/deseq2/de_results.tsv
- results/enrichment/gsea_results.tsv
- results/figures/pca.png
- results/figures/top_pathways.png
```

Recommended Nextflow run style:

```bash
nextflow run main.nf -resume -with-report -with-trace -with-timeline
```

### Set up or repair Consensus MCP

```text
Use the consensus-mcp skill. Verify my Consensus MCP setup, repair OAuth if needed, then use Consensus to search for recent peer-reviewed human studies and systematic reviews on exercise for depression.
```
