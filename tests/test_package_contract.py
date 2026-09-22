"""Offline regression tests for the shared package contract, using synthetic files."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "validate_package.py"
SPEC = importlib.util.spec_from_file_location("validate_package", MODULE)
assert SPEC is not None and SPEC.loader is not None
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


class PackageContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "checkout"
        self.root.mkdir()
        self.manifest = dict(schema_version=1, family=package.FAMILY,
                             repository="CompleteTech-LLC/example-skill", skill_name="example-skill",
                             kind="catalog-renderer", entrypoints=["scripts/render.py"],
                             example_inputs=["examples/input.md"], network_mode="local", private=False)
        for value in (*package.FILES, "scripts/render.py", "examples/input.md"):
            path = self.root / value
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("demo\n", encoding="utf-8")
        (self.root / "SKILL.md").write_text("---\nname: example-skill\ndescription: Demo\n---\n", encoding="utf-8")
        (self.root / "README.md").write_text("\n".join(package.NAVIGATION), encoding="utf-8")
        (self.root / "assets").mkdir()
        (self.root / "assets/logo.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        self.save()

    def save(self):
        (self.root / "skill-package.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_valid(self):
        self.assertEqual(package.validate(self.root), [])

    def test_ledger_repository_name_differs_from_install_name(self):
        self.manifest.update(repository="CompleteTech-LLC/ai-usage-ledger-skill", skill_name="ai-usage-ledger", kind="usage-ledger", network_mode="operator-selected-hosts")
        (self.root / "SKILL.md").write_text("---\nname: ai-usage-ledger\n---\n", encoding="utf-8")
        self.save()
        self.assertEqual(package.validate(self.root), [])

    def test_schema_rejects_bad_types_and_unknown_values(self):
        for key, value in (("schema_version", True), ("family", "other"), ("kind", []), ("network_mode", {}), ("private", "false"), ("repository", "other/example"), ("skill_name", "../example"), ("entrypoints", []), ("example_inputs", "input.md")):
            with self.subTest(key=key):
                original = self.manifest[key]
                self.manifest[key] = value
                self.save()
                self.assertTrue(package.validate(self.root))
                self.manifest[key] = original
        self.save()

    def test_unknown_and_missing_fields(self):
        self.manifest["typo"] = True
        del self.manifest["private"]
        self.save()
        self.assertTrue(package.validate(self.root))

    def test_duplicate_json_keys(self):
        (self.root / "skill-package.json").write_text('{"family":"a","family":"b"}', encoding="utf-8")
        self.assertIn("duplicate JSON key", package.validate(self.root)[0])

    def test_invalid_or_non_object_json(self):
        for text in ("{", "[]", "null"):
            (self.root / "skill-package.json").write_text(text, encoding="utf-8")
            self.assertTrue(package.validate(self.root))

    def test_unsafe_and_missing_paths(self):
        for value in ("../outside", "/tmp/outside", "C:/outside", "scripts\\render.py", "missing.py", None, {}, ""):
            with self.subTest(path=value):
                self.manifest["entrypoints"] = [value]
                self.save()
                self.assertTrue(package.validate(self.root))

    def test_duplicate_paths(self):
        self.manifest["entrypoints"] *= 2
        self.save()
        self.assertTrue(package.validate(self.root))

    def test_symlink_escape(self):
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("private", encoding="utf-8")
        path = self.root / "scripts/render.py"
        path.unlink()
        try:
            path.symlink_to(outside)
        except OSError as exc:
            self.skipTest(str(exc))
        self.assertTrue(package.validate(self.root))

    def test_missing_brand_asset_and_invalid_png(self):
        logo = self.root / "assets/logo.png"
        logo.write_text("not an image", encoding="utf-8")
        self.assertTrue(package.validate(self.root))
        logo.unlink()
        self.assertTrue(package.validate(self.root))

    def test_frontmatter_mismatch(self):
        (self.root / "SKILL.md").write_text("---\nname: another-skill\n---\n", encoding="utf-8")
        self.assertTrue(package.validate(self.root))

    def test_quoted_frontmatter_and_crlf(self):
        (self.root / "SKILL.md").write_bytes(b'---\r\nname: "example-skill"\r\n---\r\n')
        self.assertEqual(package.validate(self.root), [])

    def test_missing_navigation(self):
        (self.root / "README.md").write_text("demo", encoding="utf-8")
        self.assertTrue(package.validate(self.root))

    def test_broken_onboarding_link(self):
        (self.root / "ONBOARDING.md").write_text("[Missing](missing.md)", encoding="utf-8")
        self.assertTrue(package.validate(self.root))

    def test_valid_local_external_and_anchor_links(self):
        (self.root / "ONBOARDING.md").write_text("[Readme](README.md#demo) [Web](https://example.com) [Here](#demo)", encoding="utf-8")
        self.assertEqual(package.validate(self.root), [])

    def test_never_executes_declared_entrypoints(self):
        (self.root / "scripts/render.py").write_text("raise RuntimeError('must not execute')", encoding="utf-8")
        self.assertEqual(package.validate(self.root), [])


if __name__ == "__main__":
    unittest.main()
