#!/usr/bin/env python3
"""Render the news-image-20261124 broadsheet: 1024x1024 PNG, PIL only.

Dense one-day broadsheet for Tuesday 24 November 2026 (early edition):
masthead, lead story, two minis, first-reported UTC timeline strip,
8 sections x 4 stories, markets ticker, visible DATE CHECK line.
All 35 stories were first reported 24 Nov 2026. No network access.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (25, 25, 25)
MUTED = (90, 84, 70)
RED = (158, 27, 27)
NAVY = (30, 58, 95)
RULE = (25, 25, 25)
LIGHT_LINE = (190, 182, 164)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SERIF = F + "DejaVuSerif.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(draw, text, fnt, width, max_lines):
    lines = wrap(draw, text, fnt, width)
    assert len(lines) <= max_lines, f"OVERFLOW ({len(lines)}>{max_lines}): {text!r}"
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

LEAD = ("Anthropic launches Claude Ship, an AI that reviews, fixes "
        "and approves code",
        "Claude can now review, fix and approve pull requests; PR Steward "
        "and Claude Approvals launch in beta today. (The Verge)")

MINIS = [
    ("Schumer vows probe into possible wrongdoing behind Nvidia's "
     "reinstatement of Huang",
     "Senate Democratic leader says he will investigate possible illegal "
     "conduct behind the CEO's return. (UDN)"),
    ("Appeals court gives Trump a path to erasing hush-money conviction",
     "Case moves to federal court, where Trump can seek dismissal on "
     "immunity grounds. (PBS)"),
]

TIMELINE = [
    ("00:15", "V4 leaders dismiss EU budget cut"),
    ("00:18", "Suspected DPRK jet breached S. Korea airspace"),
    ("00:33", "US to blacklist AI firm Megaspeed"),
    ("01:10", "Israeli strike on Gaza City kills three"),
    ("01:21", "Lion on the loose near Istanbul"),
    ("02:35", "De Bruyne: feelings for Man City unchanged"),
]

SECTIONS = [
    ("WORLD", (30, 58, 95), [
        ("US to blacklist AI firm Megaspeed",
         "US firms would need a licence. (TechCrunch)"),
        ("Senate panel probes Vance role in Venezuela oil deal",
         "Did the VP play a role? (Japan Today)"),
        ("Colombian gangs hit forces with rockets, drones",
         "Homemade rockets hit police, army. (WSJ)"),
        ("Trump urges faster federal executions, hits Newsom",
         "Calls to 'expedite' executions. (Newsmriti)"),
    ]),
    ("EUROPE", (31, 77, 46), [
        ("Denmark top court backs hardline 'ghetto law'",
         "Court upholds tough housing rules. (DW)"),
        ("V4 leaders dismiss EU budget cut, urge ETS delay",
         "Rejects funding cut, seeks ETS delay. (Digest)"),
        ("Lion on the loose near Istanbul; search under way",
         "Large-scale search after lion report. (Digest)"),
        ("Vienna talks go on; ECB policymakers to speak",
         "Conference continues through today. (KIMKJ)"),
    ]),
    ("MIDDLE EAST", (122, 31, 31), [
        ("Israeli strike on Gaza City kills at least three",
         "UNRWA staffer killed, three hurt. (Digest)"),
        ("Turkey and Egypt discuss ties, de-escalation",
         "Leaders talk by phone on links. (Digest)"),
        ("Iran threatens European sites with 4,500 km missiles",
         "Tehran: rockets can reach Europe. (Digest)"),
        ("Indonesia weighs Mecca Accord security pact",
         "Jakarta debates a fresh approach. (Digest)"),
    ]),
    ("ASIA & INDIA", (107, 58, 10), [
        ("Suspected N. Korean jet breached S. Korean airspace",
         "DPRK jet violated airspace: Seoul. (Digest)"),
        ("Taiwan candidate probed over 20,000 photos 'for China'",
         "TPP hopeful 'collected photos'. (LTN)"),
        ("Congress, SP open seat-sharing talks for UP polls",
         "Meeting opens discussions. (Newsmriti)"),
        ("Activist says he was stopped at Delhi airport",
         "Barred from UK flight, he says. (Newsmriti)"),
    ]),
    ("TECH", (20, 61, 89), [
        ("Google pledges $5m for AI research at IIT Kharagpur",
         "Funds AI research at IIT. (Jagran Josh)"),
        ("US curbs on China reshape academic science race",
         "158 bills since 2018; 24 became law. (SCMP)"),
        ("India's back office aims to be deep-tech powerhouse",
         "Back office turns to deep tech. (Newsmriti)"),
        ("Black Friday streaming deals from $2 a month",
         "HBO Max, Apple TV+, Roku cut prices. (CNET)"),
    ]),
    ("SCIENCE & SPACE", (61, 44, 90), [
        ("Supermoon meets the Seven Sisters tonight",
         "Supermoon lines up with Pleiades. (CNET)"),
        ("Cold front brings three days of rain to Taiwan",
         "Gusts of force 8 possible. (ETtoday)"),
        ("Drought pushes millions in Afghanistan to despair",
         "Severe drought deepens crisis. (Digest)"),
        ("Germany to adopt Kyiv's Delta battlefield tool",
         "Berlin to use Ukraine's Delta. (Digest)"),
    ]),
    ("CULTURE", (90, 44, 77), [
        ("Felton invites freed Ukrainian Marine to Potter studio",
         "Hosts a Marine freed from captivity. (Digest)"),
        ("7 cool cars we'd rock in GTA VI",
         "Hagerty picks rides for the game. (Hagerty)"),
        ("US vs China mahjong rivalry stirs controversy",
         "Cross-Pacific rivalry heats up. (Newsmriti)"),
        ("FIFA picks hosts for 2031, 2035 Women's World Cups",
         "Congress selects next two hosts. (Newsmriti)"),
    ]),
    ("SPORT", (20, 83, 45), [
        ("Gukesh vs Sindarov: chess title fight begins in Geneva",
         "Gukesh defends his crown. (Sportstar)"),
        ("De Bruyne: feelings for Man City 'will never change'",
         "Speaks before facing old club. (BBC)"),
        ("Hosting World Cup 'a decade of excitement' — Weir",
         "Weir on what hosting would mean. (BBC)"),
        ("Ovechkin hosts children battling cancer at Capitals rink",
         "Young patients get a special day. (TOI)"),
    ]),
]

TICKER = ("MARKETS — MON 23 NOV CLOSES:  NVDA $165.05 +31.5% (+$952bn)  •  NASDAQ +6.5%  •  "
          "S&P +4.7%  •  DOW +1,448  •  BRENT $89.37  •  WTI $80.17  •  GOLD $3,661 +2.9%  •  "
          "TSMC ADR +14.0%  •  DOLLAR 104.31  •  TWSE margin ratio to 120% today")

DATECHECK = [
    "DATE CHECK — Every story above was first reported TUESDAY 24 NOVEMBER 2026. Sources: The Verge, "
    "TechCrunch, WSJ, PBS, BBC, SCMP, CNET, Hagerty, LTN, UDN, ETtoday, Sportstar, Newsmriti, Jagran Josh, "
    "KIMKJ, NationPress, wire digests 00:14–01:21 UTC.",
    "EXCLUDED as first reported 23 Nov or earlier: Libya corvette, Sparta II, Kyiv strikes, COP31, Banten factory "
    "fire, Lisbon protests, Nvidia/Huang return, DOJ Binance $1.1bn, space-nuke reports, CrowdStrike–Zscaler, UK "
    "Myanmar sanctions, NATO AWACS, Godhra bail, Saryu-Kamala Express.",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin
    cw = W - 2 * mx  # 968

    # ---- Masthead ----
    y = 22
    d.line([(mx, y), (mx + cw, y)], fill=RULE, width=3)
    y += 10
    title_f = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=title_f)) / 2, y), title,
           font=title_f, fill=INK)
    y += 72
    date_f = font(SANS_B, 33)
    date = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, y), date,
           font=date_f, fill=RED)
    y += 42
    sub_f = font(SANS_B, 14)
    sub = "EARLY EDITION  •  00:40 UTC  •  35 STORIES  •  ALL FIRST REPORTED TODAY"
    d.text(((W - d.textlength(sub, font=sub_f)) / 2, y), sub,
           font=sub_f, fill=NAVY)
    y += 22
    d.line([(mx, y), (mx + cw, y)], fill=RULE, width=2)
    y += 8

    # ---- Lead ----
    kick_f = font(SANS_B, 13)
    d.text((mx, y), "LEAD", font=kick_f, fill=RED)
    y += 18
    lead_f = font(SERIF_B, 29)
    lines = fit_lines(d, LEAD[0], lead_f, cw, 2)
    y = draw_lines(d, lines, mx, y, lead_f, INK, 34)
    sum_f = font(SANS, 15)
    lines = fit_lines(d, LEAD[1], sum_f, cw, 2)
    y = draw_lines(d, lines, mx, y + 2, sum_f, MUTED, 19)
    y += 8
    d.line([(mx, y), (mx + cw, y)], fill=LIGHT_LINE, width=1)
    y += 8

    # ---- Two minis ----
    mini_w = (cw - 16) // 2
    mini_top = y
    mini_bottom = mini_top
    for i, (h, s) in enumerate(MINIS):
        x = mx + i * (mini_w + 16)
        yy = mini_top
        d.text((x, yy), "MINI", font=kick_f, fill=RED)
        yy += 17
        hf = font(SANS_B, 15)
        lines = fit_lines(d, h, hf, mini_w, 2)
        yy = draw_lines(d, lines, x, yy, hf, INK, 18)
        sf = font(SANS, 12)
        lines = fit_lines(d, s, sf, mini_w, 2)
        yy = draw_lines(d, lines, x, yy + 1, sf, MUTED, 15)
        mini_bottom = max(mini_bottom, yy)
    d.line([(mx + mini_w + 8, mini_top), (mx + mini_w + 8, mini_bottom)],
           fill=LIGHT_LINE, width=1)
    y = mini_bottom + 8
    d.line([(mx, y), (mx + cw, y)], fill=RULE, width=2)
    y += 8

    # ---- Timeline strip ----
    tl_f = font(SANS_B, 12)
    label = "FIRST REPORTED — UTC  •  24 NOV"
    d.text((mx, y), label, font=tl_f, fill=NAVY)
    y += 17
    ttime_f = font(SANS_B, 12)
    ttext_f = font(SANS, 12)
    row_h = 16
    for r in range(2):
        yy = y + r * row_h
        for c in range(3):
            t, txt = TIMELINE[r * 3 + c]
            x = mx + c * (cw // 3)
            d.text((x, yy), t, font=ttime_f, fill=RED)
            tw = d.textlength(t, font=ttime_f)
            d.text((x + tw + 6, yy), txt, font=ttext_f, fill=INK)
    y += 2 * row_h + 6
    d.line([(mx, y), (mx + cw, y)], fill=RULE, width=2)
    y += 8

    # ---- Grid: 4 cols x 2 rows of sections ----
    grid_top = y
    gap = 8
    box_w = (cw - 3 * gap) // 4
    box_h = 214
    row_gap = 8
    lab_f = font(SANS_B, 13)
    head_f = font(SANS_B, 12)
    summ_f = font(SANS, 10)
    for idx, (name, color, stories) in enumerate(SECTIONS):
        r, c = divmod(idx, 4)
        x = mx + c * (box_w + gap)
        yy = grid_top + r * (box_h + row_gap)
        d.rectangle([x, yy, x + box_w, yy + 20], fill=color)
        d.text((x + 6, yy + 3), name, font=lab_f, fill=(255, 255, 255))
        yy += 26
        for h, s in stories:
            lines = fit_lines(d, h, head_f, box_w - 4, 2)
            yy = draw_lines(d, lines, x + 2, yy, head_f, INK, 14)
            lines = fit_lines(d, s, summ_f, box_w - 4, 2)
            yy = draw_lines(d, lines, x + 2, yy, summ_f, MUTED, 12)
            yy += 5
        assert yy <= grid_top + r * (box_h + row_gap) + box_h, \
            f"section {name} overflows box"
    y = grid_top + 2 * box_h + row_gap + 8

    # ---- Ticker ----
    tick_f = font(SANS_B, 12)
    lines = fit_lines(d, TICKER, tick_f, cw, 2)
    y = draw_lines(d, lines, mx, y, tick_f, NAVY, 15)
    y += 6
    d.line([(mx, y), (mx + cw, y)], fill=RULE, width=2)
    y += 7

    # ---- Date check ----
    dc_f = font(SANS_B, 11)
    for line in DATECHECK:
        lines = fit_lines(d, line, dc_f, cw, 3)
        y = draw_lines(d, lines, mx, y, dc_f, INK, 14)
    y += 6
    assert y <= H - 12, f"page overflow: content ends at y={y}"
    d.line([(mx, H - 10), (mx + cw, H - 10)], fill=RULE, width=2)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
