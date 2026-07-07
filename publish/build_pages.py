#!/usr/bin/env python3
"""Generate the site's entity/trust pages: /about, /contact, /privacy.

Phase C.5 (WS0-C). A real, accountable publisher identity is the single biggest
anti-deindex + E-E-A-T signal for a new domain. This emits:
  - publish/about/index.html    author + org + editorial standard + AI disclosure
                                + Organization and Person JSON-LD (with sameAs)
  - publish/contact/index.html  how to reach a real human
  - publish/privacy/index.html  a plain-language privacy statement

All values come from the `identity` + `site` blocks in autopilot/config.yaml, so
there is one source of truth and nothing is fabricated here. Run after
build_index.py (run.py publish() calls both).

Usage:
  equipment/.venv/bin/python publish/build_pages.py
"""
from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PUBLISH = ROOT / "publish"
CONFIG = ROOT / "autopilot" / "config.yaml"

CSS = """*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.65;
background:#0b1220;color:#e6edf6}
main{max-width:720px;margin:0 auto;padding:3rem 1.25rem 4rem}
a{color:#7cc0ff}a:hover{color:#a6d4ff}
h1{font-size:1.9rem;line-height:1.2;margin:0 0 1rem}h2{font-size:1.25rem;margin:2rem 0 .5rem}
nav{max-width:720px;margin:0 auto;padding:1.25rem 1.25rem 0;font-size:.95rem}
nav a{margin-right:1.25rem}
.muted{color:#9fb0c6}.card{background:#111a2e;border:1px solid #1f2b45;border-radius:12px;padding:1.25rem 1.5rem;margin:1.5rem 0}
footer{max-width:720px;margin:0 auto;padding:2rem 1.25rem;color:#9fb0c6;border-top:1px solid #1f2b45;font-size:.9rem}
@media(prefers-color-scheme:light){body{background:#fff;color:#12203a}a{color:#0b62c4}
.card{background:#f6f9ff;border-color:#dbe6f7}nav,footer{border-color:#dbe6f7}.muted,footer{color:#5a6b85}}"""


def cfg() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def e(s: str) -> str:
    return html.escape((s or "").strip())


def _clean(s: str) -> str:
    return " ".join((s or "").split())


def page(title: str, base: str, site: str, body: str, jsonld: str = "") -> str:
    desc = e(f"{title} — {site}")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} — {e(site)}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{e(base)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:title" content="{e(title)} — {e(site)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{e(base)}">
<style>{CSS}</style>
{jsonld}
</head>
<body>
<nav><a href="/">{e(site)}</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a></nav>
<main>
{body}
</main>
<footer>&copy; {date.today().year} {e(site)}. {e(_clean(''))}</footer>
</body>
</html>
"""


def build_about(c: dict, base_url: str, site: str) -> str:
    idn = c.get("identity", {})
    a = idn.get("author", {})
    org = idn.get("organization", {})
    bio = _clean(a.get("bio", ""))
    disclosure = _clean(idn.get("ai_disclosure", ""))
    standard = _clean(idn.get("editorial_standard", ""))
    a_same = [s for s in (a.get("same_as") or []) if s]
    o_same = [s for s in (org.get("same_as") or []) if s]

    graph = [
        {
            "@type": "Organization",
            "@id": base_url.rstrip("/") + "/#org",
            "name": org.get("name", site),
            "url": org.get("url") or base_url,
            **({"logo": org["logo"]} if org.get("logo") else {}),
            **({"sameAs": o_same} if o_same else {}),
        },
        {
            "@type": "Person",
            "@id": base_url.rstrip("/") + "/#" + e(a.get("name", "author")).lower().replace(" ", "-"),
            "name": a.get("name", ""),
            "jobTitle": a.get("title", ""),
            "description": bio,
            "url": a.get("url") or (base_url.rstrip("/") + "/about/"),
            "worksFor": {"@id": base_url.rstrip("/") + "/#org"},
            **({"sameAs": a_same} if a_same else {}),
        },
    ]
    jsonld = ('<script type="application/ld+json">'
              + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
              + "</script>")

    same_html = ""
    if a_same:
        links = " ".join(f'<a href="{e(u)}" rel="me">{e(u.split("//")[-1].split("/")[0])}</a>' for u in a_same)
        same_html = f'<p class="muted">Find {e(a.get("name",""))} on: {links}</p>'

    body = f"""<h1>About {e(site)}</h1>
<p>{e(bio)}</p>
{same_html}
<div class="card">
<h2>Our editorial standard</h2>
<p>{e(standard)}</p>
</div>
<div class="card">
<h2>How we use AI</h2>
<p>{e(disclosure)}</p>
</div>
<p class="muted">Questions or a correction? <a href="/contact/">Contact us</a>.</p>"""
    return page(f"About {site}", base_url.rstrip("/") + "/about/", site, body, jsonld)


def build_contact(c: dict, base_url: str, site: str) -> str:
    idn = c.get("identity", {})
    a = idn.get("author", {})
    email = _clean(idn.get("contact_email", ""))
    email_html = (f'<p>Email us at <a href="mailto:{e(email)}">{e(email)}</a>.</p>'
                  if email else
                  '<p class="muted">A public contact address is being set up. In the meantime, '
                  'corrections and questions are welcome and reviewed by a person.</p>')
    body = f"""<h1>Contact {e(site)}</h1>
<p>{e(site)} is published by {e(a.get('name',''))}. We read every message and correct errors quickly.</p>
{email_html}
<p class="muted">We fact-check every statistic against a named primary source. If you spot one that
looks wrong, tell us and we will fix or retract it.</p>"""
    return page(f"Contact {site}", base_url.rstrip("/") + "/contact/", site, body)


def build_privacy(c: dict, base_url: str, site: str) -> str:
    idn = c.get("identity", {})
    email = _clean(idn.get("contact_email", ""))
    contact_line = (f'email <a href="mailto:{e(email)}">{e(email)}</a>' if email
                    else 'reach us via the <a href="/contact/">contact page</a>')
    body = f"""<h1>Privacy Policy</h1>
<p class="muted">Last updated {date.today().isoformat()}.</p>
<p>{e(site)} is a content website. We aim to collect as little data as possible.</p>
<h2>What we collect</h2>
<p>Standard server logs (IP address, browser type, pages viewed) and, if enabled, privacy-respecting
analytics used only in aggregate to understand which content is useful. We do not sell personal data.</p>
<h2>Cookies</h2>
<p>We use only the cookies required for the site to function and, if present, aggregate analytics.
You can block cookies in your browser without losing access to the content.</p>
<h2>Third parties</h2>
<p>Pages may link to third-party sources we cite. Their privacy practices are their own; review their
policies when you visit them.</p>
<h2>Your rights and contact</h2>
<p>You can request access to, or deletion of, any personal data we hold. To do so, {contact_line}.</p>"""
    return page("Privacy Policy", base_url.rstrip("/") + "/privacy/", site, body)


def main() -> int:
    c = cfg()
    site = c["site"]["title"]
    base_url = c["site"]["base_url"]
    pages = {
        "about": build_about(c, base_url, site),
        "contact": build_contact(c, base_url, site),
        "privacy": build_privacy(c, base_url, site),
    }
    for name, htmltext in pages.items():
        d = PUBLISH / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(htmltext, encoding="utf-8")
    print(f"Wrote {', '.join('/' + n + '/' for n in pages)} for {site}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
