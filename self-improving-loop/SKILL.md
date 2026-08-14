---
name: self-improving-loop
description: Rules, architecture, and workflows for designing self-improving agent loops and evaluation harnesses. Use when building, evaluating, or optimizing AI agent systems, designing metrics/judges, or automating prompt/instruction optimization.
metadata:
  short-description: Design and execute self-improving agent evaluation loops
---

# Self-Improving Agent Loop

This skill provides rules, architectural principles, and execution workflows for building self-improving agent optimization loops.

## Core Philosophy

The measure-and-improve loop automates prompt updates, trace generation, and iteration. However, **the loop cannot define quality**. 
- The metric sits upstream of the prompt, code, and agent behavior.
- An agent will optimize towards whatever number you give it—even a shallow target that scores high while worsening real-world utility.
- Authoring the metric (defining "good") and holding the evaluation harness secure is where engineering judgment belongs.

---

## The 7 Rules for Self-Improving Loops

### Rule 1: Start with One Case, Not a Suite
- **Principle**: One failing case tells you what to fix next. Twenty failing cases create noise.
- **Workflow**: Start with 1 failing case. Expect 5–10 iterations before it passes. Only add the next case once the fix holds.

### Rule 2: Make Judges Explain Themselves
- **Principle**: A score (0 or 1) only indicates failure; the one-line reason provides directional guidance for the next prompt revision.
- **Exception**: Deterministic checks (code assertions) are exempt since the failed assertion is its own explanation.

### Rule 3: Use Code Wherever the Answer is Deterministic
- **Principle**: Do not waste LLM judge calls on binary system state (e.g., "Did it call the retention tool before confirming?").
- **Implementation**: Write a Python function for exact, free, zero-variance assertions. Reserve LLM judges for tone, completeness, and qualitative reasoning.

### Rule 4: Score Behavior, Not Paths
- **Principle**: Do not enforce exact trajectory matching. An agent that geocodes before checking weather is not wrong.
- **Focus**: Grade final outputs, side-effects, and key state transitions—not step-by-step intermediate execution sequence.

### Rule 5: Treat a Flaky Case as a Finding
- **Principle**: A score that fluctuates across identical runs signals non-determinism in either the agent or the judge.
- **Action**: Run flaky cases multiple times to isolate the instability. Never delete a flaky case to clean up scores; deleting it removes evidence, not behavior.

### Rule 6: Never Let the Proposer Move the Bar
- **Principle**: Prevent metric gaming (lowering thresholds, modifying expected outputs, dropping hard cases).
- **Protection**: Keep a **held-out evaluation slice** that the optimizing agent cannot view or modify. Real gains hold on the held-out set; gamed gains fail.

### Rule 7: Auto-Optimize Once, at the End
- **Principle**: Prompt auto-optimization is expensive and only refines wording—it cannot fix missing tool implementations or flawed logic.
- **Execution**: Resolve structural gaps and tool access manually first. Run automated prompt tuning only as the final polish stage.

---

## Optimization Cycle Architecture

```
                 +-----------------------+
                 |  Defined Metric/Good  |  (Human-Authored, Read-Only to Loop)
                 +-----------+-----------+
                             |
                             v
                 +-----------------------+
                 |    Generate Traces    |  (Run agent on dataset cases)
                 +-----------+-----------+
                             |
                             v
                 +-----------------------+
                 |     Grade Traces      |  (Evaluate against metric -> score + reason)
                 +-----------+-----------+
                             |
                   Pass? ----+---- Fail?
                     |               |
                     v               v
             +---------------+ +-----------------------+
             | Test Held-out | | Propose Fix (Prompt)  | (Driven by metric's reason)
             +---------------+ +-----------+-----------+
                                         |
                                         v
                               +-------------------+
                               | Compare Runs      | (Ensure no regressions)
                               +-------------------+
```

---

## Standard CLI Workflow (e.g. `agents-cli`)

1. **Setup & Metric Definition**:
   Define custom metrics returning `0` or `1` with a concise `reason`.

2. **Generate Traces**:
   Run the agent over test cases to record execution traces.
   ```bash
   agents-cli eval generate --dataset tests/eval/datasets/cases.json -o artifacts/traces/
   ```

3. **Grade Traces**:
   Grade traces using an independent judge/metric standard.
   ```bash
   agents-cli eval grade --traces artifacts/traces/ --config tests/eval/eval_config.yaml
   ```

4. **Iterate and Compare**:
   Feed failure reasons into prompt revisions, then compare against baseline to verify improvement without regressions.
   ```bash
   agents-cli eval compare artifacts/grade_results/baseline.json artifacts/grade_results/after_fix.json
   ```

---

## Production & Monitoring Bridge

- **Development**: Eval suite run over synthetic/written dataset cases.
- **Production**: BigQuery / log trace grading run over real production traffic using the **exact same metrics**.
- Every production failure or customer escalation is converted into a new test case in the eval suite to prevent regression.
