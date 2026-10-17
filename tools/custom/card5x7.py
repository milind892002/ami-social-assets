"""Two-sided 5x7 patient card for Canva import: front = Google review ask, back = self-pay prices.

Usage: python3 tools/custom/card5x7.py [--preview]
Pages are 1500x2100 px (5x7 in at 300 dpi). Fonts: Inter + DM Sans only.
Review QR = Seminole Google profile (place id ChIJ9T1Dg6T7wogRn7zymMqhyzU). No incentives, ask everyone.
Prices copied from amiweb src/app/pricing/page.tsx (origin/main 12ebf58, Oct 17 2026). Re-check before reprinting.
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
SLUG = "2026-10-17-card-5x7"
OUT = ROOT / "imports" / SLUG
BASE = f"https://milind892002.github.io/ami-social-assets/imports/{SLUG}/"
PREVIEW = "--preview" in sys.argv
IMG = "img/" if PREVIEW else BASE + "img/"
W, HT = 1500, 2100
INK, TEAL, SOFT, LINE, MUTED, MINT = "#16302D", "#0A7A70", "#EAF5F3", "#D5E2DF", "#3F5A56", "#A5F3EB"
H = "font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif"
B = "font-family: 'DM Sans', 'Helvetica Neue', Arial, sans-serif"
REVIEW = "https://search.google.com/local/writereview?placeid=ChIJ9T1Dg6T7wogRn7zymMqhyzU"
BOOK = "https://www.advancedimg.com/schedule?utm_source=print&utm_medium=card&utm_campaign=review-card-prices"

LEFT = [
    ("MRI", [("MRI, no contrast", "$295", 0), ("MRI with/without contrast", "$395", 0),
             ("Prostate MRI (PI-RADS)", "$499", 1), ("NeuroQuant brain MRI", "$999", 0),
             ("Whole-body MRI", "$1,499", 1)]),
    ("CT", [("CT, no contrast", "$295", 0), ("CT with/without contrast", "$395", 0),
            ("Heart calcium score", "$99", 1), ("Lung screening CT", "$150", 1),
            ("Cleerly coronary CTA", "$1,399", 1)]),
]
RIGHT = [
    ("Ultrasound", [("Ultrasound, routine", "$195", 0), ("Echocardiogram", "$250", 0),
                    ("Vascular, one side", "$150", 0), ("Vascular, both sides", "$250", 0)]),
    ("Mammogram", [("Screening 2D", "$195", 1), ("3D mammogram", "$249", 1)]),
    ("DEXA", [("Bone density", "$75", 1), ("Body composition", "$100", 1)]),
    ("X-ray", [("Per body part", "$50", 0)]),
]

def head(title):
    if PREVIEW:
        F = pathlib.Path.home() / ".cache/ami-fonts/node_modules/@fontsource"
        faces = "".join(f"@font-face{{font-family:'Inter';font-weight:{w};src:url(file://{F}/inter/files/inter-latin-{w}-normal.woff2)}}" for w in (600, 700, 800))
        faces += "".join(f"@font-face{{font-family:'DM Sans';font-weight:{w};src:url(file://{F}/dm-sans/files/dm-sans-latin-{w}-normal.woff2)}}" for w in (400, 500, 700))
        fonts = f"<style>{faces}</style>"
    else:
        fonts = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800'
                 '&amp;family=DM+Sans:wght@400;500;700&amp;display=swap">')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
            f'<title>{title}</title>{fonts}<style>html,body{{margin:0;padding:0;background:#fff}}</style></head><body>')

def front():
    corner = 300
    addr = lambda city, l1, l2: (
        f'<div style="flex: 1; text-align: center"><div style="font-size: 34px; font-weight: 700; letter-spacing: 0.14em; color: {MINT}">{city}</div>'
        f'<div style="font-size: 38px; line-height: 1.35; margin-top: 8px">{l1}<br>{l2}</div></div>')
    return f'''<div data-document-role="page" data-label="Front: review" style="position: relative; width: {W}px; height: {HT}px; overflow: hidden; background: #FFFFFF; color: {INK}; {B}">
  <div style="position: absolute; left: 0; top: 0; width: {corner}px; height: {corner}px; background: {TEAL}; border-radius: 0 0 {corner}px 0"></div>
  <img src="{IMG}flip.png" alt="" style="position: absolute; left: 44px; top: 40px; width: 72px; height: 72px">
  <div style="position: absolute; left: 44px; top: 118px; {H}; font-weight: 800; font-size: 54px; line-height: 1; color: #FFFFFF; letter-spacing: 0.04em">FLIP</div>
  <div style="position: absolute; left: 46px; top: 180px; font-size: 28px; font-weight: 700; line-height: 1.1; color: {MINT}">for prices</div>
  <div style="position: absolute; left: 0; right: 0; top: 0; height: {HT - 400}px; box-sizing: border-box; padding: 110px 110px 50px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center">
    <img src="{IMG}logo.png" alt="Advanced Medical Imaging" style="display: block; width: 900px; height: auto">
    <div style="width: 140px; height: 9px; border-radius: 99px; background: {TEAL}; margin: 50px 0"></div>
    <div style="{H}; font-weight: 800; font-size: 120px; line-height: 1.04; letter-spacing: -0.02em">How did we do today?</div>
    <div style="font-size: 50px; line-height: 1.4; color: {MUTED}; margin-top: 30px; width: 1080px">Your Google review helps neighbors find imaging care they can trust.</div>
    <div style="margin-top: 60px; padding: 36px; border-radius: 42px; background: {SOFT}; border: 5px solid {LINE}">
      <img src="{IMG}qr-review.png" alt="QR code to leave a Google review" style="display: block; width: 540px; height: 540px; border-radius: 14px">
    </div>
    <div style="{H}; font-weight: 700; font-size: 58px; color: {TEAL}; margin-top: 44px">Scan to review us on Google</div>
    <div style="font-size: 42px; color: {MUTED}; margin-top: 12px">Takes about a minute. Thank you!</div>
  </div>
  <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 400px; background: {INK}; color: #FFFFFF; box-sizing: border-box; padding: 50px 60px 44px; display: flex; flex-direction: column; justify-content: space-between">
    <div style="display: flex; gap: 40px">{addr("SEMINOLE", "9555 Seminole Blvd, Suite 101", "Seminole, FL 33772")}{addr("ST. PETERSBURG", "2201 Central Ave, Suite 100", "St. Petersburg, FL 33713")}</div>
    <div style="{H}; font-size: 54px; font-weight: 700; text-align: center">(727) 398-5999 &nbsp;·&nbsp; advancedimg.com</div>
  </div>
</div>'''

def section(title, rows):
    out = (f'<div style="{H}; font-weight: 800; font-size: 42px; color: {TEAL}; letter-spacing: 0.06em; '
           f'text-transform: uppercase; padding-bottom: 10px; border-bottom: 5px solid {TEAL}; margin-bottom: 4px">{title}</div>')
    for name, price, scr in rows:
        dot = f'<div style="flex: 0 0 18px; width: 18px; height: 18px; border-radius: 99px; background: {TEAL if scr else "#FFFFFF"}"></div>'
        out += (f'<div style="display: flex; align-items: center; gap: 16px; padding: 17px 0; '
                f'border-bottom: 2px solid {LINE}; font-size: 37px; line-height: 1.2">{dot}'
                f'<div style="flex: 1; color: {INK}; font-weight: {700 if scr else 400}">{name}</div>'
                f'<div style="{H}; font-weight: 800; font-size: 40px; color: {INK}; white-space: nowrap">{price}</div></div>')
    return f'<div style="margin-bottom: 44px">{out}</div>'

def back():
    col = lambda secs: "".join(section(t, r) for t, r in secs)
    perks = "".join(
        f'<div style="background: rgba(255,255,255,0.12); border-radius: 99px; padding: 12px 28px; font-size: 34px; font-weight: 500">{t}</div>'
        for t in ("No referral needed", "Radiologist read included", "Same-day often available"))
    return f'''<div data-document-role="page" data-label="Back: self-pay prices" style="position: relative; width: {W}px; height: {HT}px; overflow: hidden; background: #FFFFFF; color: {INK}; {B}">
  <div style="position: absolute; left: 0; right: 0; top: 0; height: 380px; background: {INK}; color: #FFFFFF; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center">
    <div style="font-size: 36px; font-weight: 700; letter-spacing: 0.16em; color: {MINT}">NO INSURANCE? NO PROBLEM.</div>
    <div style="{H}; font-weight: 800; font-size: 116px; line-height: 1.05; letter-spacing: -0.02em; margin-top: 14px">Self-pay prices</div>
    <div style="display: flex; gap: 16px; margin-top: 30px; color: #FFFFFF">{perks}</div>
  </div>
  <div style="position: absolute; left: 80px; right: 80px; top: 440px; display: flex; gap: 70px">
    <div style="flex: 1">{col(LEFT)}</div>
    <div style="flex: 1">{col(RIGHT)}</div>
  </div>
  <div style="position: absolute; left: 80px; right: 80px; top: 1652px; font-size: 30px; color: {MUTED}; display: flex; align-items: center; gap: 14px">
    <div style="flex: 0 0 18px; width: 18px; height: 18px; border-radius: 99px; background: {TEAL}"></div>
    <div>Popular screenings. Ask about payment plans and HSA/FSA receipts.</div>
  </div>
  <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 370px; background: {SOFT}; border-top: 5px solid {LINE}; display: flex; align-items: center; box-sizing: border-box; padding: 0 80px; gap: 50px">
    <div style="background: #FFFFFF; border-radius: 26px; padding: 16px; border: 4px solid {LINE}">
      <img src="{IMG}qr-book.png" alt="QR code to request an appointment" style="display: block; width: 240px; height: 240px">
    </div>
    <div style="flex: 1">
      <div style="{H}; font-weight: 800; font-size: 56px; color: {INK}">Scan to book, or call</div>
      <div style="{H}; font-weight: 800; font-size: 66px; color: {TEAL}; margin-top: 4px">(727) 398-5999</div>
      <div style="font-size: 26px; line-height: 1.4; color: {MUTED}; margin-top: 14px">Prompt-pay prices for uninsured and self-pay patients who pay at the time of service; not for insurance claims. Prices as of October 2026 and subject to change; we confirm your price before your visit. 3T MRI also in St.&nbsp;Petersburg.</div>
    </div>
  </div>
</div>'''

def build_images():
    import qrcode, shutil
    from PIL import Image, ImageDraw
    d = OUT / "img"; d.mkdir(parents=True, exist_ok=True)
    for name, url in (("qr-review.png", REVIEW), ("qr-book.png", BOOK)):
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=16, border=1)
        q.add_data(url); q.make(fit=True)
        q.make_image(fill_color=INK if "book" in name else "#000000", back_color="white").save(d / name)
    shutil.copy(ROOT / "tools/brand/lockup_pill.png", d / "logo.png")
    # flip arrow icon (white on transparent), drawn at 4x then downsampled
    import math
    S = 288; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    c, R, r = S / 2, S * 0.40, S * 0.25
    dr.arc([c - R, c - R, c + R, c + R], start=40, end=-50 + 360 - 0, fill="white", width=int(R - r))
    a = math.radians(-50); m = (R + r) / 2; mx, my = c + m * math.cos(a), c + m * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a); nx, ny = math.cos(a), math.sin(a); L = S * 0.22
    dr.polygon([(mx + nx * L, my + ny * L), (mx - nx * L, my - ny * L), (mx - tx * L * 1.1, my - ty * L * 1.1)], fill="white")
    im.resize((144, 144), Image.LANCZOS).save(d / "flip.png")

OUT.mkdir(parents=True, exist_ok=True)
build_images()
(OUT / "card.html").write_text(head("AMI patient card 5x7") + front() + back() + "</body></html>")
(OUT / "index.html").write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>Temporary media</title></head><body></body></html>')
print("wrote", OUT)
if PREVIEW:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": W, "height": HT * 2}); pg.goto(f"file://{OUT}/card.html"); pg.wait_for_timeout(800)
        info = pg.evaluate("""() => [...document.querySelectorAll('[data-document-role=page]')].map(p => { const r=p.getBoundingClientRect();
          return [...p.querySelectorAll('*')].filter(e=>{const q=e.getBoundingClientRect(); return q.bottom>r.bottom+1||q.right>r.right+1}).length })""")
        for i, el in enumerate(pg.query_selector_all('[data-document-role=page]')):
            el.screenshot(path=str(OUT / f"preview-{i+1}.png"))
        print("overflow per page:", info)
        b.close()
