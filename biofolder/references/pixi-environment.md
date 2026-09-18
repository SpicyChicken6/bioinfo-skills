# Default Python and R environment

New-project initialization includes **installing** a working data-science
environment, unless the user requests a different baseline or a scaffold-only
setup. Use one project-root Pixi workspace with both Python and R in its default
environment. Human and agent work share it. Add named environments within that
workspace only when dependencies genuinely conflict.

## Starter packages

| Purpose | Python packages | R packages (conda names) |
| --- | --- | --- |
| Runtime | `python` | `r-base` |
| Data handling | `numpy`, `pandas` | `r-dplyr`, `r-tidyr`, `r-readr`, `r-data.table` |
| Statistics/modeling | `scipy`, `statsmodels`, `scikit-learn` | Base R `stats` (included with `r-base`) |
| Plotting | `matplotlib`, `seaborn` | `r-ggplot2` |
| Notebooks | `jupyterlab`, `ipykernel` | `r-irkernel` |
| File formats | `pyyaml`, `openpyxl` | `r-readxl`, `r-jsonlite`, `r-yaml` |
| Testing | `pytest` | Base R checks; add further testing tools when needed |

This baseline is for general data science. Add domain packages such as Scanpy,
DESeq2, Seurat, or enrichment tools when the selected analyses need them. Avoid
installing every possible bioinformatics tool during initialization.

## Initialize and install

Inspect existing manifests first. For a project without a Pixi workspace, run
these commands from its root:

```sh
pixi init --format pixi --channel conda-forge .
pixi add python numpy pandas scipy matplotlib seaborn scikit-learn statsmodels \
  jupyterlab ipykernel pyyaml openpyxl pytest \
  r-base r-dplyr r-tidyr r-readr r-ggplot2 r-data.table r-readxl \
  r-irkernel r-jsonlite r-yaml
pixi install --locked
```

`pixi init` defaults to the current platform; declare additional known compute
targets when needed and resolve for them too. Do not claim that solving a target
platform verifies execution on that platform. Let Pixi select compatible versions
and record its generated constraints and lockfile. Apply known analysis/runtime
constraints before solving, rather than assuming the newest runtime is required.

For an existing workspace, preserve its manifest format, channels, constraints,
tasks, and lockfile. A Pixi-enabled `pyproject.toml` is also valid; do not create a
competing `pixi.toml`. Add missing baseline packages when environment setup is
requested, without blindly rerunning an unversioned add over existing pins or
upgrading unrelated dependencies. Preserve explicitly chosen narrower baselines.

Use conda-forge for the starter set. Add other required channels, such as
Bioconda, only for a known dependency, respecting their documented channel order
and platform support. Do not remove a requested package silently to make solving
succeed. Explain incompatibilities and resolve them with suitable constraints or
a named environment.

Track the actual manifest and generated `pixi.lock`; ignore `.pixi/`. Initialization
is incomplete if the environment has only been described or locked but not
installed. If Pixi is unavailable or installation fails, complete independent
scaffolding, report the exact blocker, and leave the environment marked incomplete.
Do not fabricate a lockfile or silently use system Python/R instead.

## Verify both runtimes

Run lightweight checks from the project root after installation:

```sh
pixi run --locked python -c 'import sys, numpy, pandas, scipy, matplotlib, seaborn, sklearn, statsmodels, jupyterlab, ipykernel, yaml, openpyxl, pytest; print(sys.version); print(sys.executable)'
pixi run --locked Rscript --vanilla -e 'pkgs <- c("dplyr", "tidyr", "readr", "ggplot2", "data.table", "readxl", "IRkernel", "jsonlite", "yaml"); invisible(lapply(pkgs, library, character.only = TRUE)); print(R.version.string); print(R.home())'
```

Confirm the Python executable and R home belong to the project environment.
Ensure imported packages come from that environment, not an inherited user
library or `PYTHONPATH`. Record resolved Python/R versions, verification outcome,
and any omitted user-requested packages in the root README's setup section. Adapt
checks when the user chose a different baseline. Do not run scientific analyses
as an environment smoke test.

## Maintain it throughout the project

- Run Python, R, notebooks, tests, and scientific CLIs with `pixi run --locked`
  from the project root. Ordinary file inspection and Git need no Pixi wrapper.
  Keep commands and explicit task input/output paths in the relevant README.
- Add analysis dependencies with `pixi add`; use `pixi add --pypi` for required
  Python packages unavailable from the configured conda channels. Prefer
  Pixi-managed conda packages for R as well.
- Do not use direct `pip install`, `conda install`, `install.packages()`, or
  `BiocManager::install()` to mutate the project environment or a user library.
  If an R dependency cannot be supplied through Pixi-managed packages, report the
  gap and propose a reproducible packaging solution; do not invent a fallback.
- Resolve deliberate dependency edits with Pixi, review manifest/lock changes,
  and rerun the affected import checks. For an unexpected stale lock, diagnose
  the mismatch rather than dropping `--locked` to hide it.
- Select notebook interpreters/kernels from the project environment. Avoid
  globally registering a kernel or changing user-wide R/Python configuration
  merely to initialize a project.

Command behavior is documented in [pixi init](https://pixi.prefix.dev/latest/reference/cli/pixi/init/),
[pixi add](https://pixi.prefix.dev/latest/reference/cli/pixi/add/), and
[pixi run](https://pixi.prefix.dev/latest/reference/cli/pixi/run/).
