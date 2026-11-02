# filmsera-invite Worker

Gives every shared invite link (`getfilmsera.cam/join/<code>`) a rich preview:
its own title ("Biswas invited you to “Saturday Rolls”"), description, and a
1200×630 share card with the cover photo. Also injects the film into
`join.html` so the invitation renders instantly.

- Routes: `getfilmsera.cam/join*`, `getfilmsera.cam/card/*` (zone getfilmsera.cam).
- Cards are drawn by the app repo's Convex `/invite-card` HTTP route
  (`convex/inviteCard.ts`) and cached here at the edge for a day; the card URL
  carries a content hash, so edits get a fresh card.
- Lookups try production Convex first, then dev.
- A Cloudflare redirect rule still sends `/join/<code>` → `/join.html?code=<code>`;
  the Worker handles both.

Deploy (token: Workers Scripts + Routes on getfilmsera.cam, kept at
`~/.config/filmsera/cf-token`):

```sh
cd worker
CLOUDFLARE_API_TOKEN="$(cat ~/.config/filmsera/cf-token)" npx wrangler@4 deploy
```

If the Worker is removed, `join.html` still works alone: it looks the code up
in the browser.
