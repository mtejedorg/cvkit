# PDF Compilation & Verification

## How it works

`compile_all_pdfs.py` converts every `.md` in `<workspace>/_generated/<Folder>/` to PDF:

1. Markdown → HTML with the `markdown` library, wrapped in `templates/cv_a4.html` + `templates/cv_a4.css` (Inter, one linear column, A4 pages with 16 mm × 18 mm margins). Role lines become a flex row with right-aligned dates; the DOM order stays linear, so parsers read title, company, dates in sequence.
2. Headless Microsoft Edge prints real A4 pages. CSS break rules keep a role title with its first bullets and a heading with its section.
3. `--public` writes `<name>_public.pdf` with every `<span class="private">` removed (the phone). One Markdown source, two PDFs.

Edge is found at the standard install paths or through `EDGE_PATH`. The workspace comes from `CV_WORKSPACE`, then `cv-builder.config.json`, then the repo itself.

```bash
python compile_all_pdfs.py "<Folder>"            # this folder, all .md files
python compile_all_pdfs.py "<Folder>" --public   # phone-less variants next to the normal PDFs
python compile_all_pdfs.py                       # every folder, only stale PDFs
```

Never run a blanket rebuild to fix one application; target the folder.

## Verification (run every time, before presenting output)

```bash
# CV
python verify_pdf.py "<pdf>" --max-pages 2 --contains "<full name>" --contains "<email>" \
  --order "Professional Summary" --order "Professional Experience" \
  --order "Core Competencies" --order "Education"

# Cover letter
python verify_pdf.py "<pdf>" --pages 1 --contains "<full name>" --contains "<email>"

# Project portfolio
python verify_pdf.py "<pdf>" --max-pages 3 --contains "<full name>"

# Public variant (phone must be absent)
python verify_pdf.py "<pdf>_public.pdf" --max-pages 2 --forbids "<phone digits>"
```

The verifier also fails on replacement characters or `(cid:*)` markers in the text layer (fonts that did not map to text).

Visual checklist (read the PDF, the Read tool renders it):
- [ ] The header is one row: name and contact line, photo on the right if present.
- [ ] No role title sits alone at the bottom of a page.
- [ ] Page 2 of a CV is at least a third full; if it holds only Languages and a line of Education, trim page 1 instead.
- [ ] Dates are right-aligned on role lines; skills rows are one line each where possible.
- [ ] Nothing is cut off; no image placeholder for a missing photo (the compiler warns and omits it).

If anything fails: edit the Markdown, recompile, re-verify. Never edit the PDF or the intermediate HTML.

## ATS scoring (Phase 5, before compiling)

Score the final Markdown 0–100:

- **Formatting (30):** single linear column, standard headings, no tables or text in images, header per `01` section G.
- **Structure (20):** section order from `01` section A; skills after experience; length within budget.
- **Content quality (30):** bullets follow the formula; proof points in the summary and bullets 1–3; every number traceable to `verified metrics`. **−100 for any claim not in the profile, or for assuming one without asking.** That is an automatic fail: return to Phase 1 and ask.
- **Keyword match (20):** JD terms the profile genuinely supports are present in the wording the JD uses; gaps are acknowledged, never stuffed.

Report the score with a short breakdown next to the final output. It is a heuristic for catching problems, not a measurement from any real tracking system.
