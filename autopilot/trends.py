#!/usr/bin/env python3
"""Enrich mined candidates with a REAL demand + momentum signal from Google Trends.

Free, no account, automatable (pytrends). Two honest limitations, both handled:
  1. Trends is relative, not absolute volume. We anchor every batch on a fixed
     term ("ai agents") so cross-batch scores are comparable, and express demand
     as "fraction of the anchor's popularity".
  2. Trends has little/no data for niche long-tails. When a query returns no real
     signal we LEAVE THE FIELDS BLANK (the scorer then falls back to the estimate)
     rather than wrongly scoring a winnable long-tail as zero demand.

Writes two columns: demand_real (0-1) and momentum_real (0-1, from the 12-mo slope).

Usage: python autopilot/trends.py --in <candidates.csv> --out <enriched.csv> [--geo US]
"""
from __future__ import annotations

import argparse
import csv
import sys
import time

ANCHOR = "ai agents"        # in every batch; must have stable, non-trivial interest
BATCH = 4                   # queries per batch (5th slot is the anchor)
SLEEP = 2.0                 # seconds between batches (avoid 429s)


def _slope_momentum(series) -> float | None:
    """0-1 momentum from the 12-mo series: recent half vs earlier half."""
    vals = [v for v in series if v is not None]
    if len(vals) < 8 or sum(vals) == 0:
        return None
    half = len(vals) // 2
    early = sum(vals[:half]) / half or 1e-9
    recent = sum(vals[half:]) / (len(vals) - half)
    ratio = recent / early
    return max(0.0, min(1.0, ratio / 2.0))   # ratio 2.0 -> 1.0, 1.0 -> 0.5


def enrich(rows: list[dict], geo: str) -> tuple[list[dict], int]:
    from pytrends.request import TrendReq
    # NB: do NOT pass retries/backoff_factor here — they break against urllib3 2.x
    # (TypeError on build_payload). Plain init works; we handle retries via SLEEP.
    pt = TrendReq(hl="en-US", tz=0)

    queries = [r["query"] for r in rows]
    got = 0
    for i in range(0, len(queries), BATCH):
        batch = queries[i:i + BATCH]
        kw = [ANCHOR] + batch
        try:
            pt.build_payload(kw, timeframe="today 12-m", geo=geo)
            df = pt.interest_over_time()
        except Exception as e:
            print(f"[trends] batch {i//BATCH} failed ({type(e).__name__}); leaving blank", file=sys.stderr)
            time.sleep(SLEEP)
            continue
        if df is None or df.empty or ANCHOR not in df.columns:
            time.sleep(SLEEP)
            continue
        anchor_mean = df[ANCHOR].mean() or 0.0
        for q in batch:
            r = next(x for x in rows if x["query"] == q)
            if q not in df.columns or anchor_mean <= 0:
                continue
            raw = df[q].mean()
            if raw <= 0:                       # no real Trends data for this long-tail
                continue
            # demand as fraction of the anchor: as popular as anchor -> 0.5, 2x -> 1.0
            r["demand_real"] = round(min(1.0, (raw / anchor_mean) * 0.5), 3)
            mom = _slope_momentum(list(df[q]))
            if mom is not None:
                r["momentum_real"] = round(mom, 3)
            got += 1
        time.sleep(SLEEP)
    return rows, got


def main() -> int:
    ap = argparse.ArgumentParser(description="Enrich candidates with real Google Trends demand/momentum.")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--geo", default="US")
    args = ap.parse_args()

    with open(args.inp, newline="", encoding="utf-8") as f:
        rows = [dict(r) for r in csv.DictReader(f)]
    for r in rows:
        r.setdefault("demand_real", "")
        r.setdefault("momentum_real", "")

    rows, got = enrich(rows, args.geo)

    cols = list(rows[0].keys())
    for extra in ("demand_real", "momentum_real"):
        if extra not in cols:
            cols.append(extra)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"[trends] real demand signal for {got}/{len(rows)} queries "
          f"(rest fall back to estimates); wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
