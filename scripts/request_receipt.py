#!/usr/bin/env python3
"""Request a CompleteTech certificate receipt for a skill run.

This helper is intentionally self-contained so each skill repository can carry
the same classroom receipt workflow without depending on a shared package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT_API_URL = "https://cert.complete.tech/api/skill-runs"


def load_env_file(path: Path) -> None:
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or key in os.environ:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ[key] = value


def first_present(*values: Optional[str]) -> str:
    for value in values:
        if value is not None and value.strip():
            return value.strip()
    return ""


def env_profile_prefix(profile: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", profile).strip("_").upper()
    return f"CT_CERT_{normalized}"


def skill_metadata() -> tuple[str, str]:
    skill_md = ROOT / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""
    name_match = re.search(r"^name:\s*([A-Za-z0-9._-]+)\s*$", text, re.MULTILINE)
    version_match = re.search(r"^version:\s*([A-Za-z0-9._-]+)\s*$", text, re.MULTILINE)
    fallback = ROOT.name.replace("_", "-")
    return (
        name_match.group(1) if name_match else fallback,
        version_match.group(1) if version_match else "1.0.0",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def load_receipts(raw_values: list[str], raw_file: Optional[str]) -> list[str]:
    receipts = [value.strip() for value in raw_values if value and value.strip()]
    if not raw_file:
        return receipts
    data = json.loads(Path(raw_file).expanduser().read_text(encoding="utf-8"))
    if isinstance(data, list):
        receipts.extend(str(value).strip() for value in data if str(value).strip())
    elif isinstance(data, dict):
        raw_receipts = data.get("prerequisite_receipts") or data.get("receipts") or []
        if not isinstance(raw_receipts, list):
            raise SystemExit("Prerequisite receipt JSON must contain a receipts array.")
        receipts.extend(str(value).strip() for value in raw_receipts if str(value).strip())
    else:
        raise SystemExit("Prerequisite receipt JSON must be an array or object.")
    return receipts


def post_json(api_url: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        api_url,
        data=body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"{payload['skill_id']}/receipt-helper",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8")
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Receipt API rejected the request with HTTP {exc.code}: {details}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Receipt API request failed: {exc.reason}") from exc
    decoded = json.loads(data)
    if not isinstance(decoded, dict) or decoded.get("ok") is not True:
        raise RuntimeError(f"Receipt API returned an unsuccessful response: {decoded!r}")
    return decoded


def parse_args() -> argparse.Namespace:
    default_skill_id, default_skill_version = skill_metadata()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt-api-url", default=None)
    parser.add_argument("--registry-profile", default=None)
    parser.add_argument("--class-id", default=None)
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--completion-key", default=None)
    parser.add_argument("--completion-key-env", default=None)
    parser.add_argument("--skill-id", default=None)
    parser.add_argument("--skill-version", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--artifact", default=None, help="Optional output artifact path to hash.")
    parser.add_argument("--artifact-hash", default=None)
    parser.add_argument("--metadata", action="append", default=[], help="Metadata as key=value.")
    parser.add_argument("--receipt-out", default=None, help="Receipt JSON output path.")
    parser.add_argument("--prerequisite-receipt", action="append", default=[])
    parser.add_argument("--prerequisite-receipts-file", default=None)
    parser.set_defaults(default_skill_id=default_skill_id, default_skill_version=default_skill_version)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_env_file(ROOT / ".env")
    load_env_file(ROOT / ".env.local")

    profile: dict[str, str] = {}
    if args.registry_profile:
        prefix = env_profile_prefix(args.registry_profile)
        profile = {
            "class_id": os.environ.get(f"{prefix}_CLASS_ID", ""),
            "session_id": os.environ.get(f"{prefix}_SESSION_ID", ""),
            "completion_key": os.environ.get(f"{prefix}_COMPLETION_KEY", ""),
        }

    key_env = first_present(args.completion_key_env, os.environ.get("CT_CERT_COMPLETION_KEY_ENV"), "CT_CERT_COMPLETION_KEY")
    artifact_hash = first_present(args.artifact_hash)
    if not artifact_hash and args.artifact:
        artifact_hash = sha256_file(Path(args.artifact).expanduser())

    metadata: dict[str, str] = {
        "requested_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repository": ROOT.name,
    }
    if args.artifact:
        metadata["artifact"] = Path(args.artifact).expanduser().name
    for entry in args.metadata:
        if "=" not in entry:
            raise SystemExit(f"--metadata must be key=value, got: {entry}")
        key, value = entry.split("=", 1)
        metadata[key.strip()] = value.strip()

    payload: dict[str, Any] = {
        "class_id": first_present(args.class_id, profile.get("class_id"), os.environ.get("CT_CERT_CLASS_ID")),
        "session_id": first_present(args.session_id, profile.get("session_id"), os.environ.get("CT_CERT_SESSION_ID")),
        "completion_key": first_present(args.completion_key, profile.get("completion_key"), os.environ.get(key_env)),
        "skill_id": first_present(args.skill_id, os.environ.get("CT_CERT_SKILL_ID"), args.default_skill_id),
        "skill_version": first_present(args.skill_version, os.environ.get("CT_CERT_SKILL_VERSION"), args.default_skill_version),
        "run_id": first_present(args.run_id, str(uuid.uuid4())),
        "metadata": metadata,
    }
    if artifact_hash:
        payload["artifact_hash"] = artifact_hash
    prerequisite_receipts = load_receipts(args.prerequisite_receipt, args.prerequisite_receipts_file)
    if prerequisite_receipts:
        payload["prerequisite_receipts"] = prerequisite_receipts

    missing = [key for key in ("class_id", "session_id", "completion_key", "skill_id", "run_id") if not payload[key]]
    if missing:
        raise SystemExit(f"Missing receipt field(s): {', '.join(missing)}")

    api_url = first_present(args.receipt_api_url, os.environ.get("CT_CERT_RECEIPT_API_URL"), DEFAULT_RECEIPT_API_URL)
    receipt = post_json(api_url, payload)
    record = {
        "receipt_code": str(receipt["receipt_code"]),
        "claim_url": str(receipt["claim_url"]),
        "expires_at": str(receipt["expires_at"]),
        "class_id": payload["class_id"],
        "session_id": payload["session_id"],
        "skill_id": payload["skill_id"],
        "skill_version": payload["skill_version"],
        "run_id": str(receipt.get("run_id") or payload["run_id"]),
        "artifact_hash": artifact_hash,
        "prerequisite_receipts_count": len(prerequisite_receipts),
    }

    receipt_out = Path(args.receipt_out).expanduser() if args.receipt_out else ROOT / "output" / f"{record['run_id']}.receipt.json"
    receipt_out.parent.mkdir(parents=True, exist_ok=True)
    receipt_out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Receipt Code: {record['receipt_code']}")
    print(f"Claim URL: {record['claim_url']}")
    print(f"Receipt JSON: {receipt_out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)
