from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


AUDIT_PATH = os.getenv("AUDIT_LOG_PATH", "data/audit.jsonl")


def _get_audit_path() -> Path:
    path = Path(AUDIT_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def audit_log(
    action: str,
    user_id_hash: str | None = None,
    session_id: str | None = None,
    feature: str | None = None,
    message_preview: str | None = None,
    latency_ms: int | None = None,
    tokens_in: int | None = None,
    tokens_out: int | None = None,
    cost_usd: float | None = None,
    quality_score: float | None = None,
    error_type: str | None = None,
    error_detail: str | None = None,
) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "user_id_hash": user_id_hash,
        "session_id": session_id,
        "feature": feature,
        "message_preview": message_preview,
        "latency_ms": latency_ms,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": cost_usd,
        "quality_score": quality_score,
        "error_type": error_type,
        "error_detail": error_detail,
    }
    audit_file = _get_audit_path()
    with open(audit_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
