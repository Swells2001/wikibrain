# Your WikiBrain

This is a **WikiBrain** — an LLM second brain for ITM 370. It's three things at
once in a single folder:

- an **Obsidian vault** (your note-taking + graph front end),
- a folder of plain **Markdown** files, and
- a **private GitHub repo** (your versioning + backup).

**Kiro (desktop + CLI) is the engine.** It reads and writes these files directly,
running INGEST / QUERY / LINT per the rules in [`AGENTS.md`](./AGENTS.md). You
decide what's worth keeping; Kiro does the filing — always with your approval.

## How to use it

1. **Open this folder as a vault in Obsidian** (Open folder as vault → pick this
   folder). Open the graph view to see your notes connect.
2. **Open this folder in Kiro** so the engine can see your files.
3. **Add a source:** drop a link, note, or file into `inbox/`, then ask Kiro to
   **ingest** it.
4. **Version it:** commit and push with `gh` / Git — yourself, or let Kiro run the
   git commands in its terminal with your approval. Keep the repo **private**.
5. **Ask it questions:** have Kiro **query** the vault; good answers cite their
   `[[wikilinks]]` and can be filed as a `wiki/syntheses/` page.

## The content floor (at least 10 notes to start)

Your vault needs **at least 10 notes** to start, and must include:

- the two required source notes — the **Google Open Knowledge Format**
  (<https://github.com/GoogleCloudPlatform/open-knowledge-format>) and the
  **Karpathy LLM-wiki gist**
  (<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>),
- class info from **more than one class**,
- a **job** note,
- **real class notes**, and
- your **Ikigai 1 / 2 / 3** material as notes.

## Folder map

```
inbox/      sources waiting to be processed
raw/        processed originals (raw/assets/ for images)
wiki/
  sources/    one page per source
  entities/   people, orgs, products, places, works
  concepts/   ideas, methods, topics
  syntheses/  comparisons, answers, hubs
index.md    a table of every page
log.md      a dated, append-only history
AGENTS.md   the schema — the rulebook Kiro follows
```

See [`AGENTS.md`](./AGENTS.md) for the full schema (page types, frontmatter, body
skeleton, and the INGEST / QUERY / LINT operations).
