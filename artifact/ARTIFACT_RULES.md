# Artifact Rules

## PDF Handling

- For scanned PDFs: `pdfinfo` -> one `pdftotext -layout` check -> if empty, render with `pdftoppm` to `tmp/pdfs/` and inspect PNGs with `view_image` original detail.
- Keep a tiny inventory: page count, text-extraction result, and what the pages contain.
- Stay local-first; no internet OCR/upload unless explicitly requested.
- After editing or creating a PDF the user needs to inspect, first verify locally by rendering a page/image.
- Then use the environment's documented user-visible opener and confirm that the viewer starts. On Masih's workstation, follow the `workstation` skill's `op` procedure.

## HTML UI Verifiability

- When creating reports, prototypes, dashboards, visual research artifacts, or demos, make the result visible in HTML.
- The HTML should show the actual artifact: text, formulas, tables, charts, controls, outputs, and relevant state/results.
- After creating or meaningfully editing a user-facing HTML report/artifact, open it for the user unless they explicitly say not to. A screenshot or headless render is verification, not a substitute for opening the artifact.
- Open HTML files in Chromium. Prefer a local HTTP server for site folders, especially when assets/scripts/maps exist: `setsid python3 -m http.server <port> --directory <site-dir> >/tmp/<task>-server.log 2>&1 &`, then open `http://127.0.0.1:<port>/...` in Chromium. Use `file://` only for simple standalone HTML. If Chromium loads indefinitely, switch from `file://` to local HTTP before claiming it is open.
- Browser automation and screenshots are token/compute expensive. Prefer cheaper local checks unless the UI/formulas/charts are newly created or materially changed; in those cases do one visual verification pass before opening for the user.
- If there are multiple design/options, make them switchable in the HTML rather than only describing them in chat.
- Keep the source file too when useful, such as Markdown, notebook, Python, or JS.

## HTML Slide/PDF Layout Lessons

- For browser-printed HTML slides, do not rely on `.active` styles for PDF output. Print mode often forces every `.slide` to `display:flex`; put layout-critical defaults such as `flex-direction`, `justify-content`, and `gap` on the base `.slide` class.
- Verify spatial layout by rendering the generated PDF pages, not by reading extracted PDF text. Use spot checks for the most layout-sensitive pages and a contact sheet for the whole deck.
- In RTL slide decks with image/text split layouts, CSS grid can inherit `direction: rtl` and visually reverse columns. Set the split container to `direction:ltr` for physical left-to-right grid placement, then set the text area back to `direction:rtl`.
- For mixed Persian/English slide text, prefer Persian-led phrasing and isolate short English terms only when needed; long English-led bullets often render with broken order in PDF.

## XeLaTeX Bilingual / RTL Typesetting Lessons (Farsi & English)

When compiling XeLaTeX with Babel Farsi (RTL) and English (LTR) languages:
1. **Paragraph Termination**: Always insert a blank line (paragraph break) immediately before starting any LTR environment (like `\begin{otherlanguage}{english}` or `\begin{LTR}`). This terminates the RTL Farsi paragraph first, preventing bidi direction stack mismatch (`\endL or \endR` compiler errors).
2. **English Typewriter Font**: Always define English typewriter fonts in the preamble:
   ```latex
   \babelfont{tt}[]{DejaVu Sans Mono}
   \babelfont[english]{tt}[]{DejaVu Sans Mono}
   ```
   **CRITICAL PYTHON ESCAPING WARNING**: When writing or replacing text in LaTeX files using Python, never write `\b` inside regular double-quoted strings (e.g. `"\babelfont"`), as Python interprets `\b` as an ASCII backspace (`0x08`). This corrupts the command to `\x08abelfont` and causes XeLaTeX to render the command name itself as empty rectangles. Always use raw strings (`r"\babelfont"`) or double backslashes (`"\\babelfont"`).
3. **Itemize Bullet Points**: In Babel RTL mode, standard list item bullets (`\item`) use the text bullet (U+2022) which B-Nazanin fails to render, drawing empty rectangles. Always redefine itemize bullets to math-mode symbols in the preamble so they use math fallback fonts (DejaVu Sans):
   ```latex
   \renewcommand{\labelitemi}{$\bullet$}
   \renewcommand{\labelitemii}{$-$}
   \renewcommand{\labelitemiii}{$\ast$}
   \renewcommand{\labelitemiv}{$\cdot$}
   ```
4. **Math Mode Latin Characters**: Ensure all Latin variable names and text inside math blocks (like `u`, `v`, `f`, `x`, `y` or `\text{since}`) are wrapped in `\mathrm{...}`, `\eng{...}`, or `\text{\eng{...}}` to prevent them from falling back to Farsi fonts and rendering as empty squares `☐`.
5. **No ZWNJs in Nazanin**: The B-Nazanin font fails to display the zero-width non-joiner (`\u200c`), rendering it as an empty square. Always replace ZWNJs (`\u200c`) with spaces in `.tex` files.
6. **English Words in Farsi Blocks**: English words inside Farsi blocks (like `\textbf{... (Notch Reject) ...}`) that are not wrapped in `\eng{...}` or an LTR block will render as empty rectangles. Wrap them in `\eng{...}`.


## HTML Formula Rendering Harness

Use this whenever an HTML report/page needs mathematical formulas.

- Do not put raw LaTeX delimiters such as `\(...\)`, `\[...\]`, or `$$...$$` directly into handwritten HTML and assume the browser will render them. Browsers show those as text unless a renderer or MathML is present.
- For handwritten HTML, prefer native MathML directly in the file. This is the most reliable local-first method because Chromium/Firefox render it without internet or extra JavaScript. Use a styled wrapper such as:

```html
<div class="math-display">
  <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
    <mrow>
      <msub><mi>s</mi><mi>k</mi></msub>
      <mo>=</mo>
      <mi>T</mi><mo>(</mo><msub><mi>r</mi><mi>k</mi></msub><mo>)</mo>
      <mo>=</mo>
      <munderover>
        <mo>&#x2211;</mo>
        <mrow><mi>j</mi><mo>=</mo><mn>0</mn></mrow>
        <mi>k</mi>
      </munderover>
      <msub><mi>p</mi><mi>r</mi></msub>
      <mo>(</mo><msub><mi>r</mi><mi>j</mi></msub><mo>)</mo>
    </mrow>
  </math>
</div>
```

- Recommended CSS:

```css
.math-display {
  direction: ltr;
  text-align: center;
  background: #fbfcfe;
  border: 1px solid #d9e0e8;
  border-radius: 6px;
  padding: 12px 14px;
  margin: 10px 0;
  overflow: auto;
}
.math-display math { font-size: 1.18rem; }
```

- If starting from Markdown instead of handwritten HTML, use Pandoc to generate the same kind of browser-renderable MathML:

```bash
pandoc input.md -s --mathml -c style.css -o output.html
```

- Verify formulas became real MathML and that raw TeX delimiters are not left behind:

```bash
rg -n '<math' output.html | head
rg -n '\[|\]|\$\$' output.html | head
```

- If MathML is too slow to author for a large document, use Pandoc Markdown-to-MathML rather than raw TeX in HTML. A real renderer such as MathJax/KaTeX is acceptable only when its script/CSS is included and verified; avoid CDN/network renderers unless internet use is acceptable for the task.
- A plain-text formula block is acceptable only when the user does not need typeset math; label ambiguous notation in words, e.g. `G_inverse(s_k)` means inverse CDF, not exponentiation.
- Verification before delivery:
  - Render/open the HTML in Chromium or the target viewer.
  - Confirm formulas visually render as math, not literal TeX delimiters.
  - For reports with formulas, keep the source `.md` alongside generated `.html` when practical.
- Two approaches proven to work in practice:
  - Handwritten native MathML inside a `.math-display` block.
  - Markdown `$$...$$` converted by Pandoc into `<math ...>` MathML, emitted alongside the source `.md`.
