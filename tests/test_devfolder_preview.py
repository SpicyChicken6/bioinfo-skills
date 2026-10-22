"""Exercise the preview writer template without installing Research Flow."""
import ast
import os
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "devfolder/assets/preview_workflow.py"
WRITER = next(node for node in ast.parse(SCRIPT.read_text(encoding="utf-8")).body
              if isinstance(node, ast.FunctionDef) and node.name == "write_preview")
CODE = compile(ast.Module(body=[WRITER], type_ignores=[]), str(SCRIPT), "exec")
MARKER = b"<!-- development-workflow-preview -->\n"


class PreviewWriterTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / "workflow-preview.html"
        # Exercise the fallback even on systems that provide these flags.
        self.os = SimpleNamespace(**{
            name: getattr(os, name) for name in dir(os)
            if name not in {"O_NOFOLLOW", "O_NONBLOCK"}
        })
        namespace = {"os": self.os, "stat": stat, "tempfile": tempfile, "MARKER": MARKER}
        exec(CODE, namespace)
        self.write_preview = namespace["write_preview"]

    def symlink(self, link, target):
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"Symbolic links unavailable: {error}")

    def test_create_and_repeat_shorter_unicode_without_optional_flags(self):
        for content in ("First preview " * 30, "研究\nPreview 🌱", "短"):
            self.write_preview(self.path, content)
            self.assertEqual(self.path.read_bytes(), MARKER + content.encode("utf-8"))

    def test_unowned_and_wrong_marker_files_are_unchanged(self):
        for original in (b"An unrelated document", b"<!-- another workflow -->\nOriginal"):
            with self.subTest(original=original):
                self.path.write_bytes(original)
                with self.assertRaises(FileExistsError):
                    self.write_preview(self.path, "Replacement")
                self.assertEqual(self.path.read_bytes(), original)

    def test_symlink_to_marked_file_is_preserved(self):
        target = self.root / "target.html"
        original = MARKER + b"Target content"
        target.write_bytes(original)
        self.symlink(self.path, target)
        with self.assertRaises(OSError):
            self.write_preview(self.path, "Replacement")
        self.assertTrue(self.path.is_symlink())
        self.assertEqual(target.read_bytes(), original)

    def test_dangling_symlink_does_not_create_target(self):
        target = self.root / "missing.html"
        self.symlink(self.path, target)
        with self.assertRaises(OSError):
            self.write_preview(self.path, "Replacement")
        self.assertTrue(self.path.is_symlink())
        self.assertFalse(target.exists())

    def test_hardlinked_marked_file_is_preserved(self):
        target = self.root / "target.html"
        original = MARKER + b"Target content"
        target.write_bytes(original)
        try:
            os.link(target, self.path)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"Hard links unavailable: {error}")
        with self.assertRaises(OSError):
            self.write_preview(self.path, "Replacement")
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(target.read_bytes(), original)

    def test_directory_is_preserved(self):
        self.path.mkdir()
        child = self.path / "personal.txt"
        child.write_bytes(b"Personal content")
        with self.assertRaises(OSError):
            self.write_preview(self.path, "Replacement")
        self.assertEqual(child.read_bytes(), b"Personal content")

    def test_dangling_symlink_created_during_publication_is_preserved(self):
        target = self.root / "missing.html"

        def racing_link(source, destination):
            self.symlink(self.path, target)
            return os.link(source, destination)

        self.os.link = racing_link
        with self.assertRaises(OSError):
            self.write_preview(self.path, "Must not be published")
        self.assertTrue(self.path.is_symlink())
        self.assertFalse(target.exists())
        self.assertEqual(list(self.root.iterdir()), [self.path])

    def test_publication_failure_cleans_temporary_file(self):
        def unsupported_link(*args):
            raise OSError("Filesystem does not support hard links")

        self.os.link = unsupported_link
        with self.assertRaises(OSError):
            self.write_preview(self.path, "Must not be published")
        self.assertEqual(list(self.root.iterdir()), [])

    def check_open_race(self, use_symlink):
        original = MARKER + b"Original preview"
        replacement = MARKER + b"Different marked preview"
        self.path.write_bytes(original)
        target = self.root / "replacement.html"
        target.write_bytes(replacement)
        backup = self.root / "original.html"

        def replacing_open(path, flags, *args, **kwargs):
            if not flags & os.O_EXCL:
                self.path.rename(backup)
                if use_symlink:
                    self.symlink(self.path, target)
                else:
                    target.rename(self.path)
            return os.open(path, flags, *args, **kwargs)

        self.os.open = replacing_open
        with self.assertRaises(OSError):
            self.write_preview(self.path, "Must not be written")
        self.assertEqual(backup.read_bytes(), original)
        self.assertEqual(self.path.read_bytes(), replacement)
        if use_symlink:
            self.assertTrue(self.path.is_symlink())
            self.assertEqual(target.read_bytes(), replacement)

    def test_replacement_between_lstat_and_open_is_preserved(self):
        self.check_open_race(use_symlink=False)

    def test_symlink_swap_between_lstat_and_open_is_preserved(self):
        self.check_open_race(use_symlink=True)

    def test_unavailable_file_identity_refuses_refresh(self):
        original = MARKER + b"Original preview"
        self.path.write_bytes(original)

        def unidentified_fstat(fd):
            info = os.fstat(fd)
            values = {name: getattr(info, name) for name in dir(info) if name.startswith("st_")}
            return SimpleNamespace(**{**values, "st_ino": 0})

        self.os.fstat = unidentified_fstat
        with self.assertRaises(FileExistsError):
            self.write_preview(self.path, "Replacement")
        self.assertEqual(self.path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
