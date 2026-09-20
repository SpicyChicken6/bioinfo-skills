#!/usr/bin/env python3
"""Copy to <project>/scripts/biofolder.py and register the two Pixi tasks."""

import argparse
import os
from pathlib import Path
import re


WORKSPACE_DIRS = (
    "code", "tests", "data/interim", "data/processed",
    "figures", "tables", "docs", "logs",
)
NUMBERED = re.compile(r"^(\d+)-(.+)$")


def slug(value):
    name = re.sub(r"[\s_]+", "-", value.strip().lower())
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Use a name containing letters, digits, spaces, underscores or hyphens, not a path.")
    return name


def directory(path):
    if path.is_symlink():
        raise ValueError(f"Refusing to scaffold through a symbolic link: {path}")
    path.mkdir(exist_ok=True)
    return path


def write_missing(path, text):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError(f"Expected a regular file: {path}")
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(text)
    except FileExistsError:
        pass


def project_root():
    # Pixi supplies this even though named tasks execute from the workspace root.
    # The fallback also supports running the installed helper directly.
    root = Path(os.environ.get("PIXI_PROJECT_ROOT") or Path(__file__).resolve().parents[1]).resolve()
    if not any((root / name).is_file() for name in ("pixi.toml", "pyproject.toml")):
        raise ValueError("Install this helper as scripts/biofolder.py in a Pixi project first.")
    return root


def module_path(root, name):
    modules = root / "modules"
    if modules.is_symlink():
        raise ValueError(f"Refusing to scaffold through a symbolic link: {modules}")
    exact = modules / name
    if exact.exists() or exact.is_symlink() or not modules.exists():
        return exact
    # Reuse modules made by earlier biofolder versions without renaming them.
    matches = [
        path for path in modules.iterdir()
        if (path.is_dir() or path.is_symlink())
        and (match := NUMBERED.fullmatch(path.name)) and match[2] == name
    ]
    if len(matches) > 1:
        raise ValueError(f"Ambiguous module '{name}'; use its full folder name.")
    return matches[0] if matches else exact


def add_module(root, name):
    path = module_path(root, name)
    directory(root / "modules")
    existed = path.exists()
    directory(path)
    directory(path / "tasks")
    write_missing(path / "tasks" / ".gitkeep", "")
    write_missing(path / "README.md", f"# {name}\n\n## Scope\n\n## Inputs\n\n## Tasks\n\nSee [tasks/](tasks/).\n")
    return path, existed


def infer_module(root):
    # Path.cwd() alone loses the module when invoked through a named Pixi task.
    caller = Path(os.environ.get("INIT_CWD") or Path.cwd()).resolve()
    try:
        parts = caller.relative_to(root / "modules").parts
    except ValueError:
        parts = ()
    if not parts:
        raise ValueError("From the project root use: pixi run add-task <module> <task>. Inside a module, supply just <task>.")
    return parts[0]


def add_task(root, module, name):
    path, _ = add_module(root, module)
    tasks = path / "tasks"
    matches = []
    highest = 0
    for candidate in tasks.iterdir():
        if not (candidate.is_dir() or candidate.is_symlink()):
            continue
        match = NUMBERED.fullmatch(candidate.name)
        if match:
            highest = max(highest, int(match[1]))
        if candidate.name == name or (match and match[2] == name):
            matches.append(candidate)
    if len(matches) > 1:
        raise ValueError(f"Multiple tasks named '{name}' exist in {tasks}; resolve the duplicate names first.")
    if matches:
        return directory(matches[0]), True
    task = tasks / f"{highest + 1:02d}-{name}"
    task.mkdir()
    write_missing(
        task / "README.md",
        f"# {name}\n\n## Goal\n\n## Inputs\n\n## Methods\n\n## Validation\n\n## Accepted outputs\n\n"
        "## Workspaces\n\n- [agent/](agent/)\n- [manual/](manual/)\n",
    )
    for workspace in ("agent", "manual"):
        base = directory(task / workspace)
        for relative in WORKSPACE_DIRS:
            leaf = base
            for part in Path(relative).parts:
                leaf = directory(leaf / part)
            write_missing(leaf / ".gitkeep", "")
    return task, False


def main():
    parser = argparse.ArgumentParser(description="Create biofolder modules and numbered task workspaces.")
    commands = parser.add_subparsers(dest="command", required=True)
    module = commands.add_parser("module", help="Create an unnumbered module.")
    module.add_argument("name")
    task = commands.add_parser("task", help="Create the next numbered task; infer the module when inside one.")
    task.add_argument("names", nargs="+", metavar="NAME", help="TASK, or MODULE TASK from the project root")
    args = parser.parse_args()
    try:
        root = project_root()
        if args.command == "module":
            path, existed = add_module(root, slug(args.name))
        else:
            if len(args.names) not in (1, 2):
                raise ValueError("Supply TASK inside a module, or MODULE TASK from the project root.")
            name = slug(args.names[-1])
            module = slug(args.names[0]) if len(args.names) == 2 else infer_module(root)
            path, existed = add_task(root, module, name)
    except (ValueError, OSError) as error:
        parser.exit(2, f"biofolder: {error}\n")
    print(f"{'Existing' if existed else 'Created'}: {path.relative_to(root)}")


if __name__ == "__main__":
    main()
