# cvkit — career tooling skills

Three Claude Code skills with one rule: nothing is claimed that its source does not back. cv-builder and linkedin share one private fact file about you; portfolio reads the project repo's own documents. Fork it, write your profile, point the skills at a posting, a repo or your LinkedIn page.

## Skills and entry points

| Task | Follow |
|---|---|
| Any CV, cover-letter or job-application task | **[.claude/skills/cv-builder/SKILL.md](.claude/skills/cv-builder/SKILL.md)**: workspace resolution, JD analysis with a question for every gap, fit check and saved `JD.md`, positioning profile and proof points, drafting within a length budget, humanization, fresh-context review, format and truth gates with an evidence score, A4 PDFs with phone-less public variants, write-back to the profile and the applications log, outcomes. |
| A portfolio site, a project page for a repo, GitHub Pages, a project card or preview | **[.claude/skills/portfolio/SKILL.md](.claude/skills/portfolio/SKILL.md)**: hub and project roles, the `portfolio.json` contract, captures, Pages workflow, discovery through the git remote and `gh`. |
| Anything LinkedIn: headline, About, experience, skills, posts, recruiter replies, settings | **[.claude/skills/linkedin/SKILL.md](.claude/skills/linkedin/SKILL.md)**: audit against the profile, paste-ready sections within limits, posts and messages, a record of what is live. |

## Setup

1. **Fork or clone this repo.** Install the dependencies:

   ```bash
   pip install PyMuPDF markdown pytest Pillow
   ```

   PDF rendering uses Microsoft Edge (headless). The script finds it at the standard Windows, macOS and Linux paths, or set `EDGE_PATH`.

2. **Choose where your private data lives.** Two options:
   - *Simple:* keep it inside this folder. `_private/` and `_generated/` are gitignored.
   - *Recommended:* a separate private folder or private repo (e.g. `../my-career-data/`), so the public skill repo never holds a single personal file. Copy `cvkit.config.example.json` to `cvkit.config.json` (gitignored) and set `workspace` to that folder, or export `CV_WORKSPACE`. The scripts and the skill resolve the workspace in that order: `CV_WORKSPACE`, config file, this repo.

3. **Write your candidate profile.** Copy `templates/candidate_profile_template.md` to `<workspace>/_private/candidate_profile_<your-name>.md` and fill it in. The headings are a contract with the skill; [05-profile-schema.md](.claude/skills/cv-builder/05-profile-schema.md) explains each section. The parts that matter most:
   - **Positioning profiles**: one per kind of role you apply to, each with a 50–70 word summary and three leading proof points.
   - **Proof points**: your strongest verifiable claims, ranked, with the evidence behind each.
   - **Skills with a depth level** (`production`, `working`, `academic`, `evaluated`, `supervised`). The depth decides how the skill may word a claim, and anything below `working` counts as a gap the skill must ask about.
   - **Verified metrics** inside each role, with how and when each number was confirmed. Numbers anywhere else are not used.
   - **Not claimable**: things you have confirmed you do not have. Never claimed, never asked again.
   - **Preferences**: how many numbers you like in a CV, output language, photo rules.

   **Do not edit the profile by hand during a tailoring session.** The skill writes every answer you give back into it (Phase 7) and shows you the exact lines, so the file stays consistent.

4. **Privacy check.** Copy `templates/privacy_patterns.example.txt` to `<workspace>/_private/privacy_patterns.txt` and list your email, phone spellings and private file names. Then enable the pre-commit hook once per clone:

   ```bash
   git config core.hooksPath .githooks
   ```

   `python privacy_check.py` fails if any tracked file contains one of your patterns. Run it with `--paths` against any site folder before publishing it.

5. **Run the tests** to confirm the toolchain works on your machine:

   ```bash
   python -m pytest -q
   ```

6. **Tailor.** Open Claude Code in this folder and say: "Tailor my CV for `<posting URL or pasted text>`". Answer its questions about gaps. Results land in `<workspace>/_generated/<Company_Role>/`.

## Repository structure

```
cvkit/
├── .claude/skills/cv-builder/   # SKILL.md + 01…06 rule files + evals/
├── .claude/skills/portfolio/    # SKILL.md + references/ + assets/ + scripts/portfolio_tool.py + evals/
├── .claude/skills/linkedin/     # SKILL.md + references/ + assets/ + evals/
├── cvtool/                      # toolchain: workspace, compile, verify, privacy
├── templates/                   # A4 HTML/CSS template, profile template, privacy patterns example
├── tests/                       # pytest suite with fictional fixtures
├── examples/Northwind_Labs/     # fictional sample CV (Markdown + compiled PDF)
├── site/                        # static explainer site
├── docs/superpowers/specs/      # design notes
├── compile_all_pdfs.py          # CLI: Markdown -> A4 PDF (+ --public)
├── verify_pdf.py                # CLI: page caps, text layer, order, forbidden text
├── privacy_check.py             # CLI: no personal data in tracked files
├── compile_pdfs.ps1 / .bat      # interactive compile launcher (Windows)
├── cvkit.config.example.json
└── .githooks/pre-commit

<workspace>/                     # yours, private, never in this repo
├── _private/candidate_profile_<name>.md
├── _private/privacy_patterns.txt
├── _private/applications_log.md
└── _generated/<Company_Role>/   # one folder per application
```

## Compile and verify

```bash
python compile_all_pdfs.py "<Folder>"                 # all .md in <workspace>/_generated/<Folder>/
python compile_all_pdfs.py "<Folder>" --public        # writes only the *_public.pdf files, without the phone number
python verify_pdf.py "<pdf>" --max-pages 2 --contains "<name>" --contains "<email>" \
  --order "Professional Summary" --order "Professional Experience" --order "Core Competencies" --order "Education"
python verify_pdf.py "<pdf>_public.pdf" --forbids "<phone digits>"
```

The CV header must follow the HTML convention in [01-structure-and-style.md](.claude/skills/cv-builder/01-structure-and-style.md) (section G): the phone number sits inside `<span class="private">`, which is what `--public` removes.

## Design philosophy

- **Never lie.** A posting item the profile does not support at `production` or `working` depth is a question, however small. A "no" is recorded so it is never claimed later.
- **Lead with the strongest proof.** The summary, the first bullets and the cover letter's opening carry the three proof points chosen for this posting.
- **Adapt to the offer.** A named positioning profile per role family, content ordered by what the posting values, a length budget so the result reads well on paper.
- **Humanized, not detector-evasion.** The humanization pass rewrites for natural tone while preserving every fact. No translation chains.
- **Fresh-context review.** A subagent with no memory of the drafting critiques the result.
- **Verified PDFs.** Page caps, clean text layer, section order and contact details are checked by script, then by eye.
- **Private by construction.** Workspace outside the repo, privacy check on every commit, public builds without the phone.

## Reviewer personas

Every skill puts its output in front of a panel of readers before you see it: a recruiter screener, the tracking-system parser and a generic hiring manager ship in `templates/personas/`. The readers who matter most, the people who would hire you for the roles you target, are yours to define: say "create a persona for <role or company type>" and the skill drafts one into `<workspace>/_private/personas/` from your positioning profiles and past postings. A CV panel uses only the personas relevant to that posting; the portfolio and LinkedIn panels use all of them, because those pages face everyone. Rules in [06-persona-review.md](.claude/skills/cv-builder/06-persona-review.md).

## Testing the skills

Each skill has test cases under `evals/<case>/` (a prompt, an expected outcome, graders, input files). With Claude Code 2.1.269 or later, from a skill folder: `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold`. These are real model runs and are billed.

## Git and privacy

- Commit the skill, toolchain, templates, tests, examples and site freely. Never commit anything from your workspace.
- `privacy_check.py` runs as the pre-commit hook. Keep your patterns file current.
- Before every push or publish run `python privacy_check.py --history`: it scans every commit reachable from `HEAD` (diffs, messages, author and committer) and prints the identities it saw, which should all be your noreply address. `--all-refs` also covers other branches and tags.
- Fictional examples only (the repo's sample candidate is Alex Rivera at fictional companies). Never use real application folders as examples.

## Dependencies

- Python 3.10+, `PyMuPDF`, `markdown`, `pytest`
- Microsoft Edge for headless PDF rendering (or set `EDGE_PATH`)

## References

- [ai-job-search](https://github.com/MadsLorentzen/ai-job-search) by Mads Lorentzen: the drafter/reviewer pattern and the PDF/ATS verification idea this skill adapts.
