#!/usr/bin/env python3
"""Build the blog home page and all site-level GEO files.

Scans publish/posts/<slug>/index.html and reads the matching source frontmatter
from posts/<slug>.md (title, description, date, dateModified) to build:
  - publish/index.html   the newest-first listing (home page)
  - publish/sitemap.xml  every URL with lastmod
  - publish/rss.xml      the feed
  - publish/robots.txt   allows AI crawlers (foundational for GEO) + Sitemap line
  - publish/llms.txt      AI-discovery summary + key URLs (emerging standard)

Dependency-free: a tiny frontmatter parser, no PyYAML required.

Usage:
    python3 publish/build_index.py [--site-title "My Blog"] \
        [--base-url "https://example.com"] [--description "..."]
"""
from __future__ import annotations

import argparse
import html
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_SRC = ROOT / "posts"
PUBLISH = ROOT / "publish"
PUBLISH_POSTS = PUBLISH / "posts"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# AI crawlers we explicitly welcome. Blocking these = invisible to AI answers.
AI_CRAWLERS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User",
    "ClaudeBot", "Claude-User", "anthropic-ai", "Google-Extended", "Applebot-Extended",
    "CCBot", "Bingbot", "Amazonbot", "Meta-ExternalAgent",
]


def parse_frontmatter(md_path: Path) -> dict:
    """Minimal YAML-ish frontmatter parser for flat key: value pairs."""
    meta: dict[str, str] = {}
    if not md_path.exists():
        return meta
    text = md_path.read_text(encoding="utf-8", errors="replace")
    m = FM_RE.match(text)
    if not m:
        return meta
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta


def collect_posts() -> list[dict]:
    posts = []
    if not PUBLISH_POSTS.exists():
        return posts
    for post_dir in sorted(PUBLISH_POSTS.iterdir()):
        if not post_dir.is_dir():
            continue
        slug = post_dir.name
        html_file = post_dir / "index.html"
        if not html_file.exists():
            candidates = sorted(post_dir.glob("*.html"))
            if not candidates:
                continue
            html_file = candidates[0]
        meta = parse_frontmatter(POSTS_SRC / f"{slug}.md")
        date_pub = meta.get("date", "")
        posts.append(
            {
                "slug": slug,
                "title": meta.get("title", slug.replace("-", " ").title()),
                "description": meta.get("description", ""),
                "date": date_pub,
                "modified": meta.get("dateModified", date_pub),
                # Clean directory URL when the file is index.html, else the named file.
                "path": f"posts/{slug}/" if html_file.name == "index.html" else f"posts/{slug}/{html_file.name}",
            }
        )
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def _rfc822(d: str) -> str:
    try:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000")
    except ValueError:
        return datetime.utcnow().strftime("%a, %d %b %Y 00:00:00 +0000")


def _abs(base: str, path: str) -> str:
    return base.rstrip("/") + "/" + path.lstrip("/")


def render_index(site_title: str, posts: list[dict]) -> str:
    cards = []
    for p in posts:
        cards.append(
            f"""    <article class="card">
      <a href="{html.escape(p['path'])}"><h2>{html.escape(p['title'])}</h2></a>
      <p class="date">{html.escape(p['date'])}</p>
      <p class="desc">{html.escape(p['description'])}</p>
    </article>"""
        )
    cards_html = "\n".join(cards) if cards else '    <p class="empty">No posts published yet.</p>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(site_title)}</title>
  <link rel="alternate" type="application/rss+xml" title="{html.escape(site_title)}" href="rss.xml">
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ font-family: -apple-system, system-ui, sans-serif; max-width: 760px;
           margin: 0 auto; padding: 2.5rem 1.25rem; line-height: 1.6; }}
    h1 {{ font-size: 2rem; margin-bottom: 2rem; }}
    .card {{ padding: 1.25rem 0; border-bottom: 1px solid color-mix(in srgb, currentColor 15%, transparent); }}
    .card h2 {{ margin: 0 0 .25rem; font-size: 1.25rem; }}
    .card a {{ text-decoration: none; color: inherit; }}
    .card a:hover h2 {{ text-decoration: underline; }}
    .date {{ font-size: .85rem; opacity: .6; margin: 0 0 .35rem; }}
    .desc {{ margin: 0; opacity: .85; }}
    .empty {{ opacity: .6; }}
    footer {{ margin-top: 3rem; font-size: .8rem; opacity: .55; }}
  </style>
</head>
<body>
  <h1>{html.escape(site_title)}</h1>
{cards_html}
  <footer><a href="/about/">About</a> · <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a> · <a href="rss.xml">RSS</a><br>{html.escape(site_title)} · {date.today().isoformat()}</footer>
</body>
</html>
"""


def render_sitemap(base: str, posts: list[dict]) -> str:
    urls = [f"""  <url>
    <loc>{html.escape(base.rstrip('/') + '/')}</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""]
    for p in posts:
        urls.append(f"""  <url>
    <loc>{html.escape(_abs(base, p['path']))}</loc>
    <lastmod>{html.escape(p['modified'] or p['date'])}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")
    body = "\n".join(urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""


def render_rss(base: str, site_title: str, description: str, posts: list[dict]) -> str:
    items = []
    for p in posts:
        link = _abs(base, p["path"])
        items.append(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{html.escape(link)}</link>
      <guid isPermaLink="true">{html.escape(link)}</guid>
      <pubDate>{_rfc822(p['date'])}</pubDate>
      <description>{html.escape(p['description'])}</description>
    </item>""")
    items_xml = "\n".join(items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{html.escape(site_title)}</title>
    <link>{html.escape(base.rstrip('/') + '/')}</link>
    <atom:link href="{html.escape(_abs(base, 'rss.xml'))}" rel="self" type="application/rss+xml"/>
    <description>{html.escape(description)}</description>
    <language>en-us</language>
    <lastBuildDate>{_rfc822(date.today().isoformat())}</lastBuildDate>
{items_xml}
  </channel>
</rss>
"""


def render_robots(base: str) -> str:
    lines = ["# AI answer engines are welcome (GEO-first).", ""]
    for bot in AI_CRAWLERS:
        lines.append(f"User-agent: {bot}")
        lines.append("Allow: /")
        lines.append("")
    lines.append("User-agent: *")
    lines.append("Allow: /")
    lines.append("")
    lines.append(f"Sitemap: {_abs(base, 'sitemap.xml')}")
    return "\n".join(lines) + "\n"


def render_llms(base: str, site_title: str, description: str, posts: list[dict]) -> str:
    lines = [f"# {site_title}", "", f"> {description}", ""]
    lines.append("## Posts")
    for p in posts:
        link = _abs(base, p["path"])
        desc = p["description"].strip()
        lines.append(f"- [{p['title']}]({link}){': ' + desc if desc else ''}")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Build index + sitemap + rss + robots + llms.")
    ap.add_argument("--site-title", default="My Blog")
    ap.add_argument("--base-url", default="https://example.com")
    ap.add_argument("--description",
                    default="Agentic AI for founders and small teams: run a lean business with AI agents.")
    args = ap.parse_args()

    posts = collect_posts()
    base = args.base_url

    (PUBLISH / "index.html").write_text(render_index(args.site_title, posts), encoding="utf-8")
    (PUBLISH / "sitemap.xml").write_text(render_sitemap(base, posts), encoding="utf-8")
    (PUBLISH / "rss.xml").write_text(render_rss(base, args.site_title, args.description, posts), encoding="utf-8")
    (PUBLISH / "robots.txt").write_text(render_robots(base), encoding="utf-8")
    (PUBLISH / "llms.txt").write_text(render_llms(base, args.site_title, args.description, posts), encoding="utf-8")

    print(f"Wrote index.html, sitemap.xml, rss.xml, robots.txt, llms.txt for {len(posts)} post(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
