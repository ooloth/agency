# Questions

The questions vitals is designed to answer, grouped by category. Each maps to
one or more agent prompts and optionally a supporting script.

---

## Errors

What errors are occurring across a project's logs, how frequently, and is the
situation improving or worsening?

**Agent**: `agents/log-sniffer.md`

**Supported log sources**: Axiom, Google Cloud Logging, Grafana Loki

---

## Future questions (ideas)

- **Deployments** — recent deploy history, success/failure rate
- **Latency** — p50/p95/p99 response times, trends
- **Uptime** — is it up? recent incidents
- **Usage** — active users, request volume, growth patterns
- **Cost** — cloud spend, anomalies
- **DB health** — slow queries, connection pool, table sizes
- **Background jobs** — queue depth, failure rate, processing lag
- **PRs** — open PRs, PRs awaiting review, recent comments
- **Tasks** — open issues across Linear, GitHub, Trekker
