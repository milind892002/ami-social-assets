"""Oct 18 2026 ultrasound prep, v5: bold colour-block editorial look.

Each slide is a saturated brand colour with a giant number, and an editorial still life shot on
a matching coloured backdrop sits in a rounded card (frames swapped in Canva with update_fill).

    python3 tools/custom/ultrasound_prep_v5.py --preview
    python3 tools/custom/ultrasound_prep_v5.py
"""
import pathlib, sys
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_post import head, render, BASE_URL, ROOT  # noqa: E402
import ultrasound_prep_v2 as v2  # noqa: E402

SLUG = "2026-10-18-ultrasound-prep-v5"
PREVIEW = "--preview" in sys.argv
OUT = ROOT / ("preview" if PREVIEW else "imports") / SLUG
IMG = "img/" if PREVIEW else f"{BASE_URL}{SLUG}/img/"
NAVY, COBALT, AMB, AQU, GRN, SUN = "#0B2440", "#1D5FA6", "#F5A623", "#2BB3C0", "#34B37A", "#FFD58A"
H, at, icon = v2.H, v2.at, v2.icon
R = 44


def frame(name, w, hgt, x, y, tint, r=R):
    Image.new("RGB", (w, hgt), tint).save(OUT / "img" / f"frame-{name}.png")
    return at(x, y, f'<img src="{IMG}frame-{name}.png" width="{w}" height="{hgt}" alt="" '
                    f'style="display: block; width: {w}px; height: {hgt}px; border-radius: {r}px">')


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
    return page("Slide 1 Hook", COBALT,
                frame("hook", 984, 780, 48, 48, "#2A6DB5")
                + at(88, 880, '<div style="display: flex; flex-direction: column; gap: 22px">' + tag("Save this before your scan", NAVY, SUN)
                     + v2.h("Ultrasound prep?", "Depends on the type.", 88, "#FFFFFF", SUN, 904, "h1") + "</div>")
                + at(88, 1252, f'<div style="display: flex; justify-content: space-between; align-items: center; width: 904px">'
                     f'<div style="display: flex; align-items: center; gap: 14px; font-size: 30px; font-weight: 700; color: #FFFFFF">Swipe {icon("arrow", "#FFFFFF", 38)}</div>{mark("#CFE0F4")}</div>'))


def s2():
    tiles = [("Abdomen", "8&ndash;12h", "no food before", AMB), ("Pelvis", "32 oz", "water, 1 hour before", AQU),
             ("Thyroid &amp; breast", "0", "special prep", GRN), ("Vascular", "0", "special prep", GRN)]
    def tile(name, num, sub, c):
        return (f'<div style="box-sizing: border-box; width: 440px; height: 400px; border-radius: {R}px; background: {c}; padding: 36px; '
                f'display: flex; flex-direction: column; justify-content: space-between">'
                f'<div style="font-size: 30px; font-weight: 700; color: {NAVY}">{name}</div>'
                f'<div>{big(num, 120, NAVY, 368)}<div style="font-size: 27px; font-weight: 600; color: {NAVY}; margin-top: 10px">{sub}</div></div></div>')
    grid = '<div style="display: flex; flex-wrap: wrap; gap: 24px; width: 904px">' + "".join(tile(*t) for t in tiles) + "</div>"
    return page("Slide 2 Prep by type", NAVY,
                at(88, 96, v2.h("Which ultrasound are you having?", None, 68, "#FFFFFF", SUN, 904))
                + at(88, 330, grid) + footer("Not sure? Check your doctor&#39;s order.", "#9CC6F0"))


def stat_slide(label, bg, name, tint, tagtxt, number, unit, line, sub, foot=""):
    return page(label, bg,
                frame(name, 984, 560, 48, 48, tint)
                + at(88, 652, '<div style="display: flex; flex-direction: column; gap: 18px">' + tag(tagtxt, NAVY, "#FFFFFF")
                     + f'<div style="display: flex; align-items: baseline; gap: 22px">{big(number, 230, NAVY, None)}'
                       f'<div style="{H}; font-weight: 800; font-size: 64px; color: {NAVY}; letter-spacing: -0.02em">{unit}</div></div>'
                     + txt(line, 46, NAVY, 904, 800, 1.1, H + ";")
                     + txt(sub, 30, NAVY, 904, 500) + "</div>")
                + footer(foot, NAVY), color=NAVY)


def s3():
    return stat_slide("Slide 3 Abdomen", AMB, "abd", "#F2B046", "Abdomen", "8&ndash;12", "hrs",
                      "No food before your abdominal ultrasound.", "Water is OK.", "Your doctor may give different instructions.")


def s4():
    return stat_slide("Slide 4 Pelvis", AQU, "pel", "#4CC0CB", "Pelvis", "32", "oz",
                      "of water, 1 hour before your pelvic ultrasound.", "And don&#39;t empty your bladder. A full bladder gives a clearer view.")


def s5():
    return stat_slide("Slide 5 No prep", GRN, "thy", "#52C08E", "Thyroid &middot; breast &middot; vascular", "0", "prep",
                      "Nothing special needed. Just come in.", "Wear loose, comfy clothes and leave jewelry at home.")


def s6():
    def tile(num, sub, c, fg=NAVY):
        return (f'<div style="box-sizing: border-box; width: 285px; height: 300px; border-radius: 40px; background: {c}; padding: 30px; '
                f'display: flex; flex-direction: column; justify-content: flex-end">'
                f'{big(num, 64, fg, 230, 0.95)}<div style="font-size: 25px; font-weight: 600; color: {fg}; margin-top: 12px">{sub}</div></div>')
    row = ('<div style="display: flex; gap: 24px">' + tile("0", "radiation. Just sound waves.", AQU)
           + tile("20&ndash;45", "minutes for most exams.", AMB) + tile("48&ndash;72h", "results to your doctor.", GRN) + "</div>")
    return page("Slide 6 What to expect", NAVY,
                frame("probe", 984, 520, 48, 48, "#14325A")
                + at(88, 610, '<div style="display: flex; flex-direction: column; gap: 18px">' + tag("What to expect", SUN, NAVY)
                     + v2.h("Warm gel. Slight pressure.", "No pain.", 66, "#FFFFFF", SUN, 904) + "</div>")
                + at(88, 880, row) + at(88, 1256, f'<span style="font-size: 22px; font-weight: 500; color: #9CC6F0">{v2.SRC}</span>'))


def s7():
    def btn(k, t, bg, fg):
        return (f'<div style="box-sizing: border-box; display: flex; align-items: center; gap: 22px; padding: 30px 40px; border-radius: 999px; background: {bg}; width: 904px">'
                f'{icon(k, fg, 40)}<span style="font-size: 36px; font-weight: 700; color: {fg}">{t}</span></div>')
    chips = ('<div style="display: flex; flex-wrap: wrap; gap: 14px; width: 904px">'
             + tag("$195 self-pay", SUN, NAVY) + tag("No referral needed", "#FFFFFF", NAVY) + tag("Same-day often", NAVY, "#FFFFFF") + "</div>")
    return page("Slide 7 CTA", COBALT,
                at(88, 120, '<div style="display: flex; flex-direction: column; gap: 34px">'
                     + big("Save this.", 150, "#FFFFFF") + big("Book when you&#39;re ready.", 96, SUN, 904, 1.0) + chips + "</div>")
                + at(88, 800, '<div style="display: flex; flex-direction: column; gap: 20px">'
                     + btn("phone", "Call (727) 398-5999", "#FFFFFF", NAVY) + btn("cal", "Book through the link in our bio", NAVY, "#FFFFFF") + "</div>")
                + at(88, 1080, f'<div style="display: flex; align-items: center; gap: 16px">{icon("send", "#FFFFFF", 34)}'
                     f'<span style="font-size: 30px; font-weight: 600; color: #FFFFFF">Send this to someone with an ultrasound coming up.</span></div>')
                + footer("General information, not medical advice.", "#CFE0F4"))


def gbp():
    return page("Google image", COBALT,
                frame("gbp", 560, 820, 600, 40, "#2A6DB5", 40)
                + at(64, 110, '<div style="display: flex; flex-direction: column; gap: 24px">' + mark("#CFE0F4")
                     + tag("Before your ultrasound", NAVY, SUN)
                     + v2.h("Ultrasound prep?", "It varies by scan.", 58, "#FFFFFF", SUN, 500)
                     + txt("Abdomen: no food 8&ndash;12 hrs. Pelvis: 32 oz of water. Thyroid, breast, vascular: no prep.", 27, "#FFFFFF", 480)
                     + txt("Painless, no radiation. $195 self-pay in Seminole.", 27, "#CFE0F4", 480) + "</div>")
                + at(64, 760, f'<div style="width: 400px; height: 76px; border-radius: 38px; background: #FFFFFF; display: flex; align-items: center; justify-content: center">'
                     f'<span style="font-size: 27px; font-weight: 700; color: {NAVY}">Book at advancedimg.com</span></div>'), 1200, 900)


def main():
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    (OUT / "carousel.html").write_text(head("Ultrasound prep (bold)", PREVIEW) + "\n".join([s1(), s2(), s3(), s4(), s5(), s6(), s7()]) + "</body></html>")
    (OUT / "gbp.html").write_text(head(SLUG + " google", PREVIEW) + gbp() + "</body></html>")
    print("built", OUT)
    if PREVIEW:
        render(OUT, ["carousel.html", "gbp.html"])
    else:
        for f in ("carousel.html", "gbp.html"):
            print("import URL:", f"{BASE_URL}{SLUG}/{f}")


if __name__ == "__main__":
    main()
