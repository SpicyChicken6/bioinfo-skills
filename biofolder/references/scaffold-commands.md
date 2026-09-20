# Module and task commands

During project initialization, copy [the helper](../assets/biofolder.py) to
`scripts/biofolder.py` in the project. It uses only Python's standard library.
Register these tasks in the existing Pixi manifest, preserving other tasks and
any customized helper. For an existing project, install them when adding a
module/task or when requested.

```toml
[tasks]
add-module = "python scripts/biofolder.py module"
add-task = "python scripts/biofolder.py task"
```

For a Pixi-enabled `pyproject.toml`, use `[tool.pixi.tasks]` instead. Keep the
default task working directory and do not override `INIT_CWD`: the helper uses
Pixi's original invocation directory to identify the module.

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

A module gets `README.md` and `tasks/`. A new task gets a shared `README.md` plus
`agent/` and `manual/`, each with `code/`, `tests/`, `data/interim/`,
`data/processed/`, `figures/`, `tables/`, `docs/`, and `logs/`. Empty directories
contain `.gitkeep` so they survive Git checkout. Existing tasks are returned
unchanged, and existing files are never overwritten. Commands print the path;
workflow plans and analysis execution remain separate from folder creation.

Verify both root and module-local invocations in a temporary project before
reporting command setup complete; also check repeat calls preserve existing work.
