---
name: multi-agent
description: Split work across agents without losing control, with one worktree and prompt file per task and a coordinator who integrates. Use when dispatching more than one agent or writing a brief for another agent.
---

# Multi-Agent Dispatch

Dispatch parallel agents only for genuinely independent tasks, because two agents editing the same interface produce two plausible diffs that cannot both be right.

For implementation, the unit of dispatch is **one task, one branch, one worktree, one prompt file, one acceptance check**. Read-only reviewers may inspect the same working tree when they must see its pending changes; forbid writes explicitly.

## Roles

- **Coordinator:** owns the task list, the architecture, the ordering, the integration and the final acceptance decision. Creates and removes worktrees, chooses which model runs which task, and never lets a worker redefine the product.
- **Worker:** implements one bounded task inside its own worktree and returns changed files, checks run, evidence and risks. Does not touch the task list, the vision document or any file outside its declared scope.
- **User:** decides product behavior and accepts the result.

## Setup, per task

The project's instructions name the worktree location and base branch. Do not assume `main` or the default branch contains the work the task depends on. Set `worktree_path`, `task_branch` and `base_ref` to those verified values:

```bash
git worktree add "$worktree_path" -b "$task_branch" "$base_ref"
```

Independent implementation tasks use the same verified baseline. A new worktree contains committed content only.

Write the prompt to `WORKER_PROMPT.md` **at the root of that worktree**, not in a shared prompts folder, so whoever opens a session there finds its instructions without cross-referencing. Mark it untracked scratch: "Do not commit it." Remove the worktree only after its branch is integrated or deliberately abandoned.

## The prompt contract

Every dispatched prompt contains these fields. A missing or contradictory field is a reason to challenge the task, not to start coding.

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

- **Desired user-visible behavior** is what a person sees, not an implementation. "The window accepts a keystroke immediately" beats "optimize startup."
- **Allowed files** is a real list, with a rule for the ragged edge, such as "source files only where a compile error forces a change, each reported with the error that caused it."
- **Forbidden scope** names the specific temptations: adjacent refactors, the neighboring platform, the file the coordinator owns, publishing or tagging anything.
- **Dependencies already verified** saves the worker from re-deriving what is known and tells it what it may trust without checking.
- **Acceptance test** is numbered, and each item can pass or fail. If an item cannot fail, delete it.
- **Required checks** carries the environment's hard rules: build flags, disk limits, commands that must never run, where CI must run instead of the local machine.

Add a short **Note for the coordinator** below the contract when the task has a legitimate null result, such as "if the only lever costs more than it buys, report that and close the task." It stops a worker from shipping churn to look productive.

## Constraints belong in the prompt

State whatever binds the task where the work happens:

- A task nobody can verify locally (no such hardware, no clean machine) says so, names the ceiling of what CI can prove, and forbids claiming more.
- A task that can exhaust the disk carries the build flags and the size history.
- A task that observes rather than fixes says it reports what it finds and does not patch it; otherwise every harness grows into a fix for the first thing it catches.

## Independence check, before dispatching

1. **Files:** if two tasks' allowed-file lists intersect, serialize them.
2. **Interfaces:** work on a shared runtime, protocol or permission contract that is still being reshaped is single-threaded, even in separate files.
3. **Machine:** parallel builds share one disk, one CPU and one target directory per worktree. Check free space before dispatching, not after.
4. **User state:** agents that install a binary to the same path, or write to the same application home, collide outside git. Only one may own that path at a time.

## Verification vocabulary

Record verification with one of three labels; the trust ranking behind them lives in the [spec skill's Verify section](../spec/SKILL.md#4-verify).

- `user-verified`: the user used it and accepted it. The only label that means done.
- `agent-verified`: an agent ran a check and it passed.
- `unverifiable here`: the environment to confirm it does not exist; name what would be needed, which is often the next task.

## Integration

Review and integrate one branch at a time, and run the acceptance test again after integration: a check that passed inside a worktree proves nothing about the merged tree. The coordinator alone records a task's verification label.
