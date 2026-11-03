import type { Metadata } from "next";
import { APP_ID, SITE_URL } from "../lib/site";
import { FAQ_ITEMS } from "../lib/faq";
import "./globals.css";

const TITLE = "Disposable Camera App for Weddings & Parties | Filmsera";
const DESCRIPTION =
  "A shared disposable camera for your wedding or party. Guests join by QR code, shoot on their iPhones, and every photo stays hidden until the reveal.";

export const metadata: Metadata = {
  title: TITLE,
  description: DESCRIPTION,
  metadataBase: new URL(SITE_URL),
  alternates: {
    canonical: "/",
    types: { "text/plain": "/llms.txt" },
  },
  openGraph: {
    title: TITLE,
    description: DESCRIPTION,
    url: `${SITE_URL}/`,
    siteName: "Filmsera",
    type: "website",
    images: [`${SITE_URL}/shots/filmsera-social.png`],
  },
  twitter: {
    card: "summary_large_image",
    title: TITLE,
    description: DESCRIPTION,
    images: [`${SITE_URL}/shots/filmsera-social.png`],
  },
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/favicon.svg", type: "image/svg+xml" },
      { url: "/favicon-16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: "/apple-touch-icon.png",
  },
  other: {
    "apple-itunes-app": `app-id=${APP_ID}, app-argument=${SITE_URL}/open/create`,
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  // Entity graph for the whole site. Other pages reference these @ids.
  // Never add aggregateRating until the page shows a meaningful App Store rating count.
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": `${SITE_URL}/#org`,
        name: "Filmsera",
        url: `${SITE_URL}/`,
        logo: `${SITE_URL}/favicon-512.png`,
        email: "support@getfilmsera.cam",
        sameAs: [`https://apps.apple.com/app/id${APP_ID}`],
      },
      {
        "@type": "WebSite",
        "@id": `${SITE_URL}/#website`,
        name: "Filmsera",
        url: `${SITE_URL}/`,
        publisher: { "@id": `${SITE_URL}/#org` },
      },
      {
        "@type": "MobileApplication",
        "@id": `${SITE_URL}/#app`,
        name: "Filmsera",
        operatingSystem: "iOS 17 or later",
        applicationCategory: "MultimediaApplication",
        url: `${SITE_URL}/`,
        installUrl: `https://apps.apple.com/app/id${APP_ID}`,
        publisher: { "@id": `${SITE_URL}/#org` },
        description:
          "A shared disposable camera app for weddings and parties, with 25 live film looks.",
        offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
      },
      {
        "@type": "FAQPage",
        "@id": `${SITE_URL}/#faq`,
        mainEntity: FAQ_ITEMS.map((item) => ({
          "@type": "Question",
          name: item.q,
          acceptedAnswer: { "@type": "Answer", text: item.a },
        })),
      },
    ],
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
