---
name: ai-seo
description: "Optimize content to get retrieved and cited as a source inside AI answers (ChatGPT, Perplexity, Google AI Overviews, Gemini, Copilot, Claude). Use whenever the user mentions AI SEO, GEO, AEO, LLMO, answer engine optimization, generative engine optimization, AI Overviews, getting cited by ChatGPT or Perplexity, AI citations, AI visibility, or zero-click search, AND when they ask to audit why a competitor is cited and they are not, optimize a page for AI answers, write a comparison, FAQ, or how-to page that AI will quote, or check whether content is extractable by LLMs, even if they never say 'AI SEO'. Covers AI-visibility audits, page-level optimization, AI-first content creation, entity presence, and lightweight monitoring. Route schema implementation to schema-markup, large-scale mention tracking to ai-visibility-monitoring, third-party mention seeding to llm-seeding, and earned links to link-building or citation-building."
metadata:
  version: 3.0.0
  last_reviewed: 2026-06-18
---

# AI SEO (GEO)

Make content discoverable, extractable, and citable by AI answer engines. The goal is not ranking, it is getting *retrieved and quoted* as a source when an AI assembles an answer. Traditional SEO gets a page ranked. GEO gets a passage cited.

## When to use this vs related skills

This skill owns the page and the brand's entity footprint: extractability, citability, the audit, per-page creation, and the consistent-facts work that feeds parametric memory. Hand off the rest.

| User wants | Use |
| --- | --- |
| Audit AI visibility, optimize a page, write AI-first content, build entity presence | **This skill** |
| Rank the page in classic Google / Bing results (intent, keywords, title, meta, headings) | `on-page-seo` |
| Full optimization — rank **and** get cited | **Both** (`on-page-seo` pass, then this skill) |
| Implement the actual schema/JSON-LD | `schema-markup` |
| Track mentions and share of voice across many AI platforms | `ai-visibility-monitoring` |
| Plant brand mentions in Reddit, Wikipedia, forums, review sites | `llm-seeding` |
| Earn backlinks and citations from authoritative domains | `link-building`, `citation-building` |
| Build topic clusters and a topical map | `topical-authority` |
| Build SEO pages at scale from a template | `programmatic-seo` |
| Founder authority, LinkedIn presence | `thought-leadership`, `linkedin-content` |

If the user asks for several of these at once, do the on-page and entity work here and name the hand-offs as next steps rather than trying to do everything.

**Working with `on-page-seo` (the two-pass method).** This skill makes a page *cited* in AI answers; `on-page-seo` makes the same page *rank* in classic search. For full optimization, run the **SEO pass first** (`on-page-seo`: intent match, keyword placement, title, meta, URL, heading hierarchy, internal links) to set the structure, then the **GEO pass** (this skill: front-loaded answer, extractable blocks, citability, strip promotional tone) to refine the prose. They mostly reinforce each other; where they tension — classic SEO once tolerated keyword repetition — **this skill's anti-stuffing, write-naturally rule wins on the body copy.** Follow the handoff contract: the SEO pass fixes intent, title, meta, URL, and the heading structure and keyword positions, then **defers the lead and body prose to this (GEO) pass** so it is not written twice. Promotional tone is acceptable in the title tag and meta description (SERP click targets) but banned in the H1 and body, which this skill writes. The full contract lives in `on-page-seo`.

## Before starting

If `.claude/product-marketing-context.md` exists, read it and skip questions it already answers. Otherwise establish only what the task needs:

- The 10 to 20 queries that matter to the business (these are the unit of work, not keywords).
- The category and competitors, so source priority can be set correctly (see Core model).
- Whether the user wants to audit, optimize an existing page, create new content, build entity presence, or set up monitoring.

Ask at most one or two of these. Infer the rest from context and state assumptions inline.

## Core model: read this before optimizing anything

**1. Two systems, two strategies.** AI answers come from two places. *Retrieval* (live web search inside ChatGPT, Perplexity, AI Overviews, Copilot) is fast to influence and rewards structure and freshness. *Parametric memory* (what the base model already absorbed in training) is slow to influence and rewards broad, consistent presence across many sources over time. Most page-level work targets retrieval (Tasks 2-3). Most entity and third-party work targets parametric memory (Task 5). Name which one a tactic serves so expectations are right.

**2. Win two things.** First get *retrieved* (the engine has to pull your page into its working set). Then get *cited* (your passage has to be the one it quotes). Structure drives retrieval. Authority and clarity drive the citation.

**3. The unit is the passage, not the page.** Engines extract self-contained blocks. Every key claim must read correctly with zero surrounding context. A brilliant page made of context-dependent sentences gets retrieved and then ignored.

**4. Prompts are long, so answer questions, not keywords.** AI prompts run far longer than search queries. Optimize headings and blocks to answer a fully phrased question, not a two-word term.

**5. Volatility is the baseline, not the exception.** Which domains get cited shifts in weeks. Treat every citation-share statistic as perishable and verify before quoting it to a user. Detail and current figures live in `references/research-stats.md`, all dated and caveated.

**6. The biggest own-goal is promotional tone.** Marketing language ("the best choice", "industry-leading", "act now") measurably *suppresses* citation. Removing it is usually higher leverage than adding any tactic. Keyword stuffing also actively hurts. See guardrails.

## Pick the task

Route to the matching section. When unsure, run the audit first. For any optimize-or-create task, read `references/worked-example.md` once — it shows a full audit-to-rewrite on one page and is the fastest way to calibrate quality.

1. **Audit current AI visibility** (below)
2. **Optimize an existing page** (below)
3. **Create new AI-first content** (below, branches by content type)
4. **Set up monitoring** (below)
5. **Build entity presence** (parametric memory; read `references/entity-presence.md`)
6. **MENA / Arabic optimization** (read `references/mena-arabic.md`)

## Task 1: Audit current AI visibility

Goal: find where competitors are cited and the user is not, and *exactly why*.

**First settle how you will observe the answers.** The whole audit rests on seeing what engines actually answer and recovering the cited passage — that is not free. If you can run the queries live, do. If an AI-visibility tool is connected (Brand-Radar-class MCP tools that return cited domains, cited pages, and AI responses), use it. If you have neither, ask the user to run the test set and paste the answers rather than guessing. The three paths and their caveats (account, region, recency) are in `references/measurement.md`.

1. **Build the test set.** Take the 10 to 20 priority queries. Phrase each the way a person actually asks an assistant (a full question), not as a keyword. Include category, "best X for Y", "X vs competitor", "how to [problem]", a roundup intent ("top N X"), a troubleshooting intent ("X complaints / not working", where Reddit often wins), and pricing-style queries. For a vertical you do not know well, expand by crossing intents (best / vs / how-to / complaints / pricing) with the audience modifiers that matter (industry, company size, region).
2. **Run them, more than once.** AI answers are non-deterministic, so a single run is noise. Run each query at least three times across ChatGPT, Perplexity, and Google AI Overviews (or pull the aggregated equivalent from a connected tool), and record: does an AI answer appear, is the user cited, who is cited instead, and which exact page got pulled. Mark any query you could not actually observe as "not observed" rather than assuming a winner. The full method, sample sizes, and a tracking template are in `references/measurement.md`.
3. **Diagnose the gap with a passage diff.** For each query a competitor wins, do not stop at "their page is better." Open the exact page the engine cited, find the specific passage the answer drew from (it is usually near-verbatim — search the AI answer's phrasing in their page), and diff that passage against your closest equivalent on these axes: is it more *self-contained* (reads right with zero context), more *specific* (numbers, dates, named sources vs adjectives), *fresher* (visible recent date), better *structured* (table/list vs prose), or simply *present on a third-party source you are missing*. Name the one axis that explains the win.
4. **Run the extractability and access checks.** Use the two checklists in `references/content-patterns.md` (extractability) and `references/platform-factors.md` (AI bot access in robots.txt). A page blocked to GPTBot or PerplexityBot cannot be cited by that platform no matter how good it is.
5. **Output.** A prioritized gap list: per query, who wins, the one diff axis that explains it, and the single highest-leverage fix. See the audit table format in `references/worked-example.md`. If the diff points off-page (the winner is a listicle you cannot edit, the engine states wrong facts about the brand, the citation is negative, or the query is local), the fix is not a rewrite — read `references/hard-cases.md` and route accordingly.

## Task 2: Optimize an existing page

1. **Identify the target query** for the page (one primary). Match the H1 and the lead to how that query is asked.
2. **Front-load the answer.** The first paragraph must answer the query directly in roughly 40 to 60 words, self-contained. No throat-clearing before it.
3. **Convert prose to extractable blocks** using the templates in `references/content-patterns.md`: definition block, comparison table, step list, pros and cons, FAQ, sourced-statistic block. Tables beat prose for "X vs Y". Numbered lists beat paragraphs for process.
4. **Raise citability.** Add specific numbers with dated, linked sources. Add at least one named-expert quote with title. Replace generic claims with concrete, attributable ones. Show a visible "last updated" date.
5. **Strip the own-goals.** Remove promotional tone and any keyword stuffing (see guardrails). This step alone often moves citation rate.
6. **Add or request schema.** Identify which schema types fit (Article, FAQPage, HowTo, Product, ItemList) and hand the implementation to `schema-markup`.
7. **Confirm access.** Verify AI crawlers are allowed (`references/platform-factors.md`).

`references/worked-example.md` walks every step above on a real page, before and after.

## Task 3: Create new AI-first content

Pick the format by the query intent, then build it from the matching template in `references/content-patterns.md`. Apply every citability step from Task 2 as you write.

- **Comparison / alternatives page** ("X vs Y", "best X alternatives"): structured table with specific criteria, fair and balanced (visible bias is penalized), current pricing and features. Comparison and roundup formats tend to be among the most-cited (treat as directional, not a guarantee — verify per `references/research-stats.md`), so they are usually worth prioritizing.
- **Roundup / "top N" page** ("top 10 X", "best X for Y"): a genuinely fair ranked list including competitors, each entry one self-contained, sourced block with a concrete reason. Self-serving lists read as marketing and get skipped. If the cited roundups are ones you cannot edit, the play is off-page — see `references/hard-cases.md`. Caveat: prioritizing your own roundup assumes the vertical is winnable; in YMYL (health, finance, legal) and local head terms, engines lean on institutional or directory sources you cannot outrank, so the segment and off-page plays usually beat it (`references/hard-cases.md`).
- **Definitive guide / blog** ("what is X", "how does X work"): definition in the first paragraph, one clear target query, original data or expert quotes, author bio with credentials, visible update date.
- **Product page** ("best X for Y"): concrete description of what it does and who it is for in the lead, feature table, specific metrics instead of adjectives, visible pricing, buyer FAQ.
- **How-to / docs** ("how to X with Y"): numbered steps, prerequisites and expected outcome stated, HowTo schema, descriptive alt text on screenshots.

For multiple pages on one topic, plan the cluster with `topical-authority` rather than producing them ad hoc here.

## Task 4: Set up monitoring

You cannot improve what you do not measure, and citation share drifts constantly.

- For a lightweight, no-tool routine (a monthly manual check the user can run themselves), give them the DIY protocol in `references/measurement.md`.
- For multi-platform tracking at scale, share of voice, and sentiment, hand off to `ai-visibility-monitoring`.
- Track *citation velocity* (how fast new pages enter AI answers after publishing) as a leading indicator, not just current presence.

## Task 5: Build entity presence (parametric memory)

Page work earns retrieval. Entity work earns the slower, stickier prize: the base model "knowing" the brand without a live lookup, and engines trusting it as a consistent thing. Read `references/entity-presence.md`. It covers the consistent-facts baseline, Wikipedia and Wikidata, the third-party source map by vertical, and how to sequence this against page work. Execution of mention placement routes to `llm-seeding`; earned links route to `link-building`.

## Task 6: MENA / Arabic optimization

Read `references/mena-arabic.md`. It covers Arabic and dialect query testing, multilingual entity consistency, citation-density tactics for Arabic content, and a MENA source-priority table. The strategic point: LLMs handle Arabic less comprehensively than English, so there is less competition for Arabic AI citations. That gap is an opening, not a problem.

## Guardrails: the own-goals that suppress citation

- **Promotional tone suppresses citation.** Cut "best", "leading", "act now", and similar. This is the single most common and most damaging mistake.
- **Keyword stuffing actively hurts** in AI contexts (it does not merely fail like in classic SEO).
- **Undated content loses to dated content.** Always show when a page was last updated.
- **Gated content is invisible.** AI cannot read what is behind a form. Keep the authoritative content open.
- **Blocked bots cannot cite you.** Check robots.txt for GPTBot, PerplexityBot, ClaudeBot, Google-Extended, Bingbot.
- **Generic claims do not get cited.** "We are the best" loses to "customers see 3x improvement in [metric], measured [date]".
- **Do not quote a stale citation statistic as fact.** Verify against `references/research-stats.md` and frame numbers as perishable.
- **Inconsistent entity facts confuse parametric memory.** A brand described five different ways across the web is harder for a model to "know". See `references/entity-presence.md`.
- **Cited is not the same as traffic, and traffic is not conversion.** Being inside an AI Overview can still help (cited brands tend to earn higher click-through). Frame outcomes honestly, not as doom or hype.

## References

- `references/worked-example.md`: a complete audit-to-rewrite on one page — gap table, the before page, the after page, and why each change was made. Read once to calibrate quality.
- `references/content-patterns.md`: extractability checklist, the passage-diff method, and copy-paste block templates (definition, comparison, roundup, FAQ, how-to, statistic, pros/cons).
- `references/hard-cases.md`: the cases where a rewrite is the wrong fix — uneditable competitor listicles, wrong facts in parametric memory, negative-sentiment citations, engines disagreeing, and local/multi-location intent.
- `references/platform-factors.md`: how each engine selects sources, per-platform priorities, and the full robots.txt configuration for AI crawlers.
- `references/measurement.md`: non-deterministic testing method, sample sizes, tracking templates, DIY monthly protocol, and monitoring tools.
- `references/entity-presence.md`: consistent-facts baseline, Wikipedia/Wikidata, third-party source map, and how to sequence entity work against page work.
- `references/mena-arabic.md`: Arabic and dialect testing, multilingual entity work, Arabic citation density, MENA source priority.
- `references/research-stats.md`: the underlying research (Princeton GEO study, citation-distribution studies) with dates, caveats, and "verify before quoting" framing.
