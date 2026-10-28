---
name: multi-agent
description: Split work across agents without losing control: one worktree per task, a prompt file per folder, an acceptance test before work starts, a coordinator who integrates. Load when dispatching more than one agent or writing a brief for another agent.
---

# Multi-Agent Dispatch

Parallel agents multiply throughput only when the tasks are genuinely independent. They
multiply damage otherwise: two agents editing the same interface produce two plausible
diffs that cannot both be right, and the cost of untangling them exceeds what was saved.

For implementation, the unit of dispatch is **one task, one branch, one worktree,
one prompt file, one acceptance check**. Read-only reviewers may inspect the same
working tree when they must see its pending changes; forbid writes explicitly.

## Roles

**Coordinator** — owns the task list, the architecture, the ordering, the integration,
and the final acceptance decision. Creates and removes worktrees. Chooses which model
runs which task. Never lets a worker redefine the product.

**Worker** — implements one bounded task inside its own worktree. Returns changed files,
checks run, evidence, and risks. Does not touch the task list, the vision document, or
any file outside its declared scope.

**User** — decides product behavior and is the sole arbiter of done. A worker's own check
is evidence, never acceptance.

## Setup, per task

Resolve the worktree location from the project's instructions; Masih's shared
location policy lives in `../dev/AGENTS.md`. Identify the current integration
branch or other required base before creating a worktree. Do not assume `main`
or the default branch contains the work the task depends on.

Set `worktree_path`, `task_branch`, and `base_ref` to those verified values:

```bash
git worktree add "$worktree_path" -b "$task_branch" "$base_ref"
```

Independent implementation tasks use the same verified baseline. A new worktree
contains committed content only; account for required pending changes without
resetting or moving another session's work.

Write the prompt to `WORKER_PROMPT.md` **at the root of that worktree**, not in a shared
prompts folder. The person or agent opening a session in that folder should find its
instructions already there, with no cross-referencing. Mark it untracked scratch: "Do not
commit it."

Remove the worktree only after its branch is integrated or deliberately abandoned:

```bash
git worktree remove "$worktree_path"
```

## The prompt contract

Every dispatched prompt contains these fields. A missing or contradictory field is a
reason to challenge the task, not to start coding.

```text
Task ID:
Desired user-visible behavior:
Why it is needed:
Allowed files:
Forbidden scope:
Dependencies already verified:
Acceptance test:
Required checks:
Return: summary, changed files, verification, risks, commit hash.
```

What separates a working prompt from a decorative one:

- **Desired user-visible behavior** is written as what a person sees, not as an
  implementation. "The window accepts a keystroke immediately" beats "optimize startup."
- **Allowed files** is a real list, with a rule for the ragged edge — e.g. "source files
  only where a compile error forces a change, and each such change reported individually
  with the error that caused it."
- **Forbidden scope** names the specific temptations: adjacent refactors, the neighboring
  platform, the file the coordinator owns, publishing or tagging anything.
- **Dependencies already verified** saves the worker from re-deriving what is known, and
  tells it what it may trust without checking.
- **Acceptance test** is numbered, and each item is something that can pass or fail. If an
  item cannot fail, delete it.
- **Required checks** carries the environment's hard rules: build flags, disk limits,
  commands that must never run, where CI must run instead of the local machine.

Add a short **Note for the coordinator** below the contract when the task has a
legitimate null result — "if the finding is that the only lever costs more than it buys,
take that and close the task." It stops a worker from shipping churn to look productive.

## Constraints belong in the prompt

Whatever binds the task must be stated where the work happens:

- A task nobody can verify locally (no such hardware, no clean machine) must say so, name
  the honest ceiling of what CI can prove, and forbid claiming more.
- A task that can exhaust the disk must carry the build flags and the size history.
- A task that observes rather than fixes must say that it reports what it finds and does
  not patch it — otherwise every harness grows into a fix for the first thing it catches.
- A GPT agent (sol through `elpis exec`) does the letter of the brief (25 Oct: it reran all
  197 browser files to prove a six-line test change; Masih: "it's too literal"). Give it the
  scope of its proof, what not to rerun, and when to stop and report.

## Independence check, before dispatching

Run these four before starting anything in parallel:

1. **Files** — do two tasks' allowed-file lists intersect? If yes, serialize them.
2. **Interfaces** — do they share a runtime, protocol, or permission contract that is
   still being reshaped? Shared-interface work is single-threaded even in separate files.
3. **Machine** — parallel builds share one disk, one CPU, and one target directory per
   worktree. Check free space before dispatching, not after.
4. **User state** — agents that install a binary to the same path, or write to the same
   application home, collide outside git entirely. Only one may own that path at a time.

## Verification vocabulary

Record verification literally, so a later reader cannot mistake one kind for another:

- `user-verified` — the user used it and accepted it. The only state that means done.
- `agent-verified` — an agent ran a check and it passed. Necessary, never sufficient.
- `unverifiable here` — the machine or environment to confirm it does not exist. Name
  what would be needed.

Never let `agent-verified` be written up as done. When a task ends in
`unverifiable here`, the next task is usually building the thing that would verify it.

## Integration

Review and integrate one branch at a time, and run the acceptance test again after
integration — a check that passed inside a worktree proves nothing about the merged tree.
Move commits between diverged branches with `git cherry-pick`, never `git merge`. The
coordinator alone marks a task verified.
