"""Build the Many Worlds Cloud product sheet (HTML, printed to PDF by print_pdf.js), sales deck (PPTX) and texts.md
per language from materials/content/<lang>.json. Laid out like spacerisk/tools/build_materials.py; the look follows the Historian
website: ink on paper, ruled, monospace labels.

    pip install jinja2 python-pptx
    python cloud/tools/build_materials.py && node cloud/tools/print_pdf.js
"""
import html
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["en", "nb", "es"]
INK, PAPER, MUTED, LINE, SOFT, WARM = (18, 24, 31), (251, 252, 253), (98, 102, 107), (217, 224, 231), (240, 243, 246), (253, 244, 236)
HUES = [(111, 29, 18), (180, 82, 43), (230, 180, 156), (243, 228, 218)]  # how bad, dark to light
TEAL, MINT, AMBER = (18, 52, 59), (127, 214, 200), (242, 184, 75)
SANS, MONO = "Arial", "Consolas"
# an invented set of risks for the five by five matrix: (likelihood, consequence) -> how many
MATRIX = {(4, 5): 1, (3, 4): 2, (5, 3): 1, (2, 4): 3, (3, 2): 2, (2, 2): 4}


def cell_hue(l, c):
    s = l * c
    return HUES[0] if s >= 20 else HUES[1] if s >= 12 else HUES[2] if s >= 6 else HUES[3]


# --- product sheet (HTML, one A4 page) -------------------------------------------------------------------

SHEET = """<!doctype html><html lang="{html_lang}"><head><meta charset="utf-8"><title>{product}</title><style>
@font-face {{ font-family: "Inter"; src: url("../../website/assets/fonts/InterVariable.woff2") format("woff2"); font-weight: 100 900; }}
@page {{ size: A4; margin: 0; }}
:root {{ --ink: #12181f; --paper: #fbfcfd; --muted: #62666b; --line: #d9e0e7; --soft: #f0f3f6; --warm: #fdf4ec;
  --mono: "DejaVu Sans Mono", ui-monospace, Menlo, Consolas, monospace; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ width: 210mm; height: 297mm; overflow: hidden; background: var(--paper); color: var(--ink); font: 400 8.6pt/1.42 "Inter", Arial, sans-serif;
  padding: 9mm 14mm 0; position: relative; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.lbl {{ font: 500 6.4pt var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }}
.brand {{ display: flex; align-items: center; gap: 3mm; font-weight: 700; font-size: 12pt; letter-spacing: -.015em; }}
.brand img {{ width: 8mm; height: 8mm; }}
.brand .lbl {{ margin-left: auto; }}
h1 {{ font-size: 24pt; font-weight: 680; letter-spacing: -.03em; line-height: 1.06; margin-top: 5mm; max-width: 150mm; text-wrap: balance; }}
.sub {{ font-size: 10.5pt; font-weight: 500; line-height: 1.4; margin-top: 3.5mm; max-width: 160mm; }}
.meta {{ display: flex; flex-wrap: wrap; gap: 1mm 7mm; margin-top: 5mm; padding-bottom: 3.5mm; border-bottom: 3px solid var(--ink); font: 7.2pt var(--mono); }}
.meta b {{ font-weight: 500; color: var(--muted); letter-spacing: .1em; text-transform: uppercase; font-size: 6.4pt; margin-right: 1.5mm; }}
.flow {{ display: flex; align-items: stretch; margin-top: 4.5mm; }}
.flow div {{ flex: 1; border: 1.5px solid var(--ink); padding: 2.2mm 2mm; font-weight: 600; font-size: 8pt; text-align: center; display: flex; align-items: center; justify-content: center; background: #fff; }}
.flow div.on {{ background: var(--ink); color: #fff; }}
.flow i {{ flex: 0 0 5mm; align-self: center; text-align: center; font-style: normal; font-family: var(--mono); color: var(--muted); }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 8mm; margin-top: 3.5mm; }}
.sec {{ border-top: 1px solid var(--line); padding: 2.2mm 0 2mm; }}
.sec h2 {{ font-size: 10pt; font-weight: 650; letter-spacing: -.015em; line-height: 1.2; margin: 1mm 0 1.2mm; }}
.sec p {{ color: #2b3138; }}
.boxes {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; margin-top: 2.5mm; }}
.box {{ border: 1.5px solid var(--ink); background: #fff; padding: 2.6mm 3mm; }}
.box b {{ display: block; font-size: 11pt; letter-spacing: -.015em; margin: .6mm 0 1mm; }}
.sample {{ margin-top: 3.5mm; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 1.5mm; font-size: 7.8pt; }}
th {{ text-align: left; font: 500 6.2pt var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); padding: 1mm 2mm 1mm 0; border-bottom: 1.5px solid var(--ink); }}
td {{ padding: 1.3mm 2mm 1.3mm 0; border-bottom: 1px solid var(--line); vertical-align: top; }}
.sev {{ display: inline-block; min-width: 15mm; padding: .3mm 1.6mm; font: 500 6.6pt var(--mono); text-transform: uppercase; letter-spacing: .08em; }}
.s0 {{ background: #6f1d12; color: #fff; }} .s1 {{ background: #b4522b; color: #fff; }} .s2 {{ background: #e6b49c; }} .s3 {{ background: #f3e4da; }}
.note {{ font: 6.2pt var(--mono); color: var(--muted); margin-top: 1.2mm; }}
footer {{ position: absolute; left: 0; right: 0; bottom: 0; height: 15mm; background: var(--ink); color: #fff; padding: 0 14mm; display: flex; align-items: center; gap: 6mm; }}
footer b {{ font-size: 10.5pt; letter-spacing: -.01em; }}
footer span {{ margin-left: auto; font: 7.4pt var(--mono); text-align: right; line-height: 1.5; }}
</style></head><body>
<div class="brand"><img src="../../website/assets/logo.svg" alt="">{product}<span class="lbl">{eyebrow}</span></div>
<h1>{headline}</h1>
<p class="sub">{sub}</p>
<div class="meta">{meta}</div>
<div class="flow">{flow}</div>
<div class="grid">{sections}</div>
<div class="boxes">{boxes}</div>
<div class="sample"><span class="lbl">{sample_title}</span>
<table><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table><p class="note">{sample_note}</p></div>
<footer><b>{cta_title}</b><span>{cta_button}<br>{email}</span></footer>
</body></html>"""


def product_sheet(c, out):
    e = html.escape
    flow = "<i>→</i>".join(f'<div class="{"on" if i == 2 else ""}">{e(s)}</div>' for i, s in enumerate(c["flow"]))
    secs = "".join(f'<div class="sec"><span class="lbl">{e(s["label"])}</span><h2>{e(s["title"])}</h2><p>{e(s["text"])}</p></div>' for s in c["sections"])
    boxes = "".join(f'<div class="box"><span class="lbl">{e(b["t"])}</span><b>{e(b["k"])}</b>{e(b["d"])}</div>' for b in c["boxes"])
    sev = {0: "s0", 1: "s1", 2: "s1", 3: "s2"}
    rows = "".join("<tr>" + f'<td><span class="sev {sev[i]}">{e(r[0])}</span></td>' + "".join(f"<td>{e(x)}</td>" for x in r[1:]) + "</tr>"
                   for i, r in enumerate(c["sample"]["rows"][:3]))
    out.write_text(SHEET.format(html_lang=c["html_lang"], product=e(c["product"]), eyebrow=e(c["eyebrow"]), headline=e(c["headline"]), sub=e(c["sub"]),
                                meta="".join(f'<span><b>{e(m["k"])}</b>{e(m["v"])}</span>' for m in c["meta"]), flow=flow, sections=secs, boxes=boxes,
                                sample_title=e(c["sample"]["title"]), th="".join(f"<th>{e(x)}</th>" for x in c["sample"]["cols"]), rows=rows,
                                sample_note=e(c["sample"]["note"]), cta_title=e(c["cta"]["title"]), cta_button=e(c["cta"]["button"]), email=e(c["cta"]["email"])),
                   encoding="utf-8")


# --- sales deck (PPTX, 16:9) -----------------------------------------------------------------------------

def sales_deck(c, out):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    total = 11

    def rect(s, x, y, w, h, fill=None, line=None, lw=1.25):
        r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        st = r._element.find(qn('p:style'))
        if st is not None:
            r._element.remove(st)
        if fill is None:
            r.fill.background()
        else:
            r.fill.solid(); r.fill.fore_color.rgb = RGBColor(*fill)
        if line is None:
            r.line.fill.background()
        else:
            r.line.color.rgb = RGBColor(*line); r.line.width = Pt(lw)
        return r

    def text(s, x, y, w, h, value, size, bold=False, colour=INK, font=SANS, align=None, anchor=None, gap=6, spacing=None):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        if anchor:
            tf.vertical_anchor = anchor
        for i, line in enumerate(value if isinstance(value, list) else [value]):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r = p.add_run()
            r.text = line
            r.font.size, r.font.bold, r.font.name = Pt(size), bold, font
            r.font.color.rgb = RGBColor(*colour)
            p.space_after = Pt(gap)
            if spacing:
                p.line_spacing = spacing
            if align:
                p.alignment = align
        return tb

    def label(s, x, y, w, value, colour=MUTED, size=11):
        text(s, x, y, w, 0.3, value.upper(), size, False, colour, MONO)

    def slide(lbl, title, n, title_w=11.6):
        s = prs.slides.add_slide(blank)
        rect(s, 0, 0, 13.333, 7.5, PAPER)
        rect(s, 0.7, 0.55, 11.933, 0.045, INK)
        label(s, 0.7, 0.72, 8, lbl)
        text(s, 9.6, 0.72, 3.033, 0.3, f"{c['product'].upper()}  ·  {n:02d}/{total:02d}", 10, False, MUTED, MONO, align=3)
        text(s, 0.7, 1.15, title_w, 1.5, title, 32, True, INK, spacing=0.95)
        return s

    def points(s, x, y, w, items, size=17, step=0.95):
        for k, it in enumerate(items):
            rect(s, x, y + k * step, w, 0.012, LINE)
            text(s, x, y + k * step + 0.14, 0.5, 0.4, f"{k + 1:02d}", 11, False, MUTED, MONO)
            text(s, x + 0.6, y + k * step + 0.1, w - 0.6, step - 0.15, it, size, False, INK)

    def body(s, sec, n_points_y=2.95):
        text(s, 0.7, 2.95, 5.1, 3.9, sec["text"], 20, False, (43, 49, 56), spacing=1.1)
        points(s, 6.5, n_points_y, 6.133, sec["points"], 19, 1.25)

    secs = {x["id"]: x for x in c["sections"]}

    # 1 cover
    s = prs.slides.add_slide(blank)
    rect(s, 0, 0, 13.333, 7.5, PAPER)
    s.shapes.add_picture(str(ROOT / "materials" / "assets" / "logo.png"), Inches(0.7), Inches(0.6), Inches(0.5))
    text(s, 1.35, 0.66, 6, 0.4, c["product"], 20, True)
    label(s, 0.7, 1.75, 10, c["eyebrow"])
    text(s, 0.7, 2.15, 11.9, 2.4, c["headline"], 46, True, INK, spacing=0.92)
    text(s, 0.7, 4.7, 9.2, 1.3, c["sub"], 19, False, INK, spacing=1.08)
    rect(s, 0.7, 6.72, 11.933, 0.045, INK)
    x = 0.7
    for m in c["meta"]:
        w = 2.25 if len(m["v"]) < 26 else 4.4
        text(s, x, 6.2, w, 0.2, m["k"].upper(), 9, False, MUTED, MONO)
        text(s, x, 6.4, w, 0.25, m["v"], 11, False, INK, MONO)
        x += w + 0.15

    # 2 problem
    s = slide(c["problem"]["label"], c["problem"]["title"], 2)
    points(s, 0.7, 2.95, 11.933, c["problem"]["bullets"], 20, 1.0)

    # 3 how it works + it only reads
    sec = secs["reads"]
    s = slide(c["flow_title"] + "  ·  " + sec["label"], sec["title"], 3)
    bw, gapw = 2.1, 0.358
    for k, st in enumerate(c["flow"]):
        x = 0.7 + k * (bw + gapw)
        on = k == 2
        r = rect(s, x, 2.75, bw, 0.85, INK if on else (255, 255, 255), INK, 1.5)
        text(s, x + 0.08, 2.75, bw - 0.16, 0.85, st, 14, True, (255, 255, 255) if on else INK, align=2, anchor=MSO_ANCHOR.MIDDLE, gap=0)
        if k < len(c["flow"]) - 1:
            text(s, x + bw, 2.75, gapw, 0.85, "→", 16, False, MUTED, MONO, align=2, anchor=MSO_ANCHOR.MIDDLE, gap=0)
    text(s, 0.7, 4.05, 5.1, 3, sec["text"], 17, False, (43, 49, 56), spacing=1.1)
    points(s, 6.5, 4.0, 6.133, sec["points"], 15, 0.88)

    # 4 trust
    sec = secs["trust"]
    s = slide(sec["label"], sec["title"], 4)
    body(s, sec)

    # 5 findings, with the illustration table
    sec = secs["findings"]
    s = slide(sec["label"], sec["title"], 5)
    sm = c["sample"]
    cols = [(0.7, 1.55), (2.3, 5.2), (7.6, 2.3), (10.0, 2.633)]
    for (x, w), h in zip(cols, sm["cols"]):
        text(s, x, 2.72, w, 0.25, h.upper(), 9.5, False, MUTED, MONO)
    rect(s, 0.7, 3.0, 11.933, 0.025, INK)
    sev = [HUES[0], HUES[1], HUES[1], HUES[2]]
    for k, row in enumerate(sm["rows"]):
        y = 3.1 + k * 0.56
        rect(s, cols[0][0], y + 0.06, 1.35, 0.32, sev[k])
        text(s, cols[0][0], y + 0.06, 1.35, 0.32, row[0].upper(), 10, False, INK if k == 3 else (255, 255, 255), MONO, align=2, anchor=MSO_ANCHOR.MIDDLE, gap=0)
        for (x, w), v in zip(cols[1:], row[1:]):
            text(s, x, y + 0.08, w - 0.15, 0.4, v, 13.5, False, INK)
        rect(s, 0.7, y + 0.5, 11.933, 0.012, LINE)
    text(s, 0.7, 5.42, 11.9, 0.25, sm["note"], 9.5, False, MUTED, MONO)
    for k, it in enumerate(sec["points"]):
        x = 0.7 + k * 4.05
        text(s, x, 5.92, 0.4, 0.3, f"{k + 1:02d}", 10, False, MUTED, MONO)
        text(s, x + 0.45, 5.88, 3.4, 1.2, it, 13, False, INK)

    # 6 one report, three readers
    q = c["questions"]
    s = slide(q["label"], q["title"], 6)
    for k, col in enumerate(q["columns"]):
        x = 0.7 + k * 6.15
        rect(s, x, 2.85, 5.78, 0.025, INK)
        label(s, x, 2.98, 5.7, col["title"], INK)
        text(s, x, 3.42, 5.7, 3.8, col["items"], 14.5, False, INK, gap=5.5)

    # 7 requirements
    sec = secs["compliance"]
    s = slide(sec["label"], sec["title"], 7)
    body(s, sec)

    # 8 conclusions: three boxes and the matrix
    sec = secs["conclusions"]
    s = slide(sec["label"], sec["title"], 8)
    for k, b in enumerate(c["boxes"]):
        y = 2.85 + k * 1.02
        rect(s, 0.7, y, 4.9, 0.9, (255, 255, 255), INK, 1.5)
        text(s, 0.88, y + 0.1, 1.6, 0.4, b["k"], 17, True)
        text(s, 0.88, y + 0.5, 1.6, 0.3, b["t"].upper(), 7.5, False, MUTED, MONO)
        text(s, 2.5, y + 0.1, 3.0, 0.75, b["d"], 10.5, False, (43, 49, 56))
    size = 0.5
    mx, my = 6.35, 2.85
    for l in range(1, 6):
        for co in range(1, 6):
            x, y = mx + (co - 1) * size, my + (5 - l) * size
            rect(s, x, y, size - 0.03, size - 0.03, cell_hue(l, co))
            n = MATRIX.get((l, co))
            if n:
                text(s, x, y, size - 0.03, size - 0.03, str(n), 13, True, (255, 255, 255) if l * co >= 12 else INK, MONO, align=2, anchor=MSO_ANCHOR.MIDDLE, gap=0)
    text(s, mx, my + 5 * size + 0.05, 2.5, 0.2, c["sample"]["consequence"].upper() + " →", 8, False, MUTED, MONO)
    text(s, mx, my + 5 * size + 0.27, 2.5, 0.4, c["sample"]["note"], 7.5, False, MUTED, MONO)
    points(s, 9.25, 2.85, 3.383, sec["points"], 12, 1.25)

    # 9 every account at once
    sec = secs["accounts"]
    s = slide(sec["label"], sec["title"], 9)
    body(s, sec)

    # 10 one risk picture
    p = c["portfolio"]
    s = slide(p["label"], p["title"], 10)
    text(s, 0.7, 2.9, 11, 0.9, p["text"], 17, False, (43, 49, 56))
    for k, it in enumerate(p["items"][:3]):
        y = 4.0 + k * 0.95
        on = k == 1
        rect(s, 0.7, y, 5.4, 0.8, INK if on else (255, 255, 255), INK, 1.5)
        text(s, 0.9, y + 0.1, 5.0, 0.3, it["k"], 15, True, (255, 255, 255) if on else INK)
        text(s, 0.9, y + 0.42, 5.0, 0.3, it["d"], 11.5, False, (220, 226, 232) if on else MUTED)
        text(s, 6.1, y, 1.4, 0.8, "→", 20, False, MUTED, MONO, align=2, anchor=MSO_ANCHOR.MIDDLE, gap=0)
    it = p["items"][3]
    rect(s, 7.5, 4.0, 5.133, 2.7, TEAL)
    text(s, 7.8, 4.25, 4.5, 0.5, it["k"], 26, True, (255, 255, 255))
    text(s, 7.8, 4.95, 4.5, 0.8, it["d"], 15, False, MINT)
    text(s, 7.8, 5.95, 4.5, 0.5, c["flow"][3], 13, False, AMBER, MONO)

    # 11 next step
    s = slide(c["cta"]["label"], c["cta"]["title"], 11)
    text(s, 0.7, 2.95, 9, 1.3, c["cta"]["text"], 20, False, (43, 49, 56), spacing=1.1)
    rect(s, 0.7, 4.6, 3.2, 0.75, INK)
    text(s, 0.7, 4.6, 3.2, 0.75, c["cta"]["button"], 17, True, (255, 255, 255), align=2, anchor=MSO_ANCHOR.MIDDLE, gap=0)
    text(s, 4.2, 4.6, 8, 0.75, c["cta"]["email"], 15, False, INK, MONO, anchor=MSO_ANCHOR.MIDDLE, gap=0)
    text(s, 0.7, 6.6, 11.9, 0.3, c["footer"].upper(), 10, False, MUTED, MONO)
    prs.save(out)


def texts_md(c, out):
    t, h = c["texts"], c["h"]
    lines = [f"# {c['product']} · {c['lang_name']}", "", f"## {h['taglines']}", *[f"- {x}" for x in t["taglines"]], "",
             f"## {h['short']}", t["short"], "", f"## {h['medium']}", t["medium"], "", f"## {h['long']}", t["long"], "",
             f"## {h['blurbs']}", *[f"- **{s['label']}:** {s['title']} {s['text']}" for s in c["sections"]], "", f"## {h['boilerplate']}", t["boilerplate"], ""]
    out.write_text("\n".join(lines), encoding="utf-8")


def keys(v, path=""):
    if isinstance(v, dict):
        return {q for k, x in v.items() for q in keys(x, f"{path}.{k}")}
    if isinstance(v, list):
        return {q for i, x in enumerate(v) for q in keys(x, f"{path}[{i}]")}
    return {path}


def main():
    en = keys(json.loads((ROOT / "materials" / "content" / "en.json").read_text(encoding="utf-8")))
    for lang in LANGS:
        c = json.loads((ROOT / "materials" / "content" / f"{lang}.json").read_text(encoding="utf-8"))
        assert keys(c) == en, f"{lang}: differs from en at {sorted(keys(c) ^ en)[:5]}"
        out = ROOT / "materials" / lang
        out.mkdir(parents=True, exist_ok=True)
        product_sheet(c, out / "cloud-product-sheet.html")
        sales_deck(c, out / "cloud-sales-deck.pptx")
        texts_md(c, out / "texts.md")
        print("built", lang)


if __name__ == "__main__":
    main()
