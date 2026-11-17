#!/usr/bin/env python3
"""Synchronize and inspect a private Plotbook reference checkout."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit

REPO_URL = "https://github.com/SpicyChicken6/plotbook.git"
SITE_URL = "https://plotbook.yzj-dev.org"
BRANCH = "main"
SYNONYMS = (
    ("heatmap", "heatmaps", "热图"),
    ("volcano", "火山图"),
    ("scatter", "散点图"),
    ("boxplot", "box plot", "箱线图"),
    ("violin", "小提琴图"),
    ("barplot", "bar chart", "柱状图", "条形图"),
    ("network", "网络图"),
    ("enrichment", "富集"),
    ("survival", "生存"),
    ("correlation", "相关性"),
)


class PlotbookError(Exception):
    """An actionable retrieval or synchronization failure."""


def default_root():
    if os.environ.get("PLOTBOOK_ROOT"):
        return Path(os.environ["PLOTBOOK_ROOT"]).expanduser().resolve()
    data = Path(os.environ.get("XDG_DATA_HOME") or "~/.local/share").expanduser()
    return (data / "plotbook").resolve()


def _root(root):
    return Path(root).expanduser().resolve()


def _git(root, *args, check=True):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"}
    # Retrieval must not run user-installed merge hooks or recurse into submodules.
    command = ["git", "-c", f"core.hooksPath={os.devnull}", "-c", "submodule.recurse=false"]
    if root is not None:
        command += ["-C", str(root)]
    try:
        result = subprocess.run(command + list(args), capture_output=True, text=True,
                                env=env, timeout=600)
    except FileNotFoundError as exc:
        raise PlotbookError("Git is required; install it before using Plotbook.") from exc
    except subprocess.TimeoutExpired as exc:
        raise PlotbookError("Git timed out; check connectivity and retry synchronization.") from exc
    if check and result.returncode:
        # Git/credential-helper diagnostics can contain authenticated URLs.
        raise PlotbookError(f"Git {args[0]} failed. Check repository access, connectivity, and local Git state.")
    return result


def _json(path):
    try:
        with path.open(encoding="utf-8") as stream:
            value = json.load(stream)
    except (OSError, ValueError) as exc:
        raise PlotbookError(f"Cannot read valid Plotbook JSON: {path.name}. Run sync or check the checkout.") from exc
    if not isinstance(value, dict):
        raise PlotbookError(f"Expected a JSON object in {path.name}.")
    return value


def _catalog(root):
    catalog = _json(root / "library" / "catalog.json")
    if not isinstance(catalog.get("templates"), list):
        raise PlotbookError("Plotbook catalog has no templates list.")
    return catalog


def _official_origin(origin):
    name = "spicychicken6/plotbook"
    return origin.lower().rstrip("/") in {
        f"https://github.com/{name}", f"https://github.com/{name}.git",
        f"git@github.com:{name}", f"git@github.com:{name}.git",
        f"ssh://git@github.com/{name}", f"ssh://git@github.com/{name}.git",
    }


def sync(root, repo_url=REPO_URL):
    """Clone once or fast-forward main; never discard local work."""
    root = _root(root)
    root.parent.mkdir(parents=True, exist_ok=True)
    lock = root.parent / f".{root.name}.plotbook-sync.lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise PlotbookError(f"Plotbook sync is busy: {lock}. Wait for the other sync; remove a stale lock only after confirming no sync is active.") from exc
    try:
        return _sync_locked(root, repo_url)
    finally:
        lock.rmdir()


def _sync_locked(root, repo_url):
    cloned = False
    if not root.exists():
        print(f"Downloading Plotbook to {root}", file=sys.stderr, flush=True)
        staging = Path(tempfile.mkdtemp(prefix=".plotbook-download-", dir=root.parent))
        try:
            _git(None, "clone", "--depth", "1", "--single-branch", "--branch", BRANCH,
                 "--", str(repo_url), str(staging))
            _catalog(staging)
            # Refuse to replace a path created by another process during the clone.
            if root.exists():
                raise PlotbookError("The download destination appeared during cloning. Retry sync.")
            staging.rename(root)
            cloned = True
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    if not root.is_dir():
        raise PlotbookError("Plotbook destination exists and is not a directory; choose another --root.")
    top = _git(root, "rev-parse", "--show-toplevel", check=False)
    if top.returncode or Path(top.stdout.strip()).resolve() != root:
        raise PlotbookError("Destination is not a Plotbook checkout root; choose another --root.")
    origin = _git(root, "remote", "get-url", "origin").stdout.strip()
    valid_origin = _official_origin(origin) if repo_url == REPO_URL else origin == str(repo_url)
    if not valid_origin:
        raise PlotbookError("Destination has a different origin; it will not be repointed. Choose another --root.")
    if _git(root, "status", "--porcelain", "--untracked-files=all").stdout.strip():
        raise PlotbookError("Plotbook has local changes or untracked files. Preserve them and resolve manually before syncing.")
    branch = _git(root, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    if branch.returncode or branch.stdout.strip() != BRANCH:
        raise PlotbookError("Plotbook is not on main. Select the intended clean checkout manually; no branch was switched.")
    before = _git(root, "rev-parse", "HEAD").stdout.strip()
    if not cloned:
        _git(root, "fetch", "--no-tags", "origin", BRANCH)
        upstream = _git(root, "rev-parse", "FETCH_HEAD").stdout.strip()
        if before != upstream:
            ancestry = _git(root, "merge-base", "--is-ancestor", "HEAD", upstream, check=False)
            if ancestry.returncode:
                raise PlotbookError("Plotbook has local commits, divergent history, or insufficient history for a fast-forward. Resolve manually; nothing was reset.")
            # Fast-forward alone still permits replacing ignored local files.
            _git(root, "merge", "--ff-only", "--no-overwrite-ignore", upstream)
    commit = _git(root, "rev-parse", "HEAD").stdout.strip()
    return {"root": str(root), "action": "cloned" if cloned else "updated" if before != commit else "current",
            "commit": commit, "catalog_updated_at": _catalog(root).get("updatedAt")}


def _asset(root, value):
    if not isinstance(value, str):
        raise PlotbookError("Invalid Plotbook asset path.")
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise PlotbookError("Expected a local Plotbook asset path, not a URL.")
    decoded = unquote(parsed.path)
    if not decoded.startswith("/library/") or "\\" in decoded or "\0" in decoded:
        raise PlotbookError("Invalid Plotbook library asset path.")
    library = (root / "library").resolve()
    path = (root / decoded.lstrip("/")).resolve()
    try:
        path.relative_to(library)
    except ValueError as exc:
        raise PlotbookError("Plotbook asset path escapes the library.") from exc
    return str(path)


def _board(root):
    path = root / "library" / "inspiration.json"
    if not path.exists():
        return []
    items = _json(path).get("items")
    if not isinstance(items, list):
        raise PlotbookError("Plotbook inspiration board has no items list.")
    return items


def _terms(query):
    words = {part.casefold() for part in re.split(r"[\s,，]+", query.strip()) if part}
    if not words:
        raise PlotbookError("Provide at least one search term.")
    expanded = set(words)
    for group in SYNONYMS:
        if any(term in query.casefold() for term in group):
            expanded.update(group)
    return expanded


def _url(identifier, inspiration=False):
    if inspiration:
        return f"{SITE_URL}/?view=inspiration&ref={quote(identifier, safe='')}"
    return f"{SITE_URL}/?figure={quote(identifier, safe='')}"


def search(root, query, limit=6, kind="figures"):
    """Search metadata only and return a bounded shortlist with image paths."""
    root = _root(root)
    if not isinstance(limit, int) or not 1 <= limit <= 20:
        raise PlotbookError("Search limit must be between 1 and 20.")
    if kind not in {"figures", "inspiration", "all"}:
        raise PlotbookError("Search kind must be figures, inspiration, or all.")
    catalog = _catalog(root)
    terms = _terms(query)
    records = []
    if kind != "inspiration":
        records.extend((record, False) for record in catalog["templates"])
    if kind != "figures":
        records.extend((record, True) for record in _board(root))
    matches = []
    for record, inspiration in records:
        if not isinstance(record, dict) or not isinstance(record.get("id"), str):
            raise PlotbookError("Invalid Plotbook catalog record.")
        score = 0
        for field, weight in (("title", 5), ("tags", 4), ("category", 3),
                              ("analysisCategories", 3), ("kind", 2),
                              ("description", 1), ("notes", 1)):
            text = json.dumps(record.get(field, ""), ensure_ascii=False).casefold()
            score += weight * sum(term in text for term in terms)
        if score:
            matches.append((score, record, inspiration))
    matches.sort(key=lambda match: -match[0])
    results = []
    for score, record, inspiration in matches[:limit]:
        item = {key: record[key] for key in ("id", "title", "kind", "category", "tags", "language",
                                             "analysisCategories", "source", "sourceUrl") if key in record}
        item.update({"description": (record.get("description") or record.get("notes") or "")[:500],
                     "preview_path": _asset(root, record.get("image" if inspiration else "preview")),
                     "url": _url(record["id"], inspiration), "score": score})
        results.append(item)
    return {"root": str(root), "catalog_updated_at": catalog.get("updatedAt"), "query": query,
            "total_matches": len(matches), "results": results}


def show(root, identifier):
    """Read one record and resolve its listed files without executing them."""
    root = _root(root)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", identifier):
        raise PlotbookError("Invalid Plotbook record ID.")
    catalog = _catalog(root)
    is_figure = any(record.get("id") == identifier for record in catalog["templates"])
    if is_figure:
        source = _json(root / "library" / "templates" / f"{identifier}.json")
        # Avoid duplicating full archived source structures and whole tutorial series.
        record = {key: source[key] for key in (
            "id", "title", "category", "analysisCategories", "tags", "language", "kind", "description",
            "preview", "source", "createdAt", "updatedAt", "code", "codeFilename", "intro",
            "interpretation", "environment", "files", "notes", "sourceAttribution", "sourceUsageScope"
        ) if key in source}
        if isinstance(source.get("sourceMetadata"), dict) and "paper" in source["sourceMetadata"]:
            record["paper"] = source["sourceMetadata"]["paper"]
        record["files"] = [{**file, "local_path": _asset(root, file["path"])} for file in source.get("files", [])]
    else:
        source = next((item for item in _board(root) if item.get("id") == identifier), None)
        if source is None:
            raise PlotbookError("Plotbook record not found. Search the current catalog first.")
        record = dict(source)
    return {"root": str(root), "catalog_updated_at": catalog.get("updatedAt"), "record": record,
            "preview_path": _asset(root, record.get("preview" if is_figure else "image")),
            "url": _url(identifier, not is_figure)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root(), help="Plotbook checkout (or PLOTBOOK_ROOT)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("sync", help="Clone once or update main safely before each skill use")
    search_parser = commands.add_parser("search", help="Search metadata without loading all assets")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=6)
    search_parser.add_argument("--kind", choices=("figures", "inspiration", "all"), default="figures")
    show_parser = commands.add_parser("show", help="Read one figure or inspiration reference")
    show_parser.add_argument("id")
    args = parser.parse_args(argv)
    try:
        if args.command == "sync":
            result = sync(args.root)
        elif args.command == "search":
            result = search(args.root, args.query, args.limit, args.kind)
        else:
            result = show(args.root, args.id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (PlotbookError, OSError) as exc:
        print(f"Plotbook: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
