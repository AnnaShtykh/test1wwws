#!/usr/bin/env python3
"""Client setup-guide renderer: data.json + template -> branded PDF.

Usage: python3 render_setup_guide.py <data.json> <output.pdf>

Always uses setup-guide-template.html, the file next to this script.

data.json fields:
  company_name   Display name of the brand, e.g. "Fernway"
  slug           The slug used for <slug>-skill / <slug>-project, e.g. "fernway"
  has_fonts      true/false — whether <slug>-project/Sources/ has real font
                 files, so a font-upload sentence gets added to step 2

This is Spaceberry's own client-facing collateral, not the target brand's
material — the accent color (#fc4a22) and the rest of the visual system in
setup-guide-template.html are Spaceberry's fixed brand constants and must not
be swapped for the generated brand's own colors.
"""
import json, sys, glob, pathlib

HERE = pathlib.Path(__file__).parent

def render(data_path, out_pdf):
    data = json.loads(pathlib.Path(data_path).read_text())
    tpl = (HERE / "setup-guide-template.html").read_text()

    font_note = ""
    if data.get("has_fonts"):
        font_note = ("The Sources folder also includes your real font "
                      "file(s) — that lets Claude or ChatGPT use your actual "
                      "typeface when it builds a real document for you (like "
                      "a Word file or a PDF), instead of just describing it "
                      "in words. ")

    repl = {
        "{{COMPANY_NAME}}": data["company_name"],
        "{{SLUG}}": data["slug"],
        "{{FONT_NOTE}}": font_note,
    }
    for k, v in repl.items():
        tpl = tpl.replace(k, v)

    html_path = pathlib.Path(out_pdf).with_suffix(".html")
    html_path.write_text(tpl)

    from playwright.sync_api import sync_playwright
    chromium = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))
    exe = chromium[-1] if chromium else None
    footer = (
        '<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5px;color:#909090;'
        'padding:0 12mm;display:flex;justify-content:space-between;">'
        '<span>Delivered by Spaceberry</span>'
        '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if exe: kw["executable_path"] = exe
        b = p.chromium.launch(**kw)
        pg = b.new_page()
        pg.goto(html_path.resolve().as_uri())
        pg.emulate_media(media="print")
        pg.pdf(path=str(out_pdf), format="A4", print_background=True,
               display_header_footer=True, header_template="<span></span>",
               footer_template=footer,
               margin={"top": "13mm", "bottom": "16mm", "left": "12mm", "right": "12mm"})
        b.close()
    print("wrote", out_pdf)

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
