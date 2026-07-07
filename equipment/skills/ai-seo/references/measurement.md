# Measurement: Testing, Tracking, and Tools

AI answers are non-deterministic and citation share drifts week to week. A single check is noise. This file covers how to test properly, what to track, and which tools help.

## Contents

- How to obtain the AI answers (do this before anything else)
- Why one run is not enough
- The test-set method
- Tracking template
- The brand-knowledge probe (entity check)
- DIY monthly protocol (no tools)
- What to track over time
- Monitoring tools

## How to obtain the AI answers (do this before anything else)

The entire audit rests on observing what the engines actually answer and recovering the exact passage they cited. That observation is not free, and you may not be able to do it directly. Pick the path that matches your access before running Task 1.

1. **Live runs (best fidelity).** If you can open ChatGPT, Perplexity, and Google, run each query yourself, three-plus times, and copy the answer text and the cited URLs. This is the default the rest of this file assumes.
2. **Tool-assisted (best at scale).** If an AI-visibility data source is connected, use it to pull citations programmatically instead of eyeballing. Brand-Radar-class tools expose exactly the fields the audit needs — cited domains, cited pages, and the AI responses themselves, often with history. In this environment those may be available as MCP tools (for example Ahrefs Brand Radar endpoints for AI responses, cited domains, and cited pages). Prefer these for any run beyond a handful of queries; they remove the non-determinism problem by aggregating across many responses. For full multi-platform share-of-voice programs, still hand off to `ai-visibility-monitoring`.
3. **Operator-paste fallback (when you have no access).** If you are running this skill without live AI access and no tool is connected, do not fabricate or assume the answers. Ask the user to run the test set and paste, per query: the answer text, who was cited, and the cited URLs. Then do the passage diff on what they paste. State explicitly that you are working from their captures, not your own runs.

Caveats that bite regardless of path:

- **Account, region, and personalization shift results.** A logged-in account with memory, or a different country, can change citations. Note the account/region used so reruns are comparable.
- **Recency shifts results.** "Best X in 2026" answers move as the year progresses and as the index refreshes. Re-date the test set.
- **Never present an assumed answer as observed.** If you could not obtain a real answer for a query, mark that row "not observed" rather than guessing who won.

## Why one run is not enough

The same prompt can return different sources on different runs, and the source mix for a query can shift substantially inside a few weeks. So two rules: run each query multiple times before drawing a conclusion, and re-test on a fixed cadence rather than treating any snapshot as settled.

## The test-set method

1. **Choose 10 to 20 priority queries.** Phrase each as a full question the way a person prompts an assistant, not as a keyword. Cover several intents: category definition, "best X for Y", "X vs competitor", "how to [problem]", and pricing.
2. **Run each query at least three times** on each platform you care about (ChatGPT, Perplexity, Google AI Overviews at minimum). More runs give a more stable read.
3. **Record, per run:** whether an AI answer appeared, whether the user was cited, who was cited instead, and the exact URL pulled.
4. **Aggregate across runs** into a citation rate per query (for example, cited in 2 of 3 runs), not a single yes or no.

## Tracking template

| Query | Platform | Runs cited / total | Competitor cited | Their page | Likely reason | Fix |
| --- | --- | --- | --- | --- | --- | --- |
| [full question] | ChatGPT | 1 / 3 | [brand] | [url] | [extractability / sourcing / freshness] | [single highest-leverage action] |

## The brand-knowledge probe (entity check)

Retrieval tests above measure page citations. To measure *parametric memory* (what the model knows without a live lookup), probe the entity directly. This is the measurement for Task 5 / `entity-presence.md`.

1. With web access **off** where the platform allows it, ask each engine: "What is [brand]?", "Who founded [brand]?", "What category is [brand] in?", "Who is [brand] for?"
2. Check the answers against the canonical facts you locked in the consistent-facts baseline.
3. Log three outcomes per fact: **correct**, **wrong**, or **absent** (the model does not know). Wrong is worse than absent — it signals contradictory sources to go fix.
4. Re-probe quarterly. Movement from absent to correct is the lagging signal that entity work is landing; drift from correct to wrong is the signal to re-align sources.

## DIY monthly protocol (no tools)

For a user who wants a routine they can run themselves without paying for a platform:

1. Keep a fixed list of the top 20 queries.
2. Once a month, run each through ChatGPT, Perplexity, and Google, three runs each.
3. Log cited or not, who else was cited, and which page.
4. Compare against last month. Watch the direction of travel, not the absolute number on any single day.

## What to track over time

- **Citation rate**: how often the brand is cited for its priority queries.
- **Share of AI voice**: brand citations versus named competitors.
- **Citation velocity**: how quickly a newly published page starts appearing in AI answers. This is a leading indicator; rising velocity predicts future visibility.
- **Brand-knowledge accuracy**: the share of canonical facts the engines return correctly (from the probe above).
- **Sentiment**: how the AI describes the brand when it does cite it.
- **Source attribution**: which specific pages get cited, so effort concentrates on what works.

## Monitoring tools

Hand off to `ai-visibility-monitoring` for serious multi-platform tracking. Tool coverage and naming change, so confirm current capabilities before recommending one to a user. Categories that exist in this space:

- Multi-platform share-of-voice trackers (ChatGPT, Perplexity, Gemini, Claude, Copilot, AI Overviews).
- Brand-mention and sentiment monitors.
- Keyword-to-AI-visibility mappers that connect classic SEO terms to AI citation.

Treat any single tool's citation-share numbers as that tool's measurement, not ground truth, since methodologies differ widely (share of total citations versus frequency of appearance are different metrics and are often confused).
