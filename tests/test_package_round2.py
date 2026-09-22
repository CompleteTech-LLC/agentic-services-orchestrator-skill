"""Additional cross-platform library regression cases."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from test_package_library import library


class RoundTwoTests(unittest.TestCase):
    def test_powershell_is_literal_and_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "client's $data"
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(library.main(["plan", "--shell", "powershell", "--destination", str(target)]), 0)
            self.assertIn("client''s $data", output.getvalue())
            self.assertIn("New-Item", output.getvalue())
            self.assertFalse(target.exists())

    def test_control_characters_rejected(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(library.main(["plan", "--destination", "bad\ncommand"]), 1)

    def test_mismatched_install_key_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            path.write_text(json.dumps(dict(schema_version=1, family=library.FAMILY, members=[dict(repository="CompleteTech-LLC/other", skill_name="demo", role="demo", private=False)])), encoding="utf-8")
            with self.assertRaises(ValueError):
                library.load_members(path)

    def test_all_shared_files_declared(self):
        for path in ("BRANDING.md", "AGENTS.md", ".editorconfig", ".github/PULL_REQUEST_TEMPLATE.md"):
            self.assertIn(path, library.SHARED)


if __name__ == "__main__":
    unittest.main()
