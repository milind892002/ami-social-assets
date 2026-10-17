"""Oct 18 2026 ultrasound prep, v6: soft pastel, art-gallery look (arched frames, plaster-plinth still lifes).

Each slide is a saturated brand colour with a giant number, and an editorial still life shot on
a matching coloured backdrop sits in a rounded card (frames swapped in Canva with update_fill).

    python3 tools/custom/ultrasound_prep_v6.py --preview
    python3 tools/custom/ultrasound_prep_v6.py
"""
import pathlib, sys
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_post import head, render, BASE_URL, ROOT  # noqa: E402
import ultrasound_prep_v2 as v2  # noqa: E402

SLUG = "2026-10-18-ultrasound-prep-v6"
PREVIEW = "--preview" in sys.argv
OUT = ROOT / ("preview" if PREVIEW else "imports") / SLUG
IMG = "img/" if PREVIEW else f"{BASE_URL}{SLUG}/img/"
NAVY, COBALT, AMB, AQU, GRN, SUN = "#22304A", "#CFE3F3", "#F9D9C4", "#CDEBE6", "#E2D8F1", "#F8EBB8"
CREAM, DUSK = "#F6F0E6", "#5B7FB0"
H, at, icon = v2.H, v2.at, v2.icon
R = 44


def frame(name, w, hgt, x, y, tint, r=R, arch=True):
    Image.new("RGB", (w, hgt), tint).save(OUT / "img" / f"frame-{name}.png")
    rad = f"{w//2}px {w//2}px {r}px {r}px / {min(w//2, hgt//2)}px {min(w//2, hgt//2)}px {r}px {r}px" if arch else f"{r}px"
    return at(x, y, f'<img src="{IMG}frame-{name}.png" width="{w}" height="{hgt}" alt="" '
                    f'style="display: block; width: {w}px; height: {hgt}px; border-radius: {rad}">')


def txt(t, size, color, width, weight=500, lh=1.3, extra=""):
    return f'<p style="margin: 0; width: {width}px; font-size: {size}px; line-height: {lh}; font-weight: {weight}; color: {color}; {extra}">{t}</p>'


def big(t, size, color, width=904, lh=0.9):
    w = f"width: {width}px; " if width else ""
    return (f'<div style="{w}{H}; font-weight: 800; font-size: {size}px; line-height: {lh}; '
            f'letter-spacing: -0.04em; color: {color}">{t}</div>')


def tag(t, bg, fg):
    return (f'<div style="align-self: flex-start; padding: 12px 24px; border-radius: 999px; background: {bg}; '
            f'font-size: 24px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: {fg}">{t}</div>')


def mark(color):
    return f'<div style="font-size: 22px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: {color}">Advanced Medical Imaging</div>'


def footer(left, color):
    return at(88, 1256, f'<div style="display: flex; justify-content: space-between; align-items: center; width: 904px">'
                        f'<span style="font-size: 22px; font-weight: 500; color: {color}">{left}</span>{mark(color)}</div>')


def page(label, bg, inner, w=1080, hgt=1350, color="#FFFFFF"):
    return v2.page(label, bg, inner, w, hgt, color=color)


def s1():
    return page("Slide 1 Hook", CREAM,
                frame("hook", 984, 800, 48, 48, "#E3ECF5")
                + at(88, 890, '<div style="display: flex; flex-direction: column; gap: 22px">' + tag("Save this before your scan", COBALT, NAVY)
                     + v2.h("Ultrasound prep?", "Depends on the type.", 86, NAVY, DUSK, 904, "h1") + "</div>")
                + at(88, 1252, f'<div style="display: flex; justify-content: space-between; align-items: center; width: 904px">'
                     f'<div style="display: flex; align-items: center; gap: 14px; font-size: 30px; font-weight: 700; color: {NAVY}">Swipe {icon("arrow", NAVY, 38)}</div>{mark(DUSK)}</div>'), color=NAVY)


def s2():
    tiles = [("Abdomen", "8&ndash;12h", "no food before", AMB), ("Pelvis", "32 oz", "water, 1 hour before", AQU),
             ("Thyroid &amp; breast", "0", "special prep", GRN), ("Vascular", "0", "special prep", SUN)]
    def tile(name, num, sub, c):
        return (f'<div style="box-sizing: border-box; width: 440px; height: 400px; border-radius: 220px 220px {R}px {R}px / 200px 200px {R}px {R}px; background: {c}; padding: 40px; '
                f'display: flex; flex-direction: column; justify-content: flex-end">'
                f'<div style="font-size: 30px; font-weight: 700; color: {NAVY}; margin-bottom: 18px">{name}</div>'
                f'<div>{big(num, 110, NAVY, 368)}<div style="font-size: 27px; font-weight: 600; color: {NAVY}; margin-top: 10px">{sub}</div></div></div>')
    grid = '<div style="display: flex; flex-wrap: wrap; gap: 24px; width: 904px">' + "".join(tile(*t) for t in tiles) + "</div>"
    return page("Slide 2 Prep by type", CREAM,
                at(88, 96, v2.h("Which ultrasound are you having?", None, 68, NAVY, DUSK, 904))
                + at(88, 330, grid) + footer("Not sure? Check your doctor&#39;s order.", DUSK), color=NAVY)


def stat_slide(label, bg, name, tint, tagtxt, number, unit, line, sub, foot=""):
    return page(label, bg,
                frame(name, 984, 580, 48, 48, tint)
                + at(88, 670, '<div style="display: flex; flex-direction: column; gap: 18px">' + tag(tagtxt, "#FFFFFF", NAVY)
                     + f'<div style="display: flex; align-items: baseline; gap: 22px">{big(number, 220, NAVY, None)}'
                       f'<div style="{H}; font-weight: 800; font-size: 60px; color: {NAVY}; letter-spacing: -0.02em">{unit}</div></div>'
                     + txt(line, 44, NAVY, 904, 800, 1.1, H + ";")
                     + txt(sub, 30, NAVY, 904, 500) + "</div>")
                + footer(foot, NAVY), color=NAVY)


def s3():
    return stat_slide("Slide 3 Abdomen", AMB, "abd", "#F3CBB2", "Abdomen", "8&ndash;12", "hrs",
                      "No food before your abdominal ultrasound.", "Water is OK.", "Your doctor may give different instructions.")


def s4():
    return stat_slide("Slide 4 Pelvis", AQU, "pel", "#B9E0D9", "Pelvis", "32", "oz",
                      "of water, 1 hour before your pelvic ultrasound.", "And don&#39;t empty your bladder. A full bladder gives a clearer view.")


def s5():
    return stat_slide("Slide 5 No prep", GRN, "thy", "#D3C6EA", "Thyroid &middot; breast &middot; vascular", "0", "prep",
                      "Nothing special needed. Just come in.", "Wear loose, comfy clothes and leave jewelry at home.")


def s6():
    def tile(num, sub, c):
        return (f'<div style="box-sizing: border-box; width: 285px; height: 290px; border-radius: 142px 142px 40px 40px / 120px 120px 40px 40px; background: {c}; padding: 30px; '
                f'display: flex; flex-direction: column; justify-content: flex-end">'
                f'{big(num, 62, NAVY, 230, 0.95)}<div style="font-size: 25px; font-weight: 600; color: {NAVY}; margin-top: 12px">{sub}</div></div>')
    row = ('<div style="display: flex; gap: 24px">' + tile("0", "radiation. Just sound waves.", AQU)
           + tile("20&ndash;45", "minutes for most exams.", AMB) + tile("48&ndash;72h", "results to your doctor.", GRN) + "</div>")
    return page("Slide 6 What to expect", SUN,
                frame("probe", 984, 520, 48, 48, "#EFE0A6", arch=False)
                + at(88, 610, '<div style="display: flex; flex-direction: column; gap: 18px">' + tag("What to expect", "#FFFFFF", NAVY)
                     + v2.h("Warm gel, slight pressure.", "No pain.", 58, NAVY, DUSK, 760) + "</div>")
                + at(88, 880, row) + at(88, 1256, f'<span style="font-size: 22px; font-weight: 500; color: {NAVY}">{v2.SRC}</span>'), color=NAVY)


def s7():
    def btn(k, t, bg, fg):
        return (f'<div style="box-sizing: border-box; display: flex; align-items: center; gap: 22px; padding: 30px 40px; border-radius: 999px; background: {bg}; width: 904px">'
                f'{icon(k, fg, 40)}<span style="font-size: 36px; font-weight: 700; color: {fg}">{t}</span></div>')
    chips = ('<div style="display: flex; flex-wrap: wrap; gap: 14px; width: 904px">'
             + tag("$195 self-pay", AMB, NAVY) + tag("No referral needed", "#FFFFFF", NAVY) + tag("Same-day often", GRN, NAVY) + "</div>")
    return page("Slide 7 CTA", COBALT,
                at(88, 120, '<div style="display: flex; flex-direction: column; gap: 34px">'
                     + big("Save this.", 150, NAVY) + big("Book when you&#39;re ready.", 96, DUSK, 904, 1.0) + chips + "</div>")
                + at(88, 800, '<div style="display: flex; flex-direction: column; gap: 20px">'
                     + btn("phone", "Call (727) 398-5999", NAVY, "#FFFFFF") + btn("cal", "Book through the link in our bio", "#FFFFFF", NAVY) + "</div>")
                + at(88, 1080, f'<div style="display: flex; align-items: center; gap: 16px">{icon("send", NAVY, 34)}'
                     f'<span style="font-size: 30px; font-weight: 600; color: {NAVY}">Send this to someone with an ultrasound coming up.</span></div>')
                + footer("General information, not medical advice.", DUSK), color=NAVY)


def gbp():
    return page("Google image", CREAM,
                frame("gbp", 560, 820, 600, 40, "#E3ECF5", 40)
                + at(64, 110, '<div style="display: flex; flex-direction: column; gap: 24px">' + mark(DUSK)
                     + tag("Before your ultrasound", COBALT, NAVY)
                     + v2.h("Ultrasound prep?", "It varies by scan.", 58, NAVY, DUSK, 500)
                     + txt("Abdomen: no food 8&ndash;12 hrs. Pelvis: 32 oz of water. Thyroid, breast, vascular: no prep.", 27, NAVY, 480)
                     + txt("Painless, no radiation. $195 self-pay in Seminole.", 27, DUSK, 480) + "</div>")
                + at(64, 760, f'<div style="width: 400px; height: 76px; border-radius: 38px; background: {NAVY}; display: flex; align-items: center; justify-content: center">'
                     f'<span style="font-size: 27px; font-weight: 700; color: #FFFFFF">Book at advancedimg.com</span></div>'), 1200, 900, color=NAVY)


def main():
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    (OUT / "carousel.html").write_text(head("Ultrasound prep (pastel)", PREVIEW) + "\n".join([s1(), s2(), s3(), s4(), s5(), s6(), s7()]) + "</body></html>")
    (OUT / "gbp.html").write_text(head(SLUG + " google", PREVIEW) + gbp() + "</body></html>")
    print("built", OUT)
    if PREVIEW:
        render(OUT, ["carousel.html", "gbp.html"])
    else:
        for f in ("carousel.html", "gbp.html"):
            print("import URL:", f"{BASE_URL}{SLUG}/{f}")


if __name__ == "__main__":
    main()
