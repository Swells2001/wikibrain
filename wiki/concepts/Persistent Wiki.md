---
type: concept
aliases: [LLM-maintained wiki, llm-wiki]
source_count: 1
tags: [knowledge-management]
created: 2026-11-05
updated: 2026-11-05
---

# Persistent Wiki
<!-- note: source_count reflects the single source that defines this concept
(2026-11-05-llm-wiki-pattern). The 2026-11-05-itm-370-week-9-notes source only
cross-references it via [[Expert in the Loop]], so it is not counted as a defining
source. -->


## Core
A persistent wiki is a structured, interlinked collection of [[Markdown]] files that
an LLM incrementally builds and maintains between you and your raw sources. Unlike
[[RAG]], where knowledge is re-derived on every query, the wiki is compiled once and
kept current, so it compounds with every source added.

## Key Points
- Adding a source means reading, extracting, and integrating it — not just indexing.
- Cross-references and contradictions are captured up front, not rediscovered at query
  time.
- The human owns sourcing, exploration, and questions; the LLM does the summarizing,
  cross-referencing, filing, and bookkeeping.
- Three layers: immutable raw sources, the LLM-generated wiki, and the schema.
- Working metaphor: "Obsidian is the IDE; the LLM is the programmer; the wiki is the
  codebase."

## Details
The pattern comes from [[Andrej Karpathy]]'s llm-wiki gist, framed as an idea file to
paste into an LLM agent that then builds out specifics with you. It applies across
personal knowledge tracking, long-running research, reading a book (building a
companion wiki like fan wikis such as Tolkien Gateway), team/business wikis fed by
Slack and meeting transcripts, and other accumulating-knowledge contexts. This
WikiBrain vault itself is an implementation of the pattern.

## Related
- [[RAG]]
- [[Markdown]]
- [[Obsidian]]
- [[Andrej Karpathy]]
- [[Open Knowledge Format]]
- [[Expert in the Loop]] — the "dueling models" second-opinion idea shares this
  pattern's goal of surfacing disagreement rather than affirming the user

## Sources
- [[2026-11-05-llm-wiki-pattern]]
