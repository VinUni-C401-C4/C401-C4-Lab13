# Langfuse Observability Best Practices

This app follows Langfuse best practices for tracing:

## Trace Naming
- Use descriptive names: `api.chat`, `agent.run`, `agent.retrieve`, `agent.generate`
- Names should reflect the operation, not generic "trace-1"

## Span Hierarchy
- Nested spans for multi-step operations
- `api.chat` → `agent.run` → `agent.retrieve`, `agent.generate`

## Sensitive Data
- PII masked with `hash_user_id()` for user_id
- Only relevant data captured: `summarize_text()` for previews

## Flush Traces
- Always call `flush_traces()` in scripts before exit
- FastAPI app has shutdown hook to flush traces

## Context
- session_id for conversation grouping
- user_id (hashed) for user filtering
- tags for feature/model tracking
