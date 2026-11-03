// Recompute the CSP hash for join.html's inline script and write it into the
// page's Content-Security-Policy meta tag. Run after editing that script:
//   node scripts/csp-hash.mjs           (updates join.html)
//   node scripts/csp-hash.mjs --check   (exit 1 if the hash is stale)
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const file = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "join.html");
const html = readFileSync(file, "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
if (scripts.length !== 1) throw new Error(`expected exactly 1 inline <script>, found ${scripts.length}`);
const hash = `sha256-${createHash("sha256").update(scripts[0], "utf8").digest("base64")}`;
const re = /'sha256-[A-Za-z0-9+/=]+'|'sha256-PLACEHOLDER'/;
const current = html.match(re)?.[0];
if (!current) throw new Error("no sha256 source in the CSP meta tag");
if (process.argv.includes("--check")) {
  if (current !== `'${hash}'`) { console.error(`stale CSP hash: ${current} != '${hash}'`); process.exit(1); }
  console.log("CSP hash OK");
} else {
  writeFileSync(file, html.replace(re, `'${hash}'`));
  console.log(`CSP hash set: ${hash}`);
}
