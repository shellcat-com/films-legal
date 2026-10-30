"use client";

import { motion, useReducedMotion, AnimatePresence } from "framer-motion";
import { useEffect, useState } from "react";
import { CAMERAS, FILM_STRIP, LOOKS, HOW_STEPS, type Camera } from "../lib/site";

/** Shader/Mobbin-inspired film-strip of real app sample photos */
export function FilmStrip() {
  const reduce = useReducedMotion();
  const frames = [...FILM_STRIP, ...FILM_STRIP];
  return (
    <section className="relative overflow-hidden border-y border-hair py-10">
      <div className="mx-auto mb-6 max-w-[1120px] px-5 text-center">
        <span className="inline-flex rounded-full border border-[rgba(230,180,80,0.25)] bg-[rgba(230,180,80,0.14)] px-3.5 py-1.5 font-mono text-[11.5px] font-bold uppercase tracking-[0.2em] text-brass">
          From the roll
        </span>
        <h2 className="font-display mt-3 text-[clamp(28px,4vw,40px)] text-cream">
          The pictures guests actually see.
        </h2>
        <p className="mx-auto mt-2 max-w-[520px] text-[15px] text-muted">
          Real frames from Filmsera&apos;s sample roll — the same look new users meet on day one.
        </p>
      </div>
      <div className="relative">
        <div className="pointer-events-none absolute inset-y-0 left-0 z-10 w-16 bg-gradient-to-r from-[#0a0807] to-transparent" />
        <div className="pointer-events-none absolute inset-y-0 right-0 z-10 w-16 bg-gradient-to-l from-[#0a0807] to-transparent" />
        <motion.div
          className="flex gap-3 px-4"
          animate={reduce ? undefined : { x: ["0%", "-50%"] }}
          transition={
            reduce
              ? undefined
              : { duration: 42, ease: "linear", repeat: Infinity }
          }
        >
          {frames.map((src, i) => (
            <div
              key={`${src}-${i}`}
              className="relative w-[168px] shrink-0 overflow-hidden rounded-xl border border-[rgba(244,236,221,0.18)] bg-[#1a1510] sm:w-[200px]"
            >
              <div className="absolute inset-x-0 top-0 z-[1] flex justify-between px-2 py-1.5">
                <span className="h-1.5 w-3 rounded-sm bg-black/50" />
                <span className="h-1.5 w-3 rounded-sm bg-black/50" />
              </div>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={src}
                alt=""
                className="aspect-[3/4] w-full object-cover"
                loading="lazy"
              />
              <div className="absolute inset-x-0 bottom-0 z-[1] flex justify-between px-2 py-1.5">
                <span className="h-1.5 w-3 rounded-sm bg-black/50" />
                <span className="h-1.5 w-3 rounded-sm bg-black/50" />
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

/** Interactive camera viewfinder — cycles Looks with shutter flash */
export function CameraStage() {
  const reduce = useReducedMotion();
  const [i, setI] = useState(0);
  const [flash, setFlash] = useState(false);
  const look = LOOKS[i % LOOKS.length];

  useEffect(() => {
    if (reduce) return;
    const t = setInterval(() => {
      setFlash(true);
      setTimeout(() => {
        setFlash(false);
        setI((n) => (n + 1) % LOOKS.length);
      }, 160);
    }, 3200);
    return () => clearInterval(t);
  }, [reduce]);

  return (
    <div className="relative mx-auto w-full max-w-[340px]">
      <div className="overflow-hidden rounded-[36px] border border-hair bg-[#12100c] p-3 shadow-[0_50px_110px_-20px_rgba(0,0,0,0.75)]">
        <div className="mb-2 flex items-center justify-between px-1 font-mono text-[10px] uppercase tracking-[0.18em] text-muted">
          <span>Look Lab</span>
          <span className="text-brass">{look.name}</span>
        </div>
        <div className="relative aspect-[3/4] overflow-hidden rounded-[26px] bg-black">
          <AnimatePresence mode="wait">
            <motion.img
              key={look.cover}
              src={look.cover}
              alt={`${look.name} look preview`}
              className="absolute inset-0 h-full w-full object-cover"
              initial={reduce ? false : { opacity: 0.35, scale: 1.04 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={reduce ? undefined : { opacity: 0 }}
              transition={{ duration: 0.45 }}
            />
          </AnimatePresence>
          {/* Viewfinder chrome */}
          <div className="pointer-events-none absolute inset-3 rounded-2xl border border-white/25" />
          <div className="pointer-events-none absolute left-1/2 top-1/2 h-8 w-8 -translate-x-1/2 -translate-y-1/2 rounded-full border border-brass/70" />
          <div className="pointer-events-none absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 to-transparent p-4">
            <div className="font-display text-xl text-cream">{look.name}</div>
            <p className="text-xs text-muted">{look.blurb}</p>
          </div>
          {flash && (
            <motion.div
              className="absolute inset-0 bg-white"
              initial={{ opacity: 0.85 }}
              animate={{ opacity: 0 }}
              transition={{ duration: 0.28 }}
            />
          )}
        </div>
        <div className="mt-3 flex items-center justify-center gap-2">
          {LOOKS.map((l, idx) => (
            <button
              key={l.id}
              type="button"
              aria-label={`Show ${l.name}`}
              onClick={() => {
                setFlash(true);
                setTimeout(() => {
                  setFlash(false);
                  setI(idx);
                }, 120);
              }}
              className={`h-2 w-2 rounded-full transition ${
                idx === i % LOOKS.length ? "bg-brass" : "bg-white/25"
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export function LookShelf({ looks }: { looks: readonly Camera[] }) {
  return (
    <div className="flex gap-4 overflow-x-auto px-5 pb-6 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
      {looks.map((look) => (
        <a
          key={look.id}
          href={`/looks/${look.id}.html`}
          className="group w-[260px] shrink-0 overflow-hidden rounded-[22px] border border-hair bg-surface transition hover:border-[rgba(230,180,80,0.35)]"
        >
          <div className="relative aspect-[4/5] overflow-hidden">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={look.cover}
              alt={`${look.name} graded sample`}
              className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.04]"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/25 to-transparent" />
            <div className="absolute left-3 top-3 flex items-center gap-2">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={look.icon}
                alt=""
                className="h-11 w-11 rounded-[12px] border border-white/15 bg-black/40"
              />
            </div>
            <div className="absolute bottom-0 p-4">
              <div className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-brass">
                {look.stockCode} · No. {look.modelNumber}
              </div>
              <div className="font-display text-2xl text-cream">{look.name}</div>
            </div>
          </div>
          <div className="p-4">
            <p className="text-sm text-muted">{look.blurb}</p>
            <div className="mt-3 flex gap-1.5 overflow-hidden">
              {look.strip.map((src) => (
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  key={src}
                  src={src}
                  alt=""
                  className="h-[70px] w-[54px] rounded-lg object-cover ring-1 ring-white/10"
                  loading="lazy"
                />
              ))}
            </div>
          </div>
        </a>
      ))}
    </div>
  );
}

/** Full camera list block for homepage — matches Cameras screen strips */
export function CameraCatalogPreview() {
  const preview = CAMERAS.slice(0, 8);
  return (
    <div className="mx-auto mt-10 grid max-w-[1120px] gap-4 px-5 md:grid-cols-2">
      {preview.map((cam) => (
        <a
          key={cam.id}
          href={`/looks/${cam.id}.html`}
          className="rounded-[22px] border border-hair bg-surface p-4 transition hover:border-[rgba(230,180,80,0.35)]"
        >
          <div className="flex gap-3">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={cam.icon} alt="" className="h-14 w-14 rounded-[14px] border border-hair" />
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-baseline gap-2">
                <span className="font-display text-xl text-cream">{cam.name}</span>
                <span className="font-mono text-[10px] tracking-wide text-muted">{cam.stockCode}</span>
                <span className="rounded bg-[rgba(230,180,80,0.14)] px-1.5 py-0.5 font-mono text-[10px] text-brass">
                  No. {cam.modelNumber}
                </span>
              </div>
              <p className="mt-1 line-clamp-2 text-sm text-muted">{cam.story}</p>
            </div>
          </div>
          <div className="mt-3 flex gap-2 overflow-x-auto [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
            {cam.strip.map((src) => (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                key={src}
                src={src}
                alt=""
                className="h-[110px] w-[84px] shrink-0 rounded-lg object-cover"
                loading="lazy"
              />
            ))}
          </div>
        </a>
      ))}
    </div>
  );
}

export function HowItWorks() {
  return (
    <div className="mx-auto mt-10 grid max-w-[1120px] gap-5 px-5 sm:grid-cols-2 lg:grid-cols-4">
      {HOW_STEPS.map((step) => (
        <div
          key={step.n}
          className="overflow-hidden rounded-[22px] border border-hair bg-surface"
        >
          <div className="relative aspect-[9/16] bg-black">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={step.screen}
              alt={step.title}
              className="h-full w-full object-cover object-top"
              loading="lazy"
            />
          </div>
          <div className="p-5 text-center">
            <div className="mx-auto mb-3 flex h-9 w-9 items-center justify-center rounded-full bg-brass font-display text-lg text-brass-deep">
              {step.n}
            </div>
            <h3 className="font-display text-[22px] text-cream">{step.title}</h3>
            <p className="mt-2 text-sm text-muted">{step.body}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

export function RecapShowcase() {
  const strip = FILM_STRIP.slice(0, 6);
  return (
    <section id="recap" className="mx-auto max-w-[1120px] px-5 py-16">
      <div className="grid items-center gap-10 md:grid-cols-2">
        <div>
          <span className="inline-flex rounded-full border border-[rgba(230,180,80,0.25)] bg-[rgba(230,180,80,0.14)] px-3.5 py-1.5 font-mono text-[11.5px] font-bold uppercase tracking-[0.2em] text-brass">
            Recap reel
          </span>
          <h2 className="font-display mt-4 text-[clamp(30px,4.4vw,46px)] text-cream">
            Turn the Film into a vertical reel.
          </h2>
          <p className="mt-3 text-[17px] text-muted">
            After Reveal, Filmsera stitches Frames into a shareable Recap — music, stickers,
            and the same Looks your guests shot through.
          </p>
          <div className="mt-6 flex gap-2 overflow-x-auto pb-1">
            {strip.map((src) => (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                key={src}
                src={src}
                alt=""
                className="h-24 w-16 shrink-0 rounded-lg object-cover ring-1 ring-white/10"
                loading="lazy"
              />
            ))}
          </div>
        </div>
        <div className="flex justify-center">
          <div className="w-[260px] overflow-hidden rounded-[40px] border border-hair bg-[#171411] p-2 shadow-[0_40px_90px_-20px_rgba(0,0,0,0.7)]">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/shots/screens/08-recap.png"
              alt="Filmsera Recap reel"
              className="aspect-[9/19] w-full rounded-[32px] object-cover object-top"
            />
          </div>
        </div>
      </div>
    </section>
  );
}

export function FeatureBento() {
  const cells = [
    {
      title: "Looks",
      body: "25 hand-tuned cameras live in the viewfinder — grain, halation, Frame and all.",
      img: "/shots/screens/02-looks.png",
    },
    {
      title: "Shared Films",
      body: "Host a Film. Guests join by QR or code. Every Shot lands on one roll.",
      img: "/shots/screens/06-group.png",
    },
    {
      title: "Reveal",
      body: "Nobody peeks early. When the timer hits zero, the whole album opens together.",
      img: "/shots/screens/05-reveal.png",
    },
    {
      title: "Recap",
      body: "Turn a developed Film into a vertical reel with music and stickers.",
      img: "/shots/screens/08-recap.png",
    },
  ];
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {cells.map((c) => (
        <div
          key={c.title}
          className="overflow-hidden rounded-[22px] border border-hair bg-surface"
        >
          <div className="relative h-44 overflow-hidden bg-black sm:h-52">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={c.img} alt={c.title} className="h-full w-full object-cover object-top" loading="lazy" />
            <div className="absolute inset-0 bg-gradient-to-t from-[#1c1813] via-transparent to-transparent" />
          </div>
          <div className="p-6">
            <div className="mb-2 font-mono text-[11px] font-bold uppercase tracking-[0.2em] text-brass">
              {c.title}
            </div>
            <p className="text-[15.5px] leading-relaxed text-muted">{c.body}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
