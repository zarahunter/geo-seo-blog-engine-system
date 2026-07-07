# The GEO-SEO Blog Engine System

A complete, AI-run **blog factory**: you give a topic (or the engine finds its own), and the
system researches, writes, optimizes for classic search (SEO) *and* AI answer engines (GEO),
fact-checks, scores against quality gates, adds licensed images, and publishes a standalone
HTML page. You stay the editor-in-chief; the gates do the heavy lifting.

This is the **system**. It contains all the procedures (SOPs), the 12 content templates, the
quality tools, and the autopilot — but no brand, no posts, and no data. Make it yours in five
steps.

## Setup (do these in order)

1. **Fill in your brand.** Edit `blueprints/brand/BRAND.md` and `blueprints/brand/VOICE.md` —
   replace every `{{PLACEHOLDER}}`. The writer loads these before every post; the quality of
   your whole blog depends on how specific you are here.
2. **Fill in the control panel.** Edit `autopilot/config.yaml` — your niche, thesis, seed
   topics, domain, author identity (a real person!), and timezone. Every `{{PLACEHOLDER}}`
   must go.
3. **Install the tools.**
   ```bash
   python3 -m venv equipment/.venv
   equipment/.venv/bin/pip install -r equipment/requirements.txt
   ```
4. **Plan your clusters.** Edit `blueprints/calendar.md` — 2-3 pillar topics with their spokes.
5. **Set up tracking.** Create your tracker (Airtable base or Google Sheet) with three tables —
   Keyword Universe, Content Pipeline, AI-Citation Log — using the column sets described in
   `blueprints/sops/07-produce-loop.md` ("The intelligence layer"). Optional but strongly
   recommended: it is the engine's memory.

Then open the repo in Claude Code and say: **"run the weekly research sprint"** (fills your
topic backlog), followed by **"produce the next post"** (runs the full pipeline on the top
topic). `CLAUDE.md` teaches the AI how to drive everything.

## How it's organised (the three engines)

| Engine | What it is | Where |
|--------|-----------|-------|
| 🧠 **Architect** | The AI that thinks, plans, decides | `CLAUDE.md` + `architect/` |
| 📐 **Blueprints** | The SOPs, templates, brand — the *how* | `blueprints/` |
| 🔧 **Equipment** | The scripts and skills — the *tools* | `equipment/` |

The Architect runs the Blueprints using the Equipment. It never freelances.

## The pipeline (each stage has a written SOP in `blueprints/sops/`)

Intake → Research → Write → Optimize (SEO + GEO) → QA gates → Images → Publish → Track → Refresh.

Hard rules the gates enforce on every post: no fabricated statistics (every number traces to a
named source), no paragraph over 150 words, clean heading structure, at most one
self-promotional mention, and a minimum quality score of 80–85/100 before anything ships.

## License & author

Created by **Zara Hunter** ([Eduk8agentic](https://eduk8agentic.com) · [LinkedIn](https://www.linkedin.com/in/zarahunter/)).
Released under the [MIT License](LICENSE) — free to use, adapt, and build your own blog system on,
with attribution preserved in the license notice.

## Requirements

- Python 3.11+ (for the quality/render tools)
- Claude Code with the `blog` suite and `on-page-seo` / `ai-seo` skills installed
- A place to deploy static HTML (e.g. Vercel — configure `publish/config` at first publish)
