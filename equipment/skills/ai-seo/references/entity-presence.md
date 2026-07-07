# Entity Presence: Optimizing for Parametric Memory

Page work (Tasks 2-3) wins *retrieval* — it gets a URL pulled into the engine's working set for a specific query. Entity work wins the slower, stickier prize: the base model "knows" the brand without a live lookup, and live engines treat it as a consistent, trustworthy thing. This is the parametric-memory half of the core model. It compounds over months, not days, so set expectations accordingly and start it early.

Last reviewed 2026-06-18. The principles are stable; specific properties and their relative weight shift, so verify before relying on any single channel.

## Contents

- The consistent-facts baseline (do this first)
- Wikipedia and Wikidata
- The third-party source map
- Author and expert entities
- Sequencing entity work against page work

## The consistent-facts baseline (do this first)

A model learns an entity from many sources agreeing. Disagreement is the enemy. Before chasing any new property, make the brand describe itself *identically* everywhere it already appears.

Lock a single canonical version of each fact and propagate it:

- **Name** (exact casing, with/without suffix like "Inc." — pick one).
- **One-sentence definition** ("X is a [category] for [audience] that [core job]") — the same sentence on the homepage, About page, LinkedIn, Crunchbase, G2, app stores.
- **Category** (the noun a model should file the brand under).
- **Founding year, HQ, founder names** — stated, not implied.
- **Core differentiator** in one concrete clause.

The single highest-leverage entity action for most brands is not a new Wikipedia page — it is removing contradictions between the descriptions that *already exist*. A brand described five different ways across the web is one a model cannot confidently "know".

## Wikipedia and Wikidata

These two feed entity understanding disproportionately because engines treat them as structured, vetted ground truth.

- **Wikidata** is the more accessible of the two. It is a structured database, not an encyclopedia, so notability bars are lower. Ensure the brand has an item with: an English label and description, `instance of` the right class, `industry`, `official website`, founders, and inception date. Add `inLanguage`-relevant labels for every market the brand serves. Engines pull entity facts from here directly.
- **Wikipedia** has a real notability bar — independent, secondary coverage. Do not fabricate it and do not write a promotional article (it will be removed and can harm reputation). If the brand genuinely meets notability, a neutral, well-sourced article is high value. If it does not yet, treat Wikipedia as a *goal that follows earned press*, not a task you can complete unilaterally. Route the earned-coverage work to `link-building`.

Order of effort: Wikidata now (low bar, direct payoff), Wikipedia when notability is genuinely met.

## The third-party source map

Parametric memory and live retrieval both lean on the *same* third-party sources an engine trusts for a vertical, so presence on these does double duty. Use the single canonical source map in `platform-factors.md` ("Source priority by vertical") rather than maintaining a second copy here — set priority by category rather than chasing the same generic sites for every brand.

Two rules for this map:

1. **Consistency over volume.** Ten profiles telling the same story beat thirty telling different ones. Update them all when a canonical fact changes.
2. **Earn, do not spam.** Placing genuine, useful mentions is execution that routes to `llm-seeding`; manipulative seeding is detectable and risks the trust signal you are trying to build.

## Author and expert entities

Engines attribute to people, not just brands. A named author with verifiable credentials raises citation odds for the pages they write.

- Give each substantive page a real author with a title and a linked bio.
- Keep that author's identity consistent across the site, LinkedIn, and any bylined external pieces — the author is an entity too.
- One credentialed expert quote per key page (name + title) is a strong citation signal and is cheap to add.

## Sequencing entity work against page work

Do not block page optimization on entity work — they run in parallel on different clocks.

1. **Week 0:** Fix the consistent-facts baseline (fast, internal, high leverage) *and* ship the page rewrites from Task 2. Page wins arrive in weeks; entity wins compound over months.
2. **Weeks 0-4:** Stand up or correct Wikidata; audit and align existing third-party profiles.
3. **Ongoing:** Earn the press and mentions that justify Wikipedia and deepen third-party presence (hand to `link-building` and `llm-seeding`).
4. **Re-measure** entity effects with the brand-knowledge probe in `measurement.md` — ask each engine "what is [brand]?" with no link and check whether the canonical facts come back correctly. Drift there is the signal to re-align.
