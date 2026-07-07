# Equipment — Skills & Scripts Index

The **equipment** engine is the toolbox the Architect uses to run the pipeline. It has two
parts: **vendored Python scripts** (live in this repo) and **referenced Claude skills**
(installed globally, invoked by name).

---

## Part 1 — Vendored Python scripts (`equipment/scripts/`)

Run them with the project venv: `equipment/.venv/bin/python equipment/scripts/<name>.py ...`
(Python 3.11+. Core deps `textstat`, `beautifulsoup4` installed in `equipment/.venv`.)

| Script | Stage | What it does | Key invocation |
|--------|-------|-------------|----------------|
| `analyze_blog.py` | QA | 5-category, 100-point quality score | `analyze_blog.py posts/<slug>.md --format markdown` |
| `blog_preflight.py` | QA | 5-gate delivery contract (blocking) | `blog_preflight.py --draft <folder> --strict` |
| `blog_render.py` | Publish | Render markdown → standalone `.html` (+ optional `.pdf`) | `blog_render.py --md posts/<slug>.md --out-dir publish/<slug>` |
| `generate_hero.py` | Write/Publish | Hero image generation ladder | `generate_hero.py --help` |
| `cognitive_load.py` | QA | Per-section concept-density analysis | `cognitive_load.py posts/<slug>.md` |
| `discourse_research.py` | Research | API-free last-30-day discourse synthesis | `discourse_research.py --help` |
| `lint_prose.py` | QA | Prose hygiene (forbidden chars: em-dash, en-dash, ` -- `) | `lint_prose.py --root posts` |
| `load_untrusted_root.py` | Safety | CSPRNG-nonce fences BRAND/VOICE/DISCOURSE before loading | used by `/blog` internally |
| `sync_flow.py` | Maint. | Pull FLOW framework references from upstream | `sync_flow.py --help` |

Source: vendored from `AgriciDaniel/claude-blog` `scripts/`. To refresh, re-clone that repo and
re-copy `scripts/*.py`.

---

## Part 2 — Claude skills (invoked by name during the pipeline)

These are the "smart" half of the equipment. Two sources, two vendoring states (below).

### From `zarahunter/seo-geo-skills` — the SEO + GEO plugin — **VENDORED**
Copied into `equipment/skills/` (version-controlled with this repo) AND installed globally at
`~/.claude/skills/` (which is what makes them invocable as skills). To refresh: re-clone the repo
and re-copy into `equipment/skills/`.

| Skill | Stage | Use | In repo |
|-------|-------|-----|---------|
| `on-page-seo` | Optimize | Classic Google/Bing ranking: search intent, keyword placement, title tag, meta description, heading hierarchy, internal links, alt text | `equipment/skills/on-page-seo/` |
| `ai-seo` (GEO) | Optimize | Get retrieved + cited in AI answers (ChatGPT, Perplexity, AI Overviews, Gemini, Copilot, Claude). Entity presence, AI-first content, hard cases, **MENA / Arabic playbook** | `equipment/skills/ai-seo/` |

### From `AgriciDaniel/claude-blog` — the `/blog` suite — **REFERENCED** (scripts vendored, skills global)
The 9 Python scripts ARE vendored (Part 1). The 30 sub-skills are NOT copied in — they're invoked
from the global install (the suite is large; the scripts are the load-bearing part for this factory).

| Skill | Stage | Use |
|-------|-------|-----|
| `/blog write <topic>` | Write | Full article generation (template + answer-first + sourced stats) |
| `/blog rewrite <file>` | Optimize | Optimize an existing draft |
| `/blog analyze <file>` | QA | Quality scoring (wraps `analyze_blog.py`) |
| `/blog brief <topic>` | Research | Content brief + competitive gaps |
| `/blog schema <file>` | Optimize | JSON-LD structured data |
| `/blog geo <file>` | Optimize | AI-citation readiness audit |
| `/blog image` | Write | Hero / inline image generation |
| (+ 23 more sub-skills) | — | See the `/blog` orchestrator |

---

## How equipment maps to the pipeline

```
Intake → Research → Write → Optimize → QA → Publish
            │          │        │        │       │
   discourse_research  /blog   on-page  analyze  blog_render
   /blog brief         write   -seo     _blog    (→ standalone HTML)
                       /blog    ai-seo   blog_
                       image    /blog    preflight
                                schema
                                /blog geo
```
