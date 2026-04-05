# Draft Issues

Write GitHub issue drafts from triaged findings.

## Instructions

You will receive triaged clusters. For each cluster that warrants a GitHub
issue, write a clear, actionable issue using the three-section structure below.

## Structure

### Problem

One paragraph: what is wrong and why it matters. Include the problematic code
verbatim inline as evidence — greppable, so the implementer can find it by
searching rather than by trusting a file path or line number that may have
shifted.

### Definition of done

Describe what the fixed state looks like from the outside. Frame it as:
*"you know this is fixed when..."* — observable outcomes, not implementation
prescriptions. This is not an exhaustive checklist; it is the key proof that
the problem is gone. Implementers and reviewers can go beyond it.

### Out of scope

What not to change. Protects the implementer from over-engineering and the
reviewer from scope creep. Be specific — name the related concerns that are
tracked elsewhere or intentionally deferred.

---

## Rules

**Reference by snippet, never by location.** File paths and line numbers go
stale the moment any other issue is resolved. The code snippet is stable.

**Definition of done is outside-in.** Each proof point describes something
you can observe by running the code — not something you can verify by reading
it. "Run X, see Y" not "the code now does Z."

Two failure forms to avoid:

- **Source-state description** (documentation issues): "the file now reads X"
  or "the section has been updated to say Y" — these describe what the source
  looks like, not what you observe when running the code. Fix: name the
  command and the output you'd see.
  - Bad: "the Architecture section now describes the new module layout"
  - Good: "grep for `loops/common/agent` in `docs/architecture.md`; the
    result names the unified agent module"

- **Implementation description** (code issues): "retains only X
  functionality" or "the function now returns Y" — these describe the
  implementation, not observable behaviour. Fix: describe what a caller
  sees or what a test asserts.
  - Bad: "the function retains only the error-handling path"
  - Good: "pass a non-JSON string as output; observe an error that includes
    the raw string and names the step that failed"

**Titles name the problem, not the solution.** A good title makes the problem
legible; a bad title prescribes the fix. "Subprocess failures surface as
cryptic JSONDecodeError" is better than "Add check=True to subprocess calls."

---

## Output format

Write your output as JSON to the file path provided by the coordinator.

Include `reflections` — a list of brief observations about **your own drafting decisions**: what context was missing or ambiguous, what caused hesitation or retries, what would have made this step faster or more accurate. If you are redrafting in response to review feedback, report what was hard to reformulate and why — not the reviewer's observations, which are already captured elsewhere. Return `[]` if you have nothing to add.

```json
{
  "issues": [
    {
      "title": "short, specific problem statement — not a solution",
      "body": "markdown body following the three-section structure above",
      "label": "sev:critical | sev:high | sev:medium | sev:low"
    }
  ],
  "reflections": []
}
```

One cluster = one issue. Do not bundle unrelated problems.
