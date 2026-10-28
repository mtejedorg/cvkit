---
name: portfolio
description: Build and keep in sync a personal portfolio hub site and the project sites it links to, on GitHub Pages, from one small manifest contract. Use this whenever the user wants a portfolio website, a project page or landing page for a repo, a summary card and preview image for a project, GitHub Pages set up for a site folder, or to pull every project's summary into a main site, even if they only say "add my game to my site" or "make a page for this repo". Owner, repo names and URLs are read from the git remote, never hardcoded.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Portfolio

One skill, two roles. A **hub** is the personal site at `https://<owner>.github.io/`; it shows one card per project. A **project** is any repo that publishes its own site at `https://<owner>.github.io/<repo>/` plus a manifest the hub reads. The contract between them is [references/contract.md](references/contract.md); the hub never scrapes a project, it reads `portfolio.json`.

Three rules decide every choice, the same ones the cv-builder skill uses:

1. **Only real facts and real images.** Every sentence on a site comes from the repo's own documents or from running the software. Screenshots are captures of the real thing; concept art is labelled concept art. If a fact is not documented, leave the section out and say so.
2. **Nothing personal leaks.** No phone numbers anywhere. Email, if shown, is assembled by JavaScript from split attributes. The privacy check runs before any commit.
3. **Nothing is hardcoded.** Owner and repo come from `git remote get-url origin`; URLs are computed; a `base_url` field overrides them for custom domains. A fork works with no edits.

## Requires the cvkit repo

The helper script ships with this skill; the privacy scan, the generic personas and the rules the panel and the copy follow live in the cvkit repo. `<cvkit>` below is the root of a clone of `https://github.com/mtejedorg/cvkit` (or a fork) and `<skill>` is the folder this `SKILL.md` was loaded from. Locate `<cvkit>` at the start of every run: the current directory if it holds `privacy_check.py` and `cvtool/`, else the folder the `CVKIT_HOME` environment variable names, else ask the user (offer `git clone`, and wait for a yes).

| What | Path |
|---|---|
| Helper script (detect, remote, validate, discover, preview) | `python <skill>/scripts/portfolio_tool.py` |
| Privacy scan | `python <cvkit>/privacy_check.py` |
| Generic personas | `<cvkit>/templates/personas/` |
| Persona panel rules, banned phrases | `<cvkit>/.claude/skills/cv-builder/06-persona-review.md`, `02-humanization-checklist.md` |

**Running it against another repo.** The skill is not tied to the cvkit folder. Copy `<cvkit>/.claude/skills/portfolio` to `~/.claude/skills/portfolio` to have it in every repo, or into that repo's `.claude/skills/` for one, then open Claude Code in the repo that needs the page.

## Detect the role first

Run `python <skill>/scripts/portfolio_tool.py detect` in the repo. It answers `hub` (a `portfolio.hub.json` at the site root), `project` (`docs/site/portfolio.json` or `site/portfolio.json`), or `none`. On `none`, `init` asks which role to scaffold. Do not guess from the repo's contents.

## Commands

| Command | Hub | Project |
|---|---|---|
| `init` | Scaffold `portfolio_site/` (or the chosen folder) with `portfolio.hub.json`, a starter page and the Pages workflow. See [references/hub.md](references/hub.md). | Scaffold `docs/site/` with three pages, `portfolio.json`, the capture helper and the Pages workflow. See [references/project.md](references/project.md). |
| `sync` | Discover projects, read their manifests (local sibling folder first, published URL second), rebuild only the project cards and modals, run `check`. Never pushes. | Refresh captures if asked, rebuild the pages from the repo's docs, rewrite the manifest and preview, run `check`. |
| `check` | Validate every manifest against the contract, run the privacy check on the site folder, grep for banned phrases, confirm image sizes, then run the **persona panel** on the hub page with every persona whose `reviews` lists `portfolio-site` (generic ones in `<cvkit>/templates/personas/`, the user's in `<workspace>/_private/personas/`), per the cv-builder skill's `06-persona-review.md`. A public page faces every reader at once, so nobody is left out. | Same, for this project's manifest and pages. |
| `publish` | Copy the site folder into the hub repo checkout, run `check`, commit. Pushing stays with the user. | Explain the one-time Pages setting; the workflow deploys on push. |

`<skill>/scripts/portfolio_tool.py` does the deterministic parts (detect, remote parsing, validation, discovery, preview resizing) so each run spends its effort on content, not plumbing. Read its `--help` once.

## Writing the copy

Plain sentences, specific facts, no marketing words. The banned list in the cv-builder skill's `02-humanization-checklist.md` (in `<cvkit>/.claude/skills/cv-builder/`) applies here too. Say "built solo with AI coding agents" once per project, on its tech page, naming the agents the repo actually uses; the author wants that visible, and it is true. Any figure (players, zones, tests, fps) must appear in a repo document; cite the file in an HTML comment next to it.

## Approval model

Mechanical steps run without asking: detecting the role, parsing the remote, validating manifests, discovering projects, resizing previews, running the checks and the privacy scan. Everything a reader will see is shown first and written only on a yes: the pitch, each page's copy, the blurb and tags in the manifest, which capture becomes the preview, card changes on the hub, and the `publish` commit. One question per decision, with the proposed text in it. The profile's `## Preferences` → `approval:` line may make this stricter, never looser.

## Boundaries

- Touch only the site folder, the manifest, the Pages workflow and the single capture helper. Never change gameplay or product code, build settings or assets outside the site folder.
- Stop and ask before adding a dependency, deleting a file, or if the software does not launch for captures.
- Never push, never enable Pages, never create a repo. Report the exact Settings → Pages step instead.

## Progress and reporting

After each command, one line: what was produced, with paths. End a `sync` with: manifests found (local or remote), what changed per card, anything skipped and why, and facts you could not source.
