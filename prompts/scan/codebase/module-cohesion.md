# Scan: Module Cohesion

Scan a codebase for functions or classes that live in the wrong module.

## Instructions

Explore the codebase at the path provided in the project config. Look for:

- **Name mismatch**: a function or class whose name contains domain
  vocabulary that does not appear in its module's name, while a module
  named after that domain already exists elsewhere in the same package
- **Single-caller misplacement**: a function in a shared or utility
  module whose only call site is a single more-specific module —
  suggesting it is an implementation detail of that module, not a
  general-purpose utility
- **Concept leakage**: a utility module whose docstring or stated purpose
  is general-purpose, but which contains logic that encodes knowledge
  about a specific domain (particular label names, agent prompt paths,
  loop-specific data shapes, etc.)

A finding is worth reporting only when at least two of these signals
coincide — a name mismatch alone is weak; a single-caller violation
alone may just be an unused helper. The combination is strong.

Do not flag:
- Functions that are legitimately general even if currently called from
  one place (e.g. a utility that *could* be reused and has a generic
  name)
- Private helpers (leading underscore) that already live inside the
  module they serve

## How to explore

1. Read the module docstrings (or first few lines) of all files in the
   shared/common package to understand each module's stated purpose.
2. For each public function in those modules, check whether its name
   contains vocabulary that maps to a more specific module.
3. For functions that fail the name check, use Grep to find all call
   sites and confirm whether there is only one caller.
4. Read the function body to check for concept leakage (hard-coded
   domain strings, imports of domain-specific modules, etc.).

## Output format

Write your output as JSON to the file path provided by the coordinator.

Include `reflections` — a list of brief observations about this step:
what context was missing or ambiguous, what caused hesitation or
retries, what would have made this step faster or more accurate. Return
`[]` if you have nothing to add.

```json
{
  "findings": [
    {
      "pattern": "brief label for this type of misplacement",
      "location": "file path and line range of the misplaced definition",
      "description": "which signals fired, where the code belongs instead, and why",
      "severity": "high | medium | low",
      "sample": "the misplaced definition verbatim"
    }
  ],
  "reflections": []
}
```

If nothing worth flagging is found, return `{ "findings": [], "reflections": [] }`.
