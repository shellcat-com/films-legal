// Filmsera invite Worker.
//
//   /join/<code>, /join.html?code=<code>
//       The static join.html from GitHub Pages, with the film's own <title>,
//       description and og:/twitter: tags written in, and window.__INVITE__
//       injected so the page paints without its own lookup. Link previews
//       (iMessage, WhatsApp, Instagram, Slack…) read these tags.
//   /card/<code>.jpg
//       The 1200×630 share card, drawn by the Convex `/invite-card` route and
//       cached here at the edge.
//
// Anything unexpected falls through to the static page, which still works on
// its own. Workers Free CPU limits are fine: this only fetches and rewrites.

const BACKENDS = [
  // Production first; films made by debug builds live on the dev deployment.
  // `name` is passed to the page so its browser join talks to the same deployment.
  { name: "prod", cloud: "https://elated-gopher-868.convex.cloud", site: "https://elated-gopher-868.convex.site" },
  { name: "dev", cloud: "https://resilient-goat-339.convex.cloud", site: "https://resilient-goat-339.convex.site" },
];
const SITE = "https://getfilmsera.cam";
const FALLBACK_CARD = `${SITE}/shots/filmsera-social.png`;
const PAGE_TTL = 60;          // seconds — member counts stay fresh
const CARD_TTL = 60 * 60 * 24; // the card URL is versioned, so long is safe

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (request.method !== "GET" && request.method !== "HEAD") return fetch(request);
    try {
      if (url.pathname.startsWith("/card/")) return await card(request, url, ctx);
      const code = readCode(url);
      if (code) return await page(request, url, code, ctx);
    } catch (err) {
      console.error("invite worker", err && err.stack || err);
    }
    return fetch(request);
  },
};

function cleanCode(raw) {
  return String(raw || "").toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 16);
}

function readCode(url) {
  const m = url.pathname.match(/^\/join\/([A-Za-z0-9]{4,16})\/?$/);
  if (m) return cleanCode(m[1]);
  if (url.pathname === "/join.html" || url.pathname === "/join") return cleanCode(url.searchParams.get("code"));
  return "";
}

async function lookup(code) {
  for (const b of BACKENDS) {
    const res = await fetch(`${b.cloud}/api/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: "films:getByInviteCode", args: { inviteCode: code }, format: "json" }),
    });
    if (!res.ok) throw new Error(`lookup ${res.status}`);
    const j = await res.json();
    if (j.status !== "success") throw new Error(`lookup ${j.status}`);
    if (j.value) return { film: j.value, backend: b };
  }
  return { film: null, backend: null };
}

// Short stable hash so a changed title/cover/date gets a fresh card URL —
// chat apps cache previews by image URL.
async function version(film) {
  const key = [film.title, film.hostName, film.coverUrl && film.coverUrl.split("?")[0], film.revealAt, film.status, film.shotsPerPerson].join("|");
  const digest = await crypto.subtle.digest("SHA-1", new TextEncoder().encode(key));
  return [...new Uint8Array(digest)].slice(0, 5).map(b => b.toString(16).padStart(2, "0")).join("");
}

function firstName(name) {
  return String(name || "").trim().split(/\s+/)[0] || "";
}

function describe(film, tz) {
  const parts = [];
  if (film.shotsPerPerson) parts.push(`${Math.round(film.shotsPerPerson)} shots each`);
  const revealed = film.status === "revealed" || (film.revealAt && film.revealAt <= Date.now());
  if (revealed) parts.push("Developed");
  else if (film.revealAt) {
    let when;
    try { when = new Intl.DateTimeFormat("en-US", { weekday: "short", month: "short", day: "numeric", hour: "numeric", minute: "2-digit", timeZone: tz }).format(film.revealAt); }
    catch { when = new Intl.DateTimeFormat("en-US", { weekday: "short", month: "short", day: "numeric" }).format(film.revealAt); }
    parts.push(`Develops ${when}`);
  }
  const lead = parts.length ? parts.join(" · ") + ". " : "";
  return revealed
    ? `${lead}Open Filmsera to see every guest's photos.`
    : `${lead}Tap to join — everyone's photos stay hidden until the reveal.`;
}

function scriptJSON(value) {
  return JSON.stringify(value).replace(/</g, "\\u003c").replace(/>/g, "\\u003e").replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029");
}

async function page(request, url, code, ctx) {
  // iMessage builds the preview on the sender's phone, so the requester's
  // time zone is the host's — the right one for "Develops Mon 11:00 PM".
  const tz = (request.cf && request.cf.timezone) || "America/Chicago";
  const cacheKey = new Request(`${SITE}/__invite/${code}?tz=${encodeURIComponent(tz)}`);
  const cache = caches.default;
  const hit = await cache.match(cacheKey);
  if (hit) return hit;

  const [{ film, backend }, origin] = await Promise.all([
    lookup(code),
    fetch(new Request(`${SITE}/join.html`, { headers: { Accept: "text/html" } })),
  ]);
  if (!origin.ok) return fetch(request);

  const link = `${SITE}/join/${code}`;
  let title, description, image, alt;
  if (film) {
    const who = firstName(film.hostName);
    title = who ? `${who} invited you to “${film.title}”` : `You're invited to “${film.title}”`;
    description = describe(film, tz);
    image = `${SITE}/card/${code}.jpg?v=${await version(film)}&tz=${encodeURIComponent(tz)}`;
    alt = `Invitation to ${film.title} on Filmsera`;
  } else {
    title = "Filmsera invitation";
    description = "This invite code doesn't match a Film. Check the code with your host.";
    image = FALLBACK_CARD;
    alt = "Filmsera";
  }

  const set = (value) => ({ element(el) { el.setAttribute(el.tagName === "link" ? "href" : "content", value); } });
  const rewritten = new HTMLRewriter()
    .on("title", { element(el) { el.setInnerContent(film ? `${title} · Filmsera` : title); } })
    .on('link[rel="canonical"]', set(link))
    .on('meta[name="apple-itunes-app"]', set(`app-id=6781880091, app-argument=${link}`))
    .on('meta[name="description"]', set(description))
    .on('meta[property="og:title"]', set(title))
    .on('meta[property="og:description"]', set(description))
    .on('meta[property="og:url"]', set(link))
    .on('meta[property="og:image"]', set(image))
    .on('meta[property="og:image:alt"]', set(alt))
    .on('meta[name="twitter:title"]', set(title))
    .on('meta[name="twitter:description"]', set(description))
    .on('meta[name="twitter:image"]', set(image))
    .on("head", { element(el) { el.append(`<script>window.__INVITE__=${scriptJSON({ code, film, backend: backend ? backend.name : null })};</script>`, { html: true }); } })
    .transform(origin);

  const headers = new Headers(rewritten.headers);
  headers.set("Content-Type", "text/html; charset=utf-8");
  headers.set("Cache-Control", `public, max-age=${PAGE_TTL}`);
  headers.delete("ETag");
  headers.delete("Last-Modified");
  const response = new Response(rewritten.body, { status: 200, headers });
  ctx.waitUntil(cache.put(cacheKey, response.clone()));
  // Draw the card now, so it's cached by the time a chat app asks for it (a
  // cold render takes a few seconds; previews give up quickly).
  if (film) ctx.waitUntil(card(new Request(image), new URL(image), ctx).catch(() => {}));
  return response;
}

async function card(request, url, ctx) {
  const m = url.pathname.match(/^\/card\/([A-Za-z0-9]{4,16})\.jpg$/);
  if (!m) return Response.redirect(FALLBACK_CARD, 302);
  const code = cleanCode(m[1]);
  const tz = (url.searchParams.get("tz") || "").slice(0, 64);
  const cache = caches.default;
  const cacheKey = new Request(url.toString());
  const hit = await cache.match(cacheKey);
  if (hit) return hit;

  for (const b of BACKENDS) {
    const res = await fetch(`${b.site}/invite-card?code=${code}${tz ? `&tz=${encodeURIComponent(tz)}` : ""}`);
    if (res.status === 404) continue;
    if (!res.ok) break;
    const response = new Response(res.body, {
      status: 200,
      headers: {
        "Content-Type": "image/jpeg",
        "Cache-Control": `public, max-age=${CARD_TTL}, immutable`,
        "Access-Control-Allow-Origin": "*",
      },
    });
    ctx.waitUntil(cache.put(cacheKey, response.clone()));
    return response;
  }
  return Response.redirect(FALLBACK_CARD, 302);
}
