# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Chatbot hỗ trợ Onboarding sinh viên VinUni
- [REPO_URL]: https://github.com/VinUni-C401-C4/C401-C4-Lab13
- [MEMBERS]:
  - Member A: Phạm Hữu Hoàng Hiệp | Role: Logging & PII
  - Member B: Dũng | Role: Tracing & Enrichment
  - Member C: Cường | Role: SLO & Alerts & Dashboard
  - Member D: Lâm | Role: Load Test & Incident & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: >10
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]: (Briefly explain one interesting span in your trace)

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:


| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | |
| Error Rate | < 2% | 28d | |
| Cost Budget | < $2.5/day | 1d | |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Tốc độ phản hồi của hệ thống bị chậm đi đáng kể so với mức bình thường (~700ms vọt lên hơn 10000ms), dẫn tới độ trễ (latency) khi chạy load test cao bất thường.
- [ROOT_CAUSE_PROVED_BY]: Log ghi nhận thời gian `latency_ms` lớn (hơn 10000) cùng với truy vết trên Trace ID trỏ tới quá trình truy xuất (retrieval) tài liệu, trong trường hợp này `mock_rag.py` dùng vòng lặp bị làm chậm nhân tạo (`time.sleep(2.5)` lặp lại).
- [FIX_ACTION]: Sửa lỗi độ trễ tại RAG retrieval process (Về mặt mô phỏng: tắt lệnh cố ý chờ này đi qua tính năng disable incident).
- [PREVENTIVE_MEASURE]: Triển khai Timeout cho các tác vụ gọi ra dịch vụ bên ngoài (như gọi API vector database), cũng như xây dựng tính năng fallback/cache nếu DB trả kết quả chậm hơn mức quy định của SLO.

---

## 5. Individual Contributions & Evidence

### Phạm Hữu Hoàng Hiệp - 2A202600415
- [TASKS_COMPLETED]: Xây dựng toàn bộ nền tảng Observability Logging. Khởi tạo và thiết lập `Correlation_id` tại middleware. Làm giàu Log context (`bind_contextvars`) với ẩn danh user_id_hash. Thiết lập Regex chặn PII siêu khắt khe (chặn email, cccd, visa, phone, ipv4, passport) qua processor `scrub_event`. Nâng cấp chống OOM Flooding (giới hạn độ dài session_id/feature). Hỗ trợ team chạy script đạt mốc 100/100 Điểm kỹ thuật.
- [EVIDENCE_LINK]: https://github.com/VinUni-C401-C4/C401-C4-Lab13/commit/b5e40bdee60bcfdb18643f1e39d9eb466f920134
- [EVIDENCE_LINK]: https://github.com/VinUni-C401-C4/C401-C4-Lab13/commit/986c55c045ddf476567e185785c0aca64fa36793

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### Phạm Việt Cường - 2A202600420 (SLO & Alerts & Dashboard)
- [TASKS_COMPLETED]:
  - Xây dựng và chuẩn hóa SLO tại `config/slo.yaml`: bổ sung objective/target/unit/comparator/source metric cho các SLI chính (`latency_p95_ms`, `latency_p99_ms`, `error_rate_pct`, `daily_cost_usd`, `quality_score_avg`), đồng bộ ngưỡng phục vụ chấm rubric.
  - Thiết kế và cấu hình alert rules tại `config/alert_rules.yaml`: hoàn thiện tối thiểu 3 luật cảnh báo, mở rộng thành 4 luật gồm `high_latency_p95`, `high_error_rate`, `cost_budget_spike`, `quality_score_drop`; gắn `severity`, `owner`, `slo_ref`, kênh notify và runbook.
  - Viết và liên kết runbook xử lý sự cố trong `docs/alerts.md`, bổ sung quy trình cho trường hợp tụt chất lượng (`quality_score_drop`) và hướng điều tra theo flow Metrics -> Traces -> Logs.
  - Thiết kế blueprint Dashboard giám sát tại `docs/dashboard-spec.md` với đúng 6 panels, có đơn vị hiển thị và threshold/SLO line; cấu hình mặc định `Last 1 hour`, auto-refresh `30s`, và SLO summary cho 4 chỉ số cốt lõi.
  - Hỗ trợ kiểm thử khi bơm tải bằng `scripts/load_test.py`, đối chiếu ngưỡng cảnh báo với kết quả runtime để đảm bảo dashboard/alerts bám sát hành vi hệ thống.
- [EVIDENCE_LINK]: https://github.com/VinUni-C401-C4/C401-C4-Lab13/commit/8705a93
- [EVIDENCE_LINK]: `config/slo.yaml`, `config/alert_rules.yaml`, `docs/alerts.md`, `docs/dashboard-spec.md`

### Lâm (QA & Team Lead)
- [TASKS_COMPLETED]: 
  - Chạy mô phỏng tải (`load_test.py`) để giả lập lưu lượng với `--concurrency 5`.
  - Thiết lập kịch bản Incident (cụ thể `rag_slow` và `tool_fail`) để đánh thử nghiệm và theo dõi trạng thái.
  - Thực hiện Trace Root Cause dựa vào việc tìm kiếm `correlation_id` trên log `logs.jsonl` thu thập được để từ đó phân tích lỗi `tool_fail` hay `Vector store timeout`.
  - Quản lý kịch bản Demo Live (soạn file `docs/demo-scenario.md`) để có thể mô tả quá trình từ hệ thống sập đến truy vết để hoàn thành Demo A3.
- [EVIDENCE_LINK]: Kịch bản Live Demo (`docs/demo-scenario.md`) và phần Incident Response (Section 4).

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
