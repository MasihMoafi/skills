---
name: reference-driven-product
description: Use when improving or rebuilding a product from a reference app, screenshots, user feedback, or open-source alternatives, when speed and a restart guide matter. Not for isolated bug fixes or purely visual imitation.
---

# Improve a product from a working reference

Deliver the user's important workflows, prove the claims, and leave a guide that lets someone reach the same destination without this conversation.

## 1. Establish the destination

Read the actual project state and the user's newest priorities before extending an
old plan. Identify the few jobs the user wants to complete, the behaviors they value
in the reference, and the constraints that still bind. Separate essential, optional
and deferred work; not every visible reference feature is a requirement. Keep one
acceptance contract, following the [spec](../spec/SKILL.md) skill.

## 2. Inspect the reference and the real product

View every supplied screenshot and exercise the working reference when available.
Compare the same task and state (opening a note, typing, searching commands,
changing a setting, recovering a failed save) and record concrete differences in
behavior, hierarchy, typography, spacing and interaction. Account for zoom, display
scale, window size and theme before measuring pixels; a similar screenshot is not
proof of equivalent behavior. Inspect the built product as well as the source, and
confirm which changes have reached the executable. Ask for feedback early on a
usable result, before a long optional feature.

## 3. Learn from existing implementations

Research a small relevant set of open-source projects from primary sources. Record
versions, licenses, platforms, editing models and important capability gaps, and
separate published claims from observed results; popularity, language and marketing
do not establish which product is best or fastest. Read the code behind an observed
advantage, and reuse a component or a small proven technique when it fits the
architecture and license, keeping required attribution. Do not replace the stack
because another product looks fast, or copy features the user does not need.

## 4. Compare performance fairly

Design the measurement with the [experiment workflow](../experiment-workflow/SKILL.md).
Give each product equivalent user work, on the same host and conditions, run serially.
Keep startup, indexing, input-to-frame response and save latency distinct, and check
correctness (exact saved text, Unicode, retained input) alongside speed.

## 5. Fix the most valuable gap and verify it

Choose a small change tied to the user's priority, with a check that fails on the
current product. Implement it through the shared component, editing or storage path,
then verify the real user flow on the exact built artifact. Show the result and its
limits, and apply feedback to the acceptance contract before the next increment.
Never call partial work finished or ship controls that do nothing.

## 6. Write the guide as if starting over

Keep one project guide, linked from the project's orientation file, that answers:

- What product are we building, and what can wait?
- Which references, versions, licenses and observed behaviors matter?
- What is the simplest architecture that serves those workflows, and why?
- In what order would we build and verify it from a clean checkout, with which commands and inputs?
- What failed, what evidence explains it, and what decision avoids repeating it?
- What is verified now, what is unknown, and what comes next?

Write a route to the destination, not a diary. Link raw results and sources so each
important decision can be checked, and update the guide on each meaningful
iteration so a fresh agent can continue without rediscovery.
