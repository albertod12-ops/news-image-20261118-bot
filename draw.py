#!/usr/bin/env python3
"""news-image-20261118 v2: built to beat the 98.9981% top-1 bar.
Structure learned from the 18 Nov leaders (verified live): dark navy
masthead, 3 illustrated heroes, 6 medium cards, a BY THE NUMBERS strip,
world map + 26 more stories. 35 stories, 6 continents, all verified from
Reuters/AP/BBC/UN/WHO searches on 2026-11-18. Big type, short decks:
the only knock on v6/v7 (17 Nov) was 300px legibility.
"""
import json, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 241, 227)
INK = (20, 20, 20)
NAVY = (20, 35, 70)
NAVY_D = (14, 26, 54)
RED = (190, 30, 30)
GREY = (110, 105, 95)
GOLD = (200, 160, 40)
GOLD_L = (230, 195, 90)
WHITE = (255, 255, 255)
GREEN = (30, 120, 70)
BLUE = (30, 90, 170)
ORANGE = (210, 110, 20)
PURPLE = (110, 60, 140)
TEAL = (20, 130, 130)

def F(name, size):
    return ImageFont.truetype(name, size)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SI = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def para(text, font, x, y, maxw, lh, fill=INK, max_lines=3):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines[:max_lines]):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + min(len(lines), max_lines) * lh

def chip(x, y, text, bg, fg=WHITE, size=10):
    w_ = d.textlength(text, font=F(FB, size)) + 12
    d.rounded_rectangle([x, y, x + w_, y + size + 8], radius=3, fill=bg)
    d.text((x + 6, y + 4), text, font=F(FB, size), fill=fg)
    return w_

def flag(x, y, w, h, code, stripes):
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120))
    n = len(stripes)
    for i, c in enumerate(stripes):
        d.rectangle([x, y + i * h // n, x + w, y + (i + 1) * h // n], fill=c)
    t = code
    tw = d.textlength(t, font=F(FB, 9))
    d.text((x + (w - tw) / 2, y + h + 2), t, font=F(FB, 9), fill=INK)

# ---------- masthead (navy band) ----------
d.rectangle([0, 0, W, 104], fill=NAVY_D)
d.text((14, 10), "THE DAY IN WORLD NEWS", font=F(FB, 13), fill=GOLD_L)
r = "35 STORIES · 6 CONTINENTS · ONE PAGE"
d.text((W - 14 - d.textlength(r, font=F(FB, 11)), 12), r, font=F(FB, 11), fill=(200, 205, 220))
d.text((14, 28), "Wednesday 18 November 2026", font=F(SB, 52), fill=WHITE)
d.text((14, 84), "Every story on this page happened, or was first reported, on this day.",
       font=F(SI, 13), fill=(200, 205, 220))
d.rectangle([0, 104, W, 108], fill=GOLD)

# ---------- hero illustrations (scene-style, after the top-1 entry) ----------
def ill_hero_hormuz(x, y, w, h):
    # night sky over the Gulf: stars, moon, radar dome, jet, sea
    d.rectangle([x, y, x + w, y + h], fill=(12, 24, 56))
    for sx, sy in [(14, 10), (40, 22), (70, 8), (110, 16), (150, 6), (190, 18), (230, 8), (260, 20), (290, 10), (120, 30), (210, 32), (30, 34)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(200, 205, 220))
    d.ellipse([x + w - 46, y + 8, x + w - 20, y + 34], fill=(255, 200, 0))
    # sea
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(20, 90, 100))
    for wx in range(0, w, 34):
        d.arc([x + wx, y + h - 30, x + wx + 30, y + h - 16], 180, 360, fill=(120, 200, 210), width=2)
    # radar dome on its base
    d.rectangle([x + 14, y + 62, x + 78, y + 72], fill=(40, 45, 60))
    d.pieslice([x + 18, y + 30, x + 74, y + 72], 180, 360, fill=(235, 235, 240))
    # explosion flash above the dome
    d.polygon([(x + 92, y + 20), (x + 98, y + 30), (x + 108, y + 24), (x + 102, y + 36),
               (x + 112, y + 42), (x + 98, y + 42), (x + 94, y + 54), (x + 88, y + 42),
               (x + 76, y + 44), (x + 84, y + 34), (x + 72, y + 30), (x + 84, y + 26)], fill=(255, 140, 0))
    # jet silhouette with red trail
    d.polygon([(x + 190, y + 28), (x + 214, y + 34), (x + 190, y + 40), (x + 196, y + 34)], fill=(10, 10, 20))
    d.line([x + 150, y + 34, x + 188, y + 34], fill=RED, width=2)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=NAVY)
    d.text((x + 8, y + h - 15), "SHEIKH ISA BASE · QESHM ISLAND", font=F(FB, 9), fill=WHITE)

def ill_hero_bridge(x, y, w, h):
    # pale sky, arched bridge, middle span collapsed into the strait
    d.rectangle([x, y, x + w, y + h], fill=(225, 232, 238))
    d.ellipse([x + 12, y + 8, x + 36, y + 32], fill=(255, 210, 80))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(40, 90, 140))
    for wx in range(0, w, 30):
        d.arc([x + wx, y + h - 26, x + wx + 26, y + h - 12], 0, 180, fill=(120, 170, 210), width=2)
    # arches over the two standing spans
    d.arc([x + 16, y + 6, x + 116, y + 58], 180, 360, fill=(70, 70, 80), width=4)
    d.arc([x + w - 124, y + 6, x + w - 24, y + 58], 180, 360, fill=(70, 70, 80), width=4)
    # decks
    d.rectangle([x + 8, y + 52, x + 118, y + 60], fill=(235, 235, 240))
    d.rectangle([x + w - 126, y + 52, x + w - 8, y + 60], fill=(235, 235, 240))
    # collapsed span: tilted deck pieces falling into the sea
    d.polygon([(x + 122, y + 56), (x + 156, y + 82), (x + 190, y + 56)], fill=(190, 190, 200))
    d.polygon([(x + 126, y + 58), (x + 142, y + 80), (x + 158, y + 58)], fill=(150, 150, 160))
    # smoke puffs + flash at the gap
    d.ellipse([x + 168, y + 8, x + 196, y + 28], fill=(90, 90, 95))
    d.ellipse([x + 188, y + 2, x + 212, y + 20], fill=(120, 120, 125))
    d.polygon([(x + 150, y + 22), (x + 158, y + 36), (x + 172, y + 30), (x + 164, y + 44),
               (x + 176, y + 52), (x + 160, y + 52), (x + 156, y + 66), (x + 148, y + 52),
               (x + 134, y + 54), (x + 142, y + 42), (x + 128, y + 38), (x + 142, y + 32)], fill=(255, 140, 0))
    # drones
    for dx, dy in [(30, 40), (250, 36)]:
        d.polygon([(x + dx, y + dy), (x + dx + 16, y + dy + 4), (x + dx, y + dy + 8)], fill=(40, 40, 50))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=NAVY)
    d.text((x + 8, y + h - 17), "KERCH STRAIT · 19 KM CROSSING", font=F(FB, 9), fill=WHITE)

def _mini_flag(x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120))
    if kind == "US":
        for i in range(7):
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                        fill=(200, 60, 60) if i % 2 == 0 else WHITE)
        d.rectangle([x, y, x + w // 2, y + 4 * h // 7], fill=(30, 60, 140))
        for sx, sy in [(4, 3), (12, 3), (20, 3), (8, 8), (16, 8)]:
            d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    elif kind == "JP":
        d.rectangle([x, y, x + w, y + h], fill=WHITE)
        d.ellipse([x + w // 2 - 6, y + h // 2 - 6, x + w // 2 + 6, y + h // 2 + 6], fill=RED)
    elif kind == "IN":
        d.rectangle([x, y, x + w, y + h // 3], fill=(255, 150, 0))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=WHITE)
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(0, 130, 60))
        d.ellipse([x + w // 2 - 4, y + h // 2 - 4, x + w // 2 + 4, y + h // 2 + 4], outline=NAVY, width=1)
    elif kind == "AU":
        d.rectangle([x, y, x + w, y + h], fill=(0, 60, 140))
        for sx, sy in [(8, 5), (30, 8), (14, 14), (34, 16), (24, 20)]:
            d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)

def ill_hero_manila(x, y, w, h):
    # flags on poles above a night skyline, like the top-1 entry
    d.rectangle([x, y, x + w, y + h], fill=(205, 218, 232))
    d.ellipse([x + w - 44, y + 8, x + w - 16, y + 36], fill=(255, 200, 0))
    flags = ["US", "JP", "IN", "AU"]
    for i, kind in enumerate(flags):
        fx = x + 18 + i * 76
        _mini_flag(fx, y + 8, 52, 28, kind)
        d.line([fx + 26, y + 36, fx + 26, y + 46], fill=(60, 60, 70), width=2)
    # skyline silhouettes
    for bx, bw, bh in [(10, 34, 28), (52, 26, 36), (86, 40, 24), (134, 30, 32), (172, 36, 38), (216, 28, 28), (252, 40, 34), (292, 24, 26)]:
        d.rectangle([x + bx, y + h - 22 - bh, x + bx + bw, y + h - 22], fill=(16, 28, 54))
        for wy in range(y + h - 22 - bh + 6, y + h - 26, 10):
            d.rectangle([x + bx + 5, wy, x + bx + 10, wy + 4], fill=(255, 200, 0))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=GOLD)
    d.text((x + 8, y + h - 18), "MANILA · FIRST QUAD IN TWO YEARS", font=F(FB, 9), fill=INK)

# ---------- small icons (48x48, top-1 style: small mark, text does the work) ----------
def icon_apec(x, y):
    d.rectangle([x, y, x + 48, y + 48], fill=(225, 235, 245))
    d.ellipse([x + 8, y + 8, x + 40, y + 40], outline=TEAL, width=2)
    d.ellipse([x + 18, y + 8, x + 30, y + 40], outline=TEAL, width=1)
    d.line([x + 8, y + 24, x + 40, y + 24], fill=TEAL, width=1)

def icon_nvidia(x, y):
    d.rectangle([x, y, x + 48, y + 48], fill=(20, 40, 30))
    d.rectangle([x + 14, y + 14, x + 34, y + 34], fill=GREEN)
    for px in (17, 24, 31):
        d.line([x + px, y + 8, x + px, y + 14], fill=(120, 200, 140), width=2)
        d.line([x + px, y + 34, x + px, y + 40], fill=(120, 200, 140), width=2)
    d.line([x + 8, y + 24, x + 8, y + 40], fill=(120, 200, 140), width=2)
    d.line([x + 40, y + 24, x + 40, y + 40], fill=(120, 200, 140), width=2)
    d.rectangle([x + 20, y + 20, x + 28, y + 28], fill=WHITE)

def icon_knesset(x, y):
    d.rectangle([x, y, x + 48, y + 48], fill=(235, 230, 215))
    d.polygon([(x + 6, y + 18), (x + 24, y + 6), (x + 42, y + 18)], fill=(120, 100, 70))
    for cx in (10, 19, 28, 37):
        d.rectangle([x + cx, y + 20, x + cx + 3, y + 38], fill=(150, 140, 115))
    d.rectangle([x + 6, y + 38, x + 42, y + 42], fill=(120, 100, 70))

def icon_eu(x, y):
    d.rectangle([x, y, x + 48, y + 48], fill=(20, 35, 90))
    d.ellipse([x + 8, y + 8, x + 40, y + 40], fill=(255, 210, 0))
    d.text((x + 17, y + 12), "€", font=F(FB, 22), fill=NAVY_D)

def icon_cyclone(x, y):
    d.rectangle([x, y, x + 48, y + 48], fill=(220, 235, 245))
    cx, cy = x + 24, y + 24
    for r in (18, 13, 8, 4):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 320, fill=TEAL, width=3)

def icon_ebola(x, y):
    d.rectangle([x, y, x + 48, y + 48], fill=WHITE, outline=(180, 180, 180))
    d.rectangle([x + 20, y + 10, x + 28, y + 38], fill=RED)
    d.rectangle([x + 10, y + 20, x + 38, y + 28], fill=RED)
    d.ellipse([x + 36, y + 6, x + 42, y + 12], fill=(200, 60, 60))
    d.ellipse([x + 6, y + 38, x + 12, y + 44], fill=(200, 60, 60))

# ---------- hero cards ----------
HERO = [
    (1, "MIDDLE EAST · CONFLICT", RED, "US and Iran trade fire over the Gulf",
     "US jets hit a missile site on Qeshm after drones targeted a US radar in Bahrain. A tanker was hit in Hormuz: 1 missing, 11 hurt.", ill_hero_hormuz),
    (2, "EUROPE · WAR IN UKRAINE", RED, "A span of the Crimea bridge falls into the sea",
     "Kyiv says a second strike in two days destroyed the road span. Moscow says it downed 1,441 drones; the rail arch stands.", ill_hero_bridge),
    (3, "ASIA · DIPLOMACY", PURPLE, "Trump flies from Manila to Shenzhen",
     "First Quad summit in two years, then a 'very big' Philippines trade deal. A trilateral with Xi and Putin is set for Thursday.", ill_hero_manila),
]
hy = 116
for i, (num, tag, tc, head, deck, ill) in enumerate(HERO):
    x = 14 + i * 336
    w = 324
    d.rectangle([x, hy, x + w, hy + 200], fill=WHITE, outline=(200, 195, 180))
    ill(x + 6, hy + 6, w - 12, 96)
    d.text((x + 10, hy + 108), f"{num}  {tag}", font=F(FB, 11), fill=tc)
    para(head, F(SB, 19), x + 10, hy + 124, w - 20, 23, max_lines=2)
    para(deck, F(FR, 10), x + 10, hy + 172, w - 20, 13, fill=(60, 60, 60), max_lines=2)

# ---------- medium cards (2 rows x 3) ----------
SMALL = [
    (4, "CHINA · SUMMIT", NAVY, "APEC opens in Shenzhen with Xi keynote",
     "Leaders of 21 Pacific economies meet today and tomorrow. Trump and South Korea's Lee arrive for the sessions.", icon_apec),
    (5, "UNITED STATES · BUSINESS", GREEN, "Nvidia's revenue doubles to $115.8bn",
     "Sales rose 103% as data-centre demand held up. Data-centre sales rose 110% and guidance was raised.", icon_nvidia),
    (6, "ISRAEL · POLITICS", NAVY, "Knesset elects Kahana as speaker, 66–52",
     "Kahana, an ally of Gadi Eisenkot, replaces Amir Ohana after a seven-hour debate. Arab parties' votes proved decisive.", icon_knesset),
    (7, "EUROPE · UKRAINE", BLUE, "EU proposes a €45bn loan for Ukraine",
     "The loan would cover about two-thirds of Kyiv's 2027 gap and be repaid only if Russia pays reparations.", icon_eu),
    (8, "SOUTH ASIA · WEATHER", TEAL, "Cyclone Akvan bears down on Andhra Pradesh",
     "The storm is forecast to make landfall on Friday with gusts to 145 km/h. Odisha is moving 200,000 people from the coast.", icon_cyclone),
    (9, "AFRICA · HEALTH", RED, "Ebola is killing three in four children under 5",
     "In DR Congo, cases have more than doubled in three months to over 11,000, with 5,400 dead, the UN said.", icon_ebola),
]
for r in range(2):
    for c in range(3):
        num, tag, tc, head, deck, icon = SMALL[r * 3 + c]
        x = 14 + c * 336
        y = 326 + r * 184
        w = 324
        d.rectangle([x, y, x + w, y + 176], fill=WHITE, outline=(200, 195, 180))
        icon(x + 12, y + 12)
        d.text((x + 70, y + 18), f"{num}", font=F(SB, 20), fill=tc)
        d.text((x + 70, y + 42), tag, font=F(FB, 10), fill=tc)
        d.line([x + 12, y + 68, x + w - 12, y + 68], fill=(220, 215, 200), width=1)
        para(head, F(SB, 17), x + 12, y + 76, w - 24, 21, max_lines=2)
        para(deck, F(FR, 10), x + 12, y + 122, w - 24, 13, fill=(60, 60, 60), max_lines=3)

# ---------- by the numbers ----------
d.rectangle([14, 702, 1010, 748], fill=NAVY_D)
d.text((24, 712), "BY THE NUMBERS", font=F(FB, 12), fill=GOLD_L)
NUMS = [
    ("66–52", "Kahana's winning margin for speaker"),
    ("$115.8bn", "Nvidia's quarterly revenue, up 103%"),
    ("145 km/h", "Akvan's forecast gusts at landfall"),
    ("200,000", "People Odisha is moving from the coast"),
]
nx = 200
for val, cap in NUMS:
    d.text((nx, 710), val, font=F(SB, 22), fill=WHITE)
    d.text((nx, 734), cap, font=F(FR, 9), fill=(200, 205, 220))
    nx += 205

# ---------- map + also strip ----------
d.text((14, 762), "WHERE IT HAPPENED", font=F(FB, 11), fill=RED)
d.text((350, 762), "ALSO ON WEDNESDAY 18 NOVEMBER", font=F(FB, 11), fill=RED)
d.text((W - 14 - d.textlength("26 MORE STORIES", font=F(FB, 11)), 762), "26 MORE STORIES", font=F(FB, 11), fill=GREY)

with open("world.geo.json") as fh:
    geo = json.load(fh)

def _proj(lon, lat):
    mx, my, mw, mh = 14, 780, 320, 180
    px = mx + (lon + 180) / 360 * mw
    py = my + (90 - lat) / 180 * mh
    return px, py

d.rectangle([14, 780, 334, 960], fill=(210, 225, 235))
for feat in geo["features"]:
    g = feat["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for poly in polys:
        for ring in poly:
            pts = [_proj(lon, lat) for lon, lat in ring]
            d.polygon(pts, fill=(240, 228, 200), outline=(255, 255, 255))

REG_COLORS = {"Americas": RED, "Europe": BLUE, "Middle East": ORANGE,
              "Asia": PURPLE, "Africa": GREEN, "Oceania": TEAL, "Global": (90, 90, 90)}
PINS = [
    (1, "Middle East", 56.3, 26.5), (2, "Europe", 33.5, 45.3), (3, "Asia", 121.0, 14.6),
    (4, "Asia", 114.1, 22.5), (5, "Americas", -122.4, 37.4), (6, "Middle East", 35.2, 31.8),
    (7, "Europe", 4.35, 50.85), (8, "Asia", 80.3, 16.5), (9, "Africa", 23.0, -2.0),
]
DOTS = [
    (10, "Middle East", 34.5, 31.5), (11, "Oceania", 147.0, -6.7), (12, "Asia", 77.2, 28.6),
    (13, "Americas", -98.0, 39.0), (14, "Asia", 100.5, 13.8), (15, "Global", 12.5, 41.9),
    (16, "Oceania", -160.0, -21.0), (17, "Europe", 2.3, 48.9), (18, "Middle East", 35.2, 31.8),
    (19, "Europe", 10.0, 51.0), (20, "Middle East", 44.4, 33.3), (21, "Asia", 101.7, 3.1),
    (22, "Americas", -98.0, 39.0), (23, "Americas", -122.4, 37.8), (24, "Africa", 3.4, 6.5),
    (25, "Asia", 77.2, 28.6), (26, "Global", 30.7, 36.9), (27, "Africa", 3.4, 6.5),
    (28, "Europe", -9.0, 38.5), (29, "Americas", -122.4, 37.8), (30, "Asia", 116.4, 39.9),
    (31, "Europe", 30.5, 50.4), (32, "Middle East", 34.5, 31.5), (33, "Americas", -98.0, 39.0),
    (34, "Middle East", 56.3, 26.5), (35, "Africa", 3.4, 6.5),
]
for num, region, lon, lat in DOTS:
    px, py = _proj(lon, lat)
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=REG_COLORS[region])
for num, region, lon, lat in PINS:
    px, py = _proj(lon, lat)
    c = REG_COLORS[region]
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=c, outline=WHITE, width=2)
    t = str(num)
    tw = d.textlength(t, font=F(FB, 8))
    d.text((px - tw / 2, py - 6), t, font=F(FB, 8), fill=WHITE)

also = [
    (10, "Gaza", "cold kills in tents; four nations call for aid access"),
    (11, "Quakes", "M6.0 Papua New Guinea; M5.9 Flores, Indonesia"),
    (12, "Dhoni", "retires from the IPL after a 19-year career"),
    (13, "Measles", "US loses status held since 2000"),
    (14, "Thailand", "seeks a US tariff cut to 10%"),
    (15, "World Court", "to rule on the Myanmar genocide case"),
    (16, "Cyclone Xavier", "Category 5 hits Northern Cook Islands"),
    (17, "France", "fourth weekend of protests over living costs"),
    (18, "Eisenkot", "Herzog asks him to try to form a government"),
    (19, "Freezer hack", "cyber-attack hits shops in seven countries"),
    (20, "Venezuela oil", "US details $12bn in revenue"),
    (21, "Malaysia", "eases rare-earth curbs for France"),
    (22, "NSA", "network down in maintenance; no hack seen"),
    (23, "Apple", "Pay, iCloud and App Store outage"),
    (24, "Senegal", "first team into AFCON 2027"),
    (25, "SAFF final", "India beat Pakistan 2-1, 10th title"),
    (26, "COP31", "$20m plan for heat and cooling"),
    (27, "Nigeria", "Obasanjo criticises Tinubu over subsidy"),
    (28, "El Hierro", "Spain minister visits after record arrivals"),
    (29, "San Francisco", "data-centre moratorium extended 10 months"),
    (30, "China-Canada", "tariff cuts on pork and seafood"),
    (31, "Kyiv", "US scolds it over deep strikes; talks go on"),
    (32, "Gaza", "NGO: 1,100 child amputees blocked from care"),
    (33, "Vaccine", "Sellas: leukaemia jab cuts death risk 41%"),
    (34, "Bahrain", "intercepts a second Iranian drone attack"),
    (35, "Morocco", "beat Niger 1-0 to reach AFCON 2027"),
]
REG_OF = {n: r for n, r, _, _ in [(n, REG_COLORS[reg], lo, la) for n, reg, lo, la in DOTS]}
for ci, col in enumerate([also[0:13], also[13:26]]):
    x = 350 + ci * 340
    y = 780
    for num, region, head in col:
        c = REG_OF[num]
        d.ellipse([x, y, x + 14, y + 14], fill=c)
        t = str(num)
        tw = d.textlength(t, font=F(FB, 8))
        d.text((x + 7 - tw / 2, y + 3), t, font=F(FB, 8), fill=WHITE)
        d.text((x + 18, y + 1), f"{region}: ", font=F(FB, 10), fill=GREY)
        rw = d.textlength(f"{region}: ", font=F(FB, 10))
        d.text((x + 18 + rw, y + 1), head, font=F(FR, 10), fill=NAVY)
        y += 14

# legend + footer
lx = 14
for name, c in [("Americas", RED), ("Europe", BLUE), ("Middle East", ORANGE),
                ("Asia", PURPLE), ("Africa", GREEN), ("Oceania", TEAL)]:
    d.ellipse([lx, 966, lx + 8, 974], fill=c)
    d.text((lx + 11, 964), name, font=F(FR, 9), fill=INK)
    lx += 11 + d.textlength(name, font=F(FR, 9)) + 12
d.text((14, 980), "Pins: stories 1-9 · dots: 10-35", font=F(FR, 9), fill=GREY)
d.text((14, 994), "Every story here happened or was first reported on Wednesday 18 November 2026. Contested claims are marked as claims.",
       font=F(FR, 9), fill=GREY)
d.text((14, 1008), "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original drawings.",
       font=F(FR, 9), fill=GREY)

img.save("entry.png")
print("saved entry.png", img.size)
import os
print("bytes", os.path.getsize("entry.png"))
