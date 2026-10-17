"""Back of the 4x6 review card: self-pay price list, for Canva import (then merged as page 2 of DAHYRzQ_b-4).

Usage: python3 tools/custom/price_back.py [--preview]
Prices copied from amiweb src/app/pricing/page.tsx (origin/main 12ebf58, Oct 17 2026). Re-check before reprinting.
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
SLUG = "2026-10-17-price-back"
OUT = ROOT / "imports" / SLUG
BASE = f"https://milind892002.github.io/ami-social-assets/imports/{SLUG}/"
PREVIEW = "--preview" in sys.argv
IMG = "img/" if PREVIEW else BASE + "img/"
INK, TEAL, SOFT, LINE, MUTED, MINT = "#16302D", "#0A7A70", "#EAF5F3", "#D5E2DF", "#3F5A56", "#A5F3EB"
H = "font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif"
B = "font-family: 'DM Sans', 'Helvetica Neue', Arial, sans-serif"
BOOK = "https://www.advancedimg.com/schedule?utm_source=print&utm_medium=card&utm_campaign=review-card-prices"

# (name, price, screening?)
LEFT = [
    ("MRI", [("MRI, no contrast", "$295", 0), ("MRI with/without contrast", "$395", 0),
             ("Prostate MRI (PI-RADS)", "$499", 1), ("NeuroQuant brain MRI", "$999", 0),
             ("Whole-body MRI", "$1,499", 1)]),
    ("CT", [("CT, no contrast", "$295", 0), ("CT with/without contrast", "$395", 0),
            ("Heart calcium score", "$99", 1), ("Lung cancer screening CT", "$150", 1),
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

def section(title, rows):
    out = (f'<div style="{H}; font-weight: 800; font-size: 34px; color: {TEAL}; letter-spacing: 0.06em; '
           f'text-transform: uppercase; padding-bottom: 8px; border-bottom: 4px solid {TEAL}; margin-bottom: 4px">{title}</div>')
    for name, price, scr in rows:
        dot = (f'<span style="display: inline-block; width: 14px; height: 14px; border-radius: 99px; background: {TEAL}; '
               f'margin-right: 12px; vertical-align: middle; position: relative; top: -2px"></span>') if scr else \
              '<span style="display: inline-block; width: 14px; margin-right: 12px"></span>'
        out += (f'<div style="display: flex; justify-content: space-between; align-items: baseline; padding: 14px 0; '
                f'border-bottom: 2px solid {LINE}; font-size: 30px; line-height: 1.2">'
                f'<span style="color: {INK}; font-weight: {700 if scr else 400}">{dot}{name}</span>'
                f'<span style="{H}; font-weight: 800; font-size: 32px; color: {INK}; white-space: nowrap; margin-left: 12px">{price}</span></div>')
    return f'<div style="margin-bottom: 34px">{out}</div>'

def page():
    col = lambda secs: "".join(section(t, r) for t, r in secs)
    perks = "".join(
        f'<div style="background: rgba(255,255,255,0.10); border-radius: 99px; padding: 10px 24px; font-size: 28px; font-weight: 500">{t}</div>'
        for t in ("No referral needed", "Radiologist read included", "Same-day often available"))
    return f'''<div data-document-role="page" data-label="Self-pay prices (back)" style="position: relative; width: 1200px; height: 1800px; overflow: hidden; background: #FFFFFF; color: {INK}; {B}">
  <div style="position: absolute; left: 0; right: 0; top: 0; height: 330px; background: {INK}; color: #FFFFFF; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center">
    <div style="font-size: 30px; font-weight: 700; letter-spacing: 0.16em; color: {MINT}">NO INSURANCE? NO PROBLEM.</div>
    <div style="{H}; font-weight: 800; font-size: 96px; line-height: 1.05; letter-spacing: -0.02em; margin-top: 14px">Self-pay prices</div>
    <div style="display: flex; gap: 14px; margin-top: 28px; color: #FFFFFF">{perks}</div>
  </div>
  <div style="position: absolute; left: 70px; right: 70px; top: 380px; display: flex; gap: 60px">
    <div style="flex: 1">{col(LEFT)}</div>
    <div style="flex: 1">{col(RIGHT)}</div>
  </div>
  <div style="position: absolute; left: 70px; right: 70px; top: 1396px; font-size: 24px; color: {MUTED}; display: flex; align-items: center; gap: 12px">
    <span style="display: inline-block; width: 14px; height: 14px; border-radius: 99px; background: {TEAL}"></span>
    <span>Popular screenings. Ask about payment plans and HSA/FSA receipts.</span>
  </div>
  <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 340px; background: {SOFT}; border-top: 4px solid {LINE}; display: flex; align-items: center; box-sizing: border-box; padding: 0 70px; gap: 44px">
    <div style="background: #FFFFFF; border-radius: 22px; padding: 14px; border: 3px solid {LINE}">
      <img src="{IMG}qr-book.png" alt="QR code to request an appointment" style="display: block; width: 200px; height: 200px">
    </div>
    <div style="flex: 1">
      <div style="{H}; font-weight: 800; font-size: 46px; color: {INK}">Scan to book, or call</div>
      <div style="{H}; font-weight: 800; font-size: 54px; color: {TEAL}; margin-top: 4px">(727) 398-5999</div>
      <div style="font-size: 21px; line-height: 1.4; color: {MUTED}; margin-top: 14px">Prompt-pay prices for uninsured and self-pay patients who pay at the time of service; not for insurance claims. Prices as of October 2026 and subject to change; we confirm your exact price before your visit. 3T MRI also in St.&nbsp;Petersburg.</div>
    </div>
  </div>
</div>'''

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "img").mkdir(exist_ok=True)
import qrcode
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=1)
qr.add_data(BOOK); qr.make(fit=True)
qr.make_image(fill_color=INK, back_color="white").save(OUT / "img" / "qr-book.png")
(OUT / "back.html").write_text(head("AMI self-pay prices (card back)") + page() + "</body></html>")
(OUT / "index.html").write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>Temporary media</title></head><body></body></html>')
print("wrote", OUT)
if PREVIEW:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1200, "height": 1800}); pg.goto(f"file://{OUT}/back.html"); pg.wait_for_timeout(700)
        info = pg.evaluate("""() => { const p=document.querySelector('[data-document-role=page]'); const r=p.getBoundingClientRect();
          const cols=p.children[1].getBoundingClientRect(); return {colsBottom: Math.round(cols.bottom),
          over: [...p.querySelectorAll('*')].filter(e=>{const q=e.getBoundingClientRect(); return q.bottom>r.bottom+1||q.right>r.right+1}).length} }""")
        pg.screenshot(path=str(OUT / "preview-back.png")); print(info)
        b.close()
