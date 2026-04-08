# Deduplicate Against Open Issues

Decide whether each candidate issue should be posted, added as a comment
on an existing issue, or skipped.

## Input

You will receive JSON with two keys:

- **`candidates`** — issues approved by the reviewer, ready to post.
- **`open_issues`** — all currently open issues in the repository (number,
  title, body). These include both human-filed and autonomously-created issues.

## Instructions

For each candidate, compare it against every open issue. Consider titles,
body content, and the underlying problem — not just surface wording. Then
choose one action:

| Action      | When to use                                                        |
| ----------- | ------------------------------------------------------------------ |
| **post**    | The candidate describes a genuinely distinct problem.              |
| **comment** | The candidate overlaps an existing issue, and the new observations add useful context that the existing issue does not already contain. |
| **skip**    | The candidate is a near-duplicate of an existing issue with nothing new to add. |

### Guidance

- **Semantic, not lexical.** "Subprocess failures surface as cryptic
  JSONDecodeError" and "JSONDecodeError hides real subprocess errors" are the
  same problem even though the titles differ.
- **Partial overlap → comment.** If the candidate adds new evidence, a new
  reproduction path, or a new angle on a known problem, choose `comment` so
  the context enriches the existing issue.
- **Comment body is concise.** Write the comment as a short update — new
  evidence only, not a restatement of the existing issue. Start with
  `**New observations from scan:**` so it's visually distinct.
- **When in doubt, comment rather than post.** A comment on an existing issue
  is cheap to ignore; a duplicate issue splits attention.
- **One candidate = one action.** Never split a candidate across multiple
  existing issues.

## Output format

Write your output as JSON to the file path provided by the coordinator.

Include `reflections` — a list of brief observations about this step: what
context was missing or ambiguous, what caused hesitation or retries, what
would have made this step faster or more accurate. Return `[]` if you have
nothing to add.

```json
{
  "actions": [
    {
      "action": "post",
      "title": "...",
      "body": "...",
      "label": "..."
    },
    {
      "action": "comment",
      "target_issue": 42,
      "comment_body": "**New observations from scan:**\n\n...",
      "reason": "brief explanation of the overlap"
    },
    {
      "action": "skip",
      "title": "...",
      "reason": "brief explanation of why this is a duplicate"
    }
  ],
  "reflections": []
}
```
