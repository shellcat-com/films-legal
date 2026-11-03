# Web join app-style camera: QA report

- **Branch:** `feat/webjoin-app-ui` @ 01c9f36 (b3ff8c9 + 01c9f36)
- **Date:** 2026-11-03
- **Backend:** dev Convex `resilient-goat-339`. `/web/lookup`, `/web/join` and `/web/status` return `presetID`. Confirmed live: `"presetID":"original"`.
- **Pages served:** the worktree on :8796 (QA) and on :8787 (regression E2E). Both servers are stopped.
- **QA harness:** `/tmp/webjoin-qa/*.mjs`, outside the repo. Screenshots are in `docs/webjoin-ui/qa-shots/` (untracked).
- **Not changed:** `join.html` and all backend code.

## Verdict: **NO-GO**, close to GO

The core works on WebKit and Chromium: the real looks, a single grade, the fallbacks, and every data-path behaviour. Four things block launch. All are small.

1. **Not tested on Firefox.** Playwright's Firefox won't launch on this Mac (see §1). It has to be run somewhere else first.
2. **The focus trap leaks in Safari/WebKit** (§5, F1).
3. **"Get the iPhone app" renders as a muted, cramped pill**, so it reads as disabled (§2, V1).
4. **The viewfinder card floats mid-screen** instead of sitting under the header, as it does in the app (§2, V2).

Viewfinder FPS on a real Pixel or iPhone still needs a device check (§4). Headless emulation renders WebGL in software, so its numbers are only a pessimistic bound.

**Totals:** 185 automated checks PASS and 10 FAIL. Of the FAILs:
- 2 are test bugs: my seed used 3 shots, not 5.
- 2 are FPS thresholds that are inconclusive under software GL.
- 2 are harness issues: a transient Convex CLI 5xx, and the WebKit fake-camera shim. I re-ran both and they pass.
- 4 are real: the 3 WebKit focus-trap failures and 1 WebKit focus-return failure.

---

## 1. Regression

| Check | Result |
|---|---|
| `PLAYWRIGHT_DIR=/tmp/webjoin-e2e node scripts/webjoin-e2e.mjs` (:8787, WEBDEV) | **PASS**: 49/49, "ALL PASSED" |
| `node scripts/csp-hash.mjs --check` | **PASS**: "CSP hash OK" |
| 0 CSP violations, Chromium (Pixel 8 + desktop) | **PASS**. Checked with the `securitypolicyviolation` listener plus console, on camera, album and every look |
| 0 CSP violations, WebKit (iPhone 15) | **PASS** |
| 0 CSP violations, Firefox | **NOT RUN (BLOCKED)**. See below |

**Why Firefox is blocked:** Playwright Firefox (builds 1555, 1543 and 1538, headless and headed, sandbox on and off) exits with `Could not find profile folder` or `sandbox_extension_issue_file_to_process … Operation not permitted` on this macOS 27 beta host. Stock Firefox.app headless gives the same sandbox error. **Action:** run `looks.mjs` / `behave.mjs` with `ENG=firefox` on CI Linux or another Mac before launch.

## 2. Visual fidelity vs the app

I checked against the Swift source: `FilmCameraView.swift`, `ShutterButton.swift`, `CameraInstruments.swift`, `CameraChrome.swift`, `FilmDetailView.swift`, `FilmPhotoViewer.swift`, `NameSetupView.swift`, `StatTrio.swift` and `ContributorAvatars.swift`.

These already match: graphite #292929, shutter gradient #383838→#212121 at 78 px with press scale .88, record red, viewfinder radius 28, tiles 74×62 r18, hint pill, focus reticle, and the per-look aspect (verified for 0.667, 0.75, 1.0 and 2.39).

Overall result: **PASS with mismatches**. Fix V1–V3 before launch; the rest are polish.

**V1. "Get the iPhone app" looks disabled — FAIL, a real bug.**
- `join.html:339` `.d-foot a` overrides `.btn2` (`:201`). The text turns muted #A89C88 and the side padding drops to 6 px.
- Seen in `qa-shots/b-desktop-03-camera.png` and in `09`/`11`.
- Fix: `.d-foot .btn2{color:var(--cream);padding:0 18px}`.

**V2. The viewfinder is centred in the free space — FAIL.**
- The app stacks header → 14 pt → card → controls → spacer → deck (`FilmCameraView.swift:57-67`).
- Web uses `place-items:center` (`join.html:245`), which leaves a gap of about 56 px under the header on iPhone and desktop.
- Fix: `.vf-wrap{place-items:start center}`.

**V3. The flash/zoom/flip row keeps a 58 px empty band when all three are hidden.**
- `join.html:281/286` (`visibility:hidden`).
- Fix: toggle a class from `setupTrackControls` and set `.ctrl.empty{display:none}`.
- When the row is shown:
  - App padding-top is 22 (`FilmCameraView.swift:64`), web is 14. Fix: `padding:22px 22px 0`.
  - App icons are 20 pt (`:280,:311`), web is 24 (`join.html:284`). Fix: 20 px.

**Camera, other mismatches:**
- **Counter neighbour spacing:** web uses fixed 30/44/58 px slots (`join.html:1369`). The app uses a 7 pt HStack gap (`CameraChrome.swift:18`), so two-digit neighbours nearly vanish on web. Fix: 20/30/42 px slots and `.counter .track{align-items:baseline}` (`:294`).
- **Glyph sizes:** QR glyph is 20 px vs 18 pt (`:237` vs `FilmCameraView.swift:137`). Sealed-tile glyph is 24 vs 20 (`:300` vs `:480`). Header chevron is 22 vs 20 (`:235`).
- **Subtitle:** web shows "Name · 2h left" in cream (`:1259`, `:242`). The app shows only the time (`:126`). Keeping the name is fine as a deliberate choice, but mute it: `.g-sub .chip{color:inherit}`.
- **First-run hint:** "Tap the shutter to take a photo" vs the app's "Tap for photo · hold for video". The web copy is correct, because the web can't record video.

**Roll finished:**
- The overlay covers only the card (`join.html:257,311`). The app dims the whole screen at 82% (`FilmCameraView.swift:517`). Fix: add `.cam.done .g-top{opacity:.3}`, or make `.msg.done` cover the whole `.cam`.
- Copy and type differ:

  | | App | Web |
  |---|---|---|
  | Title | "You're out of shots", serif 24 (`:520`) | "That's your roll.", 28 px (`:1422,:256`) |
  | Body | Serif 18, "N shots in {title}. Photos stay hidden until reveal." (`:523`) | Hanken 15 |
  | Gap | 16 | 12 |

**Name sheet** (nearest app view is `NameSetupView.swift:32-82`):
- Title is 34 px vs 30 (`join.html:214`).
- Field is r14 #070605 vs r13 #1C1813 with a hairline (`:216`).
- The CTA is a gradient with glow in mono vs a flat brass button in Hanken 16 bold with 14 pt padding.
- When focused, the field shows a double brass ring. Fix: `.field:focus-visible{outline:none}`.

**Waiting for reveal / details:** the app shows one brass Space Mono 26 readout (`FilmDetailView.swift:707-722`). The web shows a 4-box D/H/M/S grid (`join.html:101-103`). Optional fix.

**Album:**

| Item | App | Web | Fix |
|---|---|---|---|
| Recap CTA | Flat brass, Hanken 17 bold, 56 tall (`FilmDetailView.swift:604-610`) | Mono gradient with glow (`join.html:111-113`) | Match the app |
| Tile captions | None (`:1244`) | `.by` names (`:364`) | `.grid .by{display:none}` |
| Grid gap | 6 | 7 (`:359`) | 6 |
| Stats | 22 px, label gap 8, no tracking (`StatTrio.swift:20-22`) | 24 px, label gap 6, 1.4 px tracking (`:353-355`) | Match the app |
| Eyebrow kerning | 3 | 4 (`:351`) | 3 |
| Title | 34 | clamp 36–46 (`:352`) | 34 |
| Avatars | 26 px, -8 overlap, at most 4 + "+N" (`ContributorAvatars.swift:15-40`) | 30 px, up to 8 (`:357,:1791`) | Match the app |

**Lightbox:**

| Item | App | Web |
|---|---|---|
| Background | #060504 (`FilmPhotoViewer.swift:27`) | #000 (`join.html:372`) |
| Save button | Full-width cream r16, Hanken 15 bold, "Save to camera roll" (`:84-92`) | Right-aligned brass mono capsule, "Save photo" (`:381,:1872`) |
| Close button | Brass xmark on black 50% | Cream X on graphite (`:313`) |
| Image | Edge to edge | 8 px padding, r6 (`:375-376`) |

Prev/next buttons are web-only and fine to keep.

**Toasts:** the app's confirmation is a brass capsule in Space Mono 13 bold (`FilmPhotoViewer.swift:95-100`). Web's `.toast` is a #1C1813 r16 card in Hanken 14 (`join.html:341-342`). Fix: `border-radius:999px` and a `.toast.ok` brass variant. The long offline `.queue` text wraps to two lines over the viewfinder (`qa-shots/b-*-05-offline.png`). That is acceptable.

## 3. Looks

**Can `seedFilm` set a preset?** No. It hardcodes `presetID:"original"` (`Camera-webjoin/convex/webJoinDev.ts:70`) and passing `presetID` is rejected by its validator. Instead, the harness rewrites `film.presetID` in the `/web/lookup|join|status` responses.

**How the page maps preset → LUT:** `lookIdOf` (`join.html:882-886`) sends unknown or missing IDs to `original`, and the file is `/assets/looks/<id>.png` (`:895`).

**Method:** the fake camera is a flat RGB(180,120,80) frame. At the frame centre the vignette is 1. I compared the centre colour against a CPU trilinear lookup through the same PNG, applied once and applied twice. The saved photo is the full-size JPEG fetched from `/web/album` after `revealFilm`.

| Preset | Engine | Correct LUT, and only it | Viewfinder Δ once / Δ twice | Saved Δ once / Δ twice | Aspect (viewfinder and saved) |
|---|---|---|---|---|---|
| disposable | Pixel 8 | PASS | 1 / 28 | 0 / 29 | 2:3 PASS |
| cpm35 (Sprocket 35) | Pixel 8 | PASS | 1 / 20 | 1 / 21 | 2:3 PASS |
| instant | Pixel 8 | PASS | 2 / 27 | 1 / 30 | 1:1 PASS |
| vhs | Pixel 8 | PASS | 2 / 8 | PASS | 3:4 PASS |
| eightmm (8mm) | Pixel 8 | PASS | PASS | PASS | 3:4 PASS |
| digi (Digicam) | Pixel 8 | PASS | PASS | PASS | 3:4 PASS |
| original | Pixel 8 | PASS | PASS | PASS | 2:3 PASS |
| kino (2.39 wide) | Pixel 8 + iPhone 15 | PASS | PASS | PASS | 2.39 PASS |
| grf (Noir, mono) | Pixel 8 | PASS | PASS (146,145,145) | PASS | PASS |
| disposable, instant | iPhone 15 (WebKit) | PASS | 1–2 / ≥27 | PASS | PASS |

- **The viewfinder shows the graded image: PASS.** Every case is within 2 of the once-graded value.
- **The saved photo carries the same grade: PASS.** Saved vs viewfinder is within 3.
- **The grade is not applied twice: PASS.** Capture develops from the raw `<video>`, not from the graded canvas (`join.html:1619`). The album uses no CSS filter.
- **Missing LUT** (all `/assets/looks/*` return 404): **PASS, graceful.**
  - The viewfinder falls back to the plain live video.
  - The shot saves in 1.5 s with no toast and no errors.
  - The saved photo gets the generic fixed curve: (181,122,80) from a (180,120,80) input.
  - Note: the preview is ungraded but the saved photo has the fallback curve. The 404 is also requested twice (`renderLook`, then `gradeCPU`). Cosmetic only.
- **No WebGL** (`--disable-webgl --disable-3d-apis`, confirmed `getContext` returns null): **PASS.**
  - The viewfinder shows plain, ungraded video. This is the documented fallback.
  - The saved photo goes through the CPU cube: exactly (217,133,86), the same as WebGL.
  - With a 2560×1920 stream, the 1280×1920 output saved in 1.3 s.
- **Stale comment:** `join.html:881` still says "/web/* film summary doesn't carry presetID yet". Remove it.

## 4. Performance

All measured on Chromium Pixel 8 emulation, headless, where WebGL is software (SwiftShader).

**Viewfinder FPS: INCONCLUSIVE, needs a device.** With a 1920×1440 fake stream:

| CPU throttle | Video / draw fps | rAF fps | Same page without WebGL |
|---|---|---|---|
| 1× | 23.4 / 23.4 | 52 | 30 fps video, 60 rAF |
| 4× | 10.8 / 10.8 | 27 | 30 fps video, 60 rAF |

- The renderer draws every frame it gets. The cost is software GL uploading the full camera frame with `texImage2D` on every frame (`join.html:957`).
- On a real phone GPU this should be far cheaper, but it is unverified.
- **Risk:** the page asks for 2560×1920 (`:1556`) and uploads the whole frame per draw, even though it shows a ≤1280 px canvas. **Suggestion:** request about 1920 on the long edge, or measure on an iPhone 12 and a mid-range Android before launch.

**Shutter → saved: PASS.**
- Shutter → counter updates: 330–390 ms at 1×, 1.4–1.5 s at 4×.
- Shutter → "All shots saved ✓": 1.2–2.7 s at 1× (Pixel, iPhone, desktop), 3.1–4.3 s at 4×.

**Page weight: PASS, and LUTs are lazy.**
- Invite page: 232 KB, with no LUT.
- Camera live: 304 KB total. That is join.html 123 KB, fonts 83 KB, sounds 45 KB (loaded on first press), JS 21 KB, and **exactly one LUT** (26 KB, the film's own).
- All 25 LUTs together are 787 KB on disk and are never bulk-loaded.

## 5. Behaviour that must not regress

| Item | Result |
|---|---|
| Join (name sheet, empty name, duplicate names, Terms/Privacy) | PASS: E2E plus WebKit, Pixel and desktop |
| Shoot to limit → shutter disabled + roll finished | PASS on all 3 engines |
| Reload resume (same guest, same count) | PASS on all 3 engines |
| Offline retry (shot kept on the phone, counted, uploads on reconnect) | PASS on all 3 engines |
| Upload timeout retry | PASS (E2E: hung upload retried, 37 s) |
| Lost commit response counted once | PASS (E2E) |
| Late join after reveal | PASS. The invite offers "See the photos in your browser" and lands on the album |
| Host-only | PASS on all 3 engines |
| Full film (`guestCap`) | PASS: no browser join |
| Removed guest | PASS (E2E) |
| Rate-limit message | PASS. 429 lookup (E2E) and 429 join both show "Too many tries…" |
| 8- and 6-char codes | PASS. `UIQ12345` and `UIQ123`, typed in lower case into the not-found form, open the invite and join. The two FAIL lines in the log are my seed using 3 shots, not 5 |
| Focus trap: name sheet, QR sheet, lightbox (Chromium) | PASS |
| **Focus trap (WebKit / Safari default Tab)** | **FAIL (F1)**, below |
| **QR sheet: Esc returns focus (WebKit)** | **FAIL (F2)**, below |
| Targets ≥ 44 px (camera, details, album, lightbox) | PASS on all 3 engines |
| prefers-reduced-motion | PASS: counter and shutter transitions 0 s, the counter doesn't slide, blink ≤ .01 s |
| No page errors | PASS on every run |

**F1. The focus trap leaks on WebKit/Safari.**
- `trapTab` (`join.html:815-823`) only steps in when focus is on the first or last element, or already outside the dialog.
- In Safari's default Tab mode, Tab skips buttons and links, so native Tab from the name field jumps to the "Filmsera" link behind the modal. The trace on the name sheet was `INPUT → OUT:Filmsera`.
- With full keyboard access (Option+Tab) the trap works. The same leak affects the QR sheet and the lightbox.
- **Repro:** WebKit iPhone 15 → Join in your browser → press Tab repeatedly. Focus alternates between inside and outside the dialog.
- **Fix:** in `trapTab`, always `preventDefault()` and move to `els[(i ± 1 + n) % n]`, or set `inert` on `#app` while a modal is open.

**F2. Focus-return target on WebKit.**
- Safari doesn't focus a button when it is clicked, so `opener = document.activeElement` (`join.html:1333`) records a stale element. In the test it was an INPUT.
- On close, focus goes there instead of to the QR button.
- **Fix:** `const opener = document.getElementById("qrbtn")`. The lightbox already takes the tile as its opener.

## 6. Desktop Mac layout (Chromium 1440×900)

| Check | Result |
|---|---|
| Camera at phone size | PASS: 420×804 card, 44 px radius |
| Camera + details centred as a pair | PASS: offset 0 px |
| Camera itself centred on the page | Not the case: it sits 208 px left of centre, beside the details. This is by design (`join.html:383`); confirm that's what you want |
| "Get the iPhone app" shown, "Open in the app" absent | PASS on the invite page (E2E) and the camera page. iPhone WebKit shows both (correct) |
| Button styling | See V1: the button looks disabled |

## To clear for GO

1. Run Firefox: `cd /tmp/webjoin-qa && ENG=firefox EXTRAS=0 node behave.mjs`, then `LOOKS=disposable:firefoxPhone node looks.mjs`, on a host where Playwright Firefox launches.
2. Fix F1 and F2 (focus), and V1–V3 (CSS).
3. Do one real-device FPS check on iPhone and Android. Lower the requested camera resolution if it runs hot.

---

## Re-QA: commit 7bcd796 (2026-11-03)

**Scope:** WebKit iPhone 15, Chromium Pixel 8 and Chromium desktop. join.html was not edited. The harness is `/tmp/webjoin-qa` (the roll-finished check now expects "You're out of shots"). Screenshots `qa-shots/b-*` and `r-*` were refreshed.

### Verdict: **GO** for WebKit and Chromium

Every must-fix item and every regression check passes. Two conditions remain from the first round, and neither is caused by this commit:

1. **Firefox is still unverified.** Playwright's Firefox can't launch on this host.
2. **Viewfinder FPS still needs one check on a real device.** This is now lower risk, because the camera stream was cut from 2560 to 1920 px on the long edge.

| Check | Result |
|---|---|
| E2E (`webjoin-e2e.mjs`, :8787) | **PASS**: all 48 checks plus "ALL PASSED". The E2E's own roll-finished check now matches "You're out of shots" |
| `csp-hash.mjs --check` | **PASS** (new script hash) |
| 0 CSP violations / 0 page errors | **PASS** on all 3 engines: camera, album, lightbox, two-camera and looks runs |
| **F1** focus trap on WebKit (name sheet, QR sheet, lightbox) | **PASS**: 12/12 Tabs stay inside on every engine. The page behind is `inert` + `aria-hidden` while open |
| **F2** QR sheet Esc returns focus | **PASS**: focus goes back to `qrbtn` on all 3 engines. The lightbox returns focus to its tile |
| **V1** "Get the iPhone app" | **PASS**: cream text rgb(244,236,221), 20 px padding. The automated line logged FAIL only because my colour regex was too strict |
| **V2** viewfinder under the header | **PASS**: 14 px gap below the header on all 3 engines |
| **V3** control row collapse | **PASS**: one camera and no torch/zoom → `.ctrl.empty`, `display:none`, flip hidden |
| Flip only with two cameras | **PASS**: two fake cameras → flip shown, row visible, 44×44 target, on all 3 engines |
| Looks spot-check (viewfinder vs saved) | **PASS**. Fake camera is 1440×1920 portrait. disposable@iPhone 15, vhs@Pixel 8, instant@desktop each loaded only their own LUT. Viewfinder Δ1–2 and saved Δ≤2 from the once-graded value, not the twice-graded one |
| Saved sizes | **PASS**. Live shots are 1280×1920 (2:3), 1440×1920 (3:4) and 1440×1440 (1:1). A picked photo is 2560×1707 (E2E) |
| Behaviour (join, shoot to limit, reload resume, offline retry, host-only, full film, late join after reveal, 6- and 8-char codes, 429 join, reduced motion, ≥44 px on camera/album/lightbox) | **PASS** on all 3 engines (89 checks) |
| Desktop | **PASS**: 420×804 camera; the camera + details pair is centred; "Get the iPhone app" shown, no "Open in the app" |

### Smaller visual items, verified in source and screenshots

- **Fixed — name sheet:** title 30, field r13 on `--elev`, flat brass CTA in Hanken 16 bold, no double focus ring.
- **Fixed — camera glyphs:** header 20, QR 18, controls 20, sealed tile 20. The subtitle name is muted.
- **Fixed — counter:** one neighbour on each side with a 7 px baseline gap, like the app.
- **Fixed — roll finished:** "You're out of shots" with the app body copy in serif 18, gap 16, and the header dims with the deck.
- **Fixed — countdown:** the develops countdown is now a single brass readout.
- **Fixed — album:** recap CTA 56 tall in Hanken 17 bold; tile captions visually hidden; grid gap 6; stats 22/8/no tracking; eyebrow 3; title 34; avatars 26 px with a +N chip after 4.
- **Fixed — lightbox:** background #060504, full-bleed image, brass close on black 50%, full-width cream Save button (r16).
- **Fixed — toasts:** a brass "Saved" capsule.
- **Left as is:**
  - The lightbox button reads "Save photo" (`join.html:1902`) rather than the app's "Save to camera roll". This is acceptable on the web, which saves a download.
  - The header subtitle keeps the guest name; this is deliberate.
- **Missing LUT:** the missing cube is now requested only once per page.

The servers on :8787 and :8796 were stopped.
