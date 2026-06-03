Use the over-representation-analysis skill.

Run pathway ORA for a patient-vs-control differential expression contrast.

Inputs:
- Up-regulated genes in patient: `results/de/patient_up.txt`
- Down-regulated genes in patient: `results/de/patient_down.txt`
- Background/tested genes: `results/de/tested_genes.txt`

Requirements:
- Use human MSigDB Hallmark (`h.all`) and Reactome (`c2.cp.reactome`) collections.
- Retrieve GMT files through GSEApy's MSigDB helper rather than requiring local GMT files.
- Treat `patient_up.txt` as the right-side/positive direction and `patient_down.txt` as the left-side/negative direction.
- Label the paired plot sides as `Control` and `Patient`.
- Save all ORA tables, summaries, PNG plots, and PDF plot companions under `results/ora_patient_vs_control`.
- Report the MSigDB version, foreground sizes, background definition, adjusted p-value cutoff, top enriched terms, and overlap genes.
