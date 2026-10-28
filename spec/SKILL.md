---
name: spec
description: Use for nontrivial implementation, requirements, a PRD or vision document, or acceptance criteria. Defines done before code. Not for trivial edits, exploration, spikes or prototypes.
---

# Spec-Driven Development

Define what done means before code is generated, because an agent silently fills any gap in intent from its training data.

Right-size the loop to the work. A small, well-understood change can use a short spec and plan in one session. For discovery, use a focused prompt, Plan Mode or a throwaway spike first; specify the production change once its behavior is known. A spec adds no approval gate; ask only about material gaps in intent.

The loop: **Specify, Plan, Execute, Verify, Integrate, Learn.** Return to Specify or Plan whenever the evidence changes the intent or the approach.

## 1. Specify

State exactly what must be true when the work is done. Make the happy path observable; "feature works" is not a criterion. Add the risk criteria relevant to the change, and all four when it touches money, data, security or external integrations:

1. **Failure mode:** what happens when a dependency or write fails (*"If the write fails, restore UI state and show an error without clearing the form"*).
2. **Concurrency:** what happens when actors or async events collide (*"Toggling a preference does not affect notifications already queued"*).
3. **Observability:** how production behavior is measured, with a metric or threshold where useful.
4. **Rollback:** how the earlier behavior is restored and verified.

When the intent has gaps, interview the user instead of guessing:

> *"I want to build [1-3 sentences]. Before writing anything, ask me as many questions as you need to write a complete spec: goal, context, constraints, acceptance criteria and non-goals. Cover trade-offs, edge cases, failure modes and concurrency where relevant. Do not write the spec until I tell you to."*

Keep the artifacts under version control and reachable from the code they govern: in `specs/NNN-feature-name/`, `docs/specs/` or beside the code.

```markdown
# SPEC: [Feature Name]

## Goal
[1-3 sentences: the problem and the outcome for the user or business]

## Context and Architecture Invariants
- [Services, databases or contracts involved; rules that must not break]

## Constraints
- [Stack restrictions, banned dependencies, latency or memory limits]

## Acceptance Criteria
- [ ] [Observable happy path]
- [ ] [Other independently testable behavior]
- [ ] [Relevant failure, concurrency, observability or rollback condition]

## Non-Goals
- [Behavior or features the agent must not touch]

## Stop Conditions
- [Four to six specific to this task, such as:]
- Stop and ask if two valid approaches conflict in architecture fit.
- Stop and ask if a test still fails after 3 fix attempts.
- Stop and ask before deleting or migrating data outside a test environment.
```

## 2. Plan

The agent reads `spec.md`, explores the codebase's conventions and writes `plan.md` with no implementation code; the user reviews it only when a decision is theirs.

```markdown
# PLAN: [Feature Name]

## Approach
[Strategy grounded in the existing architecture]

## Trade-Offs Considered
- [A vs B]: why A, and what it gives up.

## Files Affected
- `path/to/file.ts`: [nature of change]

## Sequencing
1. [Prerequisite, such as a migration]
2. [Core logic or endpoints]
3. [UI and integration tests]
```

Then decompose `plan.md` into `tasks.md`: one atomic change per task, ordered by dependency, each small enough for one session. A done-check is binary and observable, such as a passing test or a command's output; if it needs "and" more than once, split the task. Rate each task on two independent axes: **importance** (Foundational, Important, Nice-to-have) expresses value; **difficulty** (Easy, Medium, Hard) routes the implementation.

```markdown
# TASKS: [Feature Name]

## Phase 1: Backend
- [ ] 1.1 [Task] (Foundational, Medium)
  **Done when:** [endpoint returns 200 on a valid token, 401 without one]
```

For high-risk or stateful work, add `risks.md`, `rollback.md` or `adr.md`. An optional `implementation_notes.md` carries surprising legacy behavior, workarounds and discoveries across turns.

## 3. Execute

Hand the agent `spec.md`, `plan.md` and `tasks.md`. Run one task per fresh session when a combined diff would be too large to review or context rot is a real risk; otherwise run the whole list in one session. Mark `[x]` as each done-check passes. When reality contradicts the spec, stop, update `spec.md` and, if needed, `plan.md`, then resume.

## 4. Verify

Every applicable project gate must pass before you advance: linting, type checking, unit tests and relevant integration tests. Evidence ranks in ascending trust:

1. Agent claim: untrusted by default.
2. Automated test or CI: necessary, never sufficient.
3. A real end-to-end run in a production-like environment.
4. The user's manual acceptance: the only thing that closes "done."

Name the level behind every completion claim. Give the user a plain test checklist, one bullet per behavior stating what to do and what must happen. The task is done only when the user has checked it against the agreed criteria.

## 5. Integrate and Learn

Prepare a reviewable local result. Create a PR or merge only within existing authorization, after the gates and review. Specs live in two tiers. The strategic tier stays current: system-wide rules (`AGENTS.md`), ADRs and architecture invariants. The tactical tier is history: each `specs/NNN-...` folder records intent at one point in time. After integration, decide what the evidence requires you to update: the current spec or plan, strategic rules or ADRs, done-checks, or follow-on work.

## Vision and requirements documents

A vision document or PRD states:

- **Thesis:** what the product is, in one line.
- **Purpose:** what problem it solves, and for whom.
- **Value:** each value proposition that is useful on its own.
- **Non-goals:** deferred and unsupported behavior, next to the goals.

Keep the stable vision apart from current implementation status, and cross-reference the two.

Source: *AI-Native Software Engineering*, chapters 5 and 6.
