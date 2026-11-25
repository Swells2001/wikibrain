---
name: idea-validator
description: Use this skill to validate a project idea by running five frameworks against validation/project.md, scoring the results, and producing an action list and dashboard.
---

# Idea Validator

Runs Six Thinking Hats, Blue Ocean Strategy, SWOT, Jobs To Be Done, and MoSCoW on one project, scores each, and tracks the results over time.

## Workflow

1. Read `validation/project.md`.
2. Run each framework file in `validation/frameworks/` against the project, one at a time: `six-hats.md`, `blue-ocean.md`, `swot.md`, `jtbd.md`, `moscow.md`.
3. For every point you make, cite evidence from `project.md` or say "no evidence yet".
4. Score each framework using `validation/rubric.md`.
5. Before scoring, read `validation/action-log.yaml`. For every action from the last run, the student must have a status (done, partly done, not done, won't do) and a how or a why-not. If any are missing, stop and ask for them.
6. Write the run to `validation/runs/` as `run-NN.yaml`, update `validation/history.json`, and append one row to `validation/indicators.csv`.
7. Write a new action list to `validation/actions.md` (see the action rules below) and add the new actions to `action-log.yaml` with status open.
8. Run `python validation/build_dashboard.py`.
9. Print a short summary: scores, what changed since the last run and which finished actions explain it, the top 3 risks, and the next 5 actions.

Save the full framework outputs for each run as `validation/runs/run-NN-frameworks.md`.

## Rules

1. Never invent evidence.
2. Say "unknown" instead of guessing.
3. Keep each framework output under 300 words.
4. Tell the user which statements are AI opinion and which are from real people. Tag each point: [real person], [desk research], [AI opinion], or [no evidence yet].

## Action rules

`validation/actions.md` is rewritten at the end of every run. It lists up to 8 actions, most valuable first. Each action has:

- an id (A-01, A-02, and so on; ids are never reused)
- what to do, in one sentence
- why: which framework and which score it came from
- 2 or 3 recommended ways to do it (concrete, free, doable this week)
- effort: small, medium, or large
- which score it should move

`validation/action-log.yaml` has one entry per action: id, text, created_in_run, status (open, done, partly done, not done, won't do), how (what the student did, and where the proof is), why_not (required if the status is not done or won't do), and updated.

- Do not invent that the student did something.
- At the start of each run, ask the student for the status of every open action and write the answers into the log in the student's own words.
- Do not mark an action done for the student.
- Refuse to run until every action from earlier runs has a status and a how or why-not.
- At the next run, note which scores moved after actions were done, and which moved without any action. A score that moved with no action or new evidence is suspicious and must be explained or reversed.
- Show the status counts (done, partly done, not done, won't do, open) so the dashboard can use them.

## Labels

Every score is an "AI-assisted estimate". Print that label next to every score.
