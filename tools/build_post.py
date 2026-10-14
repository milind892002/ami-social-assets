"""Build an AMI social post (carousel + optional single image + Google 4:3 image)
as Canva-importable HTML from a short JSON spec.

Usage:
  python3 tools/build_post.py posts/<slug>.json            # publish build -> imports/<slug>/
  python3 tools/build_post.py posts/<slug>.json --preview  # local render -> preview/<slug>/ (PNG + sheet.jpg)

Options:
  --photos DIR   folder the spec's photo paths are relative to
                 (default /home/claude/amiweb/public/images, the website's stock photos)

Canva import rules this follows (learned the hard way):
  - each top-level <div data-document-role="page"> becomes one Canva page
  - fonts: Inter (headings) + DM Sans (body) survive import; most others do not
  - text must sit in child elements, never directly in the page div
  - photos are pre-cropped/faded/rounded here and placed as plain <img> at final size
  - headings get an explicit pixel width so Canva wraps them
  - no CSS gradients, object-fit or slide numbers (Instagram shows its own counter)

Spec format: see tools/README.md and posts/example.json.
"""
import json, pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE_URL = "https://milind892002.github.io/ami-social-assets/imports/"

PALETTES = {
    # Default brand look (first post, Oct 2026).
    "blue": dict(dark="#0B2440", card="#12355C", on_dark="#D6E4F3", accent_dark="#9CC6F0", light="#F2F6FB",
                 ink="#0B2440", body="#3D5674", muted="#52698A", accent="#1D5FA6", divider="#CBDCEE",
                 ribbon_dark="#9CC6F0", ribbon_light="#1D5FA6",
                 rings=("#15304F", "#1B3A5E", "#22466F", "#12355C", "#2D5C8F")),
    # Breast health / mammography.
    "pink": dict(dark="#4A0F2E", card="#6B1A45", on_dark="#F8DDE8", accent_dark="#F7B8D1", light="#FDF1F5",
                 ink="#3A0B24", body="#57203D", muted="#74435C", accent="#C2185B", divider="#F1CADA",
                 ribbon_dark="#F48FB1", ribbon_light="#E2457F",
                 rings=("#5E1739", "#6B1A45", "#7A2350", "#5A1438", "#9C3368")),
    # Website teal.
    "teal": dict(dark="#053D38", card="#075E56", on_dark="#CCEFEC", accent_dark="#A5F3EB", light="#EAF9F7",
                 ink="#053D38", body="#065F57", muted="#3F6F6A", accent="#0A7A70", divider="#CCEFEC",
                 ribbon_dark="#A5F3EB", ribbon_light="#0A7A70",
                 rings=("#0A4A44", "#0C554E", "#10625A", "#075E56", "#1D8A80")),
}
H = "font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif"
B = "font-family: 'DM Sans', 'Helvetica Neue', Arial, sans-serif"
INNER = 904  # 1080 - 2 * 88 padding


# ---------- photos ----------
def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

def sharpen(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

def fade_bottom(im, color, start, end):
    w, h = im.size
    over = Image.new("RGB", (w, h), hexrgb(color))
    mask = Image.new("L", (w, h), 0); d = ImageDraw.Draw(mask)
    for y in range(start, h):
        t = min(1.0, (y - start) / max(1, end - start))
        d.line([(0, y), (w, y)], fill=int(255 * (t ** 1.4)))
    return Image.composite(over, im, mask)

def rounded(im, r):
    im = im.convert("RGBA"); w, h = im.size
    m = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], r * 4, fill=255)
    im.putalpha(m.resize((w, h), Image.LANCZOS)); return im

def crop_to(photo, size, photos_dir):
    """photo = {"src": "file.jpg", "crop": [x0, y0, x1, y1]} (crop optional: centre-crop to size ratio)."""
    im = Image.open(pathlib.Path(photos_dir) / photo["src"]).convert("RGB")
    tw, th = size
    if photo.get("crop"):
        im = im.crop(tuple(photo["crop"]))
    else:
        w, h = im.size; r = tw / th
        if w / h > r:
            nw = int(h * r); x0 = (w - nw) // 2; im = im.crop((x0, 0, x0 + nw, h))
        else:
            nh = int(w / r); y0 = (h - nh) // 2; im = im.crop((0, y0, w, y0 + nh))
    return sharpen(im.resize(size, Image.LANCZOS))


class Builder:
    def __init__(self, spec, out, img_url, photos_dir):
        self.s, self.out, self.img_url, self.photos = spec, out, img_url, photos_dir
        self.P = PALETTES[spec.get("palette", "blue")]
        self.use_ribbon = bool(spec.get("ribbon"))
        (out / "img").mkdir(parents=True, exist_ok=True)
        self.n = 0

    # ----- primitives -----
    def save_photo(self, photo, size, kind="plain", radius=28):
        self.n += 1
        im = crop_to(photo, size, self.photos)
        if kind == "fade":
            name = f"p{self.n}.jpg"; fade_bottom(im, self.P["dark"], int(size[1] * 0.62), size[1]).save(self.out / "img" / name, quality=90)
        elif kind == "round":
            name = f"p{self.n}.png"; rounded(im, radius).save(self.out / "img" / name)
        else:
            name = f"p{self.n}.jpg"; im.save(self.out / "img" / name, quality=90)
        return name

    def img(self, name, w, h, style=""):
        return (f'<img src="{self.img_url}{name}" width="{w}" height="{h}" alt="" '
                f'style="display: block; width: {w}px; height: {h}px; {style}">')

    def ribbon(self, w, color, gap):
        h = round(w * 1.5)
        under = "M37 56 C44 84, 66 116, 77 146"
        over_lower = "M23 146 C34 116, 56 84, 63 56"
        over = over_lower + " C70 28, 62 9, 50 9 C38 9, 30 28, 37 56"
        return (f'<svg aria-hidden="true" width="{w}" height="{h}" viewBox="0 0 100 150" style="flex: none; display: block">'
                f'<path d="{under}" fill="none" stroke="{color}" stroke-width="15"></path>'
                f'<path d="{over_lower}" fill="none" stroke="{gap}" stroke-width="23"></path>'
                f'<path d="{over}" fill="none" stroke="{color}" stroke-width="15"></path></svg>')

    def rings(self, right, top):
        r1, r2, r3, fill, stroke = self.P["rings"]
        return (f'<svg aria-hidden="true" width="980" height="980" viewBox="0 0 980 980" style="position: absolute; right: {right}px; top: {top}px">'
                f'<circle cx="490" cy="490" r="470" fill="none" stroke="{r1}" stroke-width="2"></circle>'
                f'<circle cx="490" cy="490" r="380" fill="none" stroke="{r2}" stroke-width="2"></circle>'
                f'<circle cx="490" cy="490" r="290" fill="none" stroke="{r3}" stroke-width="2"></circle>'
                f'<circle cx="490" cy="490" r="200" fill="{fill}" stroke="{stroke}" stroke-width="2"></circle></svg>')

    def page(self, label, dark, inner, w=1080, h=1350):
        P = self.P
        bg, color = (P["dark"], "#FFFFFF") if dark else (P["light"], P["ink"])
        return (f'<div data-document-role="page" data-label="{label}" style="position: relative; width: {w}px; height: {h}px; '
                f'box-sizing: border-box; padding: 88px; overflow: hidden; background: {bg}; color: {color}; {B}; '
                f'display: flex; flex-direction: column; justify-content: space-between">{inner}</div>')

    def wordmark(self, dark, size=24):
        P = self.P
        col = P["accent_dark"] if dark else P["accent"]
        rib = self.ribbon(26, P["ribbon_dark"] if dark else P["ribbon_light"], P["dark"] if dark else P["light"]) if self.use_ribbon else ""
        return (f'<div style="position: relative; display: flex; align-items: center; gap: 16px">{rib}'
                f'<span style="font-size: {size}px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: {col}">Advanced Medical Imaging</span></div>')

    def eyebrow(self, text, color=None, size=26):
        return (f'<div style="font-size: {size}px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; '
                f'color: {color or self.P["muted"]}">{text}</div>')

    def heading(self, title, accent=None, size=76, dark=False, tag="h2", width=INNER):
        acc = ""
        if accent:
            acc = f' <span style="color: {self.P["accent_dark"] if dark else self.P["accent"]}">{accent}</span>'
        return (f'<{tag} style="position: relative; margin: 0; width: {width}px; {H}; font-weight: 800; font-size: {size}px; '
                f'line-height: 1.04; letter-spacing: -0.015em">{title}{acc}</{tag}>')

    def icon(self, kind, color, size):
        paths = {
            "check": '<circle cx="12" cy="12" r="10"></circle><path d="M7.5 12.5l3 3 6-6.5"></path>',
            "arrow": '<path d="M5 12h14"></path><path d="M13 6l6 6-6 6"></path>',
            "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"></path>',
            "cal": '<rect x="3" y="4" width="18" height="18" rx="2"></rect><path d="M16 2v4M8 2v4M3 10h18"></path>',
            "send": '<path d="M22 2L11 13"></path><path d="M22 2l-7 20-4-9-9-4z"></path>',
            "bookmark": '<path d="M6 3h12v18l-6-4-6 4z"></path>',
            "star": '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"></path>',
        }
        fill = color if kind == "star" else "none"
        return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="{color}" '
                f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex: none">{paths[kind]}</svg>')

    def check_rows(self, items, size=36, pad=24):
        P = self.P; rows = []
        for i, t in enumerate(items):
            bb = f"; border-bottom: 2px solid {P['divider']}" if i == len(items) - 1 else ""
            rows.append(f'<div style="display: flex; align-items: center; gap: 28px; padding-block: {pad}px; border-top: 2px solid {P["divider"]}{bb}">'
                        f'{self.icon("check", P["accent"], 56)}<p style="margin: 0; font-size: {size}px; line-height: 1.3; font-weight: 600">{t}</p></div>')
        return '<div style="display: flex; flex-direction: column">' + "".join(rows) + "</div>"

    def foot(self, text, size=26):
        return f'<p style="margin: 0; font-size: {size}px; line-height: 1.45; color: {self.P["muted"]}">{text}</p>' if text else ""

    def top(self, sl, default_size=76):
        eb = self.eyebrow(sl["eyebrow"]) if sl.get("eyebrow") else ""
        if sl.get("save"):
            eb = (f'<div style="display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 700; letter-spacing: 0.14em; '
                  f'text-transform: uppercase; color: {self.P["muted"]}">{self.icon("bookmark", self.P["muted"], 30)}<span>Save this for later</span></div>')
        return (f'<div style="display: flex; flex-direction: column; gap: 26px">{eb}'
                + self.heading(sl["title"], sl.get("title_accent"), sl.get("title_size", default_size)) + "</div>")

    # ----- slide types -----
    def s_hook(self, sl, i):
        P = self.P
        photo = self.save_photo(sl["photo"], (1080, 900), "fade")
        rib = self.ribbon(34, P["ribbon_dark"], P["dark"]) if self.use_ribbon else ""
        eb = (f'<div style="display: flex; align-items: center; gap: 18px">{rib}{self.eyebrow(sl["eyebrow"], P["accent_dark"])}</div>'
              if sl.get("eyebrow") else "")
        return (f'<div data-document-role="page" data-label="Slide {i} Hook" style="position: relative; width: 1080px; height: 1350px; '
                f'overflow: hidden; background: {P["dark"]}; color: #FFFFFF; {B}">'
                + self.img(photo, 1080, 900, "position: absolute; left: 0; top: 0")
                + f'<div style="position: absolute; left: 88px; width: {INNER}px; bottom: 78px; display: flex; flex-direction: column; gap: 30px">'
                + eb + self.heading(sl["title"], sl.get("title_accent"), sl.get("title_size", 80), dark=True, tag="h1")
                + f'<div style="display: flex; align-items: center; justify-content: space-between; padding-top: 6px">'
                f'<div style="display: flex; align-items: center; gap: 16px; font-size: 30px; font-weight: 600">Swipe {self.icon("arrow", "#FFFFFF", 40)}</div>'
                f'<span style="font-size: 22px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: {P["accent_dark"]}">Advanced Medical Imaging</span></div>'
                "</div></div>")

    def s_stat(self, sl, i):
        P = self.P
        card = ""
        if sl.get("card"):
            c = sl["card"]
            card = (f'<div style="display: flex; flex-direction: column; gap: 14px; background: #FFFFFF; border: 2px solid {P["divider"]}; border-radius: 22px; padding: 40px 44px">'
                    f'<span style="font-size: 22px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: {P["muted"]}">{c.get("label", "")}</span>'
                    f'<span style="{H}; font-weight: 800; font-size: 50px; line-height: 1.1">{c["title"]}</span>'
                    f'<span style="font-size: 30px; line-height: 1.4; color: {P["body"]}">{c.get("body", "")}</span></div>')
        return self.page(f"Slide {i}", False,
            self.wordmark(False) + self.top(sl, 74)
            + f'<div style="display: flex; flex-direction: column; gap: 18px">'
            f'<div style="{H}; font-weight: 800; font-size: 180px; line-height: 0.95; letter-spacing: -0.03em; color: {P["accent"]}">{sl["stat"]}</div>'
            f'<p style="margin: 0; font-size: 34px; line-height: 1.4; color: {P["body"]}">{sl["stat_caption"]}</p></div>'
            + card + self.foot(sl.get("source"), 22))

    def s_photo_list(self, sl, i):
        photo = self.save_photo(sl["photo"], (INNER, 500), "round")
        return self.page(f"Slide {i}", False,
            self.wordmark(False) + self.img(photo, INNER, 500) + self.top(sl, 64) + self.check_rows(sl["items"], 36, 22))

    def s_cards(self, sl, i):
        P = self.P
        cards = "".join(
            f'<div style="display: flex; flex-direction: column; gap: 14px; background: #FFFFFF; border: 2px solid {P["divider"]}; '
            f'border-radius: 22px; padding: 38px 36px; min-height: 250px; box-sizing: border-box">'
            f'<span style="{H}; font-weight: 800; font-size: 60px; line-height: 1; letter-spacing: -0.02em; color: {P["accent"]}">{big}</span>'
            f'<span style="font-size: 30px; line-height: 1.35; color: {P["body"]}">{small}</span></div>' for big, small in sl["cards"])
        return self.page(f"Slide {i}", False,
            self.wordmark(False) + self.top(sl, 80)
            + f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px">{cards}</div>' + self.foot(sl.get("footnote"), 28))

    def s_list(self, sl, i):
        return self.page(f"Slide {i}", False,
            self.wordmark(False) + self.top(sl, 76) + self.check_rows(sl["items"], 36, 28) + self.foot(sl.get("footnote"), 28))

    def s_steps(self, sl, i):
        P = self.P
        steps = "".join(
            f'<div style="display: flex; align-items: flex-start; gap: 36px">'
            f'<div style="flex: none; width: 80px; height: 80px; border-radius: 999px; background: {P["accent"]}; color: #FFFFFF; display: flex; '
            f'align-items: center; justify-content: center; {H}; font-weight: 800; font-size: 40px">{n}</div>'
            f'<div style="display: flex; flex-direction: column; gap: 10px; min-width: 0">'
            f'<span style="font-size: 42px; font-weight: 700; line-height: 1.2">{t}</span>'
            f'<span style="font-size: 34px; line-height: 1.4; color: {P["body"]}">{x}</span></div></div>'
            for n, (t, x) in enumerate(sl["steps"], 1))
        return self.page(f"Slide {i}", False,
            self.wordmark(False) + self.top(sl, 84)
            + f'<div style="display: flex; flex-direction: column; gap: 56px">{steps}</div>' + self.foot(sl.get("footnote"), 28))

    def s_quote(self, sl, i):
        """Patient review spotlight. Quote must be verbatim; trims marked with an ellipsis."""
        P = self.P
        stars = "".join(self.icon("star", "#F5B301", 44) for _ in range(5))
        return self.page(f"Slide {i}", True,
            self.rings(-440, 560) + self.wordmark(True)
            + f'<div style="position: relative; display: flex; flex-direction: column; gap: 36px">'
            f'{self.eyebrow(sl.get("eyebrow", "What patients say"), P["accent_dark"])}'
            f'<div style="display: flex; gap: 8px">{stars}</div>'
            f'<p style="margin: 0; width: {INNER}px; {H}; font-weight: 800; font-size: {sl.get("quote_size", 58)}px; line-height: 1.18; letter-spacing: -0.01em">&ldquo;{sl["quote"]}&rdquo;</p>'
            f'<p style="margin: 0; font-size: 32px; color: {P["on_dark"]}">{sl["name"]}, Google review</p></div>'
            + f'<p style="position: relative; margin: 0; font-size: 24px; color: {P["accent_dark"]}">{sl.get("footnote", "Shared from our public Google reviews.")}</p>')

    def s_perspective(self, sl, i):
        """Closing point of view from a real AMI person (wording approved by them). No buttons, no ask."""
        P = self.P
        photo = self.save_photo(sl["photo"], (220, 220), "round", radius=110)
        return self.page(f"Slide {i} Perspective", True,
            self.rings(-440, 560) + self.wordmark(True)
            + f'<div style="position: relative; display: flex; flex-direction: column; gap: 36px">'
            f'{self.eyebrow(sl.get("eyebrow", "Our perspective"), P["accent_dark"])}'
            f'<p style="margin: 0; width: {INNER}px; {H}; font-weight: 800; font-size: {sl.get("quote_size", 52)}px; line-height: 1.2; letter-spacing: -0.01em">&ldquo;{sl["quote"]}&rdquo;</p>'
            f'<div style="display: flex; align-items: center; gap: 30px">{self.img(photo, 220, 220)}'
            f'<div style="display: flex; flex-direction: column; gap: 6px"><span style="font-size: 36px; font-weight: 700">{sl["name"]}</span>'
            f'<span style="font-size: 28px; color: {P["on_dark"]}">{sl.get("role", "")}</span></div></div></div>'
            + f'<p style="position: relative; margin: 0; font-size: 22px; line-height: 1.45; color: {P["accent_dark"]}">{sl.get("disclaimer", "General information, not medical advice.")}</p>')

    def s_cta(self, sl, i):
        P = self.P
        rib = (f'<div style="position: absolute; right: 88px; top: 88px">{self.ribbon(130, P["ribbon_dark"], P["dark"])}</div>'
               if self.use_ribbon else "")
        btn = lambda ic, t: (f'<div style="display: flex; align-items: center; gap: 28px; background: {P["card"]}; border-radius: 20px; padding: 32px 40px">'
                             f'{self.icon(ic, P["accent_dark"], 52)}<span style="font-size: 40px; font-weight: 700">{t}</span></div>')
        return self.page(f"Slide {i} CTA", True,
            self.rings(-440, -420) + rib + self.wordmark(True)
            + self.heading(sl["title"], sl.get("title_accent"), sl.get("title_size", 88), dark=True, width=740 if self.use_ribbon else INNER)
            + f'<div style="position: relative; display: flex; flex-direction: column; gap: 20px">'
            + btn("phone", sl.get("phone_line", "Call (727) 398-5999")) + btn("cal", sl.get("book_line", "Book through the link in our bio")) + "</div>"
            + f'<div style="position: relative; display: flex; flex-direction: column; gap: 32px">'
            f'<div style="display: flex; align-items: center; gap: 24px; font-size: 34px; line-height: 1.35; color: {P["on_dark"]}">'
            f'{self.icon("send", "#FFFFFF", 46)}<span>{sl.get("share", "Know someone who needs this? Send it to them.")}</span></div>'
            f'<p style="margin: 0; font-size: 22px; line-height: 1.45; color: {P["accent_dark"]}">{sl.get("disclaimer", "General information, not medical advice. Coverage and costs vary by plan.")}</p></div>')

    # ----- other formats -----
    def single(self, sp):
        """1080x1350 single image (organic single post or ad creative)."""
        P = self.P
        photo = self.save_photo(sp["photo"], (INNER, 494), "round")
        rib = self.ribbon(30, P["ribbon_dark"], P["dark"]) if self.use_ribbon else ""
        lines = "".join(f"<span>{l}</span>" for l in sp.get("lines", []))
        return self.page("Single", True,
            self.rings(-420, 640) + self.wordmark(True) + self.img(photo, INNER, 494, "position: relative")
            + f'<div style="position: relative; display: flex; flex-direction: column; gap: 26px">'
            + (f'<div style="display: flex; align-items: center; gap: 16px">{rib}{self.eyebrow(sp["eyebrow"], P["accent_dark"])}</div>' if sp.get("eyebrow") else "")
            + self.heading(sp["title"], sp.get("title_accent"), sp.get("title_size", 76), dark=True, tag="h1")
            + f'<div style="display: flex; flex-direction: column; gap: 6px; font-size: 32px; line-height: 1.35; color: {P["on_dark"]}">{lines}</div></div>'
            + f'<div style="position: relative; display: flex; align-items: center; justify-content: space-between">'
            f'<div style="background: {P["accent_dark"]}; color: {P["dark"]}; border-radius: 999px; padding: 24px 44px; font-size: 36px; font-weight: 700">{sp.get("button", "Book at advancedimg.com")}</div>'
            f'<span style="font-size: 24px; color: {P["on_dark"]}">{sp.get("footer", "9555 Seminole Blvd")}</span></div>')

    def gbp(self, g):
        """1200x900 (4:3) image for Google Business Profile posts: photo left, text right."""
        P = self.P
        photo = self.save_photo(g["photo"], (600, 900))
        rib = self.ribbon(24, P["ribbon_dark"], P["dark"]) if self.use_ribbon else ""
        return (f'<div data-document-role="page" data-label="Google 4x3" style="position: relative; width: 1200px; height: 900px; overflow: hidden; '
                f'background: {P["dark"]}; color: #FFFFFF; {B}; display: flex">'
                + self.img(photo, 600, 900)
                + f'<div style="width: 600px; box-sizing: border-box; padding: 64px 56px; display: flex; flex-direction: column; justify-content: space-between">'
                f'<div style="display: flex; align-items: center; gap: 14px">{rib}<span style="font-size: 20px; font-weight: 600; letter-spacing: 0.14em; '
                f'text-transform: uppercase; color: {P["accent_dark"]}">Advanced Medical Imaging</span></div>'
                f'<div style="display: flex; flex-direction: column; gap: 24px">'
                + (self.eyebrow(g["eyebrow"], P["accent_dark"], 20) if g.get("eyebrow") else "")
                + self.heading(g["title"], g.get("title_accent"), g.get("title_size", 54), dark=True, tag="h1", width=488)
                + (f'<p style="margin: 0; width: 488px; font-size: 24px; line-height: 1.4; color: {P["on_dark"]}">{g["sub"]}</p>' if g.get("sub") else "")
                + "</div>"
                f'<div style="align-self: flex-start; background: {P["accent_dark"]}; color: {P["dark"]}; border-radius: 999px; padding: 18px 34px; '
                f'font-size: 26px; font-weight: 700">{g.get("button", "Book at advancedimg.com")}</div></div></div>')


FONT_CACHE = pathlib.Path.home() / ".cache" / "ami-fonts"

def head(title, preview):
    if preview:
        F = FONT_CACHE / "node_modules" / "@fontsource"
        if not (F / "inter").exists():
            FONT_CACHE.mkdir(parents=True, exist_ok=True)
            subprocess.run(["npm", "i", "--silent", "--prefix", str(FONT_CACHE), "@fontsource/inter@5.0.18", "@fontsource/dm-sans@5.0.21"], check=True)
        faces = "".join(f"@font-face{{font-family:'Inter';font-weight:{w};src:url(file://{F}/inter/files/inter-latin-{w}-normal.woff2)}}" for w in (600, 700, 800))
        faces += "".join(f"@font-face{{font-family:'DM Sans';font-weight:{w};src:url(file://{F}/dm-sans/files/dm-sans-latin-{w}-normal.woff2)}}" for w in (400, 500, 600, 700))
        fonts = f"<style>{faces}</style>"
    else:
        fonts = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800'
                 '&amp;family=DM+Sans:wght@400;500;600;700&amp;display=swap">')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
            f'<title>{title}</title>{fonts}<style>html,body{{margin:0;padding:0;background:#fff}}</style></head><body>')


def render(out, files):
    """Screenshot every page and make a contact sheet (preview mode)."""
    from playwright.sync_api import sync_playwright
    shots = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1200, "height": 1350})
        for f in files:
            pg.goto(f"file://{out}/{f}"); pg.wait_for_timeout(600)
            els = pg.locator('[data-document-role="page"]')
            problems = pg.evaluate("""() => [...document.querySelectorAll('[data-document-role=page]')].flatMap((p, i) => {
              const r = p.getBoundingClientRect();
              return [...p.querySelectorAll('h1,h2,p,span,img')].filter(e => { const q = e.getBoundingClientRect();
                return q.width && (q.bottom > r.bottom + 1 || q.right > r.right + 1 || q.left < r.left - 1); })
                .map(e => `page ${i+1}: ${e.tagName} "${(e.textContent||'').slice(0,40)}" runs off the page`)})""")
            for pr in problems: print("WARNING", f, pr)
            for k in range(els.count()):
                path = out / f"{f[:-5]}-{k + 1}.png"; els.nth(k).screenshot(path=str(path)); shots.append(path)
        b.close()
    ims = [Image.open(s).convert("RGB") for s in shots]
    W = 360
    rows = [ims[i:i + 4] for i in range(0, len(ims), 4)]
    heights = [max(int(im.height * W / im.width) for im in r) for r in rows]
    sheet = Image.new("RGB", (4 * W + 50, sum(heights) + 10 * (len(rows) + 1)), "#E5E7EB")
    y = 10
    for r, hgt in zip(rows, heights):
        for k, im in enumerate(r):
            sheet.paste(im.resize((W, int(im.height * W / im.width))), (10 + k * (W + 10), y))
        y += hgt + 10
    sheet.save(out / "sheet.jpg", quality=88)
    print("preview sheet:", out / "sheet.jpg")


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
    b = Builder(spec, out, "img/" if preview else f"{BASE_URL}{slug}/img/", photos)
    kinds = {"hook": b.s_hook, "stat": b.s_stat, "photo_list": b.s_photo_list, "cards": b.s_cards,
             "list": b.s_list, "steps": b.s_steps, "quote": b.s_quote, "perspective": b.s_perspective, "cta": b.s_cta}
    files = []
    if spec.get("slides"):
        pages = [kinds[sl["type"]](sl, i) for i, sl in enumerate(spec["slides"], 1)]
        (out / "carousel.html").write_text(head(spec.get("title", slug), preview) + "\n".join(pages) + "</body></html>"); files.append("carousel.html")
    if spec.get("single"):
        (out / "single.html").write_text(head(slug + " single", preview) + b.single(spec["single"]) + "</body></html>"); files.append("single.html")
    if spec.get("gbp"):
        (out / "gbp.html").write_text(head(slug + " google", preview) + b.gbp(spec["gbp"]) + "</body></html>"); files.append("gbp.html")
    print("built", out, files)
    if preview:
        render(out, files)
    else:
        for f in files:
            print("import URL:", f"{BASE_URL}{slug}/{f}")


if __name__ == "__main__":
    main()
