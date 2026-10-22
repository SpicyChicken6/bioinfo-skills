"""Refresh the generated preview for this project's development plan."""

from datetime import datetime, timezone
from pathlib import Path
import os
import stat
import tempfile

from research_flow.server import parse_project
from research_flow.workflow_html import render_workflow_html


MARKER = b"<!-- development-workflow-preview -->\n"


def write_preview(path, content):
    payload = MARKER + content.encode("utf-8")
    flags = os.O_RDWR | getattr(os, "O_BINARY", 0)
    def check_file(info):
        reparse = getattr(info, "st_file_attributes", 0) & getattr(
            stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0
        )
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or reparse:
            raise FileExistsError(f"Refusing non-regular or linked output: {path}")

    try:
        expected = path.lstat()
    except FileNotFoundError:
        # Publish without opening the destination or following a raced symlink.
        fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".workflow-preview-")
        try:
            with os.fdopen(fd, "wb") as output:
                output.write(payload)
            os.link(temporary, path)
        finally:
            os.unlink(temporary)
        return
    check_file(expected)
    fd = os.open(path, flags | getattr(os, "O_NOFOLLOW", 0)
                 | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "r+b") as output:
        opened = os.fstat(output.fileno())
        check_file(opened)
        if output.read(len(MARKER)) != MARKER:
            raise FileExistsError(f"Refusing output not owned by this workflow: {path}")
        current = path.lstat()
        check_file(current)
        check_file(os.fstat(output.fileno()))
        if (not opened.st_ino or not os.path.samestat(opened, current)
                or not os.path.samestat(opened, expected)):
            raise FileExistsError(f"Output changed or identity is unavailable: {path}")
        output.seek(0)
        output.write(payload)
        output.truncate()


def main():
    root = Path(__file__).resolve().parent.parent
    source = root / "docs" / "workflow.yaml"
    preview = source.with_name("workflow-preview.html")
    document = parse_project(source.read_text(encoding="utf-8"))
    html = render_workflow_html(
        document,
        read_only=True,
        layout_mode="stages",
        saved_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    write_preview(preview, html)
    print(preview.resolve())


if __name__ == "__main__":
    main()
