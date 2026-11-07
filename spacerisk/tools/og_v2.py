"""Social preview images for the v2 site: v2/assets/og/<lang>.png (1200x630), from the hero text and the dashboard screen."""
import json
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "v2"


def main():
    (V2 / "assets" / "og").mkdir(parents=True, exist_ok=True)
    font = (V2 / "assets" / "fonts" / "InterVariable.woff2").as_uri()
    mark = (V2 / "assets" / "mark.svg").as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for path in sorted((ROOT / "content" / "v2").glob("*.json")):
            c = json.loads(path.read_text())
            shot = (V2 / "assets" / "shots" / c["app_lang"] / "dashboard.webp").as_uri()
            html = f"""<!doctype html><html lang="{c['html_lang']}"><style>
@font-face {{ font-family: Inter; src: url({font}); font-weight: 100 900; }}
body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; background: #fff; font-family: Inter; color: #0b0d12;
  background: radial-gradient(70% 60% at 30% 0%, #eef2ff 0%, #fff 70%); }}
.b {{ position: absolute; left: 72px; top: 64px; display: flex; gap: 12px; align-items: center; font-weight: 700; font-size: 28px; letter-spacing: -.02em; }}
.b img {{ width: 36px; }}
h1 {{ position: absolute; left: 72px; top: 150px; width: 560px; margin: 0; font-size: 58px; line-height: 1.05; letter-spacing: -.045em; font-weight: 700; text-wrap: balance; }}
p {{ position: absolute; left: 72px; bottom: 64px; margin: 0; color: #2f5bff; font-weight: 600; font-size: 20px; }}
.s {{ position: absolute; left: 680px; top: 96px; width: 760px; border-radius: 14px; border: 1px solid #e6e8ec; overflow: hidden;
  box-shadow: 0 30px 60px -20px rgba(16,24,40,.25); }}
.s img {{ display: block; width: 100%; }}
</style><div class="b"><img src="{mark}">SpaceRisk</div><h1>{c['hero']['title']}</h1><p>{c['hero']['eyebrow']}</p>
<div class="s"><img src="{shot}"></div></html>"""
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
                f.write(html)
            pg.goto(Path(f.name).as_uri()); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(300)
            Path(f.name).unlink()
            pg.screenshot(path=str(V2 / "assets" / "og" / f"{c['lang']}.png"))
            print("og", c["lang"])
        b.close()


if __name__ == "__main__":
    main()
