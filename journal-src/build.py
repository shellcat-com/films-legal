# -*- coding: utf-8 -*-
"""
build.py — render The Journal into films-legal/blog/.

Authoring tooling only: the *output* under blog/ is plain static HTML/CSS/SVG
(no runtime build step on the deployed site). Run from anywhere:

    python3 journal-src/build.py

Reads posts.py (metadata) + content/<slug>.html (body) + covers.py (art),
writes blog/index.html, blog/<slug>.html, and blog/art/<slug>.svg.
"""

import json
import os
import shutil
from datetime import datetime

import covers
from posts import POSTS, CATS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
ART = os.path.join(BLOG, "art")
CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")
BASE = "https://getfilmsera.cam"

# Real app photos for Journal covers (LookSourceImages + SamplePhotos + lifestyle).
PHOTO_POOL = [
    "shots/samples/party.jpg",
    "shots/samples/beach.jpg",
    "shots/samples/hug.jpg",
    "shots/samples/paris.jpg",
    "shots/samples/dinner.jpg",
    "shots/samples/sunset.jpg",
    "shots/samples/street.jpg",
    "shots/samples/lake.jpg",
    "shots/samples/sample01.jpg",
    "shots/samples/sample03.jpg",
    "shots/samples/sample05.jpg",
    "shots/samples/sample07.jpg",
    "shots/samples/sample09.jpg",
    "shots/samples/sample11.jpg",
    "shots/looks/look03.jpg",
    "shots/looks/look05.jpg",
    "shots/looks/look08.jpg",
    "shots/looks/look09.jpg",
    "shots/looks/look14.jpg",
    "shots/looks/look15.jpg",
    "shots/looks/look20.jpg",
    "shots/looks/look22.jpg",
]


def photo_for(slug: str) -> str:
    h = 0
    for ch in slug:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return PHOTO_POOL[h % len(PHOTO_POOL)]


def cover_src(p) -> str:
    """Prefer copied JPG cover under blog/art/; fall back to SVG."""
    jpg = f"art/{p['slug']}.jpg"
    if os.path.exists(os.path.join(BLOG, jpg)):
        return jpg
    return f"art/{p['slug']}.svg"

MARK = covers.MARK.replace('width="100" height="100"', 'class="daybreak" aria-hidden="true"')

APP_STORE = "https://apps.apple.com/us/app/filmsera-group-film-camera/id6781880091"
SMART_BANNER = '<meta name="apple-itunes-app" content="app-id=6781880091"/>'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"/>'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600'
         '&family=Hanken+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700'
         '&display=swap" rel="stylesheet"/>')


def updated_html(p):
    u = p.get("updated")
    if not u or u == p["date"]:
        return ""
    return f'<span class="dot">·</span><span>Updated <time datetime="{u}">{pretty(u)}</time></span>'


def pretty(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %-d, %Y")


def nav(prefix=""):
    return f'''<nav><div class="wrap">
    <a class="logo" href="/">{MARK}Filmsera</a>
    <div class="navlinks">
      <a href="/weddings/">Weddings</a>
      <a href="/parties/">Parties</a>
      <a href="/how-it-works/">How it works</a>
      <a href="/faq/">FAQ</a>
      <a href="{prefix}index.html" class="active">Journal</a>
      <a class="btn" href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store">Download</a>
    </div></div></nav>'''


def footer(prefix=""):
    return f'''<footer><div class="wrap">
    <div class="logo">{MARK}Filmsera</div>
    <div class="links">
      <a href="index.html">Journal</a>
      <a href="/weddings/">Weddings</a>
      <a href="/parties/">Parties</a>
      <a href="/holiday-parties/">Holiday parties</a>
      <a href="/vintage-film-camera/">Vintage camera</a>
      <a href="/how-it-works/">How it works</a>
      <a href="/faq/">FAQ</a>
      <a href="/vs/">Compare</a>
      <a href="{prefix}../looks/index.html">Look Lab</a>
      <a href="{prefix}../privacy.html">Privacy</a>
      <a href="{prefix}../terms.html">Terms</a>
      <a href="{prefix}../support.html">Support</a>
      <a href="/llms.txt">llms.txt</a>
    </div>
    <div>© 2026 Filmsera</div>
  </div></footer>'''


def cta_band():
    return f'''<section><div class="wrap"><div class="band reveal">
      <span class="pill">On the App Store</span>
      <h2>Download Filmsera</h2>
      <p>25 Looks. Shared Films. Timed Reveal. Host the night — then open every Frame together.</p>
      <a class="btn" href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store">Download on the App Store</a>
    </div></div></section>'''


def card(p):
    return f'''<a class="card reveal" data-cat="{p['cat']}" href="{p['slug']}.html">
      <div class="art"><img loading="lazy" src="{cover_src(p)}" alt="{p['title']}"/></div>
      <div class="body">
        <div class="meta"><span class="cat">{p['cat']}</span><span>·</span><span>{p['read']} min read</span></div>
        <h3>{p['title']}</h3>
        <p>{p['excerpt']}</p>
        <span class="more">Read the story →</span>
      </div></a>'''


def related_for(post):
    same = [q for q in POSTS if q["cat"] == post["cat"] and q["slug"] != post["slug"]]
    others = [q for q in POSTS if q["cat"] != post["cat"] and q["slug"] != post["slug"]]
    picks = (same + others)[:3]
    cards = "".join(card(p) for p in picks)
    return f'''<section class="related"><div class="wrap">
      <div class="lbl">Keep reading</div>
      <div class="grid">{cards}</div></div></section>'''


def page_title(title):
    """Keep <title> under ~60 chars: short suffix, dropped for long headlines."""
    return title if len(title) > 50 else f"{title} · Filmsera"


def article_ld(p):
    url = f"{BASE}/blog/{p['slug']}.html"
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "description": p["excerpt"],
        "datePublished": p["date"],
        "dateModified": p.get("updated", p["date"]),
        "author": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "Filmsera", "url": f"{BASE}/"},
        "publisher": {"@id": f"{BASE}/#org"},
        "image": f"{BASE}/blog/art/{p['slug']}.jpg",
        "mainEntityOfPage": url,
        "url": url,
        "inLanguage": "en",
    }


def head(title, desc, slug, ld=None):
    ld_tag = ""
    if ld:
        ld_tag = ('<script type="application/ld+json">'
                  + json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
                  + "</script>\n")
    return f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>{page_title(title)}</title>
<meta name="description" content="{desc}"/>
<meta name="theme-color" content="#0A0807"/>
{SMART_BANNER}
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="Filmsera"/>
<meta property="og:image" content="{BASE}/blog/art/{slug}.jpg"/>
<meta property="og:url" content="{BASE}/blog/{slug}.html"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{desc}"/>
<link rel="canonical" href="{BASE}/blog/{slug}.html"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
{FONTS}
<link rel="stylesheet" href="journal.css"/>
{ld_tag}</head><body>'''


def build_cover(p):
    a, b = CATS[p["cat"]]
    svg = covers.cover_svg(p["slug"], p["motif"], a, b)
    with open(os.path.join(ART, f"{p['slug']}.svg"), "w") as f:
        f.write(svg)
    # Real photograph cover (same pool users see in-app)
    src = os.path.join(ROOT, photo_for(p["slug"]))
    dst = os.path.join(ART, f"{p['slug']}.jpg")
    if os.path.exists(src):
        shutil.copyfile(src, dst)


# Hosting posts link up to the landing page that owns the commercial query.
LANDING = {
    "best-disposable-camera-apps-for-weddings-2026": ("/weddings/", "Filmsera for weddings"),
    "how-to-run-filmsera-at-your-wedding": ("/weddings/", "Filmsera for weddings"),
    "shared-camera-roll-at-a-wedding": ("/weddings/", "Filmsera for weddings"),
    "collecting-guest-photos-without-chaos": ("/how-it-works/", "how Filmsera works"),
    "choosing-the-right-reveal-time": ("/how-it-works/", "how Filmsera works"),
    "disposable-camera-party-playbook": ("/parties/", "Filmsera for parties and birthdays"),
    "one-trip-one-film": ("/parties/", "Filmsera for parties, trips and weekends"),
    "how-to-write-a-film-invitation": ("/holiday-parties/", "Filmsera for holiday parties"),
    "disposable-vs-vhs-vs-super8-which-look": ("/vintage-film-camera/", "all 25 film looks"),
    "what-makes-a-photo-feel-like-film": ("/vintage-film-camera/", "all 25 film looks"),
    "grain-halation-light-leaks-explained": ("/vintage-film-camera/", "all 25 film looks"),
}


def landing_note(p):
    if p["slug"] not in LANDING:
        return ""
    href, label = LANDING[p["slug"]]
    return (f'<p class="landing-link">Planning your own? See <a href="{href}">{label}</a>, '
            'or read the <a href="/faq/">FAQ</a>.</p>')


def build_article(p):
    frag = os.path.join(CONTENT, f"{p['slug']}.html")
    if os.path.exists(frag):
        with open(frag) as f:
            body = f.read()
    else:
        body = "<p>Coming soon.</p>"
    divider = f'<div class="divider">{covers.divider_svg(CATS[p["cat"]][0])}</div>'
    body = body.replace("{{divider}}", divider) + landing_note(p)

    html = head(p["title"], p["excerpt"], p["slug"], article_ld(p))
    html += nav()
    html += f'''<div class="wrap" style="padding-top:18px"><a class="btn" href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store" style="display:inline-flex">Download Filmsera</a></div>
<article>
  <div class="wrap"><header class="article-hero">
    <span class="pill">{p['cat']}</span>
    <h1>{p['title']}</h1>
    <p class="dek">{p['dek']}</p>
    <div class="byline"><span>Filmsera</span><span class="dot">·</span>
      <time datetime="{p['date']}">{pretty(p['date'])}</time>{updated_html(p)}
      <span class="dot">·</span><span>{p['read']} min read</span></div>
  </header></div>
  <div class="wrap"><figure class="cover">
    <img src="{cover_src(p)}" alt="{p['title']}"/>
  </figure></div>
  <div class="wrap"><div class="prose">{body}</div></div>
  <div class="wrap"><div class="end-note">
    <div class="mark">{MARK}</div>
    <div><h4>Written by the Filmsera team</h4>
    <p>Filmsera is a shared disposable camera app for iPhone: create a film for your event, let every guest shoot through 25 film looks, and open the whole roll together at the reveal. <a href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store" style="color:var(--brass)">Download on the App Store →</a></p></div>
  </div></div>
</article>'''
    html += related_for(p)
    html += cta_band()
    html += footer()
    html += '<script src="journal.js"></script></body></html>'

    with open(os.path.join(BLOG, f"{p['slug']}.html"), "w") as f:
        f.write(html)


def build_index():
    feat = POSTS[0]
    rest = POSTS[1:]
    cats = list(CATS.keys())
    filters = '<button class="filter on" data-filter="all">All</button>' + "".join(
        f'<button class="filter" data-filter="{c}">{c}</button>' for c in cats)
    grid = "".join(card(p) for p in rest)

    html = f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>The Journal — Filmsera</title>
<meta name="description" content="Notes on film, memory, and shooting together — from the team behind Filmsera, the group film camera."/>
<meta name="theme-color" content="#0A0807"/>
{SMART_BANNER}
<meta property="og:title" content="The Journal — Filmsera"/>
<meta property="og:description" content="Notes on film, memory, and shooting together."/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Filmsera"/>
<meta property="og:image" content="{BASE}/blog/{cover_src(feat)}"/>
<meta property="og:url" content="{BASE}/blog/"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="canonical" href="{BASE}/blog/"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
{FONTS}
<link rel="stylesheet" href="journal.css"/>
</head><body>'''
    html += nav()
    html += '''<header class="j-head"><div class="wrap">
    <span class="pill">The Journal</span>
    <h1>Notes on film, memory, and shooting together.</h1>
    <p>Stories on the Looks, the wait, and the craft of capturing a night the way it actually felt — from the team behind Filmsera.</p>
    <div class="j-mosaic" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:28px auto 0;max-width:720px">
      <img src="../shots/samples/party.jpg" alt="" style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px" loading="lazy"/>
      <img src="../shots/samples/beach.jpg" alt="" style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px" loading="lazy"/>
      <img src="../shots/samples/hug.jpg" alt="" style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px" loading="lazy"/>
      <img src="../shots/samples/paris.jpg" alt="" style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px" loading="lazy"/>
    </div>
    <p style="margin-top:20px"><a class="btn" href="''' + APP_STORE + '''" target="_blank" rel="noopener" data-cta="app_store">Download Filmsera</a></p>
  </div></header>'''
    html += f'''<div class="wrap"><article class="featured reveal">
    <div class="art"><a href="{feat['slug']}.html"><img loading="lazy" src="{cover_src(feat)}" alt="{feat['title']}"/></a></div>
    <div class="copy">
      <div class="meta"><span class="pill">Featured</span><span>{feat['cat']}</span><span>·</span><span>{feat['read']} min read</span></div>
      <h2><a href="{feat['slug']}.html">{feat['title']}</a></h2>
      <p class="ex">{feat['excerpt']}</p>
      <a class="read" href="{feat['slug']}.html">Read the story →</a>
    </div></article></div>'''
    html += f'''<div class="wrap">
    <div class="filters">{filters}</div>
    <div class="grid">{grid}</div>
  </div>'''
    html += cta_band()
    html += footer()
    html += '<script src="journal.js"></script></body></html>'

    with open(os.path.join(BLOG, "index.html"), "w") as f:
        f.write(html)


def main():
    os.makedirs(ART, exist_ok=True)
    for p in POSTS:
        build_cover(p)
        build_article(p)
    build_index()
    have = sum(1 for p in POSTS if os.path.exists(os.path.join(CONTENT, f"{p['slug']}.html")))
    print(f"Built {len(POSTS)} covers + {len(POSTS)} articles + index. "
          f"Content fragments present: {have}/{len(POSTS)}.")


if __name__ == "__main__":
    main()
