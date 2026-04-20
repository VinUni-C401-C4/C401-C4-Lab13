#!/usr/bin/env python
"""Test script to send chat requests via HTTP to /chat endpoint"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

import httpx
from app.tracing import tracing_enabled, flush_traces
from app.audit import audit_log


def main():
    base_url = os.getenv("TEST_BASE_URL", "http://127.0.0.1:8000")

    print(f"Testing /chat endpoint at {base_url}")
    print(f"Tracing enabled: {tracing_enabled()}")

    with httpx.Client(timeout=30.0) as client:
        for i in range(10):
            try:
                response = client.post(
                    f"{base_url}/chat",
                    json={
                        "user_id": f"user_{i}",
                        "feature": "test",
                        "session_id": f"session_{i}",
                        "message": f"Test message {i}",
                    },
                )
                result = response.json()
                print(
                    f"Request {i + 1}: status={response.status_code}, latency={result.get('latency_ms')}ms"
                )

                audit_log(
                    action="test_chat_response",
                    session_id=f"session_{i}",
                    feature="test",
                    latency_ms=result.get("latency_ms"),
                    tokens_in=result.get("tokens_in"),
                    tokens_out=result.get("tokens_out"),
                    cost_usd=result.get("cost_usd"),
                    quality_score=result.get("quality_score"),
                )
            except Exception as e:
                print(f"Request {i + 1} failed: {e}")

    flush_traces()
    print("\nAll 10 traces sent to Langfuse (flushed)!")
    print("Audit logs written to data/audit.jsonl")


if __name__ == "__main__":
    main()
