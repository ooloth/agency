# Log Sniffer

Scan logs for a given project and surface anything worth paying attention to.

## Your job

1. Query the project's logs for the relevant time window
2. Group similar errors/warnings by message pattern
3. Identify anything unusual, new, or worsening
4. Give a short, direct summary with recommendations

## What to look for

- **Errors**: anything at `error` or `fatal` level
- **Warnings**: spikes or new patterns at `warn` level worth flagging
- **Anomalies**: sudden increases in log volume, new error types, recurring failures
- **Silence**: if a service that normally logs has gone quiet, flag it

## How to query

Find the project's log source in `vitals.config.toml`. Then:

### Axiom

Use the Axiom web UI or CLI. Key APL patterns:

```apl
# Error summary grouped by message
['<dataset>']
| where level in ("error", "ERROR", "fatal", "FATAL")
| summarize count(), min(_time), max(_time) by message
| order by count_ desc

# Recent errors in full
['<dataset>']
| where level in ("error", "ERROR", "fatal", "FATAL")
| order by _time desc
| limit 50
```

Note: free tier restricts API query range. Use the Axiom web UI for older data.

### Google Cloud Logging

```bash
gcloud logging read 'severity>=ERROR' \
  --project=<project-id> \
  --freshness=24h \
  --limit=100 \
  --format=json
```

ADC handles auth automatically after `gcloud auth application-default login`.

### Grafana Loki

Use LogQL in the Grafana UI or via the Loki API:

```logql
{app="<app-label>"} |= "error" | pattern `<_> level=<level> <_> msg=<msg>`
```

See `docs/architecture/auth.md` for Grafana auth options.

## Output format

Keep it short. Prefer this shape:

```
Project: <name>
Period: <time window>

Summary: <1-2 sentences on overall health>

Issues:
- <error message or pattern> — <count> occurrences, first seen <time>, last seen <time>
  → <recommendation>

Nothing to flag: <categories that look clean>
```

If there's nothing to flag, say so clearly. "No errors in this period" is a
useful signal too.
