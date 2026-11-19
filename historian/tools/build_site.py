"""Build the Many Worlds Historian website: website/<lang>/index.html from content/<lang>.json, plus the language
redirect at website/index.html. The website folder is self-contained (stylesheet, font, logo and screens), so it can be
uploaded to any static host on its own. The pages carry no scripts (only the language redirect does), no cookies and no third-party requests."""
import datetime
import json
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "website"
ORDER = ["en", "es", "nb", "de", "fr", "it", "pt-br"]  # menu order, as on the SpaceRisk site
SPACERISK_URL = "https://partoneoftwo.github.io/marketing-material/spacerisk/v3/"


def main():
    env = Environment(loader=FileSystemLoader(ROOT / "tools" / "templates"), autoescape=True, undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True)
    contents = {l: json.loads(p.read_text()) for l in ORDER if (p := ROOT / "content" / f"{l}.json").exists()}
    langs = list(contents.values())
    for lang, c in contents.items():
        shot_lang = lang if (OUT / "assets" / "shots" / lang).is_dir() else "en"  # screens are English until captured per language
        dims = {}
        for f in sorted((OUT / "assets" / "shots" / shot_lang).glob("*.webp")):
            with Image.open(f) as im:
                dims[f.stem] = (im.width // 2, im.height // 2)  # 2x screens: CSS pixels
        mailto = Markup(f"mailto:{c['contact']['email']}?subject={quote(c['contact']['subject'])}")
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        (OUT / lang / "index.html").write_text(env.get_template("index.html").render(
            c=c, langs=langs, shot_lang=shot_lang, dims=dims, mailto=mailto, spacerisk_url=SPACERISK_URL + lang + "/",
            version=datetime.date.today().strftime("%Y%m%d"), year=datetime.date.today().year))
        print("wrote", f"website/{lang}/index.html")
    # language redirect: the browser's first language we have, else English; works without JS through the meta refresh
    codes = json.dumps(list(contents))
    (OUT / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Many Worlds Historian</title>\n'
        f'<script>var have={codes},want=(navigator.languages||[navigator.language||"en"]).map(function(x){{x=x.toLowerCase();'
        'return x.indexOf("pt")===0?"pt-br":/^(nb|nn|no)\\b/.test(x)?"nb":x.slice(0,2)}),pick="en";'
        'for(var i=0;i<want.length;i++){if(have.indexOf(want[i])>=0){pick=want[i];break}}location.replace(pick+"/");</script>\n'
        '<meta http-equiv="refresh" content="1; url=en/"></head><body style="background:#fbfcfd"><a href="en/">Many Worlds Historian</a></body></html>\n')


if __name__ == "__main__":
    main()
