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
const convex = (fn, args) => {
  const out = execSync(`npx convex run ${fn} '${JSON.stringify(args)}'`, { cwd: CONVEX_DIR, stdio: ["ignore", "pipe", "pipe"] }).toString();
  return out;
};
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

  const browser = await chromium.launch({ args: ["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"] });
  const phone = { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true };

  // ---- Guest A: live viewfinder (fake camera) -------------------------------
  const ctxA = await browser.newContext({ ...phone, permissions: ["camera"] });
  const a = await ctxA.newPage();
  a.on("pageerror", e => { console.log("pageerror A:", e.message); failures++; });
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
  b.on("pageerror", e => { console.log("pageerror B:", e.message); failures++; });
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

  await browser.close();
  console.log(failures ? `\n${failures} FAILED` : "\nALL PASSED");
  console.log(`Screenshots: ${OUT}`);
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
