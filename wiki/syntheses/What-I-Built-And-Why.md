---
type: synthesis
aliases: [What I Built And Why, build recap]
source_count: 0
tags: [itm-370, wikibrain, recap]
created: 2026-11-05
updated: 2026-11-05
---

# What I Built And Why

A plain-language recap of building my WikiBrain on 2026-11-05, from `log.md`, my git
history, and the work session with Kiro. Hub: [[My Project]].

## 1. Step by step

1. **Read the rulebook.** Kiro read `AGENTS.md` and summarized how it files a source.
2. **Ingested the two required sources.** Created [[2026-11-05-open-knowledge-format]]
   and [[2026-11-05-llm-wiki-pattern]], plus [[Open Knowledge Format]],
   [[Persistent Wiki]], [[Markdown]], [[YAML Frontmatter]], [[RAG]], [[Obsidian]],
   [[Google Cloud]], and [[Andrej Karpathy]].
3. **Ingested my class notes, then split them.** Kiro first filed my ITM 370 reflection
   and my International Econ notes as one source. I said they were two classes, so it
   split them into [[2026-11-05-itm-370-week-9-notes]] (with [[Noah]] and
   [[Expert in the Loop]]) and [[2026-11-05-intl-econ-import-quotas]] (with
   [[Import Quota]], [[Tariff]], [[Quota Rent]], [[Small Open Economy]]). I chose to
   rewrite that log entry instead of appending a correction.
4. **Wrote my job note.** [[Quail Hollow Golf Course]], five skill pages
   ([[Customer Service]], [[Conflict Resolution]], [[Phone Skills]], [[CRM Skills]],
   [[Sales Skills]]), and the [[Career & Skills Hub]].
5. **Ingested Ikigai Parts 1–3.** [[2026-11-05-ikigai-1-discover]],
   [[2026-11-05-ikigai-2-opportunity]], and a placeholder [[2026-11-05-ikigai-3-validate]]
   (I haven't pasted Part 3 yet). This built [[My Project]],
   [[Youth Hockey Skills Training]], [[Ikigai]], [[Robin]], [[Idaho IceWorld]],
   [[Next Level Hockey Idaho]], [[Market Gap Analysis]], [[Customer Discovery]],
   [[AI Stress Test]], [[Solomon Wells]], [[Leadership]], and [[Public Speaking]]. The
   ingest got cut off halfway, so seven of those pages were missing until the next step.
6. **Ran LINT.** It found the seven missing Ikigai pages, which Kiro then wrote. It also
   added links back to [[My Project]] and aliases so the hub's "Ikigai Part 1/2/3"
   links resolve.
7. **Backed up to GitHub.** Installed Git, made commit `5044c96` ("add required sources,
   Ikigai, class + job notes"), logged in to GitHub, and pushed to my private repo
   `Swells2001/wikibrain`.
8. **Built a no-API-key LINT robot.** `.github/workflows/wikibrain-lint.yml` and
   `scripts/lint.py` check broken links, orphans, and frontmatter, and commit
   `lint-report.md` as `wikibrain-bot`. *Status: written, not yet committed or run.*
9. **Asked my brain a question (QUERY).** "How does my Ikigai project connect to my
   other classes?" The answer is filed as [[Ikigai Project and Coursework]].
10. **Made one bounded change.** Sorted `index.md` A–Z within each section and wrote my
    Bounded Change Receipt. *Status: written, not yet committed.*

## 2. Why each step mattered

1. The rulebook keeps every page the same shape, so the vault stays searchable.
2. The two required sources explain the idea I'm building: a wiki an AI maintains instead
   of re-reading files every time.
3. Splitting the notes kept two different classes from being mixed up in one page.
4. The job note ties my work skills to the rest of my learning.
5. Ikigai is the core of the class project, and every later step connects to it.
6. LINT caught a broken half-finished ingest that I would have missed by eye.
7. Git gives me a backup and a history, so any change can be undone.
8. The robot keeps checking the vault's health without me remembering to.
9. Filing answers makes the brain grow from questions, not just sources.
10. A small, reversible change shows I can control what the AI does, not just accept it.

## 3. How the pieces fit

Obsidian is my notebook. I read and browse my notes there and watch the graph connect.
Kiro is the writer. It reads `AGENTS.md`, writes and links the pages, and updates
`index.md` and `log.md`, but only after I approve each change. GitHub is the backup. It
stores every version of the vault privately and runs the LINT robot. The SDLC shows up
all the way through:
- **Requirements:** `AGENTS.md` and the assignment's content floor.
- **Design:** page types and the [[My Project]] hub.
- **Implementation:** the ingests.
- **Testing:** LINT and the row-count checks on `index.md`.
- **Deployment:** pushing to GitHub.
- **Maintenance:** the daily LINT Action and the append-only `log.md`.

## 4. What I learned to watch for

I pasted a GitHub token into the chat while trying to log in, and I had to revoke it.
Secrets and one-time login codes belong only in GitHub's own pages, never in a chat.
For my bounded change, I chose tidying `index.md` over the other three options because
it touched only one file, was easy to check by counting rows, and could be undone with
`git revert`.
