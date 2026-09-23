---
name: biofolder
description: Initialize and maintain bioinformatics projects with root READMEs for project background and research questions, concise module/task READMEs, modality modules, agent/manual workspaces, Git, Pixi, and manual-result cloud uploads. Use when starting a project, documenting its purpose or tasks, placing analysis files, reorganizing work, or setting up result sync.
---

# Biofolder

Organize projects as **project → module → task → agent/manual**. Follow the
[project rules](assets/AGENTS.md), adapting defaults to the user's choices and
existing conventions. Use the [full example tree](references/project-layout.md)
when proposing a layout; create only what the project needs.

## Update source

The canonical source is the `biofolder/` directory in
[SpicyChicken6/bioinfo-skills](https://github.com/SpicyChicken6/bioinfo-skills).
When an update is requested or newer guidance is needed, fetch the repository's
default branch and compare the complete skill directory, including its bundled
resources, with the local copy. Honor explicit version pins and preserve local
customizations.

For a clean checkout on the default branch, use `git pull --ff-only`; for a
copied installation, refresh the complete `biofolder/` directory from that source
after reviewing the differences. Updating the skill does not automatically
migrate existing project files; apply those changes only within the requested scope.

## Initialize a project

1. Inspect existing instructions, files, Git changes, and environments. Ask only
   for missing essentials: research goal, modalities, input locations and sample
   identifiers, initial tasks, and compute/runtime constraints.
2. Propose modules for each modality or major analysis component, including
   integration where needed. Use unnumbered module names and stable, zero-padded
   task numbers. Preserve existing names and reference datasets in place.
3. Adapt the [project README template](assets/project-README.md) into root `README.md`,
   containing only project background and research questions to state the project's
   high-level purpose. Module READMEs use **Description**, **Requirements**, and
   **Tasks**. Create initial tasks with a shared README containing **Description**,
   **Plan**, and **Output**, plus `agent/` and `manual/` workspaces; add deeper
   folders as needed. For manual scaffolding, create `agent/docs/methods.md` from the
   [methods template](assets/task-methods.md) and link it from **Plan**. Label
   unexecuted steps as planned.
4. Merge [AGENTS.md](assets/AGENTS.md) into the project root, preserving existing
   project instructions. Keep research notes in task docs.
5. Draft the canonical task list and dependencies in `docs/workflow.yaml` using
   the [Research Flow schema](references/workflow-yaml.md).
   New-project initialization includes this initial plan; existing plans change
   only when requested. Detailed workflows belong in task docs.
6. Install the [starter environment](references/pixi-environment.md) with Python,
   R, Jupyter/MCP, Research Flow, and rclone through Pixi unless the user specifies otherwise.
   Verify the runtimes, shared notebook connection, Research Flow, lockfile, and
   requested packages/data. Reuse existing manifests and constraints; follow the
   reference's fallback and post-link rules.
   Install the [module/task and result sync commands](references/scaffold-commands.md).
   Cloud credentials and uploads are separate from initialization.
7. Reuse the covering Git repository or initialize one at the project root.
   Review tracking exclusions and commit the scaffold and environment definitions,
   preserving unrelated work. Report checks, unresolved choices, and incomplete
   setup. Initialization does not include scientific analyses or publication.

## Maintain or reorganize a project

Apply the project rules for file placement, ownership, Pixi, and session Git
checkpoints. Module READMEs describe the module's role, record applicable
requirements, and link task READMEs for navigation. Requirements can cover group
labels, color palettes, or output conventions; omit the section if none apply.
Define shared conventions once in project configuration (for example,
`config/plotting.yaml` for sample-group colors) and reference them from modules.
Keep detailed input information in the module's `data/README.md` and task status
and dependencies in `docs/workflow.yaml`.

Keep task READMEs concise: **Description** states what the task does
and why, **Plan** lists the main steps, and **Output** describes expected deliverables
and links accepted artifacts when available. Create and maintain
`agent/docs/methods.md` for each task using the [methods template](assets/task-methods.md);
add it when first working on an existing task if missing, and link it from the
task README's **Plan** section. Record actual inputs, ordered data processing,
analysis methods, reproduction commands, and validation, with links to supporting
code, notebooks, and outputs. Distinguish inherited preprocessing from steps
performed in this task; document normalization and transformations precisely,
including parameters, formulas, data scale, and checks. Mark unknowns and planned
steps explicitly, and update the record when methods or inputs change.
After each agent run on a task, including partial or failed runs, append a dated run
summary and caveats to this file before the final response: outcomes, output
links, validation status, limitations, and remaining work. Preserve earlier
entries and relevant unresolved caveats; mark caveats resolved or superseded with
supporting evidence, and link the record in the response.
Downstream tasks should reference selected upstream artifacts with their provenance.

Human reviews and next-task guidance live in each task's `agent/docs/review.md`;
the [simple review template](assets/task-review.md) is optional. Read relevant
reviews, when present, before continuing work or starting a dependent task.
These files are human-written; preserve them unless asked to edit. Agents do not
need to create or update reviews.

For new modules/tasks, use the [scaffold commands](references/scaffold-commands.md):
`pixi run add-module <module>` or `pixi run add-task <module> <task>`.
Inside a module, `pixi run add-task <task>` infers the module. Install the commands
if missing when adding a module/task; preserve existing work and task numbering.
New tasks include `agent/docs/methods.md` from the template and a README **Plan**
link; existing tasks are returned unchanged.

For cloud result uploads, use the [result sync command](references/sync-results.md):
`pixi run sync-results --remote <name> --destination <folder>` previews manual
results across all modules; `--module <name>` narrows the selection and `--upload`
copies them. Preserve the full `modules/<module>/tasks/<task>/manual/...` paths.
Use an existing configured rclone remote and upload only when requested. Install
or update the helper, Pixi task, and rclone dependency in existing projects only
within the requested scope, preserving customizations.

For a requested reorganization, review affected paths and consumers, preserve
existing work, update references, and verify what moved. Archive retired work
with its original location, reason, and replacement documented. A placement
question alone does not authorize a bulk migration.

Verify the actual change: layout and links for scaffolds, YAML validity for plan
edits, runtime/package checks for environment changes, and affected consumers
for moves. Report remaining problems without claiming unperformed validation.
