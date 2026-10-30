"""Build the SpaceRisk marketing site: one page per language from content/<lang>.json (decision 0055 in the app repo)."""
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["en", "es", "de", "pt-br", "fr", "it"]
DOWNLOADS = {  # short UI strings not in the content files
    "en": ("Product sheet (PDF)", "Sales deck (PPTX)", "Texts"),
    "es": ("Ficha de producto (PDF)", "Presentación comercial (PPTX)", "Textos"),
    "de": ("Produktblatt (PDF)", "Vertriebspräsentation (PPTX)", "Texte"),
    "pt-br": ("Folha do produto (PDF)", "Apresentação comercial (PPTX)", "Textos"),
    "fr": ("Fiche produit (PDF)", "Présentation commerciale (PPTX)", "Textes"),
    "it": ("Scheda prodotto (PDF)", "Presentazione commerciale (PPTX)", "Testi"),
}
GREEN, AMBER, RED = "#22c55e", "#fbbf24", "#f43f5e"

ICONS = {k: Markup(f'<svg viewBox="0 0 48 48" width="44" height="44" aria-hidden="true">{v}</svg>') for k, v in {
    "register": '<rect x="8" y="6" width="32" height="36" rx="6" fill="#fff" stroke="#1f2a44" stroke-width="3"/><path d="M15 17h18M15 25h18M15 33h11" stroke="#14b8a6" stroke-width="3" stroke-linecap="round"/>',
    "cycle": '<circle cx="24" cy="24" r="15" fill="none" stroke="#14b8a6" stroke-width="4" stroke-dasharray="70 30"/><path d="M34 9l5 6-8 2z" fill="#1f2a44"/><circle cx="24" cy="24" r="4" fill="#f97362"/>',
    "bowtie": '<path d="M6 12l16 12-16 12zM42 12L26 24l16 12z" fill="#14b8a6"/><circle cx="24" cy="24" r="6" fill="#1f2a44"/><rect x="11" y="18" width="3" height="12" fill="#22c55e"/><rect x="34" y="18" width="3" height="12" fill="#fbbf24"/>',
    "events": '<circle cx="24" cy="24" r="15" fill="#fde68a" stroke="#1f2a44" stroke-width="3"/><path d="M24 15v11" stroke="#1f2a44" stroke-width="4" stroke-linecap="round"/><circle cx="24" cy="32" r="2.5" fill="#1f2a44"/>',
    "money": '<rect x="7" y="13" width="34" height="22" rx="5" fill="#d1fae5" stroke="#1f2a44" stroke-width="3"/><circle cx="24" cy="24" r="6" fill="#22c55e"/><path d="M12 24h2M34 24h2" stroke="#1f2a44" stroke-width="3"/>',
    "summary": '<rect x="9" y="7" width="30" height="34" rx="5" fill="#fff" stroke="#1f2a44" stroke-width="3"/><rect x="15" y="27" width="4" height="8" fill="#f97362"/><rect x="22" y="21" width="4" height="14" fill="#fbbf24"/><rect x="29" y="15" width="4" height="20" fill="#14b8a6"/>',
    "export": '<path d="M24 8v20M16 21l8 8 8-8" stroke="#f97362" stroke-width="4" fill="none" stroke-linecap="round"/><rect x="9" y="32" width="30" height="8" rx="3" fill="#1f2a44"/>',
    "showcase": '<rect x="6" y="10" width="16" height="12" rx="3" fill="#14b8a6"/><rect x="26" y="10" width="16" height="12" rx="3" fill="#fbbf24"/><rect x="6" y="26" width="16" height="12" rx="3" fill="#f97362"/><rect x="26" y="26" width="16" height="12" rx="3" fill="#a78bfa"/>',
}.items()}


def bowtie_svg(prefix):
    """Animated bowtie: risk particles flow from threats toward the knot; barriers stop them (state via CSS classes)."""
    rows, cy = [80, 210, 340], 210
    bars_p = [(250, [GREEN, AMBER, GREEN]), (320, [GREEN, GREEN, RED])]
    bars_m = [(690, [AMBER, GREEN, GREEN]), (760, [GREEN, AMBER, GREEN])]
    out = [f'<svg class="bt" viewBox="0 0 1000 420" role="img" aria-label="Bowtie diagram">']
    for i, y in enumerate(rows):
        out.append(f'<path class="ln" d="M170,{y} L390,{y} L455,{cy}"/><path class="ln ln-r" d="M545,{cy} L610,{y} L830,{y}"/>')
        out.append(f'<rect class="box threat" x="20" y="{y - 28}" width="150" height="56" rx="16"/>'
                   f'<rect class="box cons" x="830" y="{y - 28}" width="150" height="56" rx="16"/>')
        out.append(f'<circle class="glyph glyph-t" cx="56" cy="{y}" r="11"/><rect class="glyph-bar" x="76" y="{y - 5}" width="70" height="10" rx="5"/>'
                   f'<circle class="glyph glyph-c" cx="866" cy="{y}" r="11"/><rect class="glyph-bar" x="886" y="{y - 5}" width="70" height="10" rx="5"/>')
        for k, (x, colours) in enumerate(bars_p):
            out.append(f'<rect class="bar bar-p" x="{x - 7}" y="{y - 24}" width="14" height="48" rx="5" fill="{colours[i]}"/>')
        for k, (x, colours) in enumerate(bars_m):
            out.append(f'<rect class="bar bar-m" x="{x - 7}" y="{y - 24}" width="14" height="48" rx="5" fill="{colours[i]}"/>')
        for n, (cls, path, dur) in enumerate([
            ("pt p-on", f"M170,{y} L238,{y}", 1.6),
            ("pt p-off", f"M170,{y} L390,{y} L455,{cy}", 2.4),
            ("pt m-on", f"M545,{cy} L610,{y} L678,{y}", 1.8),
            ("pt m-off", f"M545,{cy} L610,{y} L830,{y}", 2.6),
        ]):
            for d in (0, dur / 2):
                out.append(f'<circle class="{cls}" r="7"><animateMotion dur="{dur}s" begin="{d + i * 0.3:.1f}s" repeatCount="indefinite" path="{path}"/>'
                           f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" begin="{d + i * 0.3:.1f}s" repeatCount="indefinite"/></circle>')
    out.append(f'<ellipse class="knot" cx="500" cy="{cy}" rx="62" ry="50"/><text class="knot-t" x="500" y="{cy + 14}" text-anchor="middle">!</text>')
    out.append("</svg>")
    return Markup("".join(out))


def main():
    env = Environment(loader=FileSystemLoader(ROOT / "tools" / "templates"), autoescape=True)
    tpl = env.get_template("site.html")
    pricing_tpl = env.get_template("pricing.html")
    prices = json.loads((ROOT / "content" / "pricing.json").read_text())
    contents = {l: json.loads((ROOT / "content" / f"{l}.json").read_text()) for l in LANGS if (ROOT / "content" / f"{l}.json").exists()}
    langs = [{"lang": c["lang"], "html_lang": c["html_lang"], "name": c["lang_name"]} for c in contents.values()]
    for lang, c in contents.items():
        out = ROOT / lang / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(tpl.render(c=c, langs=langs, icons=ICONS, bowtie_svg=bowtie_svg, downloads=DOWNLOADS[lang]))
        (ROOT / lang / "pricing.html").write_text(pricing_tpl.render(c=c, langs=langs, prices=prices))
        print("wrote", out.relative_to(ROOT.parent), "+ pricing.html")


if __name__ == "__main__":
    main()
