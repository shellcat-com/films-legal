# -*- coding: utf-8 -*-
"""
build-pages.py: render the static marketing pages that share one template.

    python3 scripts/build-pages.py

Writes (plain static HTML, no runtime build on the deployed site):
  weddings/ parties/ holiday-parties/ vintage-film-camera/
  how-it-works/ faq/                         -> <dir>/index.html
  vs/index.html vs/pov.html vs/once.html vs/lense.html
  open/{create,films,camera,templates,booth}/index.html  (noindex fallbacks
  for the app's /open/<screen> universal links)

Page copy lives in scripts/pages_content.py. Pricing copy is centralised in
PRICING there (owner-confirmed current pricing, 2026-11-11).
Do NOT hand-edit the generated HTML; edit the content file and rerun.
"""

import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "journal-src"))

import covers  # noqa: E402  (brand mark SVG, shared with the Journal)
import pages_content as C  # noqa: E402

BASE = "https://getfilmsera.cam"
APP_ID = "6781880091"
MARK = covers.MARK.replace('width="100" height="100"', 'class="daybreak" aria-hidden="true"')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500'
         '&family=Hanken+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700'
         '&display=swap" rel="stylesheet" />')


def esc(s):
    return html.escape(s, quote=True)


def text_of(fragment):
    """Visible text of an HTML fragment (for JSON-LD answers that must match the page)."""
    t = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(re.sub(r"\s+", " ", t)).strip()


def org_ref():
    return {"@id": f"{BASE}/#org"}


def breadcrumb(path, trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"}]
    for i, (name, url) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": BASE + url})
    return {"@type": "BreadcrumbList", "@id": f"{BASE}{path}#breadcrumb", "itemListElement": items}


def faq_schema(path, faqs):
    return {
        "@type": "FAQPage", "@id": f"{BASE}{path}#faq",
        "mainEntity": [{"@type": "Question", "name": text_of(q),
                        "acceptedAnswer": {"@type": "Answer", "text": text_of(a)}} for q, a in faqs],
    }


def faq_html(faqs, open_first=False):
    out = ['<div class="faq">']
    for i, (q, a) in enumerate(faqs):
        o = " open" if (open_first and i == 0) else ""
        out.append(f"<details{o}><summary>{q}</summary><p>{a}</p></details>")
    out.append("</div>")
    return "\n".join(out)


def head(p):
    path = p["path"]
    url = BASE + path
    robots = '<meta name="robots" content="noindex" />\n' if p.get("noindex") else ""
    canonical = "" if p.get("noindex") else f'<link rel="canonical" href="{url}" />\n'
    banner = f'app-id={APP_ID}'
    if p.get("app_argument"):
        banner += f', app-argument={BASE}{p["app_argument"]}'
    ld = ""
    if p.get("jsonld"):
        ld = ('<script type="application/ld+json">'
              + json.dumps({"@context": "https://schema.org", "@graph": p["jsonld"]},
                           ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
              + "</script>\n")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}" />
{robots}{canonical}<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta name="apple-itunes-app" content="{banner}" />
<meta name="theme-color" content="#0A0807" />
<meta property="og:title" content="{esc(p["title"])}" />
<meta property="og:description" content="{esc(p["desc"])}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{url}" />
<meta property="og:site_name" content="Filmsera" />
<meta property="og:image" content="{BASE}/shots/filmsera-social.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(p["title"])}" />
<meta name="twitter:description" content="{esc(p["desc"])}" />
{FONTS}
<link rel="stylesheet" href="/vs/vs.css" />
<link rel="stylesheet" href="/assets/pages.css" />
{ld}</head>
<body>
'''


def nav(active=""):
    def a(href, label):
        cls = ' class="active"' if href == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''<nav>
  <div class="wrap">
    <a class="logo" href="/">{MARK}Filmsera</a>
    <div class="navlinks">
      {a("/weddings/", "Weddings")}
      {a("/parties/", "Parties")}
      {a("/how-it-works/", "How it works")}
      {a("/faq/", "FAQ")}
      {a("/vs/", "Compare")}
      {a("/blog/", "Journal")}
      <a class="nav-badge" href="{C.APP_STORE}" target="_blank" rel="noopener" data-cta="app_store" aria-label="Download Filmsera on the App Store">
        <img src="/shots/app-store-badge.svg" alt="Download on the App Store" width="120" height="40" />
      </a>
    </div>
  </div>
</nav>
'''


def badge(url=None):
    return (f'<a class="as-badge" href="{url or C.APP_STORE}" target="_blank" rel="noopener" data-cta="app_store">'
            '<img src="/shots/app-store-badge.svg" alt="Download on the App Store" width="148" height="44" /></a>')


def band(title, line, url=None):
    return f'''<section class="wrap">
  <div class="band">
    <span class="pill">On the App Store</span>
    <h2 style="margin-top:14px">{title}</h2>
    <p>{line}</p>
    <div class="band-cta">
      {badge(url)}
      <div class="band-qr">
        <img src="/shots/appstore-qr.png" alt="QR code to download Filmsera" width="80" height="80" />
        <div><strong>Scan to download</strong><span>App Store · iPhone</span></div>
      </div>
    </div>
  </div>
</section>
'''


def footer():
    links = [("/weddings/", "Weddings"), ("/parties/", "Parties"), ("/holiday-parties/", "Holiday parties"),
             ("/vintage-film-camera/", "Vintage film camera"), ("/how-it-works/", "How it works"),
             ("/faq/", "FAQ"), ("/vs/", "Compare"), ("/looks/", "Look Lab"), ("/blog/", "Journal"),
             ("/privacy.html", "Privacy"), ("/terms.html", "Terms"), ("/support.html", "Support"),
             ("/llms.txt", "llms.txt")]
    ls = "\n      ".join(f'<a href="{h}">{t}</a>' for h, t in links)
    return f'''<footer>
  <div class="wrap">
    <div class="logo">{MARK}Filmsera</div>
    <div class="links">
      {ls}
    </div>
    <div>© 2026 Filmsera</div>
  </div>
</footer>
</body>
</html>
'''


def webpage_ld(p, page_type="WebPage"):
    path = p["path"]
    d = {"@type": page_type, "@id": f"{BASE}{path}#webpage", "url": BASE + path, "name": p["title"],
         "description": p["desc"], "inLanguage": "en", "dateModified": C.UPDATED,
         "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": f"{BASE}/#app"},
         "publisher": org_ref(), "breadcrumb": {"@id": f"{BASE}{path}#breadcrumb"}}
    return d


def render(p):
    out = head(p) + nav(p.get("nav_active", "")) + p["body"]
    if p.get("band"):
        out += band(*p["band"])
    out += footer()
    return out


def write(rel, content):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    return rel


def build_content_page(p):
    """Landing / FAQ / how-it-works / vs pages: wrap body sections with hero + FAQ + JSON-LD."""
    faqs = p.get("faqs", [])
    graph = [webpage_ld(p, p.get("page_type", "WebPage")), breadcrumb(p["path"], p["crumbs"])]
    if faqs:
        graph.append(faq_schema(p["path"], faqs))
    graph.extend(p.get("extra_ld", []))
    p["jsonld"] = graph
    crumbs = " › ".join([f'<a href="/">Home</a>'] + [
        (f'<a href="{u}">{n}</a>' if i < len(p["crumbs"]) - 1 else n)
        for i, (n, u) in enumerate(p["crumbs"])])
    hero = f'''<article class="wrap page">
  <div class="crumbs">{crumbs}</div>
  <span class="pill" style="margin-top:14px">{p["pill"]}</span>
  <h1>{p["h1"]}</h1>
  <p class="dek">{p["dek"]}</p>
  <p class="updated">Updated {C.UPDATED_PRETTY}</p>
  {('<div class="answer">' + p["answer"] + '</div>') if p.get("answer") else ""}
  <div class="hero-cta">{badge(p.get("cta"))}</div>
'''
    faq_block = ""
    if faqs:
        faq_block = f'\n  <h2 id="faq">{p.get("faq_title", "Questions")}</h2>\n{faq_html(faqs)}\n'
    p["body"] = hero + p["sections"] + faq_block + "\n</article>\n"
    return write(p["file"], render(p))


def build_open(screen, info):
    path = f"/open/{screen}/"
    p = {"path": path, "title": f"Open {info['label']} in Filmsera", "noindex": True,
         "desc": "This link opens Filmsera on iPhone. If you don't have the app yet, get it on the App Store.",
         "app_argument": f"/open/{screen}"}
    p["body"] = f'''<main class="open-card">
  <span class="pill">Filmsera link</span>
  <h1>This link opens {info['label']} in Filmsera</h1>
  <p>{info['line']}</p>
  <p>On an iPhone with Filmsera installed, this link opens the app directly. If you're seeing this page, the app isn't installed yet, or you opened the link on another device.</p>
  <div class="hero-cta">{badge()}<a class="btn" href="{C.APP_STORE}" target="_blank" rel="noopener" data-cta="app_store">Open in the App Store</a></div>
  <p class="fine" style="margin-top:22px">Filmsera is an iPhone app (iOS 17 or later). Already installed? Open Filmsera, then tap this link again. <a class="inl" href="/how-it-works/" style="color:var(--brass)">How Filmsera works</a></p>
</main>
'''
    return write(f"open/{screen}/index.html", render(p))


def main():
    written = []
    for p in C.pages():
        written.append(build_content_page(p))
    for screen, info in C.OPEN_SCREENS.items():
        written.append(build_open(screen, info))
    print(f"Wrote {len(written)} pages:")
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
