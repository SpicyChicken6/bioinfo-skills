# Tool workflow contract

Use `docs/workflow.yaml` for both the component overview and the development plan.
The [example](../examples/workflow.yaml) uses Research Flow schema version 1:

| Field | Constraint |
| --- | --- |
| `schema_version` | Integer `1`. |
| `project.name` | Required nonempty text. |
| `project.id`, `project.description` | Optional text. |
| `tasks` | List of at most 500 tasks; may be empty. |
| `tasks[].id` | Globally unique, stable; matches `[A-Za-z0-9][A-Za-z0-9_-]{0,63}`. |
| `title` | Required nonempty text. |
| `goal`, `notes`, `agent_instructions` | Optional text context, not execution authority. |
| `status` | `todo`, `in_progress`, `blocked`, or `done`; default `todo`. |
| `depends_on` | Distinct existing task IDs; no self-reference or cycles. |
| `parent_id` | Optional existing parent ID or null; no ancestry cycles. |
| `inputs`, `outputs` | Lists of textual artifact references. |
| `layout.positions` | Optional task-ID mapping to numeric `{x, y}` positions. |

## Components and relationships

Put the tool's purpose, component paths, responsibilities, and runtime call/data
relationships in multiline `project.description`. Distinguish planned components
from implemented ones. Task-specific interface details can live in YAML `notes`
or the linked task README. This uses supported fields without creating a second
architecture document or requiring custom schema extensions.

The component overview is prose context; Research Flow does not turn it into a
separate runtime component graph. `depends_on` represents development
prerequisites, not imports or runtime calls. Optional `parent_id` groups work by
component; grouping and visual placement do not define execution order.

## Tasks and paths

Use stable task IDs and link workspace READMEs from `notes` when present. Record
the corresponding ID in each task README. Grouping nodes and small tasks need
no separate folder; `agent/` and `manual/` are not separate YAML tasks.

Resolve new plans' relative artifact paths from `docs/`, using `../src/`,
`../tests/`, and `../tasks/`. Commands run from the project root. Preserve an
existing plan's explicitly different path base.

Initialization includes drafting an initial plan. Use `todo` for future work and
identify outputs as expected. Keep actual validation evidence in task READMEs
or linked reports. A recorded `done` status alone does not prove validation.

Reading the plan does not request execution or edits. Edit existing plans only
within the requested scope; preserve unrelated fields, comments, extension
metadata, and visual positions. Validate read-only using
`research_flow.server.parse_project` when available, otherwise safely parse
YAML and check the constraints above. Report which validation was performed.
