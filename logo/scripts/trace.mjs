import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';
import { pathToFileURL } from 'node:url';
import { assertVector } from './vector-contract.mjs';

const [input, output, coloursText = '24', ...flags] = process.argv.slice(2);
const colours = Number(coloursText);
if (!input || !output || !Number.isInteger(colours) || colours < 2 || colours > 64 || flags.some(f => f !== '--remove-background')) {
  throw new Error('Usage: node trace.mjs input.png output.svg [colours 2..64] [--remove-background]');
}
const modulePath = process.env.SVG_STUDIO_MODULE;
if (!modulePath) throw new Error('Set SVG_STUDIO_MODULE to SVG Studio’s built multicolour dist/vectorize.js module.');
const engine = await import(pathToFileURL(modulePath).href);
if (!engine.vectorizeMulticolourImage) throw new Error('Set SVG_STUDIO_MODULE to the built multicolour SVG Studio dist/vectorize.js module.');
const svg = await engine.vectorizeMulticolourImage(input, { colours, removeBackground: flags.includes('--remove-background') });
assertVector(svg);
await mkdir(dirname(output), { recursive: true });
await writeFile(output, svg);
console.log(`${output}: up to ${colours} palette colours, ${Buffer.byteLength(svg)} bytes`);
