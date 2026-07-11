# Example Prompt

Use the grill-me skill to stress-test this plan before implementation. Prioritize scientific and computational correctness over convenience. Ask one high-impact question at a time, and explain the rationale for your recommendations.

Plan:

```text
Build a resumable Nextflow pipeline for a human bulk RNA-seq study. It will take a count
matrix and sample metadata, run a DESeq2 patient-versus-control analysis, split significant
genes into up- and down-regulated lists, and run Hallmark and Reactome over-representation
analysis with GSEApy. Use package defaults where possible and produce result tables and plots
for a biological interpretation report.
```

Inspect relevant code, configuration, and metadata if available. Look up discoverable facts instead of asking me. Challenge any method, statistical test, hypothesis universe, threshold, or package parameter whose choice could materially change the result. Stop when the major correctness risks are resolved, then summarize decisions, assumptions, consequential parameters, open risks, and validation steps.
