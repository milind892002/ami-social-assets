"""Oct 18 2026 ultrasound prep, v2: illustrated visuals (no stock photos).

    python3 tools/custom/ultrasound_prep_v2.py --preview   # preview/<slug>/ + sheet.jpg
    python3 tools/custom/ultrasound_prep_v2.py             # imports/<slug>/ for Canva import

Illustrations are drawn here as SVG and rasterised to PNG (Canva keeps PNGs exactly);
all words stay as live HTML text so they stay editable in Canva.
"""
import math, pathlib, random, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from build_post import head, render, BASE_URL, ROOT  # noqa: E402

SLUG = "2026-10-18-ultrasound-prep-v2"
PREVIEW = "--preview" in sys.argv
OUT = ROOT / ("preview" if PREVIEW else "imports") / SLUG
IMG = "img/" if PREVIEW else f"{BASE_URL}{SLUG}/img/"

NAVY, CARD, LIGHT, INK = "#0B2440", "#12355C", "#F2F6FB", "#0B2440"
ACC, ACC_D, BODY, MUTED, DIV = "#1D5FA6", "#9CC6F0", "#3D5674", "#52698A", "#CBDCEE"
ON_D = "#D6E4F3"
# prep colour key: amber = fast, aqua = full bladder, green = no prep
AMB, AMB_D = "#F5A623", "#9A5B00"
AQU, AQU_D = "#2BB3C0", "#0B6F78"
GRN, GRN_D = "#34B37A", "#1C7A4F"
H = "font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif"
B = "font-family: 'DM Sans', 'Helvetica Neue', Arial, sans-serif"

ART = {}  # name -> (svg, w, h)


def art(name, w, h, body):
    ART[name] = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>', w, h)
    return f'<img src="{IMG}{name}.png" width="{w}" height="{h}" alt="" style="display: block; width: {w}px; height: {h}px">'


# ---------- illustrations ----------
def probe(x, y, s=1.0, ang=0, body="#E8F0F9", head_c="#9CC6F0", line="#0B2440"):
    """Ultrasound transducer; (x, y) is the centre of the scanning face, pointing down."""
    return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">'
            f'<path d="M-30 -330 C -60 -230 -70 -150 -80 -70 L 80 -70 C 70 -150 60 -230 30 -330 Z" fill="{body}"/>'
            f'<path d="M-92 -70 L 92 -70 C 100 -40 96 -12 84 0 L -84 0 C -96 -12 -100 -40 -92 -70 Z" fill="{head_c}"/>'
            f'<rect x="-84" y="-6" width="168" height="14" rx="7" fill="{line}" opacity="0.85"/>'
            f'<path d="M-52 -250 H 52 M-58 -215 H 58 M-62 -180 H 62" stroke="{line}" stroke-opacity="0.18" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M0 -330 C 0 -420 150 -420 230 -500 S 330 -680 300 -800" fill="none" stroke="{body}" stroke-width="22" stroke-linecap="round"/>'
            '</g>')


def sector(cx, cy, r0, r1, a0, a1, seed=7, bg="#081A30", grain=("#9CC6F0", "#D6E4F3", "#5E86B3")):
    """Ultrasound 'fan' image: apex at (cx, cy), angles in degrees from straight down."""
    rnd = random.Random(seed)
    def pt(r, a):
        t = math.radians(90 + a)
        return cx + r * math.cos(t), cy + r * math.sin(t)
    p0, p1, p2, p3 = pt(r0, a0), pt(r0, a1), pt(r1, a1), pt(r1, a0)
    clip = (f'M{p0[0]:.1f} {p0[1]:.1f} A {r0} {r0} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} L {p2[0]:.1f} {p2[1]:.1f} '
            f'A {r1} {r1} 0 0 0 {p3[0]:.1f} {p3[1]:.1f} Z')
    dots = []
    for _ in range(2600):
        r = rnd.uniform(r0, r1); a = rnd.uniform(a0, a1)
        x, y = pt(r, a)
        depth = (r - r0) / (r1 - r0)
        op = rnd.uniform(0.15, 0.75) * (1 - 0.55 * depth)
        rx = rnd.uniform(2, 9); ry = rx * rnd.uniform(0.25, 0.5)
        rot = a
        dots.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({rot:.0f} {x:.1f} {y:.1f})" '
                    f'fill="{rnd.choice(grain)}" opacity="{op:.2f}"/>')
    # bright tissue bands
    bands = []
    for rr, w, op in ((r0 + 70, 10, 0.55), (r0 + 150, 6, 0.35), (r0 + 330, 8, 0.4)):
        b0, b1 = pt(rr, a0 + 4), pt(rr, a1 - 4)
        bands.append(f'<path d="M{b0[0]:.1f} {b0[1]:.1f} A {rr} {rr} 0 0 1 {b1[0]:.1f} {b1[1]:.1f}" fill="none" stroke="#D6E4F3" stroke-width="{w}" opacity="{op}" stroke-linecap="round"/>')
    # dark fluid-filled 'organ'
    ox, oy = pt(r0 + (r1 - r0) * 0.55, (a0 + a1) / 2 + 6)
    organ = (f'<ellipse cx="{ox:.0f}" cy="{oy:.0f}" rx="{(r1-r0)*0.16:.0f}" ry="{(r1-r0)*0.09:.0f}" fill="#061426" opacity="0.85" stroke="#D6E4F3" stroke-opacity="0.35" stroke-width="4"/>')
    return (f'<defs><clipPath id="fan{seed}"><path d="{clip}"/></clipPath></defs>'
            f'<path d="{clip}" fill="{bg}"/>'
            f'<g clip-path="url(#fan{seed})">{"".join(dots)}{"".join(bands)}{organ}</g>'
            f'<path d="{clip}" fill="none" stroke="#9CC6F0" stroke-opacity="0.35" stroke-width="3"/>')


def waves(cx, cy, radii, a0, a1, color, widths=None):
    out = []
    for i, r in enumerate(radii):
        t0, t1 = math.radians(90 + a0), math.radians(90 + a1)
        x0, y0 = cx + r * math.cos(t0), cy + r * math.sin(t0)
        x1, y1 = cx + r * math.cos(t1), cy + r * math.sin(t1)
        w = widths[i] if widths else 8
        out.append(f'<path d="M{x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{color}" '
                   f'stroke-width="{w}" stroke-linecap="round" opacity="{1 - i * 0.18:.2f}"/>')
    return "".join(out)


def clock(cx, cy, r, frac_from, frac_to, color, face="#FFFFFF", ring="#0B2440"):
    """Clock face with a highlighted arc from frac_from to frac_to (0..1 of 12 h)."""
    def p(f, rr):
        t = math.radians(-90 + 360 * f)
        return cx + rr * math.cos(t), cy + rr * math.sin(t)
    a, b = p(frac_from, r * 0.78), p(frac_to, r * 0.78)
    large = 1 if (frac_to - frac_from) > 0.5 else 0
    ticks = "".join(
        f'<line x1="{p(i/12, r*0.86)[0]:.1f}" y1="{p(i/12, r*0.86)[1]:.1f}" x2="{p(i/12, r*0.94)[0]:.1f}" y2="{p(i/12, r*0.94)[1]:.1f}" '
        f'stroke="{ring}" stroke-width="{8 if i % 3 == 0 else 4}" stroke-linecap="round"/>' for i in range(12))
    h1, h2 = p(frac_to, r * 0.45), p(0.0, r * 0.62)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{face}" stroke="{ring}" stroke-width="12"/>'
            f'<path d="M{cx} {cy} L {a[0]:.1f} {a[1]:.1f} A {r*0.78:.1f} {r*0.78:.1f} 0 {large} 1 {b[0]:.1f} {b[1]:.1f} Z" fill="{color}" opacity="0.9"/>'
            f'{ticks}'
            f'<line x1="{cx}" y1="{cy}" x2="{h1[0]:.1f}" y2="{h1[1]:.1f}" stroke="{ring}" stroke-width="12" stroke-linecap="round"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{h2[0]:.1f}" y2="{h2[1]:.1f}" stroke="{ring}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="12" fill="{ring}"/>')


def plate(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{DIV}" stroke-width="6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.72}" fill="none" stroke="{DIV}" stroke-width="4"/>'
            # fork
            f'<g transform="translate({cx - r - 60} {cy - 150})" fill="{MUTED}">'
            f'<rect x="-6" y="0" width="12" height="300" rx="6"/><rect x="-26" y="0" width="8" height="90" rx="4"/>'
            f'<rect x="18" y="0" width="8" height="90" rx="4"/><rect x="-4" y="0" width="8" height="90" rx="4"/>'
            f'<path d="M-26 80 H 26 V 110 C 26 130 -26 130 -26 110 Z"/></g>'
            # knife
            f'<g transform="translate({cx + r + 60} {cy - 150})" fill="{MUTED}">'
            f'<path d="M-8 0 C 26 30 22 120 14 150 L -8 150 Z"/><rect x="-8" y="140" width="16" height="160" rx="8"/></g>')


def glass(x, y, w, h, fill_frac, water="#7FD3DC", outline="#0B2440"):
    top = y + h * (1 - fill_frac)
    taper = w * 0.12
    return (f'<defs><clipPath id="g{x}{y}"><path d="M{x} {y} L {x+w} {y} L {x+w-taper} {y+h} L {x+taper} {y+h} Z"/></clipPath></defs>'
            f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{water}" clip-path="url(#g{x}{y})"/>'
            f'<path d="M{x} {top} q {w/4} -14 {w/2} 0 t {w/2} 0" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.7" clip-path="url(#g{x}{y})"/>'
            f'<path d="M{x} {y} L {x+w} {y} L {x+w-taper} {y+h} L {x+taper} {y+h} Z" fill="none" stroke="{outline}" stroke-width="10" stroke-linejoin="round"/>')


def badge(cx, cy, r, color, kind):
    sym = {
        "check": f'<path d="M{cx-r*0.4} {cy+2} l {r*0.28} {r*0.3} l {r*0.55} {-r*0.6}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.2:.0f}" stroke-linecap="round" stroke-linejoin="round"/>',
        "no": f'<path d="M{cx-r*0.38} {cy-r*0.38} L {cx+r*0.38} {cy+r*0.38}" stroke="#FFFFFF" stroke-width="{r*0.2:.0f}" stroke-linecap="round"/>',
    }[kind]
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="#FFFFFF" stroke-width="{r*0.14:.0f}"/>{sym}'


def figure(cx, top, s, col="#D6E4F3"):
    """Simple, friendly, gender-neutral body silhouette."""
    def S(v): return v * s
    return (f'<g fill="{col}">'
            f'<circle cx="{cx}" cy="{top+S(70)}" r="{S(66)}"/>'
            f'<rect x="{cx-S(26)}" y="{top+S(122)}" width="{S(52)}" height="{S(50)}" rx="{S(14)}"/>'
            f'<path d="M{cx-S(150)} {top+S(210)} Q {cx-S(150)} {top+S(165)} {cx-S(100)} {top+S(162)} L {cx+S(100)} {top+S(162)} '
            f'Q {cx+S(150)} {top+S(165)} {cx+S(150)} {top+S(210)} L {cx+S(132)} {top+S(560)} Q {cx} {top+S(600)} {cx-S(132)} {top+S(560)} Z"/>'
            f'<rect x="{cx-S(205)}" y="{top+S(185)}" width="{S(56)}" height="{S(360)}" rx="{S(28)}" transform="rotate(8 {cx-S(177)} {top+S(185)})"/>'
            f'<rect x="{cx+S(149)}" y="{top+S(185)}" width="{S(56)}" height="{S(360)}" rx="{S(28)}" transform="rotate(-8 {cx+S(177)} {top+S(185)})"/>'
            f'<rect x="{cx-S(122)}" y="{top+S(540)}" width="{S(104)}" height="{S(420)}" rx="{S(46)}"/>'
            f'<rect x="{cx+S(18)}" y="{top+S(540)}" width="{S(104)}" height="{S(420)}" rx="{S(46)}"/>'
            '</g>')


def zone(x, y, r, color):
    return (f'<circle cx="{x}" cy="{y}" r="{r*1.9:.0f}" fill="{color}" opacity="0.18"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="#FFFFFF" stroke-width="6"/>')


# ---------- HTML helpers ----------
def page(label, bg, inner, w=1080, h=1350, color="#FFFFFF"):
    return (f'<div data-document-role="page" data-label="{label}" style="position: relative; width: {w}px; height: {h}px; '
            f'overflow: hidden; background: {bg}; color: {color}; {B}">{inner}</div>')


def at(x, y, inner, w=None, extra=""):
    ws = f" width: {w}px;" if w else ""
    return f'<div style="position: absolute; left: {x}px; top: {y}px;{ws} {extra}">{inner}</div>'


def wordmark(dark):
    return (f'<div style="font-size: 24px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; '
            f'color: {ACC_D if dark else ACC}">Advanced Medical Imaging</div>')


def eyebrow(t, color):
    return f'<div style="font-size: 26px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: {color}">{t}</div>'


def h(title, accent, size, color, acc_color, width, tag="h2"):
    a = f' <span style="color: {acc_color}">{accent}</span>' if accent else ""
    return (f'<{tag} style="margin: 0; width: {width}px; {H}; font-weight: 800; font-size: {size}px; line-height: 1.04; '
            f'letter-spacing: -0.015em; color: {color}">{title}{a}</{tag}>')


def p(t, size, color, width, weight=500, lh=1.35):
    return f'<p style="margin: 0; width: {width}px; font-size: {size}px; line-height: {lh}; font-weight: {weight}; color: {color}">{t}</p>'


def chip(label, color, dark):
    bg = "#12355C" if dark else "#FFFFFF"
    fg = "#FFFFFF" if dark else INK
    return (f'<div style="align-self: flex-start; display: flex; align-items: center; gap: 12px; padding: 14px 22px; border-radius: 999px; background: {bg}; '
            f'border: 2px solid {"#22466F" if dark else DIV}"><div style="width: 20px; height: 20px; border-radius: 10px; background: {color}"></div>'
            f'<span style="font-size: 26px; font-weight: 600; color: {fg}">{label}</span></div>')


def icon(kind, color, size):
    paths = {
        "arrow": '<path d="M5 12h14"></path><path d="M13 6l6 6-6 6"></path>',
        "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"></path>',
        "cal": '<rect x="3" y="4" width="18" height="18" rx="2"></rect><path d="M16 2v4M8 2v4M3 10h18"></path>',
        "send": '<path d="M22 2L11 13"></path><path d="M22 2l-7 20-4-9-9-4z"></path>',
        "bookmark": '<path d="M6 3h12v18l-6-4-6 4z"></path>',
    }
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex: none">{paths[kind]}</svg>')


def save_tag(color):
    return (f'<div style="display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 700; letter-spacing: 0.14em; '
            f'text-transform: uppercase; color: {color}">{icon("bookmark", color, 30)}<span>Save this for later</span></div>')


SRC = "Sources: RadiologyInfo.org (ACR, RSNA); NIH MedlinePlus."


# ---------- slides ----------
def s1():
    fan = sector(540, 230, 92, 600, -36, 36, seed=3)
    img = art("hook", 1080, 860,
              fan + waves(540, 230, [130, 170, 210], -27, 27, "#9CC6F0", [10, 8, 6]) + probe(540, 318, 0.62))
    chips = ('<div style="display: flex; flex-wrap: wrap; gap: 14px; width: 904px">'
             + chip("Abdomen", AMB, True) + chip("Pelvis", AQU, True) + chip("Thyroid, breast, vascular", GRN, True) + "</div>")
    inner = (at(0, 0, img) + at(88, 72, wordmark(True))
             + at(88, 850, f'<div style="display: flex; flex-direction: column; gap: 26px; width: 904px">'
                  + eyebrow("Save this before your scan", ACC_D)
                  + h("Ultrasound prep?", "Depends on the type.", 84, "#FFFFFF", ACC_D, 904, "h1") + chips + "</div>")
             + at(88, 1236, f'<div style="display: flex; align-items: center; gap: 16px; font-size: 30px; font-weight: 600; color: #FFFFFF">Swipe {icon("arrow", "#FFFFFF", 40)}</div>'))
    return page("Slide 1 Hook", NAVY, inner)


def s2():
    cx, top, s = 250, 40, 0.9
    zs = [(cx, top + 150 * s, 22, GRN), (cx - 62 * s, top + 255 * s, 22, GRN), (cx, top + 370 * s, 26, AMB),
          (cx, top + 500 * s, 26, AQU), (cx + 70 * s, top + 760 * s, 22, GRN)]
    rows_y = [150, 290, 430, 570, 760]  # label centres (same coordinate system as the art)
    lines = "".join(
        f'<path d="M{x + r + 4:.0f} {y:.0f} C {x + 140:.0f} {y:.0f} {380:.0f} {ry:.0f} {470} {ry}" fill="none" stroke="{c}" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>'
        for (x, y, r, c), ry in zip(zs, rows_y))
    img = art("bodymap", 480, 930, figure(cx, top, s) + lines + "".join(zone(x, y, r, c) for x, y, r, c in zs))
    labels = [("Thyroid", "No special prep", GRN, GRN_D), ("Breast", "No special prep", GRN, GRN_D),
              ("Abdomen", "No food for 8 to 12 hours", AMB, AMB_D), ("Pelvis", "Full bladder", AQU, AQU_D),
              ("Vascular", "No special prep", GRN, GRN_D)]
    lab = "".join(at(560, 360 + y - 46, f'<div style="font-size: 40px; font-weight: 800; {H}; color: {INK}">{t}</div>'
                     f'<div style="font-size: 28px; font-weight: 700; color: {cd}; margin-top: 4px">{sub}</div>', 440)
                  for (t, sub, c, cd), y in zip(labels, rows_y))
    inner = (at(88, 72, wordmark(False))
             + at(88, 150, f'<div style="display: flex; flex-direction: column; gap: 22px">{eyebrow("Prep by type", MUTED)}'
                  + h("Which ultrasound are you having?", None, 68, INK, ACC, 904) + "</div>")
             + at(80, 360, img) + lab
             + at(88, 1236, p("Not sure? Check your doctor&#39;s order, or ask us.", 28, MUTED, 904, 600)))
    return page("Slide 2 Body map", LIGHT, inner, color=INK)


def s3():
    body = (plate(310, 330, 180) + clock(800, 200, 140, 0, 0.75, AMB)
            + glass(810, 390, 120, 190, 0.7) + badge(925, 395, 36, GRN, "check"))
    img = art("abdomen", 1080, 620, body)
    inner = (at(0, 120, img) + at(88, 72, wordmark(False))
             + at(88, 790, f'<div style="display: flex; flex-direction: column; gap: 24px">'
                  + chip("Abdomen", AMB, False)
                  + h("No food for 8 to 12 hours before.", None, 76, INK, ACC, 904)
                  + p("Water is OK.", 34, BODY, 904) + "</div>")
             + at(88, 1236, p("Your doctor or our team may give you different instructions.", 26, MUTED, 904)))
    return page("Slide 3 Abdomen", LIGHT, inner, color=INK)


def s4():
    # 32 oz as four 8 oz glasses + 1-hour clock
    gl = "".join(glass(110 + i * 165, 250, 120, 230, 0.82, water="#7FD3DC", outline="#FFFFFF") for i in range(4))
    body = gl + clock(870, 360, 130, 0, 1 / 12, AQU, face="#12355C", ring="#FFFFFF")
    img = art("pelvis", 1080, 600, body)
    marks = "".join(at(110 + i * 165, 710, f'<div style="width: 120px; text-align: center; font-size: 28px; font-weight: 700; color: {ACC_D}">8 oz</div>') for i in range(4))
    inner = (at(0, 120, img) + marks + at(88, 72, wordmark(True))
             + at(800, 710, f'<div style="width: 140px; text-align: center; font-size: 28px; font-weight: 700; color: {ACC_D}">1 hr before</div>')
             + at(88, 800, f'<div style="display: flex; flex-direction: column; gap: 24px">'
                  + chip("Pelvis", AQU, True)
                  + h("Drink 32 oz of water 1&nbsp;hour before.", None, 76, "#FFFFFF", ACC_D, 904)
                  + p("And don&#39;t empty your bladder. A full bladder gives us a clearer view.", 34, ON_D, 904) + "</div>"))
    return page("Slide 4 Pelvis", NAVY, inner)


def s5():
    tiles = [("Thyroid", "neck"), ("Breast", "chest"), ("Vascular", "arms, legs, neck")]
    def tile(name, where):
        return (f'<div style="box-sizing: border-box; width: 280px; padding: 34px 28px; border-radius: 28px; background: #FFFFFF; border: 2px solid {DIV}; '
                f'display: flex; flex-direction: column; gap: 14px">'
                f'<div style="width: 64px; height: 64px; border-radius: 32px; background: {GRN}; display: flex; align-items: center; justify-content: center">'
                f'<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg></div>'
                f'<div style="{H}; font-weight: 800; font-size: 40px; color: {INK}">{name}</div>'
                f'<div style="font-size: 26px; font-weight: 600; color: {MUTED}">{where}</div></div>')
    row = '<div style="display: flex; gap: 32px">' + "".join(tile(*t) for t in tiles) + "</div>"
    shirt = art("relax", 1080, 420,
                f'<path d="M380 120 L 470 80 Q 540 130 610 80 L 700 120 L 760 230 L 690 260 L 670 220 L 670 400 L 410 400 L 410 220 L 390 260 L 320 230 Z" fill="#FFFFFF" stroke="{DIV}" stroke-width="8" stroke-linejoin="round"/>'
                f'<path d="M470 80 Q 540 150 610 80" fill="none" stroke="{DIV}" stroke-width="8"/>'
                + badge(760, 330, 50, GRN, "check")
                + f'<g transform="translate(220 250)"><circle r="56" fill="none" stroke="{MUTED}" stroke-width="10"/><circle cy="-64" r="16" fill="{MUTED}"/></g>'
                + badge(270, 300, 34, "#D9534F", "no"))
    inner = (at(88, 72, wordmark(False))
             + at(88, 150, f'<div style="display: flex; flex-direction: column; gap: 24px">{chip("No prep", GRN, False)}'
                  + h("Thyroid, breast or vascular? Just come in.", None, 72, INK, ACC, 904) + "</div>")
             + at(88, 470, row)
             + at(0, 780, shirt)
             + at(88, 1236, p("Wear loose, comfy clothes and leave jewelry at home.", 30, BODY, 904, 600)))
    return page("Slide 5 No prep", LIGHT, inner, color=INK)


def s6():
    def tile(art_html, big, small):
        return (f'<div style="width: 904px; padding: 30px 36px; border-radius: 28px; background: {CARD}; display: flex; align-items: center; gap: 36px">'
                f'{art_html}<div><div style="{H}; font-weight: 800; font-size: 54px; color: #FFFFFF">{big}</div>'
                f'<div style="font-size: 28px; font-weight: 500; color: {ON_D}; margin-top: 6px">{small}</div></div></div>')
    gel = art("gel", 150, 150, '<path d="M75 14 C 75 14 28 74 28 100 a 47 47 0 0 0 94 0 C 122 74 75 14 75 14 Z" fill="#7FD3DC"/>'
              '<path d="M52 98 a 24 24 0 0 0 20 26" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.8"/>')
    tmr = art("timer", 150, 150, clock(75, 80, 60, 0, 0.25, ACC_D, face="#0B2440", ring="#FFFFFF").replace('stroke-width="12"', 'stroke-width="7"', 1))
    rad = art("noradiation", 150, 150, f'<circle cx="75" cy="75" r="60" fill="none" stroke="{GRN}" stroke-width="10"/>'
              + waves(75, 40, [30, 50, 70], -30, 30, "#9CC6F0", [6, 6, 6])
              + f'<path d="M30 120 L 120 30" stroke="{GRN}" stroke-width="10" stroke-linecap="round"/>')
    inner = (at(88, 72, wordmark(True))
             + at(88, 150, f'<div style="display: flex; flex-direction: column; gap: 22px">{eyebrow("What to expect", ACC_D)}'
                  + h("Painless, and no radiation.", None, 76, "#FFFFFF", ACC_D, 904) + "</div>")
             + at(88, 440, '<div style="display: flex; flex-direction: column; gap: 26px">'
                  + tile(gel, "Warm gel", "A smooth probe glides over your skin. Slight pressure, no pain.")
                  + tile(tmr, "20 to 45 min", "for most exams. You may see the images on screen.")
                  + tile(rad, "0 radiation", "Just sound waves. Results to your doctor in 48 to 72 hours.") + "</div>")
             + at(88, 1236, p(SRC, 24, ACC_D, 904)))
    return page("Slide 6 What to expect", NAVY, inner)


def s7():
    deco = art("ctawaves", 1080, 520, waves(1080, -40, [180, 270, 360, 450, 540], 20, 80, "#1B3A5E", [14, 12, 10, 8, 6])
               + probe(960, 150, 0.5, ang=35, body="#22466F", head_c="#2D5C8F", line="#0B2440"))
    def btn(k, t):
        return (f'<div style="display: flex; align-items: center; gap: 22px; padding: 26px 34px; border-radius: 20px; background: {CARD}; width: 836px">'
                f'{icon(k, ACC_D, 40)}<span style="font-size: 34px; font-weight: 600; color: #FFFFFF">{t}</span></div>')
    facts = ('<div style="display: flex; flex-wrap: wrap; gap: 14px; width: 904px">'
             + chip("$195 self-pay", ACC_D, True) + chip("No referral needed", ACC_D, True) + chip("Same-day often available", ACC_D, True) + "</div>")
    inner = (at(0, 0, deco) + at(88, 72, wordmark(True))
             + at(88, 300, f'<div style="display: flex; flex-direction: column; gap: 34px">{save_tag(ACC_D)}'
                  + h("Save this for scan day.", "Book when you&#39;re ready.", 80, "#FFFFFF", ACC_D, 904) + facts + "</div>")
             + at(88, 860, '<div style="display: flex; flex-direction: column; gap: 18px">' + btn("phone", "Call (727) 398-5999")
                  + btn("cal", "Book through the link in our bio") + "</div>")
             + at(88, 1150, f'<div style="display: flex; align-items: center; gap: 16px">{icon("send", "#FFFFFF", 34)}'
                  f'<span style="font-size: 30px; font-weight: 600; color: #FFFFFF">Send this to someone with an ultrasound coming up.</span></div>')
             + at(88, 1240, p("General information, not medical advice. Coverage varies by plan.", 22, ACC_D, 904)))
    return page("Slide 7 CTA", NAVY, inner)


def gbp():
    fan = sector(300, 170, 80, 680, -36, 36, seed=11)
    img = art("gbp", 600, 900, fan + waves(300, 170, [115, 150, 185], -28, 28, "#9CC6F0", [9, 7, 5]) + probe(300, 246, 0.55))
    chips = ('<div style="display: flex; flex-wrap: wrap; gap: 12px; width: 480px">'
             + chip("Abdomen", AMB, True) + chip("Pelvis", AQU, True) + chip("No prep", GRN, True) + "</div>")
    inner = (at(600, 0, img) + at(64, 60, wordmark(True))
             + at(64, 220, f'<div style="display: flex; flex-direction: column; gap: 26px">{eyebrow("Before your ultrasound", ACC_D)}'
                  + h("Ultrasound prep?", "It varies by scan.", 58, "#FFFFFF", ACC_D, 520) + chips
                  + p("Painless, no radiation. $195 self-pay in Seminole, no referral needed.", 28, ON_D, 500) + "</div>")
             + at(64, 760, f'<div style="width: 400px; height: 76px; border-radius: 38px; background: {ACC_D}; display: flex; align-items: center; justify-content: center">'
                  f'<span style="font-size: 28px; font-weight: 700; color: {NAVY}">Book at advancedimg.com</span></div>'))
    return page("Google image", NAVY, inner, w=1200, h=900)


def rasterise():
    from playwright.sync_api import sync_playwright
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(device_scale_factor=2)
        for name, (svg, w, hgt) in ART.items():
            pg.set_viewport_size({"width": w, "height": hgt})
            pg.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
            pg.locator("svg").screenshot(path=str(OUT / "img" / f"{name}.png"), omit_background=True)
        b.close()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    slides = [s1(), s2(), s3(), s4(), s5(), s6(), s7()]
    (OUT / "carousel.html").write_text(head("Ultrasound prep (illustrated)", PREVIEW) + "\n".join(slides) + "</body></html>")
    (OUT / "gbp.html").write_text(head(SLUG + " google", PREVIEW) + gbp() + "</body></html>")
    rasterise()
    print("built", OUT)
    if PREVIEW:
        render(OUT, ["carousel.html", "gbp.html"])
    else:
        for f in ("carousel.html", "gbp.html"):
            print("import URL:", f"{BASE_URL}{SLUG}/{f}")


if __name__ == "__main__":
    main()
