// Web join end-to-end test against the DEV Convex deployment (never prod).
//
// Drives join.html in headless Chromium: join → shoot (fake camera) → status
// hides photos → offline shot survives and retries → second guest shoots via the
// file-input fallback → shot limit → reveal (dev helper) → album shows photos.
//
// Prereqs (see docs in ~/Camera-webjoin/docs/plans/web-join-progress.md):
//   1. Dev backend deployed and WEBJOIN_DEV_TOOLS=1 set on dev.
//   2. A static server for this repo:   python3 -m http.server 8787   (repo root)
//   3. Playwright installed somewhere:  npm i --prefix /tmp/webjoin-e2e playwright@1.64.1
// Run:
//   PLAYWRIGHT_DIR=/tmp/webjoin-e2e node scripts/webjoin-e2e.mjs
// Env: CODE (default WEBDEV), CONVEX_DIR (default ~/Camera-webjoin), BASE (default http://localhost:8787)

import { createRequire } from "node:module";
import { execSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";

const require = createRequire(path.join(process.env.PLAYWRIGHT_DIR || process.cwd(), "noop.js"));
const { chromium } = require("playwright");

const CODE = process.env.CODE || "WEBDEV";
const CONVEX_DIR = process.env.CONVEX_DIR || path.join(os.homedir(), "Camera-webjoin");
const BASE = process.env.BASE || "http://localhost:8787";
const URL_ = `${BASE}/join.html?code=${CODE}&backend=dev`;
const OUT = process.env.OUT || "/tmp/webjoin-e2e/shots";
mkdirSync(OUT, { recursive: true });

let failures = 0;
const ok = (cond, msg) => { console.log(`${cond ? "PASS" : "FAIL"}  ${msg}`); if (!cond) failures++; };
const convex = (fn, args, identity) => {
  const id = identity ? ` --identity '${identity}'` : "";
  return execSync(`npx convex run ${fn} '${JSON.stringify(args)}'${id}`, { cwd: CONVEX_DIR, stdio: ["ignore", "pipe", "pipe"] }).toString();
};
const cspViolations = [];
const watch = (page, label) => {
  page.on("pageerror", e => { console.log(`pageerror ${label}:`, e.message); failures++; });
  page.on("console", m => { if (/Content Security Policy|Refused to (load|execute|connect|apply)/i.test(m.text())) cspViolations.push(`${label}: ${m.text()}`); });
};
const toastTexts = page => page.evaluate(() => [...document.querySelectorAll(".toast")].map(t => t.textContent));
const shot = (page, name) => page.screenshot({ path: path.join(OUT, `${name}.png`), fullPage: true });

async function countText(page) { return (await page.locator("#count").innerText()).replace(/\s+/g, " ").trim().toLowerCase(); }
async function waitSaved(page, left) {
  await page.waitForFunction((left) => {
    const q = document.getElementById("queue")?.textContent || "";
    const c = (document.querySelector("#count b")?.textContent || "");
    return /All shots saved/.test(q) && (left === undefined || c === String(left).padStart(2, "0"));
  }, left, { timeout: 30000 });
}

(async () => {
  console.log(`Seeding dev film ${CODE} (3 shots each)…`);
  convex("webJoinDev:seedFilm", { code: CODE, title: "Web Join E2E", shotsPerPerson: 3, revealInMinutes: 90 });
  execSync(`node ${JSON.stringify(path.join(path.dirname(new URL(import.meta.url).pathname), "csp-hash.mjs"))} --check`, { stdio: "inherit" });

  const browser = await chromium.launch({ args: ["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"] });
  const phone = { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true };

  // ---- Guest A: live viewfinder (fake camera) -------------------------------
  const ctxA = await browser.newContext({ ...phone, permissions: ["camera"] });
  const a = await ctxA.newPage();
  watch(a, "A");
  await a.goto(URL_);
  await a.getByRole("button", { name: /Join in your browser/ }).waitFor();
  ok(await a.getByRole("link", { name: "Open in the app" }).isVisible(), "invite shows 'Open in the app'");
  ok(await a.getByRole("link", { name: "Get the iPhone app" }).isVisible(), "invite shows 'Get the iPhone app'");
  await shot(a, "01-invite");
  await a.getByRole("button", { name: /Join in your browser/ }).click();
  ok(await a.getByRole("dialog").getByRole("link", { name: "Terms" }).isVisible() && await a.getByRole("dialog").getByRole("link", { name: "Privacy Policy" }).isVisible(), "join sheet links Terms + Privacy");
  await a.getByRole("dialog").getByRole("button", { name: "Join", exact: true }).click();
  ok(/Type your name/.test(await a.locator(".err").innerText()), "empty name is refused");
  await a.getByLabel("Your name").fill("Ana E2E");
  await shot(a, "02-name");
  await a.getByRole("dialog").getByRole("button", { name: "Join", exact: true }).click();
  await a.locator("#shutter").waitFor();
  ok(/03 shots left/.test(await countText(a)), `counter starts at 3 (${await countText(a)})`);
  ok(/Add to calendar/.test(await a.locator(".develop").innerText()), "reveal countdown + Add to calendar shown");
  const ics = await a.locator("a.cal").getAttribute("href");
  ok(ics.startsWith("data:text/calendar") && decodeURIComponent(ics).includes("BEGIN:VEVENT"), "calendar link is a valid .ics");
  await a.waitForFunction(() => { const v = document.getElementById("video"); return v && v.videoWidth > 0; }, null, { timeout: 15000 });
  ok(true, "live viewfinder streaming (fake camera)");
  await shot(a, "03-camera");
  await a.locator("#shutter").click();
  await waitSaved(a, 2);
  ok(/02 shots left/.test(await countText(a)), `one shot uploaded (${await countText(a)})`);

  // Privacy before the reveal: status has no URLs, album refused, no photo <img> on the page.
  const priv = await a.evaluate(async (code) => {
    const s = JSON.parse(localStorage.getItem(`filmsera.webjoin.dev.${code}`));
    const h = { Authorization: `Bearer ${s.token}`, "Content-Type": "application/json" };
    const site = "https://resilient-goat-339.convex.site";
    const st = await (await fetch(`${site}/web/status`, { method: "POST", headers: h, body: "{}" })).json();
    const al = await fetch(`${site}/web/album`, { method: "POST", headers: h, body: "{}" });
    return { st, albumStatus: al.status, imgs: document.querySelectorAll("main img").length };
  }, CODE);
  ok(priv.st.ok && priv.st.shotsUsed === 1 && !/https?:\/\//.test(JSON.stringify(priv.st)), "status: shots used, no URLs");
  ok(priv.albumStatus === 403, "album refused before reveal (403)");
  ok(priv.imgs === 0, "camera view shows no photos");

  // Reload resumes as the same guest.
  await a.reload();
  await a.locator("#shutter").waitFor();
  ok(/ana e2e/i.test(await a.locator(".g-top .chip").innerText()) && /02 shots left/.test(await countText(a)), "reload resumes same guest + count");

  // Offline shot: saved to IndexedDB, uploads when back online.
  await a.waitForFunction(() => { const v = document.getElementById("video"); return v && v.videoWidth > 0; }, null, { timeout: 15000 });
  await ctxA.setOffline(true);
  await a.locator("#shutter").click();
  await a.waitForFunction(() => /saved on this phone/.test(document.getElementById("queue")?.textContent || ""), null, { timeout: 20000 });
  const idb = await a.evaluate(() => new Promise(res => { const r = indexedDB.open("filmsera-webjoin", 1); r.onsuccess = () => { const q = r.result.transaction("pending").objectStore("pending").count(); q.onsuccess = () => res(q.result); }; }));
  ok(idb === 1, `offline shot persisted in IndexedDB (${idb})`);
  ok(/01 shots? left/.test(await countText(a)), `offline shot still counts (${await countText(a)})`);
  await shot(a, "04-offline");
  await ctxA.setOffline(false);
  await waitSaved(a, 1);
  ok(true, "offline shot uploaded after reconnect");

  // Last shot → roll finished.
  await a.locator("#shutter").click();
  await waitSaved(a, 0);
  ok(await a.locator("#shutter").isDisabled(), "shutter disabled after 3 shots");
  ok(/That's your roll/.test(await a.locator("#vfmsg").innerText()), "roll-finished message");
  await shot(a, "05-roll-done");

  // ---- Guest B: no camera permission → file input fallback ------------------
  const ctxB = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  await ctxB.addInitScript(() => {
    if (navigator.mediaDevices) navigator.mediaDevices.getUserMedia = () => Promise.reject(new DOMException("denied", "NotAllowedError"));
  });
  const b = await ctxB.newPage();
  watch(b, "B");
  // A 3000×2000 JPEG made in the browser, to check the 2560px resize.
  const jpeg = await b.evaluate(async () => {
    const c = document.createElement("canvas"); c.width = 3000; c.height = 2000;
    const x = c.getContext("2d"); const g = x.createLinearGradient(0, 0, 3000, 2000);
    g.addColorStop(0, "#c84"); g.addColorStop(1, "#348"); x.fillStyle = g; x.fillRect(0, 0, 3000, 2000);
    x.fillStyle = "#fff"; x.font = "200px sans-serif"; x.fillText("Guest B", 200, 1000);
    return c.toDataURL("image/jpeg", 0.9).split(",")[1];
  });
  const jpegPath = path.join(OUT, "guest-b.jpg");
  writeFileSync(jpegPath, Buffer.from(jpeg, "base64"));
  await b.goto(URL_);
  await b.getByRole("button", { name: /Join in your browser/ }).first().click();
  await b.getByLabel("Your name").fill("Ana E2E"); // same name → server makes it unique
  await b.getByRole("dialog").getByRole("button", { name: "Join", exact: true }).click();
  await b.locator("#shutter").waitFor();
  await b.waitForFunction(() => /Camera access is off/.test(document.getElementById("vfmsg")?.textContent || ""), null, { timeout: 10000 });
  ok(true, "denied camera → file-input fallback message");
  ok(/ana e2e 2/i.test(await b.locator(".g-top .chip").innerText()), "duplicate name made unique (Ana E2E 2)");
  const [chooser] = await Promise.all([b.waitForEvent("filechooser"), b.locator("#shutter").click()]);
  await chooser.setFiles(jpegPath);
  await waitSaved(b, 2);
  ok(/02 shots left/.test(await countText(b)), "fallback shot uploaded");
  await shot(b, "06-fallback-desktop");

  // ---- Fix round 1 checks on a second film (so the album counts above stay put) ----
  const CODE2 = `${CODE}2`;
  const seeded2 = JSON.parse(convex("webJoinDev:seedFilm", { code: CODE2, title: "Round 1", shotsPerPerson: 3, revealInMinutes: 90 }));
  const URL2 = `${BASE}/join.html?code=${CODE2}&backend=dev`;
  const ctxC = await browser.newContext({ ...phone, permissions: ["camera"] });
  const c = await ctxC.newPage(); watch(c, "C");
  await c.goto(URL2);
  // F10: tap targets on the invite.
  await c.getByRole("button", { name: /Join in your browser/ }).waitFor();
  const small = await c.evaluate(() => [...document.querySelectorAll(".copy, .btn2, .footer a, .wordmark, [data-webjoin]")]
    .filter(el => el.offsetParent).map(el => [el.textContent.trim().slice(0, 20), Math.round(el.getBoundingClientRect().height)]).filter(([, h]) => h < 44));
  ok(small.length === 0, `invite tap targets ≥ 44 px ${small.length ? JSON.stringify(small) : ""}`);
  // F11: focus trap + return in the name sheet.
  await c.getByRole("button", { name: /Join in your browser/ }).focus();
  await c.keyboard.press("Enter");
  await c.getByLabel("Your name").waitFor();
  let inside = true;
  for (let i = 0; i < 8; i++) { await c.keyboard.press("Tab"); inside &&= await c.evaluate(() => !!document.activeElement.closest(".modal")); }
  ok(inside, "Tab stays inside the name sheet");
  ok(await c.evaluate(() => [...document.querySelectorAll(".modal .linkbtn")].every(el => el.getBoundingClientRect().height >= 44)), "'Not now' ≥ 44 px");
  await c.keyboard.press("Escape");
  ok(await c.evaluate(() => document.activeElement && document.activeElement.hasAttribute("data-webjoin")), "Esc returns focus to 'Join in your browser'");
  await c.getByRole("button", { name: /Join in your browser/ }).click();
  await c.getByLabel("Your name").fill("Cleo");
  await c.getByRole("dialog").getByRole("button", { name: "Join", exact: true }).click();
  await c.locator("#shutter").waitFor();
  await c.waitForFunction(() => { const v = document.getElementById("video"); return v && v.videoWidth > 0; }, null, { timeout: 15000 });
  // F9: .ics lines folded at 75 octets.
  const icsText = decodeURIComponent((await c.locator("a.cal").getAttribute("href")).split(",").slice(1).join(","));
  ok(icsText.split("\r\n").every(l => Buffer.byteLength(l) <= 75) && /\r\n /.test(icsText), ".ics lines folded at 75 octets");
  ok((await c.locator("a.cal").boundingBox()).height >= 44, "'Add to calendar' ≥ 44 px");
  // F4: commit reaches the server but its response is lost → retry says committed, no false toast.
  let dropped = false;
  await c.route("**/web/commit", async route => {
    if (dropped) return route.continue();
    dropped = true; await route.fetch(); await route.abort("connectionreset");
  });
  await c.locator("#shutter").click();
  await waitSaved(c, 2);
  ok(dropped, "a commit response was dropped");
  ok(!(await toastTexts(c)).some(t => /wasn't saved/.test(t)), "lost commit response: no 'wasn't saved' toast, counted once (02 left)");
  await c.unroute("**/web/commit");
  // F2: an upload that never answers is aborted and retried; the shot still saves.
  let held = 0;
  await c.route("**/web/upload?*", route => { if (held++ === 0) return; /* never answer the first upload */ route.continue(); });
  const t0 = Date.now();
  await c.locator("#shutter").click();
  await c.waitForFunction(() => /Saving 1 shot/.test(document.getElementById("queue")?.textContent || ""), null, { timeout: 10000 });
  await waitSaved(c, 1).catch(() => {});
  await c.waitForFunction(() => (document.querySelector("#count b")?.textContent || "") === "01" && /All shots saved/.test(document.getElementById("queue")?.textContent || ""), null, { timeout: 90000 });
  ok(held >= 2, `hung upload timed out and was retried (${Math.round((Date.now() - t0) / 1000)} s)`);
  await c.unroute("**/web/upload?*");

  // F3 + F5: a browser that can't store shots (IndexedDB put fails), offline; and a HEIC pick.
  const ctxD = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  await ctxD.addInitScript(() => {
    IDBObjectStore.prototype.put = function () { throw new DOMException("no blobs here", "DataError"); };
    if (navigator.mediaDevices) navigator.mediaDevices.getUserMedia = () => Promise.reject(new DOMException("denied", "NotAllowedError"));
  });
  const d = await ctxD.newPage(); watch(d, "D");
  await d.goto(URL2);
  await d.getByRole("button", { name: /Join in your browser/ }).first().click();
  await d.getByLabel("Your name").fill("Dana");
  await d.getByRole("dialog").getByRole("button", { name: "Join", exact: true }).click();
  await d.locator("#shutter").waitFor();
  const heicPath = path.join(OUT, "pick.heic");
  execSync(`sips -s format heic ${JSON.stringify(path.join(OUT, "guest-b.jpg"))} --out ${JSON.stringify(heicPath)}`, { stdio: "ignore" });
  let [chooser2] = await Promise.all([d.waitForEvent("filechooser"), d.locator("#shutter").click()]);
  await chooser2.setFiles(heicPath);
  await d.waitForFunction(() => /HEIC/.test([...document.querySelectorAll(".toast")].map(t => t.textContent).join(" ")), null, { timeout: 10000 });
  ok(true, "HEIC that this browser can't decode → accurate HEIC message");
  await ctxD.setOffline(true);
  [chooser2] = await Promise.all([d.waitForEvent("filechooser"), d.locator("#shutter").click()]);
  await chooser2.setFiles(path.join(OUT, "guest-b.jpg"));
  await d.waitForFunction(() => /Keep this page open/i.test(document.getElementById("queue")?.textContent || ""), null, { timeout: 20000 });
  ok(!/saved on this phone/.test(await d.locator("#queue").innerText()), "no IndexedDB → honest 'keep this page open', never 'saved on this phone'");
  await ctxD.setOffline(false);
  await waitSaved(d, 2);
  ok(true, "memory-only shot uploads once back online");

  // F8: a host-only film doesn't offer browser join.
  convex("webJoinDev:seedFilm", { code: `${CODE}H`, title: "Private", hostOnly: true });
  const e = await ctxD.newPage(); watch(e, "E");
  await e.goto(`${BASE}/join.html?code=${CODE}H&backend=dev`);
  await e.locator(".cta").first().waitFor();
  ok(await e.getByRole("button", { name: /Join in your browser/ }).count() === 0 && /private/i.test(await e.locator(".sheet .fine").first().innerText()),
    "hostOnly film: no 'Join in your browser', explains why");

  // M2: the host removes guest D (via the app API) → D's page says so and stops offering web join.
  const guests = JSON.parse(convex("webJoin:listWebGuests", { filmClientId: seeded2.clientId }, seeded2.hostIdentity));
  const dana = guests.find(g => g.name === "Dana");
  ok(guests.length === 2 && dana && dana.shots === 1, `host lists web guests (${guests.map(g => `${g.name}:${g.shots}`).join(", ")})`);
  const removed = JSON.parse(convex("webJoin:removeWebGuest", { filmClientId: seeded2.clientId, memberClientId: dana.memberClientId, deletePhotos: true }, seeded2.hostIdentity));
  ok(removed.removed && removed.photosDeleted === 1, "host removed Dana and her photo");
  await d.reload();
  await d.locator(".cta").first().waitFor();
  ok(await d.getByRole("button", { name: /Join in your browser/ }).count() === 0 && /removed you/i.test(await d.locator("body").innerText()),
    "removed guest: session ended, told why, no browser join offered");

  ok(cspViolations.length === 0, `no CSP violations ${cspViolations.slice(0, 3).join(" | ")}`);

  // ---- Reveal (dev helper) → album --------------------------------------------
  convex("webJoinDev:revealFilm", { code: CODE });
  await a.reload();
  await a.locator("#grid button").first().waitFor({ timeout: 20000 });
  const n = await a.locator("#grid button").count();
  ok(n === 4, `album shows all 4 photos (${n})`);
  const names = await a.locator("#grid .by").allInnerTexts();
  ok(names.filter(x => x === "Ana E2E").length === 3 && names.includes("Ana E2E 2"), `author names shown (${names.join(", ")})`);
  await a.waitForFunction(() => [...document.querySelectorAll("#grid img")].every(i => i.complete && i.naturalWidth > 0), null, { timeout: 20000 });
  ok(true, "thumbnails load");
  await shot(a, "07-album");
  await a.locator("#grid button").first().click();
  await a.waitForFunction(() => { const i = document.querySelector(".lb-stage img"); return i && i.complete && i.naturalWidth > 0; }, null, { timeout: 20000 });
  ok(await a.getByRole("button", { name: /Save photo/ }).isVisible(), "full-size viewer with Save button");
  ok(await a.evaluate(() => !!document.activeElement.closest(".lightbox")), "lightbox takes focus");
  await shot(a, "08-lightbox");

  // Desktop guest B: its 3000px upload was resized to 2560 and the thumb to 480.
  await b.reload();
  await b.locator("#grid button").first().waitFor({ timeout: 20000 });
  const dims = await b.evaluate(async () => {
    const s = JSON.parse(localStorage.getItem(Object.keys(localStorage).find(k => k.startsWith("filmsera.webjoin.dev."))));
    const r = await fetch("https://resilient-goat-339.convex.site/web/album", { method: "POST", headers: { Authorization: `Bearer ${s.token}`, "Content-Type": "application/json" }, body: "{}" });
    const p = (await r.json()).page.find(p => p.mine);
    const load = u => new Promise(res => { const i = new Image(); i.onload = () => res([i.naturalWidth, i.naturalHeight]); i.src = u; });
    return { full: await load(p.imageUrl), thumb: await load(p.thumbUrl) };
  });
  ok(Math.max(...dims.full) === 2560 && Math.max(...dims.thumb) === 480, `resize: full ${dims.full.join("×")}, thumb ${dims.thumb.join("×")}`);
  await shot(b, "09-album-desktop");

  ok(cspViolations.length === 0, `still no CSP violations after the album ${cspViolations.slice(0, 3).join(" | ")}`);
  await browser.close();
  console.log(failures ? `\n${failures} FAILED` : "\nALL PASSED");
  console.log(`Screenshots: ${OUT}`);
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
