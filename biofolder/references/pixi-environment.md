# Python and R environment

New-project initialization installs both runtimes in one project-root Pixi
workspace, shared across modules and human/agent work. Use the default environment;
add named environments only for incompatible dependencies. Honor a user-requested
baseline or scaffold-only setup.

## Starter packages

Install this baseline from conda-forge, then add domain packages as analyses need
them. Let Pixi resolve compatible versions within known project constraints.

| Purpose | Python packages | R packages (conda names) |
| --- | --- | --- |
| Runtime | `python` | `r-base` |
| Data handling | `numpy`, `pandas` | `r-dplyr`, `r-tidyr`, `r-readr`, `r-data.table` |
| Statistics/modeling | `scipy`, `statsmodels`, `scikit-learn` | Base R `stats` |
| Plotting | `matplotlib`, `seaborn` | `r-ggplot2` |
| Notebooks | `jupyterlab`, `ipykernel` | `r-irkernel` |
| File formats | `pyyaml`, `openpyxl` | `r-readxl`, `r-jsonlite`, `r-yaml` |
| Testing | `pytest` | Base R checks |

## Setup and maintenance

- Reuse an existing Pixi manifest (`pixi.toml` or Pixi-enabled `pyproject.toml`),
  preserving constraints, channels, tasks, and unrelated dependencies. Declare
  known compute platforms; a successful solve does not verify execution there.
- Track the manifest and generated `pixi.lock`; ignore `.pixi/`. Initialization
  requires a real installation and lightweight Python/R package-loading checks,
  with interpreters and libraries coming from the project environment. Record
  resolved runtime versions and verification in the root README.
- Run analysis code, notebooks, tests, and scientific CLIs through Pixi with the
  lockfile enforced. Ordinary shell inspection and Git need no Pixi wrapper.
- Manage dependencies through Pixi, including its PyPI support when needed.
  Avoid direct pip, conda, or R package installs and user-wide configuration.
  Add channels or named environments only as required, then verify affected
  packages. Diagnose stale locks rather than bypassing them.
- If installation or a dependency is unavailable, report the blocker and a
  reproducible resolution; finish independent scaffolding and mark environment
  setup incomplete. Do not silently omit packages or substitute system runtimes.

See the [Pixi documentation](https://pixi.prefix.dev/latest/) for command details.
