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

### `consensus-mcp`

A compact Claude Code / Codex skill for installing, verifying, repairing, and using the official Consensus MCP server for peer-reviewed literature search.

It focuses on:

- Claude Code, Claude Desktop, and Codex setup
- OAuth repair for expired tokens and failed reconnects
- correct use of the required `/mcp` endpoint
- practical search constraints for evidence-focused paper search
- avoiding accidental token/API-key exposure

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

### `grill-me`

A compact Claude Code / Codex skill for adaptively stress-testing a plan before implementation, with a strong bioinformatics emphasis on scientific and computational correctness.

It focuses on:

- asking the highest-impact unresolved question, one at a time
- treating package defaults as candidates that require justification
- matching statistical tests and models to the study design and assumptions
- checking computational, statistical, and biological correctness separately
- verifying consequential parameter semantics against the installed version or primary documentation
- using appropriate hypothesis universes and selection-bias checks, such as experiment-specific eligible backgrounds for ORA
- tracking dependencies, provenance, silent failure modes, and validation evidence

The skill remains collaborative rather than adversarial and uses review domains as adaptive lenses instead of a fixed checklist.

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

### Grill a plan or design

```text
Use the grill-me skill.

Stress-test my bioinformatics plan before implementation. Prioritize scientific and computational correctness over convenience. Ask the highest-impact unresolved question one at a time. Challenge consequential method, statistical-test, background-universe, threshold, and package-parameter choices instead of accepting defaults. Inspect available project evidence before asking me for facts, and summarize the decisions, rationales, risks, and validation steps when the major uncertainties are resolved.

Plan:
...
```
