"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ReactNode } from "react";

/** Parable-inspired scroll reveal — respects prefers-reduced-motion */
export function Reveal({
  children,
  className = "",
  delay = 0,
}: {
  children: ReactNode;
  className?: string;
  delay?: number;
}) {
  const reduce = useReducedMotion();
  if (reduce) return <div className={className}>{children}</div>;
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.15 }}
      transition={{ duration: 0.55, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  );
}

/** Parable-style FAQ accordion */
export function FaqAccordion() {
  const items = [
    {
      q: "What exactly is Filmsera?",
      a: "A group film camera for iPhone. Shoot Shots through 25 Looks, host a shared Film your Guests join, and open every Frame together at Reveal.",
    },
    {
      q: "Can I see photos before they develop?",
      a: "No — Frames stay hidden while you shoot. When Reveal hits, the entire Film appears at once. You can Reveal early if you can't wait.",
    },
    {
      q: "Do guests need to download the app?",
      a: "Yes. Guests need Filmsera on iPhone to join and shoot. A QR or join link opens the app (or the App Store if they don't have it yet).",
    },
    {
      q: "What's free, and what's Film Pro?",
      a: "The core camera, shared Films, and Guests are free. Film Pro unlocks all 25 cameras, premium Look packs, and every Recap style — $1.99/week, $5.99/month, or $34.99/year, with a 3-day free trial on the weekly plan. Prefer a one-off? Event Pass is $7.99 once for an HD, watermark-free Recap of a single Film.",
    },
  ];
  return (
    <div className="mx-auto max-w-[760px]">
      {items.map((item) => (
        <details key={item.q} className="group border-b border-hair py-1">
          <summary className="cursor-pointer list-none py-5 text-left text-[17px] font-semibold text-cream marker:content-none">
            <span className="flex items-center justify-between gap-4">
              {item.q}
              <span className="text-brass transition group-open:rotate-45">+</span>
            </span>
          </summary>
          <p className="pb-5 text-[15px] leading-relaxed text-muted">{item.a}</p>
        </details>
      ))}
    </div>
  );
}

