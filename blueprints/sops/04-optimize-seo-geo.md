# SOP 04 — Optimize (SEO + GEO)

**Goal:** Make the draft rank in classic search AND get cited by AI answer engines.

**Owner:** Architect, using the `on-page-seo` + `ai-seo` skills (from `zarahunter/seo-geo-skills`).

> **Routing (see `blueprints/sops/00-skill-routing.md`):** this stage OPTIMIZES, so it uses
> **your** skills only — `on-page-seo` then `ai-seo`. The claude-blog audits (`/blog seo-check`,
> `/blog geo`) are NOT optimizers; they run later as validators in SOP 05. Schema is `/blog schema`.

Run both passes in order. They are complementary, not alternatives.

## Pass A — Classic search (`on-page-seo`)
Invoke the `on-page-seo` skill against `posts/<slug>.md`. Validate/fix:
- Search intent match (does the content answer the query type?)
- Primary keyword in: title tag, H1, first 100 words, ≥1 H2, URL slug, meta description.
- Title tag 50–60 chars; meta description 150–160 chars.
- Heading hierarchy clean (H1→H2→H3).
- Internal-link zones + descriptive anchor text.
- Image alt text present + naturally keyworded.

## Pass B — AI answers / GEO (`ai-seo`)
Invoke the `ai-seo` skill against `posts/<slug>.md`. Validate/fix:
- Extraction-ready passages (the answer-first openers).
- Entity presence + clarity (who/what is unambiguous to an LLM).
- Q&A / FAQ formatting with self-contained 40–60 word answers.
- Citable, sourced claims with named publishers.
- **If MENA/Arabic audience**: apply the `ai-seo` MENA / Arabic playbook.

## Pass C — Structured data
- Run `/blog schema posts/<slug>.md` to generate JSON-LD (BlogPosting, FAQPage, Person,
  BreadcrumbList). Keep it ready for the publish stage to embed.

## Output
- Optimized `posts/<slug>.md`
- JSON-LD schema (inline or `posts/<slug>.schema.json`)

## Done when
Both SEO and GEO passes report no blocking issues and schema is generated.

## Quality gate
- Title + meta within length limits.
- Primary keyword placement complete (no stuffing).
- FAQ answers are self-contained and extraction-ready.
- Valid JSON-LD generated.
