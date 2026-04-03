# Philosophy

## The dream

A horde of agents who know what to do and validate each other's work better
than a team of humans would. They run unattended. They find real problems,
write actionable issues, implement correct fixes, and open PRs that pass
review. The human reviews a PR occasionally — not a conversation at every step.

This is not about automating the easy parts. It is about building loops that
are trustworthy enough to run without supervision.

---

## Why unattended operation requires deterministic coordination

An interactive agent can recover from a bad decision because a human is
watching. An unattended loop cannot. If the control flow lives in the agent's
interpretation of markdown, a misread instruction skips a step with no signal.
A scheduled run that silently fails provides false confidence.

The coordinator is Python. It decides what runs next. It validates structured
output before passing it to the next step. It escalates when a loop does not
converge. The agent is not trusted to sequence itself.

This is the core constraint: **intelligence lives in prompts, sequencing lives
in code.**

---

## Why fresh context per step

A multi-step pipeline running in a single agent session accumulates context.
Step 4 sees the output of steps 1–3 even when it shouldn't. The agent's
attention spreads across a growing window of partially-relevant information.
Quality degrades.

Each `claude -p` call is a new process with a clean context window. The
implementer only sees the issue. The reviewer only sees the implementation.
The triage agent only sees the raw findings. Each agent gets exactly what it
needs — nothing carried over from earlier steps that might distort its judgment.

---

## Why GitHub issues as the scan/fix handoff

Scan and fix have different rhythms. Scans might run nightly. Fix loops might
run on demand, or on a different schedule, or against a subset of issues.
Coupling them directly would force them to run together.

GitHub issues are neutral ground. Scan writes issues; fix reads them. Either
side can be replaced, improved, or paused without touching the other. The
interface is public and inspectable — you can read the issues, close them
manually, or add them by hand. Nothing is hidden in internal state.

---

## Why scan config is the primary extension point

The loops are fixed infrastructure. What varies — and what makes the system
useful — is the scan configuration. A scan type is a prompt that defines what
to look for. A scan block in `projects.json` calibrates that prompt to a
specific project: what counts as normal, what should become an issue, what is
known noise to skip.

These two dimensions are independent. You can add a new scan type (a new
prompt file) without touching any project config. You can add a new project
without writing any new prompts. And you can tune a project's calibration
without touching the loop machinery.

The result is a library of scan types that any project can opt into, each
configured for that project's specific characteristics. A logs scan for one
project might flag errors above 10/hour; for a high-traffic service, the
threshold might be 100/hour. The same prompt, different calibration. This
is why `normal`, `flag`, and `ignore` are required fields — not optional
documentation. They are the mechanism by which general prompts become
project-specific intelligence.

---

## Why prompts are the intellectual property

The coordinator is ~100 lines of Python per loop. Its job is mechanical:
run this, validate that, pass this to the next step. The insight is not there.

The insight is in the prompts: what to look for in a codebase, how to cluster
findings, what makes an issue actionable, what a good review catches. These
are the distillation of judgment about what matters. They are the thing worth
investing in.

A prompt is also the right level of abstraction for evolving this system.
Adding a new scan type is adding a markdown file. Adding a new review criterion
is editing a prompt. Changing the output schema is changing the JSON example
in the prompt and the coordinator's expectation together. No framework, no
migration.

---

## Why the coordinator stays thin

Every line of coordinator code that isn't sequencing or validation is a line
that belongs in a prompt. Adding routing logic, retry strategies, state
management, or plugin systems to the coordinator is the same mistake as
building a web dashboard: engineering around the analytical value rather than
toward it.

When the coordinator grows beyond what you can read in five minutes, something
has gone wrong. Complexity belongs in prompts, where it is visible, editable,
and testable by running the loop.
