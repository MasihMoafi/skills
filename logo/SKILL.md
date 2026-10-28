---
name: logo
description: Generate logos, icons, ornaments, illustrations, badges and diagrams with the image tool, then keep the chosen artwork as real SVG paths through SVG Studio. Use for an image-first visual-to-SVG request or /logo.
---

# Image first, then SVG

This workflow handles visual assets beyond logos. Keep the original raster, the
selected SVG and evidence of their match. A raster embedded inside SVG is not a
vector conversion.

## Establish the artwork

1. Read the brief and inspect supplied artwork. Record the intended display size,
   background, exact labels and any approved geometry or colours. Use the user's
   actual selection as evidence; an agent's suggestion is not approval. Keep
   approved lettering or existing marks separate from a new background ornament.
2. Use the built-in image generation tool for new artwork. Read that tool's live
   instructions, including local-reference and transparency handling. Do not
   substitute a hand-coded SVG before the requested image exists, switch to an
   API-key workflow, install a package or contact another image service on your
   own. If the tool is unavailable, report that dependency plainly.
3. Save exact prompts and originals in the task's artifact folder. For a new logo
   or an exploratory design, generate three distinct candidates, one image per
   call. For an already selected visual, make the requested asset directly.
   Inspect each candidate. Respect the user's palette, references and constraints;
   favour clean contours and large useful negative spaces for flat vector art.
4. Select a candidate and explain the choice briefly. Use image generation for
   revisions. Do not silently redraw a different design during vector conversion.

   Show candidates as inline images in the final response. A recommendation is not a
   selection: wait for the user's choice before applying artwork or installing it.

## Convert through SVG Studio

5. Use SVG Studio's `vectorize_multicolour_image` MCP tool for coloured artwork.
   Pass its image path, output path and a palette size from 2 to 64. Preserve
   generated alpha; remove the background only when requested. Use monochrome
   tracing only for monochrome source art.
6. When the MCP tool is not exposed, use the included CLI wrapper with an existing
   SVG Studio engine. Set `SVG_STUDIO_MODULE` to the absolute path of the built
   `mcp-server/dist/vectorize.js` that exports `vectorizeMulticolourImage`.
   Resolve the scripts relative to this skill's folder. From that folder:

   ```sh
   SVG_STUDIO_MODULE=/path/to/svg-studio/mcp-server/dist/vectorize.js \
     node scripts/trace.mjs source.png output.svg 24
   ```

   The wrapper validates this capability before conversion. A build with only
   monochrome tracing does not support the colour workflow. Do not silently
   collapse the palette or claim a missing backend is installed.
7. Pick the smallest palette that visibly preserves the source. Record colour
   count, engine and settings. Treat soft transparency, gradients, photographs
   and very fine detail as measured approximations. For exact diagrams, charts
   or scientific labels, retain the authoritative data and check every label
   against it; tracing alone does not establish correctness or editability.
8. Require real vector paths, a useful viewBox and explicit colour fills. Reject
   embedded rasters, scripts, foreignObject, external references and fonts. Keep
   masks and compound holes intact. Record any cropping, trimming or other
   optical adjustment and retain the unmodified original.

## Verify and deliver

9. Run the included proof tool using the same engine installation:

   ```sh
   SVG_STUDIO_MODULE=/path/to/svg-studio/mcp-server/dist/vectorize.js \
     node scripts/proof.mjs proof.png source.png output.svg
   ```

   Inspect source/SVG pairs on dark and light backgrounds at 24, 48, 128 and
   512 px. Also render at the intended website or illustration size. Measure
   differences on both the full frame and artwork foreground; padding must not
   dominate the result. Inspect silhouettes, negative spaces, holes, edge speckles,
   colour banding, margins and contrast. Report material limitations honestly.
   Visible damage fails the review even if the average pixel error is small.
   If tracing cannot preserve a gradient or fine detail, revise the source through
   image generation toward simpler fills, then trace and compare again. Do not
   integrate a visibly inferior conversion as a finished asset.
10. Save the selected raster, standalone SVG, prompts, settings, choice rationale
    and proof images together. Integrate into a local draft when authorized and
    check the actual UI, keyboard labels and reduced-motion behaviour. Publish or
    install only within the user's authorized scope; distinguish a draft file,
    a registered skill, and a public release in the final report.

The CLI scripts reuse SVG Studio's installed engine and dependencies. They do not
include a second tracer or depend on a particular user's home directory.
The proof tool needs the engine installation's `sharp` dependency. Run its
regression checks from this folder with:

```sh
SVG_STUDIO_MODULE=/path/to/svg-studio/mcp-server/dist/vectorize.js \
  node --test test/pipeline.test.mjs
```
