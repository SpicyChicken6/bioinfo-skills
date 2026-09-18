# Project instructions

Read the project README, `docs/workflow.yaml`, and relevant module/task READMEs
before work. Follow the user's scope and existing project conventions.

## Communication and documentation

- Default to concise, clear responses and documentation.
- For task overviews, state the goal, a short sequence of major steps, and
  expected outputs. Keep the overview high level and easy to scan.
- Include decision points only when user input is needed or the choice
  materially changes the analysis. Use sensible defaults for routine choices.
- Keep implementation details, alternative approaches, and troubleshooting
  out of the overview unless needed to understand the work. Expand when asked.

## Structure and ownership

- Use `modules/<module>/tasks/<task>/`, with stable, zero-padded names. Each task
  has a shared `README.md` and two workspaces: `agent/` and `manual/`.
- Put agent work in `agent/`, using `code/`, `tests/`, `data/interim/`,
  `data/processed/`, `figures/`, `tables/`, `docs/`, and `logs/` as needed.
  Read human work for context; change `manual/` only when explicitly requested.
- Keep the shared task README current with inputs, methods, reproduction commands,
  validation, and accepted output links. Preserve human notes. Ownership does not
  imply validation; identify which results downstream work should use.
- Keep data at its shared scope: project data across modules, module data across
  tasks, and task derivatives in their producing workspace. Reference one
  authoritative copy and preserve raw inputs unchanged.
- Use `interim/` for intermediate datasets, `processed/` for analysis-ready data,
  and `tables/` for findings. Archive retired work under root `.archive/` with
  provenance; active work must not depend on archived files.

## Pixi

- Use one project-root Pixi workspace shared by all modules and both workspaces.
  Default new projects to Python and R with the starter data-science packages;
  add analysis-specific dependencies as needed. Use named environments only
  for incompatible toolchains.
- Manage scientific dependencies and execution through Pixi's locked environment.
  Preserve existing constraints; do not silently use system runtimes or install
  packages outside Pixi. Verify affected runtimes/packages after dependency changes.
- Track the manifest and generated `pixi.lock`; ignore `.pixi/`. Reuse an existing
  Pixi-enabled `pyproject.toml` instead of adding a competing `pixi.toml`.
  Report failed or incomplete environment setup.

## Git

- Use Git throughout the project. At session start, review staged, unstaged, and
  untracked changes before editing.
- Checkpoint reviewed, in-scope changes observed unchanged for at least 24 hours.
  If age is unknown, keep a lightweight local first-observation record; update it
  when content changes. Reuse existing records rather than guessing age from file
  timestamps or the latest commit.
- Commit coherent completed agent work at session end without waiting a day.
  These local commits are authorized unless the user requests otherwise.
- Preserve unrelated human changes and staged selections. Defer checkpoints that
  would disturb them or interfere with an ongoing Git operation. A checkpoint
  preserves work; it does not certify results. Push only when authorized.
- Track source, docs, configuration, environment definitions, and selected small
  artifacts. Exclude raw/private/large datasets, secrets, environments, and caches
  according to project policy. Report commits and anything left uncommitted.

## Workflow documentation

- Keep the canonical plan in `docs/workflow.yaml` and detailed workflows in task
  workspace docs.
- Reading the plan does not authorize executing tasks or editing the plan.
  Change only requested fields and preserve unrelated content and layout.
- YAML artifact paths are relative to `docs/`; commands run from the project root.
  Preserve another path base if an existing plan explicitly declares one.
