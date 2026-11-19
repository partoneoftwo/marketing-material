"""Capture the product screens used on the website from a running Many Worlds Historian (simulated plants).
Start the app first:  MWH_SIMULATED_SITES=6 npm start   (in the historian repo; wait until every plant is read)
Then:                 python historian/tools/shots.py [http://127.0.0.1:8780]
Writes PNG originals to historian/screenshots/ and WebP copies to historian/website/assets/shots/en/."""
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8780"
W = 924  # the report column plus its padding
# page -> (name, text of the section heading to start at, offset above it, height), all in CSS pixels
JOBS = {
    "/conclusions": [("conclusions", "01Risks", -348, 830)],
    "/report": [("trust", "Can these numbers be trusted", -20, 760), ("findings", "Findings — ranked", -10, 800),
                ("ai", "AI Agents Watch", -10, 800), ("controllers", "Controller changes", -10, 800)],
    "/organization": [("organization", "Which plant needs attention first", -420, 1180)],
}
TOP = """(t) => { const h = [...document.querySelectorAll('h2')].find(e => e.textContent.includes(t));
  const s = h.closest('section') || h; return Math.round(s.getBoundingClientRect().top + scrollY); }"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    for path, crops in JOBS.items():
        page = browser.new_page(viewport={"width": W, "height": 900}, device_scale_factor=2)
        page.goto(BASE + path, timeout=180000, wait_until="networkidle")
        page.wait_for_timeout(1500)
        for name, heading, off, height in crops:
            y = page.evaluate(TOP, heading)
            png = ROOT / "screenshots" / f"{name}.png"
            page.screenshot(path=str(png), full_page=True, clip={"x": 0, "y": max(0, y + off), "width": W, "height": height})
            Image.open(png).save(ROOT / "website" / "assets" / "shots" / "en" / f"{name}.webp", quality=84, method=6)
            print("wrote", name)
    browser.close()
