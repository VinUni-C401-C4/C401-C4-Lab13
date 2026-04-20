from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Dọn sạch contextvars từ request trước để tránh rò rỉ metadata
        clear_contextvars()

        # Lấy x-request-id từ header client gửi lên; nếu không có, tự sinh mã mới
        # Format chuẩn: req-<8 ký tự hex từ uuid4>
        correlation_id = request.headers.get(
            "x-request-id",
            f"req-{uuid.uuid4().hex[:8]}",
        )

        # Gắn correlation_id vào structlog context — mọi dòng log sau đây đều kế thừa
        bind_contextvars(correlation_id=correlation_id)

        # Lưu vào request.state để các handler phía sau truy cập trực tiếp
        request.state.correlation_id = correlation_id

        # Đo thời gian xử lý request
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        # Trả correlation_id và thời gian xử lý về cho client qua response headers
        response.headers["x-request-id"] = correlation_id
        response.headers["x-response-time-ms"] = str(elapsed_ms)

        return response
