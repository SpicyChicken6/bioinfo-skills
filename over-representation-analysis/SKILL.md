---
name: over-representation-analysis
description: Run pathway over-representation analysis (ORA) on unranked gene lists using GSEApy and MSigDB, with experimental backgrounds and single-list or up/down contrast reports.
---

# Over-representation analysis

Use [scripts/run_ora.py](scripts/run_ora.py) to retrieve MSigDB gene sets, run offline ORA, and produce tables, summaries, and plots. Dependencies: `gseapy`, `pandas`, and `matplotlib`, installed through the project's environment manager.

## Analysis rules

- Use ORA for unranked foreground lists; use preranked GSEA for rank-aware analysis.
- Establish species, identifiers, and the experimental universe. Prefer all genes eligible for selection in the assay or statistical test. Without a background, the helper uses each category's gene-set union; disclose this limitation.
- Match identifier type and case across foreground, background, and gene sets. The helper deduplicates, uppercases human symbols, and preserves mouse case; it does not convert Ensembl/Entrez IDs to symbols.
- Defaults are human Hallmark (`h.all`) and the latest available species-specific MSigDB release; mouse uses `mh.all`. Record the resolved version and confirm category availability.
- Supply `--genes` for one list, or `--up-genes`/`--down-genes` for directional lists. See the [helper reference](references/gseapy-msigdb-ora.md) for inputs, plotting behavior, and API details.

## Reporting

Inspect `summary.json`, `ora_results.tsv`, and `ora_significant.tsv`. Report species, MSigDB version/categories, foreground sizes, background definition, FDR cutoff, and leading terms with overlap genes.

Base significance claims on adjusted p-values. The helper adjusts within each category and direction; apply global correction separately if required. Directional plots default to raw p-values and may show nonsignificant terms. Enrichment is association, not evidence of causation or pathway activation; consider overlapping gene sets, sample composition, and background choice when interpreting results.
