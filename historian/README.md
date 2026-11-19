# Historian

Marketing material for Many Worlds Historian, laid out the same way as [`spacerisk/`](../spacerisk). The website is built
(English); the sales material is still to be added.

- **Website:** https://partoneoftwo.github.io/marketing-material/historian/website/ . The look follows the product's own
  report: ink on paper, ruled, monospace labels. The `website` folder is self-contained and can be uploaded to any static
  host on its own. No scripts, no cookies, no third-party requests.
- **Texts** in `content/<lang>.json`. Rebuild with `python historian/tools/build_site.py` (needs `jinja2` and `pillow`).
- **Screens** are real product screens on simulated data. Recapture with `python historian/tools/shots.py` against a
  running Historian (see the top of that file).

| Folder | What goes here |
|---|---|
| [`website/`](website) | The marketing website (static HTML, one folder per language). |
| [`content/`](content), [`tools/`](tools) | The website's texts, template, build script and screen capture script. |
| [`materials/en/`](materials/en) | Material for sales, in English. Other languages get their own folder next to `en`. |
| [`materials/en/sales/`](materials/en/sales) | Sales working documents: interview guide, outreach messages, pilot offer. |
| [`materials/en/social/`](materials/en/social) | Social images: LinkedIn (1200×627), X (1500×500) and square (1080×1080). |
| [`screenshots/`](screenshots) | Product screens used on the website and in the materials. |

Files expected in `materials/en/`, named like the SpaceRisk ones:

- `historian-product-sheet.pdf`: one-page A4 product sheet
- `historian-sales-deck.pptx`: sales deck, 16:9
- `texts.md`: taglines, short, medium and long descriptions, feature blurbs and boilerplate
