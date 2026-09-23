---
name: toolfolder
description: Initialize and organize reusable software tools with shared source and tests, task workspaces, a locked project environment, and a workflow YAML for components and development tasks. Use when scaffolding a tool repository or organizing its development; use biofolder for analysis projects organized around research outputs.
---

# Toolfolder

Keep maintained source and tests in stable, shared locations. Use task folders
for plans, experiments, and review, with one canonical component overview and
development plan in `docs/workflow.yaml`.

## Initialize a tool project

1. Inspect existing instructions, source, Git changes, and environment files.
   Establish the tool's purpose, intended users, interfaces, language, and initial
   scope from context. Ask only for missing choices that affect the design.
2. Adapt the [example layout](references/project-layout.md) to the language and
   existing conventions. Start with source, tests, examples, and documentation;
   add task workspaces and deeper directories only where useful. Keep one
   canonical implementation shared by humans and agents.
3. Adapt the [project README](assets/project-README.md) to explain purpose,
   installation, and a working example. Merge the [project instructions](assets/AGENTS.md)
   into root `AGENTS.md`, preserving existing rules. Fill in actual development
   commands once configured; label anything not yet implemented or verified.
4. Create `docs/workflow.yaml` using the [workflow contract](references/workflow-yaml.md)
   and [example](examples/workflow.yaml). Put component responsibilities and
   runtime relationships in `project.description`, with development tasks in
   `tasks`. Do not create a separate `architecture.md`. Initialization includes
   an initial plan, with future work marked `todo` and expected outputs identified.
5. When a task needs a workspace, use `tasks/<NN-name>/` with a shared
   [task README](assets/task-README.md). Use stable, zero-padded numbers as
   identifiers, not execution order. Link the README from the corresponding YAML
   task and record its workflow ID in the README. Create `agent/` and `manual/`
   only for separate exploratory work. Human feedback belongs in optional
   `review.md`, which agents read and preserve unless asked to edit.
6. Reuse the project's environment and package manager. For a new Python tool,
   prefer one root Pixi workspace in `pyproject.toml`, with package metadata and
   a generated `pixi.lock`. Use the language's normal manifest and lockfile for
   other stacks. Add only the runtimes and development tools the project needs;
   document commands for installation, tests, linting, and builds as applicable.
7. Reuse a covering Git repository or initialize one at the tool root. Review
   tracking exclusions. Validate the scaffold, links, workflow, and any configured
   environment or runnable example. Report what exists, what was checked, and
   what remains planned. Implement features only when included in the request.

## Maintain or reorganize a tool

Follow the project instructions and existing language conventions. Maintained
implementation goes in `src/` (or its established equivalent), regression tests
in `tests/`, and reusable usage examples in `examples/`. Promote useful prototypes
into those locations when implementing a feature; shipped code must not import
from task workspaces. Use branches or worktrees for independent implementations.

Keep task READMEs concise: **Description**, **Plan**, and **Output**. Link shared
source, tests, and observed validation results instead of copying them. Put
longer implementation or scientific-method notes alongside the task and link
them from its README. Preserve human reviews and manual experiments.

Use `docs/workflow.yaml` as the canonical record of components, relationships,
task statuses, and dependencies. Keep detailed implementation notes in task
READMEs and link them from YAML `notes`. Reading the workflow is context for the
requested work, not a request to execute its graph. Edit an existing plan within
the user's requested scope, preserving unrelated content and layout. Record
significant design rationale in `docs/decisions.md` only when useful; do not
duplicate the component overview or task-status tracking there.

For requested reorganizations, inspect imports, entry points, packaging, tests,
examples, automation, and documentation that consume affected paths. Preserve
existing work, update consumers, and run checks appropriate to the move. A
placement question alone does not request a migration.
