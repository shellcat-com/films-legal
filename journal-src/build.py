# -*- coding: utf-8 -*-
"""
build.py — render The Journal into films-legal/blog/.

Authoring tooling only: the *output* under blog/ is plain static HTML/CSS/SVG
(no runtime build step on the deployed site). Run from anywhere:

    python3 journal-src/build.py

Reads posts.py (metadata) + content/<slug>.html (body) + covers.py (art),
writes blog/index.html, blog/<slug>.html, and blog/art/<slug>.svg.
"""

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

SPARK = ('<svg class="spark" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
         '<path d="M50 2 C53 30 70 47 98 50 C70 53 53 70 50 98 C47 70 30 53 2 50 '
         'C30 47 47 30 50 2 Z" fill="#E6B450"/></svg>')

APP_STORE = "https://apps.apple.com/us/app/filmsera-group-film-camera/id6781880091"
SMART_BANNER = '<meta name="apple-itunes-app" content="app-id=6781880091"/>'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"/>'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600'
         '&family=Hanken+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700'
         '&display=swap" rel="stylesheet"/>')


def pretty(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %-d, %Y")


def nav(prefix=""):
    return f'''<nav><div class="wrap">
    <a class="logo" href="{prefix}../index.html">{SPARK}Filmsera</a>
    <div class="navlinks">
      <a href="{prefix}../index.html#looks">Looks</a>
      <a href="{prefix}../index.html#reveal">Reveal</a>
      <a href="{prefix}../index.html#recap">Recap</a>
      <a href="{prefix}../index.html#faq">FAQ</a>
      <a href="{prefix}index.html" class="active">Journal</a>
      <a class="btn" href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store">Download</a>
    </div></div></nav>'''


def footer(prefix=""):
    return f'''<footer><div class="wrap">
    <div class="logo">{SPARK}Filmsera</div>
    <div class="links">
      <a href="index.html">Journal</a>
      <a href="{prefix}../looks/index.html">Look Lab</a>
      <a href="{prefix}../privacy.html">Privacy</a>
      <a href="{prefix}../terms.html">Terms</a>
      <a href="{prefix}../support.html">Support</a>
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


def head(title, desc, slug):
    return f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>{title} — The Journal · Filmsera</title>
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
<link rel="canonical" href="{BASE}/blog/{slug}.html"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
{FONTS}
<link rel="stylesheet" href="journal.css"/>
</head><body>'''


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


def build_article(p):
    frag = os.path.join(CONTENT, f"{p['slug']}.html")
    if os.path.exists(frag):
        with open(frag) as f:
            body = f.read()
    else:
        body = "<p>Coming soon.</p>"
    divider = f'<div class="divider">{covers.divider_svg(CATS[p["cat"]][0])}</div>'
    body = body.replace("{{divider}}", divider)

    html = head(p["title"], p["excerpt"], p["slug"])
    html += nav()
    html += f'''<div class="wrap" style="padding-top:18px"><a class="btn" href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store" style="display:inline-flex">Download Filmsera</a></div>
<article>
  <div class="wrap"><header class="article-hero">
    <span class="pill">{p['cat']}</span>
    <h1>{p['title']}</h1>
    <p class="dek">{p['dek']}</p>
    <div class="byline"><span>Filmsera</span><span class="dot">·</span>
      <time datetime="{p['date']}">{pretty(p['date'])}</time>
      <span class="dot">·</span><span>{p['read']} min read</span></div>
  </header></div>
  <div class="wrap"><figure class="cover">
    <img src="{cover_src(p)}" alt="{p['title']}"/>
  </figure></div>
  <div class="wrap"><div class="prose">{body}</div></div>
  <div class="wrap"><div class="end-note">
    <div class="mark">{SPARK}</div>
    <div><h4>Written by the Filmsera team</h4>
    <p>Filmsera is a group film camera — Host a Film, shoot Shots through 25 Looks, and open every Frame together at Reveal. <a href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store" style="color:var(--brass)">Download on the App Store →</a></p></div>
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
