# Research Flow contract

`docs/workflow.yaml` is the canonical project plan; detailed methods belong in
task docs.
Validate read-only with Research Flow in the project's Pixi environment. If
environment setup is blocked, safely parse YAML against this version 1 contract.

| Field | Constraint |
| --- | --- |
| `schema_version` | Integer `1`. |
| `project.name` | Required nonempty text. |
| `project.id`, `project.description` | Optional text. |
| `tasks` | List of at most 500 tasks; may be empty. |
| `tasks[].id` | Globally unique, stable; matches `[A-Za-z0-9][A-Za-z0-9_-]{0,63}`. |
| `title` | Required nonempty text. |
| `goal` | Optional intended outcome. |
| `status` | `todo`, `in_progress`, `blocked`, or `done`; default `todo`. |
| `depends_on` | Distinct existing task IDs; no self-reference or cycles. |
| `parent_id` | Optional existing parent ID or null; no ancestry cycles. |
| `inputs`, `outputs` | Lists of textual paths, URLs, or descriptions. |
| `notes`, `agent_instructions` | Optional context, not execution authority. |
| `layout.positions` | Optional task-ID mapping to numeric `{x, y}` positions. |

Use module-qualified IDs such as `rna-qc`. Link each shared task README in `notes`
and record its ID in that README. Only `depends_on` defines execution order;
parent grouping, folder numbers, and visual placement do not. Grouping nodes need
no separate task folder, and `agent/` and `manual/` need no separate YAML tasks.

Resolve new plans' relative artifact paths from `docs/`: `../data/...` and
`../modules/...`. Shell/Pixi commands remain project-root-relative. Preserve an
existing plan's explicitly different path base; reference external data in place.

Project initialization authorizes drafting an initial plan: use `todo`, include
understood tasks, label unknowns, and describe future outputs as expectations.
Reading a plan or working on a task does not authorize executing the graph or
editing it. Change existing plans only when requested; preserve comments,
unrelated metadata, and visual positions. Report statuses as recorded without
inferring validation or completion from other nodes.

The [example](../examples/workflow.yaml) illustrates cross-module dependencies and
paths for a generated project's `docs/workflow.yaml`; it is not a discovered plan
for this repository or the user's study.
