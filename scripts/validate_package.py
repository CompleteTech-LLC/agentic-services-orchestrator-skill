#!/usr/bin/env python3
"""Validate the CompleteTech LLC Skills checkout contract; no execution or network."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FAMILY = "completetech-skills"
FIELDS = {"schema_version", "family", "repository", "skill_name", "kind", "entrypoints", "example_inputs", "network_mode", "private"}
FILES = ("README.md", "SKILL.md", "LICENSE", "BRAND_ASSETS.md", "ONBOARDING.md", "CONTRIBUTING.md", "requirements.txt", "agents/openai.yaml")
KINDS = {"catalog-renderer", "config-generator", "orchestrator", "usage-ledger"}
NETWORK_MODES = {"local", "operator-selected-hosts", "optional-receipts"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
NAVIGATION = ("CompleteTech LLC Skills", "[Start here](ONBOARDING.md)", "[Contributing](CONTRIBUTING.md)", "assets/logo.png")


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def local_file(root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"expected a relative POSIX file path: {value!r}")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or value.startswith("."):
        raise ValueError(f"unsafe package path: {value!r}")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"package path escapes checkout: {value!r}")
    if not resolved.is_file():
        raise ValueError(f"missing package file: {value}")
    return resolved


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    try:
        manifest_path = local_file(root, "skill-package.json")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"manifest: {exc}"]
    if not isinstance(manifest, dict):
        return ["manifest must be a JSON object"]
    if set(manifest) != FIELDS:
        errors.append(f"manifest fields mismatch: missing={sorted(FIELDS - set(manifest))}, unknown={sorted(set(manifest) - FIELDS)}")
    if type(manifest.get("schema_version")) is not int or manifest.get("schema_version") != 1:
        errors.append("schema_version must be integer 1")
    if manifest.get("family") != FAMILY:
        errors.append(f"family must be {FAMILY}")
    name = manifest.get("skill_name")
    if not isinstance(name, str) or not SLUG.fullmatch(name) or len(name) > 64:
        errors.append("skill_name must be a lowercase hyphenated slug of at most 64 characters")
    repo = manifest.get("repository")
    if not isinstance(repo, str) or not re.fullmatch(r"CompleteTech-LLC/[a-z0-9]+(?:-[a-z0-9]+)*", repo):
        errors.append("repository must be CompleteTech-LLC/<repository-name>")
    elif isinstance(name, str) and repo.split("/")[1] not in (name, name + "-skill"):
        errors.append("repository and skill_name do not describe the same skill")
    if manifest.get("kind") not in tuple(KINDS):
        errors.append("unsupported kind")
    if manifest.get("network_mode") not in tuple(NETWORK_MODES):
        errors.append("unsupported network_mode")
    if type(manifest.get("private")) is not bool:
        errors.append("private must be a JSON boolean")
    paths = list(FILES) + ["assets/logo.png"]
    for field in ("entrypoints", "example_inputs"):
        values = manifest.get(field)
        if not isinstance(values, list) or not values:
            errors.append(f"{field} must be a non-empty array")
            continue
        if all(isinstance(value, str) for value in values) and len(set(values)) != len(values):
            errors.append(f"{field} contains duplicate paths")
        paths.extend(values)
    for value in paths:
        try:
            local_file(root, value)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    try:
        skill = local_file(root, "SKILL.md").read_text(encoding="utf-8")
        header = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", skill, re.S)
        declared = re.search(r'''(?m)^name:\s*(['"]?)([a-z0-9-]+)\1[ \t]*(?:\#.*)?$''', header.group(1)) if header else None
        if not declared or declared.group(2) != name:
            errors.append("skill_name must match the scalar name in SKILL.md frontmatter")
        readme = local_file(root, "README.md").read_text(encoding="utf-8")
        for marker in NAVIGATION:
            if marker not in readme:
                errors.append(f"README.md missing family navigation: {marker}")
        with local_file(root, "assets/logo.png").open("rb") as handle:
            if handle.read(8) != b"\x89PNG\r\n\x1a\n":
                errors.append("assets/logo.png must be a PNG, not a placeholder")
        for document in ("ONBOARDING.md", "CONTRIBUTING.md"):
            text = local_file(root, document).read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#")):
                    continue
                local_file(root, target.split("#", 1)[0])
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("CompleteTech LLC Skills package contract OK (full checkout; no commands executed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
