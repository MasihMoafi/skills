---
name: word-farsi-docx
description: Converting Persian (Farsi) reports to a clean .docx (B Nazanin) without breaking formatting.
---

A proven approach for producing clean Persian Word output from a B Nazanin template.

---

## Goal

- Produce a **Word-native** `.docx` (not “PDF-in-Word”) that:
  - keeps a **clean academic template** (margins, spacing, headings)
  - is **RTL-correct** (Persian punctuation + alignment)
  - uses **B Nazanin everywhere** (including Latin/English segments inside Persian text)
  - supports **tables, bullets, headings, page breaks, images**
  - avoids common TeX/PDF → Word failures (broken fonts, misaligned text, weird placeholder squares, mixed direction)

---

## Tools

- **python-docx** for Word generation and styling
- Optional: **PDF → images** or **PDF text extraction** for reference, then rebuild content *as Word objects* (paragraphs/tables/images)
- Validation: render the final document with an available Word-compatible renderer, then inspect its pages and compare against the reference. If rendering is unavailable, report visual verification as incomplete.

---

## Method (the important part)

### 1) Start from a known-good template `.docx`
Instead of styling from scratch, start from a “golden” template file that already looks right:

- correct margins
- correct spacing rules
- clean headings
- a consistent look

**Why:** Word styling is fragile; starting from a template reduces surprises.

### 2) Clear the document body but keep section properties (`sectPr`)
When replacing content, remove everything in the body **except** the section properties (`w:sectPr`).

**Why:** `sectPr` stores page size, margins, and layout. If you delete it, Word changes your whole page geometry.

### 3) Force RTL at the paragraph level
For every paragraph:
- set alignment **RIGHT**
- explicitly add the RTL flag: `w:bidi = 1`

**Why:** Persian can *look* right but behave wrong (punctuation, numbering, mixed Latin tokens) unless RTL is explicitly enabled.

### 4) Force B Nazanin at the run level (not just paragraph style)
For every run, set fonts in `w:rFonts` for:

- `w:ascii`
- `w:hAnsi`
- `w:cs`
- `w:eastAsia`

…and also set `run.font.name = "B Nazanin"`.

**Why:** Mixed-script runs (English inside Persian) often silently fall back to other fonts unless **all** channels are set.

### 5) Use Word-native structures (do not “paste PDF”)
Rebuild content as:
- **Headings** (Heading 1/2… or custom)
- **Normal paragraphs**
- **Bullets / numbered lists**
- **Tables** (Table Grid style)
- **Images** inserted with captions

**Why:** If you embed PDF pages or copy rendered text, Word sees it as an image/shape and you lose editability + consistent layout.

### 6) Control spacing explicitly (avoid “random Word spacing”)
For key paragraphs/headings, set spacing in `w:spacing`:
- `after = 120` (example; adjust as needed)

**Why:** Persian text can balloon spacing because Word decides “helpful” defaults.

### 7) Tables: build with `doc.add_table` and style them
- Use `Table Grid` (or your preferred template table style)
- Make header row **bold**
- Apply RTL and B Nazanin inside each cell paragraph/run

**Why:** Tables are where direction/font bugs show up first.

### 8) Page breaks intentionally
Insert `doc.add_page_break()` at logical boundaries:
- after cover
- after abstract
- between major sections

**Why:** Prevents Word from reflowing sections in unpredictable ways.

### 9) Final enforcement pass (must-do)
After all content is added:
- iterate all paragraphs and runs
- re-apply **RTL + B Nazanin**
- ensure centered paragraphs stay centered (cover), but still keep correct bidi handling

**Why:** Some operations add runs with default fonts or drop bidi flags.

### 10) Export-safe filenames (fix download issues)
If your environment/client has trouble downloading Persian filenames, duplicate the output:
- original Persian filename
- **ASCII-only filename** copy
- optional `.zip`

**Why:** Some systems fail on non‑ASCII filenames even when the file is valid.

---

## Quality checklist

- Persian punctuation looks correct (، ؛ ؟) and stays RTL
- English terms are inside parentheses and don’t break the sentence flow
- No “□ □” placeholder blocks
- Headings are bold and sized consistently
- Bullets align correctly in RTL
- Tables remain readable, aligned, and don’t overflow
- Images are not distorted and have captions
- Page breaks are where they should be

---

## Common failure modes and fixes

- **Font looks wrong** → enforce `w:rFonts` for all four channels (ascii/hAnsi/cs/eastAsia)
- **RTL looks OK but punctuation is wrong** → add `w:bidi=1` in paragraph properties
- **Layout changed after editing** → you accidentally removed `sectPr`; keep it
- **File downloads fail** → save an ASCII-named duplicate or zip it
