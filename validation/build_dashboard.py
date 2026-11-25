#!/usr/bin/env python3
"""Build validation/dashboard/index.html as one self-contained file.

Uses only the Python standard library. Reads:
  project.md, history.json, indicators.csv, actions.md, action-log.yaml
Run from anywhere:  python validation/build_dashboard.py
"""
import csv
import datetime
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
FRAMEWORKS = [
    ("six_hats", "Six Thinking Hats"),
    ("blue_ocean", "Blue Ocean Strategy"),
    ("swot", "SWOT"),
    ("jtbd", "Jobs To Be Done"),
    ("moscow", "MoSCoW"),
]
STATUSES = ["open", "done", "partly done", "not done", "won't do"]
BLUE = "#0b4f8a"
ORANGE = "#a33c00"


def esc(value):
    return html.escape(str(value))


def read_header(path):
    """Read the simple key: value YAML header at the top of a Markdown file."""
    out = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if ":" in line:
                key, value = line.split(":", 1)
                out[key.strip()] = value.strip().strip('"')
    return out


def read_indicators(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_actions(path):
    """Read actions.md: a '## A-01' heading followed by a '- What:' line."""
    actions, current = [], None
    if not path.exists():
        return actions
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text.startswith("## A-"):
            current = {"id": text[3:].strip(), "what": ""}
            actions.append(current)
        elif current is not None and text.startswith("- What:"):
            current["what"] = text[len("- What:"):].strip()
    return actions


def read_action_log(path):
    """Read the flat list in action-log.yaml without needing a YAML library."""
    entries, current = [], None
    if not path.exists():
        return entries
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        if text.startswith("- id:"):
            current = {"id": text.split(":", 1)[1].strip().strip('"')}
            entries.append(current)
        elif current is not None and ":" in text:
            key, value = text.split(":", 1)
            current[key.strip()] = value.strip().strip('"')
    return entries


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def x_positions(dates, left, right):
    days = [datetime.date.fromisoformat(d).toordinal() for d in dates]
    low, high = min(days), max(days)
    if low == high:
        return [(left + right) / 2 for _ in days]
    return [left + (d - low) * (right - left) / (high - low) for d in days]


def line_chart(chart_id, title, rows, series):
    """series: list of dicts with key, label, color, marker, dash, ymax, side."""
    width, height = 680, 300
    left, right, top, bottom = 60, 620, 40, 240
    out = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="{chart_id}-t" '
        f'xmlns="http://www.w3.org/2000/svg">',
        f'<title id="{chart_id}-t">{esc(title)}</title>',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
    ]
    for step in range(5):
        y = bottom - step * (bottom - top) / 4
        out.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="#c9c9c9" stroke-width="1"/>')
        for item in series:
            label = round(item["ymax"] * step / 4)
            if item["side"] == "left":
                out.append(f'<text x="{left - 8}" y="{y + 5:.1f}" text-anchor="end" font-size="13" fill="{item["color"]}">{label}</text>')
            else:
                out.append(f'<text x="{right + 8}" y="{y + 5:.1f}" text-anchor="start" font-size="13" fill="{item["color"]}">{label}</text>')
    out.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#111111" stroke-width="2"/>')
    if rows:
        xs = x_positions([r["date"] for r in rows], left + 30, right - 30)
        for x, row in zip(xs, rows):
            out.append(f'<text x="{x:.1f}" y="{bottom + 20}" text-anchor="middle" font-size="13" fill="#111111">{esc(row["date"])}</text>')
            out.append(f'<text x="{x:.1f}" y="{bottom + 37}" text-anchor="middle" font-size="12" fill="#111111">run {esc(row["run"])}</text>')
        for number, item in enumerate(series):
            points = []
            for x, row in zip(xs, rows):
                value = to_int(row.get(item["key"]))
                y = bottom - min(value, item["ymax"]) * (bottom - top) / item["ymax"]
                points.append((x, y, value))
            if len(points) > 1:
                path = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in points)
                dash = ' stroke-dasharray="7 5"' if item["dash"] else ""
                out.append(f'<polyline points="{path}" fill="none" stroke="{item["color"]}" stroke-width="3"{dash}/>')
            for x, y, value in points:
                if item["marker"] == "square":
                    out.append(f'<rect x="{x - 6:.1f}" y="{y - 6:.1f}" width="12" height="12" fill="{item["color"]}"/>')
                else:
                    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{item["color"]}"/>')
                if number == 0:
                    out.append(f'<text x="{x + 12:.1f}" y="{y - 6:.1f}" font-size="14" font-weight="bold" fill="{item["color"]}">{value}</text>')
                else:
                    out.append(f'<text x="{x - 12:.1f}" y="{y - 6:.1f}" text-anchor="end" font-size="14" font-weight="bold" fill="{item["color"]}">{value}</text>')
    legend_x = left
    for item in series:
        if item["marker"] == "square":
            out.append(f'<rect x="{legend_x}" y="12" width="12" height="12" fill="{item["color"]}"/>')
        else:
            out.append(f'<circle cx="{legend_x + 6}" cy="18" r="6" fill="{item["color"]}"/>')
        out.append(f'<text x="{legend_x + 18}" y="23" font-size="14" fill="#111111">{esc(item["label"])}</text>')
        legend_x += 30 + 8 * len(item["label"])
    out.append("</svg>")
    return "\n".join(out)


def bar_chart(chart_id, title, scores):
    row_height, left, bar_max = 40, 190, 380
    height = row_height * len(FRAMEWORKS) + 20
    out = [
        f'<svg viewBox="0 0 680 {height}" role="img" aria-labelledby="{chart_id}-t" xmlns="http://www.w3.org/2000/svg">',
        f'<title id="{chart_id}-t">{esc(title)}</title>',
        f'<rect x="0" y="0" width="680" height="{height}" fill="#ffffff"/>',
    ]
    for index, (key, label) in enumerate(FRAMEWORKS):
        value = to_int(scores.get(key))
        y = 10 + index * row_height
        out.append(f'<text x="{left - 10}" y="{y + 21}" text-anchor="end" font-size="15" fill="#111111">{esc(label)}</text>')
        out.append(f'<rect x="{left}" y="{y + 4}" width="{bar_max}" height="24" fill="#e6e6e6"/>')
        out.append(f'<rect x="{left}" y="{y + 4}" width="{bar_max * min(value, 100) / 100:.1f}" height="24" fill="{BLUE}"/>')
        out.append(f'<text x="{left + bar_max + 10}" y="{y + 21}" font-size="15" font-weight="bold" fill="#111111">{value} / 100</text>')
    out.append("</svg>")
    return "\n".join(out)


def table(headers, rows):
    head = "".join(f"<th scope=\"col\">{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def change_in_words(runs):
    if not runs:
        return "No runs have been saved yet."
    if len(runs) == 1:
        return "This is the first run, so there is no earlier run to compare with. It is the baseline."
    latest, previous = runs[-1], runs[-2]
    diff = to_int(latest.get("overall")) - to_int(previous.get("overall"))
    if diff > 0:
        lead = f"The overall score went up {diff} points since run {previous.get('run')}."
    elif diff < 0:
        lead = f"The overall score went down {-diff} points since run {previous.get('run')}."
    else:
        lead = f"The overall score did not change since run {previous.get('run')}."
    parts = []
    for key, label in FRAMEWORKS:
        delta = to_int(latest.get("scores", {}).get(key)) - to_int(previous.get("scores", {}).get(key))
        if delta:
            parts.append(f"{label} {'+' if delta > 0 else ''}{delta}")
    detail = (" By framework: " + ", ".join(parts) + ".") if parts else ""
    reason = latest.get("what_changed", "")
    return lead + detail + (" Reason given: " + reason if reason else "")


def build():
    project = read_header(ROOT / "project.md")
    history_path = ROOT / "history.json"
    runs = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
    indicators = read_indicators(ROOT / "indicators.csv")
    actions = read_actions(ROOT / "actions.md")
    log = read_action_log(ROOT / "action-log.yaml")
    latest = runs[-1] if runs else {}

    counts = {status: 0 for status in STATUSES}
    for entry in log:
        status = entry.get("status", "open")
        counts[status] = counts.get(status, 0) + 1

    chart1 = line_chart("c1", "Overall score by date", indicators, [
        {"key": "overall", "label": "Overall score (0 to 100)", "color": BLUE, "marker": "circle", "dash": False, "ymax": 100, "side": "left"},
    ])
    evidence_max = max([5] + [to_int(r.get("evidence_count")) for r in indicators])
    evidence_max = ((evidence_max + 3) // 4) * 4
    chart2 = line_chart("c2", "Evidence count and action completion by date", indicators, [
        {"key": "action_completion_pct", "label": "Action completion % (left axis)", "color": BLUE, "marker": "circle", "dash": False, "ymax": 100, "side": "left"},
        {"key": "evidence_count", "label": "Evidence count (right axis)", "color": ORANGE, "marker": "square", "dash": True, "ymax": evidence_max, "side": "right"},
    ])
    chart3 = bar_chart("c3", "Score for each framework in the latest run", latest.get("scores", {}))

    risks = latest.get("top_risks", [])[:3]
    risks_html = "".join(f"<li>{esc(r)}</li>" for r in risks) or "<li>No risks recorded yet.</li>"
    next_html = "".join(f"<li><strong>{esc(a['id'])}</strong>: {esc(a['what'])}</li>" for a in actions[:5]) or "<li>No actions yet.</li>"
    counts_html = "".join(f"<li><strong>{counts.get(s, 0)}</strong> {esc(s)}</li>" for s in STATUSES)
    log_rows = []
    for entry in log:
        note = entry.get("how") or entry.get("why_not") or "No answer recorded yet"
        log_rows.append([entry.get("id", ""), entry.get("text", ""), entry.get("status", "open"), note])
    run_rows = [[r.get("run", ""), r.get("date", ""), r.get("trigger", ""), r.get("overall", ""),
                 r.get("evidence_count", ""), r.get("what_changed", "")] for r in runs]

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(project.get('name', 'Project'))}: validation dashboard</title>
<style>
  body {{ margin: 0; background: #ffffff; color: #111111; font-family: Arial, Helvetica, sans-serif; line-height: 1.5; }}
  main {{ max-width: 900px; margin: 0 auto; padding: 24px 16px 48px; }}
  h1 {{ font-size: 1.8rem; margin: 0 0 8px; }}
  h2 {{ font-size: 1.3rem; margin: 36px 0 10px; border-bottom: 2px solid #111111; padding-bottom: 4px; }}
  .label {{ display: inline-block; background: #111111; color: #ffffff; padding: 3px 10px; font-weight: bold; font-size: 0.9rem; }}
  .score {{ font-size: 4rem; font-weight: bold; color: {BLUE}; line-height: 1; margin: 8px 0; }}
  .box {{ border: 2px solid #111111; padding: 16px; margin: 12px 0; }}
  svg {{ width: 100%; height: auto; display: block; border: 1px solid #767676; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 0.95rem; }}
  th, td {{ border: 1px solid #767676; padding: 6px 8px; text-align: left; vertical-align: top; }}
  th {{ background: #eeeeee; }}
  .wrap {{ overflow-x: auto; }}
  ul.counts {{ list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 8px; }}
  ul.counts li {{ border: 2px solid #111111; padding: 6px 12px; }}
</style>
</head>
<body>
<main>
<h1>{esc(project.get('name', 'Project'))}</h1>
<p><strong>Big idea:</strong> {esc(project.get('big_idea', ''))}</p>
<p>Owner: {esc(project.get('owner', ''))} · Stage: {esc(project.get('stage', ''))} · Project file updated: {esc(project.get('updated', ''))}</p>

<div class="box">
<p class="label">AI-assisted estimate</p>
<p>Overall score, run {esc(latest.get('run', '-'))} ({esc(latest.get('date', '-'))})</p>
<p class="score">{esc(latest.get('overall', '-'))} <span style="font-size:1.5rem;color:#111111">/ 100</span></p>
<p>Evidence count (real conversations or tests): <strong>{esc(latest.get('evidence_count', '-'))}</strong> ·
Open risks: <strong>{esc(latest.get('open_risks', '-'))}</strong> ·
Decisions changed: <strong>{esc(latest.get('decisions_changed', '-'))}</strong></p>
<p>Every score on this page is an AI-assisted estimate, not a measurement.</p>
</div>

<h2>Change since the previous run</h2>
<p>{esc(change_in_words(runs))}</p>

<h2>Overall score by date</h2>
{chart1}
<div class="wrap">{table(["Date", "Run", "Trigger", "Overall"], [[r["date"], r["run"], r["trigger"], r["overall"]] for r in indicators])}</div>

<h2>Evidence count and action completion by date</h2>
{chart2}
<div class="wrap">{table(["Date", "Run", "Evidence count", "Action completion %", "Actions done", "Actions total"], [[r["date"], r["run"], r["evidence_count"], r["action_completion_pct"], r["actions_done"], r["actions_total"]] for r in indicators])}</div>

<h2>Framework scores, latest run</h2>
{chart3}
<div class="wrap">{table(["Framework", "Score (AI-assisted estimate)"], [[label, latest.get("scores", {}).get(key, "-")] for key, label in FRAMEWORKS])}</div>

<h2>Top 3 risks</h2>
<ol>{risks_html}</ol>

<h2>Next 5 actions</h2>
<ol>{next_html}</ol>

<h2>Action status</h2>
<ul class="counts">{counts_html}</ul>
<div class="wrap">{table(["Id", "Action", "Status", "How, or why not"], log_rows)}</div>

<h2>All runs</h2>
<div class="wrap">{table(["Run", "Date", "Trigger", "Overall", "Evidence count", "What changed"], run_rows)}</div>

<p><span class="label">AI-assisted estimate</span> Scores come from the idea-validator skill and rubric.md. A score may only rise when there is new evidence or a changed decision.</p>
</main>
</body>
</html>
"""
    out_dir = ROOT / "dashboard"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"Wrote {out_dir / 'index.html'} ({len(runs)} run(s), {len(indicators)} indicator row(s), {len(log)} action(s))")


if __name__ == "__main__":
    build()
