# Filmsera — marketing site + legal pages

Public site for **Filmsera** (group film camera on the [App Store](https://apps.apple.com/us/app/filmsera-group-film-camera/id6781880091)): marketing, Look Lab, vs comparisons, Journal CTAs, Privacy / Terms / Support. Hosted on GitHub Pages; **DNS / custom-domain setup unchanged**.

**Live:** https://getfilmsera.cam/

| Path | Purpose |
|---|---|
| `index.html` | App Store marketing landing (hero, Looks, Reveal, Recap, FAQ, CTAs) |
| `looks/` | **Look Lab** — browse film Looks |
| `vs/` | Honest comparisons (Once, POV, Scene, Dazz, …) |
| `guides/` | Printable Host checklists (e.g. wedding guest photo plan) |
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

## Product notes

- `docs/PRODUCT-APP-CLIP-GAP.md` — competitors lead with no-download / App Clip guest join; Filmsera QR still requires iPhone install. Roadmap only — do not market as available.

## Before you launch — required edits

1. **Support email** — replace placeholder `support@getfilmsera.cam` if needed.
2. **Legal review** — drafts, not legal advice.
3. **Waitlist** (optional) — wire `WAITLIST_URL` if collecting emails.

## Custom domain / DNS

Paths stay the same; only the host changes. GitHub Pages DNS / CNAME workflow is unchanged — see the domain checklist historically documented below and in the app repo’s `AppStore/DOMAIN_SETUP.md`.

**Absolute URLs to update on a host swap:** `index.html` og:image, `journal-src/build.py` → `BASE` (then rerun `build.py`), in-app paywall / invite base, App Store Connect marketing URLs.

## Daybreak brand assets

`brand/filmsera-mark.svg` is the canonical brass Daybreak mark (560 × 660).
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
tight padding so the sun still reads in a browser tab. `shots/filmsera-social.png`
is the vector mark on a full-bleed 1200 × 630 ink + brass-glow card.

Phone screenshots and Look thumbnails are product imagery, not brand assets.
`shots/screens/01-start.png` and `06-group.png` had the old ✦ glyph baked in; it was
painted over with the Daybreak mark in place. Re-render them from the app repo's
App Store pipeline when the panels are next refreshed. `shots/panel-*.png` are
unused by the site and still show the old glyph.
