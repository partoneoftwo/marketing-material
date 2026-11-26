"""Build the Hyperdrive sales deck: materials/en/hyperdrive-sales-deck.pptx (12 slides, 16:9) with real product screens
cut from the PNG originals in screenshots/. The look follows the website: the navy of the app's sidebar, grey paper,
white cards, one blue, and the stage colours from the app's overview.
Needs python-pptx and pillow. Run: python hyperdrive/tools/build_deck.py"""
import io
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "materials" / "en" / "hyperdrive-sales-deck.pptx"
EMAIL = "thomas.frivold@frivolddigital.com"
FONT, MONO = "Arial", "Courier New"
INK, PAPER, CARD, MUTED, LINE = "0F172A", "F6F7F9", "FFFFFF", "55627A", "DDE2EA"
BRAND, ON_INK, DIM = "1F57D6", "C5CEDE", "8B98B0"
LANDING, RAW, NORMALISED, MODELS, OUTPUTS = "F59E0B", "0EA5E9", "10B981", "14B8A6", "8B5CF6"
W, H, M = 13.333, 7.5, 0.6
SIDEBAR = 448


def rgb(h):
    return RGBColor.from_string(h)


def crop(name, box=None, width=1800):
    """A PNG original, cut to box (left, top, right, bottom in original pixels) and scaled down, as bytes plus its ratio."""
    with Image.open(ROOT / "screenshots" / f"{name}.png") as im:
        im = im.convert("RGB")
        if box:
            im = im.crop(tuple(v if v is not None else (im.width, im.height)[i % 2] for i, v in enumerate(box)))
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        buf.seek(0)
        return buf, im.height / im.width


class Deck:
    def __init__(self):
        self.p = Presentation()
        self.p.slide_width, self.p.slide_height = Inches(W), Inches(H)
        self.n = 0

    def slide(self, dark=False, notes=""):
        s = self.p.slides.add_slide(self.p.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(INK if dark else PAPER)
        self.n += 1
        if not dark:
            self.text(s, M, 6.98, 4, 0.3, [("Hyperdrive", 10, True, MUTED)])
            self.text(s, W - M - 1, 6.98, 1, 0.3, [(str(self.n), 10, False, MUTED)], align="r")
        if notes:
            s.notes_slide.notes_text_frame.text = notes
        return s

    def text(self, s, x, y, w, h, paras, align="l", anchor="t", font=FONT, gap=6):
        """paras: (text, size, bold, colour) or (text, size, bold, colour, font)."""
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        for i, para in enumerate(paras):
            t, size, bold, colour = para[:4]
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": 1, "c": 2, "r": 3}[align]
            p.space_after = Pt(gap)
            r = p.add_run()
            r.text = t
            r.font.size, r.font.bold, r.font.name = Pt(size), bold, (para[4] if len(para) > 4 else font)
            r.font.color.rgb = rgb(colour)
        return tb

    def box(self, s, x, y, w, h, fill=CARD, line=LINE, radius=0.08, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
        b = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        b.shadow.inherit = False
        b.fill.solid()
        b.fill.fore_color.rgb = rgb(fill)
        if line:
            b.line.color.rgb = rgb(line)
            b.line.width = Pt(0.75)
        else:
            b.line.fill.background()
        if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            b.adjustments[0] = min(0.5, radius / min(w, h))
        return b

    def dot(self, s, x, y, colour, d=0.16):
        return self.box(s, x, y, d, d, fill=colour, line=None, shape=MSO_SHAPE.OVAL)

    def head(self, s, tag, title, colour=INK):
        self.dot(s, M, 0.62, colour)
        self.text(s, M + 0.28, 0.58, 6, 0.3, [(tag.upper(), 11, True, MUTED, MONO)])
        self.text(s, M, 0.95, W - 2 * M, 0.7, [(title, 30, True, INK)])

    def shot(self, s, name, x, y, w=None, h=None, box=None, alt=""):
        """Place a screen inside the w x h area (inches), keeping its ratio, with a hairline frame. Returns (w, h) used."""
        buf, ratio = crop(name, box)
        if w and h and w * ratio > h:
            w = h / ratio
        pic = s.shapes.add_picture(buf, Inches(x), Inches(y), width=Inches(w))
        pic.line.color.rgb = rgb(LINE)
        pic.line.width = Pt(0.75)
        pic._element.xpath("./p:nvPicPr/p:cNvPr")[0].set("descr", alt)
        return w, w * ratio

    def points(self, s, x, y, w, items, colour=NORMALISED, size=15, step=0.78):
        for i, t in enumerate(items):
            self.dot(s, x, y + i * step + 0.07, colour, 0.13)
            self.text(s, x + 0.32, y + i * step, w - 0.32, step, [(t, size, False, INK)])


def build():
    d = Deck()

    # 1 title
    s = d.slide(dark=True, notes="Hyperdrive is a self-hosted data platform. It does the everyday extract, load and transform work on your own server, on SQLite.")
    logo = io.BytesIO()
    with Image.open(ROOT / "screenshots" / "01-overview.png") as im:
        im.crop((30, 26, 90, 86)).resize((120, 120), Image.LANCZOS).save(logo, "PNG")
    logo.seek(0)
    s.shapes.add_picture(logo, Inches(M), Inches(0.6), width=Inches(0.42))
    d.text(s, M + 0.56, 0.6, 3, 0.42, [("Hyperdrive", 18, True, "FFFFFF")], anchor="m")
    d.text(s, M, 2.0, 5.6, 0.3, [("SELF-HOSTED DATA PLATFORM", 12, True, "6EE7B7", MONO)])
    d.text(s, M, 2.45, 5.7, 2.3, [("Your everyday data pipelines, on one small server", 40, True, "FFFFFF")])
    d.text(s, M, 4.95, 5.3, 1.3, [("The extract, load and transform work that usually ends up in AWS Glue or Microsoft Fabric. On your own machine, in SQLite, set up in the browser.", 16, False, ON_INK)])
    d.shot(s, "01-overview", 6.45, 1.3, w=9.6, box=(0, 0, None, 1290), alt="Hyperdrive overview with pipeline counts and recent runs")

    # 2 problem
    s = d.slide(notes="Most data work in a normal company is ordinary: exports, a few APIs, a few joins. The platforms sold for it are built for a much bigger problem.")
    d.head(s, "Why", "Everyday data work rarely needs a cloud platform")
    d.text(s, M, 2.1, 4.9, 3.5, [
        ("Most pipelines move CSV exports and API responses between a handful of systems.", 20, True, INK),
        ("Hyperdrive is built for that work, and only that work. It aims at the regular cases and leaves the rest to the big platforms.", 16, False, MUTED)], gap=16)
    cards = [("The work is ordinary", "CSV exports, a few REST APIs, some joins, and clean tables for the people and systems that need them."),
             ("The platform is not", "Big data platforms bring clusters to size, services to connect and a new toolset to learn."),
             ("The data moves away", "With a cloud platform the data sits in someone else's cloud, and so does the bill for it.")]
    for i, (t, b) in enumerate(cards):
        y = 2.0 + i * 1.55
        d.box(s, 6.2, y, W - M - 6.2, 1.35)
        d.box(s, 6.48, y + 0.4, 0.55, 0.55, fill=INK, line=None, shape=MSO_SHAPE.OVAL)
        d.text(s, 6.48, y + 0.4, 0.55, 0.55, [(str(i + 1), 16, True, "FFFFFF")], align="c", anchor="m")
        d.text(s, 7.3, y + 0.24, W - M - 7.6, 1.0, [(t, 17, True, INK), (b, 14, False, MUTED)], gap=3)

    # 3 pipeline
    s = d.slide(notes="Every source goes through the same five stages. Landing and raw keep everything as it arrived, so normalised tables can always be rebuilt when a rule changes.")
    d.head(s, "The pipeline", "Five steps, and you can look inside every one")
    stages = [("Landing", "Kept as received", "Every file and API response is stored exactly as it arrived.", LANDING),
              ("Raw", "Loaded as text", "One table per source, original column names, every value as text.", RAW),
              ("Normalised", "Typed and clean", "Clean names, real types, ISO dates, one row per key.", NORMALISED),
              ("Models", "Shaped with SQL", "SELECT statements kept as tables, for joins and aggregates.", MODELS),
              ("Out", "Delivered", "REST, CSV files and pushes to other systems.", OUTPUTS)]
    gap, cw = 0.42, (W - 2 * M - 4 * 0.42) / 5
    for i, (k, t, b, c) in enumerate(stages):
        x = M + i * (cw + gap)
        d.box(s, x, 2.15, cw, 3.45)
        d.dot(s, x + 0.25, 2.45, c, 0.3)
        d.text(s, x + 0.25, 2.98, cw - 0.5, 0.3, [(k.upper(), 11, True, MUTED, MONO)])
        d.text(s, x + 0.25, 3.32, cw - 0.5, 2.1, [(t, 18, True, INK), (b, 14, False, MUTED)], gap=6)
        if i:
            d.text(s, x - gap, 3.4, gap, 0.4, [("→", 18, False, MUTED)], align="c", anchor="m")
    d.text(s, M, 5.95, W - 2 * M, 0.8, [("Nothing is thrown away on the way in. Change a rule tomorrow, and the tables are rebuilt from what actually arrived.", 16, False, MUTED)])

    # 4 in
    s = d.slide(notes="Three kinds of source: CSV upload, REST pull on a schedule, and REST push from another system. The form tests the call before saving.")
    d.head(s, "In", "Files and APIs in, without writing a connector", LANDING)
    d.points(s, M, 2.1, 5.3, [
        "CSV with comma or semicolon. Delimiter and encoding are detected.",
        "REST APIs pulled on a schedule, with four kinds of paging.",
        "JSON or CSV pushed in over REST with an API key.",
        "Sign-in built in: bearer token, basic, API key, OAuth 2.0 client credentials.",
        "A test call shows the first records before anything is saved."], LANDING, step=0.9)
    d.shot(s, "03-new-rest-source", 6.5, 1.95, w=W - M - 6.5, h=4.85, box=(SIDEBAR + 100, 1180, 2880 - 100, 2540), alt="New REST pull source: records path, paging and a test call that returned 100 records")

    # 5 normalise
    s = d.slide(notes="Types are detected and can be overridden per column. The preview shows raw rows beside the normalised result. A value that does not fit becomes null and is counted, so a bad row never stops a load.")
    d.head(s, "Normalise", "Messy columns become typed tables", NORMALISED)
    w, h = d.shot(s, "06-normalisation", M, 1.95, w=6.9, box=(SIDEBAR + 100, 380, 2880 - 100, 1440), alt="Normalisation rules: each raw column with its new name and detected type")
    d.text(s, M, 1.95 + h + 0.25, 6.9, 1.2, [("Types are detected from the data, and every column can be overridden. A value that does not fit becomes null and is counted, so a bad row never stops a load.", 14, False, MUTED)])
    x = 7.95
    d.text(s, x, 1.95, 2.2, 0.3, [("AS RECEIVED", 11, True, MUTED, MONO)])
    d.text(s, x + 2.75, 1.95, 2.2, 0.3, [("WHAT YOU GET", 11, True, MUTED, MONO)])
    rows = [("Kunde Nr", "kunde_nr"), ("1.234,56", "1234.56"), ("05.01.2024", "2024-01-05"), ("ja / nei", "1 / 0"), ("0150", "0150 (text)"), ("n/a", "null")]
    for i, (a, b) in enumerate(rows):
        y = 2.35 + i * 0.72
        d.box(s, x, y, 2.2, 0.56)
        d.text(s, x + 0.2, y, 2.0, 0.56, [(a, 15, False, INK, MONO)], anchor="m")
        d.text(s, x + 2.2, y, 0.55, 0.56, [("→", 16, False, MUTED)], align="c", anchor="m")
        d.box(s, x + 2.75, y, W - M - x - 2.75, 0.56, fill="E8F8F1", line="B7E8D3")
        d.text(s, x + 2.95, y, 2.0, 0.56, [(b, 15, True, "065F46", MONO)], anchor="m")

    # 6 models
    s = d.slide(notes="Try a query in the read-only workbench, save it as a model, and Hyperdrive keeps the result as a table and rebuilds it after every source run.")
    d.head(s, "Models", "Joins and aggregates are plain SQL", RAW)
    d.shot(s, "12-sql-workbench", M, 1.95, w=7.6, box=(SIDEBAR + 100, 220, 2880 - 100, 1380), alt="SQL workbench with a join of customers and orders and its result")
    d.points(s, 8.7, 2.1, W - M - 8.7, [
        "Try a query in the read-only workbench.",
        "Save it as a model, and the result is kept as a table.",
        "Models are rebuilt after every source run.",
        "No new language. If you can write SELECT, you can model."], RAW, step=1.0)

    # 7 out
    s = d.slide(notes="Every table is available over REST as JSON or CSV. Outputs write CSV files or push to other systems, on a schedule or right after a source has run. Authentication for the receiving system is set up in the form.")
    d.head(s, "Out", "Hand clean data to whatever needs it next", OUTPUTS)
    d.points(s, M, 2.1, 6.2, [
        "Any table as JSON or CSV over REST, with filters, sorting and search.",
        "CSV with comma, semicolon or tab, and decimal point or comma.",
        "Scheduled CSV files, and REST pushes to other systems.",
        "Outputs can fire as soon as the source they depend on has run.",
        "API keys that may push, read or both, limited to one table if needed."], OUTPUTS, step=0.9)
    d.shot(s, "14-output-rest-auth", 7.9, 1.75, w=W - M - 7.9, h=5.05, box=(672, 168, 2208, 2012), alt="REST output form: destination URL, API key in a header, batch size and when to run")

    # 8 operate
    s = d.slide(notes="The run log shows every job with who started it, rows and duration, and opens to its steps. A backup is a single file with data, configuration and credentials, restored from the interface.")
    d.head(s, "Operate", "Every run is logged, and one file backs it all up", LANDING)
    cw = (W - 2 * M - 0.5) / 2
    w, h = d.shot(s, "16-runs", M, 1.95, w=cw, box=(SIDEBAR + 100, 60, 2880 - 100, 1120), alt="Run log with status, rows and duration for each job")
    d.text(s, M, 1.95 + h + 0.25, cw, 1.6, [("Runs and schedules", 17, True, INK), ("Cron schedules for sources and outputs. Each run shows who started it, how many rows it moved and how long it took.", 14, False, MUTED)])
    x = M + cw + 0.5
    w2, h2 = d.shot(s, "19-backups", x, 1.95, w=cw, box=(SIDEBAR + 100, 60, 2880 - 100, 620), alt="Backups list with contents, size and a restore button")
    d.text(s, x, 1.95 + h + 0.25, cw, 1.6, [("Backup and restore", 17, True, INK), ("One file with the data, landing files, configuration and credentials. Made on a schedule, checked against checksums, and restored from the interface.", 14, False, MUTED)])

    # 9 explore
    s = d.slide(notes="Datasette is an open-source data explorer. It ships with Hyperdrive and reads the same SQLite files, behind the same login.")
    d.head(s, "Explore", "Datasette comes with it, on the same data", NORMALISED)
    d.shot(s, "17-datasette", M, 1.95, w=6.6, h=4.85, box=(0, 0, 1760, 1500), alt="Datasette showing the customer_revenue table")
    d.points(s, 7.6, 2.1, W - M - 7.6, [
        "The open-source data explorer, included and behind the same login.",
        "Filter, facet and export a table without asking for a report.",
        "Raw and normalised tables side by side.",
        "The data is ordinary SQLite, so any SQLite tool can open it too."], NORMALISED, step=1.0)

    # 10 fit
    s = d.slide(notes="Be clear about the limits. Hyperdrive suits tables up to some millions of rows. Runs execute one at a time, the interface has one login, and normalised tables are rebuilt in full on each run.")
    d.head(s, "Fit", "Built for millions of rows, not billions")
    d.box(s, M, 1.95, W - 2 * M, 1.75, fill=INK, line=None, radius=0.12)
    d.text(s, M + 0.35, 2.12, 8, 0.3, [("MEASURED ON ONE CSV FILE OF 524 MB", 11, True, DIM, MONO)])
    stats = [("5.3 M", "rows in the file"), ("22 s", "to load it into raw"), ("103 s", "to normalise it"), ("42 MB", "of memory, flat")]
    sw = (W - 2 * M - 0.7) / 4
    for i, (n, l) in enumerate(stats):
        d.text(s, M + 0.35 + i * sw, 2.45, sw - 0.2, 1.2, [(n, 40, True, "FFFFFF"), (l, 13, False, ON_INK)], gap=0)
    cw = (W - 2 * M - 0.4) / 2
    cols = [("A good fit when", NORMALISED, ["Your data arrives as CSV exports and REST APIs", "Tables hold up to some millions of rows", "One team owns the pipelines", "You want the data on a server you control"]),
            ("Look elsewhere when", "94A3B8", ["You have billions of rows, or need streaming", "Many runs must execute at once (runs go one at a time)", "People need different roles (there is a single login)", "Loads must be incremental (tables are rebuilt each run)"])]
    for i, (t, c, items) in enumerate(cols):
        x = M + i * (cw + 0.4)
        d.box(s, x, 3.95, cw, 2.85)
        d.dot(s, x + 0.3, 4.2, c)
        d.text(s, x + 0.58, 4.16, cw - 0.9, 0.3, [(t.upper(), 11, True, MUTED, MONO)])
        d.text(s, x + 0.3, 4.62, cw - 0.6, 2.1, [(q, 15, False, INK) for q in items], gap=14)

    # 11 run it
    s = d.slide(notes="Hyperdrive runs with Docker Compose as three containers, or on Cloudron as one app. All data is in three SQLite files.")
    d.head(s, "Run it", "Runs on your own server, with one command")
    boxes = [("Docker Compose", "3 containers", "Interface, API and Datasette. Only the interface is published, behind your own reverse proxy."),
             ("Cloudron", "1 app", "A Cloudron package runs the same parts in a single container. Cloudron's own backup covers all of the data."),
             ("Storage", "3 SQLite files", "Configuration, raw data and normalised data. Plain files that you own and can open with any SQLite tool.")]
    cw = (W - 2 * M - 0.8) / 3
    for i, (k, n, b) in enumerate(boxes):
        x = M + i * (cw + 0.4)
        d.box(s, x, 2.05, cw, 3.0)
        d.text(s, x + 0.3, 2.35, cw - 0.6, 0.3, [(k.upper(), 11, True, MUTED, MONO)])
        d.text(s, x + 0.3, 2.75, cw - 0.6, 2.1, [(n, 34, True, INK), (b, 15, False, MUTED)], gap=12)
    d.box(s, M, 5.4, W - 2 * M, 0.95, fill=INK, line=None, radius=0.12)
    d.text(s, M + 0.35, 5.4, W - 2 * M - 0.7, 0.95, [("docker compose up -d", 18, True, "6EE7B7", MONO)], anchor="m")

    # 12 contact
    s = d.slide(dark=True, notes="Ask what they move between systems today, and offer to show the same flow in Hyperdrive.")
    d.text(s, M, 2.1, 9, 0.3, [("NEXT STEP", 12, True, "6EE7B7", MONO)])
    d.text(s, M, 2.55, W - 2 * M, 1.0, [("See Hyperdrive with your own flow", 40, True, "FFFFFF")])
    d.text(s, M, 3.75, 8.5, 1.0, [("Tell us what you move between systems today, and we will show you the same flow running in Hyperdrive.", 18, False, ON_INK)])
    d.box(s, M, 5.3, 5.6, 0.7, fill=BRAND, line=None, radius=0.12)
    d.text(s, M, 5.3, 5.6, 0.7, [(EMAIL, 16, True, "FFFFFF")], align="c", anchor="m")
    d.text(s, M, 6.75, W - 2 * M, 0.3, [("Frivold Digital AS. Screens show demo data. AWS Glue and Microsoft Fabric are trademarks of their owners.", 10, False, DIM)])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    d.p.core_properties.title, d.p.core_properties.author = "Hyperdrive", "Frivold Digital AS"
    d.p.save(OUT)
    print("wrote", OUT.relative_to(ROOT), d.n, "slides")


if __name__ == "__main__":
    build()
