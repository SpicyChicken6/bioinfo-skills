# Research Flow YAML contract

Schema version 1:

| Field | Constraint |
| --- | --- |
| `schema_version` | Integer `1`. |
| `project.name` | Required nonempty text. |
| `project.id`, `project.description` | Optional text. |
| `tasks` | List of at most 500 tasks. |
| `tasks[].id` | Globally unique, stable; matches `[A-Za-z0-9][A-Za-z0-9_-]{0,63}`. |
| `title` | Required nonempty text. |
| `goal`, `notes`, `agent_instructions` | Optional context; not execution authority. |
| `status` | `todo`, `in_progress`, `blocked`, or `done`; default `todo`. |
| `depends_on` | Distinct existing task IDs; no self-reference or cycles. |
| `parent_id` | Optional existing parent ID or null; no ancestry cycles. |
| `inputs`, `outputs` | Lists of textual artifact references. |
| `layout.positions` | Optional task-ID mapping to numeric `{x, y}` positions. |

Dependencies and ancestry are separate graphs. Preserve extension metadata and
visual positions during requested edits. Older plans may contain `substeps`,
which the app converts to child tasks in memory; reading must leave the original
file unchanged, including comments and formatting.

This example illustrates grouping versus dependency; it is not the user's plan:

```yaml
schema_version: 1
project:
  name: Example study
tasks:
  - id: analysis
    title: Analyze the study
  - id: qc
    title: Check inputs
    parent_id: analysis
  - id: model
    title: Fit the model
    parent_id: analysis
    depends_on: [qc]
```

`qc` is a prerequisite of `model`; their parent `analysis` is not.
