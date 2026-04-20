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


EXAMPLE_CHATS = [
    {
        "user_id": "user_1",
        "feature": "test",
        "session_id": "session_1",
        "message": "Hello, how are you?",
    },
    {
        "user_id": "user_2",
        "feature": "test",
        "session_id": "session_2",
        "message": "What is Python?",
    },
    {
        "user_id": "user_3",
        "feature": "test",
        "session_id": "session_3",
        "message": "Explain recursion in 3 sentences.",
    },
    {
        "user_id": "user_4",
        "feature": "test",
        "session_id": "session_4",
        "message": "Write a hello world function in JavaScript.",
    },
    {
        "user_id": "user_5",
        "feature": "test",
        "session_id": "session_5",
        "message": "What are decorators in Python?",
    },
    {
        "user_id": "user_6",
        "feature": "test",
        "session_id": "session_6",
        "message": "How does async/await work?",
    },
    {
        "user_id": "user_7",
        "feature": "test",
        "session_id": "session_7",
        "message": "Explain REST APIs simply.",
    },
    {
        "user_id": "user_8",
        "feature": "test",
        "session_id": "session_8",
        "message": "What is Git and how do I use it?",
    },
    {
        "user_id": "user_9",
        "feature": "test",
        "session_id": "session_9",
        "message": "Tell me about SQL joins.",
    },
    {
        "user_id": "user_10",
        "feature": "test",
        "session_id": "session_10",
        "message": "What is the difference between list and tuple?",
    },
]


def main():
    base_url = os.getenv("TEST_BASE_URL", "http://127.0.0.1:8000")

    print(f"Testing /chat endpoint at {base_url}")
    print(f"Tracing enabled: {tracing_enabled()}")

    with httpx.Client(timeout=30.0) as client:
        for i, chat in enumerate(EXAMPLE_CHATS):
            try:
                response = client.post(
                    f"{base_url}/chat",
                    json=chat,
                )
                result = response.json()
                print(
                    f"Request {i + 1}: status={response.status_code}, latency={result.get('latency_ms')}ms"
                )

                audit_log(
                    action="test_chat_response",
                    session_id=chat["session_id"],
                    feature=chat["feature"],
                    latency_ms=result.get("latency_ms"),
                    tokens_in=result.get("tokens_in"),
                    tokens_out=result.get("tokens_out"),
                    cost_usd=result.get("cost_usd"),
                    quality_score=result.get("quality_score"),
                )
            except Exception as e:
                print(f"Request {i + 1} failed: {e}")

    flush_traces()
    print(f"\nAll {len(EXAMPLE_CHATS)} traces sent to Langfuse (flushed)!")
    print("Audit logs written to data/audit.jsonl")


if __name__ == "__main__":
    main()
