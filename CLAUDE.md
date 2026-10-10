# ami-social-assets

Temporary public host for Canva imports (GitHub Pages, branch main, root).
Public URL base: https://milind892002.github.io/ami-social-assets/

- Only marketing assets. Never PHI or anything private.
- One folder per batch: imports/YYYY-MM-DD-topic/ (HTML + img/).
- HTML pages must include <meta name="robots" content="noindex, nofollow">,
  and every top-level Canva page element needs data-document-role="page".
- Pages takes about 1 minute to publish after a push. Confirm the URL loads
  before calling Canva's import.
- Delete the batch folder after the import is confirmed in Canva.
- Never push social files to the website repo (amiweb).
