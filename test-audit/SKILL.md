---
name: test-audit
description: "Invoke whenever writing, changing, reviewing, or sweeping tests: an authoring gate for new tests, an audit for low-value, implementation-coupled or duplicate tests, and layered verification for AI-generated code."
---

# Test Audit

Keep only tests that earn their maintenance cost, in three modes with one value bar.

- **Authoring:** gate every new or changed test at write time.
- **Audit:** sweep for tests that re-assert source, duplicate stronger proof,
  couple to implementation, or keep test-only production seams alive. Optimize
  for confidence, not deletion count.
- **Campaign:** review one subsystem's test surface. Define its owner boundaries
  and validation commands first, then apply the same rules to each batch.

## Authoring gate

Before adding any test, answer four questions; a missing answer means wait:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail?
3. Why does existing coverage not already catch that failure? Each contract has
   one primary test owner at the strongest boundary; another layer needs its
   own distinct risk, such as a transport or lifecycle failure the owner cannot
   reach. Prefer extending a table-driven case or shared fixture over a
   near-duplicate test; consolidate duplicated setup in the same change.
4. Does it need a production seam (export, flag, wrapper, injection hook) that no
   production caller needs? If yes, move the test to the real boundary instead.

Then check the test against every [junk pattern](#junk-patterns); a match fails
the gate unless the [retention bar](#retention-bar) names the contract it
independently guards. The [tdd skill](../tdd/SKILL.md) defines a good test
and the regression rule (sections "A good test" and "Bugs").

## Junk patterns

The gate rejects a new test that matches one; audits hunt for existing ones.

- assertion-free coverage probes;
- self-comparisons and identity copiers;
- copied fixtures, inventories, manifests, or export lists;
- exact source, import, or string greps;
- private predicate or call-shape tests duplicated at real boundaries;
- duplicate invocations of the same contract;
- provider-local replays of shared helpers;
- tests whose only purpose is preserving test-only exports, globals, or wrappers;
- dead production code whose only callers are tests;
- expected values produced by the helper or renderer under test;
- mocks that implement the asserted behavior, or one identical mock standing in
  for different APIs;
- fixtures that supply the receipt, admission, or callback ordering the owner
  should produce, or persistence asserted against a store the path never writes;
- capability tests that restate declared flags instead of exercising the
  delivery or acknowledgement the flag promises;
- negative controls that pass for an unrelated reason, such as a denial from a
  different guard or a rejection the production path never reaches;
- names or fixtures that promise more than the input exercises, such as a
  "retires the window" test asserting the window was not cleared.

## Value bar

Tests justify their maintenance cost by protecting behavior, a credible
regression, or an independently meaningful contract. In an audit, an existing
test that must change for behavior-preserving source reorganization is suspect,
not automatically deletable; the authoring gate still rejects new ones.

Before judging a candidate, read the complete test and production owner, its
entry point, callers, callees, sibling implementations, overlapping tests, CI
routing, and relevant history. Read root and scoped `AGENTS.md` files first.
When the test claims dependency-backed behavior, inspect the dependency source
or types directly.

Keep discovery read-only and report evidence before editing. For broad scope,
run parallel lanes when available: one per top-level area of the repository,
plus a cross-cutting pattern sweep. Outside campaign mode, prefer a few
high-confidence candidates over a large speculative inventory.

## Retention bar

Keep a test when it independently enforces a public API, SDK, protocol, config,
migration, storage, security, platform, default, generated-code, package,
release, or architecture contract. Also keep:

- call ordering when order is observable behavior;
- regressions with a credible failure mode;
- source inspection when it is the cheapest independent guard: it fails when
  the contract changes (the user-facing key, byte, or path) and survives an
  identifier-only refactor;
- a retained test that fails on the baseline: treat it as a possible product
  bug, reproduce it, and repair the owner rather than deleting it.

Static or slow is not a deletion reason. A test that resembles implementation
may still be the independent contract; prove otherwise before removing it.

## Candidate evidence

Record every field before editing; a missing field means not ready to delete:

- exact test name and location;
- what failure it can actually detect;
- non-test callers of the covered production or support seam;
- stronger remaining owner-boundary proof, or why no proof is needed;
- relevant history and the reason the test or seam exists;
- production or test-support deletion unlocked;
- risk and the focused validation command.

## Edit shape

Choose one coherent owner-boundary batch. Delete obsolete test-only exports,
globals, wrappers, and dead production paths instead of preserving aliases.
Move retained regressions to their canonical owners. Consolidate repeated
package or dependency assertions into one generic contract.

Prefer net-negative production lines. Do not add replacement tests that restate
the same implementation, or turn uncertain candidates into cleanup for count.

## Validation

Read the target repository's test commands and execution policy first. Do not
edit files while a test run that reads them is in progress. Route heavy proof
through the project's documented environment.

1. Run the smallest owner and sibling tests with the supported runner and filter.
2. For removed source greps or plan assertions, run the executable script or
   dry-run that owns the real contract.
3. Run targeted formatting, then `git diff --check`.
4. Run the checks required for the changed paths by repository policy.
5. Inspect `git diff --numstat`; report production and tooling apart from tests.
6. Review the final diff and run any additional review required by the project.

## Landing and report

Land only when authorized, one coherent batch at a time, then rerun read-only
discovery for the next batch. Report the root cause, removed categories,
retained false positives and why they stay, the proof actually run, production
versus test lines changed, and named follow-ups.

## Layered verification

Tests are one layer; stack cheaper layers before human attention, scaled to risk:

1. Deterministic guardrails: strict types, lint, tests, security and secret scans.
2. LLM review in a fresh, adversarial context: spec alignment and test rigor.
3. Deploy-time safety: flags, canaries, rollback on objective SLO signals.
4. Runtime observability: traces, SLOs and error budgets.
5. Focused human review: intent, architecture, and whether to build it at all.

Trust is measured and earned: track cycle time, escape and revert rates together;
widen automation one reversible step at a time and step back when evidence worsens.
