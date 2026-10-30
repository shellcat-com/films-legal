import type { Metadata } from "next";
import { APP_ID, APP_STORE_URL, SITE_URL } from "../lib/site";
import "./globals.css";

export const metadata: Metadata = {
  title: "Filmsera — Group Film Camera",
  description:
    "Filmsera is a group film camera for iPhone. Host a shared Film, invite Guests, shoot Shots through 25 Looks, and open every Frame together at Reveal.",
  metadataBase: new URL(SITE_URL),
  openGraph: {
    title: "Filmsera — Group Film Camera",
    description:
      "A group film camera. Shoot through 25 Looks. Nobody sees a Frame until Reveal.",
    url: SITE_URL,
    siteName: "Filmsera",
    type: "website",
    images: [`${SITE_URL}/shots/panel-1.png`],
  },
  twitter: {
    card: "summary_large_image",
    title: "Filmsera — Group Film Camera",
    images: [`${SITE_URL}/shots/panel-1.png`],
  },
  other: {
    "apple-itunes-app": `app-id=${APP_ID}`,
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "Filmsera",
    operatingSystem: "iOS",
    applicationCategory: "PhotoApplication",
    offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
    url: APP_STORE_URL,
  };

  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Hanken+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap"
          rel="stylesheet"
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="relative min-h-screen">{children}</body>
    </html>
  );
}
