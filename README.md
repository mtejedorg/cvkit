# cvkit

Career tooling as Claude Code skills, built around one private fact file and one rule: nothing gets claimed that the file does not back.

| Skill | What it does |
|---|---|
| [`cv-builder`](.claude/skills/cv-builder/) | Tailors a CV, cover letter and project portfolio to a posting: fit check, every-gap questions, proof points first, humanization, fresh-context review, gates and score, verified A4 PDFs, write-back to the profile and an applications log with outcomes. |
| [`portfolio`](.claude/skills/portfolio/) | Builds a portfolio hub on GitHub Pages and the project sites it links to, from a small manifest contract. Owner and URLs come from the git remote; nothing is hardcoded. |
| [`linkedin`](.claude/skills/linkedin/) | Audits and rewrites LinkedIn sections within their limits, drafts posts and messages, and recommends settings, all from the same profile. |

Shared by all three: the candidate profile schema with skill depth levels, the humanization checklist, a privacy check that blocks commits containing your contact details, and `--public` builds that drop the phone number from anything that goes online.

Setup and the workflows are in [CLAUDE.md](CLAUDE.md). The explainer site for cv-builder is in [`site/`](site/).

```bash
pip install PyMuPDF markdown pytest Pillow
python -m pytest -q                       # toolchain tests (PDF tests need Microsoft Edge)
python compile_all_pdfs.py "<Folder>"     # Markdown -> A4 PDF for one application
python verify_pdf.py "<pdf>" --max-pages 2 --contains "<name>" --order "Professional Summary" --order "Education"
python privacy_check.py                   # no personal data in tracked files
python .claude/skills/portfolio/scripts/portfolio_tool.py --help
```

Each skill ships test cases under `evals/` in the layout `claude plugin eval` reads.

Adapted from the drafter/reviewer and PDF-verification ideas in [ai-job-search](https://github.com/MadsLorentzen/ai-job-search) by Mads Lorentzen. MIT licensed.
