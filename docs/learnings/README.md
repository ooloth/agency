# Learnings

Discoveries made while running the loops — things that surprised us, things
that didn't work the way we expected, and adjustments made as a result.

---

## Parsing agent output via stdout is fragile

**What happened**: The first implementation of `agent()` used
`--output-format json` and parsed `outer["result"]` from the Claude CLI
envelope. When issue bodies contained embedded code blocks, the markdown
fence-stripping logic found an inner ` ``` ` instead of the outer closing
fence and produced a `JSONDecodeError`.

**What we learned**: Agent text output is not a reliable JSON transport once
prompts produce content with embedded markdown. The output format is not under
our control.

**What changed**: Agents now write JSON to a temp file path provided in the
prompt. The coordinator reads the file. No text parsing required.

---

## `claude -p` has full tool access in non-interactive mode

**What we assumed**: Print mode might be read-only or have reduced tool
access.

**What we found**: `claude -p` has the same tool access as interactive mode —
read files, write files, run bash commands. The Write tool works exactly as
expected when the agent is asked to write JSON to a file path.

---

## Print order requires explicit flushing

**What happened**: Coordinator progress lines (`[scan] finding problems...`)
appeared *after* the subprocess output they were meant to precede, because
Python buffers stdout while subprocess streams directly to the terminal.

**What changed**: All coordinator `print()` calls that precede a subprocess
now use `flush=True`.

---

## Scan loop convergence on first review round is common

**What we found**: The `review-issues.md` prompt with the two rules (snippet
references, observable-outcome AC) typically passes on the first round. The
feedback loop is insurance, not the common path.

**Implication**: Five rounds is a generous default. If a scan consistently
needs more than two rounds, the drafting prompt needs improvement, not more
rounds.
