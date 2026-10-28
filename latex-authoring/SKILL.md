---
name: latex-authoring
description: Write, structure and compile LaTeX papers and reports (NeurIPS, ICML, ICLR, IEEE, ACM). Use for TeX manuscripts, LaTeX/XeLaTeX build errors, BibTeX checks, TikZ diagrams or publication typesetting.
---

# LaTeX Academic Authoring & Graph Verification

A rigorous, publication-grade workflow for writing, compiling, debugging, and verifying LaTeX manuscripts. Enforces mathematical precision, clean modular architecture, and verifiable citation integrity without hallucinated references.

---

## 1. Core Principles

- **Zero Hallucinated Citations:** Every BibTeX entry must be backed by a verified DOI, arXiv ID, or official venue record. Never generate fictitious authors or titles.
- **Deterministic Build Harness:** Compile exclusively via non-interactive `latexmk` pipelines with halt-on-error flags. Clean builds must produce 0 undefined references (`??`) and 0 missing citation warnings.
- **Modular File Layout:** Never write an entire paper in a single monolithic `.tex` file. Separate structure, macros, sections, figures, and bibliography.
- **Visual Inspection via Headless Renders:** Always spot-check generated PDFs for overfull boxes, floating element collisions, and typesetting defects using local image renders (`pdftoppm`).

---

## 2. Canonical Project Architecture

```
paper/
├── main.tex              # Document root: documentclass, package imports, section inputs
├── macros.tex            # Custom mathematical notation and semantic commands
├── references.bib        # Verified BibTeX citation database
├── sections/             # Modular section content
│   ├── 00_abstract.tex
│   ├── 01_introduction.tex
│   ├── 02_related_work.tex
│   ├── 03_methodology.tex
│   ├── 04_experiments.tex
│   └── 05_conclusion.tex
├── figures/              # Vector graphics (PDF/EPS), raster images (PNG), TikZ code
└── tables/               # Standalone table files (input via \input{tables/...})
```

### Preamble & Package Loading Hierarchy
Load packages in strict dependency order to avoid namespace collisions:

1. **Math & Fonts:** `amsmath`, `amssymb`, `mathtools`, `bm`
2. **Tables & Arrays:** `booktabs`, `multirow`, `tabularx`, `array`
3. **Graphics & Floats:** `graphicx`, `subcaption`, `float`, `placeins`
4. **Algorithms:** `algorithm`, `algpseudocode` (or `algorithm2e`)
5. **Cross-Referencing:** `hyperref` (loaded late), followed immediately by `cleveref`

---

## 3. Mathematical & Typographical Hygiene

- **Semantic Notation Macros:** Define notations centrally in `macros.tex`:
  ```latex
  \newcommand{\E}{\mathbb{E}}
  \newcommand{\R}{\mathbb{R}}
  \newcommand{\Loss}{\mathcal{L}}
  \DeclareMathOperator*{\argmax}{arg\,max}
  \DeclareMathOperator*{\argmin}{arg\,min}
  ```
- **Equation Hygiene:**
  - Use `align` or `align*` for multi-line equations; never use raw `$$ ... $$` or deprecated `eqnarray`.
  - Punctuate every displayed equation with trailing periods, commas, or semicolons as part of the sentence structure.
  - Number only equations referenced in text; use `\nonumber` or `autonum` for unreferenced expressions.
- **Table Standards:**
  - Always use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`).
  - **NEVER use vertical rules (`|`) in tables.** Use subtle spacing (`\addlinespace`) instead.
  - Right-align numeric columns; left-align textual descriptions.
- **Float Placement:**
  - Standard float specifier: `\begin{figure}[t!]` (top of page is preferred in two-column formats).
  - Use `\FloatBarrier` (from `placeins`) at the end of sections to prevent figures from drifting into subsequent sections.

---

## 4. Compilation & Diagnostic Protocol

Always compile using `latexmk` in non-interactive batch mode:

### Standard PDFLaTeX Compilation
```bash
latexmk -pdf -synctex=1 -interaction=nonstopmode -halt-on-error main.tex
```

### Bilingual / XeLaTeX Compilation (e.g. Persian/English Babel)
```bash
latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error main.tex
```

### Automated Diagnostic Log Parser
When a build fails, filter the `.log` file immediately rather than reading thousands of lines:

```bash
rg -A 3 -B 1 '^!|LaTeX Warning|Package.*Warning' main.log | rg -v 'fontspec' | head -n 40
```

### Critical Troubleshooting Table

| Error / Warning in Log | Root Cause | Immediate Fix |
| :--- | :--- | :--- |
| `! Undefined control sequence.` | Typo in macro or missing package | Check macro definition in `macros.tex` or load missing package |
| `LaTeX Warning: Reference '...' undefined` | Missing `\label` or missing 2nd compile pass | Ensure label exists in target section; run `latexmk` full pass |
| `LaTeX Warning: Citation '...' undefined` | Missing key in `references.bib` | Verify BibTeX key spelling; run `bibtex main` |
| `Overfull \hbox (X pt too wide)` | Equation, table, or long word exceeds column width | Wrap equation with `\split` / `\multline`; shorten table columns |
| `\endL or \endR error` (XeLaTeX / RTL) | Paragraph break missing before LTR environment | Add an explicit blank line before switching to LTR blocks |

---

## 5. BibTeX Citation Graph Verification

Maintain citation purity with this 4-step verification check:

1. **Verify Identifiers:** Every entry in `references.bib` must have a valid `doi = {...}`, `eprint = {...}`, or exact publication venue.
2. **Canonical BibTeX Schema:**
   ```bibtex
   @inproceedings{vaswani2017attention,
     author    = {Ashish Vaswani and Noam Shazeer and Niki Parmar and Jakob Uszkoreit and Llion Jones and Aidan N. Gomez and Lukasz Kaiser and Illia Polosukhin},
     title     = {Attention is All You Need},
     booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
     volume    = {30},
     pages     = {5998--6008},
     year      = {2017},
     doi       = {10.5555/3295222.3295349}
   }
   ```
3. **Key Deduplication:** Check for duplicate citation keys:
   ```bash
   rg -o '^@[a-zA-Z]+\{[^,]+' references.bib | sort | uniq -d
   ```
4. **Unused Citations:** After a successful build, compare bibliography keys against the cited keys in all generated `.aux` files (or the `.bcf` file for Biber). Account for `\nocite{...}`, `\nocite{*}`, and included documents. Report unused candidates; remove them only when cleanup is in scope. A bibliography syntax check alone does not establish citation usage, and failed checks must remain visible.

---

## 6. Visual Verification & Open Protocol

1. **Render Pages to PNG for Headless Spot-Checks:**
   ```bash
   mkdir -p /tmp/paper_renders && pdftoppm -png -r 150 -f 1 -l 3 main.pdf /tmp/paper_renders/page
   ```
2. **Open for User Inspection:** Follow the environment's documented user-visible opening procedure and confirm that the viewer starts. On Masih's workstation, use the `workstation` skill's `op` procedure.
