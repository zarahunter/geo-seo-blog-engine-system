#!/usr/bin/env python3
"""Weekly research sprint: score, dedupe, and promote a keyword/query backlog.

CLAUDE does the creative mining (keyword universe, AI-intent questions, trends)
and drops the candidates into a CSV. THIS script owns the deterministic parts:

  - score every candidate with the config-weighted GEO prioritization formula
  - dedupe by normalized query
  - cannibalization guard vs already-queued/published primary keywords
  - select the top backlog_target respecting the intent-led content-mix ratio
  - promote the winners into architect/topic-queue.md as `intake` rows
  - write the full scored universe to architect/research/keyword-universe.csv

Candidate CSV columns (Claude fills these during mining):
  query,type,intent,cluster,source,demand,saturation,format[,brand_fit,business_value,trend]

Commands:
  schema                      print the candidate CSV header for the miner
  run --candidates <csv> [--backlog N] [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "autopilot" / "config.yaml"
QUEUE = ROOT / "architect" / "topic-queue.md"
RESEARCH = ROOT / "architect" / "research"
UNIVERSE = RESEARCH / "keyword-universe.csv"

CANDIDATE_COLS = ["query", "type", "intent", "cluster", "source", "demand",
                  "saturation", "format", "brand_fit", "business_value", "trend", "serp_difficulty",
                  "demand_real", "momentum_real"]
UNIVERSE_COLS = CANDIDATE_COLS + ["priority_score", "mix_class", "slug", "status"]

# OBSERVED SERP difficulty (from a live SERP audit) overrides the estimated
# saturation when present. real_gap = page-1 owned by tiny blogs/forums;
# saturated = defended by high-authority incumbents (Forbes/Microsoft/etc).
DIFF_TO_LOWSAT = {"real_gap": 1.0, "gap": 1.0, "moderate": 0.5, "saturated": 0.12}

# quickwin mode: when topical authority is still thin, winnability (low saturation)
# matters more than raw demand. Emphasize low_saturation + intent; drop demand.
QUICKWIN_WEIGHTS = {
    "intent_value": 0.22, "ai_citation_surface": 0.18, "demand": 0.05,
    "low_saturation": 0.33, "trend_momentum": 0.05, "brand_fit": 0.07,
    "business_value": 0.10,
}

# format -> content template (blueprints/templates/) and AI-citation surface strength
FORMAT_TEMPLATE = {
    "comparison": "comparison", "faq": "faq-knowledge", "faq-knowledge": "faq-knowledge",
    "how-to": "how-to-guide", "how-to-guide": "how-to-guide", "data-research": "data-research",
    "listicle": "listicle", "roundup": "roundup", "tutorial": "tutorial",
    "pillar": "pillar-page", "pillar-page": "pillar-page", "case-study": "case-study",
    "product-review": "product-review", "news": "news-analysis", "news-analysis": "news-analysis",
    "thought-leadership": "thought-leadership",
}
AI_SURFACE = {
    "comparison": 1.0, "faq-knowledge": 1.0, "data-research": 0.95, "how-to-guide": 0.9,
    "product-review": 0.85, "listicle": 0.85, "roundup": 0.85, "tutorial": 0.8,
    "case-study": 0.7, "pillar-page": 0.75, "news-analysis": 0.6, "thought-leadership": 0.55,
}
INTENT_VALUE = {"transactional": 1.0, "commercial": 0.9, "informational": 0.5, "navigational": 0.3}
LEVEL = {"high": 1.0, "rising": 1.0, "medium": 0.6, "med": 0.6, "steady": 0.5,
         "evergreen": 0.5, "low": 0.3}


def load_config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "-", s).strip("-")[:70] or "post"


def _num(v: str, default: float) -> float:
    try:
        f = float(v)
        return max(0.0, min(1.0, f))
    except (TypeError, ValueError):
        return default


def _level(v: str, default: float) -> float:
    return LEVEL.get((v or "").strip().lower(), default)


def template_of(fmt: str) -> str:
    return FORMAT_TEMPLATE.get((fmt or "").strip().lower(), "how-to-guide")


def factor_scores(row: dict) -> dict:
    fmt_t = template_of(row.get("format", ""))
    intent = (row.get("intent", "") or "").strip().lower()
    return {
        "intent_value": INTENT_VALUE.get(intent, 0.5),
        "ai_citation_surface": AI_SURFACE.get(fmt_t, 0.6),
        # Prefer the REAL Google Trends signal (demand_real) when present, else the estimate.
        "demand": _num(row.get("demand_real", ""), _level(row.get("demand", ""), 0.5)),
        "low_saturation": _level(row.get("saturation", ""), 0.6) if row.get("saturation", "").lower() != "low"
                          else 1.0,
        "trend_momentum": _num(row.get("momentum_real", ""),
                               _num(row.get("trend", ""), _level(row.get("trend", ""), 0.5))),
        "brand_fit": _num(row.get("brand_fit", ""), 0.85),
        "business_value": _num(row.get("business_value", ""),
                               {"transactional": 1.0, "commercial": 0.9}.get(intent, 0.6)),
    }


def _low_sat(row: dict) -> float:
    """Winnability factor. OBSERVED serp_difficulty overrides the estimate."""
    diff = (row.get("serp_difficulty", "") or "").strip().lower().replace(" ", "_")
    if diff in DIFF_TO_LOWSAT:
        return DIFF_TO_LOWSAT[diff]
    sat = (row.get("saturation", "") or "").strip().lower()
    return {"low": 1.0, "medium": 0.6, "med": 0.6, "high": 0.3}.get(sat, 0.6)


def score(row: dict, weights: dict) -> int:
    f = factor_scores(row)
    f["low_saturation"] = _low_sat(row)
    total_w = sum(weights.values()) or 1.0
    s = sum(weights.get(k, 0) * f.get(k, 0) for k in weights) / total_w
    return round(100 * s)


def is_saturated(row: dict) -> bool:
    """Proven-saturated by the SERP audit (a low-odds target; prefer winnable seats)."""
    return (row.get("serp_difficulty", "") or "").strip().lower().replace(" ", "_") == "saturated"


def mix_class(row: dict) -> str:
    intent = (row.get("intent", "") or "").lower()
    fmt = template_of(row.get("format", ""))
    trend = _num(row.get("trend", ""), _level(row.get("trend", ""), 0.0))
    if trend >= 0.9 or (row.get("source", "").lower() in ("trends", "news")):
        return "trend_timely"
    if fmt == "pillar-page" or (row.get("type", "").lower() in ("head", "head-term")):
        return "pillar_volume"
    if intent in ("commercial", "transactional") or fmt in (
            "comparison", "how-to-guide", "product-review", "listicle", "roundup"):
        return "high_intent"
    return "pillar_volume"


def _norm(q: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", "", q.lower())).strip()


def _tokens(q: str) -> set:
    return set(_norm(q).split())


def existing_keywords() -> list[str]:
    """Primary keywords of COMMITTED content (not the replaceable `intake` backlog),
    for the cannibalization guard."""
    out = []
    if QUEUE.exists():
        for ln in QUEUE.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in ln.split("|")]
            if len(cells) >= 8 and cells[1] not in ("Slug", "", "_example-slug_") \
                    and cells[5] not in ("intake", "Status"):
                out.append(cells[3])
    return out


def cannibalizes(query: str, existing: list[str]) -> bool:
    qt = _tokens(query)
    if not qt:
        return False
    for e in existing:
        et = _tokens(e)
        if not et:
            continue
        jac = len(qt & et) / len(qt | et)
        if jac >= 0.7:
            return True
    return False


def select_by_mix(rows: list[dict], target: int, mix: dict) -> list[dict]:
    """Pick `target` rows honoring the content-mix ratio, filling shortfalls by score."""
    buckets: dict[str, list[dict]] = {"high_intent": [], "pillar_volume": [], "trend_timely": []}
    for r in rows:
        buckets[r["mix_class"]].append(r)
    for b in buckets.values():
        b.sort(key=lambda r: r["priority_score"], reverse=True)
    quota = {
        "high_intent": round(target * mix.get("high_intent", 0.6)),
        "pillar_volume": round(target * mix.get("pillar_volume", 0.25)),
        "trend_timely": round(target * mix.get("trend_timely", 0.15)),
    }
    selected: list[dict] = []
    for cls, q in quota.items():
        selected.extend(buckets[cls][:q])
    # Fill any shortfall (or rounding gap) with the best remaining across all buckets.
    chosen = {id(r) for r in selected}
    remaining = sorted((r for r in rows if id(r) not in chosen),
                       key=lambda r: r["priority_score"], reverse=True)
    for r in remaining:
        if len(selected) >= target:
            break
        selected.append(r)
    return sorted(selected, key=lambda r: r["priority_score"], reverse=True)[:target]


def promote(selected: list[dict]) -> None:
    """Replace existing `intake` rows with the freshly-selected backlog (idempotent)."""
    today = date.today().isoformat()
    new_rows = []
    for r in selected:
        topic = r["query"].strip()
        new_rows.append(
            f"| {r['slug']} | {topic} | {r['query'].strip()} | "
            f"{template_of(r.get('format',''))} | intake | — | {today} |"
        )
    # Drop any prior intake rows (un-built backlog from a previous sprint).
    kept = [ln for ln in QUEUE.read_text(encoding="utf-8").splitlines()
            if not (ln.startswith("|") and len(ln.split("|")) >= 8 and ln.split("|")[5].strip() == "intake")]
    text = "\n".join(kept).rstrip("\n")
    marker = "<!-- Add one row per topic."
    if marker in text:
        head, _, tail = text.partition(marker)
        QUEUE.write_text(head.rstrip("\n") + "\n" + "\n".join(new_rows) + "\n\n" + marker + tail,
                         encoding="utf-8")
    else:
        QUEUE.write_text(text + "\n" + "\n".join(new_rows) + "\n", encoding="utf-8")


def cmd_schema(args) -> int:
    print(",".join(CANDIDATE_COLS))
    return 0


def cmd_run(args) -> int:
    cfg = load_config()
    weights = QUICKWIN_WEIGHTS if args.mode == "quickwin" else cfg["scorer_weights"]
    mix = cfg["content_mix"]
    target = args.backlog or cfg["cadence"]["backlog_target"]

    with open(args.candidates, newline="", encoding="utf-8") as f:
        raw = [dict(r) for r in csv.DictReader(f)]
    if not raw:
        print("no candidates", file=sys.stderr)
        return 1

    # Dedupe by normalized query, keep first occurrence.
    seen, deduped = set(), []
    for r in raw:
        k = _norm(r.get("query", ""))
        if k and k not in seen:
            seen.add(k)
            deduped.append(r)

    existing = existing_keywords()
    scored = []
    for r in deduped:
        r["priority_score"] = score(r, weights)
        r["mix_class"] = mix_class(r)
        r["slug"] = slugify(r["query"])
        r["status"] = "cannibal" if cannibalizes(r["query"], existing) else "backlog"
        scored.append(r)
    scored.sort(key=lambda r: r["priority_score"], reverse=True)

    eligible = [r for r in scored if r["status"] != "cannibal"]
    if args.mode == "quickwin":
        # Drop proven-saturated traps entirely in quickwin mode.
        eligible = [r for r in eligible if not is_saturated(r)]
    selected = select_by_mix(eligible, target, mix)
    sel_ids = {id(r) for r in selected}
    for r in scored:
        if id(r) in sel_ids:
            r["status"] = "selected"

    # Write the full scored universe (canonical, git).
    RESEARCH.mkdir(parents=True, exist_ok=True)
    with open(UNIVERSE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=UNIVERSE_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(scored)

    print(f"[sprint] {len(raw)} candidates -> {len(deduped)} unique -> "
          f"{len([r for r in scored if r['status']=='cannibal'])} cannibalizing dropped -> "
          f"selected {len(selected)} for the backlog")
    for r in selected:
        print(f"  {r['priority_score']:3}  [{r['mix_class']:12}] {r['query']}  ({template_of(r.get('format',''))})")

    if args.dry_run:
        print("[sprint] --dry-run: universe written, queue NOT modified")
        return 0
    promote(selected)
    print(f"[sprint] promoted {len(selected)} rows into {QUEUE.relative_to(ROOT)}; "
          f"universe -> {UNIVERSE.relative_to(ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Weekly research sprint: score + promote backlog.")
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("schema").set_defaults(func=cmd_schema)
    r = sub.add_parser("run")
    r.add_argument("--candidates", required=True, help="CSV of mined candidates")
    r.add_argument("--backlog", type=int, default=0, help="override backlog_target")
    r.add_argument("--mode", choices=["balanced", "quickwin"], default="balanced",
                   help="quickwin: favor low-saturation/winnable terms, drop proven-saturated")
    r.add_argument("--dry-run", action="store_true")
    r.set_defaults(func=cmd_run)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
