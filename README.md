# bioinfo-skills

Lightweight, portable skills for bioinformatics and scientific data-analysis workflows.

These skills are designed to be small, focused, and usable by both Claude Code and Codex through `SKILL.md`-style instruction modules.

## Included skills

### `consensus-mcp`

A compact Claude Code / Codex skill for installing, verifying, repairing, and using the official Consensus MCP server for peer-reviewed literature search.

It focuses on:

- Claude Code, Claude Desktop, and Codex setup
- OAuth repair for expired tokens and failed reconnects
- correct use of the required `/mcp` endpoint
- practical search constraints for evidence-focused paper search
- avoiding accidental token/API-key exposure

### `over-representation-analysis`

A compact Claude Code / Codex skill for running pathway over-representation analysis (ORA) on unranked foreground gene lists with GSEApy and MSigDB gene sets.

It focuses on:

- retrieving MSigDB GMT collections through GSEApy
- running offline ORA with optional experiment-specific backgrounds
- supporting single foreground lists and paired up/down contrast lists
- writing TSV/CSV/JSON enrichment outputs
- generating paired up/down pathway plots with threshold guide lines
- producing 300 DPI PNG plots and vector PDF companions

The skill is intentionally focused on ORA. If the input is a ranked statistic, use preranked GSEA instead.

### `biofolder`

Initialize and maintain bioinformatics projects with modality modules, task-local
`agent/` and `manual/` workspaces, shared task READMEs, and scoped data directories.
Persistent project rules cover Pixi, Git session checkpoints, and workflow docs.
New projects start with a Python/R data-science environment and a Research Flow
plan at `docs/workflow.yaml`.

See the [skill](biofolder/SKILL.md), [full example tree](biofolder/references/project-layout.md),
[project rules](biofolder/assets/AGENTS.md), and [starter packages](biofolder/references/pixi-environment.md).

### `research-flow`

Read Research Flow YAML plans to understand task dependencies, branch grouping,
recorded progress, and input/output references. Provides context for requested
work without automatically executing tasks or editing the plan.

Use it alongside `biofolder` to read a project's `docs/workflow.yaml`. Includes
the [skill](research-flow/SKILL.md) and [YAML reference](research-flow/references/yaml-contract.md).
For the visual editor, see the [Research Flow installation guide](https://github.com/SpicyChicken6/research-flow/blob/main/docs/install.md)
and [release downloads](https://github.com/SpicyChicken6/research-flow/releases).

### `semantic-scholar-literature-search`

A compact Claude Code / Codex skill for running structured literature searches with the Semantic Scholar API.

It focuses on:

- translating research questions into API query plans
- using Semantic Scholar paper bulk search for broad discovery
- enriching selected papers with paper details or batch lookup
- using positive and negative seed papers for recommendations
- exporting JSONL, CSV, and Markdown paper tables
- summarizing literature themes, gaps, and follow-up searches

The skill is intentionally an API-assisted search and triage layer. It does not claim full-text review unless full text is separately retrieved and read.

## Basic usage

### Initialize a multimodal research project

```text
Use the biofolder skill to initialize this project.

We have bulk RNA-seq, proteomics, and clinical metadata. Our goal is to identify disease-associated pathways across modalities.

Inspect the existing files, ask for missing information, and initialize the project using biofolder defaults. Reference existing datasets in place and verify the environment without running the analyses.
```

### Understand a research plan

```text
Use the research-flow skill to read docs/workflow.yaml and explain which tasks the multimodal integration depends on.
```

### Run pathway ORA with GSEApy

```text
Use the over-representation-analysis skill.

Run ORA for a patient-vs-control differential expression contrast.

Inputs:
- up-regulated genes in patient: results/de/patient_up.txt
- down-regulated genes in patient: results/de/patient_down.txt
- background/tested genes: results/de/tested_genes.txt

Use human MSigDB Hallmark and Reactome gene sets. Retrieve GMT files through GSEApy. Generate paired up/down pathway plots with Control on the left and Patient on the right. Save tables, summaries, PNG plots, and PDF companions under results/ora_patient_vs_control.
```

### Search literature with Semantic Scholar

```text
Use the semantic-scholar-literature-search skill.

Search Semantic Scholar for papers about digenic disease prediction using knowledge graphs and protein language model embeddings.

Requirements:
- prioritize papers from 2020 onward
- include review papers and method papers
- export a Markdown table with title, year, venue, citation count, URL, abstract summary, and why it is relevant
- suggest 5 seed papers for follow-up recommendations
```

### Set up or repair Consensus MCP

```text
Use the consensus-mcp skill. Verify my Consensus MCP setup, repair OAuth if needed, then use Consensus to search for recent peer-reviewed human studies and systematic reviews on exercise for depression.
```
