from __future__ import annotations

import time

from .incidents import STATE

CORPUS = {
    "refund": ["Refunds are available within 7 days with proof of purchase."],
    "monitoring": ["Metrics detect incidents, traces localize them, logs explain root cause."],
    "policy": ["Do not expose PII in logs. Use sanitized summaries only."],
    "ký túc xá": ["Thủ tục đăng ký KTX VinUni thực hiện qua Portal sinh viên ở Tuần định hướng (Orientation Week)."],
    "lịch học": ["Lịch học tân sinh viên sẽ được phòng Đào tạo gửi vào email cá nhân có đuôi @vinuni.edu.vn."],
    "onboarding": ["Tuần lễ Onboarding diễn ra vào tháng 9 với nhiều hoạt động kết nối và Campus Tour."],
}


def retrieve(message: str) -> list[str]:
    if STATE["tool_fail"]:
        raise RuntimeError("Vector store timeout")
    if STATE["rag_slow"]:
        time.sleep(2.5)
    lowered = message.lower()
    for key, docs in CORPUS.items():
        if key in lowered:
            return docs
    return ["No domain document matched. Use general fallback answer."]
