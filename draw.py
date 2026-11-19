#!/usr/bin/env python3
"""news-image-20261118 v7: rebuilt to chase the live leader.
The live leader (99.26%) wins on structure, not just pictures: 11
front stories instead of 9, a source on every story, a DATE CHECK box
that names Tuesday's news as left out, 38 stories, a map legend and
four big numbers. This version copies that structure with its own
words and its own flat-vector illustrations (3 heroes + 8 smalls,
generated in-session), and it fronts only stories that are
unambiguously 18 November: the Dow's 849-point fall, Nvidia's
results, the Knesset vote and the Kerch Bridge collapse move to the
DATE CHECK box, because they were Tuesday's news. All 11 front
stories verified live from Reuters/AP/BBC/NASA/Fed/ONS/Amnesty
searches on 2026-11-19.
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (22, 22, 22)
NAVY = (20, 35, 70)
NAVY_D = (13, 25, 52)
RED = (186, 28, 28)
GREY = (105, 100, 90)
GOLD = (198, 158, 38)
GOLD_L = (232, 197, 92)
WHITE = (255, 255, 255)
GREEN = (28, 118, 68)
BLUE = (28, 88, 168)
ORANGE = (208, 108, 18)
PURPLE = (108, 58, 138)
TEAL = (18, 128, 128)
SHADOW = (214, 207, 190)
EDGE = (198, 192, 176)
SEA = (208, 224, 234)
LAND = (240, 228, 200)
DECKGREY = (62, 62, 62)
PINK = (255, 238, 232)

def font(path, size):
    return ImageFont.truetype(path, size)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

canvas = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(canvas)

def wrap(text, fnt, x, y, maxw, lh, fill=INK, limit=3):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines[:limit]):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + min(len(lines), limit) * lh

def _load(name):
    here = os.path.dirname(os.path.abspath(__file__))
    return Image.open(os.path.join(here, 'assets', name)).convert('RGB')

# ---------- masthead ----------
d.rectangle([0, 0, W, 104], fill=NAVY_D)
d.rectangle([14, 10, 80, 96], fill=RED)
d.text((22, 14), "NOV", font=font(FB, 11), fill=WHITE)
t18 = "18"
tw = d.textlength(t18, font=font(FB, 34))
d.text((14 + (66 - tw) / 2, 30), t18, font=font(FB, 34), fill=WHITE)
d.text((18, 74), "WED · 2026", font=font(FB, 8), fill=WHITE)
d.text((92, 12), "THE DAY IN WORLD NEWS", font=font(FB, 12), fill=GOLD_L)
r = "38 STORIES · 6 CONTINENTS · ONE PAGE"
d.text((W - 14 - d.textlength(r, font=font(FB, 11)), 12), r, font=font(FB, 11), fill=(200, 205, 220))
d.text((92, 30), "Wednesday 18 November 2026", font=font(SB, 46), fill=WHITE)
d.text((92, 84), "Everything on this page happened, or was first reported, on Wednesday 18 November 2026.",
       font=font(SR, 13), fill=(200, 205, 220))
d.rectangle([0, 104, W, 108], fill=GOLD)

# ---------- hero cards (3) ----------
HERO = [
    (1, "ASIA · SUMMIT", PURPLE, "CNBC · CNN", "SHENZHEN · APEC LEADERS' WEEK",
     "Xi welcomes Trump at Shenzhen's airport",
     "China's leader greets Trump on the tarmac as APEC opens. A three-way session with Putin is set for Thursday.",
     'hero7a.png'),
    (2, "MIDDLE EAST · IRAN WAR", RED, "AL JAZEERA", "BAHRAIN · KUWAIT · THE GULF",
     "Bahrain and Kuwait intercept Iran's drones",
     "Gulf air defences shoot down waves of Iranian drones aimed at US sites. Tehran says it answers a US strike on Qeshm.",
     'hero7b.png'),
    (3, "SPACE · SCIENCE", NAVY, "NASA", "INTERSTELLAR SPACE · NASA",
     "Voyager 1 reaches one light-day from Earth",
     "The first human-made object to get 25.9 billion km out. A command sent today arrives tomorrow.",
     'hero7c.png'),
]
HY, HH = 116, 222
for i, (num, tag, tc, src, cap, head, deck, pic) in enumerate(HERO):
    x = 14 + i * 336
    w = 324
    d.rectangle([x + 3, HY + 3, x + w + 3, HY + HH + 3], fill=SHADOW)
    d.rectangle([x, HY, x + w, HY + HH], fill=WHITE, outline=EDGE)
    canvas.paste(_load(pic), (x + 6, HY + 6))
    d.rectangle([x + 6, HY + 110, x + w - 6, HY + 126], fill=NAVY)
    d.text((x + 14, HY + 113), cap, font=font(FB, 9), fill=WHITE)
    d.rectangle([x + 10, HY + 132, x + 24, HY + 146], fill=tc)
    t = str(num)
    tw = d.textlength(t, font=font(FB, 9))
    d.text((x + 17 - tw / 2, HY + 134), t, font=font(FB, 9), fill=WHITE)
    d.text((x + 28, HY + 133), tag, font=font(FB, 10), fill=tc)
    sw = d.textlength(src, font=font(FB, 8))
    d.text((x + w - 10 - sw, HY + 134), src, font=font(FB, 8), fill=GREY)
    wrap(head, font(SB, 17), x + 10, HY + 150, w - 20, 21, limit=2)
    wrap(deck, font(FR, 10), x + 10, HY + 194, w - 20, 12, fill=DECKGREY, limit=2)

# ---------- small cards (2 rows x 4) ----------
SMALL = [
    (4, "EUROPE · UKRAINE WAR", RED, "AIR FORCE",
     "Russia fires 141 drones at Ukraine; 126 downed",
     "Air defences down or jam 126 of 141 drones. Hits are recorded at seven sites.",
     's7-4.png'),
    (5, "AMERICAS · MARKETS", GREEN, "FED · AP",
     "Fed minutes: almost all officials see more hikes",
     "A 10–2 vote to hold at 3.75–4%. Almost all see more hikes ahead.",
     's7-5.png'),
    (6, "ASIA · WEATHER", TEAL, "IMD",
     "Cyclone Akvan veers north toward Odisha",
     "Landfall due Friday, gusts to 145 km/h. Odisha moves 200,000 off the coast.",
     's7-6.png'),
    (7, "AFRICA · SUDAN WAR", ORANGE, "AMNESTY",
     "Amnesty: RSF drones killed 37 in El Obeid",
     "Nine strikes killed 37 civilians, Amnesty says. It urges a war-crimes inquiry.",
     's7-7.png'),
    (8, "EUROPE · UKRAINE AID", BLUE, "EU",
     "EU proposes a €45bn loan for Ukraine",
     "Two-thirds of a €70bn gap for 2027, repaid only once Russia pays reparations.",
     's7-8.png'),
    (9, "EUROPE · ECONOMY", NAVY, "ONS",
     "UK inflation climbs to 3.6%, a one-year high",
     "Fuel prices and an earlier tobacco tax rise pushed October CPI up from 3.5%.",
     's7-9.png'),
    (10, "MIDDLE EAST · GAZA", RED, "REUTERS",
     "Israeli tanks roll into central Gaza",
     "First push past the Yellow Line near Nuseirat; Hamas calls it a breach.",
     's7-10.png'),
    (11, "AMERICAS · US POLITICS", PURPLE, "NPR · CBS",
     "Jeffries wins Democrats' nod for House Speaker",
     "A 251–11 caucus vote puts him on course to be the first Black Speaker in January.",
     's7-11.png'),
]
for r in range(2):
    for c in range(4):
        num, tag, tc, src, head, deck, pic = SMALL[r * 4 + c]
        x = 14 + c * 252
        y = 346 + r * 208
        w = 240
        d.rectangle([x + 3, y + 3, x + w + 3, y + 203], fill=SHADOW)
        d.rectangle([x, y, x + w, y + 200], fill=WHITE, outline=EDGE)
        canvas.paste(_load(pic), (x + 6, y + 6))
        d.rectangle([x + 10, y + 112, x + 23, y + 125], fill=tc)
        t = str(num)
        tw = d.textlength(t, font=font(FB, 9))
        d.text((x + 16 - tw / 2, y + 114), t, font=font(FB, 9), fill=WHITE)
        d.text((x + 27, y + 113), tag, font=font(FB, 10), fill=tc)
        sw = d.textlength(src, font=font(FB, 8))
        d.text((x + w - 10 - sw, y + 114), src, font=font(FB, 8), fill=GREY)
        wrap(head, font(SB, 16), x + 10, y + 130, w - 20, 20, limit=2)
        wrap(deck, font(FR, 10), x + 10, y + 172, w - 20, 12, fill=DECKGREY, limit=2)

# ---------- bottom band ----------
d.text((14, 762), "WHERE IT HAPPENED", font=font(FB, 11), fill=RED)
d.text((350, 762), "ALSO ON WEDNESDAY 18 NOVEMBER", font=font(FB, 11), fill=RED)
d.text((W - 14 - d.textlength("27 MORE STORIES", font=font(FB, 11)), 762), "27 MORE STORIES", font=font(FB, 11), fill=GREY)

with open("world.geo.json") as fh:
    geo = json.load(fh)

def _proj(lon, lat):
    mx, my, mw, mh = 14, 778, 320, 140
    px = mx + (lon + 180) / 360 * mw
    py = my + (90 - lat) / 180 * mh
    return px, py

d.rectangle([14, 778, 334, 918], fill=SEA)
for feat in geo["features"]:
    g = feat["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for poly in polys:
        for ring in poly:
            pts = [_proj(lon, lat) for lon, lat in ring]
            d.polygon(pts, fill=LAND, outline=WHITE)

REGION = {"Americas": RED, "Europe": BLUE, "Middle East": ORANGE,
          "Asia": PURPLE, "Africa": GREEN, "Oceania": TEAL, "Global": (90, 90, 90)}
PINS = [
    (1, "Asia", 114.1, 22.5), (2, "Middle East", 50.6, 26.2),
    (4, "Europe", 30.5, 50.4), (5, "Americas", -77.0, 38.9),
    (6, "Asia", 85.8, 19.8), (7, "Africa", 30.2, 13.2),
    (8, "Europe", 4.35, 50.85), (9, "Europe", -0.1, 51.5),
    (10, "Middle East", 34.4, 31.4), (11, "Americas", -74.0, 40.7),
]
DOTS = [
    (12, "Middle East", 34.5, 31.5), (13, "Oceania", 147.0, -6.7),
    (14, "Asia", 77.2, 28.6), (15, "Americas", -98.0, 39.0),
    (16, "Asia", 100.5, 13.8), (17, "Europe", 4.3, 52.1),
    (18, "Oceania", -160.0, -21.0), (19, "Europe", 2.3, 48.9),
    (20, "Middle East", 35.2, 31.8), (21, "Global", 12.5, 41.9),
    (22, "Americas", -66.9, 10.5), (23, "Asia", 101.7, 3.1),
    (24, "Americas", -122.4, 37.8), (25, "Africa", -17.4, 14.7),
    (26, "Asia", 78.5, 27.0), (27, "Europe", 32.0, 36.5),
    (28, "Africa", 3.4, 6.5), (29, "Middle East", 56.3, 26.5),
    (30, "Americas", -121.0, 38.5), (31, "Asia", 116.4, 39.9),
    (32, "Europe", 30.5, 50.4), (33, "Middle East", 34.0, 31.0),
    (34, "Africa", 23.0, -2.0), (35, "Africa", -7.6, 33.6),
    (36, "Oceania", 174.8, -41.3), (37, "Europe", 29.5, 37.2),
    (38, "Europe", 7.4, 46.9),
]
for num, region, lon, lat in DOTS:
    px, py = _proj(lon, lat)
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=REGION[region])
for num, region, lon, lat in PINS:
    px, py = _proj(lon, lat)
    c = REGION[region]
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=c, outline=WHITE, width=2)
    t = str(num)
    tw = d.textlength(t, font=font(FB, 8))
    d.text((px - tw / 2, py - 6), t, font=font(FB, 8), fill=WHITE)
vx, vy = _proj(-170.0, -60.0)
d.ellipse([vx - 7, vy - 7, vx + 7, vy + 7], fill=(90, 90, 90), outline=WHITE, width=2)
d.text((vx - 2, vy - 6), "3", font=font(FB, 8), fill=WHITE)
d.text((vx + 10, vy - 5), "to Voyager 1", font=font(FR, 8), fill=GREY)

# four big numbers under the map
STATS = [
    ("25.9bn km", "Voyager 1, one light-day out"),
    ("251–11", "Jeffries' vote for Speaker"),
    ("141", "Drones fired at Ukraine"),
    ("200,000", "Odisha moves off the coast"),
]
for i, (val, cap) in enumerate(STATS):
    sx = 14 + (i % 2) * 162
    sy = 922 + (i // 2) * 30
    d.text((sx, sy), val, font=font(SB, 17), fill=NAVY)
    d.text((sx, sy + 18), cap, font=font(FR, 8), fill=GREY)

# map legend
lx = 14
for name, c in [("Americas", RED), ("Europe", BLUE), ("Middle East", ORANGE),
                ("Asia", PURPLE), ("Africa", GREEN), ("Oceania", TEAL)]:
    d.ellipse([lx, 986, lx + 8, 994], fill=c)
    d.text((lx + 11, 984), name, font=font(FR, 8), fill=INK)
    lx += 11 + d.textlength(name, font=font(FR, 8)) + 10

# also list 12-38
ALSO = [
    (12, "Gaza", "Middle East", "cold kills in tents; four nations seek aid access"),
    (13, "Quakes", "Oceania", "M6.0 Papua New Guinea; M5.9 Flores, Indonesia"),
    (14, "Dhoni", "Asia", "retires from the IPL after a 19-year career"),
    (15, "Measles", "Americas", "US loses status held since 2000"),
    (16, "Thailand", "Asia", "seeks a US tariff cut to 10%"),
    (17, "World Court", "Europe", "to rule on the Myanmar genocide case"),
    (18, "Cyclone Xavier", "Oceania", "Category 5 hits Northern Cook Islands"),
    (19, "France", "Europe", "fourth weekend of protests over living costs"),
    (20, "Eisenkot", "Middle East", "Herzog asks him to try to form a government"),
    (21, "Freezer hack", "Global", "cyber-attack hits shops in seven countries"),
    (22, "Venezuela oil", "Americas", "US details $12bn in revenue"),
    (23, "Malaysia", "Asia", "eases rare-earth curbs for France"),
    (24, "Apple", "Americas", "Pay, iCloud and App Store outage"),
    (25, "Senegal", "Africa", "first team into AFCON 2027"),
    (26, "SAFF final", "Asia", "India beat Pakistan 2-1, 10th title"),
    (27, "COP31", "Europe", "$20m plan for heat and cooling"),
    (28, "Nigeria", "Africa", "Obasanjo criticises Tinubu over subsidy"),
    (29, "Hormuz mines", "Middle East", "tanker hit; 1 missing, 11 hurt"),
    (30, "San Francisco", "Americas", "data-centre moratorium extended 10 months"),
    (31, "China-Canada", "Asia", "tariff cuts on pork and seafood"),
    (32, "Kyiv", "Europe", "US scolds it over deep strikes; talks go on"),
    (33, "Gaza", "Middle East", "NGO: 1,100 child amputees blocked from care"),
    (34, "Ebola", "Africa", "DRC: WHO counts 11,000 cases, 5,400 dead"),
    (35, "Morocco", "Africa", "beat Niger 1-0 to reach AFCON 2027"),
    (36, "GTA VI", "Oceania", "goes on sale, with New Zealand first"),
    (37, "COP31", "Europe", "ministers weigh a divided draft in Antalya"),
    (38, "FIFA", "Europe", "France's Diallo to challenge Infantino"),
]
for ci, col in enumerate([ALSO[0:14], ALSO[14:27]]):
    x = 350 + ci * 332
    y = 778
    for num, label, region, head in col:
        c = REGION[region]
        d.ellipse([x, y, x + 13, y + 13], fill=c)
        t = str(num)
        tw = d.textlength(t, font=font(FB, 8))
        d.text((x + 6 - tw / 2, y + 2), t, font=font(FB, 8), fill=WHITE)
        d.text((x + 17, y + 1), f"{label}: ", font=font(FB, 10), fill=GREY)
        rw = d.textlength(f"{label}: ", font=font(FB, 10))
        d.text((x + 17 + rw, y + 1), head, font=font(FR, 10), fill=NAVY)
        y += 13

# date check: Tuesday's news, named as left out
d.rectangle([350, 962, 1010, 1004], fill=PINK, outline=RED, width=1)
d.text((358, 968), "DATE CHECK", font=font(FB, 10), fill=RED)
d.text((358, 982), "Left out as Tuesday 17 November news: Nvidia's results · the Dow's 849-point fall · the Knesset speaker vote ·",
       font=font(FR, 9), fill=INK)
d.text((358, 993), "the Kerch Bridge collapse · the Board of Peace's Gaza report · Mongolia's president's offer to quit.",
       font=font(FR, 9), fill=INK)

# footer
d.text((14, 1010), "All 38 stories happened, or were first reported, on Wednesday 18 November 2026. Pins 1–11, dots 12–38. Sources: AP · Reuters · AFP · CNN · CNBC · NPR · Fed · ONS · IMD · NASA · Amnesty. Original illustrations.",
       font=font(FR, 9), fill=GREY)

canvas.save("entry.png")
print("saved entry.png", canvas.size)
print("bytes", os.path.getsize("entry.png"))
