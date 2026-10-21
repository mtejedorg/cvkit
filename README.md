# cv-builder

A Claude Code skill that tailors a CV, cover letter and project portfolio to a job posting, and is not allowed to lie.

- **One source of truth.** A private profile file holds every fact. Anything the posting wants that the profile does not back becomes a question for you, never an assumption.
- **Lead with proof.** Each run names a positioning profile and three proof points and puts them where a reader looks first.
- **A4 PDFs people like to read.** Real pages, a two-page cap for the CV, one page for the letter, verified text layer for applicant tracking systems.
- **Private by construction.** Your profile and applications live in a workspace outside the public repo; a privacy check blocks commits that contain your contact details; `--public` builds drop the phone number for anything that goes online.

Setup and the full workflow are in [CLAUDE.md](CLAUDE.md). The skill itself is [`.claude/skills/cv-builder/`](.claude/skills/cv-builder/). The explainer site is in [`site/`](site/).

```bash
pip install PyMuPDF markdown pytest
python -m pytest -q                       # toolchain tests (PDF tests need Microsoft Edge)
python compile_all_pdfs.py "<Folder>"     # Markdown -> A4 PDF for one application
python verify_pdf.py "<pdf>" --max-pages 2 --contains "<name>" --order "Professional Summary" --order "Education"
python privacy_check.py                   # no personal data in tracked files
```

Adapted from the drafter/reviewer and PDF-verification ideas in [ai-job-search](https://github.com/MadsLorentzen/ai-job-search) by Mads Lorentzen. MIT licensed.
