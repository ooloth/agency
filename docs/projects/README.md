# docs/projects/

One markdown file per monitored project (named `<project-id>.md`, matching
the `id` field in `projects/projects.json`).

These files are automatically injected as context into every scan and fix
prompt for that project. Write them for an agent audience, not a human one.

## What belongs here

- **Doc map**: where the project's documentation lives and what each location
  is for — helps agents navigate unfamiliar repo layouts
- **Structural quirks**: anything about the project's layout or conventions
  that differs from what an agent would expect by default
- **Category distinctions**: if the project has multiple doc types that
  could be confused (e.g. docs about the system vs. docs about things the
  system monitors), explain the distinction explicitly

## What does not belong here

- Scan-specific instructions ("when scanning for X, do Y") — those belong
  in the scan prompt or the scan's `normal`/`flag`/`ignore` config
- Point-in-time state ("as of April 2026...") — put time-sensitive context
  in the scan config's `ignore` field, where it can be updated alongside
  the code
- Generic guidance that applies to any project — that belongs in the scan
  or fix prompt itself
