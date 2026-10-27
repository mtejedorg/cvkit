# The portfolio contract

A project becomes part of a hub by publishing two files with its site. Nothing else is required; the hub never reads a project's README or code.

## `portfolio.json` (schema 1)

Lives at `docs/site/portfolio.json` (or `site/portfolio.json`) and is served at `<project site>/portfolio.json`.

```json
{
  "schema": 1,
  "name": "Example Game",
  "slug": "example-game",
  "status": "in development",
  "engine": "Godot 4",
  "blurb": "A 2.5D beat-driven action roguelite. Ten zones, two bosses, every enemy telegraph locked to the music. Built solo with AI coding agents.",
  "tags": ["Godot 4", "GDScript", "State machines"],
  "preview": "assets/preview.jpg",
  "site": "https://example.github.io/example-game/",
  "repo": "https://github.com/example/example-game",
  "pages": { "mechanics": "mechanics.html", "tech": "tech.html" },
  "updated": "2026-10-27",
  "base_url": null
}
```

| Key | Rule |
|---|---|
| `schema` | Integer, currently `1`. A hub ignores versions it does not know and says so. |
| `name` | Display name. |
| `slug` | Lowercase letters, digits and hyphens; starts with a letter. Used for file names and `data-slug` on the hub card. |
| `status` | One of `in development`, `released`, `prototype`, `archived`. |
| `engine` | Free text, short (engine, framework or language). Optional. |
| `blurb` | At most 45 words. Plain language, facts from the repo's docs only. |
| `tags` | At most 5 short technology names. |
| `preview` | Relative path to a 1200×675 JPEG under 300 KB, cropped from a real capture. |
| `site`, `repo` | Written by the tool from the git remote, never typed. |
| `pages` | Relative paths of the mechanics and tech pages (or whatever two deep pages the project has; keys are free). |
| `updated` | ISO date of the last manifest rewrite. |
| `base_url` | Optional override of the computed site URL (custom domain, another host). |

The machine-readable version is [`../assets/portfolio.schema.json`](../assets/portfolio.schema.json); `portfolio_tool.py validate` enforces the same rules without needing a JSON Schema library.

## `preview.jpg`

Exactly 1200×675, JPEG, at most 300 KB, a real capture. `portfolio_tool.py preview <src> <dst>` crops and encodes it.

## `portfolio.hub.json` (hub side)

```json
{
  "schema": 1,
  "owner": null,
  "base_url": null,
  "projects": [],
  "hidden": ["old-student-repo", "fork-of-something"],
  "site_dir": "."
}
```

`owner` and `base_url` stay `null` unless the git remote cannot supply them. `projects` is a fallback list of repo names for machines without `gh`. `hidden` excludes repos that do publish a manifest but should not appear.

## Discovery order (hub `sync`)

1. Sibling folders of the hub checkout that contain a manifest (fast, works offline, sees unpublished work).
2. `gh api users/<owner>/repos --paginate` for every other repo, fetching `https://<owner>.github.io/<repo>/portfolio.json`; 404 means "not a portfolio project".
3. Without `gh`: the `projects` list.

A manifest found locally wins over the published one, since the local one is newer by definition.
