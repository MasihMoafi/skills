---
name: harness-eng
description: "Use when designing, evaluating or simplifying an agent project harness: startup scripts, evaluator rubrics, mechanical guardrails and the evaluation loop. The project docs themselves follow the project-docs skill."
---

# Harness Engineering

Use this skill to make an agent-run project easier to start, steer, verify, resume, and improve. Favor local project artifacts over chat-only guidance.

## Core stance

- Build a harness only around a real workflow the user wants repeated.
- Keep the injected instruction file short: it should be a table of contents, not an encyclopedia.
- Move durable knowledge into repo-local docs, scripts, checks, and templates.
- Encode high-value judgment as mechanical checks when possible.
- Every harness component should earn its keep through a clearer start, safer edit, stronger verification, or better handoff.

## First pass

1. Inspect the project locally: root files, existing docs, package scripts, tests, git state, and any existing session/progress files.
2. Identify the agent's repeated failure mode or bottleneck: startup, context discovery, feature selection, verification, review, handoff, architecture drift, or cleanup.
3. Choose the smallest harness surface that fixes that bottleneck.
4. Add or edit only the earmarked artifact. Do not scatter duplicate instructions.
5. Verify the harness by running the cheapest check that proves a future agent can follow it.

## Harness artifacts

The project docs (rules file, feature map, folder map, vision, current state) follow the `project-docs` skill; add no parallel progress, handoff or feature-list files. Add these only when they fit:

- `init.sh`: one command for setup, baseline verification and startup hints. It prints the cwd and fails clearly.
- `evaluator-rubric.md`: pass/fail scorecard for agent output quality; tune it against human judgment.
- Custom lints or tests: enforce dependency boundaries, schemas, logging, naming, file size or other rules agents keep breaking.

## Evaluation loop

For a new or changed harness, check:

1. Can a fresh agent find the right starting docs in under one minute?
2. Can it run the baseline verification without guessing commands?
3. Is there exactly one current priority or a clear selection rule?
4. Is "done" tied to evidence, not confidence?
5. Is stale or duplicate guidance avoided?
6. Can the harness be simplified without quality dropping?

If unsure whether a component is still needed, take a quality snapshot, remove or bypass one component, run the benchmark/task suite, compare results, and keep the simpler version only if quality does not drop.

## Further reading

Adapted in part from the "Learn Harness Engineering" material at https://walkinglabs.github.io/learn-harness-engineering/en/skills/.
