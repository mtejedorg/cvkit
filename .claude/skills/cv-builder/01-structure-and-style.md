# Structure & Style Rules

The default structure and style rules. Adapt them to your background and target markets (see CLAUDE.md, "Adapt the skill for your background").

## A. Section Hierarchy Order (Default)
The CV sections MUST be ordered in the following sequence:
1. **Header** (HTML Flexbox `<div class="cv-header">`)
2. **Professional Summary**
3. **Professional Experience** (Commercial Work Experience)
4. **Additional Experience & Projects** (Personal & Academic Projects)
5. **Core Competencies & Technical Skills** (ALWAYS place Skills AFTER Experience)
6. **Education**
7. **Languages**

## B. Bullet-Point Formula & Job-Specific Prioritization
- All experience bullet points must follow: `[Action Verb] + [What you did] + [How/Why you did it] + [Quantifiable Result]`.
- **Bullet Order Prioritization:** For a given job description, order the bullet points under main roles (e.g., your current employer) so that the **primary required skills of the target job** appear in bullets 1–3. Place secondary accomplishments (R&D, AI, prototyping) further down (bullets 4–6) unless the job is specifically an R&D/AI role.

## C. "ASK BEFORE LYING" (Strict Truthfulness & No Invention Rule)
- **NEVER invent, hallucinate, or claim skills, frameworks, APIs, certifications, or job titles not explicitly present in `candidate_profile_<your-name>.md`.** (e.g., never claim Kubernetes experience, a PMP certification, or a "Staff Engineer" title if the profile doesn't list it).
- **If the JD requires a skill not in the profile, YOU MUST ASK THE USER about it before assuming they have it. NEVER LIE.**
- **Save what you learn.** The user's answer, including a "no", is written back to the profile in Phase 7 (a "no" under `Confirmed gaps`), so it is never contradicted or re-asked. See `SKILL.md`.
- Ground all tailoring strictly in the candidate's real experience as documented in the profile: its skills, tools, domains, and projects. Nothing outside it.

## D. Flagship Core Skill Prominence Rule
- The candidate's primary flagship skill (the one named in the profile's Professional Headline) MUST ALWAYS be explicitly featured in the opening sentence of the Professional Summary and Cover Letter introduction, even when the target job centers on a different stack or platform.

## E. Regional Photo Rules
- **Omit Photo:** US, UK, Canada, Australia (anti-discrimination compliance).
- **Include Photo:** DACH region (Germany, Austria, Switzerland), Spain, France, Middle East, Asia (unless specifically instructed otherwise).

## F. Design & Template Selection
- **Tech/Engineering:** Minimalist, clean, single-column design. High ATS parsing priority.
- **Creative/Design:** Creative Hybrid. Can include subtle visual flair, but text must flow in a single column for parsers.
- **Corporate/Finance:** Professional Traditional. Highly conservative layout.

## G. Structural Layout Rule (The Header & PDF Compilation)
- To avoid CSS rendering glitches when building PDFs, the CV header MUST NOT be written in pure Markdown. Instead, it must be constructed using a raw HTML Flexbox wrapper (`<div class="cv-header">`).
- **Targeted Incremental Compilation:** To avoid long build times, NEVER compile all CVs for a single update. Always run targeted compilation for the specific folder being edited: `python compile_all_pdfs.py "<FolderName>"` (e.g., `python compile_all_pdfs.py "Acme_Corp"`).

```html
<div class="cv-header">
  <div class="cv-header-text">
    <h1>[Name]</h1>
    <p>[Location] | [Email] | [Phone] | [LinkedIn] | [GitHub]</p>
  </div>
  <!-- If a photo is required based on Regional Rules, include it here: -->
  <img src="file:///path/to/photo.jpg" class="profile-photo" />
</div>
```

## H. Writing Style & Anti-Redundancy Rules
- **Tone:** Professional, active, concise, highly humanized.
- **Anti-Clichés:** Absolutely ban phrases like "proven track record", "extensive background", "delve", "testament", "orchestrated", "aligns perfectly". (See `02-humanization-checklist.md` for the extended list and the dedicated humanization pass this now runs through.)
- **Anti-Redundancy:** Never restate the same tool or category twice in one phrase (e.g., "Python and Python-based scripting", "React and front-end frameworks"). Name the specific tool once and lead with it.
- **Verbs:** Use active participles (e.g., "Bringing," "Specialized in") in summaries to avoid awkward 1st/3rd person conjugation.
- **Markdown Formatting Rule (CRITICAL for PDF Generator):** You MUST place a completely blank line immediately before the start of any bulleted list. If you do not include a blank line before the first `*` or `-`, the PDF compilation script will fail to parse the list and will render it as a single broken paragraph.

## I. Project Portfolio Generation Rules
When drafting the application materials, always generate a customized Project Portfolio alongside the CV and Cover Letter.
- **Structure:** Group projects under large headers by **Company and Role** (e.g., `# Senior Backend Engineer (Example Corp)`).
- **Ordering:** Order projects in strict **Reverse-Chronological** order within and across company sections. Include development years for each project.
- **Tone:** Humanized, first-person active language (e.g., "I built", "I designed", "I hooked up") instead of robotic/ATS language. Keep the technologies list concise without long unstructured strings.
- **NEVER Include "Tailored for..." Meta-Labels:** NEVER write phrases like "Tailored for [Company]", "Customized for [Role]", or any similar meta-commentary in the CV, Cover Letter, Project Portfolio, or any other generated document. All documents must appear natural, direct, and self-contained.
