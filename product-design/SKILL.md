---
name: product-design
description: Use when shaping a new product, materially redesigning a user flow, choosing a web or app stack, or turning a product concept into an implementation-ready design.
---

# Product Design

Act as product architect and UX-driven technical lead: turn an early product vision into a coherent user experience and an implementation boundary before code is written.

## 1. Mental model first

Settle who the product is for and what they must get done before choosing any technology. Define:

- the primary user or audience;
- the platform: web, mobile, desktop, terminal, extension, or mixed;
- the core problem being removed;
- the two or three highest-value user flows;
- the minimum interactions and states that complete those flows, including screens when the product is visual.

Begin with what the user is trying to get done, not a feature inventory, and do not invent needs that were not stated or strongly implied.

For a team, high-fidelity designs or wireframes are the shared source of truth: resolve navigation, hierarchy, major states, and edge cases before backend detail spreads across the codebase.

For solo or AI-assisted work, map exact user flows and screen architecture first, explicit enough that an agent can infer component and data boundaries from them.

Either way, wireframes define implementation boundaries, and an unresolved UX decision is an unresolved product requirement, not an implementation detail.

## 2. Choose the stack from the product

Tie every stack choice to a product constraint, not habit or fashion. Match rendering and framework to how users discover and use the product:

- SEO-heavy public marketplace or content product: a server-rendered or hybrid framework such as Next.js;
- authenticated internal dashboard: an SPA or application framework, since SEO is irrelevant;
- highly native mobile interaction: a native or cross-platform mobile stack chosen by device and API needs;
- local developer tool: the smallest runtime and UI layer that fits the workflow.

When several stacks fit, prefer the one with a mature component and interaction ecosystem for the intended interface. Do not rebuild standard UI primitives without a product reason.

State the trade-offs that matter:

- speed of initial development;
- maintenance burden;
- hosting and deployment complexity;
- SEO and discoverability;
- accessibility and responsive behavior;
- ecosystem maturity;
- expected scale, only when scale is a real requirement; do not build infrastructure for hypothetical scale.

## 3. Build frontend first

Build the interface and user flow before deep backend work whenever the product allows it:

1. define screens and states;
2. build the interface with mocked data;
3. exercise the main flows end to end;
4. identify the data contracts the UI actually needs;
5. implement backend, storage, and auth boundaries against those contracts;
6. replace mocks incrementally;
7. verify the real flow against the original design.

The point is not cosmetic polish: the frontend exposes missing product decisions before backend structure hardens around them.

### Repository structure

For a coupled full-stack product built with AI assistance, default to a monorepo so agents can inspect frontend, backend, shared types, tests, and product rules in one working tree. Keep boundaries explicit inside it:

```text
apps/
  web/
  api/
packages/
  ui/
  shared/
  config/
docs/
  product/
```

Split repositories only when deployment, ownership, security, or lifecycle boundaries make it materially useful, not merely because frontend and backend use different languages.

## Input

Use what is already known; ask only for details that would change the architecture. Preferred shape:

```markdown
**Product Concept & Audience:** [product, users, platform]
**Desired UX Style / Reference:** [reference product, visual direction, or interaction style]
**Key User Flows:** [two or three main user paths]
**Execution Setup:** [Solo + AI / Team]
```

## Output

For a full UI product brief, return the four sections below in order. For a focused stack, flow, or repository question, return only the relevant sections. For terminal, API, or background products, describe commands, requests, states, and failure paths instead of inventing screens.

1. **UX/UI and screen architecture.** For each primary flow, show `entry → screen/state → action → next state → completion/failure`, then list the minimum screen set and the purpose of each screen.
2. **Tech stack.** Name the chosen stack, justify each major choice against a product requirement, and give one credible alternative with the reason it lost.
3. **Frontend-first sequence.** An ordered build from mocked interface to integrated product, marking where backend, persistence, auth, external APIs, tests, and deployment first become necessary.
4. **Repository structure.** The minimum useful directory or monorepo layout for the chosen stack.

## Guardrails

- Do not expand the product into a large feature roadmap before the core flows work.
- Keep the first implementation small enough to test the core product assumption.
