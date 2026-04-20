from __future__ import annotations

import os
from typing import Any

try:
    from langfuse import observe, get_client
except Exception:  # pragma: no cover

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func

        return decorator

    get_client = None

try:
    from langfuse import langfuse_context
except Exception:  # pragma: no cover

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

        def score(self, **kwargs: Any) -> None:
            return None

        def flush(self) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def flush_traces() -> None:
    try:
        client = get_client()
        if client:
            client.flush()
    except Exception as e:
        print(f"Flush error: {e}")
        pass
