# Structure & Style Rules

Defaults for every generated document. Adapt them to your market in your fork; the profile's `## Preferences` section overrides individual rules.

## A. Section order (CV)

1. Header (HTML block, see G)
2. Professional Summary
3. Professional Experience
4. Additional Experience & Projects
5. Core Competencies & Technical Skills (always after Experience)
6. Education
7. Languages

Periods without an employer are never left as an unexplained gap, but where they go is a parsing decision the profile makes (`## Preferences` or a `cv placement:` line on the entry): a short recent period of independent work usually belongs under **Additional Experience & Projects** with its dates, so that a parser still reads the longest employer as the latest experience. For the same reason, two successive titles inside one continuous employment stay on **one role line** with both titles and the full date range; the context line names the phases. Splitting them into two entries makes many parsers count only the last one.

## B. Length budget

| Document | Limit | Inside it |
|---|---|---|
| CV | 2 A4 pages (`--max-pages 2`) | Summary 50–70 words. Main role 5–7 bullets, each ≤ 30 words. Older roles 1–3 bullets. Projects 2–3 bullets each. Skills ≤ 7 rows. Education ≤ 2 lines per degree. |
| Cover letter | 1 page, ≤ 320 words | Subject line, greeting, 3 short paragraphs, sign-off with contact line. |
| Project portfolio | 3 A4 pages | 2–4 projects per role, 2–3 bullets each, years on every project. |

When content exceeds the budget, cut the weakest bullet, not the margins.

## C. "ASK BEFORE LYING"

- Never invent or upgrade a skill, tool, title, certification, date or number. The profile's `## Skills` depth levels (`05-profile-schema.md`) decide the wording.
- A JD item not backed at `production` or `working` depth is a question for the user, however minor. The user's answer, including "no", is written back in Phase 7.
- Numbers come only from `verified metrics` lines. Old generated documents are not a source.

## D. Proof points and positioning

- Phase 1 names a `### <Family>` positioning profile and three proof points. The summary's first sentence uses the profile's `flagship skill` and its first proof point. Bullets 1–3 of the main role carry the three proof points (or the facts behind them). The cover letter's first paragraph states the single strongest one.
- Order remaining bullets by what the JD asks for first. Secondary work (R&D, side interests) goes last unless the posting is about it.
- Metrics follow `## Preferences` → `metrics:`. Default: at most two percentages and two counts per CV; everything else in plain words. A number used in the cover letter is not repeated in the CV unless it is the leading proof point.

## E. Regional photo rules

- Omit: US, UK, Canada, Australia, Finland (and any posting that says so).
- Include: DACH, Spain, France, Middle East, most of Asia.
- The profile's `photo:` line overrides either default.

## F. Bullet formula

`[Action verb] + [what you did] + [how or why] + [result]`. The result is a number only when `verified metrics` has one and the budget allows it; otherwise a concrete outcome in words ("so layouts changed without a new build"). Vary opening verbs across consecutive bullets.

## G. Header convention (required for the PDF template)

Write the header as raw HTML, never as Markdown, so the compiler can lay it out and strip private data for public builds:

```html
<div class="cv-header">
  <div class="cv-header-text">
    <h1>First Last</h1>
    <p class="cv-contact">City, Country · email@example.com · <span class="private">+00 000 000 000 · </span>linkedin.com/in/handle · github.com/handle</p>
  </div>
  <img src="file:///absolute/path/to/photo.jpg" class="profile-photo" />  <!-- only when E says include -->
</div>
```

The phone and its trailing separator sit inside `span.private`. The cover letter uses the same header without the photo and repeats email and phone in the sign-off, phone again inside `span.private`.

Role lines must follow this exact shape so the template can right-align the dates:

```markdown
**Lead Engineer | Example Corp** *(Apr 2019 – Jul 2026, Madrid, Spain)*
```

## H. Writing style

- Plain, specific, active. Participles in summaries ("Bringing…", "Specialized in…") avoid first/third-person clashes.
- Banned phrases and AI tells: see `02-humanization-checklist.md`. They apply to every document, including the generic CV and any website copy derived from the profile.
- Name a tool once per phrase ("C# and Unity", not "Unity and game engines").
- No "Tailored for…", "Customized for…" or any meta text in the documents.
- **A blank line before every list.** The Markdown converter needs it; without it the list renders as one paragraph.

## I. Project portfolio

- Group projects under `## <Title> (<Company>)` headers by role, reverse-chronological across and within sections, with years on every project.
- First-person, active ("I built…"), 2–3 bullets per project, a short technology line per project, no long tool dumps.
- Only projects with a `status` in the profile; academic work is labelled academic.

## J. Cover letter content

The letter tells the reader who the candidate is and why that fits this posting; the CV holds the detail. Paragraph 1 names the role and the single strongest proof point; paragraph 2 says what the reader gets (how the candidate works, the skills and conditions the posting asks for, one or two proofs); paragraph 3 covers availability, engagement and a closing line. One anecdote at most, and only as support for a claim about the candidate. A letter made of anecdotes and curiosities, or one that restates the CV summary, reads as templated and tells the reader nothing about the person. For a marketplace or agency posting, say the application is to be vetted or matched.
