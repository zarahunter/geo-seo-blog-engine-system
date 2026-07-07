---
name: on-page-seo
description: "Optimize a single web page to rank in classic search results (Google, Bing). Use whenever the user mentions on-page SEO, SEO, ranking on Google, keyword optimization, title tags, meta descriptions, heading structure, internal linking, alt text, URL slugs, search intent, keyword placement, or 'optimize this page/blog/post for search', even if they don't say 'on-page SEO'. Also use as the ranking half of a full optimization pass alongside ai-seo (GEO). Route technical SEO (speed, sitemaps, crawl, indexing) elsewhere, schema/JSON-LD to schema-markup, backlinks to link-building, and AI-citation optimization to ai-seo."
metadata:
  version: 1.0.0
  last_reviewed: 2026-06-19
---

# On-Page SEO

Optimize the content and HTML *of a single page* so search engines understand it and rank it for the query it targets. On-page SEO is what you control directly on the page — intent match, keywords, title, meta, headings, links, images, structure. It is the floor that everything else builds on.

## When to use this vs related skills

This skill owns the on-page layer for **classic search ranking**. It pairs with `ai-seo`, which owns getting the same page **cited inside AI answers**. They are two passes on one page (see "Working with ai-seo" below).

| User wants | Use |
| --- | --- |
| Rank a page on Google/Bing: intent, keywords, title, meta, headings, internal links, alt text | **This skill** |
| Get the page retrieved and cited by ChatGPT / Perplexity / AI Overviews | `ai-seo` |
| Full optimization (rank **and** get cited) | **Both** — this skill, then `ai-seo` |
| Implement schema / JSON-LD | `schema-markup` |
| Technical SEO: page speed, sitemaps, crawl/index, redirects, canonicals | technical-SEO tooling (out of scope here) |
| Earn backlinks | `link-building` |
| Build topic clusters / a topical map | `topical-authority` |
| Many pages from a template | `programmatic-seo` |

Keep the scope tight. If asked for technical or off-page work, do the on-page work here and name the hand-off.

## Before starting

If `.claude/product-marketing-context.md` exists, read it and skip questions it answers. Otherwise establish only:

- The **one primary query/keyword** this page targets (one page, one primary intent).
- The **search intent** behind it (see Core model).
- Whether the user wants to audit an existing page, optimize one, or write a new one.

Ask at most one or two questions; infer the rest and state assumptions inline.

If you cannot see live search results or keyword data (no search access, no connected SEO tool), do not present guessed intent, keywords, or competitors as validated. Say what you are assuming, or ask the user to paste the current top-ranking results for the query — then work from those.

## Core model: read this before optimizing anything

**1. One page, one primary query.** A page that tries to rank for everything ranks for nothing. Pick one primary keyword/query and a small set of supporting terms. Everything on the page serves that.

**2. Match search intent first — it outranks every tactic.** Before keywords, ask what the searcher actually wants. The four intents:
   - *Informational* ("how does X work") → guide, explainer, definition.
   - *Commercial* ("best X", "X vs Y", "X review") → comparison, listicle, evaluation.
   - *Transactional* ("buy X", "X pricing", "X signup") → product/pricing/landing page.
   - *Navigational* ("[brand] login") → the specific destination page.
   A page whose format mismatches intent (a sales page for an informational query) will not rank no matter how clean the tags are. Confirm the intent by looking at what already ranks for the query. Many high-value queries are **hybrid** — "how to choose X" or "best X for Y" are informational and commercial at once, and the page that ranks is usually a guide that *contains* a comparison block. When the SERP shows mixed formats, build the dominant format and fold in a block serving the secondary intent.

**3. Keywords are placed, not stuffed.** Search engines reward a keyword appearing in the right *positions* (title, H1, early body, a subheading, URL, alt text) far more than the same keyword repeated many times. Repetition past natural use is **over-optimization** and can hurt. Write for a human first.

**4. Title and meta are for clicks as much as rank.** The title tag is a direct ranking factor and the biggest on-page lever; the meta description is not a direct ranking factor but drives click-through, which matters. Write both to be accurate and compelling, not keyword-jammed.

**5. Structure is a ranking signal.** Clean heading hierarchy, scannable paragraphs, and descriptive internal links help engines parse the page and help users stay — both feed ranking.

## Pick the task

1. **Audit a page's on-page SEO** (below)
2. **Optimize an existing page** (below)
3. **Write a new page** (below)
4. **Full optimization with AI citation** → do the task here, then hand to `ai-seo` (see "Working with ai-seo")

## Task 1: Audit a page

1. **Identify the target query and intent.** If unclear, look at what ranks for the query to infer intent.
2. **Run the on-page checklist** in `references/checklist-and-templates.md`. Each failed row is a ranking gap.
3. **Check intent match.** Does the page format match what ranks? A mismatch is the highest-priority fix.
4. **Check keyword placement** against the placement map in `references/keyword-and-intent.md` — title, H1, first 100 words, a subheading, URL, alt text. Note missing positions and any stuffing.
5. **Output.** A prioritized fix list: the one intent/format issue first (if any), then placement gaps, then title/meta, then structure and links.

## Task 2: Optimize an existing page

Work top-down — the highest-leverage elements first.

1. **Confirm intent/format match.** Fix this before anything cosmetic.
2. **Title tag.** Rewrite using the template in `references/checklist-and-templates.md`: primary keyword near the front, ~50–60 characters, compelling, unique on the site.
3. **Meta description.** ~150–160 characters, includes the query naturally, written to earn the click.
4. **URL slug.** Short, lowercase, hyphenated, contains the keyword, no stop-word clutter. (Changing a live URL needs a 301 redirect — flag this.)
5. **Headings.** Exactly one H1 matching the query; logical H2/H3; primary or supporting terms in some headings, naturally.
6. **Body.** Primary keyword in the first 100 words; supporting/semantic terms covered (see `references/keyword-and-intent.md`); content depth matched to intent; short scannable paragraphs.
7. **Internal links.** Link to relevant pages with descriptive anchor text (not "click here"); link from strong pages to the target.
8. **Images.** Descriptive filenames and alt text that describe the image and include the keyword only where it genuinely fits.
9. **Strip over-optimization.** Remove keyword stuffing, exact-match repetition, and thin filler.

## Task 3: Write a new page

Pick the format from the intent (Core model #2), then build it:

1. Outline headings around the query and its sub-questions before writing.
2. Draft for the human and the intent first; place the primary keyword in the title, H1, and first 100 words as you go.
3. Cover supporting and semantic terms naturally (`references/keyword-and-intent.md`).
4. Write the title tag and meta description from the templates.
5. Add internal links to related pages with descriptive anchors.
6. Set a clean URL slug.

Then run Task 1's checklist on your own draft before shipping.

## Full optimization: the two-pass handoff contract

On-page SEO gets the page **ranked**; `ai-seo` (GEO) gets it **cited** in AI answers. They operate on the same page and mostly reinforce each other. When you do both, follow this contract so the passes don't fight or duplicate work:

1. **Decide once, carry forward.** The SEO pass fixes the **primary query, search intent, and title tag**. The GEO pass inherits them — it does not re-decide intent or keyword. State them explicitly so they pass forward.
2. **Structure in the SEO pass, prose in the GEO pass.** In the SEO pass, lock the heading outline and the structural keyword positions (title, H1, URL, one H2, alt). Draft the headings — but **defer writing the lead and body prose to the GEO pass**, or you write the lead once for SEO and rewrite it for GEO.
3. **Resolve field by field** (where the two skills' rules actually meet):

| Field | Rule | Promotional tone? |
| --- | --- | --- |
| Title tag | Primary keyword near the front + benefit + brand | OK — it is a SERP click target, not an extracted answer |
| Meta description | Compelling, includes the query naturally | OK — SERP snippet, not extracted by engines |
| URL slug | Short, keyword, hyphenated | n/a |
| H1 | The bare query, mirrors the prompt | No |
| Lead + body | Natural, self-contained, extractable | **No — GEO's anti-stuffing / anti-promo rule wins** |

**Order:** SEO pass first (intent, title/meta/URL, heading structure, keyword positions) → GEO pass (`ai-seo`: writes the lead and body as front-loaded, extractable, promo-free prose; adds sourced stats, FAQ, dated author). Hand schema to `schema-markup`.

## Guardrails: on-page own-goals

- **Intent mismatch beats every other mistake.** The wrong page format will not rank; fix it first.
- **Keyword stuffing / over-optimization hurts** — natural placement in key positions beats repetition.
- **Duplicate or templated titles and metas** across pages waste the biggest lever; make each unique.
- **One H1 only**, and don't skip heading levels for styling.
- **Generic anchor text** ("click here", "read more") wastes internal-link value; describe the destination.
- **Changing a live URL without a 301 redirect** loses ranking equity; always redirect.
- **Writing for the engine, not the reader.** If it reads badly to a human, it will not hold rankings.
- **Keyword cannibalization.** Before targeting a query, check the site is not already ranking another page for it. If it is, consolidate the pages or differentiate their intent rather than competing with yourself.

## References

- `references/checklist-and-templates.md`: the full on-page checklist plus copy-paste templates (title tag, meta description, URL slug, heading outline, internal-link anchors, alt text).
- `references/keyword-and-intent.md`: the four search intents and how to confirm them, primary vs supporting/semantic keyword selection, the keyword placement map, and over-optimization limits.
