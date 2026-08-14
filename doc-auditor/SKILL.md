---
name: doc-auditor
description: >-
  Audits documentation, reports, HTML files, and markdown notes produced by AI agents.
  Identifies candidates for deletions, obsolete claims (e.g., 'no cost', unverified tasks,
  or AI meta-commentary talking to itself), and reports flagged sections for cleanup.
---

# Documentation & Agent Notes Auditor (`doc-auditor`)

This skill provides instructions for scanning project documentation, HTML artifacts, and markdown notes written by agents to find content that should be pruned or deleted.

---

## Deletion Targets & Audit Criteria

When reviewing files generated or modified by AI agents, flag any text that falls into the following categories:

### 1. AI Self-Talk & Meta-Commentary
* **What to look for**: Statements where the agent talks to itself, reflects on its internal process, or notes incomplete thoughts not intended for human consumption.
* **Examples**:
  * *"I couldn't finish this section because..."*
  * *"Things that weren't done:"*
  * *"Note to self / next agent: check back later..."*
  * Unresolved self-dialogue or internal scratchpad notes embedded in public docs or HTML files.

### 2. Obsolete / Invalid Financial or Constraint Claims
* **What to look for**: Outdated, inaccurate, or unverified claims about pricing, costs, or API tiers.
* **Examples**:
  * Stale assertions of *"no cost"*, *"100% free forever"*, or unverified free-tier promises without backing source/date context.

### 3. Abandoned / Partial Work Logs
* **What to look for**: Outdated progress logs, scratch notes, or temporary status summaries left in permanent files.
* **Examples**:
  * Inline `TODO` items describing completed agent iterations.
  * Incomplete task lists or status tables in docs when the feature was abandoned or refactored.

---

## Audit & Verification Workflow

1. **Scan Files**:
   * Search markdown (`*.md`) and HTML (`*.html`) files in target project documentation directories or output directories.
   * Target patterns: `no cost`, `things that weren't done`, `not done`, `AI note`, `TODO`, etc.

2. **Categorize Candidates**:
   * Group findings by file and flag category (Self-Talk, Obsolete Claims, Abandoned Work).

3. **Generate Side-by-Side Visual HTML Diff**:
   * For any proposed file modifications or deletions, generate a self-contained HTML diff file in a temporary folder (e.g., `<appDataDir>/brain/<conversation-id>/scratch/diff_<filename>.html` or `/tmp/doc_auditor_diffs/<filename>_diff.html`).
   * Structure the diff using side-by-side comparison tables or inline highlighted blocks using GitHub-style color tokens:
     * **Deletions / Before (`.del`)**: `--del-bg: #ffeef0; --del-fg: #82071e;` (Dark mode: `--del-bg: #3b1219; --del-fg: #ffa198;`)
     * **Insertions / After (`.ins`)**: `--ins-bg: #e6ffed; --ins-fg: #116329;` (Dark mode: `--ins-bg: #0f2c1c; --ins-fg: #7ee2a8;`)
   * Include clear side-by-side headers (`BEFORE (Original File)` vs `AFTER (Proposed Clean Version)`).

4. **Approval & Cleaning Policy**:
   * **HTML Files**: Can be cleaned/updated directly without prior user approval (still generating a temp HTML diff for reference).
   * **Markdown (`.md`) Files**: **REQUIRE EXPLICIT USER APPROVAL**. Present the itemized list of deletion candidates, show the generated HTML diff link, and ask for confirmation before editing any `.md` file.


