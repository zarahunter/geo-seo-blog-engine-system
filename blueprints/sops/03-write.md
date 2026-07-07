# SOP 03 — Write

**Goal:** Produce a first draft that is answer-first, sourced, on-template, and on-voice.

**Owner:** Architect, using the `/blog write` equipment + brand context.

## Steps

1. **Load voice + brand** — `blueprints/brand/BRAND.md` and `VOICE.md` define positioning,
   audience, taboo phrases, tone, and sentence ceiling. (The `/blog` skill auto-loads these when
   present at project root; for this factory, pass them in or keep symlinks — see note below.)
2. **Select the template** from `blueprints/templates/` chosen in intake (how-to-guide, listicle,
   comparison, pillar-page, etc.). Follow its section structure and word-count target.
3. **Generate the draft** — run `/blog write <topic>` feeding it the research packet
   (`research/<slug>.md`) and the chosen template. Enforce the 6 Pillars:
   - **Answer-first**: every H2 opens with a 40–60 word, stat-rich direct answer.
   - **Real sourced data**: inline attribution for every number (from the packet).
   - **Structure**: 50–150 word chunks, question-style headings, H1→H2→H3 (never skip).
   - **FAQ block**: 3+ Q&As with 40–60 word answers (GEO surface + schema feed).
   - **Visual media**: hero + at least one chart/image with descriptive alt text.
   - **Freshness**: current year anchor in prose; `dateModified` ready.
4. **Save** the draft to `posts/<slug>.md` with frontmatter (title, description, slug, primary
   keyword, date, dateModified, author, tags).
5. **Update** queue status → `drafted`.

## Output
- `posts/<slug>.md` (markdown draft with frontmatter)

## Done when
Draft is complete, on-template, every stat is attributed, and an FAQ block exists.

## Quality gate (hard rules — do not pass a draft that violates these)
- No fabricated statistics (every number traces to `research/<slug>.md`).
- No paragraph > 150 words.
- No skipped heading levels.
- ≤ 1 self-promotional mention (author-bio context only).
- No forbidden prose chars (em-dash, en-dash, `--`) — `lint_prose.py` enforces in QA.

## Note on brand auto-load
`/blog` reads `BRAND.md`/`VOICE.md` from the **project root**. Options: (a) keep canonical files
in `blueprints/brand/` and symlink to root, or (b) copy at write time. The Architect picks; the
canonical source of truth is always `blueprints/brand/`.
