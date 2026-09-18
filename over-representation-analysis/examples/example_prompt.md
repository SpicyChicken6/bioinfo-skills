Use over-representation-analysis for a human patient-vs-control contrast:

- Patient-up genes: `results/de/patient_up.txt`
- Patient-down genes: `results/de/patient_down.txt`
- Tested background: `results/de/tested_genes.txt`

Use MSigDB Hallmark and Reactome. Save tables, summaries, and paired PNG/PDF plots to `results/ora_patient_vs_control`, with Control on the left and Patient on the right. Report the database version, background, FDR cutoff, top terms, and overlap genes.
