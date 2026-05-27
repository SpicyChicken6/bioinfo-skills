# Example prompt

Use the nextflow-step-converter skill.

Convert my existing analysis scripts into a minimal, readable Nextflow DSL2 workflow.

Requirements:

- Do not change the statistical method or analysis logic.
- Use one process per logical analysis step.
- Make all inputs and outputs explicit.
- Use relative paths.
- Put final outputs under `results/`.
- Add a step manifest.
- Add brief run instructions.
- Include recommendations for containers or conda environments if obvious.

Existing scripts:

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

Recommended run style:

`nextflow run main.nf -resume -with-report -with-trace -with-timeline`
