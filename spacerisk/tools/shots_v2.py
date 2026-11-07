"""Screens for the v2 site (ADR 0091 in the app repo): python tools/shots_v2.py APP_LANG [name...]

Needs a running SpaceRisk on BASE (default http://127.0.0.1:5081) with the banking showcase, ISO 27001, ISO 22301/45001,
the cyber area and a SharpHound upload switched on, and the login ceo / demo1234. Fictional data only. Writes
v2/assets/shots/<APP_LANG>/<name>.webp at 2x. RID picks the risk for the bowtie shot (default 5)."""
import io
import os
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

BASE = os.environ.get("BASE", "http://127.0.0.1:5081")
RID = os.environ.get("RID", "5")
OUT = Path(__file__).resolve().parent.parent / "v2" / "assets" / "shots"
SHOTS = {  # name: (path, scroll-to selector, width, height); two-up shots are narrower so their text reads larger
    "dashboard": ("/executive", None, 1440, 900),
    "summary": ("/executive/summary", None, 1440, 900),
    "cyber": ("/cyber/", None, 1440, 900),
    "bowtie": (f"/risks/{RID}", ".bowtie", 1100, 760),
    "panel": ("/barriers/panel", None, 1100, 760),
    "iso": ("/iso27001/readiness", None, 1100, 760),
    "compliance": ("/compliance/iso22301", None, 1100, 760),
    "paths": ("/cyber/assessments/targets/1", None, 1100, 800),
}


def main(lang, names):
    out = OUT / lang
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name in names or list(SHOTS):
            path, sel, w, h = SHOTS[name]
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, color_scheme="light")
            pg = ctx.new_page()
            pg.goto(BASE + "/login"); pg.fill("#username", "ceo"); pg.fill("#password", "demo1234"); pg.press("#password", "Enter")
            pg.wait_for_load_state()
            pg.goto(f"{BASE}/lang/{lang}"); pg.goto(BASE + path); pg.wait_for_timeout(400)
            pg.add_style_tag(content=".cycle-banner,.banner.info{display:none!important}")
            if sel and pg.query_selector(sel):
                pg.eval_on_selector(sel, "e => window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - 24)")
                pg.wait_for_timeout(200)
            Image.open(io.BytesIO(pg.screenshot())).convert("RGB").save(out / f"{name}.webp", "WEBP", quality=82, method=6)
            ctx.close()
        b.close()
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
