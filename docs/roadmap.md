# Roadmap

## Phase 1: Validated coordinator (current)

- [x] Thin Python coordinator with fresh-context-per-step via `claude -p`
- [x] Scan loop: find → triage → draft issues → review until ready → post
- [x] Fix loop: implement → review → revise with feedback → open PR
- [x] Dry-run mode for scan
- [x] End-to-end scan validated (codebase scan of vitals itself)
- [ ] Fix the 4 issues the scan found (#1, #2, #3, #4) — validates fix loop
- [ ] Harden reviewer prompt: pass actual diff, run tests, split intent vs correctness check
- [ ] Add issue deduplication to scan (check for existing open issues before posting)

## Phase 2: Schedulable scans

- [ ] launchd job for nightly scan runs
- [ ] Scan multiple projects and scan types in one run
- [ ] Per-project context docs for all monitored projects
- [ ] Log scan prompt (Axiom) validated against real data

## Phase 3: Trusted fix loop

- [ ] Fix loop validated end-to-end on real issues
- [ ] Adversarial reviewer: sees actual diff, runs tests, checks intent separately
- [ ] Escalation path: issues the fix loop can't resolve get flagged for human review
- [ ] Fix loop picks up issues automatically (no --issue flag needed)

## Phase 4: Breadth

- [ ] Additional scan types: deployments, costs, open PRs, dependency drift
- [ ] Additional fix types: config changes, dependency updates
- [ ] Multiple projects registered and scanning cleanly

## Phase 5: Scheduling fix loops

- [ ] Nightly or triggered fix runs (scan finds → fix loop acts)
- [ ] Human-in-the-loop escalation for low-confidence fixes
