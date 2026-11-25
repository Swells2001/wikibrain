# Scoring rubric

Every score in this project is an **AI-assisted estimate**.

Score each framework output from 0 to 100. There are five criteria, worth 20 points each.

| Criterion | 20 points means |
|---|---|
| Evidence | Cites real people, data, or tests |
| Specificity | Concrete, not generic |
| Completeness | Every part of the framework is filled |
| Honesty | Names real weaknesses and unknowns |
| Actionability | Leads to a decision or next step |

## Hard rules

1. No evidence means Evidence cannot be above 5.
2. A score may only rise from the last run if you can point to new evidence or a changed decision.
3. List the reason for every change, up or down.

## Overall score

The overall score is the average of the five framework scores, rounded to a whole number.

## Three more numbers to record each run

- `evidence_count`: the number of real conversations or tests. Desk research and AI opinions do not count.
- `open_risks`: the number of distinct risks that are still unresolved.
- `decisions_changed`: the number of project decisions that changed since the last run.

## indicators.csv

Every run appends ONE row to `validation/indicators.csv` with exactly these columns in this order:

```
date,run,trigger,overall,six_hats,blue_ocean,swot,jtbd,moscow,evidence_count,open_risks,decisions_changed,actions_total,actions_done,actions_open,action_completion_pct
```

- All values are whole numbers except `date` and `trigger`.
- Never edit or delete old rows.
- Create the file with the header row if it does not exist.
- `action_completion_pct` = actions_done divided by actions_total, times 100, rounded to a whole number (0 if there are no actions).

Label every score "AI-assisted estimate".
