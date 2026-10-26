# `/portfolio` skill design (2026-10-26)

A second skill in this repo, `.claude/skills/portfolio/`, that builds a personal portfolio hub and the project sites it links to. Not built yet; this note fixes the decisions.

## Roles, detected from files

- **hub**: the folder holds `portfolio.hub.json` at the site root. Serves at the user site (`<owner>.github.io`).
- **project**: the folder holds `docs/site/portfolio.json` (or `site/portfolio.json`). Serves at `<owner>.github.io/<repo>/` from inside the project repo through a Pages workflow that publishes only the site folder.
- Neither file present: `init` asks which role and scaffolds it. No other heuristic.

## Commands

- `init`: scaffold the role (site folder, config or manifest, Pages workflow template).
- `sync`: project: capture guidance, build the pages, write the manifest and preview, run `check`. Hub: discover projects, read manifests (local sibling folder first, published URL second), skip the hidden list, rebuild only the project cards, run `check`. Never pushes.
- `check`: validate the manifest against `contract/portfolio.schema.json`, the privacy patterns, the banned-phrase list, and image size.
- `publish` (hub only): copy the site folder into the hub repo checkout, run `check`, commit. Pushing stays a human step.

## The contract

`contract/portfolio.schema.json` (JSON Schema, `schema` field versioned) and `contract/CONTRACT.md`. A hub ignores manifests with an unknown schema version and says so. Required keys: `schema`, `name`, `slug`, `status`, `blurb` (≤ 45 words), `tags` (≤ 5), `preview` (1200×675 JPEG ≤ 300 KB), `pages`, `updated`. `site` and `repo` are written by the skill, not typed by hand.

## No hardcoded URLs or owners

The skill must work after a fork with no edits:

- Owner and repo name come from `git remote get-url origin` (SSH or HTTPS forms both parsed). If there is no remote, the skill asks once and stores the answer in the role's config file.
- Project site URL = `https://<owner>.github.io/<repo>/`; hub URL = `https://<owner>.github.io/`. Both can be overridden by a `base_url` field in `portfolio.hub.json` or `portfolio.json` (custom domains, GitLab Pages, a different host).
- Discovery uses `gh api users/<owner>/repos` with `<owner>` taken from the remote, never from a constant. Without `gh`, the hub falls back to the `projects` list in `portfolio.hub.json`.
- The skill files, templates and contract contain no account name, no email, no domain other than `github.io` as a pattern. Example values use `example` placeholders. The author's own links appear only in the explainer site's footer, which forks are expected to change.
- `privacy_check.py` runs over the skill folder in this repo's tests, so a hardcoded personal value fails CI.

## Where the work happens

One driver session in the private workspace, with the project repos added as extra working directories; `hub sync` walks sibling folders. The skill is installed in every repo through the-library, so a session opened in a project repo works the same way.
