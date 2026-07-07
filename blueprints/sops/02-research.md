# SOP 02 — Research

**Goal:** Assemble sourced evidence so the draft contains zero fabricated facts.

**Owner:** Architect, using research equipment.

## Steps

1. **Authority research** — run `/blog brief <topic>` (or spawn the `blog-researcher` agent) to
   gather current statistics, competitor angles, and SERP gaps. Demand **Tier 1–3 sources only**
   (Tier 1: primary research/official data; Tier 2: major publications; Tier 3: reputable
   industry sources). Reject content mills / affiliate pages.
2. **Recency lens (optional but recommended)** — run
   `equipment/.venv/bin/python equipment/scripts/discourse_research.py` for what practitioners
   said in the last 30 days (contrarian takes, fresh specifics).
3. **Capture every stat with its source** — each claim needs: the number, the named publisher +
   title, the URL, and the year. This is the "evidence triple" enforced at draft time.
4. **Write the research packet** to `research/<slug>.md` with sections:
   - Key statistics (with full citations)
   - Competitor gaps / what's missing in the current SERP
   - Suggested angle confirmation
   - Image / chart ideas
   - FAQ candidate questions (for GEO/schema)
5. **Update** `architect/topic-queue.md` status → `researched`; note source count in the
   decision log.

## Output
- `research/<slug>.md` (the evidence packet the writer consumes)

## Done when
≥5 Tier 1–3 sourced data points and a confirmed angle exist.

## Quality gate
- Zero uncited claims in the packet.
- No Tier 4–5 sources.
- At least 3 FAQ candidate questions captured (feeds GEO + schema downstream).
