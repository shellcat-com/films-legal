# Filmsera — marketing site + legal pages

Public site for **Filmsera** (group film camera on the [App Store](https://apps.apple.com/us/app/filmsera-group-film-camera/id6781880091)): marketing, Look Lab, vs comparisons, Journal CTAs, Privacy / Terms / Support. Hosted on GitHub Pages; **DNS / custom-domain setup unchanged**.

**Live:** https://getfilmsera.cam/

| Path | Purpose |
|---|---|
| `index.html` | App Store marketing landing (hero, Looks, Reveal, Recap, FAQ, CTAs) |
| `looks/` | **Look Lab** — browse film Looks |
| `vs/` | Honest comparisons (Once, POV, Scene, Dazz, …) |
| `guides/` | Printable Host checklists (e.g. wedding guest photo plan + QR table sign) |
| `weddings/` `parties/` `holiday-parties/` `vintage-film-camera/` `how-it-works/` `faq/` | Use-case and info pages, **generated** by `scripts/build-pages.py` |
| `vs/index.html` `vs/pov.html` `vs/once.html` `vs/lense.html` | Sourced comparisons, **generated** by `scripts/build-pages.py` (`vs/dazz.html` / `vs/daze.html` are hand-written) |
| `open/<screen>/` | noindex fallbacks for the app's `/open/<screen>` universal links (generated) |
| `llms.txt` | Plain-text summary for AI search / agents |
| `sitemap.xml` | **Generated** by `scripts/build-sitemap.py` |
| `blog/` | **The Journal** — static editorial posts + CTAs → App Store |
| `journal-src/` | Journal authoring (`posts.py`, `content/`, `build.py`) — not served |
| `site/` | **Next.js source** for the marketing landing; export feeds the root static site |
| `privacy.html` / `terms.html` / `support.html` | Legal + support |
| `shots/` | App Store badges, panels, screen crops |

## The Journal

`/blog/` is generated locally from `journal-src/`:

```sh
python3 journal-src/build.py   # writes blog/index.html, blog/<slug>.html, blog/art/<slug>.svg
```

Add a post: prepend/append in `journal-src/posts.py`, drop `journal-src/content/<slug>.html`, rerun `build.py`.

## Generated static pages

```sh
python3 scripts/build-pages.py     # landing pages, FAQ, how-it-works, vs/, open/*
python3 journal-src/build.py       # the Journal
bash scripts/deploy-site.sh        # Next.js homepage export → index.html + _next/
python3 scripts/build-sitemap.py   # run last: lastmod comes from git / working tree
```

Copy lives in `scripts/pages_content.py`. **Pricing:** every price on the
generated pages comes from the `PRICING` block there, and the homepage FAQ
from `site/src/lib/faq.ts`. Both state the live 4.1 App Store model; switch
them (plus the homepage pricing cards in `site/src/app/page.tsx`, `llms.txt`
and the price table in `journal-src/content/best-disposable-camera-apps-for-weddings-2026.html`)
the day 4.2 is live.

## Product notes

- `docs/PRODUCT-APP-CLIP-GAP.md` — competitors lead with no-download / App Clip guest join; Filmsera QR still requires iPhone install. Roadmap only — do not market as available.

## Before you launch — required edits

1. **Support email** — replace placeholder `support@getfilmsera.cam` if needed.
2. **Legal review** — drafts, not legal advice.
3. **Waitlist** (optional) — wire `WAITLIST_URL` if collecting emails.

## Custom domain / DNS

Paths stay the same; only the host changes. GitHub Pages DNS / CNAME workflow is unchanged — see the domain checklist historically documented below and in the app repo’s `AppStore/DOMAIN_SETUP.md`.

**Absolute URLs to update on a host swap:** `index.html` og:image, `journal-src/build.py` → `BASE` (then rerun `build.py`), in-app paywall / invite base, App Store Connect marketing URLs.

## Pressmate brand assets

`brand/filmsera-mark.svg` is the canonical brass Pressmate camera mark (704 × 500, even-odd path generated from the app's `FilmseraMarkGeometry.swift`).
The Journal templates read this SVG directly. The Next.js navigation uses its
copy in `site/public/brand/`.

After installing the site's dependencies, regenerate favicon PNGs (16, 32, 96,
180, 512), ICO, apple-touch icon, social card, and public asset copies with:

```sh
node scripts/build-brand.cjs
# To refresh the exact app raster too, pass the app's icon-1024.png as an argument.
python3 journal-src/build.py
bash scripts/deploy-site.sh
```

Despite its name, `deploy-site.sh` only builds and copies the homepage export
into this checkout. Publishing happens when the owner merges to `main`.
`shots/filmsera-icon.png` is the app's original 1024 PNG, copied without redrawing;
`apple-touch-icon.png`, `favicon-180.png` and `favicon-512.png` are resized from it.
The 16/32/96 favicons, ICO and `favicon.svg` are drawn from the vector mark with
tight padding so the lens still reads in a browser tab. `shots/filmsera-social.png`
is the vector mark on a full-bleed 1200 × 630 ink + brass-glow card.

Phone screenshots and Look thumbnails are product imagery, not brand assets.
`shots/screens/01-start.png` and `06-group.png` are the app repo's App Store panels
`AppStore/exports/shot-1.png` / `shot-6.png`, resized to 415 × 900. `shots/panel-*.png` are
unused by the site and still show the old glyph.
