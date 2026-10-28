# Hub role

The hub is the personal site at `https://<owner>.github.io/`. Its source may live anywhere (often a private workspace); the public `<owner>.github.io` repo is a build output that `publish` writes and nobody edits by hand.

## `init`

1. `portfolio_tool.py remote` for the owner (or ask once and store it in `portfolio.hub.json`).
2. Create the site folder with `portfolio.hub.json`, an `index.html` that has a `<section id="projects">` containing a `.projects-grid`, `style.css`, `main.js` and `assets/`. If a site already exists, only add `portfolio.hub.json` and confirm the grid exists.
3. Each project card in the grid carries `data-slug="<slug>"`; the sync step finds cards by that attribute and never by position or title.

## `sync`

1. `python <skill>/scripts/portfolio_tool.py discover --local-root <parent of the sibling repos>` prints every manifest it found, with its source (local path or URL), and every validation error. Fix nothing in the projects from here; report errors and skip those projects.
2. For each valid manifest:
   - `portfolio_tool.py preview <manifest preview path or URL> assets/<slug>_preview.jpg` (re-encoded, 1200×675).
   - Update the card with that `data-slug`: image `src` and `alt`, title, blurb, up to five tags, a "Site →" link to `site` only if the URL answers 200, and a "GitHub ↗" link to `repo`. Create the card from the hub's existing card markup if none exists, after the other project cards.
   - Update the matching modal entry (in `main.js` or wherever the hub keeps modal data): badge `<status> · <year of updated>`, preview, and links to Site, each entry in `pages`, and the repo.
3. Leave every other part of the hub untouched: the order of cards, which filter they sit under and what else the page says are editorial decisions the manifest does not make.
4. Run `check`.

## `check`

```bash
python <cvkit>/privacy_check.py --paths <site folder>
grep -riE "proven|cutting-edge|seamless|pioneering|high-performance|passionate|world-class" <site folder>/*.html <site folder>/*.js
```

Serve the folder and check both themes (if the hub has them) at 375 px and 1280 px: no horizontal overflow, cards load their images, modals open and close with Escape.

## `publish`

1. `check` must pass.
2. Copy the site folder's contents (not its README) into the local checkout of `<owner>.github.io`.
3. Commit there with a message naming the manifests synced. Do not push; tell the user the push command and that Pages serves `/` of that repo with no further setting.
