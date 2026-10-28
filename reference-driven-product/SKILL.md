---
name: reference-driven-product
description: Use when improving or rebuilding a product from an existing application, screenshots, user feedback, or open-source alternatives, especially when speed and a guide for starting over matter. Do not use for ordinary isolated bug fixes or purely visual imitation.
---

# Improve a product from a working reference

Deliver the user's important workflows, prove the claims, and leave a guide that
would let someone reach the same destination without this conversation.

## 1. Establish the destination

Read the actual project state and the user's newest priorities before extending
an old plan. Identify the few jobs the user wants to complete, the behaviors they
value in the reference, and the resource and data constraints that remain binding.
Distinguish essential work, optional work, and work explicitly deferred by feedback.
Do not turn every visible reference feature into a requirement.

Use the existing specification/plan as the authoritative acceptance contract.
Apply the [spec workflow](../spec/SKILL.md) when the contract needs substantial
work; avoid creating another competing specification. Record current intent in
the project's session log.

## 2. Inspect the reference and the real product

View every supplied screenshot and exercise the relevant working application
when available. Compare the same task and state: opening a note, typing, checking
a task, searching commands, changing a setting, or recovering a failed save.
Record concrete differences in behavior, hierarchy, typography, spacing and
interaction. Account for zoom, display scale, window size and theme before taking
pixel measurements. A similar screenshot is not proof of equivalent editing.

Inspect the currently built product as well as source. Verify old summaries and
identify which changes have actually reached the executable. Ask for feedback
early on a usable result, before a long optional-feature implementation.

## 3. Learn from existing implementations

Research a small relevant set of open-source projects using primary sources.
Record versions, licenses, supported platforms, editing models and the important
capability gaps. Separate published claims from independently observed results.
Choose a defensible comparison; popularity, implementation language and marketing
do not establish which product is best or fastest.

Read the code that explains an observed advantage. Reuse an existing component or
adapt a small proven technique when it fits the current architecture and license.
Retain required attribution. Do not replace the stack merely because another
editor looks fast, or copy features that the user does not need.

## 4. Compare performance fairly

Use the [experiment workflow](../experiment-workflow/SKILL.md) for the measurement
design rather than inventing another benchmark process here. Before running,
define equivalent user work, inputs, environment, modes, timing boundary and
acceptance limits. Measure correctness alongside speed, including exact saved
text, Unicode and retained input.

Keep startup, indexing, input-to-frame response, CPU work, memory and save latency
distinct. Compare products on the same host and conditions, running serially.
Do not compare internal CPU timers in one app against visible response in another.
Preserve raw samples, failures, commands, versions, source/binary identity and
confounders. If the comparison is unavailable, say so; do not infer a win from
open-source availability or Rust alone.

## 5. Fix the most valuable gap and verify it

Choose a small change tied directly to the user's priority. Establish an evaluation
that can detect the current failure, with meaningful positive and negative controls.
Preserve unrelated work and existing permissions. Implement through the shared
editing/component/storage path, then verify the real user flow and appropriate
regressions on the exact built artifact. Keep builds, transfers and evidence within
the user's resource limits.

Show the result and its practical limitations. Apply feedback to the authoritative
scope before the next increment. Passing tests are evidence; the user decides
whether the result is good enough. Do not describe a partial implementation as
finished or advertise controls that do nothing.

## 6. Write the guide as if starting over

Maintain one project guide, linked from its orientation file, that answers:

- What useful product are we trying to build, and what can wait?
- Which references, source versions, licenses and observed behaviors matter?
- What is the simplest architecture that serves those workflows, and why?
- In what order would we implement and verify it from a clean checkout?
- Which exact commands and inputs reproduce the build, behavior and measurements?
- What failed, what evidence explains it, and what decision avoids repeating it?
- What is verified now, what remains unknown, and what should happen next?

Write a route to the destination, not a chronological agent diary. Include setup,
data safeguards, resource limits, failure recovery and enough source/evidence
links to make each important decision assessable. Preserve lessons with a trigger,
evidence, action and verification method; avoid vague advice such as "be careful."
Keep raw results separate and linked. On each meaningful iteration, update the
guide and current-state notes so a fresh agent can continue without rediscovery.
