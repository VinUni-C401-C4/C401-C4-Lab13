from __future__ import annotations

import hashlib
import re

# ---------------------------------------------------------------------------
# Bộ từ điển Regex PII — phòng thủ mọi kịch bản cross-check
# Mỗi pattern khớp sẽ bị thay bằng [REDACTED_<TÊN>] trong log output.
# ---------------------------------------------------------------------------
PII_PATTERNS: dict[str, str] = {
    # Email: bắt mọi dạng user.name+tag@sub.domain.co
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",

    # Số điện thoại VN: +84 / 0 tiếp theo 9-10 chữ số, cho phép dấu cách/chấm/gạch
    "phone_vn": (
        r"(?:\+84|0)"           # Mã quốc gia hoặc số 0 đầu
        r"(?:[\s.\-]?\d){9,10}" # 9-10 chữ số, xen kẽ dấu phân cách tùy ý
    ),

    # Số CCCD / CMND mới (đúng 12 chữ số liền nhau)
    "cccd": r"\b\d{12}\b",

    # Thẻ tín dụng: 16 chữ số, có thể cách bằng dấu cách hoặc gạch nối mỗi 4 số
    "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",

    # Hộ chiếu Việt Nam: 1 chữ cái (thường B hoặc C) + 7 chữ số
    "passport_vn": r"\b[A-Za-z]\d{7}\b",

    # Địa chỉ IPv4: chặn lộ IP nội bộ / public trong log
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
}


def scrub_text(text: str) -> str:
    safe = text
    for name, pattern in PII_PATTERNS.items():
        safe = re.sub(pattern, f"[REDACTED_{name.upper()}]", safe)
    return safe


def summarize_text(text: str, max_len: int = 80) -> str:
    safe = scrub_text(text).strip().replace("\n", " ")
    return safe[:max_len] + ("..." if len(safe) > max_len else "")


def hash_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:12]
