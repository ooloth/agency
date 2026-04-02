# Roadmap

## Phase 1: Foundation (current)

- [x] Project registry (`vitals.config.toml`)
- [x] Auth strategy docs (GCP ADC, Axiom token, Grafana)
- [x] Secrets management via `op run`
- [ ] Generic log analysis prompt
- [ ] First working agent invocation against a real project

## Phase 2: Coverage

- [ ] Per-project context docs (what's normal, what to ignore)
- [ ] Error analysis prompt refined with real results
- [ ] Additional question types: deployments, costs, usage patterns
- [ ] Scripts where pre-aggregation earns its place (Axiom, GCP)

## Phase 3: Scheduling

- [ ] launchd / cron job for daily briefing
- [ ] Delivery mechanism (Slack DM, email, or file)

## Phase 4: Breadth

- [ ] GitHub PRs prompt (open PRs, PRs to review, recent comments)
- [ ] Tasks prompt (Linear, Trekker, GitHub Issues)
- [ ] Cost monitoring prompt (GCP, cloud spend)

## Phase 5: Action

- [ ] Handoff to Agency for issues worth fixing
- [ ] Kick off implementation work from a vitals finding
