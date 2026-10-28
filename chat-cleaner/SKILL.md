---
name: chat-cleaner
description: Use when the user asks to inventory, name, archive, or delete agent conversations whose history has become difficult to navigate.
---

# Chat Cleaner

Map conversation history read-only first. Session storage may include indexes,
active writers, credentials, and recovery state, so a raw log file is not
automatically a safe deletion unit.

## Step 1 — Locate chat storage

Identify the product and prefer its supported history command, API, or interface.
Consult product documentation before touching private storage. Common locations
are clues for read-only discovery, not authorization to edit them:

| Tool | Default chat location |
|---|---|
| Claude Code | `~/.claude/` or project-local `.claude/` |
| Antigravity / AGY | `~/.gemini/antigravity-cli/brain/` |
| Codex | `~/.codex/` or per-project `.codex/` |
| Generic | `~/.config/<tool>/history/`, `~/.local/share/<tool>/` |

If no supported inventory exists, search only the confirmed history root for
that product, with a shallow depth and file-type filter. Never scan another
product's storage, the whole filesystem, or print message bodies unnecessarily.

## Step 2 — Map sessions

For each confirmed session record, extract:

- **ID** (filename or internal ID)
- **Title or a short local summary**—avoid exposing full message content
- **Last activity timestamp**
- **Message count** — rough proxy for depth
- **Named?** — does it have a human-readable title or is it a raw UUID?

Output a table:

| ID (short) | Name / Short summary | Last active | Messages | Keep? |
|---|---|---|---|---|

## Step 3 — Flag deletion candidates

Bulk removal of old Claude, Codex and Elpis chat logs (untouched for 24 hours) belongs to the
`clean-system` skill's `clean.py`, without per-session approval (Masih, 14 Oct 2026). Use the steps
below only for naming or for choosing among recent sessions.

Suggest a session for review if:

- Zero or one user message (abandoned before anything happened)
- Last activity > 90 days ago with < 5 messages
- Its content and identity are confirmed duplicates, not merely similar titles
- Name is a raw UUID and content is trivial (single greeting, test message)

These are heuristics, not proof. Present the list to the user and wait for
confirmation; do not auto-delete.

## Step 4 — Name unnamed sessions

For sessions worth keeping but without a human name:

- Derive a short name (3–6 words) from the first meaningful user message.
- Propose the name; apply it only through a supported command or interface after
  the user confirms. Do not rewrite raw logs or indexes to simulate a rename.

## Step 5 — Delete confirmed sessions

Only after explicit user approval per session or clearly identified batch, use
the product's supported delete/archive operation. If none exists, explain that
raw deletion may corrupt the history index and offer a recoverable archive or
trash operation for exact confirmed records. Report what changed and whether it
can be recovered.

## Output format

Produce a clean markdown summary:

- **Kept**: N sessions (list with proposed names if renamed)
- **Deleted**: N sessions (list with reason)
- **Skipped / needs review**: any ambiguous cases

## Caution

- Never delete the current active session or any session with an active writer.
- Never edit or delete shared indexes, databases, credentials, or configuration
  merely because they live beside session files.
- If session files are in a format you can't parse, report the path and format — don't guess.
- Chat history may contain keys, tokens, or personal data. Keep all operations local.
