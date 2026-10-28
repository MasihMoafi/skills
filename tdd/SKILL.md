---
name: tdd
description: "Test-driven development: the agent writes the failing test, then the code, one behavior at a time. Use when building a feature or fixing a bug test-first, or when the user says tdd, red-green, or test-first."
---

# Test-Driven Development

The agent writes the failing test, then the code that passes it, one **slice** at a time.

## Before the first test

1. Name the behavior in one line: input, expected outcome, non-goals.
2. Pick the **seam**: the public boundary you will test at (a function, CLI,
   HTTP route, or rendered UI). Choose it yourself from the code.
3. Find the test command the repo already uses (`package.json`, `pyproject`,
   `Makefile`). Run it once so you know the baseline.

## The loop

Repeat per slice:

1. **Red.** Write one test for the next smallest behavior. Run only that test.
   It must fail *for the intended reason*: the behavior is missing. A failure
   from a typo, import error, or broken fixture is not red; fix it and rerun.
   If the test passes at once, it is not red: call it a characterization
   test and pick a behavior that is actually missing.
2. **Green.** Write the smallest code that makes it pass. Rerun that test.
3. **Next slice.** Let what this slice taught you shape the next test. Write
   tests one at a time, not all up front.

Refactor after the behavior is complete and all tests are green, then rerun
the relevant suite.

## A good test

- Checks behavior through the seam, and survives a refactor that keeps that
  behavior.
- Has one clear reason to fail, and is deterministic and fast.
- Takes its expected value from an independent source: a known literal, a
  worked example, or the spec. A **tautological** test recomputes the
  expected value the way the code does (`assert add(a, b) == a + b`), so it
  can never fail. Replace it with a literal (`assert add(2, 3) == 5`).
- Mocks only external boundaries (network, paid APIs, clock). Use fixtures
  for paid APIs; tests must make no paid calls.
- A test that uses a fake proves the fake's boundary only. Say so; do not
  claim it verifies the real database, model, network, or UI.

## Model and ML code

Test the deterministic parts: data transforms, parsing, shapes, prompt
assembly, scoring math. Model quality is an experiment, not a unit test;
report it as a measurement with its inputs.

## Bugs

Write the regression test first and show it failing on the current code for
the intended reason. Then fix. A regression test that never failed proves nothing.

## Done

The slice is done when you can show:

- the exact test command, and its red output before the change;
- the same command green after the change;
- the relevant wider suite green.

Label the work honestly: TDD, regression test, characterization test, or
refactor. Tests existing is not TDD.

Source: `mattpocock/skills` (`tdd`), for vertical slices, seams and tautological tests.
