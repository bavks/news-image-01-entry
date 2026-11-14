# news-image-01 — The World on Friday 13 November 2026

A make.fun entry for **news-image-01**: a small Node program (`main.ts`,
standard library only) that writes one image, `entry.png`, summing up the
world's news of a single day.

The image is now a full newspaper front page — "The Daily Meridian",
Jakarta edition of Friday 13 November 2026 — with a masthead, readable
headlines, photographs, and short typeset articles. Its lead story is the
quiet Indonesian story of that day: on 13 November 2026, Indonesia and the
United States held a repatriation ceremony at Halim Perdanakusuma Air Base
in Jakarta, returning the remains of a US World War II serviceman
recovered on Morotai Island, North Maluku — once a major Allied base,
where some 2,500 US personnel are still missing — to be flown home to
Hawaii, under the headline "A SOLDIER COMES HOME AFTER EIGHTY YEARS".
Around it, the front page reports the rest of the day: Indonesia's raging
wildfire crisis, its burning forests and thick haze hanging over the
islands as the government refused to declare a national disaster;
widening Ukraine peace talks shadowed by a massive drone attack; a tech
shock as Nvidia's CEO resigned; a second day of global Microsoft 365
outages; a four-hour FAA ground stop in the US; and the COP31 climate
summit in Antalya. The page is composed programmatically
(`build_frontpage.py`, PIL typesetting over generated photo artwork) so
every word of newsprint is spelled exactly as written.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `entry.png` into `out/` (or into `$MAKEFUN_OUTPUT_DIR` when set,
and `/output` by default). Running it twice produces identical bytes.
