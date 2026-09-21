"""Exercise result uploads against rclone's local backend; never contact a cloud."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "assets" / "biofolder.py"
RCLONE = shutil.which("rclone")


@unittest.skipUnless(RCLONE, "rclone is required for local-backend sync checks")
class SyncResultsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="biofolder sync test ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "project"
        (self.root / "scripts").mkdir(parents=True)
        (self.root / "pixi.toml").write_text('[workspace]\nname = "test"\n')
        self.helper = self.root / "scripts/biofolder.py"
        shutil.copyfile(HELPER, self.helper)
        self.config = self.base / "rclone.conf"
        self.config.write_text("[test-drive]\ntype = local\n")
        self.destination = self.base / "cloud results"
        self.env = {
            key: value for key, value in os.environ.items()
            if not key.startswith("RCLONE_")
        }
        self.env.update(
            PIXI_PROJECT_ROOT=str(self.root), INIT_CWD=str(self.root),
            RCLONE_CONFIG=str(self.config),
        )
        # Ensure the helper can find the exact installed rclone checked above.
        self.env["PATH"] = str(Path(RCLONE).parent) + os.pathsep + self.env.get("PATH", "")

    def write_source(self, relative, text="result\n"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run_helper(self, *args, success=True, caller=None):
        env = dict(self.env, INIT_CWD=str(caller or self.root))
        result = subprocess.run(
            [sys.executable, str(self.helper), "sync-results", *args],
            cwd=self.root, env=env, capture_output=True, text=True, timeout=30,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def sync(self, *args, **kwargs):
        return self.run_helper(
            "--remote", "test-drive", "--destination", str(self.destination),
            *args, **kwargs,
        )

    def destination_files(self):
        return {
            path.relative_to(self.destination).as_posix(): path.read_bytes()
            for path in self.destination.rglob("*") if path.is_file()
        }

    def project_snapshot(self):
        return {
            path.relative_to(self.root).as_posix(): path.read_bytes() if path.is_file() else None
            for path in self.root.rglob("*")
        }

    def test_default_and_explicit_preview_leave_destination_absent(self):
        self.write_source("modules/rna/tasks/01-de/manual/results/contrast.csv")
        before = self.project_snapshot()
        for mode in ((), ("--dry-run",)):
            with self.subTest(mode=mode):
                self.sync(*mode)
                self.assertFalse(self.destination.exists())
                self.assertEqual(self.project_snapshot(), before)

    def test_upload_only_manual_outputs_with_complete_project_paths(self):
        expected = {
            "modules/01-bulk-rnaseq/tasks/01-de/manual/results/volcano/tables/effects.csv": b"effect\n",
            "modules/01-bulk-rnaseq/tasks/02-gsva/manual/figures/pathway plot.png": b"plot\n",
            "modules/atac/tasks/01-peaks/manual/tables/peaks.tsv": b"peak\n",
        }
        for relative, data in expected.items():
            self.write_source(relative, data.decode())
        excluded = (
            "modules/01-bulk-rnaseq/tasks/01-de/agent/results/private.csv",
            "modules/01-bulk-rnaseq/tasks/01-de/agent/figures/private.png",
            "modules/01-bulk-rnaseq/tasks/01-de/agent/tables/private.csv",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/data/processed/counts.csv",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/code/analysis.R",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/logs/run.log",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/docs/report.md",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/results/.gitkeep",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/results/.DS_Store",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/results/.ipynb_checkpoints/analysis.ipynb",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/results/nested/.gitkeep",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/results/nested/.DS_Store",
            "modules/01-bulk-rnaseq/tasks/01-de/manual/results/nested/.ipynb_checkpoints/analysis.ipynb",
            "modules/01-bulk-rnaseq/manual/results/outside-task.csv",
            "data/processed/results/outside-module.csv",
        )
        for relative in excluded:
            self.write_source(relative, "excluded\n")
        self.sync("--upload")
        self.assertEqual(self.destination_files(), expected)

    def test_repeated_upload_preserves_destination_only_files(self):
        relative = "modules/rna/tasks/01-de/manual/tables/effects.csv"
        self.write_source(relative, "effect\n")
        self.destination.mkdir()
        (self.destination / "keep-on-cloud.txt").write_text("remote notes\n")
        expected = {relative: b"effect\n", "keep-on-cloud.txt": b"remote notes\n"}
        self.sync("--upload")
        self.assertEqual(self.destination_files(), expected)
        self.sync("--upload")
        self.assertEqual(self.destination_files(), expected)

    def test_checksum_detects_change_with_same_size_and_mtime(self):
        relative = "modules/rna/tasks/01-de/manual/tables/effects.csv"
        source = self.write_source(relative, "before\n")
        original_stat = source.stat()
        self.sync("--upload")
        source.write_text("after!\n")
        os.utime(source, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
        self.assertEqual(source.stat().st_size, original_stat.st_size)
        self.assertEqual(source.stat().st_mtime_ns, original_stat.st_mtime_ns)
        self.sync("--upload")
        self.assertEqual((self.destination / relative).read_text(), "after!\n")

    def test_module_filter_preserves_path_and_accepts_normalized_name(self):
        selected = "modules/RNA_Seq/tasks/01-de/manual/tables/effects.csv"
        self.write_source(selected)
        self.write_source("modules/atac/tasks/01-peaks/manual/results/peaks.csv")
        self.sync("--module", "rna-seq", "--upload")
        self.assertEqual(self.destination_files(), {selected: b"result\n"})

    def test_exact_module_name_wins_when_normalized_names_are_ambiguous(self):
        selected = "modules/RNA_Seq/tasks/01-de/manual/tables/effects.csv"
        self.write_source(selected)
        self.write_source("modules/RNA Seq/tasks/01-de/manual/tables/effects.csv", "other\n")
        self.sync("--module", "RNA_Seq", "--upload")
        self.assertEqual(self.destination_files(), {selected: b"result\n"})

    def test_default_scope_is_all_modules_even_when_called_inside_one(self):
        expected = {}
        for module in ("rna", "atac"):
            relative = f"modules/{module}/tasks/01-analysis/manual/tables/results.csv"
            self.write_source(relative)
            expected[relative] = b"result\n"
        self.sync("--upload", caller=self.root / "modules/rna/tasks/01-analysis/manual")
        self.assertEqual(self.destination_files(), expected)

    def test_unknown_or_ambiguous_module_fails_without_scaffolding(self):
        for module in ("RNA_Seq", "RNA Seq"):
            self.write_source(f"modules/{module}/tasks/01-de/manual/tables/effects.csv")
        before = self.project_snapshot()
        for module in ("missing", "rna-seq", "../outside"):
            with self.subTest(module=module):
                self.sync("--module", module, "--upload", success=False)
                self.assertEqual(self.project_snapshot(), before)
                self.assertFalse(self.destination.exists())

    def test_invalid_arguments_do_not_write(self):
        self.write_source("modules/rna/tasks/01-de/manual/results/contrast.csv")
        before = self.project_snapshot()
        destination = str(self.destination)
        cases = (
            (),
            ("--remote", "test-drive"),
            ("--destination", destination),
            ("--remote", "", "--destination", destination),
            ("--remote", "test-drive", "--destination", ""),
            ("--remote", "test-drive:/path", "--destination", destination),
            ("--remote", "test-drive", "--destination", destination, "--dry-run", "--upload"),
        )
        for args in cases:
            with self.subTest(args=args):
                self.run_helper(*args, success=False)
                self.assertFalse(self.destination.exists())
                self.assertEqual(self.project_snapshot(), before)

    def test_unconfigured_remote_fails_without_writes(self):
        self.write_source("modules/rna/tasks/01-de/manual/results/contrast.csv")
        before = self.project_snapshot()
        self.run_helper(
            "--remote", "missing-drive", "--destination", str(self.destination),
            "--upload", success=False,
        )
        self.assertFalse(self.destination.exists())
        self.assertEqual(self.project_snapshot(), before)

    def test_file_and_nested_directory_symlinks_are_not_uploaded(self):
        relative = "modules/rna/tasks/01-de/manual/results/contrast.csv"
        source = self.write_source(relative)
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "private.csv").write_text("private\n")
        results = source.parent
        (results / "linked-file.csv").symlink_to(outside / "private.csv")
        (results / "linked-directory").symlink_to(outside, target_is_directory=True)
        (results / "linked-result.csv").symlink_to(source)
        (results / "broken.csv").symlink_to(outside / "missing.csv")
        self.sync("--upload")
        self.assertEqual(self.destination_files(), {relative: b"result\n"})

    def test_symlinked_scope_directories_never_upload_their_contents(self):
        cases = (
            ("modules", "rna/tasks/01-de/manual/results/private.csv"),
            ("modules/rna", "tasks/01-de/manual/results/private.csv"),
            ("modules/rna/tasks", "01-de/manual/results/private.csv"),
            ("modules/rna/tasks/01-de", "manual/results/private.csv"),
            ("modules/rna/tasks/01-de/manual", "results/private.csv"),
            ("modules/rna/tasks/01-de/manual/results", "private.csv"),
        )
        for index, (link_relative, outside_relative) in enumerate(cases):
            with self.subTest(link=link_relative):
                outside = self.base / f"outside-{index}"
                private = outside / outside_relative
                private.parent.mkdir(parents=True)
                private.write_text("private\n")
                link = self.root / link_relative
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(outside, target_is_directory=True)
                # A clear refusal and a safe skip are both acceptable here.
                subprocess.run(
                    [sys.executable, str(self.helper), "sync-results", "--remote", "test-drive",
                     "--destination", str(self.destination), "--upload"],
                    cwd=self.root, env=self.env, capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(self.destination_files(), {})
                self.assertEqual(private.read_text(), "private\n")
                link.unlink()
                if (self.root / "modules").exists():
                    shutil.rmtree(self.root / "modules")


if __name__ == "__main__":
    unittest.main()
