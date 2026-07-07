# SOP 07 — The Daily Produce-Loop (autopilot spine)

**Goal:** Turn ONE backlog item into a published (or review-queued) post with no human in the
loop. This is the daily "produce one post" flywheel. It chains the manual 6-stage pipeline
(SOPs 01-06) into a single repeatable sequence and hands the publish/hold decision to
`autopilot/run.py gate` (never to a human's mood, never to the model's opinion).

**Owner:** Architect (Claude), driven by the scheduled routine. Creative stages are Claude's;
the gate/publish decision is deterministic (`run.py`).

---

## The loop (run top to bottom for one slug)

1. **Pick the item.** `equipment/.venv/bin/python autopilot/run.py next` → first
   `intake`/`researched`/`drafted` row. Open/append `architect/decisions/<slug>.md` (copy
   `_TEMPLATE.md`). **Selection is dual-signal:** prefer the topic's `quadrant`
   (🟢 write-first → 🔵 geo-play → 🟡 seo-play → 🔴 defer), which combines SEO `serp_difficulty`
   × GEO `geo_winnability` — see "The intelligence layer" at the end of this SOP.
2. **Research (SOP 02).** Spawn the `blog-researcher` agent. Demand the evidence triple
   (number + named publisher + URL + year), Tier 1-3 only, ≥8 verifiable data points, ≥5 FAQ
   candidates. Save `research/<slug>.md`. **Design rule:** put headline/table numbers
   on FETCHABLE sources; keep bot-blocked primaries (analyst firms, gov portals) in supporting
   prose only (see factcheck note below).
3. **Write (SOP 03).** Load `blueprints/brand/BRAND.md` + `VOICE.md` and the chosen
   `blueprints/templates/<template>.md`. Enforce the 6 pillars + hard rules (no fabricated stats,
   no para >150w, no skipped headings, ≤1 promo, **no em/en/`--` dashes**). Save `posts/<slug>.md`.
   **Required frontmatter field `information_gain:`** — one sentence naming the post's
   original value-add (a table/chart you generated, a first-hand test, a non-obvious synthesis).
   Every post must carry ≥1 real original artifact; pure synthesis of others' sources is not enough.
4. **Optimize (SOP 04).** Write to `on-page-seo` + `ai-seo` standards (answer-first openers,
   kw in title/H1/first-100w/≥1 H2/slug/meta, self-contained FAQ, entities clear, vendor claims
   labelled). Validate with the scorer rather than eyeballing.
5. **Schema (SOP 04C).** Emit `posts/<slug>.schema.json` (@graph: BlogPosting + Person + FAQPage)
   AND inline the SAME schema in `posts/<slug>.md` **as separate flat `<script type="application/ld+json">`
   blocks, one per @type** (NOT a single @graph). See gotcha below.
6. **Factcheck.** Fetch every cited URL and confirm the claimed number appears. For bot-blocked
   primaries (403), corroborate via WebSearch against the same figure. Fix any drift. Record
   `pass` only if every load-bearing claim is fetch-verified or search-corroborated; else `fail`.
7. **Gate + publish (SOP 05+06).**
   `equipment/.venv/bin/python autopilot/run.py gate --slug <slug> --factcheck pass|fail|skip [--iteration N]`
   - score ≥85 AND factcheck pass → publish.
   - 70-84, or any factcheck flag → `architect/review-queue.md`.
   - <70 → iterate (back to step 3/4), max 3, then review-queue.
   Then the **safety gates** run before anything goes live unattended (all in `config.yaml`):
   info-gain gate (`require_information_gain`), cannibalization gate (`block_cannibalization` vs
   published keywords), and orphan-out gate (`min_internal_links`). Any trip routes to the
   review queue. (Optional: set `gate.autonomy` to `sample` or `review_all` if you want a human
   spot-check; the default `full` trusts the gates.)
8. **Images (extends steps 3-5) — every draft is visually complete.**
   - **Hero:** auto via `generate_hero.py` ladder; free tier = Openverse (real CC photos, no key).
     `run.py ensure_hero()` runs this at render. Do NOT embed the hero in the markdown body —
     the renderer injects it (a body embed double-renders it).
   - **Inline photos:** source 1-3 relevant CC/free images during research; embed in-body as
     markdown `![alt](file)` with the assets in `publish/posts/<slug>/`. Keep a `*-credit.txt`
     beside each image (title, creator, licence, source URL).
   - **Optional chart:** an original data SVG doubles as the `information_gain` artifact
     (external `.svg`, explicit colors — see gotchas).
9. **Verify the build.** Open `publish/posts/<slug>/index.html`: assets resolve, JSON-LD valid,
   robots index/follow, no `&lt;script` leak, index lists the post.
10. **Log it.** Fill the decision-log Trail + Sources; the gate already updated the queue row.
    Then write the tracker row (section D below) — this is the engine's memory; never skip it.

---

## Gotchas (learned in production — trust these)

- **@graph hides @type from the scorer.** `analyze_blog.py` reads `data.get('@type')` off the top
  object and does NOT walk `@graph`. Inline schema as separate flat scripts (one BlogPosting, one
  Person, one FAQPage) or the gate scores schema 0/4. Keep the sidecar `.schema.json` as a @graph
  (that is what `run.py` injects into the rendered `<head>`).
- **Inline SVG vs image credit.** `analyze_blog` counts markdown `![]()` / `<img>`, not inline
  `<svg>`. For image points, reference charts as external `.svg` files via markdown, with explicit
  colors (currentColor does not inherit through `<img>`), and drop the files in
  `publish/posts/<slug>/` so the render finds them.
- **Score climb levers:** inline flat schema (+4 tech), first-person original analysis
  ("we ran/analyzed/found", "in our experience") (+orig +exp), transition words ≥15% (+1),
  2+ entity definitions (`**term** is/are`), markdown chart refs (+2 tech). Readability (Flesch)
  is the sticky one with citation-dense prose; short sentences help.
- **Factcheck 403 wall.** Many analyst/gov primaries return 403 to automated fetchers. A pure
  fetch-based checker fails them on ACCESS, not accuracy, and would wrongly route good posts
  to review. The loop's factcheck MUST have a WebSearch-corroboration fallback for bot-blocked
  primaries.
- **AI-generated hero images bake garbled text into the picture.** Use real licensed photos
  (Openverse rung) for heroes; only use AI image backends for abstract/decorative art.

## Done when
The slug is `published` (site rebuilt, HTML verified) or `review-queue` with a logged reason, and
the decision log Trail is complete.

---

## The intelligence layer

Sits ON TOP of the loop above — it does NOT replace the deterministic gate (step 7). It adds
dual-signal selection, a tracking ledger, and the citation feedback loop.

**Tracker** — Airtable base or Google Sheet ({{YOUR_TRACKER_LINK}}) with 3 linked tables:
- **Keyword Universe** — selection brain (query, intent, cluster, `serp_difficulty`,
  `geo_winnability`, `quadrant`, `pillar`, `spoke_role`, `scheduled_date`, `last_scanned`,
  `produced_post`).
- **Content Pipeline** — production ledger (slug, title, status, `qa_score`, `factcheck_status`,
  `gate_decision`, `information_gain`, `published_url`, dates, decay flags, cost).
- **AI-Citation Log** — the learning loop (one row per post × engine × date: `cited`,
  `sources_named`, `measured_date`).

### A. Dual-signal selection (extends step 1)
Pick by `quadrant`, not raw priority: **🟢 write-first** (rank-able AND cite-able) → **🔵 geo-play**
(cite-able only; still valid — the goal is citations) → **🟡 seo-play** → **🔴 defer**.
`quadrant = serp_difficulty (SEO, "who ranks?") × geo_winnability (GEO, "who gets cited?")`, GEO
weighted above SEO. Method: run a live SERP audit (who is on page 1?) and a live AI-citation scan
(ask ChatGPT/Perplexity/AI Overviews/Gemini the question — whom do they cite today?). If the
citations go to small blogs and editorial sources, the seat is winnable; if platform giants or
vendor tools own the answer, defer. Re-scan any topic whose `last_scanned` is stale.

### B. Write the Content Pipeline row (after step 7 gate)
Upsert one row keyed on `slug`: `title`, `status`, `qa_score`, `factcheck_status`, `gate_decision`,
`iteration_count`, `information_gain`, `review_reason` (if held), `published_url`,
`published_date`. Link `produced_post` on the Keyword Universe row. This is the engine's memory —
never skip it.

### C. Close the loop — measure + decay (post-publish)
- **AI-Citation Log:** run the DIY prompt panel (ChatGPT/Perplexity/AI Overviews/Gemini — low
  source overlap between engines, so test all four) on the post's target queries; write one row per
  (engine × date) with `cited`, `sources_named` (who got cited INSTEAD = live competitor intel),
  `measured_date`. This is the real GEO KPI — analytics tools can't see AI citations.
- **Decay:** set `decay_flag` / `refresh_due` when `date_modified` >30d or citations drop →
  re-queue for refresh (AI engines favour ~30-day freshness).
