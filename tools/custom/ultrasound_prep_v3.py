"""Oct 18 2026 ultrasound prep, v3: realistic anatomy renders (Canva AI images).

Layouts are built here with plain navy placeholder frames; after import, each frame's
fill is replaced in Canva (update_fill) with the generated anatomy image listed in
posts/2026-10-18-ultrasound-prep-v3.json. A navy fade PNG sits above each frame so
the photo melts into the background behind the text.

    python3 tools/custom/ultrasound_prep_v3.py --preview
    python3 tools/custom/ultrasound_prep_v3.py
"""
import pathlib, sys
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_post import head, render, BASE_URL, ROOT  # noqa: E402
import ultrasound_prep_v2 as v2  # noqa: E402  (shared colours and HTML helpers)

SLUG = "2026-10-18-ultrasound-prep-v3"
PREVIEW = "--preview" in sys.argv
OUT = ROOT / ("preview" if PREVIEW else "imports") / SLUG
IMG = "img/" if PREVIEW else f"{BASE_URL}{SLUG}/img/"
NAVY, CARD, ACC_D, ON_D = v2.NAVY, v2.CARD, v2.ACC_D, v2.ON_D
AMB, AQU, GRN = v2.AMB, v2.AQU, v2.GRN
at, h, p, chip, eyebrow, wordmark, icon, save_tag = v2.at, v2.h, v2.p, v2.chip, v2.eyebrow, v2.wordmark, v2.icon, v2.save_tag


def frame(name, w, hgt, x, y, radius=0):
    """Placeholder photo frame (swapped for the real image in Canva)."""
    Image.new("RGB", (w, hgt), "#12355C").save(OUT / "img" / f"frame-{name}.png")
    r = f" border-radius: {radius}px;" if radius else ""
    return at(x, y, f'<img src="{IMG}frame-{name}.png" width="{w}" height="{hgt}" alt="" style="display: block; width: {w}px; height: {hgt}px;{r}">')


def fade(name, w, hgt, x, y, start=0.45):
    """Transparent-to-navy vertical fade, laid over a frame."""
    im = Image.new("RGBA", (w, hgt))
    nav = tuple(int(NAVY[i:i + 2], 16) for i in (1, 3, 5))
    px = im.load()
    for yy in range(hgt):
        t = max(0.0, (yy / hgt - start) / (1 - start))
        a = int(255 * min(1.0, t * t * (3 - 2 * t)))
        for xx in range(w):
            px[xx, yy] = nav + (a,)
    im.save(OUT / "img" / f"fade-{name}.png")
    return at(x, y, f'<img src="{IMG}fade-{name}.png" width="{w}" height="{hgt}" alt="" style="display: block; width: {w}px; height: {hgt}px">')


def page(label, inner, w=1080, hgt=1350):
    return v2.page(label, NAVY, inner, w, hgt)


def s1():
    return page("Slide 1 Hook", frame("hook", 1080, 1000, 0, 0) + fade("hook", 1080, 1000, 0, 0, 0.5) + at(88, 72, wordmark(True))
                + at(88, 880, '<div style="display: flex; flex-direction: column; gap: 26px; width: 904px">'
                     + eyebrow("Save this before your scan", ACC_D)
                     + h("Ultrasound prep?", "Depends on the type.", 84, "#FFFFFF", ACC_D, 904, "h1")
                     + '<div style="display: flex; flex-wrap: wrap; gap: 14px; width: 904px">'
                     + chip("Abdomen", AMB, True) + chip("Pelvis", AQU, True) + chip("Thyroid, breast, vascular", GRN, True) + "</div></div>")
                + at(88, 1240, f'<div style="display: flex; align-items: center; gap: 16px; font-size: 30px; font-weight: 600; color: #FFFFFF">Swipe {icon("arrow", "#FFFFFF", 40)}</div>'))


def s2():
    tiles = [("abd", "Abdomen", "No food for 8 to 12 hours", AMB), ("pel", "Pelvis", "Full bladder", AQU),
             ("thy", "Thyroid", "No special prep", GRN), ("vas", "Vascular", "No special prep", GRN)]
    out = ""
    for i, (k, name, sub, c) in enumerate(tiles):
        x, y = 88 + (i % 2) * 464, 330 + (i // 2) * 440
        out += frame(f"t{k}", 440, 300, x, y, 24)
        out += at(x, y + 318, f'<div style="display: flex; align-items: center; gap: 12px"><div style="width: 18px; height: 18px; border-radius: 9px; background: {c}"></div>'
                  f'<span style="{v2.H}; font-weight: 800; font-size: 36px; color: #FFFFFF">{name}</span></div>'
                  f'<div style="font-size: 26px; font-weight: 600; color: {ON_D}; margin-top: 6px">{sub}</div>', 440)
    return page("Slide 2 Prep by type", at(88, 72, wordmark(True))
                + at(88, 150, '<div style="display: flex; flex-direction: column; gap: 22px">' + eyebrow("Prep by type", ACC_D)
                     + h("Which ultrasound are you having?", None, 64, "#FFFFFF", ACC_D, 904) + "</div>")
                + out + at(88, 1236, p("Breast ultrasound: no special prep either. Not sure? Check your doctor&#39;s order.", 26, ACC_D, 904, 600)))


def big(name, label, chip_html, title, sub, foot=""):
    return page(label, frame(name, 1080, 860, 0, 0) + fade(name, 1080, 860, 0, 0, 0.55) + at(88, 72, wordmark(True))
                + at(88, 800, '<div style="display: flex; flex-direction: column; gap: 24px">' + chip_html
                     + h(title, None, 74, "#FFFFFF", ACC_D, 904) + p(sub, 32, ON_D, 904) + "</div>")
                + (at(88, 1240, p(foot, 24, ACC_D, 904)) if foot else ""))


def s3():
    return big("abd", "Slide 3 Abdomen", chip("Abdomen", AMB, True), "No food for 8 to 12 hours before.",
               "Water is OK.", "Your doctor or our team may give you different instructions.")


def s4():
    return big("pel", "Slide 4 Pelvis", chip("Pelvis", AQU, True), "Drink 32 oz of water 1&nbsp;hour before.",
               "And don&#39;t empty your bladder. A full bladder gives us a clearer view.")


def s5():
    return big("thy", "Slide 5 No prep", chip("No prep", GRN, True), "Thyroid, breast or vascular? Just come in.",
               "Wear loose, comfy clothes and leave jewelry at home.")


def s6():
    def row(big_t, small):
        return (f'<div style="display: flex; align-items: baseline; gap: 28px; padding: 22px 0; border-top: 2px solid #22466F">'
                f'<div style="width: 300px; flex: none; {v2.H}; font-weight: 800; font-size: 46px; color: #FFFFFF">{big_t}</div>'
                f'<div style="font-size: 28px; font-weight: 500; color: {ON_D}">{small}</div></div>')
    return page("Slide 6 What to expect", frame("probe", 1080, 640, 0, 0) + fade("probe", 1080, 640, 0, 0, 0.5) + at(88, 72, wordmark(True))
                + at(88, 560, '<div style="display: flex; flex-direction: column; gap: 22px">' + eyebrow("What to expect", ACC_D)
                     + h("Painless, and no radiation.", None, 72, "#FFFFFF", ACC_D, 904) + "</div>")
                + at(88, 800, '<div style="width: 904px">' + row("Warm gel", "A smooth probe glides over your skin. Slight pressure, no pain.")
                     + row("20 to 45 min", "for most exams. You may see the images on screen.")
                     + row("0 radiation", "Just sound waves. Results to your doctor in 48 to 72 hours.") + "</div>")
                + at(88, 1240, p(v2.SRC, 24, ACC_D, 904)))


def s7():
    def btn(k, t):
        return (f'<div style="display: flex; align-items: center; gap: 22px; padding: 26px 34px; border-radius: 20px; background: {CARD}; width: 836px">'
                f'{icon(k, ACC_D, 40)}<span style="font-size: 34px; font-weight: 600; color: #FFFFFF">{t}</span></div>')
    facts = ('<div style="display: flex; flex-wrap: wrap; gap: 14px; width: 904px">'
             + chip("$195 self-pay", ACC_D, True) + chip("No referral needed", ACC_D, True) + chip("Same-day often available", ACC_D, True) + "</div>")
    return page("Slide 7 CTA", frame("cta", 1080, 520, 0, 0) + fade("cta", 1080, 520, 0, 0, 0.2) + at(88, 72, wordmark(True))
                + at(88, 330, '<div style="display: flex; flex-direction: column; gap: 34px">' + save_tag(ACC_D)
                     + h("Save this for scan day.", "Book when you&#39;re ready.", 80, "#FFFFFF", ACC_D, 904) + facts + "</div>")
                + at(88, 880, '<div style="display: flex; flex-direction: column; gap: 18px">' + btn("phone", "Call (727) 398-5999")
                     + btn("cal", "Book through the link in our bio") + "</div>")
                + at(88, 1160, f'<div style="display: flex; align-items: center; gap: 16px">{icon("send", "#FFFFFF", 34)}'
                     f'<span style="font-size: 30px; font-weight: 600; color: #FFFFFF">Send this to someone with an ultrasound coming up.</span></div>')
                + at(88, 1244, p("General information, not medical advice. Coverage varies by plan.", 22, ACC_D, 904)))


def gbp():
    # side fade: rotate a vertical fade so the image melts leftwards into the text panel
    inner = frame("gbp", 640, 900, 560, 0)
    im = Image.new("RGBA", (240, 900)); px = im.load()
    nav = tuple(int(NAVY[i:i + 2], 16) for i in (1, 3, 5))
    for xx in range(240):
        a = int(255 * (1 - xx / 239) ** 1.6)
        for yy in range(900):
            px[xx, yy] = nav + (a,)
    im.save(OUT / "img" / "fade-gbp.png")
    inner += at(560, 0, f'<img src="{IMG}fade-gbp.png" width="240" height="900" alt="" style="display: block; width: 240px; height: 900px">')
    inner += (at(64, 60, wordmark(True))
              + at(64, 220, '<div style="display: flex; flex-direction: column; gap: 26px">' + eyebrow("Before your ultrasound", ACC_D)
                   + h("Ultrasound prep?", "It varies by scan.", 58, "#FFFFFF", ACC_D, 520)
                   + '<div style="display: flex; flex-wrap: wrap; gap: 12px; width: 480px">' + chip("Abdomen", AMB, True) + chip("Pelvis", AQU, True) + chip("No prep", GRN, True) + "</div>"
                   + p("Painless, no radiation. $195 self-pay in Seminole, no referral needed.", 28, ON_D, 480) + "</div>")
              + at(64, 760, f'<div style="width: 400px; height: 76px; border-radius: 38px; background: {ACC_D}; display: flex; align-items: center; justify-content: center">'
                   f'<span style="font-size: 28px; font-weight: 700; color: {NAVY}">Book at advancedimg.com</span></div>'))
    return page("Google image", inner, 1200, 900)


def main():
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    slides = [s1(), s2(), s3(), s4(), s5(), s6(), s7()]
    (OUT / "carousel.html").write_text(head("Ultrasound prep (anatomy)", PREVIEW) + "\n".join(slides) + "</body></html>")
    (OUT / "gbp.html").write_text(head(SLUG + " google", PREVIEW) + gbp() + "</body></html>")
    print("built", OUT)
    if PREVIEW:
        render(OUT, ["carousel.html", "gbp.html"])
    else:
        for f in ("carousel.html", "gbp.html"):
            print("import URL:", f"{BASE_URL}{SLUG}/{f}")


if __name__ == "__main__":
    main()
