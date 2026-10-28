---
name: product-design
description: Use when shaping a new product, materially redesigning a user flow, choosing a web or app stack, or turning a product concept into an implementation-ready design.
---

# Product Design

## Role

Act as a product architect and UX-driven technical lead.

## Objective

Translate an early product vision into a coherent user experience and an implementation boundary before code is written.

The output must connect four things directly:

1. who the product is for;
2. what those users need to accomplish;
3. what interactions and states support those jobs, including screens when the
   product is visual;
4. what technical stack best supports that product shape.

Do not choose technology before the user and flow are clear.

## 1. Design and flow foundation

### Mental model first

Establish one clear picture of the product before implementation.

Define:

- primary user or audience;
- platform: web, mobile, desktop, terminal, extension, or mixed;
- core problem being removed;
- two or three highest-value user flows;
- the minimum interactions and states required to complete those flows,
  including screens when the product is visual.

Do not begin with a feature inventory. Begin with what the user is trying to get done.

### Resizable workspaces — Masih, 21 October 2026

For web and desktop workspaces with a sidebar beside the main content, make the divider draggable so the user can expand or narrow the sidebar. Show a discoverable resize handle and cursor; support keyboard resizing, remember the chosen width and enforce bounds that keep the main content usable. Respect RTL pointer/arrow directions and keep mobile drawers usable without page overflow. Verify real dragging, reload persistence and narrow-screen behavior; a decorative divider is insufficient.

### Alignment strategy

For a team:

- use high-fidelity designs or wireframes as the shared source of truth;
- resolve navigation, hierarchy, major states, and edge cases before backend detail spreads across the codebase.

For solo or AI-assisted development:

- map exact user flows and screen architecture first;
- make design decisions explicit enough that an agent can infer component and data boundaries from them;
- treat unresolved UX decisions as unresolved product requirements, not implementation details.

## 2. Product-driven stack selection

Choose the stack from product constraints, not habit.

### Platform and audience alignment

Match rendering and framework choices to how users discover and consume the product.

Examples:

- SEO-heavy public marketplace or content product → server-rendered or hybrid framework such as Next.js;
- authenticated internal dashboard → SPA or application framework where SEO is irrelevant;
- highly native mobile interaction → native or cross-platform mobile stack based on device/API needs;
- local developer tool → prefer the smallest runtime and UI layer that fits the workflow.

### UI ecosystem priority

When multiple stacks satisfy the product requirements, prefer the one with a mature component and interaction ecosystem for the intended interface.

Do not rebuild standard UI primitives without a product reason.

### Trade-offs

State the important trade-offs explicitly:

- speed of initial development;
- maintenance burden;
- hosting/deployment complexity;
- SEO/discoverability;
- accessibility and responsive behavior;
- ecosystem maturity;
- expected scale only when scale is a real requirement.

Do not introduce infrastructure for hypothetical scale.

## 3. Execution blueprint

### Frontend first

Build the interface and user flow before deep backend implementation whenever the product allows it.

Sequence:

1. define screens and states;
2. build the interface with mocked data;
3. exercise the main flows end to end;
4. identify the data contracts the UI actually needs;
5. implement backend/storage/auth boundaries against those contracts;
6. replace mocks incrementally;
7. verify the real flow against the original design.

The purpose is not cosmetic polish. The frontend is used to expose missing product decisions before backend structure hardens around them.

### Repository structure for AI-assisted work

For a coupled full-stack product, default to a monorepo so agents can inspect frontend, backend, shared types, tests, and product rules in one working tree.

Keep boundaries explicit even inside one repository:

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

Use separate repositories only when deployment, ownership, security, or lifecycle boundaries make the separation materially useful. Do not split repositories merely because frontend and backend use different languages.

## Required input

Use the information already available. Ask only for missing details that materially change the product architecture.

Preferred input shape:

```markdown
**Product Concept & Audience:** [product, users, platform]
**Desired UX Style / Reference:** [reference product, visual direction, or interaction style]
**Key User Flows:** [2–3 main user paths]
**Execution Setup:** [Solo + AI / Team]
```

## Choose the output that fits the request

For a full UI product brief, return the four sections below in order. For a
focused stack, flow, or repository question, return only the relevant sections.
For terminal, API, or background products, describe commands, requests, states,
and failure paths instead of inventing screens.

### 1. UX/UI and screen architecture

For each primary flow, show:

```text
entry → screen/state → action → next state → completion/failure
```

Then list the minimum screen set and the purpose of each screen.

### 2. Tech stack selection

Name the chosen stack and justify each major choice against a product requirement.

Also state one credible alternative and why it was not chosen.

### 3. Frontend-first implementation sequence

Provide an ordered build sequence from mocked interface to integrated product.

Mark where backend, persistence, auth, external APIs, tests, and deployment first become necessary.

### 4. Repository structure

Show the minimum useful directory/monorepo structure for the chosen stack.

## Guardrails

- Do not select a fashionable stack without tying it to the product.
- Do not invent user needs that were not stated or strongly implied.
- Do not expand the product into a large feature roadmap before the core flows work.
- Do not treat wireframes as decoration; they define implementation boundaries.
- Do not build backend abstractions before the interface reveals the required contracts.
- Do not claim a monorepo is universally superior; use it as the default for tightly coupled AI-assisted full-stack work and state exceptions.
- Keep the first implementation small enough to test the core product assumption.
