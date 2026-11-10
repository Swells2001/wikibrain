---
type: concept
aliases: [Retrieval-Augmented Generation]
source_count: 1
tags: [knowledge-management]
created: 2026-11-05
updated: 2026-11-05
---

# RAG

## Core
RAG (Retrieval-Augmented Generation) is the common LLM+document pattern: upload files,
retrieve relevant chunks at query time, and generate an answer. It is the foil the
[[Persistent Wiki]] pattern defines itself against.

## Key Points
- Knowledge is re-derived from raw documents on every query — nothing accumulates.
- Synthesizing across many documents must be redone each time a question is asked.
- Contrasts with a persistent, compounding wiki where knowledge is compiled once.

## Related
- [[Persistent Wiki]]

## Sources
- [[2026-11-05-llm-wiki-pattern]]
