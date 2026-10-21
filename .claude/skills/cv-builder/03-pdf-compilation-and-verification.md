# PDF Compilation & Verification

## How it works

`compile_all_pdfs.py` walks `_generated/` (override with the `CV_OUTPUT_DIR` environment variable) and converts every `.md` file in each subfolder to PDF. It finds Microsoft Edge automatically at the standard install paths, or via `EDGE_PATH`:

1. Markdown → HTML via the `markdown` library, wrapped in a fixed template (Inter font, `.cv-header` flexbox styles).
2. The page is rendered at a deliberately oversized height (`OVERSIZED_PAGE_HEIGHT_MM = 2000`) via headless Microsoft Edge (`--print-to-pdf`), so content can never overflow onto a second page.
3. `pdf_crop.py`'s `crop_pdf_to_content()` then measures the actual content's bottom edge (text blocks + vector drawings like the header's CSS border + any embedded images) via PyMuPDF and sets the PDF's CropBox to exactly that height plus a small margin — eliminating the trailing whitespace that the old per-line height *estimate* used to leave.

This replaced a heuristic that guessed page height by counting/weighting Markdown lines and consistently overestimated. The new approach measures the real rendered output instead of guessing.

**Compile command (always targeted, never a blanket rebuild):**
```
python compile_all_pdfs.py "<FolderName>"
```
Add `--force` to recompile even if the PDF is already newer than the source `.md` (the default skips unchanged files).

## Verification checklist (run every time, before presenting output)

- [ ] `python compile_all_pdfs.py "<FolderName>"` ran with no `Error compiling` or `Warning: could not crop` lines.
- [ ] `python verify_pdf.py "<path>.pdf" --pages 1 --contains "<full name>" --contains "<email>" --contains "<phone>"` passes (values from your candidate profile). This checks: exactly 1 page, a clean extractable text layer (no `�` or `(cid:*)` garbling), and that contact details are present as literal text, not just an icon/image.
- [ ] Read the PDF (the Read tool renders it inline) and visually confirm:
  - No excess blank space at the bottom of the page.
  - No content is cut off (the crop's `max_ratio` safety guard raises rather than silently over-cropping, but a wrong bottom margin could still look tight — check the last line isn't touching the page edge).
  - The header renders as a proper flexbox row (name + contact line), not broken across lines.
  - Fonts and spacing are consistent throughout.
- [ ] If anything fails: edit the Markdown, recompile, re-verify. Don't hand-edit the generated PDF or HTML directly — they're regenerated from Markdown every time.

If a document is a genuine edge case (very long Project Portfolio approaching the oversized bound), `crop_pdf_to_content()` will raise instead of cropping — that error means either trim the content or, if it's a real one-off, raise `OVERSIZED_PAGE_HEIGHT_MM` in `compile_all_pdfs.py` rather than let a bad crop through silently.

## ATS Scoring Engine

Calculate an explicit ATS Score (0–100) once the Markdown is finalized (Phase 5, before compiling):

- **Formatting (30 pts):** Single column, standard fonts, clean structure.
- **Structure (20 pts):** Standard headers in the order defined in `01-structure-and-style.md` section A; Skills placed after Experience.
- **Content Quality (30 pts):** Bullets follow the Action+What+How/Why+Result formula with real metrics; truthfulness verified against your candidate profile. **-100 points for any hallucinated skill or claim, or for failing to ask before assuming one** — this is an automatic fail, go back to Phase 1 and ask the user rather than adjust the score downward and continue.
- **Keyword Optimization (20 pts):** Real JD keywords the profile genuinely supports are present; gaps are acknowledged, never stuffed.

Report the score and a short breakdown alongside the final output.
