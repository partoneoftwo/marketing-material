# Marketing material

Public marketing assets, one folder per product.

## SpaceRisk

Friendly ISO 31000 risk management with bowties, barriers, monthly team reviews, project overviews and a financial view
for the CEO. Hosted by us or self-hosted, and your data is always yours. Contact: thomas.frivold@frivolddigital.com

- **Website v2 (sleek, white):** https://partoneoftwo.github.io/marketing-material/spacerisk/v2/ in 7 languages, each with
  app screens in that language:

| Language | Home | Pricing |
|---|---|---|
| English | [en](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/en/) | [pricing](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/en/pricing.html) |
| Español | [es](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/es/) | [precios](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/es/pricing.html) |
| Norsk (bokmål) | [nb](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/nb/) | [priser](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/nb/pricing.html) |
| Deutsch | [de](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/de/) | [Preise](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/de/pricing.html) |
| Français | [fr](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/fr/) | [tarifs](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/fr/pricing.html) |
| Italiano | [it](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/it/) | [prezzi](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/it/pricing.html) |
| Português (Brasil) | [pt-br](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/pt-br/) | [preços](https://partoneoftwo.github.io/marketing-material/spacerisk/v2/pt-br/pricing.html) |

  Texts in `spacerisk/content/v2/<lang>.json`. Rebuild with `python spacerisk/tools/build_site_v2.py` (check the texts first with
  `check_content_v2.py`). Screens: `shots_v2.py <app lang>` against a running SpaceRisk with the banking showcase. Social
  images: `og_v2.py`. No cookies, no tracking, no third-party requests (the Inter font is self-hosted, SIL OFL).

### Classic site and materials
- **Pricing:** per language at `spacerisk/<lang>/pricing.html` (prices in `spacerisk/content/pricing.json`, NOK, EUR and USD)

- **Website:** https://partoneoftwo.github.io/marketing-material/spacerisk/ (English, Español, Deutsch, Português (Brasil), Français, Italiano)
- **Materials** per language in [`spacerisk/materials/<lang>/`](spacerisk/materials):
  - `spacerisk-product-sheet.pdf`: one-page A4 product sheet;
  - `spacerisk-sales-deck.pptx`: 11-slide sales deck, 16:9;
  - `social/`: LinkedIn (1200×627), X (1500×500) and square (1080×1080) images;
  - `texts.md`: taglines, short, medium and long descriptions, feature blurbs and boilerplate.
- **Sales (English, drafts):** [`interview-guide.md`](spacerisk/materials/en/sales/interview-guide.md) for discovery
  conversations, and [`pilot-offer.md`](spacerisk/materials/en/sales/pilot-offer.md), a one-page 90-day pilot offer.
- **Screenshots:** [`spacerisk/screenshots/`](spacerisk/screenshots). Real product screens with fictional showcase data.

| Language | Website | Product sheet | Sales deck | Texts |
|---|---|---|---|---|
| English | [en](https://partoneoftwo.github.io/marketing-material/spacerisk/en/) | [PDF](spacerisk/materials/en/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/en/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/en/texts.md) |
| Español | [es](https://partoneoftwo.github.io/marketing-material/spacerisk/es/) | [PDF](spacerisk/materials/es/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/es/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/es/texts.md) |
| Deutsch | [de](https://partoneoftwo.github.io/marketing-material/spacerisk/de/) | [PDF](spacerisk/materials/de/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/de/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/de/texts.md) |
| Português (Brasil) | [pt-br](https://partoneoftwo.github.io/marketing-material/spacerisk/pt-br/) | [PDF](spacerisk/materials/pt-br/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/pt-br/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/pt-br/texts.md) |
| Français | [fr](https://partoneoftwo.github.io/marketing-material/spacerisk/fr/) | [PDF](spacerisk/materials/fr/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/fr/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/fr/texts.md) |
| Italiano | [it](https://partoneoftwo.github.io/marketing-material/spacerisk/it/) | [PDF](spacerisk/materials/it/spacerisk-product-sheet.pdf) | [PPTX](spacerisk/materials/it/spacerisk-sales-deck.pptx) | [texts](spacerisk/materials/it/texts.md) |

> **Translations** (es, nb, de, pt-br, fr, it; classic site and v2) were machine-written from the English source. Have a native speaker review them before
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
