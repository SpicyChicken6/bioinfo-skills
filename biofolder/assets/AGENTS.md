# Project instructions

Read the project README, `docs/workflow.yaml`, and relevant module/task READMEs
before work. Follow the user's scope and existing project conventions.

## Communication and documentation

- Default to concise, clear responses and documentation.
- Keep root `README.md` limited to project background and research questions.
  Track tasks and dependencies in `docs/workflow.yaml`, with details in
  module/task READMEs.
- Module READMEs use **Description**, optional **Requirements**, and **Tasks** links.
  Reference shared configuration for conventions such as sample-group colors.
- Task READMEs use **Description**, **Plan**, and **Output**: briefly state
  what the task does and why, its main steps, and expected deliverables.
- Create and maintain `agent/docs/methods.md` in each task; add it if missing when
  working on an existing task and link it from the task README's **Plan** section.
  Document actual inputs, data processing in execution order, analysis methods,
  reproduction commands, and validation, with links to code and outputs. Identify
  upstream preprocessing and incoming data scale. For normalization and
  transformations, record exact methods, parameters/formulas, reference or
  scaling factors, applicable axes/groups, and resulting scale. Include filtering,
  missing-value handling, and other processing when used, plus observed checks.
  Identify the data version used by each analysis and figure. Mark unknowns and
  unexecuted steps explicitly; update this record when methods or inputs change.
- Include decision points only when user input is needed or the choice
  materially changes the analysis. Use sensible defaults for routine choices.
- Keep implementation details, alternative approaches, and troubleshooting
  out of the overview unless needed to understand the work. Expand when asked.

## Structure and ownership

- Use `modules/<module>/tasks/<NN-task>/`: unnumbered modules and stable task
  numbers. Preserve existing names. Each task has a shared `README.md` plus
  `agent/` and `manual/` workspaces.
- Use `pixi run add-module <module>` and `pixi run add-task <module> <task>`.
  Inside a module or its descendants, `pixi run add-task <task>` infers the module.
  Tasks use the next number; repeated names reuse existing tasks. The commands
  create both workspaces with the standard subfolders, preserving existing files.
- Put agent work in `agent/`, using `code/`, `tests/`, `data/interim/`,
  `data/processed/`, `figures/`, `tables/`, `docs/`, and `logs/` as needed.
  Read human work for context; change `manual/` only when explicitly requested.
- Human reviews and next-task guidance live in each task's `agent/docs/review.md`.
  Read relevant reviews, when present, before continuing work or starting a
  dependent task. These files are human-written; preserve them unless asked to
  edit. Agents do not need to create or update reviews.
- Keep the task README's **Output** section current with links to accepted artifacts;
  preserve human notes. Keep the methods record in `agent/docs/methods.md`, with
  supporting evidence in workspace notebooks or reports. Ownership does not imply validation.
- Keep data at its shared scope: project data across modules, module data across
  tasks, and task derivatives in their producing workspace. Reference one
  authoritative copy and preserve raw inputs unchanged.
- Use `interim/` for intermediate datasets, `processed/` for analysis-ready data,
  and `tables/` for findings. Archive retired work under root `.archive/` with
  provenance; active work must not depend on archived files.
- For requested uploads, use `pixi run sync-results --remote <name> --destination <folder>`
  (preview; add `--upload` to copy). Only manual `results/`, `figures/`, and `tables/`
  are included; use `--help` for options.

## Analysis and execution

- Use notebooks in agent/code/ for interactive analysis and figures.
  Keep cells focused and runnable in order; save key outputs.
- Use the configured Jupyter MCP connection and project Pixi kernel.
  If unavailable, save executed notebooks and report the limitation.
- On Slurm clusters, run notebook kernels in compute-node allocations.
  Request suitable memory and walltime; reuse suitable existing sessions.
- Extract reusable or complex logic into scripts while keeping the
  notebook's parameters, steps, and results understandable.
- Use Slurm for substantial unattended jobs and Nextflow for multi-step
  or parallel workflows. Standalone scripts may use sbatch directly.
- Reuse cluster profiles, record run details, and verify outputs.
- Review persisted results in notebooks without automatically
  resubmitting jobs. Save expensive intermediates.
- Consult [Nextflow Agent Skills](https://github.com/nextflow-io/agent-skills)
  when needed. Its launch-workflow skill targets Seqera Platform;
  use the Slurm executor for direct cluster runs.
- Preserve Nextflow caches and work directories while resume is needed.

## Pixi

- Use one project-root Pixi workspace shared by all modules and both workspaces.
  Default new projects to Python and R with the starter data-science packages;
  add analysis-specific dependencies as needed. Use named environments only
  for incompatible toolchains.
- During project setup, provision JupyterLab, collaboration support,
  kernels, and the required Jupyter MCP components through Pixi.
  Reuse compatible installations and verify shared notebook editing
  and execution. Configure the agent's MCP connection separately.
- If Research Flow is missing from the project environment, install a versioned
  wheel from its [official releases](https://github.com/SpicyChicken6/research-flow/releases)
  as a Pixi-managed PyPI dependency.
- Prefer Pixi-managed dependencies and run through its locked environment.
  Preserve constraints and diagnose failures before using a fallback. If Pixi
  cannot provide a package, use its native installer with the Pixi runtime and a
  project-local library visible to project sessions. Do not overwrite Pixi-managed
  packages or use user/system libraries. Track pinned sources, versions/checksums,
  dependencies, and reproduction commands separately from `pixi.lock`; ignore
  installed libraries and verify affected packages and required data.
- Agents may use command-scoped `--run-post-link-scripts` after reviewing package
  provenance and hook contents for appropriate setup actions. Avoid persistent
  opt-ins. If execution policy denies the action, explain it and request approval;
  do not retry the denied action through another mechanism.
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

- Keep the canonical plan in `docs/workflow.yaml` and task methods in
  `agent/docs/methods.md`. An optional `agent/docs/workflow.md` can describe
  orchestration and link to the methods record.
- Reading the plan does not authorize executing tasks or editing the plan.
  Change only requested fields and preserve unrelated content and layout.
- YAML artifact paths are relative to `docs/`; commands run from the project root.
  Preserve another path base if an existing plan explicitly declares one.
