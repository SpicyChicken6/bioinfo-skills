"""Run allocation preserves task history without executing an analysis."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "assets" / "biofolder.py"
RUN_OUTPUTS = ("figures", "tables", "logs", "docs/runs")
WORKSPACE_DIRS = (
    "code", "tests", "data/interim", "data/processed", "figures", "tables", "docs", "logs",
)


class RunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="biofolder run test ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "pixi.toml").write_text('[workspace]\nname = "test"\n')
        (self.root / "scripts").mkdir()
        self.helper = self.root / "scripts/biofolder.py"
        shutil.copyfile(HELPER, self.helper)

    def create_task(self, module="rna", name="01-qc"):
        task = self.root / "modules" / module / "tasks" / name
        task.mkdir(parents=True)
        (task / "README.md").write_text("Existing scientific task\n")
        for owner in ("agent", "manual"):
            for category in WORKSPACE_DIRS:
                (task / owner / category).mkdir(parents=True, exist_ok=True)
        return task

    def command(self, *args, caller=None):
        return dict(
            args=[sys.executable, str(self.helper), "run", *args],
            cwd=self.root,
            env=dict(os.environ, PIXI_PROJECT_ROOT=str(self.root), INIT_CWD=str(caller or self.root)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def run_helper(self, *args, caller=None, success=True):
        result = subprocess.run(**self.command(*args, caller=caller))
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def snapshot(self):
        """Capture paths and contents without reading through symbolic links."""
        result = {}
        for directory, dirs, files in os.walk(self.root, followlinks=False):
            for name in dirs + files:
                path = Path(directory) / name
                key = path.relative_to(self.root).as_posix()
                if path.is_symlink():
                    result[key] = ("symlink", os.readlink(path))
                elif path.is_dir():
                    result[key] = ("directory", None)
                else:
                    result[key] = ("file", path.read_bytes())
        return result

    def assert_run(self, task, run_id):
        for category in RUN_OUTPUTS:
            path = task / "agent" / category / run_id
            self.assertTrue(path.is_dir(), str(path))
            self.assertEqual(list(path.iterdir()), [path / ".gitkeep"])
            self.assertEqual((path / ".gitkeep").read_bytes(), b"")

    def test_root_allocation_only_adds_run_folders_and_preserves_existing_content(self):
        task = self.create_task()
        for relative in (
            "agent/docs/methods.md", "agent/docs/review.md", "manual/code/analysis.R",
            "manual/figures/plot.svg", "agent/figures/legacy.svg", "agent/tables/legacy.csv",
        ):
            (task / relative).write_text(f"Preserve {relative}\n")
        before = self.snapshot()
        result = self.run_helper("rna", "01-qc")
        self.assert_run(task, "run-001")
        self.assertEqual(
            result.stdout.strip(),
            "Created: modules/rna/tasks/01-qc/agent/docs/runs/run-001",
        )
        after = self.snapshot()
        self.assertEqual(before, {path: after[path] for path in before})
        prefix = task.relative_to(self.root).as_posix() + "/agent/"
        expected = {prefix + "docs/runs"}
        for category in RUN_OUTPUTS:
            expected.update((prefix + category + "/run-001", prefix + category + "/run-001/.gitkeep"))
        self.assertEqual(set(after) - set(before), expected)

    def test_original_cwd_resolves_module_task_and_descendant(self):
        task = self.create_task(module="RNA_Seq")
        self.run_helper("qc", caller=task.parents[1])
        self.run_helper(caller=task)
        self.run_helper(caller=task / "manual/code")
        self.assert_run(task, "run-001")
        self.assert_run(task, "run-002")
        self.assert_run(task, "run-003")
        self.assertFalse((self.root / "modules/rna-seq").exists())

    def test_exact_module_name_wins_and_unique_normalized_name_is_reused(self):
        exact = self.create_task(module="RNA_Seq")
        self.run_helper("rna-seq", "qc")
        other = self.create_task(module="RNA Seq")
        self.run_helper("RNA Seq", "01-qc")
        self.assert_run(exact, "run-001")
        self.assert_run(other, "run-001")
        before = self.snapshot()
        self.run_helper("rna-seq", "qc", success=False)
        self.assertEqual(before, self.snapshot())

    def test_exact_task_name_disambiguates_duplicate_slugs(self):
        first = self.create_task(name="01-qc")
        second = self.create_task(name="02-qc")
        before = self.snapshot()
        self.run_helper("rna", "qc", success=False)
        self.assertEqual(before, self.snapshot())
        self.run_helper("rna", "02-qc")
        self.assert_run(second, "run-001")
        self.assertFalse((first / "agent/docs/runs").exists())

    def test_invalid_missing_and_ambiguous_context_never_scaffold(self):
        task = self.create_task()
        cases = (
            ((), self.root),
            ((), task.parents[1]),
            (("qc",), self.root),
            (("missing", "qc"), self.root),
            (("rna", "missing"), self.root),
            (("rna", "qc", "extra"), self.root),
            (("../rna", "qc"), self.root),
            (("rna", "../01-qc"), self.root),
            (("rna", str(task)), self.root),
            (("rna", ""), self.root),
        )
        before = self.snapshot()
        for args, caller in cases:
            with self.subTest(args=args, caller=caller):
                self.run_helper(*args, caller=caller, success=False)
                self.assertEqual(before, self.snapshot())

    def test_maximum_run_number_is_shared_across_categories_and_task_local(self):
        categories = (
            "code", "figures", "tables", "logs", "data/interim", "data/processed",
            "docs/runs", "results",
        )
        for index, category in enumerate(categories, start=1):
            with self.subTest(category=category):
                task = self.create_task(name=f"{index:02d}-analysis")
                (task / "agent" / category / "run-007").mkdir(parents=True)
                (task / "agent/figures/run-002").mkdir()
                (task / "agent/figures/run-999-old").mkdir()
                (task / "agent/figures/run-final").mkdir()
                self.run_helper("rna", task.name)
                self.assert_run(task, "run-008")
                self.assertFalse((task / "agent/docs/runs/run-003").exists())
        fresh = self.create_task(name="20-new")
        self.run_helper("rna", fresh.name)
        self.assert_run(fresh, "run-001")

    def test_run_number_width_expands_after_999(self):
        task = self.create_task()
        (task / "agent/tables/run-999").mkdir()
        self.run_helper("rna", "qc")
        self.assert_run(task, "run-1000")

    def test_run_named_file_or_symlink_is_occupied_without_following_it(self):
        task = self.create_task()
        (task / "agent/figures/run-005").write_text("Prior run output\n")
        with tempfile.TemporaryDirectory() as outside:
            outside_path = Path(outside)
            (outside_path / "run-999").mkdir()
            (task / "agent/tables/run-006").symlink_to(outside_path, target_is_directory=True)
            (task / "agent/logs/run-007").symlink_to(outside_path / "missing")
            self.run_helper("rna", "qc")
            self.assert_run(task, "run-008")
            self.assertEqual(list(outside_path.iterdir()), [outside_path / "run-999"])
            self.assertEqual((task / "agent/figures/run-005").read_text(), "Prior run output\n")
            self.assertTrue((task / "agent/logs/run-007").is_symlink())

    def test_symlinked_ancestors_cannot_receive_run_outputs(self):
        task = self.create_task()
        paths = (
            self.root / "modules", task.parents[1], task.parent, task,
            task / "agent", task / "agent/figures", task / "agent/tables",
            task / "agent/logs", task / "agent/docs", task / "agent/docs/runs",
            task / "agent/data", task / "agent/data/interim", task / "agent/code",
        )
        with tempfile.TemporaryDirectory() as outside:
            outside_path = Path(outside)
            for path in paths:
                with self.subTest(path=path):
                    backup = path.with_name(path.name + "-saved")
                    existed = path.exists()
                    if existed:
                        path.rename(backup)
                    path.symlink_to(outside_path, target_is_directory=True)
                    before = self.snapshot()
                    try:
                        self.run_helper("rna", "01-qc", success=False)
                        self.assertEqual(list(outside_path.iterdir()), [])
                        self.assertEqual(before, self.snapshot())
                    finally:
                        path.unlink()
                        if existed:
                            backup.rename(path)

    def test_non_directory_ancestors_are_rejected_before_reservation(self):
        task = self.create_task()
        for path in (task / "agent/figures", task / "agent/docs/runs", task / "agent/data"):
            with self.subTest(path=path):
                backup = path.with_name(path.name + "-saved")
                existed = path.exists()
                if existed:
                    path.rename(backup)
                path.write_text("Existing file\n")
                before = self.snapshot()
                try:
                    self.run_helper("rna", "qc", success=False)
                    self.assertEqual(before, self.snapshot())
                finally:
                    path.unlink()
                    if existed:
                        backup.rename(path)

    def test_concurrent_allocations_create_complete_distinct_runs(self):
        task = self.create_task()
        processes = [subprocess.Popen(**self.command("rna", "qc")) for _ in range(6)]
        results = []
        try:
            for process in processes:
                stdout, stderr = process.communicate(timeout=30)
                results.append((process.returncode, stdout, stderr))
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                    process.communicate()
        for returncode, stdout, stderr in results:
            self.assertEqual(returncode, 0, stderr)
        outputs = {stdout.strip() for _, stdout, _ in results}
        self.assertEqual(len(outputs), 6)
        run_ids = {f"run-{index:03d}" for index in range(1, 7)}
        for category in RUN_OUTPUTS:
            actual = {path.name for path in (task / "agent" / category).iterdir() if path.name.startswith("run-")}
            self.assertEqual(actual, run_ids)
        for run_id in run_ids:
            self.assert_run(task, run_id)


if __name__ == "__main__":
    unittest.main()
