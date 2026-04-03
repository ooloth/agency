# Playbooks

Step-by-step instructions for common operational tasks.

---

## Add a new project

1. Add an entry to `projects/projects.toml`:

   ```toml
   [[projects]]
   id = "my-project"
   name = "My Project"
   scans = ["codebase"]          # or ["logs"], or both
   path = "~/Repos/me/my-project"  # required for codebase scans
   ```

2. Create `projects/my-project/context.md`. Include:
   - What the project does
   - What counts as normal (log volume, error rate, etc.)
   - What to ignore (known noise, expected errors)
   - What to flag urgently

3. If the project uses log scanning, add a `[[projects.logs]]` block:

   ```toml
     [[projects.logs]]
     source = "axiom"
     dataset = "my-dataset"
     token = "${MY_TOKEN}"
   ```
   Add the corresponding `MY_TOKEN=op://...` line to `secrets.env`.

4. Run a dry-run scan to verify:

   ```bash
   python run.py scan my-project --type codebase --dry-run
   ```

---

## Add a new scan type

1. Create `prompts/scans/<type>.md`. Follow the contract:
   - Instructions for what to look for and how
   - Output format: JSON written to the file path provided by the coordinator
   - Schema: `{ "findings": [ { "pattern", "description", "severity", "sample" } ] }`

2. Add the scan type to relevant projects in `projects.toml`:

   ```toml
   scans = ["codebase", "my-type"]
   ```

3. Run a dry-run scan to validate output quality before enabling for real.

---

## Run the fix loop on an issue

1. Ensure the issue is labelled `agent` in GitHub so the fix loop can find it.

2. Run:
   ```bash
   python run.py fix --issue <number>
   ```
   Or let it pick the next open `agent`-labelled issue:
   ```bash
   python run.py fix
   ```

3. The loop will implement, review, and revise until approved or escalated.
   Watch the streaming output to follow progress.

4. If the loop escalates (exits non-zero), check the issue for complexity that
   requires human judgment, then either simplify the issue scope or handle it
   manually.

---

## Handle a scan that posts duplicate issues

The scan loop does not yet deduplicate against existing open issues. Until that
is implemented (see roadmap):

1. Close the duplicate in GitHub manually.
2. Add a note to `projects/<id>/context.md` describing the pattern so the scan
   agent learns to recognise it as already-tracked.

---

## Debug a failed agent step

Agent steps stream output to the terminal. If a step fails:

1. Look at the streaming output just before the failure — the agent usually
   explains what it attempted.

2. Check whether the temp file was written:
   ```bash
   ls /tmp/*.json
   ```
   If no file exists, the agent hit its `--max-turns` limit or encountered a
   tool error before writing output.

3. Re-run with a higher `max_turns` if the agent ran out of turns:
   Edit the `agent()` call in the relevant coordinator and increase the default.

4. If the output file exists but is malformed JSON, inspect it:
   ```bash
   cat /tmp/<file>.json
   ```
   The agent may have written a partial result before a tool call failed.
