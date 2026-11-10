---
type: source
source_url: "https://github.com/GoogleCloudPlatform/open-knowledge-format"
source_format: article
author: "Google Cloud Platform"
ingested: 2026-11-05
status: summarized
tags: [knowledge-management]
created: 2026-11-05
updated: 2026-11-05
---

# Open Knowledge Format (GitHub repo)

The repository introduces the **Open Knowledge Format (OKF)**, a vendor-neutral way
to represent knowledge as plain markdown files with YAML frontmatter, organized in a
directory hierarchy. The format is the contribution; a proof-of-concept agent and a
graph visualizer are included to show production and consumption at both ends.

## Key claims
- OKF is not tied to any agent, framework, model provider, or serving system. Anyone
  can produce it (humans, agents on any framework, export pipelines, scripts) and
  anyone can consume it (static file servers, Obsidian/Notion/MkDocs, LLMs, search
  indexes, graph viewers).
- It is human- and agent-readable: no SDK or query language between the reader and
  the content — an engineer can `cat` a concept; an LLM can ingest it verbatim.
- Version-controllable out of the box: bundles live in git, so diffs, blame, and PR
  review make knowledge curation a normal software-engineering activity.
- Portable and lock-in free: a bundle is just a directory (tarball, repo, filesystem).
- Mixes structured and unstructured data deliberately — frontmatter for queryable
  fields (type, resource, tags, generated, status); markdown body for prose and
  schemas.
- v0.2 makes trust, provenance, and freshness first-class via queryable frontmatter
  signals (sources with per-source credibility, generated/verified producers, and
  status/stale_after currency).
- Minimally opinionated and extensible; composes with existing markdown+YAML tools;
  auto-generated `index.md` files give progressive disclosure; concepts link to each
  other as a graph, not just a tree.
- Ships ready-to-browse example bundles (GA4, Stack Overflow, Bitcoin, Acme Retail).

## Connections
- Defines the [[Open Knowledge Format]] concept.
- Published by [[Google Cloud]].
- Built on [[Markdown]] and [[YAML Frontmatter]].
- Designed to be browsed in tools like [[Obsidian]].
- Shares the plain-markdown-knowledge-base philosophy with the [[Persistent Wiki]]
  pattern.
