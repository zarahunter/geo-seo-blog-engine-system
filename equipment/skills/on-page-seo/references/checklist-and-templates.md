# On-Page Checklist and Templates

Run the checklist against any target page; each failed row is a ranking gap. Then use the templates to fix the high-leverage elements.

## On-page checklist

| Check | Why it matters |
| --- | --- |
| Page format matches search intent | Wrong format (sales page for an info query) will not rank, period |
| One primary query/keyword per page | Pages targeting everything rank for nothing |
| Primary keyword near the front of the title tag | Title is the strongest on-page ranking factor |
| Title tag ~50–60 characters, unique on the site | Longer truncates in results; duplicates waste the lever |
| Meta description ~150–160 chars, includes the query, written for clicks | Not a direct ranking factor, but drives click-through |
| URL slug short, lowercase, hyphenated, contains the keyword | Clean URLs are a minor signal and improve clicks |
| Exactly one H1, matching the query | Multiple/empty H1s confuse parsing |
| Logical H2/H3 hierarchy, no skipped levels | Structure helps engines and readers |
| Primary keyword in the first 100 words | Confirms topic early |
| Supporting/semantic terms covered | Signals depth and relevance (see keyword-and-intent.md) |
| Internal links with descriptive anchor text | Distributes authority and context |
| Images have descriptive filenames and alt text | Accessibility + image search + on-page context |
| Content depth matches what ranks for the query | Thin content loses to comprehensive intent-matched content |
| Visible "last updated" date, content kept current | Freshness is a ranking signal for many queries (and helps AI citation) |
| A concise answer block / question H2s for snippet & PAA targeting | Wins featured snippets and People-Also-Ask slots (overlaps the GEO front-loaded answer) |
| No keyword stuffing / exact-match repetition | Over-optimization can be penalized |
| Reads well to a human | Poor readability does not hold rankings |

## Templates

### Title tag

```
[Primary Keyword] — [Benefit / Qualifier] | [Brand]
```

- Primary keyword as close to the front as reads naturally.
- Target ~50–60 characters as a rule of thumb. Google truncates by *pixel width* (~600px), not character count, so wide words (lots of capitals/Ms/Ws) truncate sooner — check the result, don't just count characters.
- Unique on the site; compelling, not keyword-jammed.
- Example: `On-Page SEO Checklist — 15 Fixes That Move Rankings | Acme`

### Meta description

```
[One sentence answering the query] [One sentence with a reason to click —
specific benefit, number, or differentiator]. [Optional soft CTA.]
```

- ~150–160 characters. Include the query naturally once.
- Written for the human scanning results, not the crawler.
- Example: `A 15-point on-page SEO checklist with copy-paste title and meta templates. Fix the elements that actually move rankings, in order.`

### URL slug

```
/primary-keyword
```

- Lowercase, hyphen-separated, no stop-word clutter ("the", "and", "for").
- Short: the keyword and little else. `/on-page-seo-checklist`, not `/the-complete-guide-to-on-page-seo-for-beginners-2026`.
- Changing a live URL requires a 301 redirect from the old slug.

### Heading outline

```
H1: [Primary query, phrased as the page's topic]
  H2: [First major sub-topic / sub-question]
    H3: [Detail]
  H2: [Second major sub-topic — include a supporting term where natural]
  H2: [FAQ or "X vs Y" if intent calls for it]
```

- One H1 only. Don't skip levels (no H2 → H4).
- Put primary or supporting terms in some headings, naturally — not all.

### Internal-link anchor text

```
Good:  "see our [on-page SEO checklist]"            (describes the destination)
Bad:   "for more, [click here]"                      (wastes the signal)
```

- Anchor text should tell engine and reader what the linked page is about.
- Link from high-authority pages to the page you want to rank.

### Image alt text

```
alt="[plain description of the image][, with keyword only if it genuinely fits]"
```

- Describe what the image shows, for accessibility first.
- Filename: `on-page-seo-checklist.png`, not `IMG_4821.png`.
- Include the keyword only where it honestly describes the image.
