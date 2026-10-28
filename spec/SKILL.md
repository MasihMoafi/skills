---
name: spec
description: Use for nontrivial implementation, requirements, a PRD or vision document, or acceptance criteria. Defines done before code. Not for trivial edits, exploration, spikes or prototypes.
---

# Spec-Driven Development

Code is perishable; a spec records intent, and intent lasts. An agent fills gaps silently from its training data, so the human sets the intent, boundaries and acceptance criteria before generation begins. (Source: *AI-Native Software Engineering*, chapters 5 and 6.)

Right-size the loop to the work. A small, well-understood change can use a short spec and plan in one session. For discovery, use a focused prompt, Plan Mode or a throwaway spike first; specify the production change once its behavior is known.

A spec or plan adds no approval gate to clear, authorized local work. Resolve material gaps in intent before implementing, and ask only about those gaps or about consequences outside the existing authorization.

The loop: **Specify, Plan, Execute, Verify, Integrate, Learn.** Return to Specify or Plan whenever the evidence changes the intent or the approach.

## 1. Specify

State exactly what must be true when the work is done. Avoid generic checks such as "feature works"; make the happy path observable. Add the risk criteria relevant to the change, and all four when it touches money, data, security or external integrations:

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
- Stop and ask if existing behavior contradicts the spec.
- Stop and ask before deleting or migrating data outside a test environment.
```

## 2. Plan

The agent prepares the plan; the user reviews it only when a decision is theirs.

> *"Read spec.md. Explore the codebase for its conventions on [concern]. Write plan.md: approach, trade-offs, files affected and sequencing. Write no implementation code."*

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

Then decompose:

> *"Read plan.md and write tasks.md. Make each task one atomic change with an objective done-check, ordered by dependency."*

Each task must fit one session and be verifiable on its own; if its done-check needs "and" more than once, split it. Done-checks are binary and observable, such as a passing test or a command's output.

Rate each task on two independent axes. **Importance** (Foundational, Important, Nice-to-have) expresses value; **difficulty** (Easy, Medium, Hard) routes the implementation. Do not confuse one for the other.

```markdown
# TASKS: [Feature Name]

## Phase 1: Backend
- [ ] 1.1 [Task] (Foundational, Medium)
  **Done when:** [endpoint returns 200 on a valid token, 401 without one]

## Phase 2: Frontend
- [ ] 2.1 [Component] (Important, Easy)
  **Done when:** [component renders and passes its integration test]
```

For high-risk or stateful work, add `risks.md` (risks and mitigations), `rollback.md` (how to revert under incident conditions) or `adr.md` (long-term design decisions). An optional `implementation_notes.md` can carry surprising legacy behavior, workarounds and discoveries across turns.

## 3. Execute

- Hand the agent `spec.md`, `plan.md` and `tasks.md`.
- Run one task per fresh session when a combined diff would be too large to review or context rot is a real risk; otherwise run the whole list in one session.
- Mark `[x]` as each done-check passes.
- When reality contradicts the spec, stop, update `spec.md` and, if needed, `plan.md`, then resume.

## 4. Verify

Every applicable project gate must pass before you advance: linting, type checking, unit tests and relevant integration tests. Evidence ranks in ascending trust:

1. Agent claim: untrusted by default.
2. Automated test or CI: necessary, never sufficient.
3. A real end-to-end run in a production-like environment.
4. The user's manual acceptance: the only thing that closes "done."

Name the level behind every completion claim. Give the user a plain test checklist, one bullet per behavior stating what to do and what must happen. The task is done only when the user has checked it against the agreed criteria.

## 5. Integrate and Learn

Prepare a reviewable local result. Create a PR or merge only within existing authorization, after the gates and review.

Specs live in two tiers. The strategic tier stays current: system-wide rules (`AGENTS.md`), ADRs and architecture invariants. The tactical tier is history: each `specs/NNN-...` folder records intent at one point in time.

After integration, spend ten minutes deciding what the evidence requires you to update: the current spec or plan, strategic rules or ADRs, done-checks, or follow-on work. Use `implementation_notes.md` as input when it exists.

## Vision and Requirements Documents

A vision document or PRD states:

- **Thesis:** what the product is, in one line.
- **Purpose:** what problem it solves, and for whom.
- **Value:** each value proposition that is useful on its own.
- **Non-goals:** deferred and unsupported behavior, next to the goals.

Keep the stable vision apart from current implementation status, and cross-reference the two.
