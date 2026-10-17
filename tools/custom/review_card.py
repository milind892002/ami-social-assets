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
    """s = scale (1.0 for the 1200x1800 card)."""
    px = lambda v: f"{round(v * s)}px"
    return f'''<div data-document-role="page" data-label="{label}" style="position: relative; width: {w}px; height: {h}px; overflow: hidden; background: #FFFFFF; box-sizing: border-box; padding: {px(90)} {px(96)}; display: flex; flex-direction: column; align-items: center; text-align: center; color: {INK}; {B}">
  <img src="{IMG}logo.png" alt="Advanced Medical Imaging" style="width: {px(620)}; height: auto; margin-top: {px(10)}">
  <div style="width: {px(140)}; height: {px(8)}; border-radius: 99px; background: {TEAL}; margin: {px(56)} 0 {px(52)}"></div>
  <div style="{H}; font-weight: 800; font-size: {px(104)}; line-height: 1.05; letter-spacing: -0.02em">How did we do<br>today?</div>
  <div style="font-size: {px(44)}; line-height: 1.35; color: #3F5A56; margin-top: {px(36)}; max-width: {px(900)}">Your Google review helps neighbors find imaging care they can trust.</div>
  <div style="margin-top: {px(64)}; padding: {px(34)}; border-radius: {px(40)}; background: {SOFT}; border: {px(4)} solid {LINE}">
    <img src="{IMG}qr.png" alt="QR code to leave a Google review" style="display: block; width: {px(470)}; height: {px(470)}; border-radius: {px(14)}">
  </div>
  <div style="{H}; font-weight: 700; font-size: {px(50)}; color: {TEAL}; margin-top: {px(44)}">Scan to review us on Google</div>
  <div style="font-size: {px(38)}; color: #3F5A56; margin-top: {px(14)}">Takes about a minute. Thank you!</div>
  <div style="position: absolute; left: 0; right: 0; bottom: 0; background: {INK}; color: #FFFFFF; padding: {px(40)} {px(60)}; font-size: {px(34)}; line-height: 1.45">
    <span style="font-weight: 700">Seminole</span> 9555 Seminole Blvd &nbsp;·&nbsp; <span style="font-weight: 700">St. Pete</span> 2201 Central Ave<br>(727) 398-5999 &nbsp;·&nbsp; advancedimg.com
  </div>
</div>'''

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "card.html").write_text(head("AMI review card 4x6") + page("Review card 4x6", 1200, 1800, 1.0) + "</body></html>")
(OUT / "sign.html").write_text(head("AMI review sign 5x7") + page("Counter sign 5x7", 1500, 2100, 1.2) + "</body></html>")
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
