// Screenshots of every web-join screen (iPhone 15 + desktop) against the DEV
// Convex deployment, with a fake camera. Used to compare the browser camera
// with the app's FilmCameraView.
//
//   python3 -m http.server 8787        (repo root)
//   PLAYWRIGHT_DIR=/tmp/webjoin-e2e FAKE_VIDEO=/tmp/webjoin-ui-shots/fake.mjpeg \
//     OUT=docs/webjoin-ui node scripts/webjoin-ui-shots.mjs
// FAKE_VIDEO (optional): an .mjpeg/.y4m Chromium plays as the camera.
// Env: CODE (default WEBUI), CONVEX_DIR (default ~/Camera-webjoin), BASE, PICK (a JPEG for the file-picker guest).

import { createRequire } from "node:module";
import { execSync } from "node:child_process";
import { mkdirSync } from "node:fs";
import os from "node:os";
import path from "node:path";

const require = createRequire(path.join(process.env.PLAYWRIGHT_DIR || process.cwd(), "noop.js"));
const { chromium } = require("playwright");

const CODE = process.env.CODE || "WEBUI";
const CONVEX_DIR = process.env.CONVEX_DIR || path.join(os.homedir(), "Camera-webjoin");
const BASE = process.env.BASE || "http://localhost:8787";
const URL_ = `${BASE}/join.html?code=${CODE}&backend=dev`;
const OUT = process.env.OUT || "/tmp/webjoin-ui-shots";
const PICK = process.env.PICK || path.join(os.homedir(), "Camera/Camera/Resources/Sample/sample03.jpg");
mkdirSync(OUT, { recursive: true });

const convex = (fn, args) => execSync(`npx convex run ${fn} '${JSON.stringify(args)}'`, { cwd: CONVEX_DIR, stdio: ["ignore", "pipe", "pipe"] }).toString();
const snap = (page, name, full = false) => page.screenshot({ path: path.join(OUT, `${name}.png`), fullPage: full }).then(() => console.log(`  ${name}.png`));
const pause = ms => new Promise(r => setTimeout(r, ms));
async function waitSaved(page, left) {
  await page.waitForFunction(left => /All shots saved/.test(document.getElementById("queue")?.textContent || "")
    && (document.querySelector("#count b")?.textContent || "") === String(left).padStart(2, "0"), left, { timeout: 60000 });
}
async function join(page, name) {
  await page.goto(URL_);
  await page.getByRole("button", { name: /Join in your browser/ }).first().click();
  await page.getByLabel("Your name").fill(name);
  await page.getByRole("dialog").getByRole("button", { name: "Join", exact: true }).click();
  await page.locator("#shutter").waitFor();
}
const streaming = page => page.waitForFunction(() => { const v = document.getElementById("video"); return v && v.videoWidth > 0; }, null, { timeout: 20000 });

(async () => {
  convex("webJoinDev:seedFilm", { code: CODE, title: "Saturday Rolls", shotsPerPerson: 3, revealInMinutes: 150 });
  const args = ["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream", "--enable-unsafe-swiftshader"];
  if (process.env.FAKE_VIDEO) args.push(`--use-file-for-fake-video-capture=${process.env.FAKE_VIDEO}`);
  const browser = await chromium.launch({ args });
  const iphone = { viewport: { width: 393, height: 852 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true };

  // Guest A on an iPhone-sized screen.
  const ctxA = await browser.newContext({ ...iphone, permissions: ["camera"] });
  const a = await ctxA.newPage();
  a.on("pageerror", e => console.log("pageerror:", e.message));
  await a.goto(URL_);
  await a.getByRole("button", { name: /Join in your browser/ }).waitFor();
  await pause(1200);
  await snap(a, "01-invite-phone");
  await a.getByRole("button", { name: /Join in your browser/ }).click();
  await a.getByLabel("Your name").fill("Maya");
  await pause(500);
  await snap(a, "02-name-sheet-phone");
  await a.getByRole("dialog").getByRole("button", { name: "Join", exact: true }).click();
  await a.locator("#shutter").waitFor();
  await streaming(a);
  await pause(1500);
  console.log("  viewfinder WebGL:", await a.evaluate(() => document.getElementById("vf").classList.contains("gl")));
  await snap(a, "03-camera-phone");
  await a.locator("#qrbtn").click();
  await pause(600);
  await snap(a, "04-invite-qr-sheet-phone");
  await a.keyboard.press("Escape");
  await a.locator("#shutter").click();
  await pause(60);
  await snap(a, "05-shutter-blink-phone");
  await waitSaved(a, 2);
  await pause(300);
  await snap(a, "06-after-shot-phone");
  await ctxA.setOffline(true);
  await a.locator("#shutter").click();
  await a.waitForFunction(() => /saved on this phone/.test(document.getElementById("queue")?.textContent || ""), null, { timeout: 20000 });
  await pause(300);
  await snap(a, "07-offline-phone");
  await ctxA.setOffline(false);
  await waitSaved(a, 1);
  await a.locator("#shutter").click();
  await waitSaved(a, 0);
  await pause(400);
  await snap(a, "08-roll-done-phone");
  await a.locator("#details").scrollIntoViewIfNeeded();
  await pause(400);
  await snap(a, "09-come-back-at-reveal-phone");

  // Guest B: camera blocked → file-picker fallback.
  const ctxB = await browser.newContext({ ...iphone });
  await ctxB.addInitScript(() => { if (navigator.mediaDevices) navigator.mediaDevices.getUserMedia = () => Promise.reject(new DOMException("denied", "NotAllowedError")); });
  const b = await ctxB.newPage();
  await join(b, "Leo");
  await b.waitForFunction(() => /Camera access is off/.test(document.getElementById("vfmsg")?.textContent || ""));
  await pause(400);
  await snap(b, "10-camera-blocked-phone");
  const [chooser] = await Promise.all([b.waitForEvent("filechooser"), b.locator("#shutter").click()]);
  await chooser.setFiles(PICK);
  await waitSaved(b, 2);

  // Guest C on a desktop browser.
  const ctxC = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, permissions: ["camera"] });
  const c = await ctxC.newPage();
  await join(c, "Ines");
  await streaming(c);
  await pause(1500);
  await snap(c, "11-camera-desktop");
  await c.locator("#shutter").click();
  await waitSaved(c, 2);

  // Reveal → album + viewer.
  convex("webJoinDev:revealFilm", { code: CODE });
  await a.reload();
  await a.locator("#grid button").first().waitFor({ timeout: 20000 });
  await a.waitForFunction(() => [...document.querySelectorAll("#grid img")].every(i => i.complete && i.naturalWidth > 0), null, { timeout: 20000 });
  await pause(900);
  await snap(a, "12-album-phone", true);
  await a.locator("#grid button").first().click();
  await a.waitForFunction(() => { const i = document.querySelector(".lb-stage img"); return i && i.complete && i.naturalWidth > 0; }, null, { timeout: 20000 });
  await pause(500);
  await snap(a, "13-lightbox-phone");
  await c.reload();
  await c.locator("#grid button").first().waitFor({ timeout: 20000 });
  await c.waitForFunction(() => [...document.querySelectorAll("#grid img")].every(i => i.complete && i.naturalWidth > 0), null, { timeout: 20000 });
  await pause(900);
  await snap(c, "14-album-desktop");
  await browser.close();
  console.log(`Screenshots: ${OUT}`);
})().catch(e => { console.error(e); process.exit(1); });
