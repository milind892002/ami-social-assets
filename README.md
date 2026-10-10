# AMI social assets

Public, temporary file host for Advanced Medical Imaging social media designs.
Canva can only import a design from a public web link, so design files are
placed here for a few minutes, imported into Canva, then deleted.

Served by GitHub Pages at https://milind892002.github.io/ami-social-assets/

## Layout

- `tools/build_post.py` builds a post's HTML from a short JSON spec (see tools/README.md).
- `posts/` keeps one spec per post: the record of what was made, and the content log
  used to avoid repeating topics.
- `imports/` is temporary: each batch is deleted right after Canva imports it.

## Rules

- Marketing images and design files only. Never patient information (PHI),
  schedules, reports, or anything not meant to be public.
- Put each batch in `imports/YYYY-MM-DD-topic/` and delete it after the
  Canva import succeeds.
- Every HTML page carries `<meta name="robots" content="noindex, nofollow">`.
- This repository is separate from the website (amiweb) on purpose: nothing
  here can affect advancedimg.com.
