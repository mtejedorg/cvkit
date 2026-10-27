# Project role

A project site has three pages and a manifest. It lives in `docs/site/` so that the rest of `docs/` (design documents, plans, handoff notes) stays out of the published site; only `docs/site/` is deployed, through the workflow in `../assets/pages-workflow.yml`.

## `init`

1. `portfolio_tool.py remote` gives owner and repo; refuse to continue without a remote unless the user supplies both.
2. Create `docs/site/` with `index.html`, `mechanics.html`, `tech.html`, `style.css`, `assets/`, and a `portfolio.json` with the computed `site` and `repo` and placeholder text marked `TODO`.
3. Copy `../assets/pages-workflow.yml` to `.github/workflows/pages.yml`.
4. Add the capture helper for the engine (see [captures.md](captures.md)), after asking, since it touches the project.
5. Tell the user the one-time step: repository Settings → Pages → Source "GitHub Actions".

## `sync`

Sources, in this order: `README.md`, then anything under `docs/` that reads as a design or technical document (GDD, TDD, ARCHITECTURE, TESTPLAN, ASSETS), then what you observe by running the software. Read them before writing a word.

- **index.html**: the hero capture, a one-paragraph pitch in the project's own words, status, three links (mechanics, tech, repo). No feature list here; that is what the other two pages are for.
- **mechanics.html**: how it plays or how it is used. Loop, controls, classes or enemies, progression, rules. Written from the design document; where the document gives a number, cite the file in an HTML comment.
- **tech.html**: engine or stack, architecture, the systems that took real engineering (networking, combat, rendering, persistence), tooling and testing, and one short paragraph on the AI-assisted workflow naming the agents the repo uses.
- Shared header and footer. Mobile-first CSS, no external JavaScript frameworks, no trackers, fonts self-hosted or system. The project may have its own look; it does not need to match the hub.
- Pick captures: at least the main menu or landing state, something mid-use, one secondary screen, and the single strongest frame for the preview. Run `portfolio_tool.py preview <capture> docs/site/assets/preview.jpg`.
- Rewrite `portfolio.json` (blurb ≤ 45 words, ≤ 5 tags, today's date) and run `check`.

## `check`

```bash
python .claude/skills/portfolio/scripts/portfolio_tool.py validate docs/site/portfolio.json
python <cvkit>/privacy_check.py --paths docs/site        # if a patterns file exists
grep -riE "proven|cutting-edge|seamless|pioneering|high-performance|passionate|world-class|state-of-the-art" docs/site/*.html
```

Serve `docs/site/` locally and look at all three pages at 375 px and 1280 px: no horizontal overflow, every link resolves, every image loads.

## What not to do

- Do not describe features that only exist in a plan or a to-do list as if they existed.
- Do not use concept art, AI renders or mockups as gameplay or product captures. A section titled "Concept art" may show them, labelled.
- Do not publish `docs/` as a whole.
