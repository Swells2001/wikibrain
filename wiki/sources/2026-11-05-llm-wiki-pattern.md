---
type: source
source_url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
source_format: note
author: "Andrej Karpathy"
ingested: 2026-11-05
status: summarized
tags: [knowledge-management]
created: 2026-11-05
updated: 2026-11-05
---

# llm-wiki (a pattern for LLM-maintained knowledge bases)

Karpathy's gist describes a pattern for building personal knowledge bases with LLMs.
It is framed as an "idea file" meant to be pasted into your own LLM agent; the agent
then builds the specifics in collaboration with you.

## Key claims
- Most LLM+document experiences are [[RAG]]: upload files, retrieve relevant chunks
  at query time, generate an answer. The LLM rediscovers knowledge from scratch every
  question — nothing accumulates.
- The alternative: the LLM incrementally builds and maintains a **persistent wiki** —
  a structured, interlinked set of markdown files sitting between you and the raw
  sources.
- Adding a source isn't just indexing: the LLM reads it, extracts key info, and
  integrates it — updating entity pages, revising summaries, flagging contradictions,
  strengthening or challenging the synthesis.
- The wiki is a persistent, compounding artifact: cross-references and contradictions
  are already there; knowledge is compiled once and kept current, not re-derived.
- You rarely write the wiki yourself — you own sourcing, exploration, and asking good
  questions; the LLM does the summarizing, cross-referencing, filing, and bookkeeping.
- Working model: LLM agent on one side, [[Obsidian]] on the other —
  "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."
- Three layers: raw sources (immutable source of truth), the wiki (LLM-generated
  markdown), and the schema.
- Applies to personal notes, research, reading a book (like fan wikis such as Tolkien
  Gateway), business/team wikis, competitive analysis, and more.

## Connections
- Describes the [[Persistent Wiki]] concept.
- Authored by [[Andrej Karpathy]].
- Defined in contrast to [[RAG]].
- Built on [[Markdown]] and browsed in [[Obsidian]].
- Shares the plain-markdown-knowledge-base philosophy with the
  [[Open Knowledge Format]].
