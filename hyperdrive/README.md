# Hyperdrive

Marketing material for Hyperdrive, the self-hosted data platform on SQLite and Datasette. Laid out the same way as
[`historian/`](../historian) and [`cloud/`](../cloud). English only so far.

- **Website:** https://partoneoftwo.github.io/marketing-material/hyperdrive/website/ . The look follows the product: the
  navy of its sidebar, grey paper, white cards, one blue, and the stage colours from its overview. The `website` folder is
  self-contained and can be uploaded to any static host on its own. No cookies, no third-party requests, and no scripts
  apart from the language redirect.
- **Texts** in `content/<lang>.json`. Rebuild with `python hyperdrive/tools/build_site.py` (needs `jinja2` and `pillow`;
  add `--shots` to recut the screens). Adding a language is one more content file: es, nb, de, fr, it and pt-br are picked
  up when they exist.
- **Sales material** in [`materials/en/`](materials/en): [`hyperdrive-sales-deck.pptx`](materials/en/hyperdrive-sales-deck.pptx)
  (12 slides, 16:9, with speaker notes) and [`texts.md`](materials/en/texts.md) (taglines, short, medium and long
  descriptions, feature blurbs, limits and boilerplate). Rebuild the deck with `python hyperdrive/tools/build_deck.py`
  (needs `python-pptx` and `pillow`). A one-page product sheet is still to be added.
- **Screens** in [`screenshots/`](screenshots) are real product screens with demo data, copied from the product
  repository (`hyperdrive-platform/screenshots/`, made there with `node scripts/screenshots.js`). The site and the deck
  cut their pictures from these. `19-backups.png` is cut to its top part, because the rest of that screen shows a folder
  path from the capture machine.

The material only claims what the product does today. The limits are part of the message (the "Fit" section and slide):
tables up to some millions of rows, runs one at a time, a single login, and no incremental normalisation. SFTP and S3
connections are not mentioned, because they were not merged when this was written.
