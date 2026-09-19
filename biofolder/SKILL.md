---
name: biofolder
description: Initialize and maintain bioinformatics project layouts with modality modules, agent/manual task workspaces, Git tracking, and Pixi environments. Use when starting a project, placing analysis files, or reorganizing existing work.
---

# Biofolder

Organize projects as **project → module → task → agent/manual**. Follow the
[project rules](assets/AGENTS.md), adapting defaults to the user's choices and
existing conventions. Use the [full example tree](references/project-layout.md)
when proposing a layout; create only what the project needs.

## Initialize a project

1. Inspect existing instructions, files, Git changes, and environments. Ask only
   for missing essentials: research goal, modalities, input locations and sample
   identifiers, initial tasks, and compute/runtime constraints.
2. Propose modules for each modality or major analysis component, including
   integration where needed. Use stable, zero-padded names. Reference existing
   datasets in place rather than moving them to fit the example.
3. Create project/module README indexes and initial tasks. Each task has a shared
   README plus `agent/` and `manual/` workspaces; add deeper folders as needed.
4. Merge [AGENTS.md](assets/AGENTS.md) into the project root, preserving existing
   project instructions. Keep research notes in task docs.
5. Draft `docs/workflow.yaml` using the [Research Flow schema](references/workflow-yaml.md).
   New-project initialization includes this initial plan; existing plans change
   only when requested. Detailed workflows belong in task docs.
6. Install the [starter environment](references/pixi-environment.md) with Python,
   R, and Research Flow through Pixi unless the user specifies otherwise. Verify
   the runtimes, Research Flow, and lockfile. Reuse existing manifests and constraints.
7. Reuse the covering Git repository or initialize one at the project root.
   Review tracking exclusions and commit the scaffold and environment definitions,
   preserving unrelated work. Report checks, unresolved choices, and incomplete
   setup. Initialization does not include scientific analyses or publication.

## Maintain or reorganize a project

Apply the project rules for file placement, ownership, Pixi, and session Git
checkpoints. Keep task READMEs current with inputs, methods, reproducible commands,
validation, and accepted output links. Downstream tasks should reference the
selected upstream artifacts with their provenance.

For a requested reorganization, review affected paths and consumers, preserve
existing work, update references, and verify what moved. Archive retired work
with its original location, reason, and replacement documented. A placement
question alone does not authorize a bulk migration.

Verify the actual change: layout and links for scaffolds, YAML validity for plan
edits, runtime/package checks for environment changes, and affected consumers
for moves. Report remaining problems without claiming unperformed validation.
