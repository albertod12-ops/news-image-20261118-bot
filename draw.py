#!/usr/bin/env python3
"""news-image-20261118 v8: 46 stories, UTC timeline, region strip, in-art labels.
Draws entry.png (1024x1024, deterministic) from assets/ + world.geo.json.
Run: python3 draw.py  -> writes entry.png in this directory."""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (14, 27, 61)
RED = (200, 16, 46)
GOLD = (201, 162, 39)
YELLOW = (255, 210, 31)
GREY = (90, 90, 90)
RULE = (180, 170, 150)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 44)
F_EYE = font("DejaVuSans-Bold.ttf", 13)
F_SUB = font("DejaVuSerif.ttf", 14)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_DATE2 = font("DejaVuSans-Bold.ttf", 11)
F_REG = font("DejaVuSans-Bold.ttf", 11)
F_TTIME = font("DejaVuSans-Bold.ttf", 11)
F_TTEXT = font("DejaVuSans.ttf", 10)
F_KICK = font("DejaVuSans-Bold.ttf", 10)
F_SRC = font("DejaVuSans-Bold.ttf", 9)
F_HEAD = font("DejaVuSerif-Bold.ttf", 17)
F_HEAD_S = font("DejaVuSerif-Bold.ttf", 15)
F_DECK = font("DejaVuSans.ttf", 11)
F_DECK_S = font("DejaVuSans.ttf", 10)
F_LABEL = font("DejaVuSans-Bold.ttf", 11)
F_ALSO = font("DejaVuSans.ttf", 11)
F_ALSO_N = font("DejaVuSans-Bold.ttf", 11)
F_SEC = font("DejaVuSans-Bold.ttf", 12)
F_STAT = font("DejaVuSerif-Bold.ttf", 20)
F_STATC = font("DejaVuSans.ttf", 9)
F_DATECHK = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 10)

REGIONS = [
    ("ASIA", 7, (122, 63, 160)),
    ("EUROPE", 6, (36, 90, 180)),
    ("AMERICAS", 9, (30, 140, 80)),
    ("AFRICA", 6, (220, 110, 20)),
    ("MIDDLE EAST", 7, (200, 40, 40)),
    ("OCEANIA", 2, (20, 150, 160)),
    ("GLOBAL", 9, (100, 100, 100)),
]

TIMELINE = [
    ("OVERNIGHT", "Drones over Kuwait, Bahrain, Ukraine"),
    ("07:00 UTC", "UK inflation: 3.6%"),
    ("MORNING", "Xi greets Trump in Shenzhen"),
    ("10:16 UTC", "Voyager 1: one light-day"),
    ("11:00 UTC", "GTA VI unlocks in New Zealand"),
    ("AFTERNOON", "EU offers Kyiv \u20ac45bn"),
    ("19:00 UTC", "Fed minutes: more hikes"),
    ("21:00 UTC", "Wall Street: Dow down 1.1%"),
]

# num, region, topic, source, headline, deck, in-art label, image
FRONT = [
    (1, "ASIA", "SUMMIT", "CNBC \u00b7 CNN",
     "Xi greets Trump as APEC opens",
     "Shenzhen airport welcome; three-way session with Putin set for Thursday.",
     "APEC OPENS", "hero7a.png"),
    (2, "MIDDLE EAST", "IRAN WAR", "AL JAZEERA",
     "Gulf states down Iranian drones",
     "Bahrain, Kuwait intercept; Tehran calls it answer to US strike on Qeshm.",
     "INTERCEPTED", "hero7b.png"),
    (3, "SPACE", "SCIENCE", "NASA",
     "Voyager 1 reaches one light-day",
     "25.9 billion km out; a command sent today arrives tomorrow.",
     "ONE LIGHT-DAY", "hero7c.png"),
    (4, "EUROPE", "UKRAINE WAR", "AIR FORCE",
     "Russia fires 141 drones at Ukraine",
     "Air defences down 126 of 141; strikes land at seven sites.",
     "141 FIRED / 126 DOWNED", "s7-4.png"),
    (5, "AMERICAS", "MARKETS", "FED \u00b7 AP",
     "Fed minutes point to more hikes",
     "October 27\u201328 minutes: almost all officials see further tightening; 10\u20132 hold.",
     "MORE HIKES", "s7-5.png"),
    (6, "ASIA", "WEATHER", "IMD",
     "Cyclone Akvan bears down on Odisha",
     "Landfall Friday; 145 km/h gusts; 200,000 moved off the coast.",
     "200,000 MOVED", "s7-6.png"),
    (7, "AFRICA", "SUDAN WAR", "AMNESTY",
     "Amnesty: RSF drones killed 37",
     "Nine strikes in El Obeid, June to August; war-crimes inquiry urged.",
     "37 KILLED", "s7-7.png"),
    (8, "EUROPE", "UKRAINE AID", "EU",
     "EU proposes \u20ac45bn loan to Kyiv",
     "For 2027; repayment only if Russia pays reparations.",
     "\u20ac45 BILLION", "s7-8.png"),
    (9, "MIDDLE EAST", "GAZA", "REUTERS",
     "Israeli tanks push past Yellow Line",
     "First drive into central Gaza near Nuseirat; tunnel found; three killed.",
     "PAST YELLOW LINE", "s7-9.png"),
    (10, "AMERICAS", "US POLITICS", "NPR \u00b7 CBS",
     "Jeffries wins Democrats' speaker nod",
     "Caucus vote 251\u201311; floor vote set for January 3.",
     "251\u201311", "s7-10.png"),
    (11, "GLOBAL", "CULTURE", "ROCKSTAR",
     "GTA VI goes on sale after 13 years",
     "Thirteen-year wait ends; midnight launch, New Zealand first at 11:00 UTC.",
     "13-YEAR WAIT", "s8-11.png"),
]

# num, city, text
ALSO = [
    (12, "UK", "Inflation climbs to 3.6%, a one-year high"),
    (13, "Gaza", "cold kills in tents; four nations seek aid access"),
    (14, "Quakes", "M6.0 Papua New Guinea; M5.9 Flores"),
    (15, "Dhoni", "retires from the IPL after a 19-year career"),
    (16, "Measles", "US loses status held since 2000"),
    (17, "Thailand", "seeks a US tariff cut to 10%"),
    (18, "World Court", "to rule on the Myanmar genocide case"),
    (19, "Cyclone Xavier", "Category 5 hits Northern Cook Islands"),
    (20, "France", "fourth weekend of protests over living costs"),
    (21, "Eisenkot", "Herzog asks him to try to form a government"),
    (22, "Freezer hack", "cyber-attack hits shops in seven countries"),
    (23, "Venezuela oil", "US details $12bn in revenue"),
    (24, "Malaysia", "eases rare-earth curbs for France"),
    (25, "Apple Pay", "iCloud and App Store outage"),
    (26, "Senegal", "first team into AFCON 2027"),
    (27, "SAFF final", "India beat Pakistan 2-1, 10th title"),
    (28, "COP31", "$20m plan for heat and cooling"),
    (29, "Nigeria", "Obasanjo criticises Tinubu over subsidy"),
    (30, "Hormuz mines", "tanker hit; 1 missing, 11 hurt"),
    (31, "San Francisco", "data-centre freeze extended 10 months"),
    (32, "Gold", "holds near a one-year low"),
    (33, "Kyiv", "US scolds it over deep strikes; talks go on"),
    (34, "Gaza", "NGO, 1,100 child amputees blocked from care"),
    (35, "Ebola", "DRC: WHO counts 11,000 cases, 5,400 dead"),
    (36, "Morocco", "beat Niger 1-0 to reach AFCON 2027"),
    (37, "COP31", "ministers weigh a divided draft in Antalya"),
    (38, "FIFA", "France's Diallo to challenge Infantino"),
    (39, "Manila", "Trump hails 'biggest' trade deal; nothing signed"),
    (40, "Japan", "Takaichi makes first China visit as PM; no talks"),
    (41, "Kemerovo", "19 die as An-12 crashes in Siberia"),
    (42, "Riyadh", "coalition downs Houthi missile; 60 targets hit"),
    (43, "Ottawa", "Carney and Xi agree tariff relief on C$400m"),
    (44, "Bogota", "Colombia's economy shrinks 0.8% in Q3"),
    (45, "Maputo", "Mondlane trial, day two; defence seeks acquittal"),
    (46, "New York", "Anthropic prices IPO at $83, above range"),
]

STATS = [
    ("25.9bn km", "Voyager 1, one light-day out"),
    ("251\u201311", "Jeffries' vote for Speaker"),
    ("141", "Drones fired at Ukraine"),
    ("200,000", "Odisha moves off the coast"),
]

PINS = {
    1: (114.1, 22.5), 2: (50.6, 26.2), 4: (30.5, 50.4), 5: (-77.0, 38.9),
    6: (85.8, 20.2), 7: (30.2, 13.2), 8: (4.4, 50.8), 9: (34.4, 31.5),
    10: (-77.0, 38.9), 11: (174.8, -36.8),
}
DOTS = {
    12: (-0.1, 51.5), 13: (34.4, 31.5), 14: (147.0, -6.7), 15: (72.8, 19.1),
    16: (-77.0, 38.9), 17: (4.3, 52.1), 18: (-160.0, -21.0), 19: (2.3, 48.9),
    20: (34.8, 32.1), 21: (10.0, 50.0), 22: (-66.9, 10.5), 23: (101.7, 3.1),
    24: (-122.0, 37.3), 25: (-17.4, 14.7), 26: (77.2, 28.6), 27: (30.7, 36.9),
    28: (7.5, 9.1), 29: (56.3, 26.6), 30: (-122.4, 37.8), 31: (-75.7, 45.4),
    32: (-0.1, 51.5), 33: (30.5, 50.4), 34: (34.4, 31.5), 35: (15.3, -4.3),
    36: (-6.8, 34.0), 37: (30.7, 36.9), 38: (2.3, 48.9), 39: (121.0, 14.6),
    40: (139.7, 35.7), 41: (86.1, 55.4), 42: (46.7, 24.7), 43: (-75.7, 45.4),
    44: (-74.1, 4.7), 45: (32.6, -25.9), 46: (-74.0, 40.7),
}

PROBLEMS = []


def wrap(d, text, fnt, width, max_lines=None):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        PROBLEMS.append("TRUNCATED (%d lines): %s" % (len(lines), text))
        lines = lines[:max_lines]
    return lines


def cover(im, w, h):
    """Centre-crop to the target aspect, then resize (no distortion)."""
    iw, ih = im.size
    ta = w / h
    ia = iw / ih
    if ia > ta:
        nw = int(ih * ta)
        x0 = (iw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / ta)
        y0 = (ih - nh) // 2
        im = im.crop((0, y0, iw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)


def pill(d, x, y, text, fg=INK, bg=YELLOW, fnt=F_LABEL, pad=4):
    lines = text.split(" / ") if " / " in text else [text]
    w = max(int(d.textlength(ln, font=fnt)) for ln in lines) + pad * 2
    h = len(lines) * 13 + pad * 2 - 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    for i, ln in enumerate(lines):
        d.text((x + pad, y + pad + i * 13 - 1), ln, font=fnt, fill=fg)
    return w, h


# pixel nudges so clustered pins stay readable (map is small)
PIN_OFF = {2: (-8, -8), 4: (8, -10), 5: (-8, 4), 8: (-10, -6), 9: (10, 10),
           10: (16, -10)}


def draw_map(d, x0, y0, mw, mh):
    with open(os.path.join(HERE, "world.geo.json")) as f:
        gj = json.load(f)
    mask = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(mask)
    polys = []
    for feat in gj["features"]:
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            polys.append(geom["coordinates"])
        elif geom["type"] == "MultiPolygon":
            polys.extend(geom["coordinates"])
    for poly in polys:
        for ring in poly:
            pts = []
            for lon, lat in ring:
                px = (lon + 180.0) / 360.0 * mw
                py = (90.0 - lat) / 180.0 * mh
                pts.append((px, py))
            md.polygon(pts, fill=255)
    step = 4
    for gy in range(0, mh, step):
        for gx in range(0, mw, step):
            if mask.getpixel((gx, gy)):
                d.ellipse([x0 + gx - 1, y0 + gy - 1, x0 + gx + 1, y0 + gy + 1],
                          fill=(150, 140, 120))

    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * mw,
                y0 + (90.0 - lat) / 180.0 * mh)

    for n, (lon, lat) in DOTS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=NAVY)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        dx, dy = PIN_OFF.get(n, (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline="white")
        t = str(n)
        tw = d.textlength(t, font=F_LABEL)
        d.text((px - tw / 2, py - 6), t, font=F_LABEL, fill="white")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    A = os.path.join(HERE, "assets")

    # ---- masthead 0-88 ----
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([12, 8, 86, 80], fill=RED)
    d.text((49, 12), "NOV", font=F_DATE2, fill="white", anchor="ma")
    d.text((49, 26), "18", font=F_DATE, fill="white", anchor="ma")
    d.text((49, 60), "WED \u00b7 2026", font=F_DATE2, fill="white", anchor="ma")
    d.text((98, 9), "THE DAY IN WORLD NEWS", font=F_EYE, fill=GOLD)
    d.text((98, 26), "Wednesday 18 November 2026", font=F_TITLE, fill="white")
    d.text((98, 70), "Everything on this page happened, or was first reported, "
           "on Wednesday 18 November 2026.", font=F_SUB, fill=(210, 210, 210))
    d.text((1012, 11), "46 STORIES \u00b7 7 REGIONS \u00b7 ONE PAGE",
           font=F_EYE, fill="white", anchor="ra")
    d.rectangle([0, 88, W, 91], fill=GOLD)

    # ---- region strip 92-111 ----
    x = 12
    segw = (W - 24) / 7.0
    for name, count, col in REGIONS:
        d.rectangle([x, 92, x + segw - 2, 111], fill=col)
        d.text((x + segw / 2 - 1, 97), "%s %d" % (name, count),
               font=F_REG, fill="white", anchor="ma")
        x += segw

    # ---- UTC timeline 114-154 ----
    d.rectangle([12, 114, 100, 154], fill=RED)
    d.text((56, 122), "THE DAY", font=F_TTIME, fill="white", anchor="ma")
    d.text((56, 136), "IN UTC", font=F_TTIME, fill="white", anchor="ma")
    bx = 104
    bw = (W - 12 - bx) / 8.0
    for i, (t, txt) in enumerate(TIMELINE):
        cx = bx + i * bw
        if i > 0:
            d.line([cx, 116, cx, 152], fill=RULE, width=1)
        d.text((cx + 5, 116), t, font=F_TTIME, fill=NAVY)
        lines = wrap(d, txt, F_TTEXT, bw - 10, max_lines=2)
        for j, ln in enumerate(lines):
            d.text((cx + 5, 130 + j * 11), ln, font=F_TTEXT, fill=INK)
    d.line([12, 156, W - 12, 156], fill=RULE, width=1)

    # ---- heroes 160-342 ----
    hy = 160
    hw = 328
    for i, (num, reg, topic, src, head, deck, label, fn) in enumerate(FRONT[:3]):
        cx = 12 + i * (hw + 8)
        im = cover(Image.open(os.path.join(A, fn)).convert("RGB"), hw, 96)
        img.paste(im, (cx, hy))
        pill(d, cx + 5, hy + 5, label)
        d.rectangle([cx, hy + 96, cx + hw, hy + 112], fill=NAVY)
        d.text((cx + 5, hy + 100), "%d  %s \u00b7 %s" % (num, reg, topic),
               font=F_KICK, fill="white")
        sw = d.textlength(src, font=F_SRC)
        d.text((cx + hw - 5 - sw, hy + 101), src, font=F_SRC, fill=GOLD)
        lines = wrap(d, head, F_HEAD, hw - 6, max_lines=2)
        for j, ln in enumerate(lines):
            d.text((cx + 3, hy + 116 + j * 20), ln, font=F_HEAD, fill=INK)
        dlines = wrap(d, deck, F_DECK, hw - 6, max_lines=2)
        for j, ln in enumerate(dlines):
            d.text((cx + 3, hy + 116 + len(lines) * 20 + 2 + j * 13),
                   ln, font=F_DECK, fill=(60, 60, 60))

    # ---- smalls 348-674 (2 rows x 4, image 244x84) ----
    sw_ = 244
    for r in range(2):
        for c in range(4):
            k = 3 + r * 4 + c
            num, reg, topic, src, head, deck, label, fn = FRONT[k]
            cx = 12 + c * (sw_ + 8)
            cy = 348 + r * 166
            im = cover(Image.open(os.path.join(A, fn)).convert("RGB"), sw_, 84)
            img.paste(im, (cx, cy))
            pill(d, cx + 4, cy + 4, label)
            d.rectangle([cx, cy + 84, cx + sw_, cy + 99], fill=NAVY)
            d.text((cx + 4, cy + 87), "%d  %s \u00b7 %s" % (num, reg, topic),
                   font=F_KICK, fill="white")
            swd = d.textlength(src, font=F_SRC)
            d.text((cx + sw_ - 4 - swd, cy + 88), src, font=F_SRC, fill=GOLD)
            lines = wrap(d, head, F_HEAD_S, sw_ - 4, max_lines=2)
            for j, ln in enumerate(lines):
                d.text((cx + 2, cy + 102 + j * 17), ln, font=F_HEAD_S, fill=INK)
            dlines = wrap(d, deck, F_DECK_S, sw_ - 4, max_lines=2)
            for j, ln in enumerate(dlines):
                d.text((cx + 2, cy + 102 + len(lines) * 17 + 1 + j * 12),
                       ln, font=F_DECK_S, fill=(60, 60, 60))

    # ---- map + also 680-926 ----
    my = 680
    d.text((12, my), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
    d.line([12, my + 16, 300, my + 16], fill=INK, width=1)
    draw_map(d, 12, my + 22, 288, 140)
    d.text((12, my + 164), "3 \u2192 to Voyager 1", font=F_TTEXT, fill=GREY)
    # stats 2x2 grid under map
    for si, (val, cap) in enumerate(STATS):
        sx = 12 + (si % 2) * 146
        sy = my + 180 + (si // 2) * 34
        d.text((sx, sy), val, font=F_STAT, fill=NAVY)
        clines = wrap(d, cap, F_STATC, 140, max_lines=2)
        for j, ln in enumerate(clines):
            d.text((sx, sy + 22 + j * 10), ln, font=F_STATC, fill=GREY)

    ax = 316
    d.text((ax, my), "ALSO ON WEDNESDAY 18 NOVEMBER", font=F_SEC, fill=INK)
    d.text((1012, my), "35 MORE STORIES", font=F_SEC, fill=INK, anchor="ra")
    d.line([ax, my + 16, 1012, my + 16], fill=INK, width=1)
    colw = 344
    rows = 18
    for i, (num, city, txt) in enumerate(ALSO):
        col = 0 if i < rows else 1
        row = i if i < rows else i - rows
        x = ax + col * (colw + 8)
        y = my + 22 + row * 12
        d.text((x, y), "%d" % num, font=F_ALSO_N, fill=RED)
        full = "%s: %s" % (city, txt)
        lines = wrap(d, full, F_ALSO, colw - 22, max_lines=1)
        d.text((x + 20, y), lines[0] if lines else "", font=F_ALSO, fill=INK)

    # ---- date check 932-972 ----
    dy = 932
    d.rectangle([12, dy, 1012, dy + 40], outline=RED, width=2)
    chk = ("DATE CHECK \u2014 Left out, first reported Tuesday 17 November: Nvidia's results \u00b7 "
           "the Dow's 849-point fall \u00b7 the Knesset speaker vote \u00b7 the Kerch Bridge collapse \u00b7 "
           "the Board of Peace's Gaza report \u00b7 Mongolia's president's offer to quit \u00b7 "
           "the AP's Alaska Senate call. Not yet news on Wednesday: the Trump\u2013Xi\u2013Putin summit "
           "(Thu 19 Nov) \u00b7 Cyclone Akvan's landfall (Fri 20 Nov). Claims are attributed to "
           "whoever made them.")
    clines = wrap(d, chk, F_DATECHK, 976, max_lines=3)
    for j, ln in enumerate(clines):
        d.text((20, dy + 3 + j * 12), ln, font=F_DATECHK, fill=INK)

    # ---- footer 978-1004 ----
    fy = 978
    d.text((512, fy), "Reads at three sizes: the date and 3 leads at thumbnail size \u00b7 "
           "11 pictures at half size \u00b7 all 46 stories at full size.",
           font=F_FOOT, fill=GREY, anchor="ma")
    d.text((512, fy + 13), "Pins 1\u201311, dots 12\u201346. Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 CNN \u00b7 CNBC \u00b7 "
           "NPR \u00b7 CBS \u00b7 Fed \u00b7 ONS \u00b7 IMD \u00b7 NASA \u00b7 Amnesty. Original illustrations.",
           font=F_FOOT, fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out)
    print("saved", out, os.path.getsize(out), "bytes")
    if PROBLEMS:
        print("PROBLEMS:")
        for p in PROBLEMS:
            print(" -", p)
    else:
        print("no truncation")


if __name__ == "__main__":
    main()
