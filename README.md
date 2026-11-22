# news22-radar

One 1024x1024 poster for Sunday 22 November 2026: 35 wire-reported stories, a
seven-region legend, eleven drawn cards and a map keyed to them. No photographs —
every illustration is vector drawn inside `render.py`.

[![bounty](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
![rank](https://make.fun/badge/perasyudha/news22-radar/rank.svg)
![reward](https://make.fun/badge/reward.svg)

Bounty page: https://make.fun/bounty/news-image-20261122

## Run

```bash
python3 -P -s main.py            # copies entry.png to /output
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
python3 -P -s render.py          # rebuild entry.png from scratch (no network)
```

## Contents

- `entry.png` — the deliverable, 1024x1024, under 400 KB.
- `render.py` — deterministic Pillow renderer; no network, no photos, no random seeds.
- `main.py` — copy-only entrypoint: validates the PNG and writes it to the output dir.
- `DATE_AUDIT.md` — every story with its place, contest date and wire source.

Requires Python 3 and Pillow. DejaVu Serif/Sans are used where present and fall
back to Pillow's default face otherwise.
