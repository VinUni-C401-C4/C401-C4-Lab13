# Live Demo Scenario - Day 13 Observability

This guide outlines the steps for a successful live demo to showcase system observability and incident response.

## Prerequisites
- Server running: `./.venv/bin/python -m uvicorn app.main:app --reload`
- Clean logs: `rm data/logs.jsonl`

## Scenario 1: Baseline Performance (Everything is Green)
1. **Show Load**: Run `python scripts/load_test.py --concurrency 5`.
2. **Highlight**: 
   - Latency is stable around ~700ms.
   - Status codes are all 200.
   - Correlation IDs (e.g., `req-abc12345`) are generated for every request.
3. **Verify Logs**: Run `python scripts/validate_logs.py`.
   - Show the **100/100 score**.
   - Show that PII (emails/phones) in `data/sample_queries.jsonl` are automatically redacted in the logs.

## Scenario 2: System Incident (The "Meltdown")
1. **Inject Error**: Run `python scripts/inject_incident.py --scenario tool_fail`.
2. **Run Load**: Run `python scripts/load_test.py --concurrency 2`.
3. **Observation**:
   - Status codes jump to 500.
   - Latency drops to < 10ms (failed fast).
4. **Root Cause Analysis (Live Tracing)**:
   - Pick a Correlation ID from the load test output (e.g., `req-xyz789`).
   - Run: `grep "req-xyz789" data/logs.jsonl | jq .`.
   - **Point out the exact error**: `"error_type": "RuntimeError", "detail": "Vector store timeout"`.
   - Explain how this trace connects the initial request to the failure point.

## Scenario 3: Performance Degradation (The "Slow Leak")
1. **Switch Incident**: 
   - `python scripts/inject_incident.py --scenario tool_fail --disable`
   - `python scripts/inject_incident.py --scenario rag_slow`
2. **Run Load**: Run `python scripts/load_test.py --concurrency 5`.
3. **Observation**: Latency spikes to > 10,000ms (10s).
4. **Conclusion**: Show how the dashboard (if set up) would reflect the P95 latency breach.

## Scenario 4: Recovery
1. **Restore Service**: Run `python scripts/inject_incident.py --scenario rag_slow --disable`.
2. **Final Pulse**: Run `python scripts/load_test.py --concurrency 1`.
3. **Result**: System is back to normal latency (~700ms).
