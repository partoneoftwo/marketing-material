"""Build SpaceRisk site v4: v4/<lang>/index.html and pricing.html from content/v4/<lang>.json, plus the language redirect
at v4/index.html. v4 uses the look of the Many Worlds Historian site (ink on paper, ruled, monospace labels, numbered
parts), with the same page elements. The v4 folder is self-contained, so it can be uploaded to any static host on its own.
The pages carry no scripts (only the language redirect does), no cookies and no third-party requests."""
import datetime
import json
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "v4"
ORDER = ["en", "es", "nb", "de", "fr", "it", "pt-br"]  # menu order; a language is built once content/v4/<lang>.json exists
HISTORIAN_URL = "https://partoneoftwo.github.io/marketing-material/historian/website/"


def main():
    env = Environment(loader=FileSystemLoader(ROOT / "tools" / "templates" / "v4"), autoescape=True, undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True)
    prices = json.loads((ROOT / "content" / "pricing.json").read_text())
    contents = {l: json.loads(p.read_text()) for l in ORDER if (p := ROOT / "content" / "v4" / f"{l}.json").exists()}
    langs = list(contents.values())
    today = datetime.date.today()
    for lang, c in contents.items():
        shot_lang = lang if (OUT / "assets" / "shots" / lang).is_dir() else "en"
        dims = {}
        for f in sorted((OUT / "assets" / "shots" / shot_lang).glob("*.webp")):
            with Image.open(f) as im:
                dims[f.stem] = (im.width // 2, im.height // 2)  # 2x screens: CSS pixels
        common = dict(c=c, langs=langs, shot_lang=shot_lang, dims=dims, version=today.strftime("%Y%m%d"), year=today.year,
                      mailto=Markup(f"mailto:{c['contact']['email']}?subject={quote(c['contact']['subject'])}"),
                      historian_url=HISTORIAN_URL + lang + "/")
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        (OUT / lang / "index.html").write_text(env.get_template("index.html").render(page_file="index.html", **common))
        (OUT / lang / "pricing.html").write_text(env.get_template("pricing.html").render(
            page_file="pricing.html", prices=prices, default_currency=prices["default_currency"].get(lang, "EUR"), **common))
        print("wrote", f"v4/{lang}/index.html + pricing.html")
    codes = json.dumps(list(contents))
    (OUT / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>SpaceRisk</title>\n'
        f'<script>var have={codes},want=(navigator.languages||[navigator.language||"en"]).map(function(x){{x=x.toLowerCase();'
        'return x.indexOf("pt")===0?"pt-br":/^(nb|nn|no)\\b/.test(x)?"nb":x.slice(0,2)}),pick="en";'
        'for(var i=0;i<want.length;i++){if(have.indexOf(want[i])>=0){pick=want[i];break}}location.replace(pick+"/");</script>\n'
        '<meta http-equiv="refresh" content="1; url=en/"></head><body style="background:#fbfcfd"><a href="en/">SpaceRisk</a></body></html>\n')


if __name__ == "__main__":
    main()
