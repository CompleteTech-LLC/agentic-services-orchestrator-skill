"""Offline tests for library selection and non-executing installation plans."""
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import struct
import zlib
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
with patch.object(sys, "path", [str(ROOT / "scripts"), *sys.path]):
    spec = importlib.util.spec_from_file_location("skill_library", ROOT / "scripts/skill_library.py")
    assert spec is not None and spec.loader is not None
    library = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(library)


def png_fixture() -> bytes:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00")) + chunk(b"IEND", b""))


class SkillLibraryTests(unittest.TestCase):
    def test_public_default_and_private_opt_in(self):
        path = ROOT / "references/skill-library.json"
        public = library.load_members(path)
        self.assertEqual(len(public), 12)
        self.assertTrue(all(not member["private"] for member in public))
        self.assertEqual(len(library.load_members(path, True)), 13)

    def test_correct_ledger_install_directory(self):
        members = library.load_members(ROOT / "references/skill-library.json")
        plans = library.install_plan(members, Path("skills"))
        ledger = next(line for line in plans if "ai-usage-ledger-skill.git" in line)
        self.assertTrue(ledger.endswith("skills/ai-usage-ledger"))

    def test_plan_quotes_spaces_and_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "not created"
            with redirect_stdout(io.StringIO()) as output:
                result = library.main(["plan", "--destination", str(destination)])
            self.assertEqual(result, 0)
            self.assertFalse(destination.exists())
            self.assertIn("'" + str(destination), output.getvalue())
            self.assertNotIn("agentic-certificate-skill.git", output.getvalue())

    def test_duplicate_and_unsafe_catalog_entries(self):
        members = library.load_members(ROOT / "references/skill-library.json")
        for changes in (members + [members[0]], [{**members[0], "skill_name": "../escape"}], [{**members[0], "private": "false"}]):
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "catalog.json"
                path.write_text(json.dumps(dict(schema_version=1, family=library.FAMILY, members=changes)))
                with self.assertRaises(ValueError):
                    library.load_members(path)

    def test_valid_checkout_and_shared_drift(self):
        member = library.load_members(ROOT / "references/skill-library.json")[0]
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            checkout = workspace / member["skill_name"]
            manifest = dict(schema_version=1, family=library.FAMILY,
                            repository=member["repository"], skill_name=member["skill_name"],
                            private=member["private"], kind="usage-ledger", network_mode="operator-selected-hosts",
                            entrypoints=["scripts/entry.py"], example_inputs=["examples/input.md"])
            for relative in ("README.md", "SKILL.md", "LICENSE", "BRAND_ASSETS.md", "ONBOARDING.md", "requirements.txt", "agents/openai.yaml", "scripts/entry.py", "examples/input.md"):
                target = checkout / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("demo", encoding="utf-8")
            for relative in library.SHARED:
                target = checkout / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, target)
            (checkout / "README.md").write_text("CompleteTech LLC Skills [Start here](ONBOARDING.md) [Contributing](CONTRIBUTING.md) assets/logo.png", encoding="utf-8")
            (checkout / "SKILL.md").write_text("---\nname: ai-usage-ledger\n---\n", encoding="utf-8")
            (checkout / "assets").mkdir()
            (checkout / "assets/logo.png").write_bytes(png_fixture())
            (checkout / "skill-package.json").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(library.audit([member], workspace), [])
            (checkout / "CONTRIBUTING.md").write_text("drift", encoding="utf-8")
            self.assertEqual(library.audit([member], workspace), ["ai-usage-ledger: shared contract drift: CONTRIBUTING.md"])

    def test_duplicate_catalog_visibility_keys_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            path.write_text('{"schema_version":1,"family":"completetech-skills","members":[{"repository":"CompleteTech-LLC/demo","skill_name":"demo","role":"demo","private":true,"private":false}]}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                library.load_members(path)

    def test_missing_checkouts_fail_audit(self):
        members = library.load_members(ROOT / "references/skill-library.json")
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(len(library.audit(members, Path(tmp))), 12)


if __name__ == "__main__":
    unittest.main()
