#!/usr/bin/env python3
"""Fake-API tests for scripts/request_receipt.py."""

from __future__ import annotations

import http.server
import json
import subprocess
import sys
import tempfile
import threading
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUESTER = ROOT / "scripts" / "request_receipt.py"


class ReceiptHandler(http.server.BaseHTTPRequestHandler):
    requests: list[dict[str, Any]] = []
    paths: list[str] = []

    def do_POST(self) -> None:
        raw = self.rfile.read(int(self.headers.get("Content-Length", "0"))).decode("utf-8")
        payload = json.loads(raw)
        ReceiptHandler.requests.append(payload)
        ReceiptHandler.paths.append(self.path)
        response = {
            "ok": True,
            "receipt_code": f"CTREC-FAKE{len(ReceiptHandler.requests):024d}",
            "expires_at": "2099-01-01 00:00:00",
            "claim_url": "https://cert.complete.tech/claim?session_id=codex_test_session",
            "run_id": payload.get("run_id", ""),
        }
        body = json.dumps(response).encode("utf-8")
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return


def run_request(args: list[str], tmp: Path, api_url: str, run_id: str | None = None) -> None:
    command = [
        sys.executable,
        str(REQUESTER),
        "--receipt-api-url",
        api_url,
        "--class-id",
        "codex_test_class",
        "--session-id",
        "codex_test_session",
        "--completion-key",
        "codex-test-key",
        "--skill-version",
        "codex-test-version",
        "--receipt-out",
        str(tmp / f"receipt-{len(ReceiptHandler.requests)}.json"),
    ]
    if run_id:
        command.extend(["--run-id", run_id])
    command.extend(args)
    subprocess.run(command, cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)


def assert_true(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"PASS {label}")


def main() -> int:
    ReceiptHandler.requests = []
    ReceiptHandler.paths = []
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), ReceiptHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    api_url = f"http://127.0.0.1:{server.server_port}/api/skill-runs"
    try:
        with tempfile.TemporaryDirectory(prefix="codex_test_receipt_cli_") as raw_tmp:
            tmp = Path(raw_tmp)
            run_request(["--skill-id", "agentic-normal-skill"], tmp, api_url)
            normal = ReceiptHandler.requests[-1]
            uuid.UUID(normal["run_id"])
            assert_true(ReceiptHandler.paths[-1] == "/api/skill-runs", "normal receipt posts to skill-runs endpoint")
            assert_true(normal["skill_id"] == "agentic-normal-skill", "normal receipt sends skill_id")
            assert_true(normal["skill_version"] == "codex-test-version", "normal receipt sends skill_version")
            assert_true("prerequisite_receipts" not in normal, "normal receipt omits prerequisites")
            assert_true(normal["class_id"] == "codex_test_class", "normal receipt sends class_id")
            assert_true(normal["session_id"] == "codex_test_session", "normal receipt sends session_id")
            assert_true(normal["completion_key"] == "codex-test-key", "normal receipt sends completion_key")
            assert_true(bool(normal["run_id"]), "normal receipt sends run_id")

            run_request([
                "--skill-id",
                "agentic-services-orchestrator-skill",
                "--prerequisite-receipt",
                "CTREC-ONE",
                "--prerequisite-receipt",
                "CTREC-TWO",
                "--prerequisite-receipt",
                "CTREC-THREE",
            ], tmp, api_url, run_id="codex-test-orch-flags")
            flags = ReceiptHandler.requests[-1]
            assert_true(ReceiptHandler.paths[-1] == "/api/skill-runs", "orchestrator flags post to skill-runs endpoint")
            assert_true(
                flags["prerequisite_receipts"] == ["CTREC-ONE", "CTREC-TWO", "CTREC-THREE"],
                "orchestrator sends repeated prerequisite receipt flags",
            )

            receipt_file = tmp / "prereqs.json"
            receipt_file.write_text(json.dumps({"prerequisite_receipts": ["CTREC-A", "CTREC-B", "CTREC-C"]}), encoding="utf-8")
            run_request([
                "--skill-id",
                "agentic-services-orchestrator-skill",
                "--prerequisite-receipts-file",
                str(receipt_file),
            ], tmp, api_url, run_id="codex-test-orch-file")
            file_payload = ReceiptHandler.requests[-1]
            assert_true(ReceiptHandler.paths[-1] == "/api/skill-runs", "orchestrator file posts to skill-runs endpoint")
            assert_true(file_payload["prerequisite_receipts"] == ["CTREC-A", "CTREC-B", "CTREC-C"], "orchestrator sends prerequisite receipt file")
    finally:
        server.shutdown()
        server.server_close()
    print(f"Receipt CLI suite: {len(ReceiptHandler.requests)} requests checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
