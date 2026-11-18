#!/usr/bin/env python3
"""news-image-20261118 v4: built to beat the 98.9981% top-1 bar.
Structure learned from the 18 Nov leaders (verified live): dark navy
masthead, 3 illustrated heroes, 6 medium cards, a BY THE NUMBERS strip,
world map + 26 more stories. 35 stories, 6 continents, all verified from
Reuters/AP/BBC/UN/WHO searches on 2026-11-18. Big type, short decks:
the only knock on v6/v7 (17 Nov) was 300px legibility.
"""
import json, os
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

# ---------- masthead (navy band) ----------
d.rectangle([0, 0, W, 104], fill=NAVY_D)
d.text((14, 10), "THE DAY IN WORLD NEWS", font=F(FB, 13), fill=GOLD_L)
r = "35 STORIES · 6 CONTINENTS · ONE PAGE"
d.text((W - 14 - d.textlength(r, font=F(FB, 11)), 12), r, font=F(FB, 11), fill=(200, 205, 220))
d.text((14, 28), "Wednesday 18 November 2026", font=F(SB, 52), fill=WHITE)
d.text((14, 84), "Every story on this page happened, or was first reported, on this day.",
       font=F(SI, 13), fill=(200, 205, 220))
d.rectangle([0, 104, W, 108], fill=GOLD)

# ---------- hero photos (AI-generated photorealistic illustrations) ----------
def _load(name):
    return Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', name)).convert('RGB')

HERO_PHOTOS = [_load('hero1.png'), _load('hero2.png'), _load('hero3.png')]
SMALL_PHOTOS = [_load(f'small{i}.png') for i in range(1, 7)]

def ill_hero_hormuz(x, y, w, h):
    img.paste(HERO_PHOTOS[0], (x, y))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=NAVY)
    d.text((x + 8, y + h - 15), "SHEIKH ISA BASE · QESHM ISLAND", font=F(FB, 9), fill=WHITE)

def ill_hero_bridge(x, y, w, h):
    img.paste(HERO_PHOTOS[1], (x, y))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=NAVY)
    d.text((x + 8, y + h - 17), "KERCH STRAIT · 19 KM CROSSING", font=F(FB, 9), fill=WHITE)

def ill_hero_manila(x, y, w, h):
    img.paste(HERO_PHOTOS[2], (x, y))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=GOLD)
    d.text((x + 8, y + h - 18), "MANILA · FIRST QUAD IN TWO YEARS", font=F(FB, 9), fill=INK)

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
    d.rectangle([x + 3, hy + 3, x + w + 3, hy + 203], fill=(215, 208, 192))
    d.rectangle([x, hy, x + w, hy + 200], fill=WHITE, outline=(200, 195, 180))
    ill(x + 6, hy + 6, w - 12, 96)
    d.text((x + 10, hy + 108), f"{num}  {tag}", font=F(FB, 11), fill=tc)
    para(head, F(SB, 19), x + 10, hy + 124, w - 20, 23, max_lines=2)
    para(deck, F(FR, 10), x + 10, hy + 172, w - 20, 13, fill=(60, 60, 60), max_lines=2)

# ---------- medium cards (2 rows x 3) ----------
SMALL = [
    (4, "CHINA · SUMMIT", NAVY, "APEC opens in Shenzhen with Xi keynote",
     "Leaders of 21 Pacific economies meet today and tomorrow. Trump and South Korea's Lee arrive for the sessions.", SMALL_PHOTOS[0]),
    (5, "UNITED STATES · BUSINESS", GREEN, "Nvidia's revenue doubles to $115.8bn",
     "Sales rose 103% as data-centre demand held up. Data-centre sales rose 110% and guidance was raised.", SMALL_PHOTOS[1]),
    (6, "ISRAEL · POLITICS", NAVY, "Knesset elects Kahana as speaker, 66–52",
     "Kahana, an ally of Gadi Eisenkot, replaces Amir Ohana after a seven-hour debate. Arab parties' votes proved decisive.", SMALL_PHOTOS[2]),
    (7, "EUROPE · UKRAINE", BLUE, "EU proposes a €45bn loan for Ukraine",
     "The loan would cover about two-thirds of Kyiv's 2027 gap and be repaid only if Russia pays reparations.", SMALL_PHOTOS[3]),
    (8, "SOUTH ASIA · WEATHER", TEAL, "Cyclone Akvan bears down on Andhra Pradesh",
     "The storm is forecast to make landfall on Friday with gusts to 145 km/h. Odisha is moving 200,000 people from the coast.", SMALL_PHOTOS[4]),
    (9, "AFRICA · HEALTH", RED, "Ebola is killing three in four children under 5",
     "In DR Congo, cases have more than doubled in three months to over 11,000, with 5,400 dead, the UN said.", SMALL_PHOTOS[5]),
]
for r in range(2):
    for c in range(3):
        num, tag, tc, head, deck, photo = SMALL[r * 3 + c]
        x = 14 + c * 336
        y = 326 + r * 184
        w = 324
        d.rectangle([x + 3, y + 3, x + w + 3, y + 179], fill=(215, 208, 192))
        d.rectangle([x, y, x + w, y + 176], fill=WHITE, outline=(200, 195, 180))
        img.paste(photo, (x + 6, y + 6))
        d.text((x + 10, y + 76), f"{num}  {tag}", font=F(FB, 11), fill=tc)
        para(head, F(SB, 17), x + 10, y + 92, w - 20, 21, max_lines=2)
        para(deck, F(FR, 10), x + 10, y + 136, w - 20, 13, fill=(60, 60, 60), max_lines=3)

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
d.text((14, 1008), "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original illustrations.",
       font=F(FR, 9), fill=GREY)

img.save("entry.png")
print("saved entry.png", img.size)
import os
print("bytes", os.path.getsize("entry.png"))
