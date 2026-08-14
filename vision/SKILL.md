---
name: vision
description: Project orientation skill — locate or create the project's vision/identity file on arrival. Use on the first message in an unfamiliar project, when the user says "familiarize yourself", or "orient yourself", or before beginning a large task without project context.
---

# Vision

Find the document that says what the project is, why it exists, and where things live before changing anything.

## Find the orientation file

List root Markdown files, then check these names in order:

1. `VISION.md`
2. `AGENTS.md`
3. `CLAUDE.md`
4. `AGENT.md`
5. `README.md`

Read the first applicable file. Prefer the most project-specific source when several exist.

## Extract the map

Identify:

- the project's one-line identity;
- its top-level directory map;
- what is implemented versus aspirational;
- current constraints and non-goals.

## Create a vision when absent

If no orientation file exists:

1. Inspect the project structure to a depth of two.
2. Draft `VISION.md` with identity, purpose, directory map, honest current state, and non-goals.
3. Show the draft to the user before saving it.

## Flag drift

If the orientation file contradicts the repository structure or another authoritative document, report the conflict. Do not silently choose which source is correct.
