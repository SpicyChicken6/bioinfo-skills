# Helper and API reference

## Inputs

Run `scripts/run_ora.py` through the project environment. Paths below assume the skill directory as the working directory; adapt them to the project.

```bash
python scripts/run_ora.py \
  --up-genes patient_up.txt --down-genes patient_down.txt \
  --background tested_genes.txt --species human \
  --category h.all --category c2.cp.reactome \
  --contrast-label patient_vs_control \
  --negative-label Control --positive-label Patient \
  --outdir ora_patient_vs_control
```

- Use `--genes` instead for a single foreground; do not combine it with directional inputs. One direction alone is also supported. Each foreground needs at least two unique genes.
- Inputs accept TXT, CSV, or TSV. Tables default to their first column and a header; select a name or zero-based index with `--gene-column`/`--background-column`, and use `--no-header` when needed. Directional column overrides are `--up-gene-column` and `--down-gene-column`.
- `--background` accepts a file, integer universe size, or BioMart dataset. Verify file paths: a nonexistent path is interpreted as a dataset name. Integer backgrounds assume pathway membership in that universe; BioMart annotations may not match the assay.
- `--case` overrides symbol casing. `--dbver` pins a release; `--list-dbver` and `--list-categories` discover available metadata. Categories can be repeated or comma-separated. Human examples: `h.all`, `c2.cp.reactome`, `c5.go.bp`; mouse Hallmark: `mh.all`. Availability varies by release.

## Outputs and plots

- `ora_results.tsv`/`.csv`: combined results; `ora_significant.tsv`: adjusted p-values at or below `--cutoff` (default 0.05).
- `summary.json`: resolved settings, counts, top terms, and output paths.
- Single-list plots: `top_terms.png`/`.pdf`, ranked by adjusted p-value. They show significant terms when available, otherwise the best nonsignificant terms.
- Directional plots: `ora_<contrast>_<combined|up|down>_<category>_top.png`/`.pdf`. Combined plots require results in both directions; up is positive/right (coral), down negative/left (cyan).

Plots default to 300 DPI PNG plus vector PDF. `--top` controls term count (20 by default, per direction for contrasts); `--no-plot` and `--no-pdf` suppress outputs. Directional plots rank by raw p-value unless `--plot-column "Adjusted P-value"` is supplied. `--plot-threshold` marks a guide (default 0.05), not a significance filter. Plots retain threshold guides and readable labels without gridlines; paired plots also retain the central zero line and directional arrows.

## GSEApy API

For custom code, retrieve a GMT dictionary with `Msigdb().get_gmt(category=..., dbver=...)`, then call `gseapy.enrich(gene_list=..., gene_sets=gmt, background=..., outdir=None, no_plot=True)` and read `.results`. `Msigdb().list_dbver()` and `.list_category(dbver=...)` provide metadata.

With `background=None`, each ORA call uses its GMT gene union. Reserve `gseapy.enrichr` for Enrichr web-service libraries/scoring. MSigDB retrieval requires network access; enrichment against the retrieved dictionary runs locally.

Sources: [GSEApy examples](https://gseapy.readthedocs.io/en/latest/gseapy_example.html), [API](https://gseapy.readthedocs.io/en/latest/run.html), [citation](https://gseapy.readthedocs.io/en/master/index.html).
