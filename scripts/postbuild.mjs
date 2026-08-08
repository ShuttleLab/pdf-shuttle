// Remove legacy flat <route>.html files emitted next to the trailing-slash
// <route>/index.html outputs (see next.config.ts trailingSlash: true). Keeping
// both would let hosts serve /en and /en/ as two separate 200 pages, which
// splits canonical signals. After cleanup only directory paths remain, so the
// slashless variant gets redirected (308) to the canonical slash URL.
import { readdir, rm, stat } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = fileURLToPath(new URL('../out/', import.meta.url));
const KEEP_BASENAMES = new Set(['index.html', '404.html']);
// Directories copied verbatim from public/ that legitimately contain flat
// .html files referenced by iframes (PDF.js viewers).
const SKIP_DIRS = new Set(['_next', 'pdfjs-viewer', 'pdfjs-annotation-viewer']);

async function walk(dir) {
  let entries;
  try {
    entries = await readdir(dir);
  } catch {
    return;
  }
  for (const name of entries) {
    if (SKIP_DIRS.has(name)) continue;
    const full = join(dir, name);
    let isFile;
    try {
      isFile = (await stat(full)).isFile();
    } catch {
      continue;
    }
    if (!isFile) {
      await walk(full);
      continue;
    }
    if (name.endsWith('.html') && !KEEP_BASENAMES.has(name)) {
      await rm(full);
      console.log('removed', full.replace(outDir, ''));
    }
  }
}

await walk(outDir);