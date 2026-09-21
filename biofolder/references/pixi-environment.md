# Project environment

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

Also install `rclone` from conda-forge for the [result sync command](sync-results.md).
In an existing project, add it with `pixi add rclone` when result sync setup is
requested, preserving manifest constraints and tracking the updated lockfile.
Verify `pixi run rclone version`; cloud credential setup is a separate action.

## Jupyter and MCP

- Add `jupyter-collaboration` and `jupyter-mcp-tools` to the JupyterLab
  environment, and install `jupyter-mcp-server` in the connector's environment.
  Manage these through Pixi, using PyPI dependencies where needed; reuse
  compatible installations and lock the resolved versions.
- Follow the [official setup guide](https://github.com/datalayer/jupyter-mcp-server#-getting-started)
  for the selected deployment. The connector may run alongside Jupyter or in
  a separate Pixi environment on its host.
- Register the connection in the agent client separately; installing packages
  alone does not enable MCP tools.
- Verify shared notebook editing, saved cell outputs, and execution in the
  project's kernel. Report unavailable connections or failed checks as incomplete
  setup.

## Research Flow

Include `research-flow` in the project environment. If missing, install a
versioned wheel from its [official GitHub releases](https://github.com/SpicyChicken6/research-flow/releases)
as a Pixi-managed PyPI dependency; it is not published on the PyPI index.
Preserve a compatible existing version. Verify the CLI and read-only YAML parser
without starting the server.

## Setup and maintenance

- Reuse an existing Pixi manifest (`pixi.toml` or Pixi-enabled `pyproject.toml`),
  preserving constraints, channels, tasks, and unrelated dependencies. Declare
  known compute platforms; a successful solve does not verify execution there.
- Track the manifest and generated `pixi.lock`; ignore `.pixi/`. Initialization
  requires a real installation and lightweight Python/R package-loading checks,
  with interpreters and libraries coming from the project environment. Record
  setup steps, resolved runtime versions, and verification in `docs/environment.md`.
- Run analysis code, notebooks, tests, and scientific CLIs through Pixi with the
  lockfile enforced. Ordinary shell inspection and Git need no Pixi wrapper.
- Prefer Pixi-managed dependencies, including PyPI support. Preserve constraints
  and diagnose installation failures or stale locks before choosing a fallback.
- If Pixi cannot provide a required package, use its native installer with the
  Pixi runtime and a project-local library visible to project sessions. Do not
  overwrite Pixi-managed packages or use user/system libraries. Track pinned
  sources, versions/checksums, dependencies, and reproduction commands separately
  from `pixi.lock`; ignore installed libraries and verify package functionality.
- Agents may use command-scoped `--run-post-link-scripts` after reviewing package
  provenance and hook contents for actions appropriate to the setup. Avoid
  persistent opt-ins; verify package loading and any downloaded annotation data.
  If execution policy denies the action, explain the blocker and request approval;
  do not retry the denied action through another mechanism.
- If installation or a dependency is unavailable, report the blocker and a
  reproducible resolution; finish independent scaffolding and mark environment
  setup incomplete. Do not silently omit packages or substitute system runtimes.

See the [Pixi documentation](https://pixi.prefix.dev/latest/) for command details.
