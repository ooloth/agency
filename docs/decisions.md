# Design Decisions

---

## Deterministic Python coordinator, not agent-driven control flow

**Decision**: Loops are sequenced by short Python functions. Each step is an
explicit `agent()` call. The coordinator decides what runs next based on
structured output.

**Why**: An unattended loop cannot recover from a bad decision the way an
interactive session can. If control flow lives in the agent's interpretation
of markdown, a misread skips a step silently. Python makes sequencing
auditable, testable, and predictable.

**Boundary**: The coordinator checks `ready`, `approved`, and `findings` — it
never interprets content. Routing logic that reads the substance of agent
output belongs in a prompt, not in Python.

---

## Fresh subprocess per step

**Decision**: Each agent step runs as a `claude -p` subprocess. No step
reuses a running session.

**Why**: A single session accumulates context across steps. The implementer
should not see the scan output; the reviewer should not see the implementation
history. Each agent gets exactly what the coordinator passes — nothing more.
Context contamination degrades quality in ways that are hard to diagnose.

---

## File-based output handoff

**Decision**: Agents write JSON output to a temp file path provided in the
prompt. The coordinator reads the file. Agents do not return results via
stdout.

**Why**: Parsing agent response text requires stripping markdown code fences
and is fragile when issue bodies contain embedded code blocks with their own
fences. A file write produces unambiguous, well-formed JSON. The agent uses
its native Write tool — no special output mode needed.

---

## GitHub issues as the scan/fix interface

**Decision**: Scan posts GitHub issues; fix reads them. This is the only
coupling between the two loops.

**Why**: Scan and fix have different rhythms and different failure modes. A
direct coupling would require them to run together and fail together. GitHub
issues are inspectable, manually editable, and independent of both loops.
Either side can be replaced without touching the other.

**Labels**: Issues posted by scan carry a `sev:*` label for severity and an
`agent` label so the fix loop can find them via `gh issue list --label agent`.

---

## TOML project registry

**Decision**: `projects/projects.toml` is the single source of truth for
monitored projects and where their data lives.

**Why**: TOML is readable for hand-authoring, handles nested arrays of objects
cleanly, and avoids YAML's indentation sensitivity. Python 3.11+ has `tomllib`
built in — no extra dependency.

**Scope**: The registry holds non-secret config only. Secrets are referenced
as env var names injected at runtime via `op run`.

---

## 1Password via `op run`

**Decision**: Secrets injected as env vars via
`op run --env-file=secrets.env -- python run.py <cmd>`.
Coordinator and agents read `os.environ` only — no SDK, no secrets on disk.

**Why**: Complete decoupling from 1Password at the code level. Swap secret
managers by changing `secrets.env`, not code. Secrets exist only in the
process environment for the lifetime of the run.

---

## Prompts as the primary extension point

**Decision**: Adding a new scan type means adding a `prompts/scans/<type>.md`
file. Adding a new step means adding a prompt and one `agent()` call.

**Why**: A prompt is the right level of abstraction for evolving analytical
judgment. It is readable, diffable, and testable by running the loop.
Encapsulating the same logic in Python would make it harder to read and
require a code change to adjust what the agent looks for.

---

## No web UI, no API, no database

**Decision**: This is a terminal tool. It reads files, calls `claude -p`,
and posts to GitHub. Nothing else.

**Why**: A rendering layer adds no analytical value. An LLM can interpret raw
or lightly aggregated data and surface findings directly. The operational
simplicity — run from cron, inspect via `gh issue list` — is a feature. Any
server component changes the deployment model, adds auth requirements, and
creates infrastructure to maintain.
