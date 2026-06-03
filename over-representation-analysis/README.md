# Over Representation Analysis Skill

A lightweight Claude Code / Codex skill for running pathway over-representation analysis (ORA) on unranked foreground gene lists using GSEApy and MSigDB gene sets.

It focuses on:

- retrieving MSigDB GMT collections through GSEApy
- running offline ORA with optional experiment-specific backgrounds
- handling single foreground lists or paired up/down contrast lists
- writing reproducible TSV/CSV/JSON result files
- generating compact pathway plots with up/down directions, threshold guides, and PDF companions
- keeping identifier and background caveats visible

## Install for Claude Code

Copy this folder into your Claude skills directory or project-level skills folder, depending on your setup.

The important file is:

```text
over-representation-analysis/SKILL.md
```

The bundled helper script is:

```text
over-representation-analysis/scripts/run_ora.py
```

## Install for Codex

Copy this folder into your Codex skills directory or project-level skills folder.

Codex should detect the same `SKILL.md` file.

## Dependencies

Install the runtime dependencies in the analysis environment:

```bash
python -m pip install gseapy pandas matplotlib
```

## Basic usage

```text
Use the over-representation-analysis skill.

Run ORA for these differential-expression foreground lists:
- up genes: results/de/patient_up.txt
- down genes: results/de/patient_down.txt
- background genes: results/de/tested_genes.txt

Use human MSigDB Hallmark and Reactome gene sets. Generate paired up/down pathway plots with Control on the left and Patient on the right. Save results to results/ora_patient_vs_control.
```

Equivalent direct helper command:

```bash
python over-representation-analysis/scripts/run_ora.py \
  --up-genes results/de/patient_up.txt \
  --down-genes results/de/patient_down.txt \
  --background results/de/tested_genes.txt \
  --species human \
  --category h.all \
  --category c2.cp.reactome \
  --contrast-label patient_vs_control \
  --negative-label Control \
  --positive-label Patient \
  --outdir results/ora_patient_vs_control
```

## Typical outputs

- `ora_results.tsv` and `ora_results.csv`
- `ora_significant.tsv`
- `summary.json`
- `top_terms.png` and `top_terms.pdf`
- paired pathway plots such as `ora_patient_vs_control_combined_h.all_top.png` and `.pdf`

## Notes

Use an experimental background whenever possible, such as all expressed genes, detected genes, or genes tested for differential expression. If no background is supplied, GSEApy uses the union of genes in the selected gene sets, which should be described as a limitation.

The helper defaults to 300 DPI PNG output and writes vector PDF companion plots unless `--no-pdf` is supplied.
