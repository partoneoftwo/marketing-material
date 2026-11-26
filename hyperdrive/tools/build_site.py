"""Build the Hyperdrive website: website/<lang>/index.html from content/<lang>.json, plus the language redirect at
website/index.html, and the WebP screens in website/assets/shots/en/ cut from the PNG originals in screenshots/.
The website folder is self-contained (stylesheet, font, logo and screens), so it can be uploaded to any static host on
its own. The pages carry no scripts (only the language redirect does), no cookies and no third-party requests.

The PNG originals are copies of the ones in hyperdrive-platform/screenshots/ (made there with `node scripts/screenshots.js`).
19-backups.png is cut to its top 620 pixels, because the rest of that screen shows a folder path from the capture machine.
Needs jinja2 and pillow. Run: python hyperdrive/tools/build_site.py [--shots]   (--shots also recuts the screens)"""
import datetime
import json
import sys
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "website"
ORDER = ["en", "es", "nb", "de", "fr", "it", "pt-br"]  # menu order, as on the other product sites
SIDEBAR = 448  # width of the app's sidebar in the 2880 px originals; cut off so the screen reads larger on the page
# name on the site -> (original, left, right, bottom) in pixels of the original; None keeps that edge
SHOTS = {
    "overview": ("01-overview", 0, None, 1290),
    "rest-source": ("03-new-rest-source", SIDEBAR, None, 2540),
    "normalisation": ("06-normalisation", SIDEBAR, None, None),
    "sql-workbench": ("12-sql-workbench", SIDEBAR, None, 1400),
    "api-access": ("15-api-access", SIDEBAR, None, 1420),
    "runs": ("16-runs", SIDEBAR, None, 1140),
    "datasette": ("17-datasette", 0, 2200, None),
    # only the list of backups: the lower half of this screen shows a folder path from the machine it was captured on
    "backups": ("19-backups", SIDEBAR, None, 620),
}
MAX_W = 2200


def cut_shots():
    dest = OUT / "assets" / "shots" / "en"
    dest.mkdir(parents=True, exist_ok=True)
    for name, (src, left, right, bottom) in SHOTS.items():
        with Image.open(ROOT / "screenshots" / f"{src}.png") as im:
            im = im.convert("RGB").crop((left, 0, right or im.width, bottom or im.height))
            if im.width > MAX_W:
                im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            im.save(dest / f"{name}.webp", quality=86, method=6)
            print("cut", name, im.size)


def main():
    if "--shots" in sys.argv or not any((OUT / "assets" / "shots" / "en").glob("*.webp")):
        cut_shots()
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

        def shot(name, caption, eager=False):
            src, (w, h) = f"../assets/shots/{shot_lang}/{name}.webp", dims[name]
            loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
            return Markup(f'<figure class="shot"><a href="{src}"><img src="{src}" width="{w}" height="{h}" '
                          f'alt="{escape(c["shots"][name])}" {loading}></a><figcaption>{escape(caption)}</figcaption></figure>')

        mailto = Markup(f"mailto:{c['contact']['email']}?subject={quote(c['contact']['subject'])}")
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        (OUT / lang / "index.html").write_text(env.get_template("index.html").render(
            c=c, langs=langs, shot=shot, mailto=mailto,
            version=datetime.date.today().strftime("%Y%m%d"), year=datetime.date.today().year))
        print("wrote", f"website/{lang}/index.html")
    # language redirect: the browser's first language we have, else English; works without JS through the meta refresh
    codes = json.dumps(list(contents))
    (OUT / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Hyperdrive</title>\n'
        f'<script>var have={codes},want=(navigator.languages||[navigator.language||"en"]).map(function(x){{x=x.toLowerCase();'
        'return x.indexOf("pt")===0?"pt-br":/^(nb|nn|no)\\b/.test(x)?"nb":x.slice(0,2)}),pick="en";'
        'for(var i=0;i<want.length;i++){if(have.indexOf(want[i])>=0){pick=want[i];break}}location.replace(pick+"/");</script>\n'
        '<meta http-equiv="refresh" content="1; url=en/"></head><body style="background:#0f172a"><a href="en/" style="color:#fff">Hyperdrive</a></body></html>\n')


if __name__ == "__main__":
    main()
