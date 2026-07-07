# Hard Cases and Failure Modes

The audit and the templates handle the common case: your page exists, is weak, and you rewrite it. These are the cases where that playbook does not apply, and the fix is different. Recognize which one you are in before reaching for a rewrite.

## Contents

- The cited source is a competitor or third-party listicle you cannot edit
- The engine states wrong facts about the brand
- You are cited, but the sentiment is negative
- The engines disagree on who wins
- The query is local / multi-location
- The vertical is YMYL (health, finance, legal)

## The cited source is a listicle you cannot edit

Symptom: for "best X" or "top N X", the engine quotes a roundup post (a "10 best X" article, a competitor's comparison page, a review-site list) and you are absent from it or buried in it. Rewriting your own page does little, because the engine is not quoting your page — it is quoting *that list*.

The fix is off-page, not on-page:

1. **If the cited source is a claimable directory or review platform, optimize your profile on it first.** This is the highest-leverage and most-missed move. A Yelp list, a Google local pack, Healthgrades, G2, Capterra — you cannot edit the *list*, but you usually own a *claimable profile* that directly influences whether that platform ranks you onto the very list being cited. Complete the profile, fix categories, add current photos and details, and improve your reviews. You are not editing the citation; you are improving your standing inside the source the engine already trusts. Two cautions: (a) **review and listing rules differ by platform** — some (notably Yelp) prohibit soliciting reviews and filter solicited ones, while others (Google) encourage asking; verify each platform's rules before advising on reviews rather than giving blanket "get more reviews" advice. (b) **Manufacturer and association provider-locators are claimable directories too** — an official "find a [brand] provider/dealer/partner" locator (e.g. a product's certified-provider directory) is a citable source you can earn placement in, the same lever as a review site.
2. **Get included or moved up in editorial lists.** For independent roundups, pitch the publisher to add or re-rank you — with a concrete, factual reason (a capability they omitted, a dated stat). Route the outreach to `link-building`.
3. **Build your own credible roundup** that engines can cite instead — a genuinely fair "best X for Y" comparison including competitors. Fairness is the point; a self-serving list reads as marketing and is penalized.
4. **Win the long tail / the segment.** You may not crack the head term "best X" but can own "best X for [specific segment]", where the generic listicles are thin — usually the fastest realistic win. For local head terms ("best dentist in [city]"), the segment is the neighborhood or specialty ("best dentist in [neighborhood]", "best Invisalign provider in [city]"). The local case below and this section solve such queries together.

## The engine states wrong facts about the brand

Symptom: the brand-knowledge probe (`measurement.md`) returns *wrong*, not just *absent* — e.g., wrong founding year, wrong category, a discontinued product, a competitor's feature attributed to you. Wrong is worse than absent: it means contradictory or stale sources are being trusted.

Remediation:

1. **Find the contradicting sources.** Wrong parametric facts come from somewhere — an outdated Crunchbase entry, a stale Wikipedia line, an old press release, a directory with bad data. Locate them.
2. **Correct at the source, consistently.** Fix the canonical fact everywhere it appears (the consistent-facts baseline in `entity-presence.md`). One correction rarely moves a trained-in belief; broad agreement across sources does, over time.
3. **Reinforce the correct fact** on high-trust properties (Wikidata, your own clearly-dated pages, earned coverage). This is slow — parametric memory lags — so set the expectation and re-probe quarterly.
4. **Do not expect a live correction to instantly fix training-time beliefs.** Retrieval-based engines can update fast once your sources are fixed; the base model's memory updates only with new training.

## You are cited, but the sentiment is negative

Symptom: you appear in answers, but described unfavorably ("X is expensive and hard to set up"). Citation is not the goal if the citation hurts.

1. **Trace the negative source.** It is usually a specific review thread, a critical comparison, or a cluster of complaints (Reddit, G2, Trustpilot) the engine is summarizing.
2. **Address the substance, then the record.** If the criticism is fair, the durable fix is the product/positioning; surface the change in dated, factual content. If it is outdated, publish the current, sourced counter-fact and pursue updates on the source where feasible.
3. **Add balanced, honest material you control** — pros-and-cons blocks that name real limitations read as trustworthy and give engines a fairer passage to quote than a one-sided complaint.

## The engines disagree on who wins

Symptom: ChatGPT cites you, Perplexity cites a competitor, AI Overviews cite a third party. This is normal — they weight sources differently (`platform-factors.md`).

Do not chase a single universal answer. Diagnose and fix *per platform*: AI Overviews track classic rankings (so a ranking/extractability fix helps there), Perplexity leans recent and well-sourced (freshness and citations help), ChatGPT leans reference/editorial and entity authority (third-party presence helps). Prioritize the platform that matters most to the business, named in the audit output.

## The query is local / multi-location

Symptom: the query has implicit or explicit local intent ("payroll for restaurants", "best dentist in Austin", "X near me", anything tied to physical locations). Generic page work is necessary but not sufficient.

Add the local entity layer:

- **Google Business Profile** consistency and completeness, one per location — AI Overviews and Gemini lean on Google's local/entity data heavily.
- **Consistent NAP** (name, address, phone) and category across local directories; inconsistency confuses both local search and entity understanding.
- **Location-specific pages** with genuinely local facts (not boilerplate spun per city), each answering the local version of the query.
- **Locally-trusted third-party sources** (regional press, local subreddits, local review sites) in addition to the vertical's national sources.

**Multi-location chains** add a structural decision. Model the business as *one brand entity with N sub-locations*, not N unrelated entities: the brand name, category, and core facts stay identical across all locations (one consistent entity for parametric memory), while address, phone, and the local page differ per location. Give each location its own claimed GBP and directory profiles with distinct NAP, but never let the brand description drift between them. Do not pit your own locations against each other for the head term; point each at its own neighborhood/segment query.

**Head term vs segment for local.** "Best [service] in [city]" is usually a listicle/local-pack query you cannot win head-on (see the listicle case above) — the realistic play is to win the neighborhood and specialty segments while optimizing your claimable profiles on the cited platforms. Local + listicle is one combined problem; solve it with both sections.

Treat local entity work as a parallel track to `entity-presence.md`, weighted more heavily the more local the query set is.

## The vertical is YMYL (health, finance, legal)

Symptom: the brand is in health, medicine, finance, or law, and engines cite institutional sources (government domains, major hospitals, established financial press, recognized legal references) almost exclusively for the broad head terms.

These verticals have a **structurally higher citation ceiling**, and no amount of page optimization turns a private clinic or advisory firm into a source engines trust the way they trust a government health body. Plan around it rather than promising the head term:

- **Credentialed authorship and institutional signals matter more here**, not less. Named, verifiable experts with real credentials; citations to the institutional sources engines already trust; nothing that reads as a medical/financial claim without sourcing.
- **Win where institutions are thin**, not where they dominate: specific procedures, local intent, "how to choose", cost and process questions, eligibility — the practical queries the institutional sources answer poorly.
- **Do not blindly prioritize your own roundup** for a YMYL head term (the general advice in Task 3); your fair comparison still competes against sources engines weight far above you. The segment and local plays usually beat it.
- **Accuracy is reputational and sometimes regulatory.** Fabricated or overstated YMYL claims do real-world harm and are penalized hard; keep every claim sourced and current.
- **Regulated verticals constrain advertising and reviews by law, not just by platform.** Health, finance, legal, and licensed trades are governed by board/regulator rules and (for health) privacy law that limit superlative claims ("best", "#1"), patient/client testimonials, before-and-after imagery, and review handling. This skill does not encode any one vertical's code — flag the compliance layer explicitly and have the user confirm their content and review tactics against their regulator and each platform's terms before publishing. Getting this wrong risks a board complaint or a platform penalty, which outweighs any citation gain.

### Worked mini-case: a multi-location chain losing to a directory list

This case shows how the separate tools above *compose*; the dental specifics are an illustration, and the same composition applies to any regulated multi-location business (med-spas, law-firm groups, clinics, licensed trades). The lesson is the order of moves, not the vertical.

Scenario: a 6-clinic dental brand in one city. For "best dentist in [city]" and "where to get Invisalign in [city]", ChatGPT and Perplexity cite two competitors and a Yelp list; the brand is absent. No live AI access, so the operator pastes the answers (`measurement.md` fallback).

Diagnosis: the Yelp citation is the *claimable-directory* case, not a page problem — rewriting clinic pages will not change a Yelp citation. The two competitor wins are a passage-diff + local-entity problem. The head term is unwinnable head-on; the segments are open.

The plan, in priority order:

| Move | Case it comes from |
| --- | --- |
| Claim and fully optimize all 6 Yelp + Google Business Profiles (categories, reviews, responses, photos) | Claimable-directory lever |
| Target the segments: "best Invisalign provider in [city]", "best dentist in [neighborhood]" — one page per clinic's area | Head-term-vs-segment |
| Lock one consistent brand entity across all 6 locations; distinct NAP per clinic | Multi-location chain structure |
| Passage-diff the two cited competitor pages once pasted; fix the deciding axis | Standard audit |
| Earn local press / local-subreddit presence | Locally-trusted sources |

Health caveat applies (see below): dentistry is YMYL, so the citation ceiling on the broad head term is structurally higher and credentialed-author / institutional signals matter more. Set that expectation rather than promising the head term.
