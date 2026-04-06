# Add a new project

1. Add an entry to `projects/projects.json`:

   ```json
   {
     "id": "my-project",
     "name": "My Project",
     "path": "~/Repos/me/my-project",
     "scans": []
   }
   ```

2. Add one scan block per scan type you want to run. Every scan block requires
   `normal`, `flag`, and `ignore` arrays calibrated for this project:

   ```json
   {
     "type": "codebase",
     "normal": ["...what healthy looks like"],
     "flag": ["...conditions that should become issues"],
     "ignore": ["...known noise to skip"]
   }
   ```

   For log scanning, also include the data source fields:

   ```json
   {
     "type": "logs",
     "source": "axiom",
     "dataset": "my-dataset",
     "token": "${MY_TOKEN}",
     "normal": ["..."],
     "flag": ["..."],
     "ignore": ["..."]
   }
   ```

   Add the corresponding `MY_TOKEN=op://...` line to `secrets.env`.

3. Optionally create `docs/projects/<project-id>.md` with context that will
   be injected into every scan and fix prompt for this project. Useful for
   projects with unusual layouts, multiple doc categories, or anything an
   agent would need to orient itself. See `docs/projects/README.md` for
   what belongs there.

4. Optionally add `install`, `checks`, and `tests` commands if the fix loop
   should verify the project's state before working:

   ```json
   "install": "uv sync",
   "tests":   "uv run --frozen pytest"
   ```

5. Run a dry-run scan to verify:

   ```bash
   uv run --frozen python run.py scan my-project --type codebase --dry-run
   ```
