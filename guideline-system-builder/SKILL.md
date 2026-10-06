---
name: guideline-system-builder
description: Use when turning a company's brand guidelines (colors, typography, logo, icons, illustrations, tone of voice) into a portable Skill package (works in Claude and ChatGPT) plus a Project setup (Claude Projects and ChatGPT Projects) and a plain-language install guide — triggers on "build a brand skill for X", "set up the same brand system as Spaceberry/Worwyn for [company]", "onboard a new brand's guidelines", or "turn this style guide into a skill".
---

# Guideline System Builder

## Overview

Turns one company's brand material into three deliverables: a **Skill**
package, a **Project** folder, and a plain-language PDF guide. Neither the
Skill nor the Project belongs to one product — both work in Claude and in
ChatGPT (see Generate for exactly how). Brand guidelines only (colors, type,
logo, icons, illustrations, tone of voice, brand context) — not for non-brand
guidelines like coding standards or policy docs.

## Workflow

```dot
digraph workflow {
    rankdir=LR;
    Intake -> Analysis -> Confirm -> Generate -> "Self-review";
}
```

**Confirm is never skippable.** Even when Analysis turns up almost nothing (a
young or pre-logo brand), still stop and show the user what was found before
writing any file. Going straight from Analysis to Generate is the single most
common failure mode of this skill — resist the pull to "just get it done."

### 1. Intake

Ask one at a time, multiple choice where sensible:
- Company/brand name → propose a slug, confirm with user
- One-line positioning/tagline
- Target audience
- Which output-guides are needed — multiselect from: landing-pages, presentations,
  documents, smm-posts (default: all four)
- Whether a Figma file link exists (optional; use Figma MCP only if available)

Then create `<slug>-branding/intake/` and ask the user to drop every other source
file there: guideline PDFs/docs, logo/font/illustration/icon files, tone-of-voice
material, screenshots. Read that folder — do not ask the user to paste file
contents inline as the primary path.

### 2. Analysis

Read every file in `intake/` (PDF/doc text, images, Figma via MCP if linked).
Extract facts into these fixed categories: colors, typography, logo, icons,
illustrations, voice-tone, brand-context.

**Anti-fabrication rule:** never invent a hex code, font name, logo rule, icon
rule, voice trait, or brand-context fact that wasn't in the source material or
given directly by the user.

**A well-labeled placeholder is still fabrication.** Marking an invented value
"placeholder" or "provisional" does not make it OK to generate it unasked — it
just makes the fabrication easier to spot later. This applies even to values
that feel functionally necessary to keep working, such as:
- A type scale (specific px/weight values for display/headline/body/caption)
- A headline weight or style choice within an existing typeface
- Neutral utility colors (a background white, a secondary-text gray, etc.)

If a category has no usable source and the gap matters for the requested
output-guides, **ask a targeted follow-up question** instead of picking a
reasonable-looking default — e.g. "No type scale was provided. What sizes/weights
should presentations use for a hero line vs. body copy, or should I propose one
for you to approve before I build anything?" Only proceed with a
Claude-proposed value if the user explicitly says to.

If a gap doesn't matter for the output-guides in scope, or the user has no
answer, write that reference file stating plainly that the rules are
undocumented and that nothing should be substituted or guessed to fill the gap
— the same way `spaceberry-brand`'s `references/typography.md` handles its
missing Biro Script Plus font file, and `references/icons.md` handles the
not-yet-built icon system.

### 3. Confirm extracted facts

Before writing any files, show a short per-category summary of what was found
(exact colors, exact type rules, exact voice traits, which output-guides will be
built, and any question raised in Analysis) and get explicit confirmation or
corrections. Do not proceed to Generate without this checkpoint — not even when
the brand is young and the summary is short.

### 4. Generate

Write this fixed shape under `<slug>-branding/` (only the output-guides selected
in Intake; only asset subfolders that have real files):

```
<slug>-branding/
  <slug>-skill/                    (working folder — zipped below, not delivered as a folder)
    SKILL.md
    references/
      colors.md
      typography.md
      logo.md
      icons.md
      illustrations.md
      voice-tone.md
      brand-context.md
      do-dont.md
    output-guides/
      (selected subset of: landing-pages.md, presentations.md, documents.md, smm-posts.md)
    tokens/
      tokens.css
      tokens.json          (only if real hex/scale values exist)
    assets/
      logo/ illustrations/ fonts/   (only real files the user provided — logo here
                                      keeps its best original format, SVG preferred)
  <slug>-project/                  (final deliverable — a plain folder, never zipped)
    instructions.md                 (paste-into-instructions-box text — see below)
    Sources/                        (flat — no subfolders of any kind; everything
                                      the client attaches to a Project goes here)
      colors.md
      typography.md
      logo.md
      icons.md
      illustrations.md
      voice-tone.md
      brand-context.md
      do-dont.md
      logo.png                      (PNG, not SVG — see below)
      (font files sit directly here too, if any — no fonts/ subfolder)
  <slug>-skill.zip                  (final deliverable — zipped copy of <slug>-skill/)
  Setup-Guide.pdf                   (final deliverable)
```

**The final output is exactly three things: `Setup-Guide.pdf`, the
`<slug>-project/` folder, and `<slug>-skill.zip`.** `<slug>-skill/` is working
material only — it exists so Generate and Self-review have real files to
write and inspect, but the client never receives that folder directly, only
its zip:

```bash
cd <slug>-branding/ && zip -rq <slug>-skill.zip <slug>-skill/
```

Re-zip any time `<slug>-skill/` changes — the zip must always match the
folder. **`<slug>-project/` is never zipped** — it stays a plain folder
specifically so the client can open `Sources/` and select every file at once,
rather than extracting an archive first.

**Naming reflects what these things actually are, not which company made
them — never call them "the Claude Skill" or "the ChatGPT Project" anywhere
in generated copy.** They're just "the Skill" and "the Project," and both
work in more than one product:
- **The Skill** (`<slug>-skill.zip`) installs into Claude, where it works
  across every Claude product (Claude Chat, Claude Code, Claude Design,
  Claude Cowork) — or into ChatGPT, where it only runs in Work mode and in
  Codex, not in a regular ChatGPT chat.
- **The Project** (`<slug>-project/`): Claude and ChatGPT each have their own
  "Projects" feature, set up almost identically — create a project, paste
  `instructions.md` into its instructions box, attach everything in
  `Sources/`.

**Logo format differs between the two.** `<slug>-skill/assets/logo/` should
use the best format the client actually provided — SVG preferred, since Skill
uploads in both Claude and ChatGPT handle SVG fine. `<slug>-project/Sources/`
must use a **PNG** instead: ChatGPT's Project file attachment rejects SVG
uploads outright. If the client only provided an SVG, convert one rather than
skipping the logo from `Sources/`.

**Read the SVG's own intrinsic size first** (its `viewBox`, or its `width`/
`height` attributes) and set the Playwright viewport to match that aspect
ratio — never guess a fixed size like 1024×1024. A viewport that doesn't
match the SVG's shape leaves the mark tiny in a sea of blank canvas, or
crops it. Scale up for resolution with `device_scale_factor` instead of an
oversized viewport:

```bash
python3 -c "
import re, pathlib
from playwright.sync_api import sync_playwright

svg_path = pathlib.Path('/absolute/path/to/logo.svg')
svg = svg_path.read_text()
m = re.search(r'viewBox=[\"\']\s*[\d.-]+\s+[\d.-]+\s+([\d.]+)\s+([\d.]+)', svg)
if m:
    w, h = float(m.group(1)), float(m.group(2))
else:
    w = float(re.search(r'width=[\"\']([\d.]+)', svg).group(1))
    h = float(re.search(r'height=[\"\']([\d.]+)', svg).group(1))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': round(w), 'height': round(h)}, device_scale_factor=4)
    pg.goto(svg_path.resolve().as_uri())
    pg.screenshot(path='logo.png', omit_background=True)
    b.close()
"
```

After converting, open the PNG and look at it — confirm the mark fills the
frame with no unexpected whitespace border and the colors match the brand's
hex codes, before treating the conversion as done.

If the rendered PNG looks wrong (cropped, missing effects, wrong colors),
don't ship a broken conversion — ask the user for a real PNG export instead.

Use exactly these file names (`voice-tone.md`, `brand-context.md`, etc.) —
don't rename or merge them, even when a category has little content, so
every generated brand system has the same predictable shape to navigate.

**Real font files go into `<slug>-project/Sources/` too, not just the
Skill's `assets/fonts/`** — flattened directly into `Sources/`, not a
`fonts/` subfolder (see the no-inner-folders rule above). Having the real
file available lets Claude or ChatGPT match the actual typeface more closely
when generating a real document, instead of just describing the type style
in words. Only copy real files provided in `intake/` — never fabricate a
font file.

**`instructions.md` has an 8,000-character hard limit** — this is the exact
text that gets pasted into a Project's instructions box (confirmed as a hard
cap on ChatGPT Projects; treat it as the safe ceiling for Claude Projects too
unless told otherwise). Keep it to the compact operating rules (voice, hard
don'ts, how to use the files in `Sources/`, and the capability caveats
below); push any longer reference material into `Sources/*.md` instead,
which has no such limit. Count characters (`wc -m <slug>-project/instructions.md`)
before finishing Generate — if over 8,000, cut content there, don't try to
just compress formatting.

`instructions.md` must carry these capability caveats whenever a real logo or
real font exists:
- An image-generation tool cannot reproduce the real logo pixel-accurately —
  describe it for background/illustration use, never ask a model to render
  the literal logo from a text prompt.
- An image-generation tool cannot use the real font file inside a
  *generated image* — describe the type style in words there. This is
  separate from a code-execution tool embedding the real font file into an
  actual document (a Word file, a PDF), which does work and is why the font
  file is included.

No `custom-gpt/` folder — this skill only produces the Skill package, the
Project folder, and the PDF guide.

`do-dont.md` must cover both visual rules and voice rules as one checklist.

**`Setup-Guide.pdf`** is Spaceberry's own client-facing collateral, not part
of the generated brand's visual identity — it explains, in plain,
non-technical language, how to set up the Skill (in Claude, in ChatGPT, or
both) and the Project (in Claude, in ChatGPT, or both). Render it with the
bundled template and script in this skill's own `assets/` folder
(`assets/setup-guide-template.html` + `assets/render_setup_guide.py`) — never
hand-build this PDF another way, and never restyle it to the generated
brand's own colors. To render:

```bash
python3 -c "
import json, pathlib
pathlib.Path('setup-guide-data.json').write_text(json.dumps({
    'company_name': '<Company Name>',
    'slug': '<slug>',
    'has_fonts': <true if <slug>-project/Sources/ has real font files, else false>,
}))
"
python3 ~/.claude/skills/guideline-system-builder/assets/render_setup_guide.py \
    setup-guide-data.json <slug>-branding/Setup-Guide.pdf
```

Requires `playwright` (`pip install playwright --break-system-packages -q` if
not already available). Verify before delivering: rasterize the PDF
(`pdftoppm -png -r 100 Setup-Guide.pdf page`) and inspect — plain, simple
language throughout, no overflowing text, the company name and slug filled in
correctly everywhere, and the font-upload sentence present only when
`has_fonts` is true.

### 5. Self-review

Before reporting completion, check across every generated file for:
- Fabricated values (re-check against the Analysis notes and the Confirm
  summary — every color, size, and rule in the output should trace back to
  something the user provided or explicitly approved)
- Contradictions between `<slug>-skill/references/`, `<slug>-skill/output-guides/`,
  and `<slug>-project/Sources/`
- Hard rules stated unambiguously in `do-dont.md`
- `Setup-Guide.pdf` actually rendered (not skipped), reads simply and
  plainly, and has the right company name/slug and font-upload sentence
  baked in
- Real font files (if any) present in both `<slug>-skill/assets/fonts/` and
  flattened directly into `<slug>-project/Sources/` (no `fonts/` subfolder
  there)
- The logo inside `<slug>-project/Sources/` is a **PNG**, not an SVG — even
  when the Skill's own copy is SVG
- `<slug>-project/Sources/` has no inner folders at all — every file sits
  directly inside it
- `instructions.md` is 8,000 characters or fewer (`wc -m`) — trim and
  re-check if not
- `<slug>-skill.zip` exists and was zipped *after* `<slug>-skill/` was
  finalized — re-zip if any file in that folder changed afterward
- `<slug>-project/` itself was **not** zipped

Then report to the user, explicitly, as a checklist:
- What was generated and where
- Which categories are rules-only because no source asset existed
- **The three final deliverables**: `Setup-Guide.pdf`, `<slug>-project/` (a
  folder), and `<slug>-skill.zip` — these are what actually get handed to
  the client; `<slug>-skill/` is a working folder, not a deliverable
- **Manual next steps** (state these even if they seem obvious): if you use
  Claude Code yourself, you can copy `<slug>-skill/` into
  `~/.claude/skills/<slug>/` directly instead of using the zip; otherwise
  just hand the client the three deliverables above — `Setup-Guide.pdf`
  walks them through every install path; git init/commit/push at the user's
  discretion — never automated by this skill

## Common mistakes

| Mistake | Fix |
|---|---|
| Skipping Confirm and generating straight from Analysis, especially when the brand is small/young | Always show the per-category summary and get confirmation first — brand size doesn't change this |
| Inventing a type scale, headline weight, or neutral color and labeling it "placeholder" instead of asking | A labeled placeholder is still a fabricated decision — ask a specific question before generating one |
| Generating all four output-guides regardless of what was requested | Only build the subset confirmed in Intake |
| Calling these "the Claude Skill" / "the ChatGPT Project" anywhere in generated copy | They're just "the Skill" and "the Project" — each works in both products, just with different reach (see Generate) |
| `instructions.md` omits the image-generation/logo/font capability caveat | Always carry it in when a real logo/font exists |
| `instructions.md` exceeds 8,000 characters | Both platforms' Project instructions enforce this cap — trim to core operating rules, move detail into `Sources/*.md` |
| Putting an SVG logo into `<slug>-project/Sources/` | ChatGPT's Project attachment rejects SVG — convert to PNG for `Sources/`; SVG is still fine for the Skill's own `assets/logo/` |
| Nesting files inside `<slug>-project/Sources/` (e.g. a `fonts/` subfolder) | `Sources/` must be completely flat — the client selects everything inside it at once |
| Zipping `<slug>-project/` | Only the Skill gets zipped; the Project always stays a plain folder |
| Forgetting to build `<slug>-skill.zip`, or treating the raw `<slug>-skill/` folder as a deliverable | The three final outputs are `Setup-Guide.pdf` + `<slug>-project/` + `<slug>-skill.zip` |
| Generating a `custom-gpt/` folder | This skill only produces the Skill, the Project, and the PDF guide |
| Copying real font files into the Skill's `assets/fonts/` but forgetting `<slug>-project/Sources/` | Mirror real font files into both |
| Styling `Setup-Guide.pdf` in the generated brand's own colors, or hand-building it without the bundled template/script | It's Spaceberry's own collateral — always render it from `assets/setup-guide-template.html` + `assets/render_setup_guide.py`, fixed accent `#fc4a22` |
| Writing `Setup-Guide.pdf` in technical language (file paths with no explanation, jargon like "repo" or "deploy") | The reader is assumed non-technical — plain, short sentences, the way the bundled template already reads |
| Telling the client to find `~/.claude/skills/` and copy a folder into it | Use claude.ai/Desktop's native Skills upload UI instead (Customize → Skills → Upload) — that's what `<slug>-skill.zip` is for |
| Writing the generated Skill straight into `~/.claude/skills/` | Always write to the new `<slug>-branding/` project folder; installation is a manual step the client does themselves |
| Merging `voice-tone.md`/`brand-context.md` into other files or skipping them for a thin brand | Always create both, even if short — keeps every generated brand system's shape predictable |
| Reporting completion without spelling out manual next steps | Always end with the explicit next-steps checklist, even if some steps seem obvious |
