# Marketing material

Public marketing assets, one folder per product.

## SpaceRisk

Friendly ISO 31000 risk management with bowties, barriers, monthly team reviews, project overviews and a financial view
for the CEO.

- **Website:** https://partoneoftwo.github.io/marketing-material/spacerisk/ (English, Español, Deutsch, Português (Brasil))
- **Materials** per language in [`spacerisk/materials/<lang>/`](spacerisk/materials):
  - `spacerisk-product-sheet.pdf`: one-page A4 product sheet;
  - `spacerisk-sales-deck.pptx`: 11-slide sales deck, 16:9;
  - `social/`: LinkedIn (1200×627), X (1500×500) and square (1080×1080) images;
  - `texts.md`: taglines, short, medium and long descriptions, feature blurbs and boilerplate.
- **Screenshots:** [`spacerisk/screenshots/`](spacerisk/screenshots). Real product screens with fictional showcase data.

| Language | Website | Product sheet | Sales deck | Texts |
|---|---|---|---|---|
| English | [en](https://partoneoftwo.github.io/marketing-material/spacerisk/en/) | [PDF](spacerisk/materials/en/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/en/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/en/texts.md) |
| Español | [es](https://partoneoftwo.github.io/marketing-material/spacerisk/es/) | [PDF](spacerisk/materials/es/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/es/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/es/texts.md) |
| Deutsch | [de](https://partoneoftwo.github.io/marketing-material/spacerisk/de/) | [PDF](spacerisk/materials/de/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/de/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/de/texts.md) |
| Português (Brasil) | [pt-br](https://partoneoftwo.github.io/marketing-material/spacerisk/pt-br/) | [PDF](spacerisk/materials/pt-br/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/pt-br/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/pt-br/texts.md) |

> **Translations** (es, de, pt-br) were machine-written from the English source. Have a native speaker review them before
> campaigns.

### Editing and rebuilding
All text lives in `spacerisk/content/<lang>.json`. After a change:
```
pip install -r spacerisk/tools/requirements.txt && playwright install chromium
python spacerisk/tools/check_content.py      # translations match the English structure
python spacerisk/tools/build_site.py         # spacerisk/<lang>/index.html
python spacerisk/tools/build_materials.py    # PDF, PPTX, social images, texts.md
```
The site is static HTML and CSS with a small script for the bowtie demo. No tracking, no cookies, and it works without JavaScript.
Fonts in `spacerisk/tools/fonts/` are DejaVu (see the licence file there).
