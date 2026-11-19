#!/usr/bin/env python3
"""news-image v5 — newspaper front page, drawn from scratch with PIL.
Fresh code written in-session. Method studied from the live top-10 winners
(cream newspaper front page: serif date headline, data strip, 3 illustrated
leads, 10 illustrated grid stories, world map with pins, text list of the
remaining stories, DATE CHECK box, sources footer). All 43 stories are
verified 19 Nov 2026 news; the DATE CHECK lists only items NOT in the 43.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- colours ----
PAPER   = (246, 241, 227)   # cream
INK     = (26, 26, 26)      # near-black
RED     = (178, 28, 28)     # dark red (sub-headline, labels, numbers)
RED_DK  = (150, 20, 20)
NAVY    = (22, 35, 63)      # map background
BEIGE   = (217, 201, 163)   # map continents
GREY    = (90, 90, 90)
RULE    = (60, 60, 60)
# region bar colours (winners' palette)
REG_COL = {
    "EUROPE":       (43, 90, 166),
    "THE AMERICAS": (46, 125, 50),
    "ASIA-PACIFIC": (198, 40, 40),
    "MIDEAST":      (141, 110, 99),
    "AFRICA":       (239, 108, 0),
    "OCEANIA":      (0, 131, 143),
    "WORLD":        (97, 97, 97),
}

FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"

def serif(size, bold=False, italic=False):
    if italic and bold:
        p = FN + "NotoSerif-BoldItalic.ttf"
    elif italic:
        p = FN + "NotoSerif-Italic.ttf"
    elif bold:
        p = FN + "NotoSerif-Bold.ttf"
    else:
        p = FN + "NotoSerif-Regular.ttf"
    return ImageFont.truetype(p, size)

def sans(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

# ---- text helpers ----
def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, font, fill, max_w, leading=None, align="left"):
    """Draw wrapped text; returns y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.18)
    for ln in wrap(draw, text, font, max_w):
        if align == "center":
            lx = x + (max_w - draw.textlength(ln, font=font)) // 2
        else:
            lx = x
        draw.text((lx, y), ln, font=font, fill=fill)
        y += leading
    return y

def text_h(draw, text, font, max_w, leading=None):
    """Height of wrapped text."""
    if leading is None:
        leading = int(font.size * 1.18)
    return len(wrap(draw, text, font, max_w)) * leading

# ---- the 43 stories (verified 19 Nov 2026) ----
# region: EUROPE / THE AMERICAS / ASIA-PACIFIC / MIDEAST / AFRICA / OCEANIA / WORLD
# pin: (lon, lat) for the 13 illustrated stories (map pins 1-13)
LEADS = [
    dict(n=1, place="SHENZHEN", topic="SUMMIT", region="ASIA-PACIFIC",
         headline="Trump, Xi and Putin hold first three-way summit",
         sub="The three nuclear powers meet at APEC in Shenzhen; arms control and the Iran war top the agenda.",
         pin=(114.0, 22.5), art="summit"),
    dict(n=2, place="NEW YORK", topic="GAMES", region="WORLD",
         headline="GTA VI arrives after a 13-year wait",
         sub="Unlocks at midnight in each country. New Zealand first; 15.9m pre-orders banked.",
         pin=(-74.0, 40.7), art="gta"),
    dict(n=3, place="NASDAQ", topic="MARKETS", region="THE AMERICAS",
         headline="Anthropic debuts in the biggest IPO on record",
         sub="Priced at $83, above its range, the Claude maker raised $81.3bn and is valued near $1.5tn.",
         pin=(-122.4, 37.8), art="ipo"),
]

GRID = [
    dict(n=4, place="THE HAGUE", topic="LAW", region="EUROPE",
         headline="World Court rules on Myanmar's Rohingya case",
         sub="The ICJ rules in The Gambia's case over the 2017 campaign.",
         pin=(4.3, 52.1), art="court"),
    dict(n=5, place="ANTALYA", topic="CLIMATE", region="ASIA-PACIFIC",
         headline="COP31 enters its final 48 hours",
         sub="Ministers take over the text; 'phase out' and a $120bn fund still open.",
         pin=(30.7, 36.9), art="climate"),
    dict(n=6, place="CRIMEA", topic="WAR", region="EUROPE",
         headline="Crimean Bridge hit again",
         sub="Third attack halts traffic; the crossing is closed.",
         pin=(34.5, 45.3), art="bridge"),
    dict(n=7, place="ODISHA", topic="STORM", region="ASIA-PACIFIC",
         headline="Akvan bears down as 200,000 flee the coast",
         sub="Red alerts in 11 districts; landfall near Puri due Friday.",
         pin=(85.8, 20.3), art="storm"),
    dict(n=8, place="KYIV", topic="WAR", region="EUROPE",
         headline="Left off the agenda, Ukraine watches Shenzhen",
         sub="The war is off the summit agenda; Kyiv fears being carved up.",
         pin=(30.5, 50.5), art="kyiv"),
    dict(n=9, place="BRUSSELS", topic="TRADE", region="ASIA-PACIFIC",
         headline="EU approves Indonesia trade pact",
         sub="The deal opens digital trade; Jakarta calls it a milestone.",
         pin=(106.8, -6.2), art="trade"),
    dict(n=10, place="CANBERRA", topic="ECONOMY", region="OCEANIA",
         headline="Aussie jobless hits a five-year high",
         sub="Unemployment at 4.9%, the highest since October 2021.",
         pin=(149.1, -35.3), art="jobs"),
    dict(n=11, place="PARIS", topic="POLITICS", region="EUROPE",
         headline="France protests hit a fourth week",
         sub="Strikes and marches continue; the government holds its line.",
         pin=(2.3, 48.9), art="protest"),
    dict(n=12, place="ISTANBUL", topic="WEATHER", region="ASIA-PACIFIC",
         headline="Istanbul floods kill three",
         sub="Streets turn to rivers; rescue workers wade past submerged cars.",
         pin=(29.0, 41.0), art="flood"),
    dict(n=13, place="BENGHAZI", topic="CRIME", region="AFRICA",
         headline="Libya seizes a mountain of pills",
         sub="Officials display one of the country's biggest drug hauls.",
         pin=(20.1, 32.1), art="haul"),
]

# remaining 30 as one-line briefs: (place, text) — #14 to #43
# kept short (<= ~50 chars) so each fits on one line at 10px
BRIEFS = [
    ("WASHINGTON", "Jeffries nominated Speaker."),
    ("CARACAS", "US and Venezuela restore ties."),
    ("OTTAWA", "Canada sanctions West Bank settlers."),
    ("TOKYO", "India and Japan review defence ties."),
    ("JERUSALEM", "Eisenkot tapped to form a government."),
    ("MANILA", "US and Philippines sign a $2bn deal."),
    ("WASHINGTON", "US sanctions a Hezbollah network."),
    ("WASHINGTON", "Russian charged in a US spy case."),
    ("GAZA", "Allies urge aid access; crossings shut."),
    ("GAZA", "Israel pushes past the line; Hamas objects."),
    ("PYONGYANG", "North Korea expands uranium enrichment."),
    ("NEW YORK", "Van Gogh sells for $190m at auction."),
    ("SANTA CLARA", "Nvidia chief promises pay rises."),
    ("SEATTLE", "Microsoft and ByteDance open AI talks."),
    ("NEW DELHI", "Apple Maps upgrade rolls out in India."),
    ("KUALA LUMPUR", "Malaysia's GDP grows 5.5%."),
    ("LONDON", "UK cyber reports near a record."),
    ("WASHINGTON", "FBI warns of a new AI hacking tool."),
    ("BRUSSELS", "EU states propose a Rwanda asylum plan."),
    ("RIYADH", "Oil prices fall as supplies improve."),
    ("PHOENIX", "Waymo pulls driverless cars after a crash."),
    ("SPACE", "Two stars merge in Andromeda."),
    ("SPACE", "Twin black holes found circling each other."),
    ("WASHINGTON", "Pew: Islam to top world faiths by 2035."),
    ("BRUSSELS", "EU plans a \u20ac45bn loan for Ukraine."),
    ("NASHVILLE", "Swift steals the CMA Awards."),
    ("NEW DELHI", "Sindhu back in the top five."),
    ("S\u00c3O PAULO", "Corinthians thrash Botafogo 4-0."),
    ("TALLINN", "Estonia to shut its Russia border."),
    ("NEW DELHI", "Delhi schools reopen as the air clears."),
]

REGIONS = ["EUROPE", "THE AMERICAS", "ASIA-PACIFIC", "MIDEAST", "AFRICA", "OCEANIA", "WORLD"]

def region_counts():
    counts = {r: 0 for r in REGIONS}
    for s in LEADS + GRID:
        counts[s["region"]] += 1
    # briefs' regions, in #14-43 order
    brief_regions = [
        "THE AMERICAS", "THE AMERICAS", "THE AMERICAS", "ASIA-PACIFIC",
        "MIDEAST", "ASIA-PACIFIC", "MIDEAST", "THE AMERICAS",
        "MIDEAST", "MIDEAST", "ASIA-PACIFIC", "THE AMERICAS",
        "THE AMERICAS", "THE AMERICAS", "ASIA-PACIFIC", "ASIA-PACIFIC",
        "EUROPE", "THE AMERICAS", "EUROPE", "MIDEAST",
        "THE AMERICAS", "WORLD", "WORLD", "WORLD",
        "EUROPE", "THE AMERICAS", "ASIA-PACIFIC", "THE AMERICAS",
        "EUROPE", "ASIA-PACIFIC",
    ]
    assert len(brief_regions) == 30
    for r in brief_regions:
        counts[r] += 1
    return counts

BIG_NUMBERS = [
    ("$81.3bn", "raised by Anthropic — the largest IPO on record"),
    ("15.9m", "GTA VI pre-orders banked before release day"),
    ("200,000", "evacuated ahead of Cyclone Akvan"),
    ("730,000", "Rohingya who fled in 2017 — the ICJ case"),
    ("$120bn", "adaptation-finance goal still open at COP31"),
    ("5.5%", "Malaysia's GDP growth"),
]

DATE_CHECK = ("DATE CHECK — FIRST REPORTED WEDNESDAY 18 NOV, SO NOT ON THIS PAGE AS NEWS: "
    "the Iranian drone interceptions · Voyager 1 crossing one light-day, at 10:16 GMT Wednesday · "
    "the first COP31 draft (Monday) · Petrola's Alaska win · Anthropic's $83 IPO price.")

FOOTER = ("Every story here happened, or was first reported, on Thursday 19 November 2026. "
    "Disputed claims are attributed, not stated as fact. Sources: Reuters, AP, AFP, BBC, "
    "The Hindu, IMD, NASA, ICJ, Pew. Original drawings. The World in One Day — 19 November 2026.")

# ---- flat illustrations (drawn programmatically, winners' flat style) ----
# Each takes (draw, x, y, w, h) and draws into that box.

def ill_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 212, 220))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(120, 130, 140))
    # skyline
    for bx, bw, bh in [(8, 34, 52), (48, 26, 68), (80, 40, 44), (126, 30, 60),
                       (162, 36, 48), (204, 28, 66), (238, 34, 40), (278, 30, 56)]:
        d.rectangle([x + bx, y + h - 18 - bh, x + bx + bw, y + h - 18], fill=(52, 68, 84))
    # three flags on poles
    for fx, cols in [(30, [(178, 34, 34), (255, 255, 255), (178, 34, 34)]),
                     (150, [(222, 0, 0)]),
                     (262, [(255, 255, 255), (0, 57, 166), (213, 0, 50)])]:
        d.line([x + fx, y + 8, x + fx, y + 42], fill=(40, 40, 40), width=2)
        fh = 16
        for i, c in enumerate(cols):
            d.rectangle([x + fx, y + 8 + i * (fh // len(cols)),
                         x + fx + 26, y + 8 + (i + 1) * (fh // len(cols))], fill=c)
        d.rectangle([x + fx, y + 8, x + fx + 26, y + 8 + fh], outline=(40, 40, 40), width=1)

def ill_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(59, 42, 94))
    d.ellipse([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + 60], fill=(255, 166, 0))
    for bx, bw, bh in [(0, 44, 58), (50, 36, 74), (92, 42, 50), (140, 38, 66),
                       (184, 44, 54), (234, 40, 72), (280, 42, 60)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(20, 12, 40))
        for wy in range(y + h - bh + 8, y + h - 6, 14):
            for wx in range(x + bx + 6, x + bx + bw - 4, 12):
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 220, 100))
    d.text((x + 8, y + h - 16), "VICE CITY", font=sans(11, True), fill=(255, 255, 255))

def ill_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(11, 61, 46))
    # candlesticks
    pts = [(14, 58), (44, 50), (74, 54), (104, 40), (134, 44), (164, 30),
           (194, 34), (224, 20), (254, 24), (284, 10)]
    for i, (px, py) in enumerate(pts):
        c = (46, 204, 113) if i % 2 == 0 else (231, 76, 60)
        d.rectangle([x + px - 4, y + py - 6, x + px + 4, y + py + 6], fill=c)
        d.line([x + px, y + py - 12, x + px, y + py + 12], fill=c, width=2)
    d.line([(x + px, y + py) for px, py in pts], fill=(255, 214, 64), width=3)
    d.text((x + 8, y + 6), "ANT", font=sans(16, True), fill=(255, 255, 255))
    d.text((x + w - 52, y + 6), "$83", font=sans(16, True), fill=(255, 214, 64))

def ill_climate(d, x, y, w, h):
    # sky over a green field; globe left, thermometer right, sun top-right
    d.rectangle([x, y, x + w, y + h], fill=(186, 218, 232))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 170, 90))
    # sun
    sx, sy = x + w - 30, y + 9
    d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(255, 200, 40))
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([sx + dx * 8, sy + dy * 8, sx + dx * 12, sy + dy * 12],
               fill=(255, 200, 40), width=2)
    # globe: blue ocean, green land blobs kept well inside the circle
    gx, gy, gr = x + 42, y + h // 2 + 2, 15
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 140, 200))
    d.ellipse([gx - 10, gy - 9, gx - 1, gy - 1], fill=(60, 160, 90))
    d.ellipse([gx + 1, gy + 1, gx + 10, gy + 9], fill=(60, 160, 90))
    d.ellipse([gx - 4, gy + 4, gx + 4, gy + 10], fill=(90, 180, 110))
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(40, 90, 140), width=2)
    # thermometer: white tube, red fill, round bulb
    tx = x + w // 2 + 22
    d.rounded_rectangle([tx, y + 6, tx + 9, y + h - 14], radius=4, fill=(245, 245, 240))
    d.rectangle([tx + 2, y + 14, tx + 7, y + h - 16], fill=(198, 40, 40))
    d.ellipse([tx - 3, y + h - 20, tx + 12, y + h - 5], fill=(198, 40, 40))

def ill_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    cx = x + w // 2
    d.polygon([(cx - 62, y + 22), (cx + 62, y + 22), (cx, y + 4)], fill=(240, 240, 235))
    d.rectangle([x + 18, y + 22, x + w - 18, y + 27], fill=(240, 240, 235))
    for i in range(4):
        colx = x + 30 + i * 38
        d.rectangle([colx, y + 27, colx + 12, y + h - 12], fill=(245, 245, 240))
    d.rectangle([x + 18, y + h - 12, x + w - 18, y + h - 6], fill=(220, 220, 214))

def ill_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(184, 196, 204))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(90, 120, 150))
    # pylons + cables + deck
    for px in (x + 40, x + w - 48):
        d.rectangle([px, y + 12, px + 6, y + h - 22], fill=(60, 70, 80))
    d.line([x + 4, y + h - 26, x + w - 4, y + h - 26], fill=(60, 70, 80), width=4)
    d.line([x + 43, y + 12, x + w // 2, y + h - 26], fill=(120, 130, 140), width=2)
    d.line([x + w - 45, y + 12, x + w // 2, y + h - 26], fill=(120, 130, 140), width=2)
    # smoke column (light grey puffs, rising from the deck)
    for i, r in enumerate([9, 7, 6, 5]):
        d.ellipse([x + w // 2 - r + 24, y + 6 + i * 8, x + w // 2 + r + 24, y + 6 + i * 8 + r * 2],
                  fill=(150, 150, 150))

def ill_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(207, 224, 234))
    cx, cy = x + w // 2, y + h // 2 - 4
    for r in (34, 26, 18, 10):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(120, 140, 160))
    for rx in range(6, w - 6, 18):
        d.line([x + rx, y + h - 16, x + rx - 5, y + h - 6], fill=(100, 140, 180), width=2)

def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 2], fill=(0, 91, 187))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(255, 213, 0))
    for bx, bw, bh in [(6, 30, 26), (42, 24, 36), (72, 34, 22), (112, 28, 32),
                       (146, 32, 24), (184, 26, 34)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(30, 40, 60))

def ill_trade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 228, 232))
    cols = [(198, 60, 50), (40, 90, 160), (60, 140, 70), (230, 140, 40), (120, 80, 160)]
    for i in range(5):
        cx = x + 6 + i * 36
        d.rectangle([cx, y + h - 34, cx + 32, y + h - 18], fill=cols[i])
        d.rectangle([cx, y + h - 52, cx + 32, y + h - 36], fill=cols[(i + 2) % 5])
    d.line([x + 8, y + 6, x + w - 8, y + 6], fill=(60, 70, 80), width=4)
    d.line([x + 20, y + 6, x + 20, y + h - 52], fill=(60, 70, 80), width=3)
    d.line([x + w - 24, y + 6, x + w - 24, y + h - 52], fill=(60, 70, 80), width=3)

def ill_jobs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    base = y + h - 10
    bars = [46, 38, 30, 22]
    for i, bh in enumerate(bars):
        bx = x + 18 + i * 44
        d.rectangle([bx, base - bh, bx + 28, base], fill=(198, 40, 40))
    d.line([(x + 14, base - 50), (x + w - 14, base - 18)], fill=(178, 28, 28), width=4)
    d.polygon([(x + w - 14, base - 18), (x + w - 30, base - 24), (x + w - 22, base - 8)],
              fill=(178, 28, 28))

def ill_badminton(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 228, 190))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 170, 100))
    d.line([x + 8, y + h // 2, x + w - 8, y + h // 2], fill=(255, 255, 255), width=3)
    for gx in range(14, w - 8, 16):
        d.line([x + gx, y + h // 2 - 8, x + gx, y + h // 2 + 8], fill=(255, 255, 255), width=1)
    # shuttlecock
    d.polygon([(x + w - 52, y + 12), (x + w - 40, y + 12), (x + w - 46, y + 28)], fill=(255, 255, 255))
    d.ellipse([x + w - 50, y + 26, x + w - 42, y + 34], fill=(255, 255, 255))
    # racket (oval with string cross-hatch) + shuttlecock
    d.ellipse([x + 18, y + 8, x + 46, y + 34], outline=(60, 60, 60), width=3)
    for sx in (24, 30, 36, 42):
        d.line([x + sx, y + 11, x + sx, y + 31], fill=(120, 120, 120), width=1)
    for sy2 in (15, 21, 27):
        d.line([x + 21, y + sy2, x + 43, y + sy2], fill=(120, 120, 120), width=1)
    d.line([x + 32, y + 32, x + 46, y + 52], fill=(60, 60, 60), width=3)

def ill_protest(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 210))
    for i, (hx, c) in enumerate([(16, (198, 60, 50)), (44, (40, 90, 160)), (72, (60, 140, 70)),
                                 (100, (230, 140, 40)), (128, (120, 80, 160)), (156, (198, 60, 50))]):
        d.ellipse([x + hx, y + h - 34, x + hx + 16, y + h - 18], fill=(240, 200, 170))
        d.rectangle([x + hx - 2, y + h - 18, x + hx + 18, y + h - 4], fill=c)
    d.rectangle([x + 20, y + 6, x + 78, y + 20], fill=(255, 255, 255))
    d.rectangle([x + 20, y + 6, x + 78, y + 20], outline=(178, 28, 28), width=2)
    d.line([x + 24, y + 20, x + 24, y + h - 34], fill=(60, 60, 60), width=2)
    d.line([x + 74, y + 20, x + 74, y + h - 34], fill=(60, 60, 60), width=2)

def ill_flood(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 195, 205))
    for rx in range(8, w - 4, 16):
        d.line([x + rx, y + 4, x + rx - 4, y + 16], fill=(140, 160, 175), width=2)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 110, 150))
    for wy in (y + h - 20, y + h - 12):
        for wx in range(4, w - 10, 22):
            d.arc([x + wx, wy, x + wx + 18, wy + 8], 200, 340, fill=(200, 225, 240), width=2)
    # submerged car
    d.rectangle([x + w // 2 - 34, y + h - 34, x + w // 2 + 34, y + h - 22], fill=(178, 60, 50))
    d.rectangle([x + w // 2 - 22, y + h - 44, x + w // 2 + 18, y + h - 34], fill=(150, 45, 40))

def ill_haul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 222, 205))
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 8], fill=(120, 95, 70))
    for i in range(3):
        d.rectangle([x + 18 + i * 52, y + h - 40, x + 18 + i * 52 + 44, y + h - 16],
                    fill=(245, 240, 225), outline=(150, 140, 120), width=2)
        d.line([x + 18 + i * 52, y + h - 28, x + 18 + i * 52 + 44, y + h - 28],
               fill=(150, 140, 120), width=2)
    d.rectangle([x + 44, y + h - 62, x + 44 + 44, y + h - 42], fill=(245, 240, 225),
                outline=(150, 140, 120), width=2)
    # police star
    cx, cy = x + w - 26, y + 16
    d.polygon([(cx, cy - 10), (cx + 3, cy - 3), (cx + 10, cy - 3), (cx + 5, cy + 2),
               (cx + 7, cy + 9), (cx, cy + 5), (cx - 7, cy + 9), (cx - 5, cy + 2),
               (cx - 10, cy - 3), (cx - 3, cy - 3)], fill=(255, 200, 0))

ILL = {"summit": ill_summit, "gta": ill_gta, "ipo": ill_ipo, "court": ill_court,
       "bridge": ill_bridge, "climate": ill_climate, "storm": ill_storm, "kyiv": ill_kyiv, "trade": ill_trade,
       "jobs": ill_jobs, "badminton": ill_badminton, "protest": ill_protest,
       "flood": ill_flood, "haul": ill_haul}

# ---- world map ----
# Coarse continent polygons in (lon, lat); projected equirectangular into the
# map box so the numbered pins sit on the right landmass.
CONTINENTS_LL = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 70), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 20), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58)],
    # Greenland
    [(-58, 64), (-45, 60), (-40, 65), (-55, 76), (-68, 76), (-68, 70)],
    # South America
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -20),
     (-77, -12)],
    # Africa
    [(-18, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, -2), (40, -10), (35, -20), (32, -29),
     (20, -35), (12, -18), (9, -1), (-8, 4)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (28, 60), (30, 62), (25, 65), (20, 70), (15, 68),
     (5, 60), (-5, 50)],
    # Asia
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
     (160, 70), (170, 66), (158, 60), (142, 55), (135, 43), (130, 38),
     (127, 35), (122, 32), (120, 25), (110, 20), (105, 10), (100, 8),
     (95, 16), (90, 22), (85, 20), (80, 13), (77, 8), (73, 20), (67, 25),
     (60, 25), (55, 26), (50, 29), (48, 30), (44, 29), (40, 36), (35, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (135, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # Indonesia (island chain, so pin 8 sits on land)
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -5), (135, -4), (140, -8), (138, -5), (130, 0),
     (120, 5), (110, 2), (100, 5)],
]

def lonlat_to_xy(lon, lat, bx, by, bw, bh):
    # equirectangular into the map box; lat 75..-60
    x = bx + (lon + 180.0) / 360.0 * bw
    y = by + (75.0 - lat) / 135.0 * bh
    return x, y

def draw_map(d, bx, by, bw, bh, pins):
    d.rectangle([bx, by, bx + bw, by + bh], fill=NAVY)
    # faint graticule
    for gx in range(1, 6):
        xx = bx + bw * gx / 6
        d.line([xx, by, xx, by + bh], fill=(35, 52, 84), width=1)
    for gy in range(1, 4):
        yy = by + bh * gy / 4
        d.line([bx, yy, bx + bw, yy], fill=(35, 52, 84), width=1)
    for poly in CONTINENTS_LL:
        pts = [lonlat_to_xy(lon, lat, bx, by, bw, bh) for lon, lat in poly]
        d.polygon(pts, fill=BEIGE)
    f_pin = sans(10, True)
    for n, (lon, lat) in pins:
        px, py = lonlat_to_xy(lon, lat, bx, by, bw, bh)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=(200, 16, 46),
                  outline=(255, 255, 255), width=1)
        t = str(n)
        tw = d.textlength(t, font=f_pin)
        d.text((px - tw / 2, py - 5), t, font=f_pin, fill=(255, 255, 255))

# ---- layout ----
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    counts = region_counts()
    assert sum(counts.values()) == 43, counts

    # top strip
    f_top = sans(15, True)
    d.text((16, 5), "THE WORLD IN ONE DAY", font=f_top, fill=RED_DK)
    f_topr = sans(13, True)
    rt = "THURSDAY'S NEWS \u00b7 ONE PAGE \u00b7 43 STORIES"
    d.text((1008 - d.textlength(rt, font=f_topr), 7), rt, font=f_topr, fill=INK)
    d.line([16, 28, 1008, 28], fill=INK, width=2)

    # date headline
    f_date = serif(54, bold=True)
    d.text((16, 34), "Thursday 19 November 2026", font=f_date, fill=INK)

    # red italic sub-headline
    f_sub = serif(18, italic=True)
    d.text((16, 96), "Three leaders meet in Shenzhen \u00b7 GTA VI arrives after a 13-year wait \u00b7 The biggest IPO ever debuts",
           font=f_sub, fill=RED)
    d.line([16, 120, 1008, 120], fill=RULE, width=1)

    # data strip: region bars
    seg_w = 992 / 7
    y_bar, bar_h = 126, 20
    f_bar = sans(12, True)
    for i, r in enumerate(REGIONS):
        x0 = 16 + i * seg_w
        d.rectangle([x0, y_bar, x0 + seg_w - 2, y_bar + bar_h], fill=REG_COL[r])
        t = "%s %d" % (r, counts[r])
        tw = d.textlength(t, font=f_bar)
        d.text((x0 + (seg_w - 2 - tw) / 2, y_bar + 3), t, font=f_bar, fill=(255, 255, 255))
    # big numbers
    cell_w = 992 / 6
    f_num = serif(26, bold=True)
    f_cap = sans(10)
    for i, (num, cap) in enumerate(BIG_NUMBERS):
        x0 = 16 + i * cell_w
        d.text((x0 + 4, 150), num, font=f_num, fill=RED)
        draw_wrapped(d, x0 + 4, 178, cap, f_cap, INK, cell_w - 10, leading=12)
    d.line([16, 206, 1008, 206], fill=INK, width=2)

    # ---- 3 leads ----
    lead_w, lead_gap = 324, 10
    lead_y = 212
    ill_h = 76
    f_badge = sans(12, True)
    f_label = sans(11, True)
    f_head = serif(19, bold=True)
    f_lsub = sans(11)
    for i, s in enumerate(LEADS):
        x0 = 16 + i * (lead_w + lead_gap)
        ILL[s["art"]](d, x0, lead_y, lead_w, ill_h)
        ly = lead_y + ill_h + 6
        # red number badge + place/topic label
        d.rectangle([x0, ly, x0 + 16, ly + 16], fill=RED)
        d.text((x0 + 5, ly + 1), str(s["n"]), font=f_badge, fill=(255, 255, 255))
        d.text((x0 + 21, ly + 2), "%s \u00b7 %s" % (s["place"], s["topic"]),
               font=f_label, fill=RED)
        hy = ly + 20
        draw_wrapped(d, x0, hy, s["headline"], f_head, INK, lead_w, leading=22)
        sy = hy + 46
        draw_wrapped(d, x0, sy, s["sub"], f_lsub, INK, lead_w, leading=13)

    # ---- grid #4-13 (2 rows x 5) ----
    grid_y0, grid_h = 392, 125
    grid_w, grid_gap = 192, 8
    f_glabel = sans(9, True)
    f_ghead = serif(13, bold=True)
    f_gsub = sans(10)
    for i, s in enumerate(GRID):
        row, col = divmod(i, 5)
        x0 = 16 + col * (grid_w + grid_gap)
        y0 = grid_y0 + row * (grid_h + 6)
        ILL[s["art"]](d, x0, y0, grid_w, 48)
        ly = y0 + 52
        d.rectangle([x0, ly, x0 + 14, ly + 13], fill=RED)
        d.text((x0 + 4, ly), str(s["n"]), font=sans(10, True), fill=(255, 255, 255))
        d.text((x0 + 18, ly + 1), "%s \u00b7 %s" % (s["place"], s["topic"]),
               font=f_glabel, fill=RED)
        hy = ly + 17
        hl = wrap(d, s["headline"], f_ghead, grid_w)
        sl = wrap(d, s["sub"], f_gsub, grid_w)
        if len(hl) > 2 or len(sl) > 2:
            print("WARN grid #%d wraps: headline %d lines, sub %d lines" % (s["n"], len(hl), len(sl)))
        draw_wrapped(d, x0, hy, s["headline"], f_ghead, INK, grid_w, leading=15)
        draw_wrapped(d, x0, hy + 32, s["sub"], f_gsub, INK, grid_w, leading=12)

    # ---- map (left) + text list (right) ----
    map_x, map_y, map_w, map_h = 16, 674, 330, 250
    list_x = 354
    f_sec = sans(13, True)
    d.text((map_x, 654), "WHERE IT HAPPENED", font=f_sec, fill=RED_DK)
    d.text((list_x, 654), "ALSO ON THURSDAY 19 NOVEMBER \u2014 30 MORE STORIES",
           font=f_sec, fill=RED_DK)
    pins = [(s["n"], s["pin"]) for s in LEADS + GRID]
    # nudge the crowded Europe pins apart so the numbers stay readable
    # (the map note says positions are approximate)
    PIN_NUDGE = {5: (35.0, 34.0), 6: (40.0, 44.0), 11: (0.0, 45.0), 12: (27.0, 42.5)}
    pins = [(n, PIN_NUDGE.get(n, p)) for n, p in pins]
    draw_map(d, map_x, map_y, map_w, map_h, pins)
    f_note = sans(9)
    draw_wrapped(d, map_x, 928, "Red pins mark stories 1\u201313. Positions are approximate.",
                 f_note, GREY, map_w, leading=11)

    # text list: 2 columns x 15 briefs, one line each
    f_bnum = sans(10, True)
    f_bplace = sans(10, True)
    f_btxt = sans(10)
    col_w = 322
    for i, (place, txt) in enumerate(BRIEFS):
        col = 0 if i < 15 else 1
        row = i if i < 15 else i - 15
        x0 = list_x + col * (col_w + 10)
        y0 = 674 + row * 16
        n = i + 14
        d.text((x0, y0), str(n), font=f_bnum, fill=RED)
        nw = d.textlength(str(n), font=f_bnum) + 4
        full = "%s \u2014 %s" % (place, txt)
        lines = wrap(d, full, f_btxt, col_w - nw)
        if len(lines) > 1:
            print("WARN brief #%d wraps to %d lines: %s" % (n, len(lines), full))
        d.text((x0 + nw, y0), lines[0], font=f_btxt, fill=INK)

    # ---- DATE CHECK box ----
    d.rectangle([16, 946, 1008, 986], outline=RED, width=2)
    f_dc = sans(11)
    draw_wrapped(d, 24, 950, DATE_CHECK, f_dc, INK, 976, leading=13)

    # ---- footer ----
    f_foot = sans(9)
    draw_wrapped(d, 16, 992, FOOTER, f_foot, GREY, 992, leading=11, align="center")

    img.save(OUT, format="JPEG", quality=88)
    return OUT

if __name__ == "__main__":
    out = build()
    print(out, os.path.getsize(out), "bytes")
