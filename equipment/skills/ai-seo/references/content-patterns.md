# Content Patterns: Extractability and Block Templates

How to structure content so AI engines can pull a clean, self-contained passage. Every block here is designed to read correctly with zero surrounding context, because that is the unit engines extract.

## Contents

- Extractability checklist
- The passage-diff method (why a competitor won)
- Block templates (definition, comparison, step, pros/cons, FAQ, statistic)
- Structural rules

## Extractability checklist

Run this against any priority page. Each failed row is a likely reason a competitor gets cited instead.

| Check | Why it matters |
| --- | --- |
| Direct answer in the first paragraph (40 to 60 words) | Engines grab the lead; a buried answer is skipped |
| Every key claim works as a standalone sentence | Extracted passages lose their surrounding context |
| Statistics include a specific number, a date, and a linked source | Sourced numbers are the strongest citation signal |
| Comparison content is a table, not prose | Tables are cleanly extractable for "X vs Y" |
| Process content is a numbered list, not a paragraph | Step lists map directly to "how to" answers |
| FAQ section phrased as real questions | Matches how people prompt assistants |
| One idea per paragraph | Mixed paragraphs are hard to extract cleanly |
| Headings phrased as questions or clear topics | Heading-to-query match drives retrieval |
| Author named with relevant credentials | Authority signal the engine can attribute |
| Visible "last updated" date | Freshness is a ranking and trust signal |
| No promotional tone, no keyword stuffing | Both measurably suppress citation |
| Schema present (Article, FAQPage, HowTo, Product) | Gives the engine structured context |

## The passage-diff method (why a competitor won)

When a competitor is cited and you are not, "their page is better" is not a diagnosis. Find the *exact passage* the engine quoted and diff it against your closest equivalent. This is the sharpest tool in the audit.

1. **Recover the cited passage.** Take a distinctive phrase from the AI answer and search it back into the competitor's cited page. Citations are usually near-verbatim, so this locates the winning block.
2. **Find your equivalent block** — the passage on your page that *should* have answered the same query.
3. **Diff on five axes.** Name which one explains the win:
   - **Self-contained** — does it read correctly with zero surrounding context?
   - **Specific** — concrete numbers, dates, named sources vs adjectives?
   - **Fresh** — visible recent date?
   - **Structured** — table/list vs prose for the intent?
   - **Third-party presence** — did they win because the cited source is a site you are simply absent from? (If so, the fix is off-page; route to `llm-seeding` or `link-building`, not a rewrite.)
4. **Fix the one axis that explains the win**, not all five reflexively. Usually it is specificity or self-containment.

A full worked diff is in `worked-example.md`.

## Block templates

### Definition block (for "what is X")

Open the section with one tight sentence that defines the term, then expand.

```
[Term] is [plain-language definition in one sentence, no marketing].
It [what it does or why it matters] and is used by [who] to [outcome].
```

Keep the first sentence under 25 words so it lifts cleanly into an answer.

### Comparison table (for "X vs Y" and "best alternatives")

Prose comparisons get cited far less often than tables. Use a table with concrete criteria and keep it fair, because visibly biased comparisons are penalized.

```
| Criterion | Option A | Option B |
| --- | --- | --- |
| Pricing | [specific] | [specific] |
| Best for | [use case] | [use case] |
| Key limitation | [honest] | [honest] |
```

### Roundup / "top N" block (for "best X" and "top N X")

A ranked list where each entry is a self-contained, sourced block — the engine can quote a single entry without the rest of the page. Include competitors and a real reason per entry; a list that only flatters one product reads as marketing and is skipped.

```
## [N] best [X] for [audience] (as of [date])

### 1. [Option] — best for [specific segment]
[One self-contained sentence on what it is and why it ranks here, with a
concrete fact.] [Pricing or a key spec, dated.]

### 2. [Option] — best for [different segment]
...
```

If the roundups the engines actually cite are ones you do not control, rewriting your own page will not help — the fix is off-page (see `hard-cases.md`).

### Step block (for "how to X")

```
1. [Action verb] [object]. [One clarifying sentence if needed.]
2. [Action verb] [object].
3. [Action verb] [object]. Expected result: [outcome].
```

State prerequisites before step 1 and the expected outcome at the end.

### Pros and cons block (for evaluation queries)

```
Strengths: [specific], [specific], [specific].
Limitations: [honest], [honest].
Best fit: [who it suits]. Poor fit: [who it does not].
```

Including real limitations raises trust and citation odds. An all-positive block reads as marketing.

### FAQ block

Phrase each question exactly as a person would type it to an assistant, then answer in the first sentence.

```
### [Natural-language question]?
[Direct answer in the first sentence.] [One or two sentences of support.]
```

### Statistic block (the highest-value citation unit)

```
[Specific number] of [population] [did or experienced X] in [year],
according to [named source, linked]. [One sentence of context.]
```

Cite the original research, not a summary of it. Add a date to every number. Original first-party data outperforms aggregated data.

## Structural rules

- Lead every section with the answer. Do not make the reader (or the engine) wait for it.
- Keep the key answer passage to roughly 40 to 60 words. That is the sweet spot for extraction.
- Use H2 and H3 headings that mirror how the query is phrased.
- One clear idea per paragraph.
- Prefer concrete nouns and numbers over adjectives. "Processes 10,000 transactions per second" beats "blazing fast".
