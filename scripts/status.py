#!/usr/bin/env python3
"""Render the OpenFAT front page's project status: profile/status-{light,dark}.svg and the
table between the status markers in profile/README.md. Stdlib only; GH_TOKEN raises the rate limit.

Per public repo it reads the issues (closed vs open, leaving out the "[PR] …" and "(deleted)"
placeholders the migration created) and GitHub's weekly commit counts for the last 26 weeks.
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ORG = "OpenFAT"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEEKS = 26

# Stage order follows a design's path; a public repo missing here lands in "Other".
# (stage, repo, main CI workflow file or None)
REPOS = [
    ("Start a project", "AMTemplate", "ci.yaml"),
    ("Schematic", "Schemify", "ci.yml"),
    ("Schematic", "Interoperate", "ci.yml"),
    ("Schematic", "cktImg", "ci.yml"),
    ("Schematic", "PDK-Manager", "ci.yml"),
    ("Schematic", "GmId-Visualizer", "ci.yml"),
    ("Schematic", "Schemify-Themes", "gate.yaml"),
    ("Simulation", "EGSpice", "test.yml"),
    ("Simulation", "VerA", "test.yaml"),
    ("Simulation", "SpiceRack", "test.yaml"),
    ("Layout", "Philis", "ci.yml"),
    ("Verification", "GPurify", "test.yml"),
    ("Verification", "VAMS-Conformance-Suite", "conformance.yml"),
]

# Ordinal blue pair validated with the dataviz validator (closed > open) on GitHub's surfaces.
THEMES = {
    "light": dict(text="#1f2328", text2="#59636e", muted="#818b98", grid="#d1d9e0",
                  closed="#2a78d6", open="#86b6ef", line="#2a78d6"),
    "dark": dict(text="#f0f6fc", text2="#9198a1", muted="#656c76", grid="#30363d",
                 closed="#3987e5", open="#184f95", line="#3987e5"),
}
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"


def api(path, tries=10):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GH_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GH_TOKEN']}")
    for _ in range(tries):
        try:
            with urllib.request.urlopen(req) as r:
                if r.status == 202:  # stats are being computed; ask again
                    time.sleep(3)
                    continue
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise
    return None


def issues(repo):
    closed = open_ = 0
    for page in range(1, 50):
        batch = api(f"repos/{ORG}/{repo}/issues?state=all&per_page=100&page={page}") or []
        for i in batch:
            if "pull_request" in i or i["title"].startswith("[PR] ") or i["title"] == "(deleted)":
                continue
            closed += i["state"] == "closed"
            open_ += i["state"] == "open"
        if len(batch) < 100:
            return closed, open_
    sys.exit(f"{repo}: more issues than this script pages through")


def commits(repo):
    weeks = api(f"repos/{ORG}/{repo}/stats/commit_activity") or []
    return [w["total"] for w in weeks][-WEEKS:] or [0] * WEEKS


def collect():
    public = {r["name"]: r for r in api(f"orgs/{ORG}/repos?type=public&per_page=100") if not r["archived"]}
    order = [(s, r, ci) for s, r, ci in REPOS if r in public]
    order += [("Other", r, None) for r in sorted(public) if r not in {x[1] for x in REPOS} and r != ".github"]
    rows = []
    for stage, repo, ci in order:
        rel = api(f"repos/{ORG}/{repo}/releases/latest")
        rows.append(dict(stage=stage, repo=repo, ci=ci, desc=public[repo]["description"] or "",
                         issues=issues(repo), weeks=commits(repo), release=rel and rel["tag_name"]))
    return rows


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(rows, t, today):
    W, X_BAR, W_BAR, X_SPARK, W_SPARK, ROW, HEAD = 920, 210, 250, 600, 220, 30, 26
    stages = list(dict.fromkeys(r["stage"] for r in rows))
    H = 104 + len(rows) * ROW + len(stages) * HEAD + 16
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="{FONT}" role="img" aria-labelledby="t d">',
         '<title id="t">OpenFAT project status</title>',
         f'<desc id="d">Per project: issues closed and still open, and commits per week over the last {WEEKS} weeks. '
         f'The table below the chart has the same projects. Updated {today}.</desc>',
         f'<text x="0" y="22" font-size="18" font-weight="600" fill="{t["text"]}">Project status</text>',
         f'<text x="0" y="44" font-size="12" fill="{t["text2"]}">Issues closed so far, and commits per week '
         f'over the last {WEEKS} weeks (each row on its own scale). Updated {today}.</text>']
    # legend for the two bar segments
    o += [f'<rect x="{X_BAR}" y="66" width="10" height="10" rx="2" fill="{t["closed"]}"/>',
          f'<text x="{X_BAR + 15}" y="75" font-size="12" fill="{t["text2"]}">closed</text>',
          f'<rect x="{X_BAR + 70}" y="66" width="10" height="10" rx="2" fill="{t["open"]}"/>',
          f'<text x="{X_BAR + 85}" y="75" font-size="12" fill="{t["text2"]}">open</text>',
          f'<text x="{X_SPARK}" y="75" font-size="12" fill="{t["text2"]}">commits per week · total</text>']
    y = 96
    for stage in stages:
        y += HEAD
        o.append(f'<text x="0" y="{y - 8}" font-size="11" font-weight="600" letter-spacing="0.06em" '
                 f'fill="{t["muted"]}">{esc(stage.upper())}</text>')
        o.append(f'<line x1="0" y1="{y - 3}" x2="{W}" y2="{y - 3}" stroke="{t["grid"]}" stroke-width="1"/>')
        for r in (r for r in rows if r["stage"] == stage):
            mid = y + ROW / 2
            o.append(f'<text x="0" y="{mid + 4}" font-size="13" font-weight="500" fill="{t["text"]}">{esc(r["repo"])}</text>')
            closed, open_ = r["issues"]
            total = closed + open_
            if total:
                wc = round(W_BAR * closed / total)
                gap = 2 if closed and open_ else 0
                if closed:
                    o.append(f'<rect x="{X_BAR}" y="{mid - 5}" width="{max(wc - gap, 2)}" height="10" rx="3" fill="{t["closed"]}"/>')
                if open_:
                    o.append(f'<rect x="{X_BAR + wc}" y="{mid - 5}" width="{max(W_BAR - wc, 2)}" height="10" rx="3" fill="{t["open"]}"/>')
                label = f'{round(100 * closed / total)}% closed · {open_} open'
                o.append(f'<text x="{X_BAR + W_BAR + 10}" y="{mid + 4}" font-size="12" fill="{t["text2"]}" '
                         f'style="font-variant-numeric:tabular-nums">{label}</text>')
            else:
                o.append(f'<text x="{X_BAR}" y="{mid + 4}" font-size="12" fill="{t["muted"]}">no issues yet</text>')
            weeks = r["weeks"]
            peak = max(weeks) or 1
            base = mid + 10
            pts = " ".join(f'{X_SPARK + i * W_SPARK / (len(weeks) - 1):.1f},{base - 20 * c / peak:.1f}' for i, c in enumerate(weeks))
            o.append(f'<line x1="{X_SPARK}" y1="{base}" x2="{X_SPARK + W_SPARK}" y2="{base}" stroke="{t["grid"]}" stroke-width="1"/>')
            o.append(f'<polyline points="{pts}" fill="none" stroke="{t["line"]}" stroke-width="2" '
                     'stroke-linejoin="round" stroke-linecap="round"/>')
            n = sum(weeks)
            o.append(f'<text x="{X_SPARK + W_SPARK + 10}" y="{mid + 4}" font-size="12" fill="{t["text2"]}" '
                     f'style="font-variant-numeric:tabular-nums">{n:,} commit{"s" * (n != 1)}</text>')
            y += ROW
    o.append("</svg>")
    return "\n".join(o) + "\n"


def table(rows):
    out = ["| Stage | Project | What it does | Status |", "|---|---|---|---|"]
    for r in rows:
        url = f"https://github.com/{ORG}/{r['repo']}"
        badges = []
        if r["ci"]:
            badges.append(f"[![CI]({url}/actions/workflows/{r['ci']}/badge.svg)]({url}/actions/workflows/{r['ci']})")
        if r["release"]:
            badges.append(f"[![release](https://img.shields.io/github/v/release/{ORG}/{r['repo']}?label=release)]({url}/releases/latest)")
        badges.append(f"![last commit](https://img.shields.io/github/last-commit/{ORG}/{r['repo']}?label=last%20commit)")
        out.append(f"| {r['stage']} | [{r['repo']}]({url}) | {r['desc'].replace('|', '/')} | {' '.join(badges)} |")
    return "\n".join(out)


def main():
    rows = collect()
    today = datetime.date.today().isoformat()
    for mode, t in THEMES.items():
        with open(os.path.join(ROOT, "profile", f"status-{mode}.svg"), "w") as f:
            f.write(svg(rows, t, today))
    readme = os.path.join(ROOT, "profile", "README.md")
    text = open(readme).read()
    block = ("<!-- status:start -->\n<picture>\n"
             '  <source media="(prefers-color-scheme: dark)" srcset="status-dark.svg">\n'
             '  <img src="status-light.svg" alt="Project status: issues closed and open, and commits per week, '
             'for each OpenFAT project. The table below lists the same projects.">\n'
             f"</picture>\n\n{table(rows)}\n<!-- status:end -->")
    text, n = re.subn(r"<!-- status:start -->.*?<!-- status:end -->", lambda _: block, text, flags=re.S)
    assert n == 1, "profile/README.md needs one status:start/status:end block"
    open(readme, "w").write(text)
    print(f"{len(rows)} projects rendered")


if __name__ == "__main__":
    main()
