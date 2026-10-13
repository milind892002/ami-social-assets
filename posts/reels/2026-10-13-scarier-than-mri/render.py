import sys
from playwright.sync_api import sync_playwright
fps=30; dur=17.0
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/reel/reel.html'); pg.wait_for_timeout(800)
    import os; os.makedirs('frames',exist_ok=True)
    for i in range(int(fps*dur)):
        pg.evaluate(f'setT({i/fps})')
        pg.screenshot(path=f'frames/f{i:04d}.jpg',type='jpeg',quality=92)
    b.close()
