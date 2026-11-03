"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ReactNode } from "react";
import { FAQ_ITEMS } from "../lib/faq";

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
  const items = FAQ_ITEMS;
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

