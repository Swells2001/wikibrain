# WikiBrain Schema — the AI's Operating Manual

This file is the rulebook for the AI engine (Kiro) that maintains this vault. You
don't have to memorize it — Kiro reads it. Reading it once helps you know what to
expect. *(Adapted/paraphrased from the ITM 310 WikiBrain `SCHEMA.md`.)*

## Your role vs. the AI's role

- **You (the human):** choose sources, drop them in `inbox/`, say "ingest," ask
  questions, and decide what's worth keeping. You never have to do the filing.
- **The AI (Kiro):** reads each source, writes the pages, links them together, flags
  where sources disagree, updates `index.md` and `log.md`, and moves the original
  into `raw/`. It edits files **only with your approval**.

## The three layers

1. **Sources** — the things you feed it. They start in `inbox/` and move to `raw/`
   once processed. The AI reads them but never changes their content.
2. **The wiki** — everything under `wiki/`. The AI owns and writes these pages.
3. **The schema** — this file. The rules.

## Folder layout

```
inbox/      sources waiting to be processed
raw/        processed originals (archive); raw/assets/ for images
wiki/
  sources/    one page per source: wiki/sources/YYYY-MM-DD-short-title.md
  entities/   people/orgs/products/places/works: wiki/entities/Name.md
  concepts/   ideas/methods/topics: wiki/concepts/Name.md
  syntheses/  comparisons, answers, connections, hubs
index.md    a table of every page
log.md      a dated, append-only history
```

## Page naming

- **Entities & concepts:** the page name is the human-readable name, so `[[Memex]]`
  resolves. Use `aliases` for alternate names.
- **Sources:** `YYYY-MM-DD-short-title` (date = the day you added it).
- **Syntheses:** a descriptive name, e.g. `RAG vs Persistent Wiki`.
- **Links:** write `[[Page Name]]` freely in the BODY. A link to a page that doesn't
  exist yet is fine — it's a to-do marker for a page worth creating later.

## Frontmatter (the YAML block at the top of every page)

**Source page**
```yaml
---
type: source
source_url: ""            # the link, or "" if pasted/attached
source_format: article | pdf | image | note
author: ""
ingested: YYYY-MM-DD
status: summarized
tags: [domain-tag]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Entity page**
```yaml
---
type: entity
entity_kind: person | org | product | place | work
aliases: []
source_count: 1
tags: [domain-tag]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Concept page**
```yaml
---
type: concept
aliases: []
source_count: 1
tags: [domain-tag]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Bump `updated` and increment `source_count` whenever a new source touches an
existing page.

## Page body structure

Entity and concept pages follow this skeleton so they stay consistent:

1. **Core** — 2–4 sentences that stand on their own.
2. **Key Points** — self-contained bullets.
3. **Details** — fuller paragraphs; grows as more sources arrive.
4. **Related** — `[[links]]` to connected pages.
5. **Sources** — the `[[source pages]]` that informed this page.

- **Source pages:** a tight summary (key claims, takeaways, data), then a
  `## Connections` section linking the entities and concepts it touches.
- **Contradictions:** if a new source disagrees with an existing claim, do NOT
  overwrite — add a `## Contradictions / open questions` note citing both sources
  and the date.

> **Graph note:** Obsidian draws graph edges from `[[wikilinks]]` in the note
> **body**, not from frontmatter. Keep one hub / Map-of-Content note that pages
> link to.

## The three operations

### INGEST (process the inbox)
For each item in `inbox/`:
1. Read it.
2. Write a source page in `wiki/sources/` with frontmatter and a summary.
3. Create or update every entity and concept it touches, with links in both
   directions. Bump `updated`, increment `source_count`.
4. Flag contradictions against existing claims.
5. Add a row to `index.md` for each new/changed page.
6. Append an entry to `log.md`.
7. Move the original from `inbox/` into `raw/` (images into `raw/assets/`).

### QUERY (ask the wiki a question)
1. Read `index.md` to find relevant pages, then read those pages (following their
   `[[links]]`).
2. Answer with `[[wikilink]]` citations to the pages used.
3. Offer to file a good answer back as a `wiki/syntheses/` page so your
   explorations compound.

### LINT (health check)
Report, with severity, and act only with your go-ahead:
- Unresolved links (your "create next" backlog)
- Orphan pages (no inbound links)
- Items still sitting in `inbox/`
- Pages that look thin / under-developed
- Missing reciprocal links (A links to B but B doesn't link back)
- Contradictions and gaps worth filling

## index.md and log.md formats

`index.md` is a table, grouped by category (Sources, Entities, Concepts,
Syntheses):

```markdown
| Page | Summary | Sources | Updated |
|------|---------|---------|---------|
| [[Memex]] | Bush's 1945 associative knowledge store | [[2026-06-08-llm-wiki-pattern]] | 2026-06-08 |
```

`log.md` is append-only, newest entries at the bottom, each with a greppable
header:

```markdown
## [2026-06-08] ingest | Article Title
- Source: raw/2026-06-08-article-title.md
- Created: [[New Concept]], [[New Entity]]
- Updated: [[Existing Concept]]
```
