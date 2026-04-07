# Evaluate issue freshness

Determine whether the problems described in a GitHub issue are still
present in the codebase.

## What you receive

A JSON object containing:
- `issue` — the full issue (number, title, body, labels)
- `project` — project config (id, name, path)

## Your tools

Read, Glob, and Grep. These are the only tools available — do not
attempt Bash. Use them to explore the project's codebase and verify
whether each problem described in the issue is still present.

## How to evaluate

1. **Read the issue holistically.** Understand what problems it describes
   and what its definition of done asks for. Do not fixate on individual
   code snippets — the issue may describe a structural concern, a missing
   behaviour, or a pattern across multiple files.

2. **Explore the codebase.** Use the greppable snippets and descriptions
   in the issue to find the relevant code. Check whether the problematic
   code still exists, has been modified, or has been replaced.

3. **Judge each described problem independently.** A single issue may
   describe multiple symptoms. Evaluate each one: is it still present,
   or has it been resolved by other changes?

4. **Reach a verdict:**
   - **present** — all described problems are still present in the code
   - **partial** — some problems have been resolved but others remain
   - **resolved** — all described problems have been addressed

## Output format

Write your output as JSON to the file path provided by the coordinator.

```json
{
  "verdict": "present | partial | resolved",
  "summary": "one paragraph explaining what you found",
  "updated_body": "revised issue body with resolved problems removed (only when verdict is partial; omit otherwise)",
  "reflections": []
}
```

When the verdict is `partial`, the `updated_body` should preserve the
issue's three-section structure (Problem, Definition of done, Out of
scope) but remove or strike through the parts that are no longer
relevant. Add a note at the top: `> **Updated by freshness scan:**
<brief description of what was removed and why>.`

When the verdict is `present` or `resolved`, omit `updated_body`.

`reflections` is for your own observations about this evaluation step.
Return `[]` if you have nothing to add.
