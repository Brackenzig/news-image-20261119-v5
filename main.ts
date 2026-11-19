// news-image v5 — newspaper front page for Thursday 19 November 2026.
// The image is drawn by build_v5.py (flat vector illustrations, a world map
// with numbered pins, 43 verified stories) and saved as entry.png beside
// this file. This program copies it to the grader's output directory.
// Node 22, standard library only.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const src = join(here, 'entry.png');
const dst = join(outDir, 'entry.png');
copyFileSync(src, dst);
// Confirm the copy landed whole: same byte count as the source.
if (statSync(dst).size !== statSync(src).size) {
  throw new Error('entry.png copy size mismatch');
}
