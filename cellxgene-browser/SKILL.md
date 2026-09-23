---
name: cellxgene-browser
description: Set up, launch, and troubleshoot CELLxGENE Annotate for a user's single-cell H5AD, locally or on a remote host over SSH. Use for browsing their own data; public CELLxGENE Discover searches are outside this skill.
---

# CELLxGENE Browser

Launch a working browser for the requested dataset and return the URL and restart
command. Use CELLxGENE Annotate's `cellxgene` package.

## Check the input

- Establish the dataset path and execution host from context; ask only if missing
  or ambiguous. Keep remote data on its host unless a transfer is requested.
- Inspect H5AD metadata with AnnData in read-only backed mode before loading a
  large matrix. Check nonempty cells/genes, unique cell/gene identifiers and
  metadata column names, and an `X_`-prefixed embedding in `obsm`, e.g. `X_umap`:
  a dense numeric NumPy array with one row per cell and at least two columns. Embeddings
  must have no infinities and cannot be entirely NaN; partial NaNs are allowed.
- Confirm `adata.X` contains the expression values intended for display. Inspect
  `layers` and `raw` if relevant; do not silently substitute scaled values,
  normalize counts, or compute a new embedding. Preserve sparse storage.
- Export Seurat objects or repair incompatible inputs into a separate `.h5ad`;
  preserve the original and describe any changed expression, identifiers, or
  metadata. If required preprocessing is undecided, resolve it before conversion.

## Install and launch

Reuse a working dedicated environment or create one on the execution host.
Check current package compatibility; Python 3.11 is a practical starting point
for CELLxGENE 1.3.0. These examples use a macOS/Linux shell:

```bash
python3.11 -m venv .venv-cellxgene
.venv-cellxgene/bin/python -m pip install cellxgene
.venv-cellxgene/bin/cellxgene launch --help
.venv-cellxgene/bin/cellxgene launch /absolute/path/data.h5ad \
  --host 127.0.0.1 --port 5005 --disable-annotations --disable-gene-sets-save
```

Replace paths and choose a free port. Default to viewing only. If the user wants
editable cell labels, replace `--disable-annotations` with `--annotations-file`
and a writable, dataset-specific CSV path; existing CSVs are edited in place, so
copy them first. Remove `--disable-gene-sets-save` if gene-set saving is wanted.
Record the installed package version.

For local use, open `http://127.0.0.1:5005` after startup succeeds (`--open` is
optional). For SSH use, run the server on the remote host and this tunnel on the
user's computer, substituting the actual SSH host and ports:

```bash
ssh -N -L 127.0.0.1:5005:127.0.0.1:5005 user@remote-host
```

Open the same local URL. Keep the server on loopback; shared/public hosting needs
an explicit deployment request and access controls. Use the available process
manager or a terminal session to keep the server alive, and record how to stop it.

## Verify and troubleshoot

- Check startup logs and an HTTP response. When browser access is available,
  verify the embedding, cell metadata, and expression for a known gene; distinguish
  browser verification from an HTTP-only check.
- For memory pressure, consider `--backed --disable-diffexp` and an explicit
  `--X-approximate-distribution count` or `normal` based on the expression values.
  The default `auto` mode is incompatible with backed access and can load the
  matrix into memory. Backed access is slower and still needs metadata/embedding
  memory. Avoid densifying a large matrix.
- Diagnose input errors from the log and the installed version's `launch --help`.
  Keep compatibility fixes in the dedicated environment; do not upgrade unrelated
  analysis environments. Do not treat the public Discover submission schema as a
  requirement for local viewing.
- Return the dataset, environment/version, URL, launch/tunnel commands, process
  or session identifier, stop command, and any verification limits concisely.

Consult the [upstream guide](https://github.com/chanzuckerberg/cellxgene#getting-started)
for installation, data preparation, and usage details when needed.
