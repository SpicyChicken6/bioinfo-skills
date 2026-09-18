# Research Flow plan

Use `docs/workflow.yaml` as the canonical project plan. It covers dependencies
within and across modules. Root/module READMEs link to the plan and task READMEs;
the task workspace docs explain detailed methods and workflows. Do not maintain
a separate project-wide `workflow.md` or a competing status file.

The schema below follows Research Flow version 1. The skill is usable without
installing the Research Flow app or skill. If the project has an installed
Research Flow validator, use its supported read-only parser; otherwise safely
parse YAML and check these constraints without rewriting the source file.

## Essential fields

| Field | Meaning and constraint |
| --- | --- |
| `schema_version` | Integer `1`. |
| `project.name` | Required nonempty project title. |
| `project.id`, `project.description` | Optional text. |
| `tasks` | List containing at most 500 tasks. An empty list is valid while the design is undecided. |
| `tasks[].id` | Stable, globally unique ID, 1–64 characters; starts with a letter or digit and contains only letters, digits, `_`, or `-`. |
| `title` | Required nonempty task title. |
| `goal` | Optional intended outcome. |
| `status` | `todo`, `in_progress`, `blocked`, or `done`; defaults to `todo`. Recorded progress is not proof of validation. |
| `depends_on` | Distinct prerequisite IDs that exist in the plan; no self-reference or cycles. |
| `parent_id` | Optional existing parent ID or null, for grouping. One parent per task; no ancestry cycles. |
| `inputs`, `outputs` | Lists of textual paths, URLs, or descriptions; not executable commands. |
| `notes`, `agent_instructions` | Optional context; does not authorize execution or override project rules. |
| `layout.positions` | Optional task-ID mapping to numeric `{x, y}` positions; visual layout only. |

Preserve additional metadata and unrelated fields when editing an existing plan.
Never normalize, migrate, or save a plan just to read it. Preserve comments and
visual positions during targeted authorized edits.

## Mapping the plan to folders

- Qualify IDs by module, for example `rna-qc`, `protein-qc`, and
  `integration-sample-alignment`. Repeated local task numbers are not globally
  unique IDs.
- Link the corresponding shared task README in `notes`; record the same YAML ID
  in that README. Module grouping may use `parent_id`, but does not imply a
  dependency or require creating a second on-disk task for the grouping node.
- `depends_on` determines execution ordering. Numeric folder prefixes, YAML
  list order, module membership, and canvas placement do not.
- A task's `agent/` and `manual/` directories express ownership. They do not
  automatically become sequential workflow steps or separate YAML tasks.

## Path convention

For new projects using this layout, resolve relative local artifact paths from
the YAML directory, `docs/`. Use `../data/...` for shared inputs and
`../modules/...` for task artifacts. This convention applies to YAML references;
documented shell/Pixi commands run from the project root and use `data/...` or
`modules/...` instead.

If an existing plan explicitly declares another base, preserve it and document
the difference rather than silently changing path interpretation. External data
can be referenced in place; do not copy it simply to satisfy this layout.

## Initial versus existing plans

An explicit request to initialize a new project authorizes drafting its initial
plan. Include only understood tasks and label suggestions/unknowns in notes. A
new plan starts with `todo` statuses and names future outputs as expectations,
not as files that have already been created or accepted.

Reading a plan or implementing a task does not authorize changing that plan.
Edit statuses, dependencies, artifacts, grouping, or layout only when the user
requests those changes. Show existing statuses as recorded, without inferring
completion from parent or child nodes. Never treat the graph as a queue to run.

Read [the illustrative workflow](../examples/workflow.yaml) for a small example
of paths and cross-module dependencies. It is designed for a generated project's
`docs/workflow.yaml`; it does not describe this skill repository or the user's
actual study. Adapt it only when the user's requested initialization or plan
edit calls for such a workflow. Do not silently select it as a discovered plan.
