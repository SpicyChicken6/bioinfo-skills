"""Behavior checks for the installed helper, without scientific dependencies."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "assets" / "biofolder.py"
METHODS_TEMPLATE = HELPER.with_name("task-methods.md")
LEAVES = ("code", "tests", "data/interim", "data/processed", "figures", "tables", "docs", "logs")


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="biofolder test ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "pixi.toml").write_text('[workspace]\nname = "test"\n')
        (self.root / "scripts").mkdir()
        self.helper = self.root / "scripts" / "biofolder.py"
        shutil.copyfile(HELPER, self.helper)

    def run_helper(self, *args, caller=None, success=True):
        env = dict(os.environ, PIXI_PROJECT_ROOT=str(self.root), INIT_CWD=str(caller or self.root))
        result = subprocess.run(
            [sys.executable, str(self.helper), *args], cwd=self.root, env=env,
            capture_output=True, text=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_module_has_no_number_and_normalizes_names(self):
        result = self.run_helper("module", "RNA Seq")
        module = self.root / "modules" / "rna-seq"
        self.assertTrue((module / "README.md").is_file())
        self.assertTrue((module / "tasks").is_dir())
        self.assertIn("modules/rna-seq", result.stdout)

    def test_existing_module_names_are_preserved_by_both_commands(self):
        for name in ("RNA_Seq", "RNA Seq", "RNA-SEQ"):
            with self.subTest(name=name):
                module = self.root / "modules" / name
                module.mkdir(parents=True)
                (module / "README.md").write_text("Existing module notes\n")
                self.run_helper("module", name)
                self.run_helper("task", name, "qc")
                self.assertTrue((module / "tasks/01-qc").is_dir())
                self.assertEqual((module / "README.md").read_text(), "Existing module notes\n")
                self.assertEqual(list((self.root / "modules").iterdir()), [module])
            shutil.rmtree(self.root / "modules")

    def test_unique_normalized_module_match_is_reused_by_both_commands(self):
        module = self.root / "modules/RNA_Seq"
        module.mkdir(parents=True)
        self.run_helper("module", "rna-seq")
        self.run_helper("task", "RNA Seq", "qc")
        self.assertTrue((module / "tasks/01-qc").is_dir())
        self.assertEqual(list((self.root / "modules").iterdir()), [module])

    def test_exact_module_name_wins_over_normalization_equivalents(self):
        names = ("RNA_Seq", "RNA Seq", "rna-seq")
        for name in names:
            (self.root / "modules" / name).mkdir(parents=True)
        for name in names:
            with self.subTest(name=name):
                self.run_helper("module", name)
                self.run_helper("task", name, "qc")
                self.assertTrue((self.root / "modules" / name / "tasks/01-qc").is_dir())

    def test_ambiguous_normalized_module_matches_fail_before_writes(self):
        for name in ("RNA_Seq", "RNA Seq"):
            (self.root / "modules" / name).mkdir(parents=True)
        before_files = self.snapshot()
        before_paths = set(self.root.rglob("*"))
        for args in (("module", "rna-seq"), ("task", "rna-seq", "qc")):
            with self.subTest(args=args):
                result = self.run_helper(*args, success=False)
                self.assertIn("Ambiguous module", result.stderr)
                self.assertEqual(self.snapshot(), before_files)
                self.assertEqual(set(self.root.rglob("*")), before_paths)

    def test_unrelated_non_sluggable_directories_do_not_break_module_lookup(self):
        for name in ("notes.v1", "!!!", "RNA_Seq"):
            (self.root / "modules" / name).mkdir(parents=True)
        self.run_helper("module", "rna-seq")
        self.run_helper("task", "RNA Seq", "qc")
        self.run_helper("task", "Protein Study", "qc")
        self.assertTrue((self.root / "modules/RNA_Seq/tasks/01-qc").is_dir())
        self.assertTrue((self.root / "modules/protein-study/tasks/01-qc").is_dir())
        self.assertFalse((self.root / "modules/rna-seq").exists())
        for name in ("notes.v1", "!!!"):
            self.assertEqual(list((self.root / "modules" / name).iterdir()), [])

    def test_root_task_creates_module_and_both_workspaces(self):
        self.run_helper("task", "transcriptomics", "Differential Expression")
        task = self.root / "modules/transcriptomics/tasks/01-differential-expression"
        self.assertTrue((task / "README.md").is_file())
        for owner in ("agent", "manual"):
            for leaf in LEAVES:
                self.assertTrue((task / owner / leaf / ".gitkeep").is_file())

    def test_installed_helper_creates_methods_from_template_and_readme_link(self):
        self.run_helper("task", "rna", "Differential Expression")
        task = self.root / "modules/rna/tasks/01-differential-expression"
        methods = task / "agent/docs/methods.md"
        expected = METHODS_TEMPLATE.read_text(encoding="utf-8").replace(
            "<task name>", "differential-expression", 1,
        )
        self.assertEqual(methods.read_text(encoding="utf-8"), expected)
        self.assertIn("[methods and run summaries](agent/docs/methods.md)",
                      (task / "README.md").read_text())
        self.assertFalse((task / "manual/docs/methods.md").exists())
        self.assertFalse((task / "agent/docs/review.md").exists())

    def test_module_inferred_from_original_cwd_not_pixi_task_cwd(self):
        self.run_helper("module", "rna")
        module = self.root / "modules/rna"
        self.run_helper("task", "qc", caller=module)
        self.run_helper("task", "enrichment", caller=module / "tasks/01-qc/manual/code")
        self.assertTrue((module / "tasks/02-enrichment").is_dir())
        self.assertTrue((module / "tasks/02-enrichment/agent/docs/methods.md").is_file())

    def test_numbering_uses_maximum_and_is_per_module(self):
        self.run_helper("task", "rna", "qc")
        tasks = self.root / "modules/rna/tasks"
        (tasks / "07-older").mkdir()
        (tasks / "notes").mkdir()
        self.run_helper("task", "rna", "de")
        self.run_helper("task", "protein", "qc")
        self.assertTrue((tasks / "08-de").is_dir())
        self.assertTrue((self.root / "modules/protein/tasks/01-qc").is_dir())
        (tasks / "100-older").mkdir()
        self.run_helper("task", "rna", "enrichment")
        self.assertTrue((tasks / "101-enrichment").is_dir())

    def test_repeat_calls_preserve_custom_files_and_existing_task_structure(self):
        self.run_helper("task", "rna", "qc")
        module = self.root / "modules/rna"
        task = module / "tasks/01-qc"
        (module / "README.md").write_text("Human module notes\n")
        (task / "README.md").write_text("Human task notes\n")
        (task / "agent/docs/methods.md").write_text("Recorded methods and unresolved caveats\n")
        (task / "manual/code/script.R").write_text("# Human code\n")
        shutil.rmtree(task / "agent/tests")
        before = self.snapshot()
        self.run_helper("module", "rna")
        result = self.run_helper("task", "rna", "qc")
        self.assertEqual(before, self.snapshot())
        self.assertFalse((task / "agent/tests").exists())
        self.assertIn("Existing:", result.stdout)

    def test_existing_task_without_methods_is_returned_unchanged(self):
        self.run_helper("task", "rna", "qc")
        task = self.root / "modules/rna/tasks/01-qc"
        (task / "agent/docs/methods.md").unlink()
        (task / "README.md").write_text("Existing task without methods\n")
        before = self.snapshot()
        result = self.run_helper("task", "rna", "qc")
        self.assertEqual(before, self.snapshot())
        self.assertIn("Existing:", result.stdout)

    def test_missing_module_context_gives_usage_without_creating_folders(self):
        result = self.run_helper("task", "qc", success=False)
        self.assertIn("<module> <task>", result.stderr)
        self.assertFalse((self.root / "modules").exists())

    def test_invalid_names_and_argument_counts_do_not_create_modules(self):
        for args in (("module", "../outside"), ("module", ""), ("task", "rna", "/tmp/outside"),
                     ("task", "rna", "qc", "extra")):
            with self.subTest(args=args):
                self.run_helper(*args, success=False)
                self.assertFalse((self.root / "modules").exists())

    def test_old_module_is_reused_by_full_name_and_inferred_cwd(self):
        module = self.root / "modules/01-RNA_Seq"
        module.mkdir(parents=True)
        self.run_helper("module", module.name)
        self.run_helper("task", module.name, "qc")
        self.run_helper("task", "de", caller=module)
        self.run_helper("task", "enrichment", caller=module / "tasks/02-de/manual/code")
        self.assertTrue((module / "tasks/02-de").is_dir())
        self.assertTrue((module / "tasks/03-enrichment").is_dir())
        self.assertEqual(list((self.root / "modules").iterdir()), [module])

    def test_numeric_module_prefix_is_never_treated_as_an_alias(self):
        for name in ("2024-rna", "24-rna", "01-rna"):
            with self.subTest(name=name):
                existing = self.root / "modules" / name
                existing.mkdir(parents=True)
                self.run_helper("module", "rna")
                self.run_helper("task", "rna", "qc")
                self.assertTrue((self.root / "modules/rna/tasks/01-qc").is_dir())
                self.assertEqual(list(existing.iterdir()), [])
                self.run_helper("task", name, "qc")
                self.assertTrue((existing / "tasks/01-qc").is_dir())
            shutil.rmtree(self.root / "modules")

    def test_symlinked_module_cannot_write_outside_project(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / "modules").mkdir()
            (self.root / "modules/rna").symlink_to(outside, target_is_directory=True)
            self.run_helper("task", "rna", "qc", success=False)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_file_collision_is_reported_without_overwriting(self):
        self.run_helper("module", "rna")
        path = self.root / "modules/rna/tasks/01-qc"
        path.write_text("Keep me")
        self.run_helper("task", "rna", "qc", success=False)
        self.assertEqual(path.read_text(), "Keep me")

    def test_direct_helper_supports_pyproject_manifest(self):
        (self.root / "pixi.toml").rename(self.root / "pyproject.toml")
        env = {key: value for key, value in os.environ.items() if key not in ("PIXI_PROJECT_ROOT", "INIT_CWD")}
        result = subprocess.run(
            [sys.executable, str(self.helper), "task", "rna", "qc"], cwd=self.root,
            env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "modules/rna").is_dir())
        self.assertTrue((self.root / "modules/rna/tasks/01-qc/agent/docs/methods.md").is_file())


if __name__ == "__main__":
    unittest.main()
