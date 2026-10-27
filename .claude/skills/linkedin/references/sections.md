# LinkedIn sections: limits and what goes where

Limits change without notice; the numbers below are the commonly documented ones. The editor's own counter is the final word, which is why every generated section states its count and keeps a five percent margin.

| Section | Limit | Shown where | What belongs |
|---|---|---|---|
| Headline | 220 characters | Everywhere your name appears (search, comments, messages) | Role family plus the two or three things you are known for, in words a recruiter searches. The `### General` headline from the profile is the starting point. No "seeking opportunities" unless the open-to-work frame is off and the user wants it in text. |
| About | 2,600 characters | Top of the profile; only the first ~300 characters show before "see more" | First two lines: the single strongest proof point and who you are. Then three to five short paragraphs: what you build, where you have shipped it, how you work (AI-assisted workflow belongs here if the profile says so), what you are looking for. End with how to reach you (email only if the user wants it public). |
| Experience entry: title | 100 characters | Card | The real title. Both titles joined with " / " when the profile says to combine them under one date range. |
| Experience entry: description | 2,000 characters | Card, collapsed | Context line, then three to six lines mirroring the CV's leading bullets for that role. LinkedIn renders no bullets; use line breaks and a leading "•" or "–". |
| Experience: skills per role | 5 pinned | Card | The five skills with `production` depth that the role proves. |
| Skills | 50 listed (the platform may allow more; check), 3 shown as "Top skills" | Skills section, search | Every `production` and `working` skill from the profile that a recruiter would search; nothing at `academic`, `evaluated` or `supervised` depth. Top three = the flagship skills of the General positioning profile. |
| Featured | A few items | Below About | The public generic CV (`_public.pdf` only), the portfolio hub, one or two project sites with real previews, a post that did well. |
| Projects | Title 255, description 2,000 | Lower on the profile | Own projects from `## Projects` with status "in development" or "released"; link to the project site. |
| Education | Degree 100, field 100 | Lower | Both degrees from `## Education`, English names, dates as recorded. |
| Licenses, publications | — | Lower | Only what the profile lists; the profile's `## Not claimable` rules out talks and papers that do not exist. |
| Open to work | Frame or recruiter-only | Photo / recruiter search | Recruiter-only is the quiet option; the public frame is the loud one. Decide from `## Preferences`; default to recruiter-only. |
| Contact info | Email, phone, website, custom URL | Profile header, visibility configurable | Phone off. Email visible to connections only unless the profile says public. Website = the portfolio hub. Custom URL = the handle in `## Identity`. |
| Profile photo and banner | Photo square, banner 1584×396 | Header | The profile's photo path if present; banner from a real capture or a plain color, never generated art. |

## Rules that follow from the profile

- Dates and titles match `## Experience` exactly; LinkedIn is where a background check starts.
- A role's description never carries a number that the CV would not carry; `## Preferences` → `metrics:` applies here too.
- Languages: the levels in `## Languages and mobility`, using LinkedIn's own scale (elementary, limited working, professional working, full professional, native).
- Location: the city in `## Identity`. Relocation and remote preferences go into the open-to-work settings, not into the About text, unless `## Languages and mobility` has a `rule:` saying otherwise.

## `live.md` format

```markdown
# LinkedIn live text

## Headline
last pasted: 2026-10-27
<text>

## About
last pasted: 2026-10-27
<text>

## Experience: <Title> | <Company>
last pasted: 2026-10-27
<text>

## Skills
last pasted: 2026-10-27
- <skill> (top)
- <skill>
```

Sections absent from the file are treated as "unknown", not as empty: `audit` asks for them before judging.
