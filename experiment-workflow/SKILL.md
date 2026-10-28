---
name: experiment-workflow
description: Use when designing, running, or comparing a repeatable experiment in any domain where a decision question, controlled variables, baselines, measurements, and raw evidence matter. Do not use for ordinary unit tests or one-off checks.
---

# Experiment Workflow

Evaluate one stated question at a time and preserve enough evidence for another
person to reproduce the run and judge the conclusion.

## Core Principles

- **Decision first:** State what decision the experiment should inform and what
  result would change that decision.
- **Variable isolation:** Change one independent variable at a time when causal
  interpretation matters. Record unavoidable confounders instead of hiding them.
- **Falsifiability:** Define the expected outcome, comparison, and failure
  condition before seeing the result.
- **Evidence over summaries:** Preserve raw observations alongside calculated
  metrics and conclusions.
- **Decision ownership:** The agent may draft and run an approved experiment.
  Ask before choices that would change the hypothesis, data, cost, or evaluation
  method; do not interrupt for routine execution details.

## Workflow

### 1. Question and decision
Turn the request into one precise question or hypothesis. State the decision it
will inform, the comparison being made, and what the experiment cannot establish.

### 2. Variables and controls
Name the independent variable, observed outcomes, fixed conditions, baseline,
and known confounders. If multiple variables must change together, describe the
run as a comparison rather than claiming a single cause.

### 3. Inputs and environment
Record the exact inputs, versions, configuration, hardware or operating
conditions, random seeds when relevant, and any preprocessing. Keep the same
conditions across runs unless one is the variable under test.

### 4. Measurements and sampling
Choose measures that answer the stated question. Define units, collection
method, acceptance threshold, number of repetitions or samples, aggregation,
and treatment of failures or outliers before execution. Use the smallest sample
that can answer the question honestly; do not imply statistical certainty that
the design cannot support.

### 5. Execute and preserve evidence
Record commands or procedures, timestamps when relevant, raw outputs,
measurements, failures, and deviations from the plan. Keep baseline and variant
results side by side.

### 6. Evaluate and iterate
Separate observations from interpretations. Compare the evidence with the
predeclared threshold, report uncertainty and limitations, and state the
decision the evidence supports. For the next run, change one variable and retain
the previous run as the baseline.

## Domain adaptations

Apply the same workflow to software behavior, performance, ML, retrieval, UX,
operations, or process experiments. Choose domain-appropriate measures rather
than forcing one template onto every experiment.

For retrieval or RAG, a semantic/keyword/hybrid query suite is one useful stress
test—not a universal requirement. A medium-to-large corpus may justify 10 queries
of each type; smaller studies should use fewer. Preserve the query set, retrieved
passages, ranks, latency, chunking configuration, and corpus identity so results
can be compared and reproduced.
