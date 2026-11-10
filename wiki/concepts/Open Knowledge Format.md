---
type: concept
aliases: [OKF]
source_count: 1
tags: [knowledge-management]
created: 2026-11-05
updated: 2026-11-05
---

# Open Knowledge Format

## Core
The Open Knowledge Format (OKF) is a universal, vendor-neutral format for representing
knowledge as plain [[Markdown]] files with [[YAML Frontmatter]], organized in a
directory hierarchy. It is deliberately not tied to any agent, framework, model
provider, or serving system.

## Key Points
- Human- and agent-readable with no SDK or query language in between.
- Version-controllable out of the box — bundles live in git and get diffs, blame,
  and PR review.
- Portable and lock-in free: a bundle is just a directory.
- Separates a small set of queryable frontmatter fields from the markdown body prose.
- v0.2 treats trust, provenance, and freshness as first-class via queryable signals.
- Graph-shaped: concepts link to each other, not just parent/child in the tree.

## Details
OKF is maintained by [[Google Cloud]] and published as a v0.2 specification. The
repository includes a proof-of-concept agent that produces OKF bundles automatically
and a bundled graph visualizer, but the format itself — not the tooling — is the
contribution. Because it is just markdown plus YAML, it composes with existing tools
like [[Obsidian]], Notion, and MkDocs, and auto-generated `index.md` files allow an
agent or human to navigate one level at a time (progressive disclosure).

## Related
- [[Markdown]]
- [[YAML Frontmatter]]
- [[Obsidian]]
- [[Persistent Wiki]]
- [[Google Cloud]]

## Sources
- [[2026-11-05-open-knowledge-format]]
