---
name: bio-results-interpreter
description: Quickly interpret existing bioinformatics, genomics, transcriptomics, single-cell, epigenomics, proteomics, or general data-analysis results. Use when the user provides research background, result files, figures, tables, plots, logs, or asks for conclusions, hypotheses, interpretation, caveats, or a concise report. Do not run new analyses unless explicitly requested.
---

# Bio Results Interpreter

## Purpose

Create a fast, precise, evidence-grounded interpretation report from existing research background and analysis results.

This skill is for interpretation and reporting, not for performing new analyses.

The core workflow is:

**Research question + background → analysis modules → figures/tables/results → observations → interpretation → plausible conclusions/hypotheses → caveats/next steps**

## When to use this skill

Use this skill when the user asks to:

- summarize existing analysis results
- interpret bioinformatics or data-analysis outputs
- make plausible biological conclusions
- generate hypotheses from results
- write a Markdown or HTML result report
- organize result figures/tables under analysis modules
- connect research background to results
- prepare discussion points for a manuscript, presentation, or lab update

## When not to use this skill

Do not use this skill when the user primarily wants:

- a new analysis pipeline
- code debugging
- running DESeq2, Seurat, Scanpy, CellChat, CellRank, GSEA, etc.
- generic literature review without user-provided results
- unsupported speculation without evidence

If new analysis seems necessary, ask before doing it unless the user explicitly requested it.

## Required inputs to look for

Inspect available files and user-provided text for:

- research question
- project background
- sample design and comparison groups
- analysis module names
- result tables
- figure files
- figure legends
- statistical summaries
- pathway/enrichment outputs
- marker gene tables
- differential expression tables
- QC summaries
- notes, draft text, or README files

If key context is missing, still produce a useful draft, but clearly label missing information.

## Analysis module detection

Group results by analysis module. Infer module names from folder names, filenames, figure titles, table names, or user text.

Common module examples:

- QC and sample overview
- Differential expression
- Pathway or gene-set enrichment
- Cell-type annotation
- Cell composition
- Marker gene analysis
- Pseudobulk analysis
- Trajectory or RNA velocity
- Cell-cell communication
- Epigenomic peak analysis
- Motif or TF analysis
- Variant prioritization
- Phenotype/HPO analysis
- Survival or clinical association
- Model performance evaluation

Do not force every result into these categories. Use the user's actual project structure when possible.

## Output formats

Default output: Markdown.

If the user asks for HTML, produce a single standalone HTML file or HTML text with embedded relative links to figures and tables.

For Markdown reports, use relative paths for figures and tables whenever possible:

```markdown
![Short figure caption](figures/example.png)
```

For tables, either embed small tables directly or link large files:

```markdown
[Full differential expression table](tables/de_results.csv)
```

## Required report structure

Use this structure unless the user requests a different format:

```markdown
# Results Interpretation Report

## 1. Research Question

## 2. Background

## 3. Data and Analysis Modules

## 4. Key Findings

## 5. Results by Analysis Module

### Module 1: <module name>

#### Inputs reviewed

#### Figures and tables

#### Direct observations

#### Interpretation

#### Plausible conclusions or hypotheses

#### Caveats

### Module 2: <module name>

...

## 6. Cross-Module Synthesis

## 7. Claim Strength Table

## 8. Possible Conclusions

## 9. Hypotheses to Test Next

## 10. Limitations

## 11. Recommended Next Steps

## 12. Missing Information
```

## Claim discipline

Every important claim must be classified as one of:

1. **Directly supported result** — explicitly shown in the provided result, table, figure, or statistic.
2. **Reasonable interpretation** — likely interpretation based on direct results and standard domain knowledge.
3. **Plausible hypothesis** — biologically or analytically plausible, but requires validation.
4. **Speculative idea** — interesting but weakly supported.
5. **Unsupported / do not claim** — should not be presented as a conclusion.

Use cautious scientific language when evidence is indirect.

Preferred phrases:

- “These results suggest...”
- “This is consistent with...”
- “One plausible interpretation is...”
- “This raises the possibility that...”
- “A testable hypothesis is...”

Avoid unless strongly supported:

- “proves”
- “demonstrates causality”
- “is driven by”
- “confirms the mechanism”
- “establishes that”

## Required claim strength table

Always include this table:

| Claim | Evidence Source | Claim Type | Confidence | Safer Wording | Needed Validation |
|---|---|---|---|---|---|
| ... | Figure/Table/File | Direct result / Interpretation / Hypothesis / Speculation | High/Medium/Low | ... | ... |

## Bioinformatics-specific caution rules

Apply these rules when relevant:

- Do not claim causality from observational omics data alone.
- Do not claim pathway activation from enrichment alone unless directionality and gene-level evidence support it.
- Do not treat statistical significance as biological importance without effect size/context.
- Distinguish cell-composition changes from cell-intrinsic expression changes.
- For single-cell results, consider batch effects, doublets, ambient RNA, annotation uncertainty, sample imbalance, and pseudoreplication.
- For differential expression, consider sample size, covariates, design formula, multiple testing, effect size, and directionality.
- For enrichment results, name the gene sets and direction when available.
- For variant interpretation, distinguish candidate association from diagnostic or causal evidence.
- For model results, distinguish training performance, validation performance, external generalization, and biological interpretability.

## Fast interpretation mode

If the user asks for a quick interpretation, produce:

```markdown
## Research Question

## Background

## Results Reviewed

## Main Observations

## Interpretation

## Plausible Conclusions

## Caveats

## Next Checks
```

Keep it concise but evidence-grounded.

## Precision rules

- Never invent numbers, p-values, genes, pathways, phenotypes, sample sizes, methods, or file names.
- If a result is not visible, say so.
- If a figure/table is referenced but not available, list it under Missing Information.
- If the user provides a background hypothesis, evaluate whether the results support, weaken, or only partially support it.
- Keep conclusions proportional to the evidence.
- Separate what the data show from what they might mean.

## Style

Use clear scientific prose. Be concise, structured, and useful.
