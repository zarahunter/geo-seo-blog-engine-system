# SOP 01 — Intake

**Goal:** Turn a raw topic into a logged, scoped job the pipeline can run.

**Trigger:** User says "blog about X" / "write a post on X" / gives a topic.

**Owner:** Architect (Claude).

## Steps

0. **Trend discovery (when the topic is broad or the user asks "what should I write").**
   Dispatch the **`trend-scout`** agent on the topic/niche. It returns ranked angles with a
   0–100 viral-potential score. Present the top 3 to the user and let them pick (or pick the
   highest scorer if they delegate). Skip this step if the user already gave a specific, narrow
   topic. The chosen angle becomes the topic below.
1. **Capture the topic** exactly as given.
2. **Derive a slug** — lowercase, kebab-case, no stop-words where avoidable
   (e.g. "How AI is changing SEO in MENA" → `ai-changing-seo-mena`).
3. **Set defaults & confirm only if ambiguous:**
   - Primary keyword (best guess from the topic)
   - Target template (see `blueprints/templates/`; default `how-to-guide`)
   - Audience / locale (default: global English; flag if MENA/Arabic relevant → `ai-seo` MENA playbook)
   - Angle / unique take (1 line)
4. **Log it** as a new row in `architect/topic-queue.md` with status `intake`.
5. **Open a decision log** at `architect/decisions/<slug>.md` recording: topic, slug, primary
   keyword, template, audience/locale, angle, and date.

## Output
- A row in `architect/topic-queue.md`
- `architect/decisions/<slug>.md`

## Done when
Slug + primary keyword + template are set and logged. Advance to **SOP 02 — Research**.

## Quality gate
- Slug is unique (no collision in `posts/` or the queue).
- Exactly one primary keyword chosen (avoid cannibalization with existing posts — eyeball the
  queue; if overlap, pick a differentiated angle or merge).
