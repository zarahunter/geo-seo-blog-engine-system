# Platform Factors: How Each Engine Selects Sources

Per-platform behavior changes often. **Last reviewed 2026-06-18.** Treat the specifics below as a starting point and verify anything load-bearing before relying on it. The stable parts are the principles, not the percentages.

## Contents

- How each engine selects sources
- Source priority by vertical
- AI crawler access (robots.txt)

## How each engine selects sources

| Platform | How it answers | What to optimize for |
| --- | --- | --- |
| Google AI Overviews | Summarizes top-ranking pages | Correlates strongly with classic rankings, so traditional SEO is the floor |
| ChatGPT (search) | Live web plus parametric memory, cites sources | Leans reference and editorial sources; structure and authority |
| Perplexity | Always cites, links every claim | Favors recent, well-structured, authoritative content; leans academic and news |
| Gemini / AI Mode | Google index plus Knowledge Graph | Favors Google-owned and partner properties; entity consistency matters |
| Copilot | Bing-powered | Bing index plus authoritative sources |
| Claude | Web search plus training data | Structured, authoritative, well-sourced content |

Two durable takeaways. First, Google AI Overviews track classic rankings more closely than the others, so do not abandon traditional SEO for them. Second, the non-Google engines pull from a wider range than the top-ranked results, which is why a well-structured page on position two or three can still get cited.

## Source priority by vertical

Which third-party sources an engine trusts varies by category. Set priority accordingly rather than chasing the same generic sources for every client. (This table feeds both retrieval and entity work — see `entity-presence.md` for the parametric-memory side.)

| Vertical | Sources engines lean on |
| --- | --- |
| B2B SaaS | G2, Reddit, Capterra, TrustRadius |
| Health | Government domains, major hospitals, medical bodies |
| Finance | Bloomberg, regulators (for example the SEC), established financial press |
| Consumer / media | Major news outlets, YouTube, Reddit |
| E-commerce / product | Major retailers, expert review sites (Wirecutter-class), YouTube, Reddit |
| Local / multi-location | Google Business Profile, regional press, local subreddits, local review sites |
| Developer tools | GitHub, Stack Overflow, dev.to, openly-indexed official docs |
| MENA / Arabic | See `mena-arabic.md` for the regional source table |

For any query with local intent ("near me", a city, a physical-location business), the local entity layer (Google Business Profile, consistent NAP, location pages) usually matters more than page copy. See the local case in `hard-cases.md`. In YMYL verticals (health, finance, legal), engines lean on the institutional sources above so heavily that broad head terms have a structurally higher citation ceiling — plan around it (`hard-cases.md`, YMYL case).

## AI crawler access (robots.txt)

Each AI platform crawls with its own bot. Blocking a bot means that platform cannot cite the site, regardless of content quality. Audit robots.txt for Disallow rules against any of these.

| Bot | Platform |
| --- | --- |
| GPTBot, ChatGPT-User, OAI-SearchBot | OpenAI / ChatGPT |
| PerplexityBot, Perplexity-User | Perplexity |
| ClaudeBot, anthropic-ai, Claude-SearchBot | Anthropic / Claude |
| Google-Extended | Google Gemini and AI Overviews |
| Bingbot | Microsoft Copilot via Bing |

Bot names change as vendors add or rename crawlers, so confirm the current list before writing a final config.

The business decision: allowing these bots enables citation but also permits training use of the content. One middle ground is to allow the search and answer crawlers above while disallowing training-only crawlers such as CCBot (Common Crawl). Make this choice explicit with the user rather than defaulting silently.

Example allow-the-answer-engines configuration (verify bot names first):

```
User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Disallow: /
```
