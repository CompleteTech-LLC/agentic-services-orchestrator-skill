#!/usr/bin/env python3
"""List, plan installation, or audit local CompleteTech skills; never clone or execute."""
from __future__ import annotations

import argparse
import json
import re
import shlex
from pathlib import Path

from validate_package import FAMILY, unique_object, validate

ROOT = Path(__file__).resolve().parents[1]
SHARED = ("scripts/validate_package.py", "tests/test_package_contract.py", "CONTRIBUTING.md", ".github/workflows/package-contract.yml")


def load_members(path: Path, include_private: bool = False) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data.get("schema_version") != 1 or data.get("family") != FAMILY:
        raise ValueError("unsupported skill library catalog")
    members = data.get("members")
    if not isinstance(members, list) or not members:
        raise ValueError("catalog members must be a non-empty list")
    seen_names: set[str] = set()
    seen_repos: set[str] = set()
    selected = []
    for member in members:
        if not isinstance(member, dict) or set(member) != {"repository", "skill_name", "role", "private"}:
            raise ValueError("invalid catalog member fields")
        repo, name = member["repository"], member["skill_name"]
        if not isinstance(repo, str) or not re.fullmatch(r"CompleteTech-LLC/[a-z0-9]+(?:-[a-z0-9]+)*", repo):
            raise ValueError("invalid repository")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("invalid skill name")
        if type(member["private"]) is not bool or not isinstance(member["role"], str) or not member["role"]:
            raise ValueError("invalid visibility or role")
        if repo in seen_repos or name in seen_names:
            raise ValueError("duplicate repository or skill name")
        seen_repos.add(repo)
        seen_names.add(name)
        if include_private or not member["private"]:
            selected.append(member)
    return selected


def install_plan(members: list[dict], destination: Path) -> list[str]:
    return [f"git clone -- {shlex.quote('https://github.com/' + member['repository'] + '.git')} {shlex.quote(str(destination / member['skill_name']))}" for member in members]


def audit(members: list[dict], workspace: Path) -> list[str]:
    errors = []
    for member in members:
        checkout = workspace / member["skill_name"]
        if not checkout.is_dir():
            checkout = workspace / member["repository"].split("/")[1]
        issues = validate(checkout)
        if not issues:
            manifest = json.loads((checkout / "skill-package.json").read_text(encoding="utf-8"))
            for field in ("repository", "skill_name", "private"):
                if manifest[field] != member[field]:
                    issues.append(f"catalog mismatch: {field}")
            for relative in SHARED:
                target = (checkout / relative).resolve()
                if not target.is_relative_to(checkout.resolve()) or not target.is_file() or target.read_bytes() != (ROOT / relative).read_bytes():
                    issues.append(f"shared contract drift: {relative}")
        errors.extend(f"{member['skill_name']}: {issue}" for issue in issues)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("list", "plan", "audit"), nargs="?", default="list")
    parser.add_argument("--include-private", action="store_true", help="Include the optional private skill; does not grant access.")
    parser.add_argument("--destination", type=Path, default=Path("skills"), help="Destination printed in the POSIX-shell plan; nothing is created.")
    parser.add_argument("--workspace", type=Path, help="Existing sibling checkouts to audit offline.")
    args = parser.parse_args(argv)
    try:
        members = load_members(ROOT / "references/skill-library.json", args.include_private)
        if args.action == "plan":
            print("# Review before running in a POSIX shell. Nothing has been cloned or installed.")
            print("# Uses the current default branches, not a pinned or atomic suite release.")
            print(f"mkdir -p -- {shlex.quote(str(args.destination))}")
            print("\n".join(install_plan(members, args.destination)))
        elif args.action == "audit":
            if args.workspace is None:
                parser.error("audit requires --workspace")
            errors = audit(members, args.workspace)
            print("\n".join(errors) if errors else f"All {len(members)} local skill packages match the shared contract")
            return int(bool(errors))
        else:
            print(json.dumps(members, indent=2))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
