# Project instructions

These rules apply throughout this project and across sessions. Keep this file as
the shared source of project rules; keep evolving research notes in task docs.
Follow explicit user overrides and preserve existing work when applying changes.

## Orient before working

- Read the project `README.md`, `docs/workflow.yaml`, and the relevant module and
  task READMEs before analysis work. Inspect existing files before creating new
  ones; ask only for essential information that is still missing.
- Work within the requested scope. Reading these instructions or a workflow plan
  does not request new analyses, tasks, metadata, directories, or plan changes.
- Keep the hierarchy **project → module → task → agent/manual**. Use stable,
  zero-padded module/task names; preserve established identifiers and paths.

## Place files and preserve ownership

- Put analysis work under the relevant task's `agent/` workspace inside
  `modules/`, with `code/`, `tests/`, `data/interim/`, `data/processed/`, `figures/`,
  `tables/`, `docs/`, and `logs/` as needed. Do not scatter task artifacts at the
  project, module, or task root. Create deeper directories only when useful.
- Each task has one shared `README.md` and separate `agent/` and `manual/`
  workspace roots. Read `manual/` for context or comparison; edit, move, or delete
  its contents only when the user explicitly requests those changes.
- Maintain the shared task README within the requested work. Preserve human
  notes; document input paths, dependencies, commands, methods, result links, and
  validation evidence. Put detailed workflow descriptions in workspace `docs/`.
- Ownership is not validation. Distinguish exploratory, validated, and accepted
  results. Record explicitly selected downstream artifacts and their provenance;
  do not automatically favor agent outputs or claim planned outputs exist.
- Root `data/` holds datasets shared across modules; module `data/` holds inputs
  and datasets shared across its tasks. Task-specific derivatives stay in the
  producing workspace. Keep one authoritative copy and reference it directly.
- Preserve original `raw/` inputs unchanged. Write intermediate datasets to
  `data/interim/`, analysis-ready datasets to `data/processed/`, findings to
  `tables/`, and figures to `figures/`. Record sources and transformations.
- Archive established retired work under root `.archive/` with its original
  location, reason, and replacement documented. Check references before moves;
  active work must not depend on archived or disposable scratch files.

## Use Pixi for the project environment

- Use one project-root Pixi workspace for both human and agent work. Keep
  dependencies and repeatable tasks in `pixi.toml`, or reuse a Pixi-enabled
  `pyproject.toml` when already present. Track that manifest and the generated
  `pixi.lock` in Git, and ignore `.pixi/`. Preserve existing constraints and avoid
  creating competing manifests.
- A new project's default environment contains both Python and R with the
  baseline data-science packages. Add analysis-specific dependencies as needed.
  Use named environments within the same workspace only for incompatible
  toolchains; do not create separate environments per module or task by default.
- Run scientific Python, R, notebooks, tests, and analysis command-line tools
  through the root workspace with `pixi run --locked`. Run commands from the
  project root and give explicit input/output paths. Ordinary shell inspection,
  file operations, and Git do not need to run through Pixi.
- Manage dependencies with `pixi add`. Prefer available conda packages, including
  R packages; use `pixi add --pypi` for needed Python packages unavailable through
  the configured conda channels. Keep every dependency in the manifest and
  lockfile. Do not modify the environment through direct `pip`, `conda`,
  `install.packages()`, or `BiocManager::install()` calls.
- If a required R package cannot be resolved with Pixi-managed dependencies,
  explain the blocker and propose a reproducible solution. Do not silently
  install into a user/system library or switch to system Python/R.
- Resolve intended dependency changes and generate the lockfile through Pixi,
  then run lightweight Python/R import checks through the locked environment.
  If Pixi is missing or resolution fails, report setup as incomplete and continue
  independent work. Never fabricate a lockfile or remove `--locked` merely to
  conceal an unexpected manifest/lockfile mismatch.

## Keep the workflow explicit

- `docs/workflow.yaml` is the canonical Research Flow plan. Its `depends_on`
  links define dependencies; numbering, grouping, and visual position do not.
- Treat the plan as context, not an execution queue. A status such as `todo` or
  `in_progress` does not authorize running that task or its dependencies. Recorded
  completion is not independently verified evidence.
- Leave statuses, notes, inputs/outputs, dependencies, IDs, grouping, and layout
  unchanged unless the user requests plan edits. Preserve unrelated fields and
  concurrent changes when making an authorized edit.
- Resolve new workflow artifact paths relative to `docs/`, for example
  `../data/` and `../modules/`. Shell/Pixi command paths are project-root-relative.
  Preserve and document another path base if an existing plan declares one.
- Link task-specific workflow documentation from the shared task README. Do not
  create a project-level `workflow.md` or a duplicate `project-status.md`.
