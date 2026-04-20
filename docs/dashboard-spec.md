# Dashboard Spec

Required Layer-2 panels:
1. Latency P50/P95/P99
2. Traffic (request count or QPS)
3. Error rate with breakdown
4. Cost over time
5. Tokens in/out
6. Quality proxy (heuristic, thumbs, or regenerate rate)

Quality bar:
- default time range = 1 hour
- auto refresh every 15-30 seconds
- visible threshold/SLO line
- units clearly labeled
- no more than 6-8 panels on the main layer

## Suggested production-ready layout (exactly 6 panels)

Set dashboard defaults:
- Time range: `Last 1 hour`
- Auto-refresh: `30s`
- Timezone: local team timezone
- Legend: show current value + avg + max/min

Panel details:

1. **Latency P50/P95/P99 (line chart)**
   - Unit: `ms`
   - Series: `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms`
   - Threshold lines:
     - Warning: `3000` (SLO for P95)
     - Critical: `5000` (guardrail for P99)

2. **Traffic QPS / Request Count (area or bar)**
   - Unit: `req/s` (or `requests/min`)
   - Series: total requests and optional split by endpoint
   - Threshold lines:
     - Capacity warning: team-defined baseline x 1.5
     - Capacity critical: baseline x 2

3. **Error Rate with Breakdown (line + stacked bar)**
   - Unit: `%`
   - Series: `error_rate_pct` + stacked `error_type`
   - Threshold lines:
     - Warning: `1.0`
     - Critical: `2.0` (SLO limit)

4. **Cost Over Time (line chart)**
   - Unit: `USD/hour` and `USD/day`
   - Series: `hourly_cost_usd`, rolling `daily_cost_usd`
   - Threshold lines:
     - Warning: `2.0 USD/day`
     - Critical: `2.5 USD/day` (budget SLO)

5. **Tokens In / Tokens Out (stacked area)**
   - Unit: `tokens`
   - Series: `tokens_in`, `tokens_out`
   - Threshold lines:
     - Soft guardrail: expected baseline x 1.3
     - Hard guardrail: baseline x 1.6

6. **Quality Score / Regeneration Rate (line chart)**
   - Unit: `score (0-1)` or `%`
   - Series: `quality_score_avg` and optional `regenerate_rate_pct`
   - Threshold lines:
     - Warning: `0.85`
     - Critical: `0.80` (SLO floor)

## SLO table widget (recommended for rubric)

Add one compact table (or stat group) summarizing SLO status:
- `latency_p95_ms <= 3000`
- `error_rate_pct <= 2.0`
- `daily_cost_usd <= 2.5`
- `quality_score_avg >= 0.80`

Display columns:
- current value
- target
- compliance status (green/yellow/red)
- 1h trend
