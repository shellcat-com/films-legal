# -*- coding: utf-8 -*-
"""
build.py — render The Journal into films-legal/blog/.

Authoring tooling only: the *output* under blog/ is plain static HTML/CSS/SVG
(no runtime build step on the deployed site). Run from anywhere:

    python3 journal-src/build.py

Two kinds of posts:
- Hand-listed posts in posts.py (the original Journal). Their JPG cover is copied
  from the licensed photo pool on every build.
- "Guide" posts: one journal-src/meta/<slug>.json per article (SEO batch, Nov 2026).
  They own a generated hero at blog/art/<slug>.jpg (never overwritten), carry a
  separate meta description, an FAQ (FAQPage JSON-LD) and get a table of contents.

Writes blog/index.html, blog/<slug>.html and blog/art/<slug>.svg.
"""

import glob
import html as htmlmod
import json
import os
import re
import shutil
from datetime import datetime

import covers
from posts import POSTS as LISTED_POSTS, CATS

try:
    from PIL import Image
except ImportError:  # dimensions are a nicety; the build still works without PIL
    Image = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BLOG = os.path.join(ROOT, "blog")
ART = os.path.join(BLOG, "art")
CONTENT = os.path.join(HERE, "content")
META = os.path.join(HERE, "meta")
BASE = "https://getfilmsera.cam"

# Categories added for the guide posts (filter pills render in this order).
CATS.update({
    "Weddings":      ("#E6B450", "#D9663C"),
    "Slideshows":    ("#EBC169", "#B98A4A"),
    "Parties":       ("#E6B450", "#C98A3A"),
    "Photo Sharing": ("#D9C39A", "#A9824E"),
})
CAT_ORDER = ["Weddings", "Slideshows", "Parties", "Photo Sharing", "Hosting",
             "The Craft", "The Reveal", "Culture", "Field Guide"]
CAT_MOTIF = {"Weddings": "rings", "Slideshows": "reel", "Parties": "sparkburst",
             "Photo Sharing": "contactsheet", "The Craft": "swatches"}

# Older posts that belong in the new topic categories.
RECAT = {
    "best-disposable-camera-apps-for-weddings-2026": "Weddings",
    "how-to-run-filmsera-at-your-wedding": "Weddings",
    "shared-camera-roll-at-a-wedding": "Weddings",
    "from-roll-to-recap": "Slideshows",
    "disposable-camera-party-playbook": "Parties",
}

# Guide posts shown first on the index, in this order ([0] is the featured post).
GUIDE_ORDER = [
    "how-to-collect-photos-from-wedding-guests",
    "friendsgiving-ideas",
    "how-to-make-a-wedding-slideshow",
    "qr-code-for-wedding-photos",
    "christmas-party-photo-booth-ideas",
    "wedding-slideshow-songs",
    "new-years-eve-party-ideas-at-home",
    "best-way-to-share-photos-with-a-group",
    "disposable-cameras-at-weddings-worth-it",
    "photo-dump-captions",
    "holiday-party-games-for-adults",
    "wedding-photo-scavenger-hunt",
    "how-to-make-an-event-recap-video",
    "wedding-qr-code-sign-wording",
    "bachelorette-party-photo-ideas",
    "how-to-make-photos-look-like-film-on-iphone",
    "free-wedding-photo-sharing",
    "how-long-should-a-wedding-slideshow-be",
    "wedding-guest-book-alternatives",
    "birthday-slideshow-ideas",
    "how-to-ask-wedding-guests-to-share-photos",
    "wedding-photo-booth-ideas",
    "icloud-shared-album-for-events",
    "wedding-slideshow-ideas",
    "how-many-disposable-cameras-for-a-wedding",
    "birthday-party-photo-ideas",
    "google-photos-shared-album-for-a-wedding",
    "wedding-hashtag-ideas",
    "disposable-camera-filter-iphone",
    "wedding-reception-games",
    "family-reunion-photo-ideas",
    "post-wedding-brunch-ideas",
    "what-is-a-digital-disposable-camera",
    "bridal-shower-photo-ideas",
    "how-to-take-good-photos-at-a-party",
    "digicam-aesthetic",
]
GUIDE_DATE = "2026-11-16"


def words_in(fragment):
    return len(re.sub(r"<[^>]+>", " ", fragment).split())


def load_guides():
    """Guide posts from meta/<slug>.json + content/<slug>.html (skips incomplete pairs)."""
    out = []
    for path in sorted(glob.glob(os.path.join(META, "*.json"))):
        with open(path, encoding="utf-8") as f:
            m = json.load(f)
        slug = m["slug"]
        frag = os.path.join(CONTENT, f"{slug}.html")
        if not os.path.exists(frag):
            continue
        with open(frag, encoding="utf-8") as f:
            n = words_in(f.read())
        cat = m["cat"] if m["cat"] in CATS else "Field Guide"
        out.append(dict(
            slug=slug, title=m["title"], seo_title=m.get("seo_title") or None,
            desc=m["description"], cat=cat, date=m.get("date", GUIDE_DATE),
            updated=m.get("updated"), read=max(3, round(n / 230)),
            motif=CAT_MOTIF.get(cat, "filmstrip"), dek=m["dek"], excerpt=m["excerpt"],
            faq=m.get("faq", []), keywords=[m.get("primary_keyword", "")] + m.get("secondary_keywords", []),
            guide=True, words=n,
        ))
    rank = {s: i for i, s in enumerate(GUIDE_ORDER)}
    out.sort(key=lambda p: (rank.get(p["slug"], 999), p["slug"]))
    return out


def all_posts():
    listed = []
    for p in LISTED_POSTS:
        q = dict(p)
        q["cat"] = RECAT.get(q["slug"], q["cat"])
        listed.append(q)
    return load_guides() + listed


POSTS = all_posts()

# Real app photos for Journal covers (LookSourceImages + SamplePhotos + lifestyle).
PHOTO_POOL = [
    # Licensed only: our original marketing photos (shots/originals/PROVENANCE.md)
    # and the Unsplash-licensed samples (shots/samples/ATTRIBUTION.txt).
    # Never add app-bundle Looks photos (look01-40) or copies of them.
    "shots/originals/01-wedding-dancefloor.jpg",
    "shots/originals/02-wedding-dinner-lights.jpg",
    "shots/originals/03-wedding-toast.jpg",
    "shots/originals/04-wedding-sparkler-exit.jpg",
    "shots/originals/05-birthday-cake.jpg",
    "shots/originals/06-house-party-couch.jpg",
    "shots/originals/07-bachelorette.jpg",
    "shots/originals/08-nye-confetti.jpg",
    "shots/originals/09-friendsgiving.jpg",
    "shots/originals/10-holiday-party.jpg",
    "shots/originals/11-roadtrip.jpg",
    "shots/originals/12-beach-trip.jpg",
    "shots/originals/13-concert-festival.jpg",
    "shots/originals/14-city-night.jpg",
    "shots/originals/15-family-reunion.jpg",
    "shots/originals/16-photobooth-moment.jpg",
    "shots/samples/sample01.jpg",
    "shots/samples/sample03.jpg",
    "shots/samples/sample05.jpg",
    "shots/samples/sample07.jpg",
    "shots/samples/sample09.jpg",
    "shots/samples/sample11.jpg",
]


def photo_for(slug: str) -> str:
    h = 0
    for ch in slug:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return PHOTO_POOL[h % len(PHOTO_POOL)]


def cover_src(p) -> str:
    """Prefer the JPG cover under blog/art/; fall back to SVG."""
    jpg = f"art/{p['slug']}.jpg"
    if os.path.exists(os.path.join(BLOG, jpg)):
        return jpg
    return f"art/{p['slug']}.svg"


def img_size(rel):
    """(w, h) of a file under blog/, or None."""
    path = os.path.join(BLOG, rel)
    if Image is None or not os.path.exists(path) or not rel.endswith(".jpg"):
        return None
    with Image.open(path) as im:
        return im.size


def dims_attr(rel):
    s = img_size(rel)
    return f' width="{s[0]}" height="{s[1]}"' if s else ""


MARK = covers.MARK.replace('width="100" height="100"', 'class="daybreak" aria-hidden="true"')

APP_STORE = "https://apps.apple.com/us/app/filmsera-group-film-camera/id6781880091"
SMART_BANNER = '<meta name="apple-itunes-app" content="app-id=6781880091"/>'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"/>'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600'
         '&family=Hanken+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700'
         '&display=swap" rel="stylesheet"/>')


def esc(s):
    return htmlmod.escape(s, quote=True)


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
      <p>One shared camera for the whole party. Guests join by QR code, every photo stays hidden until the reveal, then the roll opens for everyone at once.</p>
      <a class="btn" href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store">Download on the App Store</a>
    </div></div></section>'''


def card(p):
    return f'''<a class="card reveal" data-cat="{p['cat']}" href="{p['slug']}.html">
      <div class="art"><img loading="lazy" src="{cover_src(p)}" alt="{esc(p['title'])}"/></div>
      <div class="body">
        <div class="meta"><span class="cat">{p['cat']}</span><span>·</span><span>{p['read']} min read</span></div>
        <h3>{p['title']}</h3>
        <p>{p['excerpt']}</p>
        <span class="more">Read the story →</span>
      </div></a>'''


def related_for(post):
    """Three related posts: same category first (guides before older posts), then others."""
    others = [q for q in POSTS if q["slug"] != post["slug"]]
    same = [q for q in others if q["cat"] == post["cat"]]
    same.sort(key=lambda q: not q.get("guide"))
    rest = [q for q in others if q["cat"] != post["cat"]]
    if post.get("guide"):
        rest.sort(key=lambda q: not q.get("guide"))
    picks = (same + rest)[:3]
    cards = "".join(card(p) for p in picks)
    return f'''<section class="related"><div class="wrap">
      <div class="lbl">Keep reading</div>
      <div class="grid">{cards}</div></div></section>'''


def page_title(p):
    """Keep <title> under ~60 chars: short suffix, dropped for long headlines."""
    if p.get("seo_title"):
        return p["seo_title"]
    title = p["title"]
    return title if len(title) > 50 else f"{title} · Filmsera"


def strip_tags(s):
    return htmlmod.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def article_ld(p):
    url = f"{BASE}/blog/{p['slug']}.html"
    img_rel = cover_src(p)
    image = f"{BASE}/blog/{img_rel}"
    size = img_size(img_rel)
    posting = {
        "@type": "BlogPosting",
        "@id": f"{url}#article",
        "headline": p["title"],
        "description": p.get("desc") or p["excerpt"],
        "datePublished": p["date"],
        "dateModified": p.get("updated") or p["date"],
        "author": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "Filmsera", "url": f"{BASE}/"},
        "publisher": {"@id": f"{BASE}/#org"},
        "image": ({"@type": "ImageObject", "url": image, "width": size[0], "height": size[1]}
                  if size else image),
        "mainEntityOfPage": url,
        "url": url,
        "articleSection": p["cat"],
        "inLanguage": "en",
    }
    if p.get("words"):
        posting["wordCount"] = p["words"]
    kws = [k for k in p.get("keywords", []) if k]
    if kws:
        posting["keywords"] = ", ".join(kws)
    graph = [posting, {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Journal", "item": f"{BASE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
        ],
    }]
    if p.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "mainEntity": [{"@type": "Question", "name": strip_tags(f["q"]),
                            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(f["a"])}}
                           for f in p["faq"]],
        })
    return {"@context": "https://schema.org", "@graph": graph}


def head(p, ld=None):
    title, slug = p["title"], p["slug"]
    desc = esc(p.get("desc") or p["excerpt"])
    img_rel = cover_src(p)
    size = img_size(img_rel)
    og_dims = (f'<meta property="og:image:width" content="{size[0]}"/>\n'
               f'<meta property="og:image:height" content="{size[1]}"/>\n') if size else ""
    ld_tag = ""
    if ld:
        ld_tag = ('<script type="application/ld+json">'
                  + json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
                  + "</script>\n")
    preload = (f'<link rel="preload" as="image" href="{img_rel}" fetchpriority="high"/>\n'
               if p.get("guide") else "")
    return f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>{esc(page_title(p))}</title>
<meta name="description" content="{desc}"/>
<meta name="theme-color" content="#0A0807"/>
{SMART_BANNER}
<meta property="og:title" content="{esc(title)}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="Filmsera"/>
<meta property="og:image" content="{BASE}/blog/{img_rel}"/>
{og_dims}<meta property="og:url" content="{BASE}/blog/{slug}.html"/>
<meta property="article:published_time" content="{p['date']}"/>
<meta property="article:modified_time" content="{p.get('updated') or p['date']}"/>
<meta property="article:section" content="{esc(p['cat'])}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{esc(title)}"/>
<meta name="twitter:description" content="{desc}"/>
<meta name="twitter:image" content="{BASE}/blog/{img_rel}"/>
<link rel="canonical" href="{BASE}/blog/{slug}.html"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
{preload}{FONTS}
<link rel="stylesheet" href="journal.css"/>
{ld_tag}</head><body>'''


def build_cover(p):
    a, b = CATS[p["cat"]]
    svg = covers.cover_svg(p["slug"], p["motif"], a, b)
    with open(os.path.join(ART, f"{p['slug']}.svg"), "w") as f:
        f.write(svg)
    if p.get("guide"):
        return  # guide posts own a generated hero at art/<slug>.jpg; never overwrite it
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

# Older posts point readers to the newer, deeper guide on the same subject.
GUIDE_LINKS = {
    "collecting-guest-photos-without-chaos": ("how-to-collect-photos-from-wedding-guests",
                                              "How to collect photos from wedding guests: 9 ways compared"),
    "shared-camera-roll-at-a-wedding": ("qr-code-for-wedding-photos", "How to set up a QR code for wedding photos"),
    "how-to-run-filmsera-at-your-wedding": ("wedding-qr-code-sign-wording", "Wedding QR code sign wording examples"),
    "from-roll-to-recap": ("how-to-make-an-event-recap-video", "How to make an event recap video for Reels and TikTok"),
    "disposable-camera-party-playbook": ("birthday-party-photo-ideas", "Birthday party photo ideas"),
    "one-trip-one-film": ("best-way-to-share-photos-with-a-group", "The best way to share photos with a group"),
    "ten-creative-prompts-for-your-film": ("wedding-photo-scavenger-hunt", "Wedding photo scavenger hunt prompts"),
    "what-makes-a-photo-feel-like-film": ("how-to-make-photos-look-like-film-on-iphone",
                                          "How to make photos look like film on iPhone"),
    "the-quiet-comeback-of-the-disposable-camera": ("disposable-cameras-at-weddings-worth-it",
                                                    "Disposable cameras at weddings: are they worth it?"),
    "best-disposable-camera-apps-for-weddings-2026": ("how-to-collect-photos-from-wedding-guests",
                                                      "How to collect photos from wedding guests: 9 ways compared"),
}


def landing_note(p):
    parts = []
    if p["slug"] in LANDING:
        href, label = LANDING[p["slug"]]
        parts.append(f'Planning your own? See <a href="{href}">{label}</a>, or read the <a href="/faq/">FAQ</a>.')
    g = GUIDE_LINKS.get(p["slug"])
    if g and any(q["slug"] == g[0] for q in POSTS):
        parts.append(f'Related guide: <a href="/blog/{g[0]}.html">{g[1]}</a>.')
    return f'<p class="landing-link">{" ".join(parts)}</p>' if parts else ""


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", strip_tags(text).lower()).strip("-")
    return s[:60].rstrip("-") or "section"


def add_toc(body):
    """Give every <h2> an id; return (body, toc_html). TOC skips the FAQ heading."""
    seen = set()
    items = []

    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        if "id=" in attrs:
            hid = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            hid = slugify(inner)
            base, n = hid, 2
            while hid in seen:
                hid, n = f"{base}-{n}", n + 1
            attrs = f'{attrs} id="{hid}"'
        seen.add(hid)
        label = strip_tags(inner)
        if label.lower() not in ("faq", "faqs", "frequently asked questions"):
            items.append((hid, label))
        return f"<h2{attrs}>{inner}</h2>"

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, body, flags=re.S)
    if len(items) < 4:
        return body, ""
    lis = "".join(f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in items)
    return body, f'<div class="toc" role="navigation" aria-label="In this article"><div class="lbl">In this article</div><ol>{lis}</ol></div>'


def insert_toc(body, toc):
    if not toc:
        return body
    m = re.search(r'<div class="answer">.*?</div>', body, flags=re.S)
    if m:
        return body[:m.end()] + toc + body[m.end():]
    return toc + body


def build_article(p):
    frag = os.path.join(CONTENT, f"{p['slug']}.html")
    if os.path.exists(frag):
        with open(frag, encoding="utf-8") as f:
            body = f.read()
    else:
        body = "<p>Coming soon.</p>"
    divider = f'<div class="divider">{covers.divider_svg(CATS[p["cat"]][0])}</div>'
    body = body.replace("{{divider}}", divider)
    if p.get("guide"):
        body, toc = add_toc(body)
        body = insert_toc(body, toc)
    body += landing_note(p)

    img_rel = cover_src(p)
    cover_alt = esc(p["title"])
    if p.get("guide"):
        cover = (f'<img src="{img_rel}" alt="{cover_alt}"{dims_attr(img_rel)} fetchpriority="high" decoding="async"/>')
        prose_cls = "prose guide"
        credit = ('<p class="img-note">Photos in this article are illustrations created for Filmsera, '
                  'not customer photos. App screenshots are from Filmsera on iPhone.</p>')
    else:
        cover = f'<img src="{img_rel}" alt="{cover_alt}"{dims_attr(img_rel)}/>'
        prose_cls = "prose"
        credit = ""

    html = head(p, article_ld(p))
    html += nav()
    html += f'''<div class="wrap" style="padding-top:18px"><a class="btn" href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store" style="display:inline-flex">Download Filmsera</a></div>
<article>
  <div class="wrap"><header class="article-hero">
    <div class="crumbs"><a href="/">Home</a> › <a href="index.html">Journal</a> › <span>{p['cat']}</span></div>
    <span class="pill">{p['cat']}</span>
    <h1>{p['title']}</h1>
    <p class="dek">{p['dek']}</p>
    <div class="byline"><span>Filmsera</span><span class="dot">·</span>
      <time datetime="{p['date']}">{pretty(p['date'])}</time>{updated_html(p)}
      <span class="dot">·</span><span>{p['read']} min read</span></div>
  </header></div>
  <div class="wrap"><figure class="cover{' wide' if p.get('guide') else ''}">
    {cover}
  </figure></div>
  <div class="wrap"><div class="{prose_cls}">{body}</div></div>
  <div class="wrap"><div class="end-note">
    <div class="mark">{MARK}</div>
    <div><h4>Written by the Filmsera team</h4>
    <p>Filmsera is a shared disposable camera app for iPhone: create a film for your event, let guests join by QR code from the app or their phone's browser, and open the whole roll together at the reveal. <a href="{APP_STORE}" target="_blank" rel="noopener" data-cta="app_store" style="color:var(--brass)">Download on the App Store →</a></p>{credit}</div>
  </div></div>
</article>'''
    html += related_for(p)
    html += cta_band()
    html += footer()
    html += '<script src="journal.js"></script></body></html>'

    with open(os.path.join(BLOG, f"{p['slug']}.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_index():
    feat = POSTS[0]
    rest = POSTS[1:]
    used = {p["cat"] for p in POSTS}
    cats = [c for c in CAT_ORDER if c in used] + [c for c in CATS if c in used and c not in CAT_ORDER]
    filters = '<button class="filter on" data-filter="all">All</button>' + "".join(
        f'<button class="filter" data-filter="{c}">{c}</button>' for c in cats)
    grid = "".join(card(p) for p in rest)
    blog_ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": f"{BASE}/blog/#blog",
        "name": "The Filmsera Journal",
        "url": f"{BASE}/blog/",
        "publisher": {"@id": f"{BASE}/#org"},
        "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{BASE}/blog/{p['slug']}.html",
                      "datePublished": p["date"]} for p in POSTS],
    }
    ld_tag = ('<script type="application/ld+json">'
              + json.dumps(blog_ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
              + "</script>")

    html = f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>Filmsera Journal: Wedding, Party and Photo-Sharing Guides</title>
<meta name="description" content="Guides to collecting wedding guest photos, QR photo sharing, wedding slideshows, party and holiday ideas, and the film look, from the team behind Filmsera."/>
<meta name="theme-color" content="#0A0807"/>
{SMART_BANNER}
<meta property="og:title" content="The Filmsera Journal"/>
<meta property="og:description" content="Guides to wedding guest photos, slideshows, party ideas and the film look."/>
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
{ld_tag}
</head><body>'''
    html += nav()
    html += '''<header class="j-head"><div class="wrap">
    <span class="pill">The Journal</span>
    <h1>Notes on film, memory, and shooting together.</h1>
    <p>Practical guides for weddings, parties and trips: collecting everyone's photos, QR codes and signs, slideshows and recap reels, and getting the film look on your phone.</p>
    <div class="j-mosaic" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:28px auto 0;max-width:720px">
      <img src="../shots/originals/06-house-party-couch.jpg" alt="" style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px" loading="lazy"/>
      <img src="../shots/originals/12-beach-trip.jpg" alt="" style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px" loading="lazy"/>
      <img src="../shots/originals/01-wedding-dancefloor.jpg" alt="" style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px" loading="lazy"/>
      <img src="../shots/originals/14-city-night.jpg" alt="" style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px" loading="lazy"/>
    </div>
    <p style="margin-top:20px"><a class="btn" href="''' + APP_STORE + '''" target="_blank" rel="noopener" data-cta="app_store">Download Filmsera</a></p>
  </div></header>'''
    html += f'''<div class="wrap"><article class="featured reveal">
    <div class="art"><a href="{feat['slug']}.html"><img loading="lazy" src="{cover_src(feat)}" alt="{esc(feat['title'])}"{dims_attr(cover_src(feat))}/></a></div>
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

    with open(os.path.join(BLOG, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    os.makedirs(ART, exist_ok=True)
    for p in POSTS:
        build_cover(p)
        build_article(p)
    build_index()
    guides = sum(1 for p in POSTS if p.get("guide"))
    have = sum(1 for p in POSTS if os.path.exists(os.path.join(CONTENT, f"{p['slug']}.html")))
    print(f"Built {len(POSTS)} articles ({guides} guides) + index. "
          f"Content fragments present: {have}/{len(POSTS)}.")


if __name__ == "__main__":
    main()
