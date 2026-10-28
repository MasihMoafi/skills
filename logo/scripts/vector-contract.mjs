// Check SVG Studio's output before saving or rendering it.
export function assertVector(svg) {
  const viewBox = svg.match(/\bviewBox\s*=\s*(["'])([^"']+)\1/)?.[2].trim().split(/[\s,]+/).map(Number);
  const hasPaths = /<path\b[^>]*\bd\s*=\s*(["'])[^"']+\1/i.test(svg);
  const forbidden = /<(?:image|script|foreignObject|text|style|use|animate\w*|set)\b|\bhref\s*=|\bon[a-z]+\s*=|data:|<!DOCTYPE|<!ENTITY|<\?xml-stylesheet|url\s*\(\s*(?!#[\w:.-]+\s*\))/i;
  if (!/^\s*(?:<\?xml[^?]*\?>\s*)?<svg\b/.test(svg) || !hasPaths || !viewBox || viewBox.length !== 4 || !viewBox.every(Number.isFinite) || viewBox[2] <= 0 || viewBox[3] <= 0 || forbidden.test(svg)) {
    throw new Error('Trace must have a positive viewBox and standalone vector paths, without rasters, scripts, fonts or external references.');
  }
}
