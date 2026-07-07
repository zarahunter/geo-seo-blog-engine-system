#!/usr/bin/env python3
"""Autopilot controller: the deterministic QA-gate + publish + state machine.

Division of labour: CLAUDE (the scheduled routine) does the creative stages
(research/write/optimize/schema/visuals via skills and agents). THIS script owns
the deterministic parts a machine should decide, not a model:

  - score the finished post (analyze_blog.py)
  - hard-rule check (no em/en/-- dashes)
  - apply the tiered safety gate from autopilot/config.yaml
  - PUBLISH (render + inject schema + rebuild site) OR route to the REVIEW QUEUE
    OR flag for another iteration
  - advance the row in architect/topic-queue.md

Commands:
  gate --slug <slug> [--factcheck pass|fail|skip] [--iteration N] [--dry-run]
      Evaluate one finished post and act on the decision.
  next
      Print the next backlog item to build (first `intake`/`researched` row).

Run via the project venv:
  equipment/.venv/bin/python autopilot/run.py gate --slug <slug> --factcheck pass
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable                                  # the venv python running us
POSTS = ROOT / "posts"
PUBLISH_POSTS = ROOT / "publish" / "posts"
QUEUE = ROOT / "architect" / "topic-queue.md"
REVIEW_QUEUE = ROOT / "architect" / "review-queue.md"
CONFIG = Path(os.environ.get("AUTOPILOT_CONFIG", ROOT / "autopilot" / "config.yaml"))
SCRIPTS = ROOT / "equipment" / "scripts"

FORBIDDEN_DASH = re.compile(r"[—–]| -- ")   # em-dash, en-dash, spaced double-hyphen

# First-person / original-artifact markers (mirror analyze_blog.analyze_originality)
FIRST_PERSON = [
    re.compile(r"\bI\s+(?:found|discovered|tested|built|created|noticed|learned|experienced)\b", re.I),
    re.compile(r"\b(?:we|our team)\s+(?:tested|built|ran|analyzed|measured|conducted|found|discovered)\b", re.I),
    re.compile(r"\bin (?:my|our) experience\b", re.I),
    re.compile(r"\bfrom (?:my|our) (?:testing|research|analysis|work)\b", re.I),
]
MD_TABLE = re.compile(r"^\|.+\|\s*$", re.M)


def load_config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))


# --- scoring & hard rules ---------------------------------------------------

def score_post(slug: str) -> dict:
    """Return the analyze_blog score dict ({'total', 'rating', 'categories', ...})."""
    md = POSTS / f"{slug}.md"
    proc = _run([PY, str(SCRIPTS / "analyze_blog.py"), str(md), "--format", "json"])
    if proc.returncode != 0:
        raise RuntimeError(f"analyze_blog failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)["score"]


def dash_violations(slug: str) -> int:
    """Count forbidden dash characters in the post prose (a hard-rule gate)."""
    text = (POSTS / f"{slug}.md").read_text(encoding="utf-8")
    return len(FORBIDDEN_DASH.findall(text))


# --- decision ---------------------------------------------------------------

def decide(score_total: int, factcheck: str, dashes: int, iteration: int, cfg: dict) -> tuple[str, str]:
    """Return (action, reason). action in {publish, review, iterate}."""
    g = cfg["gate"]
    if dashes > 0:
        return "iterate", f"hard-rule: {dashes} forbidden dash char(s) in prose"
    factcheck_clean = factcheck == "pass"
    need_factcheck = g.get("require_factcheck_pass", True)

    if score_total >= g["auto_publish_min_score"] and (factcheck_clean or not need_factcheck):
        return "publish", f"score {score_total} >= {g['auto_publish_min_score']} and factcheck={factcheck}"
    if need_factcheck and not factcheck_clean and score_total >= g["review_queue_min_score"]:
        return "review", f"score {score_total} ok but factcheck={factcheck} (needs a human glance)"
    if score_total >= g["review_queue_min_score"]:
        return "review", f"score {score_total} in review band [{g['review_queue_min_score']},{g['auto_publish_min_score']})"
    # below the floor
    if iteration >= g["max_iterations"]:
        return "review", f"score {score_total} below floor after {iteration} iterations"
    return "iterate", f"score {score_total} < {g['review_queue_min_score']} (iteration {iteration}/{g['max_iterations']})"


# --- queue state ------------------------------------------------------------

def update_queue(slug: str, status: str, score: str) -> None:
    """Rewrite the Status/Score/Updated cells of the slug's row in topic-queue.md."""
    if not QUEUE.exists():
        return
    lines = QUEUE.read_text(encoding="utf-8").splitlines()
    today = date.today().isoformat()
    for i, ln in enumerate(lines):
        cells = [c.strip() for c in ln.split("|")]
        # table row shape: ['', slug, topic, keyword, template, status, score, updated, '']
        if len(cells) >= 8 and cells[1] == slug:
            cells[5] = status
            cells[6] = score
            cells[7] = today
            lines[i] = "| " + " | ".join(cells[1:-1]) + " |"
            break
    QUEUE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_review_queue(slug: str, score: int, reason: str) -> None:
    REVIEW_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    if not REVIEW_QUEUE.exists():
        REVIEW_QUEUE.write_text(
            "# Review Queue\n\n"
            "Posts the autopilot produced that did NOT clear the auto-publish gate. "
            "A human reviews, fixes, and either re-runs the gate or discards.\n\n"
            "| Slug | Score | Reason | Draft | Flagged |\n"
            "|------|-------|--------|-------|---------|\n",
            encoding="utf-8",
        )
    row = f"| {slug} | {score} | {reason} | posts/{slug}.md | {date.today().isoformat()} |\n"
    with REVIEW_QUEUE.open("a", encoding="utf-8") as f:
        f.write(row)


# --- publish ----------------------------------------------------------------

def ensure_hero(slug: str, cfg: dict) -> str:
    """Ensure a hero image exists in the post's publish dir; return its filename."""
    out_dir = PUBLISH_POSTS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(out_dir.glob("hero.*"))
    if existing:
        return existing[0].name
    meta = _frontmatter(slug)
    cmd = [
        PY, str(SCRIPTS / "generate_hero.py"),
        "--topic", meta.get("title", slug), "--tags", meta.get("tags_raw", ""),
        "--out", str(out_dir), "--json",
    ]
    # tools.image_backend: "pollinations" allows the AI-image rung; anything else
    # skips it (AI images bake garbled text into heroes — learned 2026-07-07).
    if cfg.get("tools", {}).get("image_backend") != "pollinations":
        cmd.append("--no-pollinations")
    proc = _run(cmd)
    hero = sorted(out_dir.glob("hero.*"))
    return hero[0].name if hero else "hero.png"


def _frontmatter(slug: str) -> dict:
    text = (POSTS / f"{slug}.md").read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    meta: dict[str, str] = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"').strip("'")
        tm = re.search(r"^tags:\s*\[(.*?)\]", m.group(1), re.MULTILINE)
        if tm:
            meta["tags_raw"] = ",".join(t.strip() for t in tm.group(1).split(","))
    return meta


def publish(slug: str, cfg: dict) -> str:
    """Render + inject full schema + rebuild the site. Returns the live URL."""
    out_dir = PUBLISH_POSTS / slug
    hero = ensure_hero(slug, cfg)
    # 1. render
    proc = _run([
        PY, str(SCRIPTS / "blog_render.py"),
        "--md", str(POSTS / f"{slug}.md"), "--out-dir", str(out_dir),
        "--hero", hero, "--pdf-engine", "none",
    ])
    if proc.returncode != 0:
        raise RuntimeError(f"render failed: {proc.stderr.strip()}")
    # 2. locate rendered html (<slug>.html) and inject full sidecar schema if present
    rendered = out_dir / f"{slug}.html"
    if not rendered.exists():
        cand = [p for p in out_dir.glob("*.html") if p.name != "index.html"]
        rendered = cand[0] if cand else out_dir / "index.html"
    html = rendered.read_text(encoding="utf-8")
    sidecar = POSTS / f"{slug}.schema.json"
    if sidecar.exists():
        schema = json.loads(sidecar.read_text(encoding="utf-8"))
        schema.pop("_publish_note", None)
        blob = json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("\\", "\\\\")
        html, n = re.subn(r'<script type="application/ld\+json">.*?</script>',
                          '<script type="application/ld+json">' + blob + '</script>',
                          html, count=1, flags=re.S)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    if rendered.name != "index.html" and rendered.exists():
        rendered.unlink()
    # 3. rebuild site-level files (index/sitemap/rss/robots/llms) + entity pages
    site = cfg["site"]
    _run([
        PY, str(ROOT / "publish" / "build_index.py"),
        "--site-title", site["title"], "--base-url", site["base_url"],
        "--description", cfg["niche"]["thesis"].strip().replace("\n", " "),
    ])
    # /about, /contact, /privacy + Organization/Person schema (Phase C.5, WS0-C)
    _run([PY, str(ROOT / "publish" / "build_pages.py")])
    # 4. deploy (Phase A: mode 'none' -> skip; git/cli wired later)
    if cfg.get("deploy", {}).get("mode") not in (None, "none", ""):
        print(f"[deploy] mode={cfg['deploy']['mode']} (deploy wiring is Phase C)", file=sys.stderr)
    return site["base_url"].rstrip("/") + f"/posts/{slug}/"


# --- Phase C.5 safety gates -------------------------------------------------

def _published_rows() -> list[list[str]]:
    rows = []
    if QUEUE.exists():
        for ln in QUEUE.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in ln.split("|")]
            if len(cells) >= 8 and cells[1] not in ("Slug", "", "_example-slug_"):
                rows.append(cells)
    return rows


def published_count() -> int:
    """How many posts are already live (drives the launch autonomy ramp)."""
    return sum(1 for c in _published_rows() if c[5] == "published")


def published_keywords(exclude_slug: str) -> list[str]:
    """Primary keywords of already-published posts (cannibalization guard)."""
    return [c[3] for c in _published_rows() if c[5] == "published" and c[1] != exclude_slug]


def effective_autonomy(cfg: dict) -> str:
    """Resolve the autonomy mode, auto-ramping review_all -> full at the threshold."""
    g = cfg["gate"]
    mode = g.get("autonomy", "full")
    thresh = g.get("autonomy_ramp", {}).get("approved_threshold", 0)
    if mode == "review_all" and thresh and published_count() >= thresh:
        return "full"
    return mode


def info_gain_check(slug: str) -> tuple[bool, str]:
    """A post needs a declared `information_gain:` AND a real original artifact
    (first-person analysis, an [ORIGINAL DATA] tag, a table, or an inline chart)."""
    text = (POSTS / f"{slug}.md").read_text(encoding="utf-8")
    declared = _frontmatter(slug).get("information_gain", "").strip()
    if len(declared) < 15:
        return False, "no declared `information_gain` in frontmatter"
    has_artifact = (
        any(rx.search(text) for rx in FIRST_PERSON)
        or "[ORIGINAL DATA]" in text.upper()
        or bool(MD_TABLE.search(text))
        or "<svg" in text
    )
    if not has_artifact:
        return False, "declared info-gain but no original artifact (first-person/table/chart) found"
    return True, "ok"


def internal_link_count(slug: str) -> int:
    """Count contextual internal links (to /posts/... or a relative .md) in the body."""
    text = (POSTS / f"{slug}.md").read_text(encoding="utf-8")
    return len(re.findall(r"\]\((?:/posts/|\.{0,2}/)[^)]+\)", text))


def _tokens(q: str) -> set:
    return set(re.sub(r"[^a-z0-9\s]", "", (q or "").lower()).split())


def cannibal_hit(slug: str) -> str | None:
    """Return a colliding PUBLISHED keyword (Jaccard >= 0.7) or None."""
    fm = _frontmatter(slug)
    kw = fm.get("primary_keyword", fm.get("keyword", "")) or slug.replace("-", " ")
    qt = _tokens(kw)
    if not qt:
        return None
    for e in published_keywords(slug):
        et = _tokens(e)
        if et and len(qt & et) / len(qt | et) >= 0.7:
            return e
    return None


def apply_safety_gates(slug: str, action: str, cfg: dict) -> tuple[str, str]:
    """Downgrade a would-be publish to review when a Phase C.5 gate trips.
    Never upgrades; quality gates first, then the launch autonomy backstop."""
    if action != "publish":
        return action, ""
    g = cfg["gate"]
    if g.get("require_information_gain", False):
        ok, why = info_gain_check(slug)
        if not ok:
            return "review", f"info-gain gate: {why}"
    if g.get("block_cannibalization", False):
        hit = cannibal_hit(slug)
        if hit:
            return "review", f"cannibalization: collides with published '{hit}'"
    min_links = g.get("min_internal_links", 0)
    if min_links:
        n = internal_link_count(slug)
        if n < min_links:
            return "review", f"orphan-out: {n} internal link(s) < required {min_links}"
    mode = effective_autonomy(cfg)
    if mode == "review_all":
        thresh = g.get("autonomy_ramp", {}).get("approved_threshold", 0)
        return "review", f"launch mode: human approval required ({published_count()}/{thresh} published)"
    if mode == "sample":
        n = g.get("autonomy_ramp", {}).get("sample_every", 5) or 5
        if published_count() % n == 0:
            return "review", f"sample check: holding 1-in-{n} for a human glance"
    return "publish", ""


# --- commands ---------------------------------------------------------------

def cmd_gate(args) -> int:
    cfg = load_config()
    slug = args.slug
    if not (POSTS / f"{slug}.md").exists():
        print(f"ERROR: posts/{slug}.md not found", file=sys.stderr)
        return 2
    score = score_post(slug)
    dashes = dash_violations(slug)
    action, reason = decide(score["total"], args.factcheck, dashes, args.iteration, cfg)

    # Phase C.5: a would-be publish still has to clear the info-gain, cannibalization,
    # orphan, and launch-autonomy backstops before it goes live unattended.
    gated_action, gated_reason = apply_safety_gates(slug, action, cfg)
    if gated_action != action:
        action, reason = gated_action, gated_reason

    print(f"[gate] {slug}: score={score['total']} ({score['rating']}) "
          f"factcheck={args.factcheck} dashes={dashes} -> {action.upper()}")
    print(f"[gate] reason: {reason}")

    if args.dry_run:
        print("[gate] --dry-run: no changes made")
        return 0

    if action == "publish":
        url = publish(slug, cfg)
        update_queue(slug, "published", str(score["total"]))
        print(f"[publish] LIVE (locally built): {url}")
        return 0
    if action == "review":
        append_review_queue(slug, score["total"], reason)
        update_queue(slug, "review-queue", str(score["total"]))
        print(f"[review] routed to {REVIEW_QUEUE.relative_to(ROOT)}")
        return 0
    # iterate
    update_queue(slug, "drafted", str(score["total"]))
    print("[iterate] send back to write/optimize (Claude) and re-run the gate")
    return 3


def cmd_next(args) -> int:
    if not QUEUE.exists():
        print("no queue")
        return 1
    for ln in QUEUE.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in ln.split("|")]
        if len(cells) >= 8 and cells[1] not in ("Slug", "", "_example-slug_") and cells[5] in ("intake", "researched", "drafted"):
            print(json.dumps({"slug": cells[1], "topic": cells[2], "keyword": cells[3],
                              "template": cells[4], "status": cells[5]}))
            return 0
    print("{}")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Autopilot QA-gate + publish controller.")
    sub = ap.add_subparsers(dest="command", required=True)

    g = sub.add_parser("gate", help="evaluate one finished post and act")
    g.add_argument("--slug", required=True)
    g.add_argument("--factcheck", choices=["pass", "fail", "skip"], default="skip",
                   help="result of blog-factcheck (run by Claude); 'skip' is treated as not-clean")
    g.add_argument("--iteration", type=int, default=1)
    g.add_argument("--dry-run", action="store_true")
    g.set_defaults(func=cmd_gate)

    n = sub.add_parser("next", help="print the next backlog item to build")
    n.set_defaults(func=cmd_next)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
