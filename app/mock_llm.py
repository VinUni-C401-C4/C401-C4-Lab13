from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model

    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        doc_text = prompt.split("Docs=")[1].split("\n")[0]
        if "['" in doc_text:
            extracted_info = doc_text.replace("['", "").replace("']", "")
            answer = (
                f"[VinUni Onboarding Chatbot] Chào Tân sinh viên! Dựa theo cẩm nang nhà trường: {extracted_info}. "
                "Mong thông tin này hữu ích cho tuần lễ định hướng của bạn!"
            )
        else:
            answer = (
                "[VinUni Onboarding Chatbot] Chào bạn! Hiện tại Bot chưa tra cứu được thông tin này. "
                "Vui lòng hỏi các từ khóa như: ký túc xá, lịch học, onboarding, hoặc policy."
            )
        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)
