# Design Decisions

---

## Prompts + scripts over a web dashboard

**Decision**: No UI. Agent prompts for analysis and interpretation; optional
single-file Python scripts for pre-aggregating structured/high-volume data.

**Why**: A dashboard requires building and maintaining a rendering layer that
adds no analytical value. An LLM can interpret raw or lightly aggregated data
and surface recommendations directly. The 80/20 is dramatically better: days
of effort vs weeks, with higher-quality output (interpretation, not just display).

**Scripts when**: Raw data volume would waste token budget or slow the agent
down. A 20-line script that aggregates 200 log lines into 5 rows earns its place.
Not required for every question — prompts alone are fine to start.

---

## TOML project registry

**Decision**: `vitals.config.toml` as the single source of truth for monitored
projects and where their data lives.

**Why**: TOML is readable for hand-authoring, handles nested arrays of objects
cleanly, and avoids YAML's indentation sensitivity and edge cases. Python 3.11+
has `tomllib` built in; no extra dependency needed.

**Scope**: The registry holds non-secret config (project IDs, dataset names,
log selectors, source types). Secrets are in `secrets.env` (gitignored), resolved
at runtime via `op run`.

---

## 1Password via `op run`

**Decision**: Secrets injected as env vars via `op run --env-file=secrets.env -- <cmd>`.
Scripts and agents read `os.environ` only — no SDK, no secrets on disk.

**Why**: Complete decoupling from 1Password at the code level. Portable — swap
1Password for any other secret manager by changing `secrets.env`, not code.
Secrets exist only in the process environment for the lifetime of the run.

**Setup**: `secrets.env` (gitignored) maps env var names to `op://` paths.
`vitals.config.toml` references env var names (e.g. `"${AXIOM_TOKEN}"`).

---

## Python + uv run for scripts

**Decision**: Single-file Python scripts with inline `uv` dependencies. No
package management, no virtualenvs to maintain, no build step.

**Why**: Scripts are utilities, not a product. `uv run script.py` handles deps
inline. Python has first-class support for every data source we care about
(Axiom, GCP, Grafana). Easy to read, easy to modify, no TypeScript compilation.

---

## Prompts-first, scripts when earned

**Decision**: Start with markdown prompts that describe what to query and how
to interpret results. Add a deterministic script only when it demonstrably
saves tokens or agent time.

**Why**: Premature scripting creates maintenance burden for questions that may
evolve. A prompt is easier to refine than code. Scripts are written once the
question is stable and the data volume justifies it.

---

## Vitals vs Agency

**Decision**: Keep as separate repos with distinct purposes.

**Why**: Vitals is for *knowing* — monitoring, awareness, analysis. Agency is
for *doing* — autonomous implementation, fix loops, PRs. They compose naturally
(vitals surfaces something → agency acts on it) but have different inputs,
outputs, and rhythms. Merging would muddy both.
