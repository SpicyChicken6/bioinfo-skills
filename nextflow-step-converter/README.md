# Nextflow Step Converter Skill

A lightweight Claude Code / Codex skill for converting existing analysis scripts and manually described analysis steps into clean, resumable, trackable Nextflow DSL2 workflow components.

This skill is intentionally narrow. It should **package existing analysis logic**, not redesign the analysis.

## Main use case

Use this skill when you already have scripts, commands, notebooks, or a manually documented workflow and want to convert them into:

- Nextflow DSL2 processes
- reusable module files
- a small `main.nf`
- `nextflow.config`
- step manifests
- stub runs for quick workflow testing
- trace/report/timeline-friendly output structure

## Basic usage

```text
Use the nextflow-step-converter skill.

Convert these existing analysis steps into a minimal Nextflow DSL2 workflow. Do not change the statistical method or analysis logic. One process per logical step. Use explicit inputs and outputs. Add a step manifest and a simple nextflow.config.

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

## Recommended run command

```bash
nextflow run main.nf -resume -with-report -with-trace -with-timeline
```

## Design principle

Agent writes or wraps code. Nextflow tracks execution. Interpretation skills summarize real outputs.
