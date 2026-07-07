# GEO-SEO-BLOG — The Three-Engine Blogging System

This repo is a **blog factory**. You give a topic; the system researches, writes, optimizes for
both classic search and AI answer engines, QAs against quality gates, and publishes a standalone
HTML page to Vercel.

It runs on the **three-engine model**. Everything in this repo belongs to exactly one engine.

| Engine | What it is | Where it lives |
|--------|-----------|----------------|
| 🧠 **Architect** | The brain that thinks, plans, decides — that's **you, Claude** | this `CLAUDE.md` + `architect/` |
| 📐 **Blueprints** | The SOPs, plans, templates, and brand/voice — the *how* | `blueprints/` |
| 🔧 **Equipment** | The Python scripts and skills — the *tools* | `equipment/` |

The Architect never freelances. It runs the **Blueprints** using the **Equipment**.

---

## When the user gives a topic, do this

Run the 6-stage pipeline. Each stage has a blueprint SOP — **read the SOP, then execute it.**

| # | Stage | Blueprint | Primary tool |
|---|-------|-----------|--------------|
| 1 | Intake | `blueprints/sops/01-intake.md` | **`trend-scout` agent** (find/rank hot angles) → log to `architect/topic-queue.md` |
| 2 | Research | `blueprints/sops/02-research.md` | `/blog brief` + `discourse_research.py` → `research/<slug>.md` |
| 3 | Write | `blueprints/sops/03-write.md` | `/blog write` + template + brand → `posts/<slug>.md` |
| 4 | Optimize | `blueprints/sops/04-optimize-seo-geo.md` | **`on-page-seo` → `ai-seo`** (yours) + `/blog schema` |
| 5 | QA | `blueprints/sops/05-qa.md` | `analyze_blog.py` + `lint_prose.py` + **`/blog seo-check`** + **`/blog geo`** (≥80/100, no hard-rule violations) |
| 6 | Publish | `blueprints/sops/06-publish.md` | `blog_render.py` → `publish/`; deploy to Vercel |

**Iteration:** if QA fails, loop back to stage 3/4. Max 3 iterations. On the 3rd failure, STOP and
show the user the diagnostic — never ship a sub-80 post or hand them a broken draft to "fix."


> **Skill routing (the two repos overlap):** `blueprints/sops/00-skill-routing.md` is the single
> source of truth. Short version — **your `seo-geo-skills` OPTIMIZE** (`on-page-seo`, `ai-seo`);
> **claude-blog's skills VALIDATE** (`/blog seo-check`, `/blog geo`). Never use the audits as
> optimizers or vice-versa. `/blog schema` owns JSON-LD (uncontested).

---

## The engines in detail

### 🧠 Architect (`architect/`)
Your working memory.
- `topic-queue.md` — the job board; every topic + its status.
- `decisions/<slug>.md` — one decision log per post (angle, keyword, template, sources, trail).
  Copy `decisions/_TEMPLATE.md` at intake.

### 📐 Blueprints (`blueprints/`)
The repeatable "how". **Read these; don't improvise.**
- `sops/` — the 6 numbered stage procedures above. These are the source of truth for *how* to run
  each stage.
- `brand/BRAND.md` + `brand/VOICE.md` — positioning, audience, taboo phrases, tone, sentence
  rules. **Load these before writing or optimizing.** (Drafts marked `[CONFIRM]` need the owner's input.)
- `templates/` — 12 content templates (how-to-guide, listicle, comparison, pillar-page, ...).
  Pick one at intake.
- `calendar.md` — topic clusters, content mix, cadence, freshness/decay plan.

### 🔧 Equipment (`equipment/`)
The tools. Full index + invocations in `equipment/SKILLS.md`.
- `scripts/` — 9 vendored Python scripts (`analyze_blog.py`, `blog_render.py`, `blog_preflight.py`,
  `discourse_research.py`, `lint_prose.py`, `generate_hero.py`, ...). Run via the project venv:
  **`equipment/.venv/bin/python equipment/scripts/<name>.py ...`**
- `skills/` — **vendored** `on-page-seo` + `ai-seo` (from `zarahunter/seo-geo-skills`, incl. the
  MENA/Arabic playbook). Also installed globally, which is what makes them invocable as skills.
- **Referenced** (global install, not copied in): the `/blog` suite from `AgriciDaniel/claude-blog`
  (its 9 scripts ARE vendored above; the 30 sub-skills are invoked from the global install).

---

## Hard rules (never violate — these are the quality gates)
- **No fabricated statistics.** Every number traces to a Tier 1–3 source in `research/<slug>.md`.
- **No paragraph > 150 words.** No skipped heading levels (H1→H2→H3).
- **No em-dash, en-dash, or `--` in prose** — `lint_prose.py` enforces this in QA.
- **≤ 1 self-promotional mention** per post (author-bio context only).
- **Pass before publish:** score ≥ 80/100 AND zero hard-rule violations.
- The **gates are the first reviewer, never the user.**

---

## Artifact map (where each thing lands)
```
topic ─▶ architect/topic-queue.md + architect/decisions/<slug>.md   (intake)
      ─▶ research/<slug>.md                                          (research)
      ─▶ posts/<slug>.md                                             (write + optimize)
      ─▶ score in architect/decisions/<slug>.md                      (QA)
      ─▶ publish/posts/<slug>/index.html + publish/index.html        (publish)
```

## Setup notes
- Python venv with core deps lives at `equipment/.venv` (`textstat`, `beautifulsoup4`).
  Recreate with: `python3 -m venv equipment/.venv && equipment/.venv/bin/pip install -r equipment/requirements.txt`
- The Vercel deploy target is set once in `publish/config` (asked at first publish).
