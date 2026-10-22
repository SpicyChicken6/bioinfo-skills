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
metadata, and visual positions. Validate read-only with Research Flow using
`research_flow.server.parse_project`. If the tool is unavailable, safely parse
YAML and check the constraints above while reporting the incomplete Research
Flow setup. Parsing alone does not generate a preview.

## Regenerate the preview

Use [Research Flow](https://github.com/SpicyChicken6/research-flow) to validate and
visualize the plan. Reuse a compatible installation, or install a compatible wheel
from its [official releases](https://github.com/SpicyChicken6/research-flow/releases)
as development tooling, following the
[installation guide](https://github.com/SpicyChicken6/research-flow/blob/main/docs/install.md).
Keep it in the project's managed environment or an existing isolated tool
environment, not the tool's runtime dependencies. Record the version and setup
command. The interpreter below must be able to import `research_flow`; for Pixi,
use `pixi run --locked python` in place of `python`. A pipx installation may use
an interpreter separate from the project's Python.

Verify imports of `research_flow.server.parse_project` and
`research_flow.workflow_html.render_workflow_html`; a version string alone does
not prove preview support. The published v0.8.7 wheel predates the HTML renderer
and automatic previews on Save. Use a release that includes them or an official
source build pinned to a full commit SHA, preserving explicit project constraints
and recording the resolved source in the environment manifest and lockfile. If
those constraints prevent setup, report preview generation as incomplete.
Current upstream builds import Unix-only `fcntl` in the parser; on Windows, run
the full recipe in WSL unless the installed build passes these imports natively.
The file writer below supports both Windows and Unix, independently of that
upstream dependency.

After every authorized save of `docs/workflow.yaml`, including initial creation,
regenerate an offline, read-only HTML before reporting the work complete. App
Save refreshes `docs/workflow.html`; verify that refresh succeeded. Direct YAML
edits do not trigger it: run the recipe below from the project root to generate
`docs/workflow-preview.html` without rewriting YAML. Use that preview path in
project documentation, or adapt links to the app-generated path when using app
Save. Opening or reading a plan alone does not request a save or refresh.

```bash
python - <<'PY'
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import os
import stat
from research_flow.server import parse_project
from research_flow.workflow_html import render_workflow_html

source = Path("docs/workflow.yaml")
document = parse_project(source.read_text(encoding="utf-8"))
marker = ("<!-- toolfolder-workflow-preview source-sha256:"
          + sha256(source.name.encode("utf-8")).hexdigest() + " -->\n").encode("ascii")

def write_preview(path, content):
    payload = marker + content.encode("utf-8")
    flags = os.O_RDWR | getattr(os, "O_BINARY", 0)
    expected = None

    def check_file(info):
        reparse = getattr(info, "st_file_attributes", 0) & getattr(
            stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0
        )
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or reparse:
            raise FileExistsError(f"Refusing non-regular or linked output: {path}")

    try:
        fd = os.open(path, flags | os.O_CREAT | os.O_EXCL, 0o600)
        created = True
    except FileExistsError:
        expected = path.lstat()
        check_file(expected)
        fd = os.open(path, flags | getattr(os, "O_NOFOLLOW", 0)
                     | getattr(os, "O_NONBLOCK", 0))
        created = False
    with os.fdopen(fd, "r+b") as output:
        opened = os.fstat(output.fileno())
        check_file(opened)
        if not created and output.read(len(marker)) != marker:
            raise FileExistsError(f"Refusing output not owned by this workflow: {path}")
        current = path.lstat()
        check_file(current)
        check_file(os.fstat(output.fileno()))
        if (not opened.st_ino or not os.path.samestat(opened, current)
                or (expected is not None and not os.path.samestat(opened, expected))):
            raise FileExistsError(f"Output changed or identity is unavailable: {path}")
        output.seek(0)
        output.write(payload)
        output.truncate()

preview = source.with_name(source.stem + "-preview.html")
write_preview(preview, render_workflow_html(
    document, read_only=True, layout_mode="stages",
    saved_at=datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
))
print(preview)
PY
```

This uses the installed package's renderer without starting a server or executing
workflow tasks. It validates and reads the YAML without reserializing it, preserving
comments and layout. Use `layout_mode="freeform"` to preview saved node positions.
The writer creates new files exclusively and refreshes only regular,
unlinked files with this workflow's ownership marker. It refuses unmarked files
(including older previews), another workflow's marker, and symbolic or hard links.
Platform-specific flags are optional; path and open-file identity checks guard
refreshes before any writes even when `O_NOFOLLOW` is unavailable.
On a collision, choose an unused output basename and link that actual path; preserve
the existing file. Do not add a marker to bypass the check. The app manages
`workflow.html` with its own ownership marker, so do not write direct renderer
output there.

Verify generation succeeded and inspect the preview when a viewer is available.
Link the actual HTML path in the response and keep project README links consistent.
Users can open it directly in a browser without Research Flow running; reload an
already-open preview after a refresh. Keep YAML authoritative and regenerate
previews rather than editing them by hand.

If installation, validation, or rendering fails, report the failed step and mark
any previous preview stale. A successful YAML save alone does not mean its preview
was refreshed. Do not claim generation or visual checks that were not performed.
