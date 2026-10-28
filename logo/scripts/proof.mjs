import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const modulePath = process.env.SVG_STUDIO_MODULE;
if (!modulePath) throw new Error('Set SVG_STUDIO_MODULE to SVG Studio’s built multicolour dist/vectorize.js module.');
const sharp = createRequire(pathToFileURL(modulePath))('sharp');
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, basename, join } from 'node:path';
import { assertVector } from './vector-contract.mjs';

const [output, ...pairs] = process.argv.slice(2);
if (!output || !/\.png$/i.test(output) || !pairs.length || pairs.length % 2) throw new Error('Usage: node proof.mjs sheet.png source-cutout.png mark.svg [source.png mark.svg ...]');
const esc = value => value.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const sizes = [24, 48, 128, 512];
const grounds = [['light', '#fbfbfa', '#202736'], ['dark', '#10151d', '#eef0f4']];
const width = 2184, rowHeight = 780, header = 76, height = header + rowHeight * pairs.length / 2;
const layers = [], labels = [], stats = [];
labels.push(`<rect width="${width}" height="${height}" fill="#e6e8eb"/>`);
labels.push('<text x="24" y="32" font-size="25" font-weight="700">VISUAL PROOF · SOURCE → SVG</text>');
labels.push('<text x="24" y="58" font-size="16">Actual 24 / 48 / 128 / 512 px · Source left, SVG right in every pair · Light and dark</text>');
const renderDir = join(dirname(output), 'renders');
await mkdir(renderDir, { recursive: true });
for (let row = 0; row < pairs.length / 2; row++) {
  const [source, file] = pairs.slice(row * 2, row * 2 + 2);
  const svg = await readFile(file, 'utf8');
  assertVector(svg);
  const name = basename(file, '.svg'), y = header + row * rowHeight;
  const paths = [...svg.matchAll(/<path\b/g)].length;
  labels.push(`<text x="24" y="${y + 28}" font-size="23" font-weight="700">${esc(name.toUpperCase())}</text>`);
  labels.push(`<text x="400" y="${y + 28}" font-size="16">${paths} colour paths · ${(Buffer.byteLength(svg) / 1024).toFixed(1)} KiB</text>`);
  for (let ground = 0; ground < 2; ground++) {
    const [theme, background, ink] = grounds[ground], x = 24 + ground * 1080;
    labels.push(`<rect x="${x}" y="${y + 42}" width="1056" height="728" rx="10" fill="${background}"/>`);
    labels.push(`<text x="${x + 18}" y="${y + 69}" fill="${ink}" font-size="17">${theme.toUpperCase()} · SOURCE / SVG · 512 px</text>`);
    for (const size of sizes) {
      // Commit the transparent resize before flattening. Sharp may otherwise
      // flatten first and leave opaque black contain-padding in RGB sources.
      const sourceSquare = await sharp(source).ensureAlpha()
        .resize(size, size, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
        .png().toBuffer();
      const src = await sharp(sourceSquare).flatten({ background }).png().toBuffer();
      // Rasterise at the target size rather than downsampling a large SVG preview.
      const vector = svg.replace(/\bwidth="[^"]+"/, `width="${size}"`).replace(/\bheight="[^"]+"/, `height="${size}"`);
      const dst = await sharp(Buffer.from(vector)).resize(size, size).flatten({ background }).png().toBuffer();
      const a = await sharp(src).removeAlpha().raw().toBuffer(), b = await sharp(dst).removeAlpha().raw().toBuffer();
      let error = 0, changed = 0, foregroundError = 0, foregroundChanged = 0, foregroundPixels = 0;
      const rgbBackground = [1, 3, 5].map(offset => parseInt(background.slice(offset, offset + 2), 16));
      for (let i = 0; i < a.length; i += 3) {
        let worst = 0, pixelError = 0, foreground = false;
        for (let c = 0; c < 3; c++) {
          const d = Math.abs(a[i+c] - b[i+c]); error += d; pixelError += d; worst = Math.max(worst, d);
          foreground ||= Math.abs(a[i+c] - rgbBackground[c]) > 8 || Math.abs(b[i+c] - rgbBackground[c]) > 8;
        }
        if (worst > 32) changed++;
        if (foreground) { foregroundPixels++; foregroundError += pixelError; if (worst > 32) foregroundChanged++; }
      }
      stats.push({ name, theme, size, paths, bytes: Buffer.byteLength(svg), meanDifference: error / a.length / 255, changedPixels: changed / (a.length / 3), foregroundMeanDifference: foregroundPixels ? foregroundError / (foregroundPixels * 3 * 255) : 0, foregroundChangedPixels: foregroundPixels ? foregroundChanged / foregroundPixels : 0, foregroundPixels });
      const left = size === 512 ? x + 8 : x + ({24: 24, 48: 190, 128: 400}[size]);
      const top = size === 512 ? y + 82 : y + 590 + Math.floor((128-size)/2);
      layers.push({ input: src, left, top }, { input: dst, left: left + size + 8, top });
      if (size !== 512) labels.push(`<text x="${left}" y="${y + 750}" fill="${ink}" font-size="15">${size} px · source / SVG</text>`);
      await writeFile(join(renderDir, `${name}-${theme}-${size}-source.png`), src);
      await writeFile(join(renderDir, `${name}-${theme}-${size}-svg.png`), dst);
    }
  }
}
const canvas = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" font-family="DejaVu Sans, sans-serif" fill="#202736">${labels.join('')}</svg>`;
await mkdir(dirname(output), { recursive: true });
await sharp(Buffer.from(canvas)).composite(layers).png().toFile(output);
await writeFile(output.replace(/\.png$/i, '.json'), JSON.stringify(stats, null, 2)+'\n');
await writeFile(output.replace(/\.png$/i, '.html'), `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Source and SVG proofs</title><style>body{margin:0;background:#e6e8eb;font:16px sans-serif}p{margin:16px}img{display:block;max-width:100%;height:auto}a{color:#263c77}</style><p>Source left, SVG right. <a href="${esc(basename(output))}">Open full-resolution proof</a> to inspect actual pixel sizes.</p><img src="${esc(basename(output))}" width="${width}" height="${height}" alt="Source compared with multicolour SVG on light and dark backgrounds at 24, 48, 128 and 512 pixels"></html>\n`);
console.log(`${output}: ${pairs.length / 2} marks, ${stats.length * 2} source/SVG renders`);
