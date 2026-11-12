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
    a: "A shared disposable camera app for iPhone. A host creates a film for an event on iPhone, guests join by QR code, link or short code from any phone (in the app or the browser), and everyone shoots into the same roll. The photos stay hidden until the reveal, then the whole roll appears at once.",
  },
  {
    q: "Can I see photos before they develop?",
    a: "No. Photos stay hidden while everyone shoots. When the reveal time arrives, the whole film appears at once. The host can reveal early if the group can't wait.",
  },
  {
    q: "Do guests need to download the app?",
    a: "No. Guests can join right in their phone's browser, iPhone or Android, with no app and no account: they type a name and shoot photos. With the free Filmsera app on iPhone they also get the live film looks, plus video clips on Celebration and Wedding films. Guests never pay.",
  },
  {
    q: "Does Filmsera work on Android?",
    a: "Yes, for guests. Android guests join and shoot photos in their phone's browser, with no app or account. Hosting a film and the live film looks need the Filmsera app on iPhone (iOS 17 or later).",
  },
  {
    q: "How many guests can join a film?",
    a: "A free film holds up to 10 guests, or 20 if the host has Film Pro. For more, the host buys a one-time pass for that film: Party ($7.99, up to 30 guests), Celebration ($24.99, up to 100) or Wedding ($49.99, up to 250). Guests join from the iPhone app or from any phone's browser.",
  },
  {
    q: "What's free, and what's Film Pro?",
    a: "The core camera and shared films for up to 10 guests are free, and guests never pay. Film Pro unlocks all 25 cameras, premium look packs and every recap style, and your free films hold 20 guests: $1.99/week, $5.99/month or $34.99/year, with a 3-day free trial on the weekly plan. For a bigger event, buy a one-time pass for that film: Party $7.99 (30 guests), Celebration $24.99 (100) or Wedding $49.99 (250). Every pass adds an HD, watermark-free recap and keeps the photos for 1 year.",
  },
];
