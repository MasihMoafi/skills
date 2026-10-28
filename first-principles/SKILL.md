---
name: first-principles
description: Use only when the user explicitly requests a first-principles review of a product, requirement, workflow, or implementation.
---

# First-Principles Engineering Method

## Intro - What is it?
This is an optional lens for questioning assumptions and finding the smallest
effective system. Apply only the phases relevant to the user's actual goal.

A review request produces analysis and recommendations only. Edit, delete,
optimize, or automate only when implementation is separately authorized.

## Core Stance
- **Correct Trajectory First:** The most rigorous phase is requirement checking. Finding the right problem to solve prevents wasting cycles on things that shouldn't exist.
- **Ordering:** When several phases apply, use Question -> Delete ->
  Simplify/Optimize -> Accelerate -> Automate. Do not optimize or automate a
  process that should not exist.
- **Decision ownership:** State consequential assumptions and ask only when a
  missing choice would materially change the outcome.

---

## The 5-Step Protocol

### 1. Question the Requirements (Finding the Trajectory)
- **Goal:** Get the requirements as least wrong as possible. Do not solve a problem that shouldn't exist.
- **Procedure:**
  - Assume every requirement in the issue or prompt is wrong or sub-optimal.
  - State assumptions that materially affect the choice or result.
  - If the request has multiple plausible meanings, surface the interpretations instead of silently choosing one.
  - Ask when ambiguity makes the change risky or likely wrong.
  - Push back if a simpler or safer approach better serves the core objective.
  - Stop and name confusion immediately when code, runtime behavior, or requirements disagree.

### 2. Delete the Process (Trimming)
- **Goal:** Remove demonstrated waste while preserving required behavior.
- **Procedure:**
  - Review the code or features implemented for the task.
  - Identify parts, configs, or dependencies that can be removed without breaking core functionality.
  - Run regression tests to verify functionality remains intact.
  - Stop when further deletion would risk required behavior; do not create a
    deletion quota.

### 3. Simplify and Optimize (Surgical Coding)
- **Goal:** Keep the remaining codebase lean, boring, and readable.
- **Procedure:**
  - Write the absolute minimum code that solves the verified problem.
  - Do not add speculative features, configurations, abstractions, or shared helpers for single-use logic.
  - Avoid error handling for impossible states unless surrounding code explicitly does it.
  - Touch only the lines needed for the request. Do not perform drive-by formatting or adjacent refactors.
  - Match the local repository style exactly.

### 4. Accelerate Cycle Time (When Speed Matters)
- **Goal:** Accelerate execution speed and cycle time without sacrificing performance.
- **Procedure:**
  - Measure before optimizing when speed is part of the request or is a proven
    bottleneck.
  - Locate the slowest paths (bottlenecks).
  - Restructure loops, cache computations, or parallelize tasks.
  - Maintain a short plan with a verification check attached to each acceleration step.
  - Run the cheapest relevant regression checks to ensure speed-ups do not introduce flakes.

### 5. Automate the Process (When Repetition Justifies It)
- **Goal:** Automate the final, optimized state. Never automate a process that has not been optimized.
- **Procedure:**
  - Take the simplified, optimized, fast process.
  - Add automation only within the user-approved scope and when a repeated,
    stable process justifies it.
  - Verify that the automation runs end-to-end cleanly without human intervention.

---

## Verification Checklist
1. Were the requirements questioned and the trajectory approved before writing code?
2. Was demonstrated waste removed without imposing a deletion quota?
3. Is the code surgical, matching local style, with no speculative abstractions?
4. If speed mattered, was it measured before and after the change?
5. If automation was justified, does it run cleanly at the authorized boundary?
