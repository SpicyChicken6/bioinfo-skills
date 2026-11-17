"""Exercise Plotbook retrieval with disposable repositories and no network access."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import quote


SCRIPT = Path(__file__).resolve().parents[1] / "plotbook-reference/scripts/plotbook.py"
SPEC = importlib.util.spec_from_file_location("plotbook_reference", SCRIPT)
plotbook = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = plotbook
SPEC.loader.exec_module(plotbook)


class PlotbookReferenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name).resolve()
        self.source = self.work / "source"
        self.origin = self.work / "origin.git"
        self.root = self.work / "references" / "plotbook"
        self.source.mkdir()
        self.git(self.source, "init", "-b", "main")
        self.identity(self.source)
        self.write_library(self.source)
        self.commit(self.source, "Initial reference library")
        self.git(self.work, "clone", "--bare", str(self.source), str(self.origin))
        self.git(self.source, "remote", "add", "origin", str(self.origin))

    def git(self, cwd, *arguments):
        result = subprocess.run(
            ["git", "-C", str(cwd), *arguments],
            check=True, capture_output=True, text=True,
        )
        return result.stdout.strip()

    def identity(self, root):
        self.git(root, "config", "user.name", "Codex")
        self.git(root, "config", "user.email", "codex@openai.com")
        self.git(root, "config", "commit.gpgsign", "false")

    def commit(self, root, message):
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", message)

    def save_json(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def write_library(self, root):
        templates = [
            {"id": "fig-heatmap", "title": "聚类热图", "category": "heatmap",
             "description": "Clustered expression heatmap", "tags": ["expression", "热图"],
             "language": "R", "kind": "template"},
            {"id": "fig-expression", "title": "Expression comparison", "category": "barplot",
             "description": "Expression effect sizes", "tags": ["expression"],
             "language": "Python", "kind": "template"},
            {"id": "fig-network", "title": "PPI interaction network", "category": "network",
             "description": "A protein interaction network", "tags": ["network", "gene"],
             "language": "R", "kind": "template"},
        ]
        for item in templates:
            asset = root / "library" / "assets" / item["id"]
            asset.mkdir(parents=True)
            preview_name = "热图 one.png" if item["id"] == "fig-heatmap" else "cover.png"
            (asset / preview_name).write_bytes(b"fixture image bytes")
            (asset / "plot code.R").write_text("# Archived example; do not execute\n", encoding="utf-8")
            item["preview"] = f"/library/assets/{item['id']}/{quote(preview_name)}"
            item["source"] = {"name": "Fixture source", "url": "https://example.org/paper"}
            detail = {**item, "code": "# Archived example; do not execute\n",
                      "codeFilename": "plot code.R", "intro": "Fixture guide",
                      "files": [{"name": "plot code.R", "type": "code",
                                 "path": f"/library/assets/{item['id']}/plot%20code.R"}]}
            self.save_json(root / "library/templates" / f"{item['id']}.json", detail)
        self.save_json(root / "library/catalog.json",
                       {"version": 1, "updatedAt": "2026-11-17T00:00:00Z", "templates": templates})
        inspiration = root / "library/inspiration/ref-palette/image.png"
        inspiration.parent.mkdir(parents=True)
        inspiration.write_bytes(b"fixture inspiration")
        self.save_json(root / "library/inspiration.json", {
            "version": 1, "items": [{"id": "ref-palette", "title": "Muted botanical palette",
                                      "kind": "color", "tags": ["olive", "rose"],
                                      "notes": "Borrow the contrast", "image": "/library/inspiration/ref-palette/image.png"}],
        })

    def sync(self):
        # Git ignores --depth for plain local paths; file:// exercises real shallow clones.
        return plotbook.sync(self.root, repo_url=self.origin.as_uri())

    def state(self, root):
        return self.git(root, "rev-parse", "HEAD"), self.git(root, "status", "--porcelain")

    def publish_update(self):
        catalog_path = self.source / "library/catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog["updatedAt"] = "2026-11-18T00:00:00Z"
        catalog["templates"][0]["title"] = "Updated clustered 热图"
        self.save_json(catalog_path, catalog)
        self.commit(self.source, "Update reference library")
        self.git(self.source, "push", "origin", "main")
        return self.git(self.source, "rev-parse", "HEAD")

    def test_initial_clone_reports_absolute_root_and_revision(self):
        result = self.sync()
        self.assertEqual(result["action"], "cloned")
        self.assertEqual(Path(result["root"]), self.root)
        self.assertTrue(Path(result["root"]).is_absolute())
        self.assertEqual(result["commit"], self.git(self.source, "rev-parse", "HEAD"))
        self.assertEqual(result["catalog_updated_at"], "2026-11-17T00:00:00Z")
        self.assertTrue((self.root / "library/catalog.json").is_file())
        self.assertEqual(self.git(self.root, "remote", "get-url", "origin"), self.origin.as_uri())
        self.assertEqual(self.git(self.root, "rev-parse", "--is-shallow-repository"), "true")

    def test_repeated_sync_fetches_remote_updates_and_is_idempotent(self):
        self.sync()
        expected_commit = self.publish_update()
        result = self.sync()
        self.assertEqual(result["action"], "updated")
        self.assertEqual(result["commit"], expected_commit)
        self.assertEqual(result["catalog_updated_at"], "2026-11-18T00:00:00Z")
        self.assertEqual(self.state(self.root), (expected_commit, ""))
        repeated = self.sync()
        self.assertEqual(repeated["action"], "current")
        self.assertEqual(repeated["commit"], expected_commit)

    def test_dirty_tracked_and_untracked_files_are_preserved(self):
        self.sync()
        self.publish_update()
        for relative in ("library/catalog.json", "personal-notes.txt"):
            with self.subTest(relative=relative):
                target = self.root / relative
                original = target.read_bytes() if target.exists() else None
                target.write_bytes(b"Personal changes must survive\n")
                before = self.state(self.root)
                with self.assertRaises(plotbook.PlotbookError):
                    self.sync()
                self.assertEqual(self.state(self.root), before)
                self.assertEqual(target.read_bytes(), b"Personal changes must survive\n")
                if original is None:
                    target.unlink()
                else:
                    target.write_bytes(original)

    def test_upstream_cannot_overwrite_an_ignored_local_file(self):
        self.sync()
        (self.root / ".git/info/exclude").write_text("notes.txt\n", encoding="utf-8")
        notes = self.root / "notes.txt"
        notes.write_bytes(b"Personal notes must survive\n")
        before = self.state(self.root)
        self.assertEqual(before[1], "")
        self.assertEqual(self.git(self.root, "check-ignore", "notes.txt"), "notes.txt")

        (self.source / "notes.txt").write_bytes(b"New upstream notes\n")
        self.commit(self.source, "Start tracking notes")
        self.git(self.source, "push", "origin", "main")

        with self.assertRaises(plotbook.PlotbookError):
            self.sync()
        self.assertEqual(notes.read_bytes(), b"Personal notes must survive\n")
        self.assertEqual(self.state(self.root), before)

    def test_nonconflicting_ignored_file_does_not_block_updates(self):
        self.sync()
        (self.root / ".git/info/exclude").write_text("notes.txt\n", encoding="utf-8")
        notes = self.root / "notes.txt"
        notes.write_bytes(b"Personal notes must survive\n")
        expected_commit = self.publish_update()

        result = self.sync()
        self.assertEqual(result["action"], "updated")
        self.assertEqual(result["commit"], expected_commit)
        self.assertEqual(notes.read_bytes(), b"Personal notes must survive\n")
        self.assertEqual(self.state(self.root), (expected_commit, ""))

    def test_local_commit_ahead_of_remote_is_not_reset(self):
        self.sync()
        self.identity(self.root)
        (self.root / "personal-notes.txt").write_text("Keep my work", encoding="utf-8")
        self.commit(self.root, "Local notes")
        before = self.state(self.root)
        with self.assertRaises(plotbook.PlotbookError):
            self.sync()
        self.assertEqual(self.state(self.root), before)
        self.assertEqual((self.root / "personal-notes.txt").read_text(), "Keep my work")

    def test_diverged_checkout_is_not_merged_or_reset(self):
        self.sync()
        self.identity(self.root)
        (self.root / "local.txt").write_text("Local branch content", encoding="utf-8")
        self.commit(self.root, "Local commit")
        self.publish_update()
        before = self.state(self.root)
        with self.assertRaises(plotbook.PlotbookError):
            self.sync()
        self.assertEqual(self.state(self.root), before)
        self.assertEqual(self.git(self.root, "branch", "--show-current"), "main")

    def test_wrong_branch_is_preserved(self):
        self.sync()
        self.git(self.root, "checkout", "-b", "personal-work")
        before = self.state(self.root)
        with self.assertRaises(plotbook.PlotbookError):
            self.sync()
        self.assertEqual(self.state(self.root), before)
        self.assertEqual(self.git(self.root, "branch", "--show-current"), "personal-work")

    def test_existing_nonrepository_directory_is_not_overwritten(self):
        self.root.mkdir(parents=True)
        notes = self.root / "notes.txt"
        notes.write_text("Existing unrelated content", encoding="utf-8")
        with self.assertRaises(plotbook.PlotbookError):
            self.sync()
        self.assertEqual(notes.read_text(), "Existing unrelated content")
        self.assertEqual(list(self.root.iterdir()), [notes])

    def test_foreign_origin_and_nested_repository_paths_are_rejected(self):
        self.sync()
        before = self.state(self.root)
        wrong_origin = str(self.work / "unrelated.git")
        self.git(self.root, "remote", "set-url", "origin", wrong_origin)
        with self.assertRaises(plotbook.PlotbookError):
            self.sync()
        self.assertEqual(self.state(self.root), before)
        self.assertEqual(self.git(self.root, "remote", "get-url", "origin"), wrong_origin)
        self.git(self.root, "remote", "set-url", "origin", self.origin.as_uri())
        with self.assertRaises(plotbook.PlotbookError):
            plotbook.sync(self.root / "library", repo_url=self.origin.as_uri())
        self.assertEqual(self.state(self.root), before)

    def test_failed_remote_refresh_does_not_report_stale_checkout_as_current(self):
        self.sync()
        before = self.state(self.root)
        self.origin.rename(self.work / "unavailable-origin.git")
        with self.assertRaises(plotbook.PlotbookError) as caught:
            self.sync()
        self.assertTrue(str(caught.exception).strip())
        self.assertEqual(self.state(self.root), before)

    def test_multilingual_search_and_limit(self):
        self.sync()
        for query in ("热图", "heatmap"):
            with self.subTest(query=query):
                result = plotbook.search(self.root, query)
                self.assertEqual([item["id"] for item in result["results"]], ["fig-heatmap"])
        result = plotbook.search(self.root, "expression", limit=1)
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["total_matches"], 2)
        self.assertEqual(plotbook.search(self.root, "unmatched-phrase")["results"], [])

    def test_show_resolves_encoded_image_and_companion_paths(self):
        self.sync()
        result = plotbook.show(self.root, "fig-heatmap")
        expected_preview = self.root / "library/assets/fig-heatmap/热图 one.png"
        expected_code = self.root / "library/assets/fig-heatmap/plot code.R"
        self.assertEqual(Path(result["preview_path"]), expected_preview)
        self.assertEqual(Path(result["record"]["files"][0]["local_path"]), expected_code)
        self.assertEqual(result["record"]["source"]["name"], "Fixture source")
        self.assertEqual(result["record"]["code"], "# Archived example; do not execute\n")
        self.assertTrue(expected_preview.is_file())
        self.assertTrue(expected_code.is_file())

    def test_preview_path_traversal_is_rejected(self):
        self.sync()
        detail_path = self.root / "library/templates/fig-heatmap.json"
        detail = json.loads(detail_path.read_text(encoding="utf-8"))
        outside = self.work / "outside.png"
        outside.write_bytes(b"Unrelated private image")
        for path in ("/library/assets/../../../outside.png",
                     "/library/assets/%2e%2e/%2e%2e/%2e%2e/outside.png"):
            with self.subTest(path=path):
                detail["preview"] = path
                self.save_json(detail_path, detail)
                with self.assertRaises(plotbook.PlotbookError):
                    plotbook.show(self.root, "fig-heatmap")
                self.assertEqual(outside.read_bytes(), b"Unrelated private image")

    def test_companion_symlink_outside_library_is_rejected(self):
        self.sync()
        companion = self.root / "library/assets/fig-heatmap/plot code.R"
        outside = self.work / "outside.R"
        outside.write_text("Private unrelated source", encoding="utf-8")
        companion.unlink()
        try:
            companion.symlink_to(outside)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"Symbolic links unavailable: {error}")
        with self.assertRaises(plotbook.PlotbookError):
            plotbook.show(self.root, "fig-heatmap")
        self.assertTrue(companion.is_symlink())
        self.assertEqual(outside.read_text(), "Private unrelated source")


if __name__ == "__main__":
    unittest.main()
