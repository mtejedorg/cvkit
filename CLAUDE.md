# CV Builder — AI-Assisted CV/Cover Letter/Portfolio Generator

A reusable Claude Code skill for tailoring CVs, cover letters, and project portfolios to specific job postings. Designed to be forked and customized for any candidate's profile and experience.

## Entry point

For any CV/cover-letter/job-application task, follow **[.claude/skills/cv-builder/SKILL.md](.claude/skills/cv-builder/SKILL.md)**. It covers the full workflow:
- JD analysis (evaluate fit, clarify missing skills)
- Drafting (CV + cover letter + project portfolio in Markdown)
- Humanization pass (remove AI-sounding language, preserve facts)
- Reviewer critique (fresh-context subagent feedback)
- ATS scoring (0–100 rubric)
- PDF compilation & verification (crop whitespace, verify text layer)

## Setup for your own use

1. **Fork or clone this repo to your local machine.**

2. **Create your candidate profile** in `_private/`:

   ```bash
   mkdir -p _private
   ```

   Create a file `_private/candidate_profile_<your-name>.md` with the following structure. This is the **single source of truth** that the skill reads from — every CV, cover letter, and portfolio it generates draws from here, so keep it accurate and up-to-date.

   **Required sections:**

   - **Personal Info** — Full name, email, phone, location (city, country), LinkedIn URL, GitHub URL
   - **Employment Status** — Employed/Freelance/Seeking/Open to Opportunities, current role (if applicable)
   - **Professional Headline** — One sentence describing your primary positioning (e.g., "Senior Game Engineer specializing in multiplayer architecture")
   - **Education** — Degrees with institution, graduation year, major. Example:
     ```
     - B.S. in Computer Science, University of Example, 2015
     - Certificate in Advanced Game Development, XYZ Academy, 2018
     ```
   - **Professional Experience** — Reverse-chronological list of roles. For each, include:
     - Job title, company, location, employment dates (month/year)
     - Role description (2–3 sentences: what you did, team size, reporting structure)
     - 3–5 bullet points per role with: action verb + responsibility + result/metric. Examples:
       - "Led multiplayer networking stack for 50k+ concurrent players; reduced latency 40% via server-side prediction"
       - "Implemented automated CI/CD pipeline; reduced deployment time from 2 hours to 15 minutes"
       - "Mentored 3 junior engineers on architecture patterns; all promoted within 18 months"
     - Keep metrics (percentages, counts, time reductions) if you have them; the skill cannot invent them
   - **Technical Skills** — Organized by category (Languages, Frameworks, Tools, Platforms, etc.). Examples:
     ```
     **Languages:** C++, C#, Python, TypeScript, Rust
     **Game Engines:** Unity, Unreal Engine 4, Godot
     **Web Frameworks:** React, Vue.js, Node.js, Django
     **Databases:** PostgreSQL, MongoDB, Redis
     **Tools:** Git, Docker, Kubernetes, Jira, Confluence
     ```
   - **Certifications & Awards** (if any) — Name, issuer, date
   - **Publications & Open Source** (if any) — Title, link, date
   - **Behavioral Profile** — Freeform section for personality and work style:
     - Personality traits (e.g., analytical, collaborative, detail-oriented)
     - What motivates you (learning, mentorship, building at scale, technical depth)
     - Work style preferences (remote/onsite, team size, pace)
     - Growth areas or constraints (e.g., "not ready to relocate", "focused on game dev, avoiding finance")
     - Ideal environment description
   - **Target Sectors & Roles** — Industries/companies you want (e.g., "game development, AR/VR", "fintech for environmental impact")
   - **Deal-breakers** — Hard constraints that would make you decline a role (e.g., "no relocation", "no mandatory onsite 5 days/week", "no blockchain/crypto")
   - **Confirmed gaps** (maintained by the skill, optional to start) — Skills or experience you confirmed you do *not* have, each with the date and the posting that prompted it. The skill adds entries during Phase 7 and never claims anything listed here.
   - **STAR Examples** — Situation-Task-Action-Result examples for behavioral interviews (e.g., "Tell me about a time you resolved a conflict with a colleague"):
     ```
     **Conflict Resolution**
     - Situation: Team disagreed on technical approach for critical feature
     - Task: Reach consensus quickly without alienating either side
     - Action: Organized technical deep-dive; documented pros/cons of each approach; facilitated vote
     - Result: Team aligned, morale intact, shipped on schedule
     ```
     Include 5–10 STAR stories covering: conflict, technical challenge, leadership, failure/recovery, collaboration, innovation

   **Do NOT edit the candidate profile by hand during a CV-tailoring session.** Let the skill update it through the "State Update" phase (Phase 7 in `SKILL.md`). It records every answer you give to its clarification questions there, in your own words ("no" answers go under Confirmed gaps), and shows you exactly what it added. This keeps the profile in sync and prevents accidental drift.

3. **Organize your workspace**:
   - `_private/` — holds your candidate profile (gitignored, never committed)
   - `_generated/` — holds compiled outputs: CVs, cover letters, portfolios by company/role (gitignored, never committed)
   - Both folders are **excluded from git** so your personal data never leaks to version control

4. **Adapt the skill for your background**:
   - Review `.claude/skills/cv-builder/01-structure-and-style.md` for the CV rules: section order, bullet formula, writing style, anti-clichés, regional photo rules
   - Customize these rules for your background and target markets
   - Update `.claude/skills/cv-builder/02-humanization-checklist.md` if you have industry-specific clichés to ban

5. **Start tailoring**:
   - Open Claude Code in this folder: `claude` (or use the Claude app's Code tab)
   - Run the cv-builder skill against a job posting
   - The skill will ask about any missing skills before drafting (the "ask before lying" rule)
   - Generated files land in `_generated/<CompanyName>/`

## Repository structure

```
cv-builder-public/
├── .claude/skills/cv-builder/          # Public: skill rules & workflow
├── compile_all_pdfs.py                 # Public: toolchain
├── pdf_crop.py
├── verify_pdf.py
├── CLAUDE.md                           # Public: setup & documentation
├── examples/Northwind_Labs/            # Public: fictional sample CV (Markdown + verified PDF)
├── site/                               # Public: static site explaining how the skill works
├── .gitignore                          # Blocks _private/ and _generated/
├── _private/                           # Private (gitignored): your profile
│   └── candidate_profile_<your-name>.md  # Your profile (never committed)
└── _generated/                         # Generated (gitignored): output files
    ├── Acme_Corp/                      # One folder per application (never committed)
    ├── Example_Platform_Lead/
    └── ...etc...
```

## Key files

- **`_private/candidate_profile_<your-name>.md`** (your own) — factual source of truth for the skill. Lists your education, experience, skills, positioning, and STAR examples. Never committed to git.
- **`.claude/skills/cv-builder/`** — the skill (5 files):
  - `SKILL.md` — entry point and workflow definition
  - `01-structure-and-style.md` — CV section order, bullet formula, writing rules
  - `02-humanization-checklist.md` — how to remove AI-sounding language while keeping facts
  - `03-pdf-compilation-and-verification.md` — compile, crop, verify (ATS scoring rubric)
  - `04-drafter-reviewer-workflow.md` — how to use a subagent for critique
- **`compile_all_pdfs.py`**, **`pdf_crop.py`**, **`verify_pdf.py`** — the toolchain:
  - Renders Markdown → HTML → Edge PDF, oversized to avoid overflow
  - Crops PDFs to actual content height (removes trailing whitespace)
  - Verifies page count, text layer cleanliness, contact details present
  - No poppler dependency — uses PyMuPDF (`fitz`) directly

## Compile & verify

Generated files are output to `_generated/` (they're gitignored, so they won't leak into version control):

```bash
# Compile just one company's folder (targeted, fast)
python compile_all_pdfs.py "<FolderName>"

# Verify the PDF (page count, text layer, required contact details)
python verify_pdf.py "_generated/<FolderName>/CV_*.pdf" --contains "Your Name" --contains "your.email@example.com"
```

Note: The skill automatically compiles to `_generated/` when you run it against a job posting. Manual compilation is only needed if you edit the Markdown files directly.

## Design philosophy

- **No hallucination** — if a job requires a skill not in your profile, the skill halts and asks; it never invents or assumes.
- **Humanized, not detector-evasion** — the humanization pass rewrites for natural tone while preserving every fact exactly. No translation chains, no external APIs for obfuscation.
- **Fresh-context review** — drafts are critiqued by a subagent spawned with clean context (no bias from the drafter's phrasing), catching missed keywords and weak framing.
- **Verified PDFs** — every output is checked for ATS parseability (clean text layer, contact details present, page count correct) and visually inspected.
- **The profile learns** — every answer you give to a clarification question is written back to your profile in your own words (a "no" is kept as a confirmed gap), so the next application starts from better facts and the skill never contradicts you.

## Git & privacy

- The skill rules and toolchain are public and reusable; commit them freely.
- **Your candidate profile and generated applications are private** — add them to `.gitignore` (already included) and never push to a public repo.
- `.gitignore` prevents accidental commits of sensitive files. If you fork this and set up your own profile, you control whether it's public or private.

## Dependencies

- Python 3.10+
- `PyMuPDF` (fitz): `pip install PyMuPDF`
- `markdown`: `pip install markdown`
- Microsoft Edge (for headless PDF rendering) or substitute your preferred headless browser in `compile_all_pdfs.py`

## References

- Inspired by [ai-job-search](https://github.com/MadsLorentzen/ai-job-search), an open-source Claude Code job-application framework by Mads Lorentzen. This skill adapts its PDF/ATS verification approach and the drafter/reviewer pattern.
- The humanization pass replaces translation-chain approaches with direct rewriting, prioritizing factual accuracy over AI-detection evasion.
