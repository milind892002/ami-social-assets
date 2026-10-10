"""Build Meta ad artwork (feed 4:5 and story 9:16) as Canva-importable HTML from a JSON spec.

Usage:
  python3 tools/build_ads.py posts/<slug>.json --preview   # local render -> preview/<slug>/ (PNG + sheet.jpg)
  python3 tools/build_ads.py posts/<slug>.json             # publish build -> imports/<slug>/ (feed.html, story.html)

Each ad in the spec becomes one page in feed.html (1080x1350) and one in story.html (1080x1920),
so each size imports into Canva as its own design. Same Canva rules as build_post.py.

Layouts:
  hero        photo across the top fading into a dark page, then headline, price and chips (whole-body MRI)
  report      light page with a "what the report shows" card of segmented bars (DEXA body composition)
  price_list  real photo on top, then a list of services with prices (screening)

Story pages keep text out of the top 270px and bottom 380px, where Instagram and Facebook
draw the profile name, reply bar and button.
"""
import json, pathlib, shutil, sys
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_post import ROOT, BASE_URL, H, B, crop_to, fade_bottom, head, render  # noqa: E402

W = 1080


def shade_left(im, color, strength):
    """Darken the lower-left of a hero photo so text over it stays readable."""
    from build_post import hexrgb
    from PIL import ImageDraw
    w, h = im.size
    over = Image.new("RGB", (w, h), hexrgb(color))
    mask = Image.new("L", (w, h), 0); px = mask.load()
    for y in range(int(h * 0.3), h):
        vy = min(1.0, (y - h * 0.3) / (h * 0.3))
        for x in range(0, int(w * 0.8)):
            px[x, y] = int(255 * strength * vy * (1 - x / (w * 0.8)) ** 1.1)
    return Image.composite(over, im, mask)
SIZES = {"feed": 1350, "story": 1920}
BRAND = ROOT / "tools" / "brand"


class Ads:
    def __init__(self, spec, out, img_url, photos):
        self.s, self.out, self.url, self.photos = spec, out, img_url, photos
        (out / "img").mkdir(parents=True, exist_ok=True)
        shutil.copy(BRAND / "lockup_pill.png", out / "img" / "logo.png")
        self.n = 0

    # ----- primitives -----
    def photo(self, ph, size, kind, fade_to=None, fade_from=0.55):
        """ph = {"src": ..., "feed": [x0, y0, x1, y1], "story": [...]}; per-size crops are optional."""
        self.n += 1
        im = crop_to({"src": ph["src"], "crop": ph.get(kind)}, size, self.photos)
        if fade_to:
            im = fade_bottom(im, fade_to, int(size[1] * fade_from), size[1])
        if ph.get("polish"):
            from PIL import ImageEnhance
            im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.08)).enhance(1.06)
        if fade_to and ph.get("offset"):
            from build_post import hexrgb
            off = ph["offset"]; w, h = im.size
            ramp = Image.new("L", (w, h), 255); rp = ramp.load()
            for x in range(min(260, w)):  # feather the photo's left edge into the page colour
                v = int(255 * (x / 260) ** 1.5)
                for y in range(h):
                    rp[x, y] = v
            canvas = Image.new("RGB", im.size, hexrgb(fade_to)); canvas.paste(im, (off, 0), ramp); im = canvas
        if fade_to and ph.get("shade_left"):
            im = shade_left(im, fade_to, ph["shade_left"])
        name = f"a{self.n}.jpg"
        im.save(self.out / "img" / name, quality=90)
        return name

    def img(self, name, w, h, style=""):
        return (f'<img src="{self.url}{name}" width="{w}" height="{h}" alt="" '
                f'style="display: block; width: {w}px; height: {h}px; {style}">')

    def logo(self, style=""):
        return self.img("logo.png", 330, 110, style)

    def text(self, t, size, color, weight=500, extra=""):
        return f'<p style="margin: 0; font-size: {size}px; line-height: 1.3; font-weight: {weight}; color: {color}; {extra}">{t}</p>'

    def eyebrow(self, t, color, size=26):
        return (f'<p style="margin: 0; font-size: {size}px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; '
                f'color: {color}">{t}</p>')

    def heading(self, t, size, color, width, accent=None, accent_color=None):
        acc = f' <span style="color: {accent_color}">{accent}</span>' if accent else ""
        return (f'<h1 style="margin: 0; width: {width}px; {H}; font-weight: 800; font-size: {size}px; line-height: 1.04; '
                f'letter-spacing: -0.02em; color: {color}">{t}{acc}</h1>')

    def check(self, color, size):
        return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.6" '
                f'stroke-linecap="round" stroke-linejoin="round" style="flex: none"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>')

    def chips(self, items, fg, border, size=28, icon=None):
        out = []
        for t in items:
            ic = self.check(icon, size + 4) if icon else ""
            out.append(f'<div style="display: flex; align-items: center; gap: 10px; border: 2px solid {border}; border-radius: 999px; '
                       f'padding: 12px 22px; font-size: {size}px; font-weight: 600; color: {fg}">{ic}<span>{t}</span></div>')
        return '<div style="display: flex; flex-wrap: wrap; gap: 14px">' + "".join(out) + "</div>"

    def price(self, ad, color, side_color, size=150):
        lines = "".join(f'<span>{l}</span>' for l in ad.get("price_notes", []))
        return (f'<div style="display: flex; align-items: center; gap: 30px">'
                f'<span style="{H}; font-weight: 800; font-size: {size}px; line-height: 0.9; letter-spacing: -0.03em; color: {color}">{ad["price"]}</span>'
                f'<div style="display: flex; flex-direction: column; gap: 6px; font-size: 30px; line-height: 1.25; font-weight: 600; color: {side_color}">{lines}</div></div>')

    def page(self, label, h, bg, inner, style=""):
        return (f'<div data-document-role="page" data-label="{label}" style="position: relative; width: {W}px; height: {h}px; '
                f'overflow: hidden; background: {bg}; {B}; {style}">{inner}</div>')

    # ----- layouts -----
    def hero(self, ad, kind):
        c = ad["colors"]; h = SIZES[kind]
        ph_h = 780 if kind == "feed" else 1260
        ph = self.photo(ad["photo"], (W, ph_h), kind, c["bg"], 0.5 if kind == "feed" else 0.62)
        top = 64 if kind == "feed" else 280
        bottom = 80 if kind == "feed" else 380
        block = (f'<div style="position: absolute; left: 80px; width: 920px; bottom: {bottom}px; display: flex; flex-direction: column; gap: 30px">'
                 + self.eyebrow(ad["eyebrow"], c["accent"])
                 + self.heading(ad["title"], ad.get("title_size", 96), "#FFFFFF", 920)
                 + self.price(ad, c["price"], c["muted"])
                 + self.chips(ad["chips"], "#FFFFFF", c["chip_border"], 26, c["accent"])
                 + f'<div style="padding-top: 8px">{self.text(ad["footer"], 26, c["muted"])}</div></div>')
        return self.page(f'{ad["name"]} {kind}', h, c["bg"],
                         self.img(ph, W, ph_h, "position: absolute; left: 0; top: 0")
                         + self.logo(f"position: absolute; left: 80px; top: {top}px") + block)

    def report(self, ad, kind):
        c = ad["colors"]; h = SIZES[kind]
        story = kind == "story"
        bar_w = 560
        rows = []
        for label, segs in ad["rows"]:
            parts = []
            for k, (frac, col) in enumerate(segs):
                r = ("12px 0 0 12px" if k == 0 else "0") if k < len(segs) - 1 else ("0 12px 12px 0" if k else "12px")
                parts.append(f'<div style="width: {round(bar_w * frac)}px; height: 40px; background: {col}; border-radius: {r}"></div>')
            rows.append(f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 24px">'
                        f'<span style="font-size: 32px; font-weight: 600; color: {c["ink"]}">{label}</span>'
                        f'<div style="display: flex; gap: 4px">{"".join(parts)}</div></div>')
        legend = "".join(f'<div style="display: flex; align-items: center; gap: 10px"><div style="width: 22px; height: 22px; border-radius: 6px; background: {col}"></div>'
                         f'<span>{name}</span></div>' for name, col in ad["legend"])
        card = (f'<div style="display: flex; flex-direction: column; gap: {30 if story else 24}px; background: #FFFFFF; border: 2px solid {c["border"]}; '
                f'border-radius: 28px; padding: {44 if story else 34}px 40px">'
                f'<div style="display: flex; align-items: center; justify-content: space-between">'
                f'<span style="font-size: 24px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: {c["muted"]}">{ad["card_label"]}</span>'
                f'<div style="display: flex; gap: 24px; font-size: 24px; font-weight: 600; color: {c["muted"]}">{legend}</div></div>'
                + "".join(rows) + "</div>")
        inner = (self.logo()
                 + f'<div style="display: flex; flex-direction: column; gap: 26px">'
                 + self.eyebrow(ad["eyebrow"], c["accent"])
                 + self.heading(ad["title"], ad.get("title_size", 84), c["ink"], 920, ad.get("title_accent"), c["accent"]) + "</div>"
                 + card
                 + f'<div style="display: flex; flex-direction: column; gap: 26px">'
                 + self.price(ad, c["price"], c["ink"], 132)
                 + self.chips(ad["chips"], c["ink"], c["chip_border"], 26, c["accent"]) + "</div>"
                 + self.text(ad["footer"], 26, c["muted"]))
        pad = "64px 80px 72px" if not story else "280px 80px 380px"
        return self.page(f'{ad["name"]} {kind}', h, c["bg"], inner,
                         f"box-sizing: border-box; padding: {pad}; display: flex; flex-direction: column; justify-content: space-between")

    def price_list(self, ad, kind):
        c = ad["colors"]; h = SIZES[kind]
        story = kind == "story"
        ph_h = 540 if not story else 740
        ph = self.photo(ad["photo"], (W, ph_h), kind)
        rows = "".join(
            f'<div style="display: flex; align-items: baseline; justify-content: space-between; padding-block: {16 if not story else 22}px; '
            f'border-top: 2px solid {c["border"]}{"; border-bottom: 2px solid " + c["border"] if i == len(ad["items"]) - 1 else ""}">'
            f'<span style="font-size: 36px; font-weight: 600; color: {c["ink"]}">{name}</span>'
            f'<span style="{H}; font-size: 52px; font-weight: 800; letter-spacing: -0.02em; color: {c["price"]}">{p}</span></div>'
            for i, (name, p) in enumerate(ad["items"]))
        body = (f'<div style="position: absolute; left: 80px; width: 920px; top: {ph_h + 44}px; bottom: {72 if not story else 380}px; '
                f'display: flex; flex-direction: column; justify-content: space-between">'
                f'<div style="display: flex; flex-direction: column; gap: 20px">'
                + self.eyebrow(ad["eyebrow"], c["accent"])
                + self.heading(ad["title"], ad.get("title_size", 76), c["ink"], 920) + "</div>"
                + f'<div style="display: flex; flex-direction: column">{rows}</div>'
                + self.chips(ad["chips"], c["ink"], c["chip_border"], 26, c["accent"])
                + self.text(ad["footer"], 26, c["muted"]) + "</div>")
        top = 56 if not story else 280
        return self.page(f'{ad["name"]} {kind}', h, c["bg"],
                         self.img(ph, W, ph_h, "position: absolute; left: 0; top: 0")
                         + self.logo(f"position: absolute; left: 48px; top: {top}px") + body)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    preview = "--preview" in sys.argv
    photos = "/home/claude/amiweb/public/images"
    if "--photos" in sys.argv:
        photos = sys.argv[sys.argv.index("--photos") + 1]; args.remove(photos)
    spec = json.loads(pathlib.Path(args[0]).read_text())
    slug = spec["slug"]
    out = ROOT / ("preview" if preview else "imports") / slug
    out.mkdir(parents=True, exist_ok=True)
    a = Ads(spec, out, "img/" if preview else f"{BASE_URL}{slug}/img/", photos)
    files = []
    for kind in ("feed", "story"):
        pages = [getattr(a, ad["layout"])(ad, kind) for ad in spec["ads"]]
        (out / f"{kind}.html").write_text(head(f"{slug} {kind}", preview) + "\n".join(pages) + "</body></html>")
        files.append(f"{kind}.html")
    print("built", out, files)
    if preview:
        render(out, files)
    else:
        for f in files:
            print("import URL:", f"{BASE_URL}{slug}/{f}")


if __name__ == "__main__":
    main()
