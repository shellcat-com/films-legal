"use client";

import Link from "next/link";
import { APP_STORE_URL } from "../lib/site";

export function SiteNav() {
  return (
    <nav className="sticky top-0 z-50 border-b border-hair bg-[rgba(10,8,7,0.72)] backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-[1120px] items-center justify-between px-5">
        <Link href="/" className="font-display text-[26px] text-cream">
          <span className="mr-2 inline-block text-brass">✦</span>Filmsera
        </Link>
        <div className="flex items-center gap-6 text-sm font-semibold text-muted">
          <Link href="/#looks" className="hidden hover:text-cream sm:inline">
            Looks
          </Link>
          <Link href="/#recap" className="hidden hover:text-cream sm:inline">
            Recap
          </Link>
          <Link href="/#reveal" className="hidden hover:text-cream sm:inline">
            Reveal
          </Link>
          <Link href="/#pricing" className="hidden hover:text-cream sm:inline">
            Pricing
          </Link>
          <Link href="/looks/" className="hidden hover:text-cream md:inline">
            Look Lab
          </Link>
          <Link href="/blog/" className="hidden hover:text-cream sm:inline">
            Journal
          </Link>
          <a
            href={APP_STORE_URL}
            target="_blank"
            rel="noopener noreferrer"
            data-cta="app_store"
            className="rounded-full bg-brass px-5 py-2.5 font-bold text-brass-deep shadow-[0_12px_30px_rgba(230,180,80,0.22)]"
          >
            Download
          </a>
        </div>
      </div>
    </nav>
  );
}

export function AppStoreBadge({ className = "" }: { className?: string }) {
  return (
    <a
      href={APP_STORE_URL}
      target="_blank"
      rel="noopener noreferrer"
      data-cta="app_store"
      className={`inline-block ${className}`}
      aria-label="Download Filmsera on the App Store"
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="/shots/app-store-badge.svg"
        alt="Download on the App Store"
        width={156}
        height={52}
        className="h-[52px] w-auto"
      />
    </a>
  );
}

export function DesktopQr() {
  return (
    <div className="hidden items-center gap-3 rounded-2xl border border-hair bg-surface p-3 sm:flex">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="/shots/appstore-qr.png"
        alt="QR code to download Filmsera"
        width={88}
        height={88}
        className="rounded-lg bg-white p-1"
      />
      <div className="text-left text-sm">
        <div className="font-semibold text-cream">Scan to download</div>
        <div className="text-muted">Desktop → phone</div>
      </div>
    </div>
  );
}
