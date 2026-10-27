# PDF Compilation & Verification

## How it works

`compile_all_pdfs.py` converts every `.md` in `<workspace>/_generated/<Folder>/` to PDF:

1. Markdown → HTML with the `markdown` library, wrapped in `templates/cv_a4.html` + `templates/cv_a4.css` (Inter, one linear column, A4 pages with 16 mm × 18 mm margins). Role lines become a flex row with right-aligned dates; the DOM order stays linear, so parsers read title, company, dates in sequence.
2. Headless Microsoft Edge prints real A4 pages. CSS break rules keep a role title with its first bullets and a heading with its section.
3. `--public` writes `<name>_public.pdf` with every `<span class="private">` removed (the phone). One Markdown source, two PDFs.

Edge is found at the standard install paths or through `EDGE_PATH`. The workspace comes from `CV_WORKSPACE`, then `cvkit.config.json`, then the repo itself.

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

## Fit check

Phase 1, before drafting. It answers "should this application go out, and what will weigh against it?", which formatting and keywords cannot. Each line is `ok`, `risk` or `block`, with the profile line or fact that decides it:

| Line | Compare |
|---|---|
| Location and permit | posting's location, on-site/hybrid/remote and visa wording against `## Languages and mobility` and `## Identity` |
| Seniority band | posting's level (lead, manager, staff, senior, mid) against titles and years in `## Experience` |
| Domain years | years in the technology or domain the title names, counted from Experience and Projects, not from the skills list |
| Language | language the posting requires against the profile's levels |
| Mandatory credential or title | anything the posting treats as required (a named discipline, a degree, a licence) |

Verdict: **strong** (all `ok`, at most one `risk`), **workable** (two or more `risk`, no `block`), **unlikely** (any `block`, or three or more `risk`). On `unlikely` the skill states the reasons and asks whether to continue. The verdict is a prediction about the screen, not a verdict on the candidate, and it never changes what the CV may claim.

## Gates and score (Phase 5, before compiling)

Two pass/fail gates come first. Failing either means fix and re-run; there is no partial credit.

- **Format gate:** single linear column, standard headings, no tables or text in images, header per `01` section G, section order per `01` section A, skills after experience, length within budget. The compiled PDFs must then pass `verify_pdf.py` in Phase 6 (page caps, text layer, order, contact details); a failure there reopens this gate.
- **Truth gate:** every claim and every number is in the profile (`verified metrics` for numbers). One claim the profile does not back, or an assumption made without asking, fails the gate: return to Phase 1 and ask.

Then score the final Markdown 0–100. Evidence is half the score because rejection emails say the experience was not close enough, never that a keyword was missing.

- **Evidence coverage (50):** take the ranked must-haves from Phase 1. Give each a weight (must-have 2, preference 1). A must-have earns its weight when the profile backs it at `production` or `working` depth, or when the user confirmed it in this run, and the CV shows it with evidence (a bullet, project or proof point), not only a keyword. Score = 50 × earned weight ÷ total weight. List the uncovered must-haves by name.
- **Placement (20):** the three leading proof points appear in the summary and in bullets 1–3 of the main role (12); covered must-haves sit in the top half of page 1 (8).
- **Content quality (15):** bullets follow the formula, metrics follow `## Preferences`, the humanization checklist passes, and the cover letter's opening carries a leading proof point.
- **Keyword match (15):** JD terms the profile genuinely supports use the posting's wording; gaps are acknowledged, never stuffed.

Report together: gates (pass/fail each), score with the four-line breakdown, uncovered must-haves, and the fit verdict with its reasons. A high score with an `unlikely` fit is a normal outcome and the report should say so.

The score is a heuristic for catching problems, not a measurement from any real tracking system. It is recorded in `applications_log.md` with the outcome so Phase 9 can check whether it predicts anything; until about ten applications have a decided outcome, do not tune the weights.
