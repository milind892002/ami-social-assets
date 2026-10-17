"""Patient review card (4x6 handout) and counter sign (5x7), for Canva import.

Usage: python3 tools/custom/review_card.py [--preview]
QR = Google 'write a review' link for the Seminole profile (place id ChIJ9T1Dg6T7wogRn7zymMqhyzU).
Wording follows Google's review policy: ask everyone, no incentives, no star requests.
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
SLUG = "2026-10-17-review-card"
OUT = ROOT / "imports" / SLUG
BASE = f"https://milind892002.github.io/ami-social-assets/imports/{SLUG}/"
PREVIEW = "--preview" in sys.argv
IMG = "img/" if PREVIEW else BASE + "img/"
INK, TEAL, PURPLE, SOFT, LINE = "#16302D", "#0A7A70", "#6B2F80", "#EAF5F3", "#D5E2DF"
H = "font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif"
B = "font-family: 'DM Sans', 'Helvetica Neue', Arial, sans-serif"

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

def page(label, w, h, s):
    """s = scale (1.0 for the 1200x1800 card). Body is centered in the space above the footer."""
    px = lambda v: f"{round(v * s)}px"
    foot = round(230 * s)
    return f'''<div data-document-role="page" data-label="{label}" style="position: relative; width: {w}px; height: {h}px; overflow: hidden; background: #FFFFFF; color: {INK}; {B}">
  <div style="position: absolute; left: 0; right: 0; top: 0; height: {h - foot}px; box-sizing: border-box; padding: {px(70)} {px(90)}; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center">
    <img src="{IMG}logo.png" alt="Advanced Medical Imaging" style="display: block; width: {px(880)}; height: auto">
    <div style="width: {px(120)}; height: {px(8)}; border-radius: 99px; background: {TEAL}; margin: {px(46)} 0 {px(46)}"></div>
    <div style="{H}; font-weight: 800; font-size: {px(100)}; line-height: 1.06; letter-spacing: -0.02em">How did we do today?</div>
    <div style="font-size: {px(42)}; line-height: 1.4; color: #3F5A56; margin-top: {px(28)}; width: {px(880)}">Your Google review helps neighbors find imaging care they can trust.</div>
    <div style="margin-top: {px(56)}; padding: {px(30)}; border-radius: {px(36)}; background: {SOFT}; border: {px(4)} solid {LINE}">
      <img src="{IMG}qr.png" alt="QR code to leave a Google review" style="display: block; width: {px(460)}; height: {px(460)}; border-radius: {px(12)}">
    </div>
    <div style="{H}; font-weight: 700; font-size: {px(48)}; color: {TEAL}; margin-top: {px(40)}">Scan to review us on Google</div>
    <div style="font-size: {px(36)}; color: #3F5A56; margin-top: {px(12)}">Takes about a minute. Thank you!</div>
  </div>
  <div style="position: absolute; left: 0; right: 0; bottom: 0; height: {foot}px; background: {INK}; color: #FFFFFF; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: {px(10)}; text-align: center">
    <div style="font-size: {px(30)}; font-weight: 500; letter-spacing: 0.14em; color: #A5F3EB">SEMINOLE  ·  ST. PETERSBURG</div>
    <div style="{H}; font-size: {px(44)}; font-weight: 700">(727) 398-5999  ·  advancedimg.com</div>
  </div>
</div>'''

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "card.html").write_text(head("AMI review card 4x6") + page("Review card 4x6", 1200, 1800, 1.0) + "</body></html>")
(OUT / "sign.html").write_text(head("AMI review sign 5x7") + page("Counter sign 5x7", 1500, 2100, 1.22) + "</body></html>")
(OUT / "index.html").write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>Temporary media</title></head><body></body></html>')
print("wrote", OUT)
if PREVIEW:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        for f, (w, h) in {"card": (1200, 1800), "sign": (1500, 2100)}.items():
            pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(f"file://{OUT}/{f}.html"); pg.wait_for_timeout(700)
            over = pg.evaluate("""() => { const p=document.querySelector('[data-document-role=page]'); const r=p.getBoundingClientRect();
              return [...p.querySelectorAll('*')].filter(e=>{const q=e.getBoundingClientRect(); return q.bottom>r.bottom+1||q.right>r.right+1}).length }""")
            pg.screenshot(path=str(OUT / f"preview-{f}.png")); print(f, "overflow elements:", over)
        b.close()
