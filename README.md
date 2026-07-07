# The GEO-SEO Blog Engine System

A complete, AI-run **blog factory**: you give a topic (or the engine finds its own), and the
system researches, writes, optimizes for classic search (SEO) *and* AI answer engines (GEO),
fact-checks, scores against quality gates, adds licensed images, and publishes a standalone
HTML page. You stay the editor-in-chief; the gates do the heavy lifting.

This is the **system**. It contains all the procedures (SOPs), the 12 content templates, the
quality tools, and the autopilot — but no brand, no posts, and no data. Make it yours in five
steps.

## What you need first (one-time installs)

1. **Claude Code** — the AI runs the whole factory through it.
   Install from [claude.com/claude-code](https://claude.com/claude-code) (desktop app, terminal,
   or VS Code extension). You need a paid Claude plan (Pro or above).
2. **Git** — to download this system. Comes with macOS/Linux; Windows: [git-scm.com](https://git-scm.com).
3. **Python 3.11+** — powers the quality scorer and page builder. Check with `python3 --version`;
   install from [python.org](https://www.python.org/downloads/) if missing.

## Get it running (about 15 minutes)

**Step 1 — Download the system.**
```bash
git clone https://github.com/zarahunter/geo-seo-blog-engine-system.git my-blog-engine
cd my-blog-engine
```

**Step 2 — Install the AI skills.** Claude Code loads skills from `~/.claude/skills/`.
The two optimizer skills ship inside this repo; the `/blog` writing suite comes from its
public repo:
```bash
# The SEO + GEO optimizer skills (included in this repo)
mkdir -p ~/.claude/skills
cp -R equipment/skills/on-page-seo equipment/skills/ai-seo ~/.claude/skills/

# The /blog writing suite (30 sub-skills)
git clone https://github.com/AgriciDaniel/claude-blog /tmp/claude-blog
cp -R /tmp/claude-blog/skills/* ~/.claude/skills/
```

**Step 3 — Install the Python tools.**
```bash
python3 -m venv equipment/.venv
equipment/.venv/bin/pip install -r equipment/requirements.txt
```

**Step 4 — Make it yours (the placeholders).** Open these four files and replace every
`{{PLACEHOLDER}}`:
- `blueprints/brand/BRAND.md` — who you are, who you write for, what you refuse to publish.
- `blueprints/brand/VOICE.md` — how you sound (tone, pronouns, style rules).
- `autopilot/config.yaml` — niche, thesis, seed topics, domain, author identity (a real person!), timezone.
- `blueprints/calendar.md` — 2-3 pillar topics with their supporting spokes.

The writer loads these before every post: the more specific you are, the better every article.

**Step 5 — Set up tracking (recommended).** Create a tracker (Airtable base or Google Sheet)
with three tables — Keyword Universe, Content Pipeline, AI-Citation Log — using the column
sets in `blueprints/sops/07-produce-loop.md` ("The intelligence layer"). It is the engine's
memory of what it produced and whether AI engines cite you.

**Step 6 — Start the engine.** Open the repo folder in Claude Code and say:
> "run the weekly research sprint"

(fills your topic backlog with scored, winnable topics), then:
> "produce the next post"

(runs the full research → write → optimize → QA → publish pipeline on the top topic).
`CLAUDE.md` teaches the AI how to drive everything — you don't need to memorise the SOPs.

**Publishing:** the built site lands in `publish/` as plain HTML — deploy it anywhere
(e.g. [Vercel](https://vercel.com), free tier works). Configure `publish/config` at first publish.

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

