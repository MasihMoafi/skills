---
name: project-docs
description: Use when entering an unfamiliar project, when creating or repairing a project's agent docs (AGENTS.md, feature map, lat.md folder map, VISION.md, ES.md), or when the workspace check reports doc problems.
---

# Project docs

Before changing anything, learn what the project is, where things live and what state it is in. Each of those facts has exactly one home.

## One file per job

- `AGENTS.md` (with `CLAUDE.md` = `@AGENTS.md`, so every agent loads it): how to behave in this project. Project rules plus pointers to the files below; at most 60 lines.
- Feature map, `.agents/skills/verify-<app>/features/` (linked from `.claude/skills/`): one file per user-facing feature with how to reach it, how to drive it, its code and its gotchas. Create it with `create-verification-skill`; keep it true with `maintain-verification-skill`.
- Folder map, `lat.md/workspace.md`: every top-level item and why it exists; `lat check` validates the links and `.alint.yml` rejects files it doesn't list.
- `VISION.md`: identity in one line, `## Thesis` (why it exists, what bet it makes) and `## Non-goals`; at most 25 lines. No map, state or evidence.
- `ES.md`: the current state under `## Now`, `## Next`, `## Broken` and `## Open decisions`, with "(updated YYYY-MM-DD)" in its title; at most 40 lines. Rewrite it in place; never append a log.
- Evidence (hashes, run IDs, verification prose) goes to `reports/` or commit messages, never into these files.

These files are local working notes: keep them out of public git, and link them into new worktrees.

## Read in this order

`AGENTS.md` (already loaded), then `ES.md`, then the feature file for the task. Use the folder map before adding a file, and `VISION.md` when scope is in question. The README verifies or supplements these; it never replaces them.

## Keep them true

- Change a fact in its one home only; point to it from elsewhere instead of copying it.
- When a doc contradicts the code or another doc, check the code, fix or delete the wrong text, and say what you changed.
- Before deleting old text, move each still-valid lesson or prohibition to the matching feature's Gotchas or to `AGENTS.md`.

## Harness beyond the docs

Add a harness component only around a workflow the user repeats, and only the smallest one that fixes the agent's bottleneck: `init.sh` (setup, baseline check, startup hints, prints the cwd), `evaluator-rubric.md` (pass/fail scorecard tuned against human judgment), or a lint or test for a rule agents keep breaking. Verify it by running the cheapest check that proves a fresh agent can follow it. When unsure a component is still needed, remove it, run the task suite, and keep the simpler version if quality holds.

## Create the layout when absent

Inspect the project two levels deep, draft the missing files in the shape above, and show the user `VISION.md` before saving it. Exemplar: this library's `VISION.md`.
