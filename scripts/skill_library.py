#!/usr/bin/env python3
"""List, plan installation, or audit local CompleteTech skills; never clone or execute."""
from __future__ import annotations
import argparse
import json
import re
import shlex
from pathlib import Path
from validate_package import FAMILY, allowed_repositories, local_file, unique_object, validate

ROOT = Path(__file__).resolve().parents[1]
SHARED = ("scripts/validate_package.py", "tests/test_package_contract.py", "CONTRIBUTING.md", "AGENTS.md", "BRANDING.md", ".editorconfig", ".github/PULL_REQUEST_TEMPLATE.md", ".github/workflows/package-contract.yml")


def load_members(path: Path, include_private: bool = False) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(data, dict) or set(data) != {"schema_version", "family", "members"} or type(data.get("schema_version")) is not int or data["schema_version"] != 1 or data.get("family") != FAMILY:
        raise ValueError("unsupported skill library catalog")
    if not isinstance(data["members"], list) or not data["members"]:
        raise ValueError("catalog members must be nonempty")
    names: set[str] = set()
    repos: set[str] = set()
    result = []
    for member in data["members"]:
        if not isinstance(member, dict) or set(member) != {"repository", "skill_name", "role", "private"}:
            raise ValueError("invalid catalog member fields")
        name, repo = member["skill_name"], member["repository"]
        if not isinstance(name, str) or len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("invalid skill name")
        if not isinstance(repo, str) or repo not in allowed_repositories(name):
            raise ValueError("repository and skill name mismatch")
        if type(member["private"]) is not bool or not isinstance(member["role"], str) or not member["role"].strip():
            raise ValueError("invalid visibility or role")
        if name in names or repo in repos:
            raise ValueError("duplicate repository or skill name")
        names.add(name)
        repos.add(repo)
        if include_private or not member["private"]:
            result.append(member)
    return result


def quote(value: str, shell: str) -> str:
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError("control characters are not allowed in an installation plan")
    return "'" + value.replace("'", "''") + "'" if shell == "powershell" else shlex.quote(value)


def install_plan(members: list[dict], destination: Path, shell: str = "posix") -> list[str]:
    return [f"git clone -- {quote('https://github.com/' + m['repository'] + '.git', shell)} {quote(str(destination / m['skill_name']), shell)}" for m in members]


def audit(members: list[dict], workspace: Path) -> list[str]:
    errors = []
    for member in members:
        checkout = workspace / member["skill_name"]
        if not checkout.is_dir():
            checkout = workspace / member["repository"].split("/")[1]
        try:
            if not checkout.resolve().is_relative_to(workspace.resolve()):
                raise ValueError("checkout escapes workspace")
            issues = validate(checkout)
            if not issues:
                manifest = json.loads(local_file(checkout, "skill-package.json").read_text(encoding="utf-8"), object_pairs_hook=unique_object)
                for field in ("repository", "skill_name", "private"):
                    if manifest[field] != member[field]:
                        issues.append(f"catalog mismatch: {field}")
                for relative in SHARED:
                    # Universal newline reading avoids false drift on Windows.
                    if local_file(checkout, relative).read_text(encoding="utf-8") != local_file(ROOT, relative).read_text(encoding="utf-8"):
                        issues.append(f"shared contract drift: {relative}")
        except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
            issues = [str(exc)]
        errors.extend(f"{member['skill_name']}: {issue}" for issue in issues)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("list", "plan", "audit"), nargs="?", default="list")
    parser.add_argument("--include-private", action="store_true")
    parser.add_argument("--destination", type=Path, default=Path("skills"))
    parser.add_argument("--shell", choices=("posix", "powershell"), default="posix")
    parser.add_argument("--workspace", type=Path)
    args = parser.parse_args(argv)
    try:
        members = load_members(ROOT / "references/skill-library.json", args.include_private)
        if args.action == "plan":
            destination = quote(str(args.destination), args.shell)
            commands = install_plan(members, args.destination, args.shell)
            print("# Review before running. Nothing has been installed. Default branches are not a pinned release.")
            print(f"New-Item -ItemType Directory -Force -Path {destination} | Out-Null" if args.shell == "powershell" else f"mkdir -p -- {destination}")
            print("\n".join(commands))
        elif args.action == "audit":
            if args.workspace is None:
                parser.error("audit requires --workspace")
            errors = audit(members, args.workspace)
            print("\n".join(errors) if errors else f"All {len(members)} local skill packages match the shared contract")
            return int(bool(errors))
        else:
            print(json.dumps(members, indent=2))
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
