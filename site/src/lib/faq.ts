/**
 * Homepage FAQ: rendered by FaqAccordion and mirrored into the FAQPage JSON-LD
 * in app/layout.tsx, so the schema always matches the visible text.
 *
 * PRICING: these answers state the live 4.1 App Store model. On the day 4.2
 * ships, switch the pricing and guest-limit answers to the 4.2 tiers.
 */
export const FAQ_ITEMS: { q: string; a: string }[] = [
  {
    q: "What exactly is Filmsera?",
    a: "A shared disposable camera app for iPhone. A host creates a film for an event, guests join by QR code, link or short code, and everyone shoots from their own phone through one of 25 film looks. The photos stay hidden until the reveal, then the whole roll appears at once.",
  },
  {
    q: "Can I see photos before they develop?",
    a: "No. Photos stay hidden while everyone shoots. When the reveal time arrives, the whole film appears at once. The host can reveal early if the group can't wait.",
  },
  {
    q: "Do guests need to download the app?",
    a: "Yes. Guests need Filmsera on an iPhone to join and shoot. A QR code or join link opens the app, or the App Store if they don't have it yet. Guests never pay.",
  },
  {
    q: "Does Filmsera work on Android?",
    a: "No. Filmsera is an iPhone app (iOS 17 or later). Android phones and web browsers can't join a Filmsera film, so check your guest list before the event.",
  },
  {
    q: "How many guests can join a film?",
    a: "In the current version there is no guest limit on a film, and hosting is free. Every guest needs an iPhone with the free Filmsera app.",
  },
  {
    q: "What's free, and what's Film Pro?",
    a: "The core camera, shared films and guests are free. Film Pro unlocks all 25 cameras, premium look packs and every recap style: $1.99/week, $5.99/month or $34.99/year, with a 3-day free trial on the weekly plan. Prefer a one-off? The Event Pass is $7.99 once for an HD, watermark-free recap of a single film.",
  },
];
