"""Build the products top-level website: <lang>/index.html from content/<lang>.json and tools/template.html, plus the
language redirect at index.html. The folder is self-contained (own font), so it can be uploaded to any static host on
its own. No third-party requests. Standard library only: python products-top-level-website/tools/build_site.py"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["en", "es", "nb", "de", "fr", "it", "pt-br"]  # menu order, same as the SpaceRisk site
BASE_URL = "https://partoneoftwo.github.io/marketing-material/products-top-level-website/"

REDIRECT = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Products — Frivold Digital</title>
<script>var have=%s,want=(navigator.languages||[navigator.language||"en"]).map(function(x){x=x.toLowerCase();return x.indexOf("pt")===0?"pt-br":/^(nb|nn|no)\\b/.test(x)?"nb":x.slice(0,2)}),pick="en";for(var i=0;i<want.length;i++){if(have.indexOf(want[i])>=0){pick=want[i];break}}location.replace(pick+"/");</script>
<meta http-equiv="refresh" content="1; url=en/"></head><body style="background:#0a1430"><a href="en/" style="color:#e9eefb">Products</a></body></html>
"""


def main():
    template = (ROOT / "tools" / "template.html").read_text(encoding="utf-8")
    content = {lang: json.loads((ROOT / "content" / f"{lang}.json").read_text(encoding="utf-8")) for lang in ORDER}
    keys = set(content["en"])
    for lang, c in content.items():
        if set(c) != keys:
            raise SystemExit(f"{lang}.json: keys differ from en.json: {sorted(set(c) ^ keys)}")
    alternates = "\n".join(f'<link rel="alternate" hreflang="{content[l]["html_lang"]}" href="{BASE_URL}{l}/">' for l in ORDER)
    for lang, c in content.items():
        values = {k: html.escape(v, quote=True) for k, v in c.items()}
        values["alternates"] = alternates
        values["lang_code"] = lang.split("-")[0].upper()
        values["lang_menu"] = "".join(
            f'<li><a href="../{l}/" hreflang="{content[l]["html_lang"]}" lang="{content[l]["html_lang"]}"'
            + (' aria-current="true"' if l == lang else "") + f'>{html.escape(content[l]["lang_name"])}</a></li>' for l in ORDER)
        page = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)
        out = ROOT / lang / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page, encoding="utf-8")
    (ROOT / "index.html").write_text(REDIRECT % json.dumps(ORDER), encoding="utf-8")
    print(f"built {len(ORDER)} languages")


if __name__ == "__main__":
    main()
