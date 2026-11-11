# KOSEN PowerPoint exports

`week10.pptx … week15.pptx` were regenerated on 12 Nov 2026 from the current KOSEN Markdown lessons and use the visual system of `KOSEN69 - PBL/slides/pbl4/week03-sprint1/PBL4_W03_Sprint1.pptx`. Their current class hand-in pages reflect the shared 60-point practical plus one assigned 40-point written version.

`week01.pptx … week09.pptx` and `week16.pptx … week19.pptx` remain older exports. Their task counts, timing, grading and submission rules may contradict the current course. **Do not use those older exports as current KOSEN assessment instructions.** Use the updated [`../weekNN.md`](../) Markdown decks and matching worksheets/exam guides as the source of truth. The Markdown decks are served on `learn.zcr.ai`; the platform does not serve PPTX.

## Brand
- **KMITL main:** orange `#E35205` (Pantone 166c) — official CI 2022
- **KOSEN:** blue `#017BC4` (from the KOSEN-KMITL logo)
- **Neutrals (KMITL secondary):** white `#FFFFFF`, grey `#666666`, black `#000000`
- Logo: `assets/logo-small.png` (KOSEN-KMITL official, downscaled for small file size)
- Weeks 10–15: light 16:9 PBL layout, blue kicker, navy title, orange emphasis, logo on every slide, editable cards and tables.

## Regenerate
```bash
cd slides/pptx
npm install pptxgenjs react-icons react react-dom sharp   # once
node build_all.js                                         # older layout, all 19 .pptx
node build_kosen_pbl.js                                   # current PBL layout, Weeks 10–15 only
```
Run `build_kosen_pbl.js` last for Weeks 10–15. Running `build_all.js` alone would replace those six decks with the older layout. The PBL export keeps the current Markdown section headings, diagrams and speaker notes, and splits long hand-in text across continuation slides.
The decks open and are fully editable in PowerPoint. Edit content in the Marp
`.md` files and re-run, or tweak the generated `.pptx` directly for one-off slides.

## Diagrams
A slide line `![alt](img/name.svg)` is **embedded as a picture**: the SVG is rasterised with `sharp` to a 1600 px
palette PNG (about 20-100 KB each) and centred at the largest size that fits between the title and the footer. The
file is looked up in the week's lab directory (`labs/weekNN-<slug>/img/`), the same place the web renderer uses; only
`img/<plain name>.svg|png|jpg` is accepted. The alt text becomes the picture's alt text. The older exporter falls back to a text pointer if a diagram cannot render; the Week 10–15 exporter stops the build so a missing diagram cannot silently ship.
- The diagrams are dense web graphics, so on a 16:9 slide their labels are small; the 1600 px PNG stays sharp when you zoom in PowerPoint.
- A picture takes the whole slide: any bullets that follow it move to a "(cont.)" slide.
- Interactive simulations (```` ```sim ```` fences) cannot be embedded and still show a "Try it live: /sim/... (web only)" line.
- Rasterising uses the fonts installed on the machine that runs the build, so rebuild on the same machine for identical pictures.
