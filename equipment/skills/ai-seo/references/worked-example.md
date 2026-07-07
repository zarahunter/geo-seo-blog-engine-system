# Worked Example: Audit to Rewrite, One Page

This is the calibration reference. It runs the full method on a single realistic page so the *quality bar* is concrete, not abstract. The scenario is invented but typical: a mid-market project-management SaaS, "Tasklane", that ranks on page one for its category yet never gets cited in AI answers for "best project management tool for agencies".

Read this once before any optimize or create task. The point is not the specific copy; it is the *size of the gap* between the before and after, and the reasoning that closes it.

## Step 1 — the test set (excerpt)

Three of the twenty priority queries, phrased as a person prompts an assistant:

- "What's the best project management tool for a small creative agency?"
- "Asana vs Tasklane for agencies — which is better?"
- "How do I track billable hours across client projects?"

## Step 2 — run, three times each, record

| Query | Platform | Runs cited / total | Who won | Their page |
| --- | --- | --- | --- | --- |
| best PM tool for creative agency | ChatGPT | 0 / 3 | Teamwork | /agencies guide |
| best PM tool for creative agency | Perplexity | 0 / 3 | Teamwork, Productive | two comparison posts |
| Asana vs Tasklane for agencies | Perplexity | 1 / 3 | a third-party blog | review roundup |
| track billable hours across projects | ChatGPT | 0 / 3 | Harvest | /how-to docs page |

## Step 3 — passage diff (the part most audits skip)

For "best PM tool for creative agency", the cited Teamwork passage (found by searching the AI answer's phrasing back into their page) was:

> "Teamwork is built for client work: time tracking, billing, and retainer management are native, and agencies on the Grow plan ($10.99/user/month, billed annually as of 2026) get unlimited client users at no extra seat cost."

Tasklane's closest equivalent passage was:

> "Tasklane is the all-in-one platform that helps modern teams do their best work. Trusted by thousands of agencies worldwide, our intuitive interface and powerful features make project management effortless."

Diff on the five axes:

| Axis | Teamwork (won) | Tasklane (lost) |
| --- | --- | --- |
| Self-contained | Yes — names the audience and the proof in one block | No — "best work" means nothing extracted alone |
| Specific | Native time tracking, billing, retainers; a real price; a date | Adjectives only ("intuitive", "powerful") |
| Fresh | "as of 2026" | No date |
| Structured | Tight, liftable sentence | Marketing run-on |
| Third-party | — | — (not the deciding axis here) |

**The one axis that explains the win: specificity.** Teamwork answered the actual question (agency = client billing) with concrete facts a model can quote and attribute. Tasklane wrote a slogan. No amount of schema or backlinks fixes a slogan.

## Step 4 — access and extractability checks

robots.txt was clean (no AI bots blocked). The extractability checklist (see `content-patterns.md`) failed five rows: no direct answer in the lead, claims not self-contained, no sourced statistics, comparison done in prose, no visible date.

## Step 5 — the prioritized output

| Query | Who wins | Diff axis | Highest-leverage fix |
| --- | --- | --- | --- |
| best PM tool for creative agency | Teamwork | Specificity | Rewrite the lead to name the agency use case with concrete, dated capability facts |
| Asana vs Tasklane | third-party blog | Third-party presence | Build an owned comparison table; pitch the blog (route to `link-building`) |
| track billable hours | Harvest | Structure | Convert the how-to from prose to numbered steps + HowTo schema |

---

## The rewrite: before and after

Taking the first query's page. This is the transformation the audit demands.

### BEFORE (the page that never gets cited)

```
# Tasklane: Project Management Software for Modern Teams

Tasklane is the all-in-one platform that helps modern teams do their best
work. Trusted by thousands of agencies worldwide, our intuitive interface
and powerful features make project management effortless.

Whether you're a growing startup or an established enterprise, Tasklane
scales with you. Our customers love how easy it is to get started, and our
world-class support team is always here to help.

Ready to transform how your team works? Start your free trial today and
discover why Tasklane is the smarter choice for project management.
```

What is wrong, in GEO terms: no target query in the H1, no answer in the lead, every sentence is context-dependent marketing, zero specifics, zero sources, zero date, a call-to-action where a fact should be. It is a retrieval miss *and* a citation miss.

### AFTER (built to be quoted)

```
# Best Project Management Tool for Creative Agencies (2026)

For creative agencies, the project management tool that gets cited most
often for client work is one with native time tracking, billing, and
retainer management — not a generic task board. Tasklane covers these in
its Agency plan ($12/user/month, billed annually, as of June 2026),
including unlimited client guest seats.

## What makes a PM tool right for an agency?

Agencies need three things a generic tool rarely does well:

| Need | Why it matters | Tasklane |
| --- | --- | --- |
| Billable time tracking | Revenue is hours; untracked time is lost margin | Native, per-task timers |
| Retainer & budget caps | Scope creep eats retainers silently | Per-client budget alerts at 80% and 100% |
| Client guest access | Clients review without buying seats | Unlimited guests on Agency plan |

## How much does it cost?

Tasklane Agency is $12/user/month billed annually as of June 2026.
Client guest seats are included at no per-seat cost. (Verify current
pricing on the pricing page before quoting.)

## Tasklane vs the alternatives for agencies

| Criterion | Tasklane | Asana | Teamwork |
| --- | --- | --- | --- |
| Native billable time tracking | Yes | Add-on | Yes |
| Client guest seats | Unlimited (Agency) | Limited | Unlimited (Grow) |
| Best for | Agencies billing hourly | Cross-functional teams | Agencies on retainers |

Honest limitation: Tasklane has no built-in invoicing, so agencies that
want billing end-to-end in one tool may prefer Teamwork.

## Frequently asked questions

### Is Tasklane good for a small creative agency?
Yes, for agencies that bill by the hour and want native time tracking
without an add-on. It is a weaker fit if you need invoicing in the same
tool.

### Can clients access Tasklane without paying for a seat?
Yes. The Agency plan includes unlimited client guest seats as of June 2026.

---
Last updated: June 2026 · Author: Priya Nair, Head of Agency Success,
Tasklane (8 years in agency operations)
```

### Why each change earns citations

- **H1 = the query.** "Best project management tool for creative agencies (2026)" mirrors the prompt, driving retrieval.
- **Lead answers in ~55 words, self-contained.** It states the *criterion* (native billing for client work) before naming the product — that framing reads as analysis, not a pitch, which is exactly what engines quote.
- **A table replaced the prose comparison.** Tables are the highest-citation format for "vs" and "best for" intents.
- **Specifics replaced adjectives.** "$12/user/month, billed annually, as of June 2026", "budget alerts at 80% and 100%" — every number is liftable and attributable.
- **An honest limitation was added.** "No built-in invoicing" raises trust and citation odds; an all-positive page reads as marketing and gets skipped.
- **A visible date and a credentialed author** supply the freshness and authority signals engines attribute.
- **The CTA was removed from the answer zone.** Promotional tone suppresses citation; it lives (if anywhere) below the fold, not in the passage an engine extracts.

### The measurable difference

The before page fails 5 of 12 extractability rows and contains zero quotable passages. The after page passes all 12 and contains at least four independently citable blocks (the lead, the needs table, the pricing line, each FAQ answer). That is the gap between "ranks but never cited" and "cited". Re-test after publishing and track citation velocity (`measurement.md`) rather than assuming the change worked.

---

## Second example: when the rewrite is the wrong fix

The first example resolves with a page rewrite. Many do not — and reflexively rewriting wastes the engagement. This second case is deliberately *structurally different* so the lesson is "diagnose, then choose the fix", not "always rewrite".

Scenario: the same Tasklane, query "top project management tools for agencies in 2026". Across three runs, ChatGPT and Perplexity both cite a single article — "The 12 Best Agency PM Tools (2026)" on an independent industry blog — and list its top three. Tasklane is mentioned at #9 in that article, one bland line, no link in the AI answer.

**Passage diff result:** the deciding axis is *third-party presence*, not anything on Tasklane's own site. The engine is not quoting Tasklane's page at all; it is quoting the blog's list. Tasklane's lead could be perfect and nothing would change, because the lead is not what got retrieved.

**So the fix is off-page** (`hard-cases.md`, "listicle you cannot edit"):

| Move | Why | Route to |
| --- | --- | --- |
| Pitch the blog to re-rank Tasklane up and fix the bland line, with a concrete agency-billing fact | The engine quotes that list; changing the list changes the answer | `link-building` |
| Publish Tasklane's own fair "best agency PM tools" roundup including competitors | Gives engines an alternative citable list | this skill (roundup template) + `topical-authority` for the cluster |
| Win "best PM tool for agencies that bill hourly" | The generic top-12 lists are thin on the specific segment; easier to own | this skill, page work |

The tell that you are in this case: the cited URL is not yours and is not one you can edit. When the audit's diff axis comes back "third-party presence", stop reaching for the page editor — the leverage is in `hard-cases.md` and the off-page hand-offs.
