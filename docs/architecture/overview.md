# Architecture

## What Vitals Is

A personal monitoring and awareness system. Aggregates answers to proactively
useful questions across personal and work projects — errors, deployments, costs,
usage patterns, PRs, tasks, etc. — via agent prompts and deterministic scripts.

Not a dashboard. Not a Sentry replacement. A growing collection of prompts and
scripts that help you know what's happening across your systems without having
to remember to check.

## Shape

```
vitals/
  vitals.config.toml     # project registry — all monitored projects + context
  agents/                # markdown prompts for agent-driven analysis
  scripts/               # optional uv run scripts for structured/high-volume data
  docs/                  # invariants, auth strategies, per-project context
  secrets.env.example    # op:// paths for secrets (never commit secrets.env)
```

## Core Abstractions

### Project Registry (`vitals.config.toml`)

The single source of truth for what's being monitored. Each project declares:
- Where its logs live (Axiom, GCP Logging, Grafana Loki, etc.)
- Where its deployments are tracked
- Any other data sources relevant to it

Agents and scripts read this file to know where to look.

### Agent Prompts (`agents/`)

Markdown files that define what an agent should do, how to interpret results,
and what to recommend. Written to be invoked via Claude Code skills or manually
referenced. Each prompt is self-contained — it describes both the question and
how to answer it.

### Scripts (`scripts/`)

Single-file Python scripts using `uv run` inline dependencies. Written only when
determinism or token efficiency matters — e.g. pre-aggregating 200 log lines into
a 5-row summary before handing to an agent. Not required for every question.

## Secrets

Secrets are never stored in files. `secrets.env` (gitignored) maps env var names
to `op://` paths. Everything runs via:

```bash
op run --env-file=secrets.env -- uv run scripts/foo.py
# or
op run --env-file=secrets.env -- claude ...
```

## Relationship to Agency

Vitals and Agency are complementary, not competing:

- **Vitals** answers: "what's happening, and should I care?"
- **Agency** answers: "what should be done, and can you do it?"

Vitals notices something worth acting on → hand it to Agency to investigate and fix.
Awareness → action.
