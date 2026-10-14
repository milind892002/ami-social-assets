# build_post.py

Turns a short JSON description of a post into Canva-importable HTML.

    python3 tools/build_post.py posts/<slug>.json --preview   # render locally, check preview/<slug>/sheet.jpg
    python3 tools/build_post.py posts/<slug>.json             # build imports/<slug>/ for Canva import
    --photos DIR   where photo "src" paths live (default: /home/claude/amiweb/public/images)

Needs Python 3 with Pillow; preview needs Playwright (Chromium) and npm (fonts are fetched once into ~/.cache/ami-fonts).

## Spec

    {
      "slug": "2026-10-12-mri-what-to-expect",   // also the folder name
      "title": "optional page title",
      "palette": "blue" | "pink" | "teal",       // blue = default brand, pink = breast health, teal = website
      "ribbon": false,                           // awareness ribbon (breast health only)
      "slides": [ ... ],                         // carousel, 1080x1350 each
      "single": { ... },                         // optional single image 1080x1350 (ads)
      "gbp": { ... }                             // optional Google Business Profile image 1200x900
    }

Text fields accept simple HTML entities (&#39; for apostrophes, &gt; for >). Keep headlines short:
hook 2 to 3 lines at 80px, other headings 2 lines.

Photo object: `{"src": "file.jpg", "crop": [x0, y0, x1, y1]}`. Crop is optional (centre crop to the
slot's shape). Use crop to keep faces in frame and to cut out off-topic details.

## Slide types

| type | fields |
|---|---|
| hook | photo, eyebrow, title, title_accent, title_size (80) |
| stat | eyebrow, title, title_accent, stat, stat_caption, card {label, title, body}, source |
| photo_list | photo, eyebrow, title, items [3] |
| cards | eyebrow, title, cards [[big, small] x4], footnote |
| list | eyebrow or save: true, title, items [3-4], footnote |
| steps | eyebrow, title, steps [[title, text] x3], footnote |
| quote | quote (verbatim review), name ("First L."), eyebrow, footnote |
| cta | title, title_accent, phone_line, book_line, share, disclaimer |
| perspective | photo, eyebrow, quote (wording approved by the person quoted), name, role, quote_size (52), disclaimer. Closing slide with no buttons (no ask) |

single: photo, eyebrow, title, title_accent, lines [], button, footer
gbp: photo, eyebrow, title, title_accent, sub, button

See posts/example.json (the Oct 10 2026 Breast Cancer Awareness post).
