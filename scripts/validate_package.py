#!/usr/bin/env python3
"""Validate the CompleteTech LLC Skills checkout contract; no execution or network."""
from __future__ import annotations

import argparse
import json
import re
import struct
import zlib
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


def validate_png(path: Path) -> None:
    """Check a bounded PNG chunk envelope and CRCs, not pixel decoding or artwork."""
    limit = 16 * 1024 * 1024
    with path.open("rb") as handle:
        data = handle.read(limit + 1)
    if len(data) > limit or not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("logo must be a PNG of at most 16 MiB")
    offset = 8
    seen_header = False
    seen_data = False
    while offset + 12 <= len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            raise ValueError("truncated PNG chunk")
        payload = data[offset + 8:end - 4]
        crc = struct.unpack_from(">I", data, end - 4)[0]
        if zlib.crc32(kind + payload) != crc:
            raise ValueError("PNG chunk checksum mismatch")
        if not seen_header and kind != b"IHDR":
            raise ValueError("PNG must start with IHDR")
        if kind == b"IHDR":
            if seen_header or length != 13:
                raise ValueError("invalid PNG header")
            width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", payload)
            depths = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8), 4: (8, 16), 6: (8, 16)}
            if not width or not height or depth not in depths.get(color, ()) or compression or filtering or interlace not in (0, 1):
                raise ValueError("invalid PNG image parameters")
            seen_header = True
        elif kind == b"IDAT" and length:
            seen_data = True
        elif kind == b"IEND":
            if length or not seen_data or end != len(data):
                raise ValueError("invalid PNG end or missing image data")
            return
        offset = end
    raise ValueError("PNG missing complete IHDR/IDAT/IEND structure")


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
        validate_png(local_file(root, "assets/logo.png"))
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
