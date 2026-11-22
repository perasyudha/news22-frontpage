#!/usr/bin/env python3
"""Render entry.png: Sunday 22 November 2026, 1024x1024, 35 wire stories.

Everything is drawn here - no photographs, no network, no randomness.
Run:  python3 -P -s render.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 32
PAPER = (245, 240, 230)
INK = (20, 18, 14)
MUTED = (111, 106, 96)
RULE = (203, 194, 177)
LIGHT = (233, 225, 209)

REGIONS = [
    ("Americas", (178, 58, 47)),
    ("Europe", (46, 94, 140)),
    ("Mideast", (194, 131, 44)),
    ("Africa", (62, 122, 74)),
    ("Asia", (106, 75, 148)),
    ("Oceania", (44, 133, 133)),
    ("Global", (107, 103, 95)),
]
RCOL = dict(REGIONS)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/freefont",
]


def font_path(serif, bold):
    names = []
    if serif:
        names = ["DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf",
                 "LiberationSerif-Bold.ttf" if bold else "LiberationSerif-Regular.ttf"]
    else:
        names = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
                 "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"]
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None


_cache = {}


def F(size, serif=False, bold=False):
    key = (size, serif, bold)
    if key in _cache:
        return _cache[key]
    p = font_path(serif, bold)
    if p:
        f = ImageFont.truetype(p, size)
    else:
        f = ImageFont.load_default()
    _cache[key] = f
    return f


def tw(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, text, f, maxw, maxlines=99):
    """Wrap to width. Never drops a word; callers shrink the font instead."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, maxw, maxh, size, min_size, serif=False, bold=False, maxlines=99,
        lead=1.18):
    """Shrink until the whole wrapped block fits the box; returns (font, lines)."""
    s = size
    while s > min_size:
        f = F(s, serif, bold)
        lines = wrap(d, text, f, maxw, maxlines)
        if len(lines) <= maxlines and len(lines) * s * lead <= maxh:
            return f, lines
        s -= 1
    f = F(min_size, serif, bold)
    lines = wrap(d, text, f, maxw, maxlines)
    if len(lines) > maxlines:
        raise SystemExit("text does not fit: %r" % text)
    return f, lines


def text(d, xy, s, f, fill, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def spaced(d, xy, s, f, fill, track=1.6, anchor="la"):
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill, anchor=anchor)
        x += tw(d, ch, f) + track
    return x


def spaced_w(d, s, f, track=1.6):
    return sum(tw(d, ch, f) + track for ch in s) - track


# --------------------------------------------------------------------------
# stories
# --------------------------------------------------------------------------

CARDS = [
    dict(n=1, region="Europe", field="CLIMATE", place="Antalya, Turkey",
         head="COP31 draft drops the words 'fossil fuels'",
         deck="10-page text backs carbon removal; Panama vows to object",
         card="Turkey hosts COP31 in double overtime as the final text avoids naming coal, oil and gas.",
         lon=30.7, lat=36.9),
    dict(n=2, region="Europe", field="CONFLICT", place="Dymer, Ukraine",
         head="Drone collapses a Kyiv-region apartment block",
         deck="14 people may be trapped; nine evacuated, two hurt",
         card="Zelenskiy says part of a five-storey building came down after a night of drone and missile strikes.",
         lon=30.5, lat=50.5),
    dict(n=3, region="Africa", field="CONFLICT", place="Khartoum, Sudan",
         head="Drones hit Khartoum homes and UN premises",
         deck="Capital struck as Burhan vows to fight on in Blue Nile",
         card="Drone strikes damaged homes and United Nations premises in the Sudanese capital.",
         lon=32.5, lat=15.6),
    dict(n=4, region="Mideast", field="SECURITY", place="Makkah region, Saudi Arabia",
         head="Houthi missile intercepted over Saudi Arabia",
         deck="Coalition says it destroyed the missile; Makkah alert issued",
         card="Air defences destroyed a ballistic missile fired from Yemen towards western Saudi Arabia.",
         lon=39.8, lat=21.4),
    dict(n=5, region="Africa", field="DISASTER", place="Yenagoa, Nigeria",
         head="Funeral boat capsizes, killing 24 mourners",
         deck="Crowded vessel went down in the south; toll still rising",
         card="The boat was carrying passengers to a burial ceremony when it capsized on Friday; the toll rose on Sunday.",
         lon=6.3, lat=4.9),
    dict(n=6, region="Asia", field="INDUSTRY", place="Cikande, Indonesia",
         head="Java candy factory fire leaves 50 missing",
         deck="Seven body bags recovered; DNA sought from families",
         card="Rescuers searched for about 50 workers a day after the blaze at PT Fonusa Agung Mulia in Banten.",
         lon=106.2, lat=-6.1),
    dict(n=7, region="Global", field="SCIENCE", place="Mercury orbit",
         head="BepiColombo slips into Mercury orbit",
         deck="10 billion km over eight years for Europe and Japan",
         card="The ESA-JAXA pair looped into orbit around the smallest planet after a fly-by campaign.",
         lon=-150.0, lat=40.0, orbit=True),
    dict(n=8, region="Asia", field="EDUCATION", place="Seoul, South Korea",
         head="Education minister resigns over AI cheating",
         deck="Scandal erupted before the college entrance exam",
         card="Choi Kyo-jin quit on Sunday as the exam-fraud row widened ahead of the national college test.",
         lon=127.0, lat=37.5),
    dict(n=9, region="Americas", field="IMMIGRATION", place="Seattle, United States",
         head="Immigration arrests at Seattle airport delay a flight",
         deck="Agents held passengers at the gate; airline protests",
         card="Federal officers made arrests inside the terminal, holding up a departing flight on Sunday.",
         lon=-122.3, lat=47.6),
    dict(n=10, region="Oceania", field="DEFENCE", place="Canberra, Australia",
         head="Marles: US budget office 'wrong' on AUKUS",
         deck="A$368bn pact; CBO sees a smaller US attack fleet",
         card="The defence minister rejected a CBO finding that selling Virginia-class boats could shrink the US submarine force to 2060.",
         lon=149.1, lat=-35.3),
    dict(n=11, region="Oceania", field="CRICKET", place="Wellington, New Zealand",
         head="New Zealand 119-2 chasing India's record total",
         deck="Day four: Pant's century set India's highest score in NZ",
         card="Conway and Ravindra held out at the close after India built a mammoth first-innings lead.",
         lon=174.8, lat=-41.3),
]

BRIEFS = [
    (12, "Finland", "Sparta II still burning off Finland; 16 crew evacuated."),
    (13, "Pakistan", "Foreign minister hopeful on a US-Iran deal, warns against a long war."),
    (14, "Bahrain", "Two wounded in Iranian attacks; Pakistani resident critical."),
    (15, "Syria", "Authorities destroy 400 million Captagon pills in record haul."),
    (16, "Sudan", "Army rules out a ceasefire before Blue Nile is cleared."),
    (17, "DR Congo", "Ebola outbreak passes 11,000 cases and 5,500 deaths."),
    (18, "Congo", "Four-way Oyo summit: Tshisekedi, Ruto, Gnassingbe, Sassou-Nguesso."),
    (19, "Ghana", "Doctoral admissions frozen while training standards are audited."),
    (20, "Thailand", "Bangkok to block rare-earth chemicals bound for Myanmar."),
    (21, "North Korea", "Pyongyang marathon moved from April to October."),
    (22, "Bangladesh", "Deadly protests over exiled Hasina; PM Rahman blames India."),
    (23, "Pakistan", "Minister to visit India for SCO talks, first trip in three years."),
    (24, "India", "Nine of one family killed as car hits parked truck in Rajasthan."),
    (25, "Malaysia", "Sarawak polls: PDP to defend eight seats under GPS banner."),
    (26, "Thailand", "Arsenic in four northern rivers; boiling water 'unsafe'."),
    (27, "Gaza", "Health ministry warns of a rise in meningitis cases."),
    (28, "Israel", "Chikli defends post attacking bereaved MK Shira Shapira."),
    (29, "Canada", "Defence chief sees no change despite reported US curbs."),
    (30, "United States", "Incoming Senate Democrats test a leadership vote."),
    (31, "United States", "FBI investigates a hack of its criminal justice database."),
    (32, "Iran", "IRGC claims a 20th US drone downed, fourth in 24 hours."),
    (33, "Malaysia", "Sivasangari wins China Open after a walkover final."),
    (34, "Australia", "Hazlewood: never close to Khawaja, fine with his book."),
    (35, "United States", "Judge lets Delta 'window seat without a window' suit proceed."),
]

# brief -> region, used only for the region count in the masthead
BRIEF_REGION = {
    12: "Europe", 13: "Asia", 14: "Mideast", 15: "Mideast", 16: "Africa",
    17: "Africa", 18: "Africa", 19: "Africa", 20: "Asia", 21: "Asia",
    22: "Asia", 23: "Asia", 24: "Asia", 25: "Asia", 26: "Asia",
    27: "Mideast", 28: "Mideast", 29: "Americas", 30: "Americas",
    31: "Americas", 32: "Mideast", 33: "Asia", 34: "Oceania", 35: "Americas",
}

N_STORIES = len(CARDS) + len(BRIEFS)
REGION_COUNT = len(REGIONS)

# per-region tally, computed from the story list so the legend can never drift
COUNTS = {name: 0 for name, _ in REGIONS}
for _c in CARDS:
    COUNTS[_c["region"]] += 1
for _n, _p, _t in BRIEFS:
    COUNTS[BRIEF_REGION[_n]] += 1
assert sum(COUNTS.values()) == N_STORIES, COUNTS


# --------------------------------------------------------------------------
# illustrations (flat vector, drawn inside a panel)
# --------------------------------------------------------------------------

def illo(d, box, kind, col):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w / 2, y0 + h / 2
    dark = tuple(max(0, c - 30) for c in col)
    pale = tuple(min(255, int(c + (255 - c) * 0.62)) for c in col)

    d.rectangle(box, fill=pale)
    # horizon
    d.line([(x0, y1 - 6), (x1, y1 - 6)], fill=INK, width=2)

    if kind == 0:      # COP31 - warming globe over rising bars
        r = h * 0.30
        d.ellipse([x0 + 12, cy - r - 2, x0 + 12 + 2 * r, cy + r - 2], fill=col, outline=INK, width=2)
        d.arc([x0 + 12, cy - r - 2, x0 + 12 + 2 * r, cy + r - 2], 200, 340, fill=PAPER, width=2)
        for i, bh in enumerate((10, 15, 21, 27)):
            bx = x0 + w - 76 + i * 15
            d.rectangle([bx, y1 - 8 - bh, bx + 9, y1 - 8], fill=dark if i % 2 else col, outline=INK)

    elif kind == 1:    # Ukraine - damaged block, drone above
        bx = x0 + 14
        for i, hh in enumerate((26, 34, 30, 22)):
            top = y1 - 8 - hh
            d.rectangle([bx + i * 20, top, bx + i * 20 + 16, y1 - 8], fill=col, outline=INK, width=2)
            if i != 2:
                d.rectangle([bx + i * 20 + 4, top + 6, bx + i * 20 + 9, top + 12], fill=PAPER)
        d.polygon([(bx + 40, y1 - 8), (bx + 40, y1 - 26), (bx + 62, y1 - 8)], fill=PAPER)
        dx, dy = x1 - 58, y0 + 10
        d.polygon([(dx, dy + 8), (dx + 30, dy + 8), (dx + 15, dy)], fill=INK)
        d.line([(dx + 6, dy + 8), (dx + 2, dy + 18)], fill=INK, width=2)
        d.line([(dx + 24, dy + 8), (dx + 28, dy + 18)], fill=INK, width=2)

    elif kind == 2:    # Sudan - drone, smoke, UN flag
        for i, (px, hh) in enumerate(((0.24, 22), (0.44, 30), (0.62, 18))):
            left = x0 + w * px
            d.rectangle([left, y1 - 8 - hh, left + 26, y1 - 8], fill=col, outline=INK, width=2)
        sx = x0 + w * 0.62
        d.ellipse([sx - 6, y1 - 34, sx + 22, y1 - 14], fill=MUTED)
        d.ellipse([sx + 6, y1 - 42, sx + 24, y1 - 24], fill=MUTED)
        fx, fy = x1 - 34, y1 - 40
        d.line([(fx, fy), (fx, y1 - 8)], fill=INK, width=2)
        d.polygon([(fx, fy), (fx + 18, fy + 4), (fx, fy + 9)], fill=(60, 110, 170))
        px, py = x0 + w * 0.18, y0 + 8
        d.polygon([(px, py + 6), (px + 24, py + 6), (px + 12, py)], fill=INK)

    elif kind == 3:    # Saudi - missile arc, interceptor burst
        d.arc([x0 + 8, y0 + 4, x1 - 8, y1 + 26], 195, 330, fill=dark, width=2)
        mx, my = cx + 20, cy - 2
        d.polygon([(mx, my - 6), (mx + 14, my), (mx, my + 6), (mx - 8, my)], fill=INK)
        for a in range(0, 360, 45):
            import math
            r0, r1 = 8, 16
            ax = cx - 34 + math.cos(math.radians(a)) * r0
            ay = cy - 2 + math.sin(math.radians(a)) * r0
            bx2 = cx - 34 + math.cos(math.radians(a)) * r1
            by2 = cy - 2 + math.sin(math.radians(a)) * r1
            d.line([(ax, ay), (bx2, by2)], fill=col, width=3)
        d.ellipse([x0 + w - 52, y0 + 6, x0 + w - 16, y0 + 30], outline=INK, width=2)
        d.polygon([(x0 + w - 40, y0 + 10), (x0 + w - 34, y0 + 18), (x0 + w - 40, y0 + 26)], fill=INK)

    elif kind == 4:    # Nigeria - boat on water
        wy = y1 - 20
        d.rectangle([x0, wy, x1, y1 - 6], fill=dark)
        for k in range(3):
            yy = wy + 4 + k * 5
            pts = [(x0 + i, yy + (2 if (i // 8) % 2 else -2)) for i in range(x0, x1, 8)]
            if len(pts) > 1:
                d.line(pts, fill=PAPER, width=1)
        bx0, bx1 = cx - 46, cx + 46
        d.polygon([(bx0, wy - 4), (bx1, wy - 4), (bx1 - 14, wy + 6), (bx0 + 10, wy + 6)], fill=col, outline=INK, width=2)
        d.line([(cx, wy - 4), (cx, wy - 34)], fill=INK, width=2)
        d.polygon([(cx + 2, wy - 34), (cx + 30, wy - 12), (cx + 2, wy - 12)], fill=pale)
        d.ellipse([x1 - 30, y0 + 6, x1 - 12, y0 + 24], fill=PAPER)

    elif kind == 5:    # Indonesia - factory, flames, smoke
        d.rectangle([x0 + 10, y1 - 38, x0 + w - 40, y1 - 8], fill=col, outline=INK, width=2)
        for i in range(3):
            d.polygon([(x0 + 18 + i * 22, y1 - 38), (x0 + 30 + i * 22, y1 - 38),
                       (x0 + 24 + i * 22, y1 - 48)], fill=dark)
        d.rectangle([x0 + 20, y1 - 28, x0 + 34, y1 - 8], fill=INK)
        d.rectangle([x0 + 44, y1 - 28, x0 + 58, y1 - 8], fill=INK)
        fx = x1 - 34
        d.polygon([(fx - 12, y1 - 8), (fx + 12, y1 - 8), (fx + 4, y1 - 30), (fx - 4, y1 - 30)], fill=(214, 90, 40))
        d.polygon([(fx - 6, y1 - 8), (fx + 6, y1 - 8), (fx, y1 - 20)], fill=(240, 190, 70))
        for i in range(3):
            d.ellipse([x0 + w - 56 + i * 6, y0 + 2 + i * 5, x0 + w - 30 + i * 6, y0 + 16 + i * 5], fill=MUTED)

    elif kind == 6:    # Mercury - planet, orbiters, sun
        r = h * 0.26
        d.ellipse([cx - r - 6, cy - r - 2, cx + r + 6, cy + r - 2], fill=col, outline=INK, width=2)
        d.arc([cx - r - 18, cy - r + 4, cx + r + 18, cy + r - 8], 0, 360, fill=dark, width=1)
        d.ellipse([cx - r - 22, cy - 6, cx - r - 10, cy + 6], fill=INK)
        d.ellipse([cx + r + 10, cy - 8, cx + r + 22, cy + 4], fill=INK)
        for i in range(4):
            d.line([(x0 + 8 + i * 6, y0 + 4), (x0 + 14 + i * 6, y1 - 14)], fill=MUTED, width=1)

    elif kind == 7:    # Korea - exam sheet, AI chip, pencil
        d.rectangle([x0 + 12, y0 + 6, x0 + w * 0.46, y1 - 12], fill=PAPER, outline=INK, width=2)
        for i in range(4):
            d.line([(x0 + 18, y0 + 14 + i * 8), (x0 + w * 0.40, y0 + 14 + i * 8)], fill=MUTED, width=1)
        chx = x0 + w * 0.62
        d.rectangle([chx, cy - 16, chx + 32, cy + 16], fill=col, outline=INK, width=2)
        for i in range(3):
            d.line([(chx - 8, cy - 10 + i * 10), (chx, cy - 10 + i * 10)], fill=INK, width=2)
            d.line([(chx + 32, cy - 10 + i * 10), (chx + 40, cy - 10 + i * 10)], fill=INK, width=2)
        d.rectangle([chx + 10, cy - 6, chx + 22, cy + 6], fill=PAPER)

    elif kind == 8:    # Seattle - jet at gate, badge
        d.line([(x0 + 6, y1 - 22), (x1 - 6, y1 - 22)], fill=INK, width=2)
        for i in range(6):
            d.line([(x0 + 14 + i * 22, y1 - 22), (x0 + 20 + i * 22, y1 - 14)], fill=MUTED, width=1)
        px, py = cx - 34, cy - 4
        d.polygon([(px, py), (px + 58, py), (px + 68, py + 8), (px + 58, py + 16), (px, py + 16), (px - 6, py + 8)],
                  fill=PAPER, outline=INK, width=2)
        d.polygon([(px + 24, py + 16), (px + 34, py + 30), (px + 44, py + 30), (px + 40, py + 16)], fill=col, outline=INK)
        d.ellipse([x1 - 34, y0 + 6, x1 - 12, y0 + 28], outline=INK, width=2)
        d.rectangle([x1 - 27, y0 + 13, x1 - 19, y0 + 20], fill=col)

    elif kind == 9:    # AUKUS - submarine, sonar arcs
        d.rectangle([x0, y1 - 26, x1, y1 - 6], fill=dark)
        sx, sy = cx - 46, y1 - 20
        d.ellipse([sx, sy - 12, sx + 96, sy + 10], fill=col, outline=INK, width=2)
        d.polygon([(sx + 96, sy - 6), (sx + 96, sy + 8), (sx + 84, sy + 1)], fill=col)
        d.rectangle([sx + 40, sy - 22, sx + 56, sy - 10], fill=col, outline=INK, width=2)
        d.line([(sx + 48, sy - 22), (sx + 48, sy - 30)], fill=INK, width=2)
        for i, rr in enumerate((10, 18, 26)):
            d.arc([sx + 40 - rr, sy - rr - 26, sx + 40 + rr, sy - 26 + rr], 200, 340, fill=MUTED, width=1)

    elif kind == 10:   # cricket - stumps, ball, bat
        by = y1 - 8
        for i in range(3):
            x = x0 + 26 + i * 10
            d.rectangle([x, by - 40, x + 4, by], fill=INK)
        d.rectangle([x0 + 22, by - 44, x0 + 54, by - 40], fill=INK)
        d.ellipse([x0 + 66, by - 24, x0 + 78, by - 12], fill=(190, 60, 45), outline=INK)
        d.polygon([(cx + 26, y1 - 6), (cx + 34, y1 - 14), (cx + 62, cy - 16), (cx + 56, cy - 8)],
                  fill=(214, 188, 140), outline=INK)
        d.line([(cx + 58, cy - 14), (cx + 54, cy - 6)], fill=INK, width=2)

    d.rectangle(box, outline=INK, width=2)


# --------------------------------------------------------------------------
# map
# --------------------------------------------------------------------------

LAND = [
    # North America
    [(-168, 65), (-150, 70), (-125, 70), (-96, 72), (-80, 73), (-62, 60), (-55, 50),
     (-66, 45), (-70, 42), (-76, 35), (-81, 25), (-97, 26), (-105, 20), (-115, 30),
     (-125, 40), (-125, 49), (-135, 58), (-152, 60)],
    # Central America
    [(-105, 20), (-92, 16), (-83, 9), (-77, 8), (-84, 15), (-95, 18)],
    # Greenland
    [(-45, 83), (-22, 78), (-26, 70), (-45, 60), (-58, 68), (-56, 78)],
    # South America
    [(-81, 0), (-75, 10), (-60, 10), (-50, 0), (-35, -6), (-38, -22), (-48, -25),
     (-58, -35), (-62, -42), (-70, -52), (-75, -45), (-73, -30), (-70, -18), (-78, -5)],
    # Europe
    [(-10, 36), (0, 44), (4, 43), (12, 45), (20, 40), (28, 41), (30, 45), (40, 48),
     (30, 60), (26, 60), (30, 70), (10, 72), (5, 60), (8, 54), (-4, 50), (-9, 44)],
    # Africa
    [(-17, 15), (-17, 21), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (43, 12),
     (51, 12), (42, -2), (40, -15), (35, -25), (20, -35), (18, -30), (12, -18), (9, -1),
     (9, 4), (-8, 5), (-13, 9)],
    # Asia
    [(30, 45), (40, 42), (48, 40), (52, 30), (58, 25), (68, 24), (72, 20), (80, 10),
     (90, 22), (97, 16), (106, 10), (110, 20), (120, 31), (122, 40), (130, 43),
     (135, 50), (145, 60), (162, 62), (180, 66), (180, 71), (140, 75), (100, 78),
     (70, 72), (58, 70), (44, 67), (33, 66), (30, 58)],
    # India / peninsula
    [(68, 24), (72, 20), (77, 8), (80, 10), (88, 22), (92, 25), (80, 30), (70, 30)],
    # South-east Asia mainland
    [(97, 16), (100, 20), (106, 10), (109, 11), (105, 20), (99, 22)],
    # Indonesia
    [(95, 5), (105, -6), (116, -8), (130, -5), (141, -8), (136, 0), (120, 2), (110, 3), (100, 6)],
    # Australia
    [(114, -22), (122, -18), (130, -12), (142, -11), (146, -19), (153, -28), (150, -38),
     (140, -38), (130, -32), (115, -35)],
    # New Zealand
    [(166, -46), (174, -41), (178, -38), (172, -34), (168, -44)],
    # Japan
    [(130, 32), (141, 40), (145, 44), (141, 36), (135, 33)],
    # British Isles
    [(-6, 50), (-2, 58), (0, 54), (1, 51), (-5, 50)],
    # Antarctic rim (shown as a strip, not to scale)
    [(-180, -78), (-120, -74), (-60, -70), (0, -72), (60, -70), (120, -74), (180, -78),
     (180, -90), (-180, -90)],
]


def inside(poly, x, y):
    res = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xi:
                res = not res
    return res


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180) / 360 * (x1 - x0)
    y = y0 + (90 - lat) / 180 * (y1 - y0)
    return x, y


def draw_map(d, box, markers):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 232, 219), outline=RULE)
    pad = 12
    box = (x0 + pad, y0 + pad, x1 - pad, y1 - pad)
    step = 5
    for lat in range(-85, 90, step):
        for lon in range(-180, 180, step):
            if any(inside(poly, lon + step / 2, lat + step / 2) for poly in LAND):
                px, py = project(lon + step / 2, lat + step / 2, box)
                d.ellipse([px - 2.0, py - 2.0, px + 2.0, py + 2.0], fill=(178, 166, 143))
    # greedy de-collision: keep every marker number readable
    cands = [(0, 0), (0, -20), (-20, -6), (20, -6), (0, 20), (-15, -18), (15, -18),
             (-15, 18), (15, 18), (-26, 0), (26, 0), (0, -30), (0, 30)]
    placed = []
    r = 9
    for num, lon, lat, col, orbit in markers:
        bx, by = project(lon, lat, box)
        px, py = bx, by
        for dx, dy in cands:
            cx_, cy_ = bx + dx, by + dy
            if all((cx_ - qx) ** 2 + (cy_ - qy) ** 2 >= (2 * r + 6) ** 2 for qx, qy in placed):
                px, py = cx_, cy_
                break
        placed.append((px, py))
        px = min(max(px, box[0] + r + 1), box[2] - r - 1)
        py = min(max(py, box[1] + r + 1), box[3] - r - 1)
        if orbit:
            d.ellipse([px - r - 4, py - r - 4, px + r + 4, py + r + 4], outline=col, width=2)
        d.ellipse([px - r, py - r, px + r, py + r], fill=col, outline=INK, width=2)
        f = F(10.5, bold=True)
        d.text((px, py + 0.5), str(num), font=f, fill=PAPER, anchor="mm")


# --------------------------------------------------------------------------
# poster
# --------------------------------------------------------------------------

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead -------------------------------------------------------------
    f_lbl = F(12, bold=True)
    spaced(d, (M, 24), "THE DAY IN WORLD NEWS", f_lbl, INK, 2.2)
    right = "%d STORIES \u00b7 %d REGIONS \u00b7 ONE DAY" % (N_STORIES, REGION_COUNT)
    f_r = F(12, bold=True)
    d.text((W - M, 24), right, font=f_r, fill=INK, anchor="ra")
    d.line([(M, 48), (W - M, 48)], fill=INK, width=2)

    # dateline -------------------------------------------------------------
    dl = "Sunday 22 November 2026"
    size = 60
    while size > 30 and tw(d, dl, F(size, serif=True, bold=True)) > W - 2 * M:
        size -= 1
    f_dl = F(size, serif=True, bold=True)
    d.text((M, 56), dl, font=f_dl, fill=INK)
    dline_y = 56 + size + 6

    # deck -----------------------------------------------------------------
    f_deck = F(12)
    deck = ("COP31's draft that will not say fossil fuels, a drone that brought down a Kyiv-region "
            "apartment block, and a factory fire in Java with 50 workers missing")
    lines = wrap(d, deck, f_deck, W - 2 * M, 2)
    y = dline_y + 2
    for ln in lines:
        d.text((M, y), ln, font=f_deck, fill=MUTED)
        y += 15
    cards_top = y + 8
    d.line([(M, cards_top - 4), (W - M, cards_top - 4)], fill=RULE, width=1)

    # cards ----------------------------------------------------------------
    band_top = 578
    gap = 8
    rows = [(3, cards_top), (4, cards_top + 138), (4, cards_top + 274)]
    for ri, (ncols, ry) in enumerate(rows):
        cw = (W - 2 * M - (ncols - 1) * gap) / ncols
        ch = 132
        for ci in range(ncols):
            idx = (0, 3, 7)[ri] + ci
            if idx >= len(CARDS):
                break
            cx0 = M + ci * (cw + gap)
            card(d, (cx0, ry, cx0 + cw, ry + ch), CARDS[idx], ncols == 3)

    # bottom band ----------------------------------------------------------
    by0 = band_top
    by1 = H - 58
    d.line([(M, by0 - 6), (W - M, by0 - 6)], fill=INK, width=2)

    map_w = 484
    map_box = (M, by0 + 58, M + map_w, by1 - 46)
    f_h = F(11, bold=True)
    spaced(d, (M, by0 + 4), "WHERE IT HAPPENED", f_h, INK, 1.8)
    d.text((M + map_w, by0 + 4), "markers = cards 1-11 but 7 (orbital)", font=F(10.5), fill=MUTED, anchor="ra")

    # legend, two rows of swatches, each with its story count
    lx, ly = M, by0 + 24
    f_lg = F(10.5, bold=True)
    for i, (name, col) in enumerate(REGIONS):
        if i == 4:
            lx, ly = M, by0 + 40
        d.rectangle([lx, ly, lx + 9, ly + 9], fill=col, outline=INK)
        label = "%s %d" % (name.upper(), COUNTS[name])
        d.text((lx + 13, ly - 0.5), label, font=f_lg, fill=INK)
        lx += 13 + spaced_w(d, label, f_lg, 1.0) + 14

    markers = [(c["n"], c["lon"], c["lat"], RCOL[c["region"]], c.get("orbit", False))
               for c in CARDS if not c.get("orbit")]
    draw_map(d, map_box, markers)

    f_cap = F(11)
    cap1 = "Dots are land at 5 degrees. Markers are the eleven drawn cards, coloured by region;"
    cap2 = "briefs 12-35 are not plotted. Marker 7 rings an orbital event, not a country."
    yy = map_box[3] + 6
    for ln in (cap1, cap2):
        for sub in wrap(d, ln, f_cap, map_w, 2):
            d.text((M, yy), sub, font=f_cap, fill=MUTED)
            yy += 13

    # briefs rail
    bx = M + map_w + 20
    bw = W - M - bx
    d.text((bx, by0 + 4), "ALSO ON 22 NOVEMBER", font=f_h, fill=INK)
    d.line([(bx, by0 + 19), (W - M, by0 + 19)], fill=INK, width=1)
    colw = (bw - 10) / 2
    per_col = 12
    f_b = F(11)
    f_bn = F(10.5, bold=True)
    for i, (num, place, txt) in enumerate(BRIEFS):
        col = i // per_col
        row = i % per_col
        x = bx + col * (colw + 10)
        y = by0 + 25 + row * 29.2
        reg = BRIEF_REGION[num]
        numtxt = "%02d" % num
        d.text((x, y), numtxt, font=f_bn, fill=RCOL[reg])
        body = place.upper() + " " + txt
        lines = wrap(d, body, f_b, colw - 22, 2)
        yy = y
        for li, ln in enumerate(lines):
            if li == 0:
                d.text((x + 20, yy), ln, font=f_b, fill=INK)
            else:
                d.text((x + 20, yy), ln, font=f_b, fill=MUTED)
            yy += 12.4

    # footer ---------------------------------------------------------------
    d.line([(M, H - 46), (W - M, H - 46)], fill=INK, width=2)
    f_ft = F(11)
    foot = ("Every story was reported on Sunday 22 November 2026; disputed claims are attributed. "
            "Sources: Reuters, AP, AFP, Al Jazeera, Asharq Al-Awsat, Gulf News, PTI, Dawn. Original drawings.")
    yy = H - 40
    for ln in wrap(d, foot, f_ft, W - 2 * M, 2):
        d.text((M, yy), ln, font=f_ft, fill=INK)
        yy += 13

    return img


def card(d, box, c, wide):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    box = (x0, y0, x1, y1)
    w = x1 - x0
    h = y1 - y0
    col = RCOL[c["region"]]
    d.rectangle(box, fill=(252, 249, 242), outline=RULE)

    illo_h = 46 if wide else 44
    kinds = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}
    illo(d, (x0, y0, x1, y0 + illo_h), kinds[c["n"]], col)

    # badge + kicker
    by = y0 + illo_h + 7
    r = 9
    d.ellipse([x0 + 7, by - 1, x0 + 7 + 2 * r, by - 1 + 2 * r], fill=col, outline=INK)
    d.text((x0 + 7 + r, by - 1 + r), str(c["n"]), font=F(10.5, bold=True), fill=PAPER, anchor="mm")

    kicker = (c["region"] + " \u00b7 " + c["field"]).upper()
    fk = F(9.5, bold=True)
    kx = x0 + 27
    maxk = w - 32
    ktrack = 1.2
    while spaced_w(d, kicker, fk, ktrack) > maxk and ktrack > 0.2:
        ktrack -= 0.2
    spaced(d, (kx, by + 1), kicker, fk, MUTED, ktrack)

    # headline
    hy = by + 15
    hsize, hmin, hmax = (16, 13, 2) if wide else (14, 11, 3)
    hf, hlines = fit(d, c["head"], w - 12, y1 - hy - 26, hsize, hmin,
                     serif=True, bold=True, maxlines=hmax, lead=1.14)
    yy = hy
    for ln in hlines:
        d.text((x0 + 6, yy), ln, font=hf, fill=INK)
        yy += hf.size * 1.14

    # deck
    df, dlines = fit(d, c["deck"], w - 12, y1 - yy - 3, 11.5, 11, maxlines=2, lead=1.14)
    for ln in dlines:
        d.text((x0 + 6, yy), ln, font=df, fill=MUTED)
        yy += df.size * 1.14
    if yy > y1 - 1:
        raise SystemExit("card %d text overflows: %.1f > %d" % (c["n"], yy, y1 - 1))


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
