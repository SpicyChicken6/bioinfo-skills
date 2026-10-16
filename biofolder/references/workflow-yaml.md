# Research Flow contract

`docs/workflow.yaml` is the canonical project plan; each task's actual inputs,
ordered data processing, analysis methods, and validation belong in
`agent/docs/methods.md`, linked from its task README.
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

## Regenerate the preview

After creating or updating the canonical YAML, generate an offline, read-only
HTML with Research Flow before reporting the work complete. Direct YAML edits
do not trigger the app's automatic preview-on-Save behavior. Run from the project
root, adapting the paths to an existing project's conventions:

```bash
pixi run --locked python - <<'PY'
from datetime import datetime, timezone
from pathlib import Path
from research_flow.server import parse_project
from research_flow.workflow_html import render_workflow_html

source = Path("docs/workflow.yaml")
document = parse_project(source.read_text(encoding="utf-8"))
preview = source.with_name(source.stem + "-preview.html")
preview.write_text(render_workflow_html(
    document, read_only=True, layout_mode="stages",
    saved_at=datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
), encoding="utf-8")
print(preview)
PY
```

This uses the installed package's renderer without starting a server or executing
workflow tasks. It validates and reads the YAML without reserializing it, preserving
comments and layout. Use `layout_mode="freeform"` to preview saved node positions.
Reserve `workflow-preview.html` for this generated output; preserve unrelated files
at that path. The app manages `workflow.html` with its own ownership marker, so do
not write direct renderer output there.

When a figure is useful, add the following inside the Python block to generate
`docs/workflow-preview.svg` from the same validated document:

```python
from research_flow.workflow_plot import render_workflow_svg
preview.with_suffix(".svg").write_text(
    render_workflow_svg(document, layout_mode="stages"), encoding="utf-8",
)
```

Refresh any supplied figure after later YAML edits too. Verify the files were
generated successfully, inspect the preview when a viewer is available, and link
the HTML (and any figure) in the response. Users can open the HTML directly in a
browser without Research Flow running; an already-open preview needs reloading.
The YAML remains authoritative, and generated previews are not edited by hand.

If the renderer is unavailable, follow the [environment guidance](pixi-environment.md#research-flow).
Report failed generation and label any previous preview stale; do not present an
old file as the updated workflow or claim visual checks that were not performed.
