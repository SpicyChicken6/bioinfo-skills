# Upload manual results

Use a remote already configured in rclone, such as a Box, OneDrive, or Google
Drive connection. `--remote` takes the configured name (for example, `my-box`),
with an optional trailing colon; it does not take a provider name or cloud URL.
`--destination` is the folder path within that remote. Quote paths with spaces.

```bash
# Preview: no files are uploaded. --dry-run is also accepted explicitly.
pixi run sync-results --remote my-box --destination Project_Results

# Upload new or changed files when ready.
pixi run sync-results --remote my-box --destination Project_Results --upload

# Limit either mode to one existing module.
pixi run sync-results --remote my-onedrive --destination "Research/Project Results" --module transcriptomics
```

The command selects files in each task's `manual/results/`, `manual/figures/`,
and `manual/tables/` across all modules. Running from a module or task directory
does not narrow the selection; use `--module` explicitly. Existing numbered
modules retain their full names.

Paths are preserved relative to the project root. For example:

```text
modules/transcriptomics/tasks/01-differential-expression/manual/tables/genes.csv
→ my-box:Project_Results/modules/transcriptomics/tasks/01-differential-expression/manual/tables/genes.csv
```

Agent workspaces and other task directories, including `code/`, `data/`, and
`logs/`, are outside the selection. Keep raw inputs in their designated data
directories. Notebook checkpoints, `.gitkeep`, `.DS_Store`, and symlinks are
excluded. The command uses [rclone copy](https://rclone.org/commands/rclone_copy/)
with checksum comparison to upload new or changed files. If the remote does not
support a common checksum, rclone falls back to file size for comparison.
It never deletes remote files, including results previously
uploaded from agent workspaces.

## Setup

New-project initialization installs rclone and registers `sync-results` alongside
the module/task commands. For an existing project, when setup is requested,
merge the current [helper](../assets/biofolder.py) into `scripts/biofolder.py`,
preserving customizations, and register the task in its existing Pixi manifest:

```toml
[tasks]
sync-results = "python scripts/biofolder.py sync-results"
```

Use `[tool.pixi.tasks]` for a Pixi-enabled `pyproject.toml`. Add the dependency
with `pixi add rclone`, track the manifest and lockfile, and verify
`pixi run rclone version` and `pixi run sync-results --help`. Reuse the project's
existing environment and other tasks. Updating the installed skill alone does
not migrate existing project helpers.

The user configures cloud credentials separately; list existing remote names
with `pixi run rclone listremotes`. Preview the requested selection before the
first upload and report any setup or access failure. Do not upload as part of
initialization or feature testing.
