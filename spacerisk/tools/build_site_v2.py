"""Build the sleek SpaceRisk site (v2, ADR 0091 in the app repo): v2/<lang>/index.html and pricing.html from
content/v2/<lang>.json, plus the language redirect at v2/index.html. White only, no third-party requests."""
import datetime
import json
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "v2"
ORDER = ["en", "es", "nb", "de", "fr", "it", "pt-br"]  # menu order
CLASSIC = {"en", "es", "de", "fr", "it", "pt-br"}  # languages of the colourful site (0055); nb links to English
BASE_URL = "https://partoneoftwo.github.io/marketing-material/spacerisk/v2/"
SHOTS = ["dashboard", "bowtie", "panel", "summary", "iso", "compliance", "cyber", "paths"]

MARK = Markup('<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M3 7.5 14 16 3 24.5z" fill="#2f5bff"/>'
              '<path d="M29 7.5 18 16l11 8.5z" fill="#0b0d12"/><circle cx="16" cy="16" r="3.2" fill="#2f5bff"/></svg>')
CHECK = Markup('<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="10" fill="currentColor" opacity=".12"/>'
               '<path d="M6 10.4 8.6 13 14 7.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
TICK = Markup('<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 7.4 5.8 10 11 4.5" fill="none" stroke="currentColor" stroke-width="2.2" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>')
GLOBE = Markup('<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.3"><circle cx="8" cy="8" r="6.5"/>'
               '<path d="M1.5 8h13M8 1.5c2 2 2.8 4.2 2.8 6.5S10 12.5 8 14.5C6 12.5 5.2 10.3 5.2 8S6 3.5 8 1.5z"/></svg>')


def bowtie(c):
    """A restrained bowtie: three threats, preventive barriers, the hazard event, mitigating barriers, three consequences.
    Captions are an HTML legend below, so long words in any language never collide."""
    L = c["bowtie"]["labels"]
    ys, cy = (60, 160, 260), 160
    s = ['<figure class="bt-fig"><svg class="bt" viewBox="0 0 640 320" role="img" aria-label="'
         + f'{L["threats"]} → {L["preventive"]} → {L["hazard"]} → {L["mitigating"]} → {L["consequences"]}">']
    for i, y in enumerate(ys):
        left, right = f"M128,{y} L250,{y} L290,{cy}", f"M350,{cy} L390,{y} L512,{y}"
        s.append(f'<path class="ln" d="{left}"/><path class="ln" d="{right}"/>')
        s.append(f'<path class="flow" d="M128,{y} L{170 if i == 1 else 250},{y}{"" if i == 1 else f" L290,{cy}"}"/>')
        s.append(f'<path class="flow" d="M350,{cy} L390,{y} L{430 if i == 2 else 512},{y}"/>')
        s.append(f'<rect class="node" x="8" y="{y - 22}" width="120" height="44" rx="10"/><rect x="24" y="{y - 4}" width="{64 + 12 * i}" height="8" rx="4" fill="#e6e8ec"/>')
        s.append(f'<rect class="node" x="512" y="{y - 22}" width="120" height="44" rx="10"/><rect x="528" y="{y - 4}" width="{80 - 10 * i}" height="8" rx="4" fill="#e6e8ec"/>')
        for x, colour in ((176, "#2f5bff"), (212, "#2f5bff" if i != 1 else "#d97706")):
            s.append(f'<rect class="bar" x="{x}" y="{y - 18}" width="10" height="36" fill="{colour}"/>')
        for x, colour in ((420, "#0b0d12" if i != 2 else "#d97706"), (456, "#0b0d12")):
            s.append(f'<rect class="bar" x="{x}" y="{y - 18}" width="10" height="36" fill="{colour}"/>')
    s.append(f'<circle class="knot" cx="320" cy="{cy}" r="30"/><text class="t-knot" x="320" y="{cy + 5}" text-anchor="middle">!</text>')
    s.append("</svg><figcaption class=\"bt-key\">")
    for cls, key in (("k-node", "threats"), ("k-pre", "preventive"), ("k-knot", "hazard"), ("k-mit", "mitigating"), ("k-node", "consequences")):
        s.append(f'<span><i class="{cls}"></i>{Markup.escape(L[key])}</span>')
    s.append("</figcaption></figure>")
    return Markup("".join(s))


def main():
    env = Environment(loader=FileSystemLoader(ROOT / "tools" / "templates" / "v2"), autoescape=True, undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True)
    prices = json.loads((ROOT / "content" / "pricing.json").read_text())
    contents = {l: json.loads(p.read_text()) for l in ORDER if (p := ROOT / "content" / "v2" / f"{l}.json").exists()}
    langs = [contents[l] for l in contents]
    version = datetime.date.today().strftime("%Y%m%d")
    for lang, c in contents.items():
        shot_lang = c["app_lang"]
        heights = {}
        for name in SHOTS:
            with Image.open(OUT / "assets" / "shots" / shot_lang / f"{name}.webp") as im:
                heights[name] = (im.width // 2, im.height // 2)  # 2x screens: CSS pixels
        mailto = Markup(f"mailto:{c['contact']['email']}?subject={quote(c['contact']['subject'])}")
        common = dict(c=c, langs=langs, base_url=BASE_URL, version=version, mark=MARK, check=CHECK, globe=GLOBE, mailto=mailto,
                      classic_lang=lang if lang in CLASSIC else "en", year=datetime.date.today().year)
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        page = env.get_template("index.html").render(
            page_file="index.html", shot_lang=shot_lang, shot_h=heights, bowtie=bowtie(c),
            month=list(zip(c["reviews"]["steps"], [True, True, True, False])), tick=TICK, **common)
        (OUT / lang / "index.html").write_text(page)
        pricing = env.get_template("pricing.html").render(page_file="pricing.html", prices=prices,
                                                           default_currency=prices["default_currency"].get(lang, "EUR"), **common)
        (OUT / lang / "pricing.html").write_text(pricing)
        print("wrote", f"v2/{lang}/index.html + pricing.html")
    # language redirect: the browser's first language we have, else English; works without JS through the meta refresh
    codes = json.dumps([l for l in contents])
    (OUT / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="color-scheme" content="light only"><title>SpaceRisk</title>\n'
        f'<script>var have={codes},want=(navigator.languages||[navigator.language||"en"]).map(function(x){{x=x.toLowerCase();'
        'return x.indexOf("pt")===0?"pt-br":/^(nb|nn|no)\\b/.test(x)?"nb":x.slice(0,2)}}),pick="en";'
        'for(var i=0;i<want.length;i++){if(have.indexOf(want[i])>=0){pick=want[i];break}}location.replace(pick+"/");</script>\n'
        '<meta http-equiv="refresh" content="1; url=en/"></head><body style="background:#fff"><a href="en/">SpaceRisk</a></body></html>\n')
    (OUT / "assets" / "mark.svg").write_text(str(MARK).replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))


if __name__ == "__main__":
    main()
