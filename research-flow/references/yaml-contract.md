# Research Flow YAML contract

This reference describes schema version 1. The app is a plan editor and persistence
service; installing this skill does not create a background agent or automatically
execute the graph. Use this contract to interpret the plan. Reading it does not authorize running
steps or changing the YAML.

## Fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1` |
| `project.name` | Required nonempty project title |
| `project.id`, `project.description` | Optional text providing identity and context |
| `tasks` | List of at most 500 tasks |
| `tasks[].id` | Stable unique text ID, 1–64 characters; starts with a letter or digit, followed by letters, digits, `_`, or `-` |
| `title` | Required nonempty task title |
| `goal` | Intended outcome; optional text |
| `status` | `todo`, `in_progress`, `blocked`, or `done`; defaults to `todo` |
| `depends_on` | List of distinct existing prerequisite task IDs; no self-reference or cycles |
| `parent_id` | Optional existing parent task ID or null; one parent per task, no ancestry cycles |
| `inputs`, `outputs` | Lists of textual artifact references; not executable commands |
| `notes` | Research decisions, observations, results, or blockers; optional text |
| `agent_instructions` | Optional task-specific guidance; not a permission override |
| `layout.positions` | Map from task ID to numeric `{x, y}` positions; preserve during execution |
| Additional fields | Extension metadata; preserve unless explicitly changing it |

Dependencies and ancestry are separate graphs. Both must remain valid. A branch
container may have a high-level deliverable in addition to its child steps.
Older files may contain `substeps`; the app converts these to child tasks in memory.
Do not save just to perform that conversion. Safe reads must leave original bytes
untouched, including comments and formatting.

Example (illustrative only; never substitute it for the user's workflow):

```yaml
schema_version: 1
project:
  id: study
  name: Example study
tasks:
  - id: analysis
    title: Analyze the study
    goal: Produce a reproducible analysis report
    status: todo
    depends_on: []
  - id: qc
    parent_id: analysis
    title: Check the input data
    status: todo
    depends_on: []
    inputs: [data/counts.tsv]
    outputs: [reports/qc.md]
  - id: model
    parent_id: analysis
    title: Fit the model
    status: todo
    depends_on: [qc]
    inputs: [data/counts.tsv, reports/qc.md]
    outputs: [results/model.tsv]
    agent_instructions: Use the model specified in the study protocol.
layout:
  positions: {}
```

`qc` is a prerequisite of `model`; `analysis` is their branch parent, not an
implicit prerequisite. This describes the intended pipeline; it is not a request
to run quality control or fit the model. The user determines which work to request.
