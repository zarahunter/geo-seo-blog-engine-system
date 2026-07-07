#!/usr/bin/env python3
"""The topical-authority flywheel: pillars + internal linking (Phase C.5 WS3 / Phase D).

Single-post production (SOP 07) makes pages. THIS turns a pile of pages into a
LINKED, authoritative cluster - the "rest of the circle" a mature blog runs:

  1. Hub-and-spoke map per cluster (from the keyword universe + what's published).
  2. Pillar-building strategy: the spokes-then-pillar cluster-maturity trigger -
     a cluster earns its pillar once >= `pillar_after_spokes` spokes are live.
  3. Internal-link plan: every post should link UP to its pillar and ACROSS to a
     few sibling spokes; orphans (no inbound links) get surfaced.
  4. Outbound-authority check: every post needs >= N external Tier 1-3 links.
  5. `--apply` maintains a "## Related guides" block in each published post with
     the internal links that can be made now (target also published). No prose
     is mangled; only the Related block is (re)written.

External links (backlinks, brand mentions) are the OTHER half of the circle -
they are earned externally by a human, so this engine only reports
outbound-authority hygiene and leaves inbound link-building to the humans.

Usage:
  equipment/.venv/bin/python autopilot/link_engine.py report
  equipment/.venv/bin/python autopilot/link_engine.py apply     # inject Related blocks
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "autopilot" / "config.yaml"
POSTS = ROOT / "posts"
QUEUE = ROOT / "architect" / "topic-queue.md"
UNIVERSE = ROOT / "architect" / "research" / "keyword-universe.csv"

RELATED_START = "<!-- related:start -->"
RELATED_END = "<!-- related:end -->"


def cfg() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    meta: dict[str, str] = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def published_slugs() -> set[str]:
    out = set()
    if QUEUE.exists():
        for ln in QUEUE.read_text(encoding="utf-8").splitlines():
            c = [x.strip() for x in ln.split("|")]
            if len(c) >= 8 and c[5] == "published" and c[1] not in ("Slug", ""):
                out.add(c[1])
    return out


def load_universe() -> dict[str, dict]:
    """slug -> {cluster, format, status, title(query)} from the keyword universe."""
    rows: dict[str, dict] = {}
    if UNIVERSE.exists():
        for r in csv.DictReader(UNIVERSE.open(encoding="utf-8")):
            slug = (r.get("slug") or "").strip()
            if slug:
                rows[slug] = {"cluster": (r.get("cluster") or "uncategorized").strip(),
                              "format": (r.get("format") or "").strip(),
                              "status": (r.get("status") or "").strip(),
                              "title": (r.get("query") or "").strip()}
    return rows


def post_links(slug: str, own_domain: str) -> tuple[set[str], int]:
    """Return (internal target slugs, outbound external link count) for a published post."""
    p = POSTS / f"{slug}.md"
    if not p.exists():
        return set(), 0
    text = p.read_text(encoding="utf-8")
    internal = set(re.findall(r"\]\(/posts/([a-z0-9-]+)/?\)", text))
    ext = [u for u in re.findall(r"\]\((https?://[^)]+)\)", text) if own_domain not in u]
    return internal, len(ext)


def build_clusters(universe: dict, pub: set[str]) -> dict[str, dict]:
    clusters: dict[str, dict] = {}
    for slug, info in universe.items():
        c = clusters.setdefault(info["cluster"], {"pillar": None, "spokes": [], "members": []})
        c["members"].append(slug)
        if info["format"] == "pillar-page":
            c["pillar"] = slug
        else:
            c["spokes"].append(slug)
    for c in clusters.values():
        c["published_spokes"] = [s for s in c["spokes"] if s in pub]
        c["pillar_published"] = bool(c["pillar"] and c["pillar"] in pub)
    return clusters


def report(apply: bool = False) -> int:
    c = cfg()
    lk = c.get("linking", {})
    own = lk.get("own_domain", "example.com")
    thresh = lk.get("pillar_after_spokes", 4)
    want_links = lk.get("internal_links_per_post", 3)
    min_out = lk.get("min_outbound_authority", 2)

    universe = load_universe()
    pub = published_slugs()
    clusters = build_clusters(universe, pub)
    # published posts not in the universe (e.g. off-niche legacy) -> uncategorized
    for slug in pub:
        if slug not in universe:
            clusters.setdefault("uncategorized", {"pillar": None, "spokes": [], "members": [],
                                                  "published_spokes": [], "pillar_published": False})
            if slug not in clusters["uncategorized"]["members"]:
                clusters["uncategorized"]["members"].append(slug)
                clusters["uncategorized"]["published_spokes"].append(slug)

    print("=" * 72)
    print("1) HUB-AND-SPOKE MAP  (cluster: published_spokes/total_spokes, pillar)")
    print("=" * 72)
    for name, cl in sorted(clusters.items()):
        pil = cl.get("pillar")
        pil_str = (f"pillar={pil} " + ("LIVE" if cl.get("pillar_published") else "planned")) \
            if pil else "pillar=MISSING"
        print(f"  {name:22} {len(cl.get('published_spokes',[]))}/{len(cl.get('spokes',[])):<2} live   {pil_str}")

    print()
    print("=" * 72)
    print(f"2) PILLAR-BUILDING QUEUE  (cluster-maturity trigger: >= {thresh} live spokes)")
    print("=" * 72)
    any_pillar = False
    for name, cl in sorted(clusters.items()):
        nlive = len(cl.get("published_spokes", []))
        if name == "uncategorized":
            continue
        if cl.get("pillar") and not cl.get("pillar_published") and nlive >= thresh:
            any_pillar = True
            print(f"  WRITE PILLAR  [{name}] -> {cl['pillar']}  ({nlive} spokes live, ready)")
        elif not cl.get("pillar") and nlive >= 1:
            any_pillar = True
            print(f"  GAP: no pillar row for [{name}] ({nlive} live). Add a pillar-page keyword; "
                  f"it triggers at {thresh} live spokes (now {nlive}/{thresh}).")
        elif cl.get("pillar") and not cl.get("pillar_published"):
            print(f"  wait  [{name}] pillar '{cl['pillar']}' triggers at {thresh} spokes ({nlive}/{thresh})")
    if not any_pillar:
        print("  (nothing to do)")

    print()
    print("=" * 72)
    print(f"3) INTERNAL-LINK PLAN  (each post: up->pillar + {want_links} siblings)")
    print("=" * 72)
    inbound: dict[str, int] = {s: 0 for s in pub}
    plans: dict[str, list[str]] = {}
    for slug in sorted(pub):
        info = universe.get(slug)
        cl = clusters.get(info["cluster"]) if info else clusters.get("uncategorized")
        targets: list[str] = []
        if cl:
            if cl.get("pillar") and cl["pillar"] != slug:
                targets.append(cl["pillar"])
            for s in cl.get("spokes", []):
                if s != slug and len(targets) < want_links + 1:
                    targets.append(s)
        have, out_ct = post_links(slug, own)
        live_targets = [t for t in targets if t in pub]
        pending = [t for t in targets if t not in pub]
        for t in live_targets:
            inbound[t] = inbound.get(t, 0) + 1
        plans[slug] = live_targets
        print(f"  {slug}")
        print(f"      cluster={info['cluster'] if info else 'uncategorized'}  "
              f"outbound-authority={out_ct} ({'OK' if out_ct >= min_out else 'LOW <'+str(min_out)})")
        print(f"      internal now: {sorted(have) or '(none)'}")
        if live_targets:
            print(f"      + can link now: {live_targets}")
        if pending:
            print(f"      . pending (targets not yet published): {pending}")

    print()
    print("=" * 72)
    print("4) ORPHANS  (published posts with 0 inbound internal links)")
    print("=" * 72)
    orphans = [s for s in pub if inbound.get(s, 0) == 0]
    print("  " + (", ".join(sorted(orphans)) if orphans else "(none)"))

    if apply:
        print()
        print("=" * 72)
        print("5) APPLYING  (writing/refreshing the '## Related guides' block)")
        print("=" * 72)
        n_written = 0
        for slug, live_targets in plans.items():
            if not live_targets:
                continue
            if inject_related(slug, live_targets, universe):
                n_written += 1
                print(f"  updated Related block in posts/{slug}.md -> {live_targets}")
        if n_written == 0:
            print("  0 posts updated (no live internal targets yet - corpus too thin). "
                  "This is expected until sibling spokes publish.")
    return 0


def inject_related(slug: str, targets: list[str], universe: dict) -> bool:
    p = POSTS / f"{slug}.md"
    text = p.read_text(encoding="utf-8")
    items = []
    for t in targets:
        title = universe.get(t, {}).get("title", t.replace("-", " "))
        items.append(f"- [{title}](/posts/{t}/)")
    block = (RELATED_START + "\n## Related guides\n\n" + "\n".join(items) + "\n" + RELATED_END)
    if RELATED_START in text:
        new = re.sub(re.escape(RELATED_START) + r".*?" + re.escape(RELATED_END), block, text, flags=re.S)
    else:
        new = text.rstrip() + "\n\n" + block + "\n"
    if new != text:
        p.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Pillars + internal-linking flywheel.")
    sub = ap.add_subparsers(dest="command")
    sub.add_parser("report").set_defaults(apply=False)
    sub.add_parser("apply").set_defaults(apply=True)
    args = ap.parse_args()
    if not getattr(args, "command", None):
        ap.print_help()
        return 1
    return report(apply=args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
