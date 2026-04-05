# Per-role `--allowedTools` for agent subprocesses

**Decision**: The implement agent is granted `Bash Read Write Edit Glob Grep`.
The reviewer is granted `Read Glob Grep` only.

**Why**: Granting every tool to every agent is both unnecessary and risky. The
reviewer has no legitimate reason to write files or run commands — restricting
it to read-only tools enforces this at the permission layer, not just by prompt
instruction. The implement agent needs `Bash` for git operations. `--allowedTools`
is required in `-p` mode because omitting it means "prompt for approval",
which silently never runs in a non-interactive subprocess.

**Boundary**: If a new agent step is added, its tool list should be the
minimum required for its job. Start restrictive and expand if needed.
