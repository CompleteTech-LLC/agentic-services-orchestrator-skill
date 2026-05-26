#!/usr/bin/env python3
"""Validate lint, parser, diagram, and smoke-test gates for this skill repo."""

from __future__ import annotations

import argparse
import configparser
import json
import py_compile
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, cast

try:
    import yaml
except ImportError:  # pragma: no cover - reported clearly at runtime
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "env", "ENV", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"}


def iter_files(*suffixes: str) -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix in suffixes:
            files.append(path)
    return sorted(files)


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def run_ruff() -> None:
    if shutil.which("ruff"):
        run(["ruff", "check", "."])
        return
    if shutil.which("uvx"):
        run(["uvx", "ruff", "check", "."])
        return
    run([sys.executable, "-m", "ruff", "check", "."])


def compile_python() -> None:
    for path in iter_files(".py"):
        py_compile.compile(str(path), doraise=True)
    print("python compile ok")


def parse_structured_files() -> None:
    yaml_files = iter_files(".yaml", ".yml")
    yaml_module = cast(Any, yaml)
    if yaml_files and yaml_module is None:
        raise RuntimeError("PyYAML is required to parse YAML files")
    for path in yaml_files:
        yaml_module.safe_load(path.read_text(encoding="utf-8"))
    for path in iter_files(".json"):
        json.loads(path.read_text(encoding="utf-8"))
    for path in iter_files(".ini"):
        parser = configparser.RawConfigParser()
        with path.open(encoding="utf-8") as handle:
            parser.read_file(handle)
    print("structured files ok")


def mermaid_command() -> list[str] | None:
    if shutil.which("mmdc"):
        return ["mmdc"]
    if shutil.which("npx"):
        return ["npx", "--yes", "@mermaid-js/mermaid-cli"]
    return None


def validate_mermaid(skip: bool) -> None:
    diagrams = iter_files(".mmd")
    if not diagrams:
        print("mermaid skipped: no .mmd files")
        return
    cmd = mermaid_command()
    if skip or cmd is None:
        reason = "requested" if skip else "mmdc/npx not available"
        print(f"mermaid skipped: {reason}")
        return
    with tempfile.TemporaryDirectory(prefix="skill-mermaid-") as tmp:
        out_dir = Path(tmp)
        for index, path in enumerate(diagrams, start=1):
            run([*cmd, "-i", str(path), "-o", str(out_dir / f"diagram-{index}.svg"), "-b", "white"])
    print("mermaid ok")


def smoke_generators() -> None:
    generator_commands = {
        "generate_certificate.py": [
            "--config",
            "config.ini",
            "examples/northwind_workshop.ini",
            "--out",
            "{tmp}/certificate.pdf",
        ],
        "generate_contract.py": [
            "--config",
            "config.ini",
            "examples/northwind_support_triage.ini",
            "--out",
            "{tmp}/contract.pdf",
            "--markdown-out",
            "{tmp}/contract.md",
            "--no-envelope",
        ],
        "generate_envelope.py": [
            "--config",
            "config.ini",
            "examples/northwind_address.ini",
            "--out",
            "{tmp}/envelope.pdf",
        ],
    }
    with tempfile.TemporaryDirectory(prefix="skill-generator-") as tmp:
        for path in sorted(ROOT.glob("generate_*.py")):
            run([sys.executable, str(path), "--help"])
            args = generator_commands.get(path.name)
            if args:
                resolved_args = [arg.format(tmp=tmp) for arg in args]
                run([sys.executable, str(path), *resolved_args])
    print("generator smoke ok")


def smoke_catalog_renderers() -> None:
    scripts_dir = ROOT / "scripts"
    if not scripts_dir.exists():
        print("catalog smoke skipped: no scripts directory")
        return
    index_path = ROOT / "references" / "template-index.json"
    first_template = None
    if index_path.exists():
        index_data = json.loads(index_path.read_text(encoding="utf-8"))
        templates = index_data.get("templates", [])
        if templates:
            first_template = templates[0].get("id")
    for path in sorted(scripts_dir.glob("render_*.py")):
        if path.name == "render_pdf.py":
            continue
        run([sys.executable, str(path), "--list"])
        if first_template:
            run([sys.executable, str(path), "--template", first_template, "--var", "smoke=value", "--no-pdf"])
    print("catalog smoke ok")


def run_pyright() -> None:
    if not (ROOT / "pyrightconfig.json").exists():
        print("pyright skipped: no pyrightconfig.json")
        return
    if shutil.which("pyright"):
        run(["pyright"])
        return
    if shutil.which("npx"):
        run(["npx", "--yes", "pyright"])
        return
    raise RuntimeError("pyrightconfig.json exists, but pyright/npx is unavailable")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-mermaid", action="store_true", help="Skip Mermaid render validation when local tooling is unavailable.")
    args = parser.parse_args()

    compile_python()
    run_ruff()
    parse_structured_files()
    validate_mermaid(args.skip_mermaid)
    smoke_generators()
    smoke_catalog_renderers()
    run_pyright()
    print("quality validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
