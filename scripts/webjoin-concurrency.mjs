// Web join concurrency check against the DEV deployment (never prod): N guests
// on ONE network (this machine's IP) join the same film at once and each shoot
// S photos in parallel. Pass = zero HTTP 500s; 503 "busy" is allowed (the page
// retries it) and is counted.
//   node scripts/webjoin-concurrency.mjs            (GUESTS=30 SHOTS=3 CODE=WEBCONC)
// Seeds the film with `npx convex run webJoinDev:seedFilm` in CONVEX_DIR.
import { execSync } from "node:child_process";
import os from "node:os";
import path from "node:path";

const SITE = "https://resilient-goat-339.convex.site";
const GUESTS = +(process.env.GUESTS || 30), SHOTS = +(process.env.SHOTS || 3);
const CODE = process.env.CODE || "WEBCONC";
const CONVEX_DIR = process.env.CONVEX_DIR || path.join(os.homedir(), "Camera-webjoin");
// A real 16×12 JPEG (passes the server's structural check).
const JPEG = Buffer.from("ffd8ffe000104a46494600010100000100010000ffdb00430006040506050406060506070706080a100a0a09090a140e0f0c1017141818171416161a1d251f1a1b231c1616202c20232627292a29191f2d302d283025282928ffdb0043010707070a080a130a0a13281a161a2828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828ffc0001108000c001003012200021101031101ffc4001f0000010501010101010100000000000000000102030405060708090a0bffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffc4001f0100030101010101010101010000000000000102030405060708090a0bffc400b51100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9faffda000c03010002110311003f00b9451457c71f667fffd9", "hex");

const status = {};
const count = (s) => { status[s] = (status[s] || 0) + 1; };
async function call(p, { token, body, raw } = {}) {
  for (let attempt = 0; ; attempt++) {
    const headers = {};
    if (token) headers.Authorization = `Bearer ${token}`;
    headers["Content-Type"] = raw ? "image/jpeg" : "application/json";
    const r = await fetch(p.startsWith("http") ? p : SITE + p, { method: "POST", headers, body: raw ?? JSON.stringify(body ?? {}) });
    count(r.status); if (r.status >= 500) count(`${r.status} ${p.startsWith("http") ? "/web/upload" : p}`);
    const j = await r.json().catch(() => ({}));
    if (r.status === 500 && !globalThis.__shown) { globalThis.__shown = 1; console.log("first 500 body:", JSON.stringify(j)); }
    if (r.status === 503 && attempt < 6) { await new Promise(res => setTimeout(res, 400 * (attempt + 1) + Math.random() * 400)); continue; }
    return { status: r.status, j };
  }
}

execSync(`npx convex run webJoinDev:seedFilm '${JSON.stringify({ code: CODE, title: "Concurrency", shotsPerPerson: SHOTS })}'`, { cwd: CONVEX_DIR, stdio: "ignore" });
const t0 = Date.now();
const results = await Promise.all(Array.from({ length: GUESTS }, async (_, g) => {
  const join = await call("/web/join", { body: { code: CODE, name: `Guest ${g}` } });
  if (!join.j.ok) return { g, err: `join ${join.status} ${join.j.code}` };
  const token = join.j.token;
  const shots = await Promise.all(Array.from({ length: SHOTS }, async () => {
    const id = crypto.randomUUID();
    for (let tries = 0; tries < 8; tries++) {
      const u = await call("/web/upload-url", { token, body: { photoClientId: id } });
      if (u.j.committed) return true;
      if (!u.j.ok) { await new Promise(r => setTimeout(r, 500 + Math.random() * 1000)); continue; } // shots_pending etc.
      for (const k of ["image", "thumb"]) if (!u.j[k].filled) await call(u.j[k].uploadUrl, { token, raw: JPEG });
      const c = await call("/web/commit", { token, body: { photoClientId: id, imageTicket: u.j.image.ticket, thumbTicket: u.j.thumb.ticket } });
      if (c.j.ok) return true;
    }
    return false;
  }));
  return { g, saved: shots.filter(Boolean).length };
}));
const errors = results.filter(r => r.err);
const saved = results.reduce((n, r) => n + (r.saved || 0), 0);
console.log(`${GUESTS} guests × ${SHOTS} shots from one IP in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
console.log("HTTP statuses:", JSON.stringify(status));
console.log(`joined ${GUESTS - errors.length}/${GUESTS}, photos saved ${saved}/${GUESTS * SHOTS}`, errors.length ? JSON.stringify(errors.slice(0, 5)) : "");
const ok = !status[500] && errors.length === 0 && saved === GUESTS * SHOTS;
console.log(ok ? "PASS (0 × HTTP 500)" : "FAIL");
process.exit(ok ? 0 : 1);
