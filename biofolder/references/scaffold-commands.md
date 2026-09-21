# Project commands

During project initialization, copy [the helper](../assets/biofolder.py) to
`scripts/biofolder.py` in the project. The helper uses Python's standard library;
result uploads also require the Pixi-managed `rclone` executable.
Register these tasks in the existing Pixi manifest, preserving other tasks and
any customized helper. For an existing project, install module/task commands
when adding a module/task; add result sync when requested.

```toml
[tasks]
add-module = "python scripts/biofolder.py module"
add-task = "python scripts/biofolder.py task"
sync-results = "python scripts/biofolder.py sync-results"
```

For a Pixi-enabled `pyproject.toml`, use `[tool.pixi.tasks]` instead. Keep the
default task working directory and do not override `INIT_CWD`: the helper uses
Pixi's original invocation directory to identify the module for `add-task`.
`sync-results` always selects from the project root, regardless of invocation
directory; use its explicit `--module` option to limit scope.

```bash
# From the project root; add-task also creates a missing module.
pixi run add-module transcriptomics
pixi run add-task transcriptomics differential-expression

# From a module or anywhere below it:
cd modules/transcriptomics
pixi run add-task enrichment
```

Modules have no automatic number. Tasks use the highest existing task number + 1
within that module, starting at `01`; gaps are not reused. New names become
lowercase hyphenated folder names; quote names containing spaces. Module lookup
prefers an exact existing name, then a unique normalization-equivalent name;
ambiguous matches require an exact name. Numeric prefixes are part of module
names: select an older numbered module by its full name or from inside it.

A module gets `README.md` with **Description**, **Requirements**, and **Tasks**,
plus a `tasks/` directory. Fill in applicable requirements and task README links;
omit Requirements if none apply. A new task gets a shared `README.md` plus
`agent/` and `manual/`, each with `code/`, `tests/`, `data/interim/`,
`data/processed/`, `figures/`, `tables/`, `docs/`, and `logs/`. The task README has
**Description**, **Plan**, and **Output** sections for a concise task brief.
Empty directories contain `.gitkeep` so they survive Git checkout. Existing tasks
are returned unchanged, and existing files are never overwritten. Commands print
the path; workflow plans and analysis execution remain separate from folder creation.

See [result sync](sync-results.md) for cloud destination options, selection rules,
and setup in existing projects. Initialization registers all three commands and
installs rclone; it does not configure cloud credentials or upload files.

Verify both root and module-local invocations in a temporary project before
reporting command setup complete; also check repeat calls preserve existing work.
