---
name: biofolder
description: Initialize and maintain organized bioinformatics research projects with modality modules, task-local agent/manual workspaces, shared data, a Research Flow plan, and a project-level Pixi environment. Use when starting a research project, choosing where analysis files belong, or reorganizing an existing project.
---

# Biofolder

Keep a research project understandable and reproducible as its analyses grow. Use
the hierarchy **project → module → task → agent/manual**. Apply the user's chosen
layout and existing project conventions before these defaults; do not restructure
unrelated work just because this skill is loaded.

Read [the example project layout](references/project-layout.md) when proposing or
initializing a project. It preserves the complete recommended tree; create only
the modules, tasks, and deeper directories that the project currently needs.

## Placement and ownership

- A module represents a modality or major analysis component, including a
  cross-modality integration module when needed.
- Name module and task directories with stable, zero-padded identifiers, such as
  `modules/01-transcriptomics/tasks/01-quality-control/`. Do not renumber established
  paths merely to change their display order.
- Each task has one shared `README.md` and two workspace directories: `agent/`
  and `manual/`. Put its code, tests, data, figures, tables, docs, and logs inside
  the appropriate workspace. Do not add task-root `code/` or `output/` directories.
- Write agent work in `agent/` by default. Reading `manual/` for context or
  comparison is allowed; editing, moving, or deleting its contents requires an
  explicit user instruction covering that change.
- Update shared task documentation within the requested work, preserving human
  notes and identifying who produced each result. Ownership does not indicate
  validation: either workspace can contain exploratory or accepted results.
- Root `data/` holds cross-module inputs and shared datasets. Module `data/` holds
  modality-specific inputs and datasets reused across its tasks. Workspace
  `data/` holds task-specific derivatives. Keep one authoritative copy and use
  documented references instead of copying data into every level.
- Preserve `raw/` inputs unchanged. Write reproducible intermediate datasets to
  `data/interim/`, analysis-ready datasets to `data/processed/`, and findings such
  as enrichment summaries to `tables/`. Put one-off diagnostic artifacts under
  the producing workspace's `logs/` or a task-specific scratch subdirectory.
- Retired work belongs in root `.archive/YYYY-MM-DD_description/`, with its
  original location, retirement reason, and replacement recorded. Active analyses
  must not depend on archived or disposable scratch files.

## Initialize a project

1. **Inspect first.** Read existing instructions, documentation, environment
   files, and relevant input locations. Distinguish an empty project from an
   existing analysis. Do not move, duplicate, or rename input datasets merely to
   make the example tree look complete.
2. **Ask for missing essentials.** Infer what is already documented; bundle the
   remaining questions into a short round:
   - Research goal and expected deliverables.
   - Modalities, input locations, and shared sample/subject identifiers.
   - Known analysis tasks and dependencies; suggest a small provisional set when
     these are undecided, without inventing scientific methods or results.
   - Required languages/tools and target compute environment, including local
     versus HPC execution and relevant operating systems.
3. **Propose the smallest useful layout.** Explain the initial modules, tasks,
   shared inputs, and references to existing files. Resolve consequential unknowns
   before dependent work. When initialization is already requested and the scope
   is clear, proceed without adding repeated confirmation gates.
4. **Create the scaffold.** Add a root README and module READMEs with indexes. For
   each initial task, create its shared README plus both workspace roots; populate
   deeper directories only as needed. Document known sources and sample mappings
   without inventing metadata rows. Create project-wide methods/decision notes
   only when there is useful content to record.
5. **Record persistent rules.** Merge a concise structure/ownership/environment
   section into `AGENTS.md`; preserve existing instructions. Have `CLAUDE.md`
   explicitly refer to those shared rules rather than maintaining a second copy.
   Include where to read the workflow and relevant task README, where new files
   belong, raw-input protection, manual-workspace ownership, Pixi commands, and
   the boundary on changing the workflow plan. Keep growing research notes in
   task docs, not in instruction files.
6. **Draft the requested initial plan.** New-project initialization includes
   creating `docs/workflow.yaml` for the identified tasks. Read
   [the workflow YAML contract](references/workflow-yaml.md) first. An existing
   plan is context: preserve it unless the user has requested plan changes. Do not
   create a root `workflow.yaml`, a project-level `workflow.md`, or a duplicate
   `project-status.md`. Detailed workflow explanations belong in task workspace
   docs and are linked from the shared task README.
7. **Set up Pixi and verify.** Follow the environment and verification guidance
   below. Report what was created, what remains undecided, and any environment
   setup that could not be completed. Initializing a project does not itself
   authorize running its scientific analyses or publishing the repository.

## Project environment

- Use one Pixi workspace at the project root, shared by modules and by human and
  agent work. Keep dependencies and repeatable tasks in `pixi.toml`; track the
  generated `pixi.lock` in Git and ignore `.pixi/`.
- Inspect and reuse an existing Pixi manifest. Add only dependencies needed for
  known tasks. Use named environments within that workspace when toolchains need
  incompatible dependencies; do not create a separate environment per task by
  default or fall back silently to system Python, pip, or ad hoc conda installs.
- Generate the lockfile through Pixi after dependency resolution. If Pixi is
  unavailable or resolution fails, finish independent structure/documentation
  work and report the environment as incomplete. Never fabricate a lockfile.
- Define and document task commands from the project root with explicit input
  and output paths. Run project tools with `pixi run`; use `pixi run --locked`
  for reproduction checks that should fail on a stale lockfile.
- Ignore caches, secrets, local environments, and large/private data as
  appropriate. Preserve code, documentation, manifests, and small intentional
  test fixtures. Do not indiscriminately ignore all of `agent/` or `manual/`.

## Task documentation and ongoing work

Each shared task README records:

- Objective, module context, input references, and prerequisite tasks.
- Human and agent approaches, reproduction commands, and links to workspace docs.
- Result locations, validation evidence, comparisons, and unresolved differences.
- Explicitly selected outputs for downstream use, including their owner and
  provenance; distinguish candidates from accepted results.
- Current observations and next steps without presenting planned work as executed.

Keep detailed workflow/method notes in `agent/docs/` or `manual/docs/`, optionally
as `workflow.md`. Read the project plan and relevant task README before work.
Perform only the requested task: a YAML dependency or a `todo` status is not an
execution request. Do not silently mark tasks done, change dependencies, or alter
plan layout. Workflow edits require a user request covering those edits; see the
[YAML guidance](references/workflow-yaml.md).

An integration task references the accepted upstream artifacts directly. Do not
silently favor the agent result, overwrite a human result, or promote uncertain
findings merely to fill an expected output path.

For requested reorganization, inventory affected files and path consumers, show
the proposed moves and conflicts, and preserve work outside the authorized scope.
Do not overwrite colliding files. Update affected references and verify consumers
before retiring old paths. A placement question alone does not authorize a bulk
migration. Archive work only when its retirement is established; age alone is not
evidence that an analysis is obsolete.

## Verify proportionally

- Confirm the chosen module/task paths and ownership boundaries match the request.
- Check documentation links and declared existing inputs. Clearly distinguish
  expected future artifacts from files that should already exist.
- Validate workflow syntax, unique IDs, dependency references, acyclic graphs,
  and paths relative to `docs/`. Preserve unrelated fields in an existing plan.
- Check the Pixi manifest/lockfile and a lightweight environment command when
  setup succeeds. Do not run an expensive analysis just to verify a scaffold.
- After an authorized migration, check affected imports, paths, and run commands;
  report remaining breakage rather than claiming that a tidy tree proves success.
