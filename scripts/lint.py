"""WikiBrain LINT - no API key needed.

Scans every .md file in the vault (skipping hidden folders such as .git,
.obsidian and .github) and writes lint-report.md with three checks from
AGENTS.md:

  1. Broken [[wikilinks]]  - links that match no note name, alias, or file
  2. Orphan notes          - wiki/ pages that no other note links to
  3. Missing frontmatter   - wiki/ pages with no YAML block, or missing the
                             keys AGENTS.md requires for their page type

Wikilinks inside inline code spans and fenced code blocks are ignored.
The report has no timestamp, so it only changes when the results change.
"""
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "lint-report.md"

# index.md and log.md link to every page by design. Their links are still
# checked for breakage, but they don't count as inbound links, or no page
# could ever be an orphan.
CATALOG_NOTES = {"index.md", "log.md"}

# Frontmatter keys AGENTS.md requires, by page type.
COMMON_KEYS = ["type", "tags", "created", "updated"]
TYPE_KEYS = {
    "source": ["source_url", "source_format", "author", "ingested", "status"],
    "entity": ["entity_kind", "aliases", "source_count"],
    "concept": ["aliases", "source_count"],
    "synthesis": [],  # hub / Map-of-Content pages; no extra keys defined
}

FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?(?:^[ \t]*\1[^\n]*$|\Z)", re.M | re.S)
INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\n[ \t]*\n).)+?\1", re.S)
WIKILINK_RE = re.compile(r"!?\[\[([^\[\]\n]+?)\]\]")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def is_hidden(path):
    return any(part.startswith(".") for part in path.relative_to(ROOT).parts)


def in_wiki(path):
    return path.relative_to(ROOT).parts[0] == "wiki"


def split_frontmatter(text):
    """Return (frontmatter or None, body). Frontmatter must open on line 1."""
    if not text.startswith("---\n"):
        return None, text
    close = re.search(r"^---[ \t]*$", text[4:], re.M)
    if not close:
        return None, text
    return text[4:4 + close.start()], text[4 + close.end():]


def top_level_keys(fm):
    return set(re.findall(r"^([A-Za-z_][\w-]*)[ \t]*:", fm, re.M))


def field(fm, key):
    m = re.search(rf"^{key}[ \t]*:[ \t]*(.*)$", fm, re.M)
    return m.group(1).strip().strip("\"'") if m else ""


def parse_aliases(fm):
    """Handle both `aliases: [a, b]` and a block list of `- a` lines."""
    m = re.search(r"^aliases[ \t]*:[ \t]*(.*)$", fm, re.M)
    if not m:
        return []
    value = m.group(1).strip()
    if value.startswith("["):
        items = value.strip("[]").split(",")
    elif value:
        items = [value]
    else:
        items = []
        for line in fm[m.end():].split("\n")[1:]:
            item = re.match(r"^[ \t]*-[ \t]+(.*)$", line)
            if not item:
                break
            items.append(item.group(1))
    return [a.strip().strip("\"'") for a in items if a.strip().strip("\"'")]


def extract_links(body):
    body = FENCE_RE.sub("", body)         # drop fenced code blocks
    body = INLINE_CODE_RE.sub("", body)   # drop `inline code`
    return [m.group(1) for m in WIKILINK_RE.finditer(body)]


def link_key(target):
    """[[Folder/Page.md#Heading|Shown text]] -> 'page'."""
    target = target.replace("\\|", "|").split("|")[0].split("#")[0].strip()
    name = target.replace("\\", "/").split("/")[-1].strip()
    if name.lower().endswith(".md"):
        name = name[:-3]
    return name.lower()


def main():
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and not is_hidden(p))
    notes = [p for p in files if p.suffix.lower() == ".md" and p != REPORT]

    parsed = {}
    for p in notes:
        text = p.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
        parsed[p] = split_frontmatter(text)

    # Every name a [[link]] can land on: note names, aliases, attachment files.
    targets = defaultdict(set)
    for p in notes:
        targets[p.stem.lower()].add(p)
        for alias in parse_aliases(parsed[p][0] or ""):
            targets[alias.lower()].add(p)
    for p in files:
        if p.suffix.lower() != ".md":
            targets[p.name.lower()].add(p)

    # Links are read from the body only; Obsidian ignores frontmatter links.
    broken = []
    inbound = defaultdict(set)
    for p in notes:
        for raw in extract_links(parsed[p][1]):
            key = link_key(raw)
            if not key:
                continue  # [[#Heading]] points inside the same note
            hits = targets.get(key)
            if not hits:
                broken.append((rel(p), raw.strip()))
            elif rel(p) not in CATALOG_NOTES:
                for hit in hits - {p}:
                    inbound[hit].add(p)

    wiki_pages = [p for p in notes if in_wiki(p)]
    orphans = [rel(p) for p in wiki_pages if not inbound[p]]

    frontmatter_issues = []
    for p in wiki_pages:
        fm = parsed[p][0]
        if fm is None:
            frontmatter_issues.append((rel(p), "no frontmatter block"))
            continue
        keys = top_level_keys(fm)
        page_type = field(fm, "type")
        if page_type and page_type not in TYPE_KEYS:
            frontmatter_issues.append((rel(p), f"unknown type '{page_type}'"))
        missing = [k for k in COMMON_KEYS + TYPE_KEYS.get(page_type, []) if k not in keys]
        if missing:
            frontmatter_issues.append((rel(p), "missing " + ", ".join(missing)))

    lines = [
        "# WikiBrain LINT report",
        "",
        "Written by `scripts/lint.py` (no API key). Rules come from `AGENTS.md`.",
        f"Scanned {len(notes)} notes, {len(wiki_pages)} of them in `wiki/`. "
        "Wikilinks inside code spans and code blocks are ignored.",
        "",
        "| Check | Severity | Count |",
        "|-------|----------|-------|",
        f"| Notes missing frontmatter | HIGH | {len(frontmatter_issues)} |",
        f"| Broken wikilinks | MEDIUM | {len(broken)} |",
        f"| Orphan notes | MEDIUM | {len(orphans)} |",
        "",
        "## Notes missing frontmatter (HIGH)",
        "",
    ]
    lines += [f"- `{path}`: {problem}" for path, problem in frontmatter_issues] or ["- none"]
    lines += ["", "## Broken wikilinks (MEDIUM)", "",
              "AGENTS.md allows links to pages that don't exist yet as to-do markers, "
              "so this list doubles as your create-next backlog.", ""]
    lines += [f"- `{path}` links to `[[{link}]]`" for path, link in sorted(broken)] or ["- none"]
    lines += ["", "## Orphan notes (MEDIUM)", "",
              "Wiki pages no other note links to (links from index.md and log.md don't count).", ""]
    lines += [f"- `{path}`" for path in orphans] or ["- none"]

    with open(REPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {rel(REPORT)}: {len(frontmatter_issues)} frontmatter issues, "
          f"{len(broken)} broken links, {len(orphans)} orphans.")


if __name__ == "__main__":
    main()
