import assert from 'node:assert/strict';
import test from 'node:test';
import { mkdtemp, readFile, writeFile, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const run = promisify(execFile);
const trace = fileURLToPath(new URL('../scripts/trace.mjs', import.meta.url));
const proof = fileURLToPath(new URL('../scripts/proof.mjs', import.meta.url));
const enginePath = process.env.SVG_STUDIO_MODULE;
const engine = enginePath ? await import(pathToFileURL(enginePath).href) : null;
const sharp = enginePath ? createRequire(pathToFileURL(enginePath))('sharp') : null;
const root = await mkdtemp(join(tmpdir(), 'visual-svg-pipeline-'));
const fixture = '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="32" viewBox="0 0 64 32"><path fill="#eeb640" d="M0 0H64V32H0Z"/></svg>';

async function expectFailure(args, modulePath, pattern) {
  const env = { ...process.env }; if (modulePath) env.SVG_STUDIO_MODULE = modulePath; else delete env.SVG_STUDIO_MODULE;
  await assert.rejects(run(process.execPath, args, { env }), error => pattern.test(String(error.stderr)));
}

test('the CLI asks for an engine rather than falling back to a personal path', async () => {
  await expectFailure([trace, 'source.png', join(root, 'missing.svg')], null, /Set SVG_STUDIO_MODULE/);
});

test('a monochrome-only engine cannot silently handle a colour request', async () => {
  const file = join(root, 'mono.mjs'); await writeFile(file, 'export const vectorizeImage = () => "mono";');
  await expectFailure([trace, 'source.png', join(root, 'mono.svg')], file, /multicolour SVG Studio/);
});

test('a bitmap wrapped in SVG is rejected as a vector deliverable', async () => {
  const file = join(root, 'bitmap.mjs');
  await writeFile(file, 'export const vectorizeMulticolourImage = async () => `<svg viewBox="0 0 4 4"><image href="data:image/png;base64,AA=="/></svg>`;');
  const output = join(root, 'bitmap.svg');
  await expectFailure([trace, 'source.png', output], file, /standalone vector paths/);
  await assert.rejects(access(output));
});

test('empty SVGs, live font labels and external references cannot pass as traced paths', async () => {
  const invalid = [
    '<svg viewBox="0 0 4 4"></svg>',
    fixture.replace('</svg>', '<text x="1" y="1">Unoutlined font</text></svg>'),
    fixture.replace('</svg>', '<image href = "https://example.invalid/art.png"/></svg>'),
    fixture.replace('0 0 64 32', '0 0 0 32'),
  ];
  for (const [index, svg] of invalid.entries()) {
    const file = join(root, `invalid-${index}.mjs`);
    await writeFile(file, `export const vectorizeMulticolourImage = async () => ${JSON.stringify(svg)};`);
    await expectFailure([trace, 'source.png', join(root, `invalid-${index}.svg`)], file, /standalone vector paths/);
  }
});

test('proofs preserve transparent letterboxing on both dark and light backgrounds', async () => {
  assert.ok(sharp, 'Set SVG_STUDIO_MODULE to run the actual engine proof tests.');
  const source = join(root, 'wide.png'), svg = join(root, 'wide.svg'), output = join(root, 'proof.png');
  await sharp(Buffer.from(fixture)).ensureAlpha().png().toFile(source); await writeFile(svg, fixture);
  await run(process.execPath, [proof, output, source, svg]);
  const stats = JSON.parse(await readFile(join(root, 'proof.json'), 'utf8'));
  assert.equal(stats.length, 8);
  for (const item of stats) {
    assert.ok(item.meanDifference < 0.01, JSON.stringify(item));
    assert.ok(item.foregroundMeanDifference < 0.02, JSON.stringify(item));
    const image = join(root, 'renders', `wide-${item.theme}-${item.size}-source.png`);
    const data = await sharp(image).removeAlpha().raw().toBuffer();
    const colour = item.theme === 'dark' ? [16, 21, 29] : [251, 251, 250];
    assert.deepEqual([...data.subarray(0, 3)], colour);
  }
});

test('the installed colour engine produces standalone paths that pass the proof pipeline', async () => {
  assert.equal(typeof engine?.vectorizeMulticolourImage, 'function');
  const source = join(root, 'colour.png'), output = join(root, 'colour.svg');
  const coloured = fixture.replace('</svg>', '<path fill="#e0642d" d="M0 0H32V32H0Z"/></svg>');
  await sharp(Buffer.from(coloured)).ensureAlpha().png().toFile(source);
  await run(process.execPath, [trace, source, output, '4']);
  const svg = await readFile(output, 'utf8');
  assert.match(svg, /viewBox="/); assert.match(svg, /<path /); assert.doesNotMatch(svg, /<(?:image|script|foreignObject)\b|href=|data:/i);
  assert.ok(new Set([...svg.matchAll(/fill="(#[a-f\d]{6})"/gi)].map(match => match[1])).size >= 2, 'Both source colours survive tracing.');
  const sourcePixels = await sharp(source).removeAlpha().raw().toBuffer();
  const vectorPixels = await sharp(Buffer.from(svg)).removeAlpha().raw().toBuffer();
  assert.equal(vectorPixels.length, sourcePixels.length);
  let difference = 0; for (let i=0;i<sourcePixels.length;i++) difference += Math.abs(sourcePixels[i]-vectorPixels[i]);
  assert.ok(difference / sourcePixels.length / 255 < 0.025);
});
