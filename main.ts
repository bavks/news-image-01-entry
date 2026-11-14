// news-image-01 entry: writes the "world on Friday 13 November 2026" image
// to the output directory as entry.png.
// Node standard library only.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));

// Source image: entry.png beside this program; fall back to ./entry.png
// relative to the current working directory.
let source = resolve(here, "entry.png");
if (!existsSync(source)) {
  source = resolve(process.cwd(), "entry.png");
}
if (!existsSync(source)) {
  throw new Error(`entry.png not found (looked in ${here} and ${process.cwd()})`);
}

// Output directory: $MAKEFUN_OUTPUT_DIR resolved against the cwd when set,
// otherwise /output.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR
  ? resolve(process.cwd(), process.env.MAKEFUN_OUTPUT_DIR)
  : "/output";

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, resolve(outputDir, "entry.png"));
