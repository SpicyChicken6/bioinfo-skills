# Workflow and preview

Adapt the [example](../assets/workflow.yaml) into `docs/workflow.yaml`.
Use `project.description` for components and runtime relationships; `tasks`
tracks development work. `depends_on` means development prerequisites.
Artifact paths are relative to `docs/`; outputs of pending tasks are planned.
Keep task IDs stable and use `todo`, `in_progress`, `blocked`, or `done`.

Install [Research Flow](https://github.com/SpicyChicken6/research-flow/blob/main/docs/install.md)
as development tooling in the project's Pixi workspace. The preview helper needs
`research_flow.server.parse_project` and
`research_flow.workflow_html.render_workflow_html`. Use a compatible release or
pinned official source revision; tested revision:
`41e0db6c3758846c7e3df5410b71cda99042b32b`. On Windows, use WSL with this revision.

Copy [preview_workflow.py](../assets/preview_workflow.py) to
`scripts/preview_workflow.py` and generate the initial read-only preview:

```sh
pixi run --locked python scripts/preview_workflow.py
```

Add `-e <name>` for a named environment. Record the actual command in README.md
and link the generated `docs/workflow-preview.html`.

The helper refreshes only its own generated output; preserve unrelated files
if a filename collision is reported.
