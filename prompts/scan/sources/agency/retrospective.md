# Agency retrospective scan

Review recent agency run data and surface patterns worth acting on.

## What you receive

A JSON object with the standard scan calibration:
- `normal` — patterns expected and not worth flagging
- `flag` — patterns that indicate a systemic problem worth a GitHub issue
- `ignore` — specific known issues to skip

## Your tools

Use Read, Glob, and Grep to navigate `.logs/` run directories. Each run
directory contains:

- `metadata.json` — run type, project, scan type or issue number, step
  durations, convergence result, total duration, exit code
- `reflections.json` — list of `{"step": name, "text": observation}` entries
  collected from each step's output
- `{step}-transcript.jsonl` — raw stream-json lines from the Claude subprocess;
  use this to see exactly what the agent did and said during that step
- `{step}.json` — structured JSON output from each step (find, triage, draft,
  review-N, redraft-N, implement-N, etc.)

## How to approach this

1. **Enumerate recent runs.** Use Glob to list recent directories under `.logs/`.
   Read `metadata.json` from each to get an overview (run type, converged?,
   duration, step count).

2. **Look for patterns across runs** — not one-off anomalies, but the same
   failure mode appearing in multiple runs. Focus on:
   - Non-convergence: runs where `converged: false`
   - Excessive rounds: scan or fix runs with unusually high round counts
   - Repeated reflections: the same observation appearing across multiple steps
     or runs (agent asking for missing context, expressing ambiguity, etc.)
   - Review rejections for the same rule violation across multiple drafts
   - Wasted work: triage or draft rounds that seem to repeat without progress

3. **Read transcripts selectively.** Don't read every transcript. Use the
   metadata and step JSONs to identify which steps are worth deeper inspection,
   then read those transcripts to understand what actually happened.

4. **Reason structurally.** When you find a pattern, ask: why did this happen?
   The right remedy is almost never "remind the agent." It is usually:
   - This should be done deterministically in Python before/after the agent step
   - The prompt was missing context the agent needed
   - The output schema allowed ambiguity the agent resolved incorrectly
   - The loop structure created a situation the agent couldn't handle

## Output format

```json
{
  "findings": [
    {
      "title": "...",
      "body": "**Problem**\n...\n\n**Definition of done**\n...\n\n**Out of scope**\n..."
    }
  ],
  "reflections": []
}
```

`findings` follows the standard scan format — one entry per distinct actionable
pattern. Empty array if nothing warrants a GitHub issue.

`reflections` is for your own observations about this scan step (what was
missing, what would have helped). Usually empty.
