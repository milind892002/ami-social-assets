"""Oct 18 2026 ultrasound prep, v4: photographic images in soft, rounded cards on a light page.

Photo frames are plain placeholders with rounded corners; after Canva import each frame's
fill is swapped (update_fill) for the image listed in posts/2026-10-18-ultrasound-prep-v4.json.
No fades, no full-bleed hard edges: every image and panel has large rounded corners.

    python3 tools/custom/ultrasound_prep_v4.py --preview
    python3 tools/custom/ultrasound_prep_v4.py
"""
import pathlib, sys
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_post import head, render, BASE_URL, ROOT  # noqa: E402
import ultrasound_prep_v2 as v2  # noqa: E402

SLUG = "2026-10-18-ultrasound-prep-v4"
PREVIEW = "--preview" in sys.argv
OUT = ROOT / ("preview" if PREVIEW else "imports") / SLUG
IMG = "img/" if PREVIEW else f"{BASE_URL}{SLUG}/img/"
NAVY, LIGHT, INK, ACC, ACC_D, BODY, MUTED, DIV = v2.NAVY, "#F4F7FB", v2.INK, v2.ACC, v2.ACC_D, v2.BODY, v2.MUTED, "#DCE6F2"
AMB, AQU, GRN = v2.AMB, v2.AQU, v2.GRN
H = v2.H
at, h, p, eyebrow, icon = v2.at, v2.h, v2.p, v2.eyebrow, v2.icon
R = 44  # corner radius for photos and panels


def frame(name, w, hgt, x, y, r=R):
    Image.new("RGB", (w, hgt), "#C9D7E8").save(OUT / "img" / f"frame-{name}.png")
    return at(x, y, f'<img src="{IMG}frame-{name}.png" width="{w}" height="{hgt}" alt="" '
                    f'style="display: block; width: {w}px; height: {hgt}px; border-radius: {r}px">')


def pill(label, color, bg="#FFFFFF", fg=INK):
    return (f'<div style="align-self: flex-start; display: flex; align-items: center; gap: 12px; padding: 14px 24px; border-radius: 999px; background: {bg}">'
            f'<div style="width: 18px; height: 18px; border-radius: 9px; background: {color}"></div>'
            f'<span style="font-size: 26px; font-weight: 600; color: {fg}">{label}</span></div>')


def mark(color=ACC):
    return f'<div style="font-size: 22px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: {color}">Advanced Medical Imaging</div>'


def page(label, inner, w=1080, hgt=1350, bg=LIGHT, color=INK):
    return v2.page(label, bg, inner, w, hgt, color=color)


def photo_slide(label, name, photo_h, chip_html, title, sub, foot=None):
    top = 48 + photo_h + 52
    return page(label, frame(name, 984, photo_h, 48, 48)
                + at(88, top, '<div style="display: flex; flex-direction: column; gap: 22px">' + chip_html
                     + h(title, None, 68, INK, ACC, 904) + p(sub, 32, BODY, 904) + "</div>")
                + at(88, 1252, f'<div style="display: flex; justify-content: space-between; width: 904px; align-items: center">'
                     f'<span style="font-size: 22px; font-weight: 500; color: {MUTED}">{foot or ""}</span>{mark()}</div>'))


def s1():
    return page("Slide 1 Hook", frame("hook", 984, 820, 48, 48)
                + at(88, 920, '<div style="display: flex; flex-direction: column; gap: 22px; width: 904px">'
                     + eyebrow("Save this before your scan", ACC)
                     + h("Ultrasound prep?", "Depends on the type.", 84, INK, ACC, 904, "h1") + "</div>")
                + at(88, 1244, f'<div style="display: flex; justify-content: space-between; width: 904px; align-items: center">'
                     f'<div style="display: flex; align-items: center; gap: 14px; font-size: 30px; font-weight: 600; color: {INK}">Swipe {icon("arrow", INK, 38)}</div>{mark()}</div>'))


def s2():
    rows = [("Abdomen", "No food for 8 to 12 hours. Water is OK.", AMB), ("Pelvis", "32 oz of water 1 hour before. Full bladder.", AQU),
            ("Thyroid &amp; breast", "No special prep.", GRN), ("Vascular", "No special prep.", GRN)]
    def row(t, s, c):
        return (f'<div style="box-sizing: border-box; width: 904px; padding: 30px 36px; border-radius: 36px; background: #FFFFFF; display: flex; align-items: center; gap: 28px">'
                f'<div style="width: 26px; height: 26px; border-radius: 13px; background: {c}; flex: none"></div>'
                f'<div><div style="{H}; font-weight: 800; font-size: 42px; color: {INK}">{t}</div>'
                f'<div style="font-size: 28px; font-weight: 500; color: {BODY}; margin-top: 4px">{s}</div></div></div>')
    return page("Slide 2 Prep by type", at(88, 96, '<div style="display: flex; flex-direction: column; gap: 22px">' + eyebrow("Prep by type", ACC)
                                              + h("Which ultrasound are you having?", None, 68, INK, ACC, 904) + "</div>")
                + at(88, 400, '<div style="display: flex; flex-direction: column; gap: 22px">' + "".join(row(*r) for r in rows) + "</div>")
                + at(88, 1252, f'<div style="display: flex; justify-content: space-between; width: 904px; align-items: center">'
                     f'<span style="font-size: 24px; font-weight: 500; color: {MUTED}">Not sure? Check your doctor&#39;s order.</span>{mark()}</div>'))


def s3():
    return photo_slide("Slide 3 Abdomen", "abd", 700, pill("Abdomen", AMB), "No food for 8 to 12 hours before.", "Water is OK.",
                       "Your doctor may give different instructions.")


def s4():
    return photo_slide("Slide 4 Pelvis", "pel", 700, pill("Pelvis", AQU), "Drink 32 oz of water 1&nbsp;hour before.",
                       "And don&#39;t empty your bladder. A full bladder gives us a clearer view.")


def s5():
    return photo_slide("Slide 5 No prep", "thy", 700, pill("Thyroid, breast, vascular", GRN), "No special prep needed.",
                       "Wear loose, comfy clothes and leave jewelry at home.")


def s6():
    def row(b, s):
        return (f'<div style="box-sizing: border-box; width: 904px; padding: 24px 32px; border-radius: 32px; background: #FFFFFF; display: flex; align-items: center; gap: 28px">'
                f'<div style="width: 250px; flex: none; {H}; font-weight: 800; font-size: 40px; color: {INK}">{b}</div>'
                f'<div style="font-size: 27px; font-weight: 500; color: {BODY}">{s}</div></div>')
    return page("Slide 6 What to expect", frame("probe", 984, 520, 48, 48)
                + at(88, 610, '<div style="display: flex; flex-direction: column; gap: 18px">' + eyebrow("What to expect", ACC)
                     + h("Painless, and no radiation.", None, 64, INK, ACC, 904) + "</div>")
                + at(88, 800, '<div style="display: flex; flex-direction: column; gap: 16px">'
                     + row("Warm gel", "A smooth probe glides over your skin. Slight pressure, no pain.")
                     + row("20 to 45 min", "for most exams. You may see the images on screen.")
                     + row("0 radiation", "Just sound waves. Results to your doctor in 48 to 72 hours.") + "</div>")
                + at(88, 1256, f'<span style="font-size: 22px; font-weight: 500; color: {MUTED}">{v2.SRC}</span>'))


def s7():
    def btn(k, t, primary):
        bg, fg = (ACC_D, NAVY) if primary else ("#12355C", "#FFFFFF")
        return (f'<div style="box-sizing: border-box; display: flex; align-items: center; gap: 22px; padding: 28px 40px; border-radius: 999px; background: {bg}; width: 904px">'
                f'{icon(k, fg, 38)}<span style="font-size: 34px; font-weight: 700; color: {fg}">{t}</span></div>')
    panel = (f'<div style="box-sizing: border-box; width: 984px; height: 1254px; border-radius: {R}px; background: {NAVY}; position: relative">'
             + at(40, 80, '<div style="display: flex; flex-direction: column; gap: 30px">' + v2.save_tag(ACC_D)
                  + h("Save this for scan day.", "Book when you&#39;re ready.", 80, "#FFFFFF", ACC_D, 904)
                  + '<div style="display: flex; flex-wrap: wrap; gap: 14px; width: 904px">'
                  + pill("$195 self-pay", ACC_D, "#12355C", "#FFFFFF") + pill("No referral needed", ACC_D, "#12355C", "#FFFFFF")
                  + pill("Same-day often available", ACC_D, "#12355C", "#FFFFFF") + "</div></div>")
             + at(40, 760, '<div style="display: flex; flex-direction: column; gap: 18px">' + btn("phone", "Call (727) 398-5999", True)
                  + btn("cal", "Book through the link in our bio", False) + "</div>")
             + at(40, 1030, f'<div style="display: flex; align-items: center; gap: 16px">{icon("send", "#FFFFFF", 32)}'
                  f'<span style="font-size: 29px; font-weight: 600; color: #FFFFFF">Send this to someone with an ultrasound coming up.</span></div>')
             + at(40, 1140, f'<div style="display: flex; justify-content: space-between; width: 904px"><span style="font-size: 21px; color: {ACC_D}">General information, not medical advice. Coverage varies by plan.</span></div>')
             + "</div>")
    return page("Slide 7 CTA", at(48, 48, panel))


def gbp():
    return page("Google image", frame("gbp", 560, 820, 600, 40, 40)
                + at(64, 120, '<div style="display: flex; flex-direction: column; gap: 24px">' + mark()
                     + eyebrow("Before your ultrasound", ACC)
                     + h("Ultrasound prep?", "It varies by scan.", 56, INK, ACC, 500)
                     + '<div style="display: flex; flex-wrap: wrap; gap: 12px; width: 480px">' + pill("Abdomen", AMB) + pill("Pelvis", AQU) + pill("No prep", GRN) + "</div>"
                     + p("Painless, no radiation. $195 self-pay in Seminole, no referral needed.", 27, BODY, 480) + "</div>")
                + at(64, 760, f'<div style="width: 400px; height: 76px; border-radius: 38px; background: {NAVY}; display: flex; align-items: center; justify-content: center">'
                     f'<span style="font-size: 27px; font-weight: 700; color: #FFFFFF">Book at advancedimg.com</span></div>'), 1200, 900)


def main():
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    (OUT / "carousel.html").write_text(head("Ultrasound prep (photo)", PREVIEW) + "\n".join([s1(), s2(), s3(), s4(), s5(), s6(), s7()]) + "</body></html>")
    (OUT / "gbp.html").write_text(head(SLUG + " google", PREVIEW) + gbp() + "</body></html>")
    print("built", OUT)
    if PREVIEW:
        render(OUT, ["carousel.html", "gbp.html"])
    else:
        for f in ("carousel.html", "gbp.html"):
            print("import URL:", f"{BASE_URL}{SLUG}/{f}")


if __name__ == "__main__":
    main()
