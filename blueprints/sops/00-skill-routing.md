# SOP 00 — Skill Routing (conflict resolution)

Both equipment repos ship SEO/GEO skills that overlap. This table is the **single source of
truth** for which tool runs which job. The principle: **your `seo-geo-skills` optimize (do the
work); claude-blog's skills validate/score (check the work).**

## Routing table

| Job | Use | NOT |
|-----|-----|-----|
| Optimize classic on-page SEO (intent, keywords, title, meta, headings, internal links, alt) | **`on-page-seo`** (yours) | ~~/blog seo-check for optimizing~~ |
| Optimize AI citations / GEO (extractability, citability, entity presence, AI-first prose) | **`ai-seo`** (yours) | ~~/blog geo for optimizing~~ |
| MENA / Arabic GEO | **`ai-seo`** MENA/Arabic playbook (yours) | — (only tool with this) |
| Validate SEO — pass/fail checklist (title length, meta, OG/Twitter, canonical, alt) | **`/blog seo-check`** | ~~on-page-seo for QA scoring~~ |
| Score GEO — 0–100 AI Citation Readiness + citation capsules | **`/blog geo`** | — |
| Schema / JSON-LD (BlogPosting, FAQPage, Person, Breadcrumb) | **`/blog schema`** | — (uncontested; both seo-geo skills route schema out) |
| 100-point quality score | **`analyze_blog.py`** (equipment) | — |

## The two-pass optimize order (inside SOP 04)
Your two skills already define a handoff contract; run them in this order:
1. **`on-page-seo` first** — fixes intent, title, meta, URL, heading structure + keyword positions.
   It then **defers the lead + body prose** to the GEO pass (so prose isn't written twice).
2. **`ai-seo` second** — front-loads the answer, makes blocks extractable, strips promotional
   tone from H1/body. Where the two tension, **`ai-seo`'s anti-stuffing / write-naturally rule
   wins on body copy.**

## Why this split (not "pick a winner")
- Your skills are **optimizers / methodology** (deeper, and `ai-seo` is the only one with the
  MENA/Arabic playbook). They should own the actual content changes.
- claude-blog's `blog-seo-check` / `blog-geo` are **auditors / scorers** — ideal as the QA gate,
  wrong as the optimizer.
- Running both as optimizers would double-write prose and risk contradictions. Do-vs-check
  removes that entirely.
