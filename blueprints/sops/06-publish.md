# SOP 06 — Publish (Standalone HTML → Vercel)

**Goal:** Render the approved draft to a self-contained HTML page and deploy it via Vercel.

**Owner:** Architect, using `blog_render.py` + the publish engine.

## Preconditions
- SOP 05 passed (score ≥ 80, no hard-rule violations).
- A hero image exists (or `generate_hero.py` was run).

## Steps

1. **Render to standalone HTML:**
   ```
   equipment/.venv/bin/python equipment/scripts/blog_render.py \
     --md posts/<slug>.md \
     --out-dir publish/posts/<slug> \
     --pdf-engine none
   ```
   This emits `publish/posts/<slug>/index.html` — a self-contained page with embedded CSS,
   dark-mode support, and JSON-LD schema. (Use `--pdf-engine auto` only if a PDF artifact is
   wanted and weasyprint/playwright is installed.)
2. **Embed schema** — confirm the JSON-LD from SOP 04 is present in the `<head>`. If `blog_render`
   didn't inline it, inject `posts/<slug>.schema.json` into the rendered HTML.
3. **Update the index** — run `publish/build_index.py` to regenerate `publish/index.html`
   (the blog home page listing all posts, newest first).
4. **Deploy to Vercel** — see `publish/config` for the target. Two supported modes:
   - **Git mode**: commit `publish/` and push to the Vercel-connected repo/branch → auto-deploy.
   - **CLI mode**: `vercel deploy publish/ --prod` (requires `vercel` CLI + linked project).
   The deploy target is captured in `publish/config` on first publish (ask the user once).
5. **Update** `architect/topic-queue.md` status → `published`; record the live URL in the
   decision log.

## Output
- `publish/posts/<slug>/index.html` (the standalone post)
- Updated `publish/index.html` (the blog index)
- Live URL on the Vercel site

## Done when
The post is live and renders correctly in a browser (open the HTML locally to verify first).

## Quality gate
- HTML opens standalone with no broken assets (images embedded or correctly pathed).
- JSON-LD present and valid in `<head>`.
- Index page links to the new post.
- Mobile-friendly (the rendered CSS is responsive by default).
