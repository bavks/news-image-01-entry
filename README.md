# news-image-01 — The World on Friday 13 November 2026

A make.fun entry for **news-image-01**: a small Node program (`main.ts`,
standard library only) that writes one image, `entry.png`, summing up the
world's news of a single day.

The image sums up Friday 13 November 2026 — a day of widening Ukraine peace
talks shadowed by a massive drone attack, a tech shock as Nvidia's CEO
resigned, a second day of global Microsoft 365 outages, US–Iran drone
tensions over Bahrain, a four-hour FAA ground stop in the US, the COP31
climate summit in Antalya, and Taiwan's warning over China's Pacific naval
drills — and, featured largest of all, Indonesia's raging wildfire crisis,
its burning forests and thick haze hanging over Jakarta as the government
refused to declare a national disaster — arranged as an editorial newspaper
collage around a glowing Earth under the banner "FRIDAY 13 NOVEMBER 2026".

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `entry.png` into `out/` (or into `$MAKEFUN_OUTPUT_DIR` when set,
and `/output` by default). Running it twice produces identical bytes.
