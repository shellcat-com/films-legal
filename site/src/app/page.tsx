import Link from "next/link";
import { AppStoreBadge, DesktopQr, SiteNav } from "../components/Nav";
import { FaqAccordion, Reveal } from "../components/ParablePieces";
import {
  CameraCatalogPreview,
  CameraStage,
  FeatureBento,
  FilmStrip,
  HowItWorks,
  LookShelf,
  RecapShowcase,
} from "../components/VisualPieces";
import { LOOKS } from "../lib/site";

export default function HomePage() {
  return (
    <>
      <SiteNav />
      <main className="relative z-[2]">
        {/* Hero — TIDAL/Mobbin: phone + lifestyle photography */}
        <header className="mx-auto grid max-w-[1120px] items-center gap-10 px-5 py-14 md:grid-cols-2 md:py-20">
          <div>
            <span className="inline-flex rounded-full border border-[rgba(230,180,80,0.25)] bg-[rgba(230,180,80,0.14)] px-3.5 py-1.5 font-mono text-[11.5px] font-bold uppercase tracking-[0.2em] text-brass">
              Available on iOS
            </span>
            <h1 className="font-display mt-4 text-[clamp(32px,7vw,78px)] leading-[1.04] text-cream">
              Your day,
              <br />
              <span className="text-brass">everyone&apos;s camera.</span>
            </h1>
            <p className="mt-5 max-w-[520px] text-[19px] text-muted">
              Filmsera is a group film camera. Host a shared Film, invite your people, and
              everyone shoots Shots through 25 Looks — then{" "}
              <em className="font-display not-italic text-cream">nobody sees a single Frame</em>{" "}
              until Reveal.
            </p>
            <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center">
              <AppStoreBadge />
              <DesktopQr />
            </div>
          </div>
          <CameraStage />
        </header>

        {/* Trust */}
        <div className="mx-auto flex max-w-[1120px] flex-wrap justify-center gap-x-8 gap-y-2 border-y border-hair px-5 py-4 text-[13px] font-semibold text-muted">
          <span>
            <b className="text-cream">25</b> Looks
          </span>
          <span>
            <b className="text-cream">iOS</b>
          </span>
          <span>
            <b className="text-cream">Private</b> by design
          </span>
          <span>
            Timed <b className="text-cream">Reveal</b>
          </span>
          <span>
            Shareable <b className="text-cream">Recap</b>
          </span>
        </div>

        {/* Film strip — real sample photos from the app bundle */}
        <FilmStrip />

        {/* Look Lab */}
        <section id="looks" className="py-16">
          <Reveal className="mx-auto max-w-[700px] px-5 text-center">
            <span className="inline-flex rounded-full border border-[rgba(230,180,80,0.25)] bg-[rgba(230,180,80,0.14)] px-3.5 py-1.5 font-mono text-[11.5px] font-bold uppercase tracking-[0.2em] text-brass">
              Look Lab · Equipment shelf
            </span>
            <h2 className="font-display mt-4 text-[clamp(30px,4.4vw,46px)] text-cream">
              Twenty-five cameras. One pocket.
            </h2>
            <p className="mt-3 text-[17px] text-muted">
              The same photo pool your Look Lab grades in-app — swipe the shelf, open a family.
            </p>
          </Reveal>
          <div className="mt-8">
            <LookShelf looks={LOOKS} />
          </div>
          <p className="mt-2 text-center font-mono text-xs tracking-[0.2em] text-muted">
            ← SWIPE THE SHELF →
          </p>
          <Reveal className="mx-auto mt-14 max-w-[700px] px-5 text-center">
            <h3 className="font-display text-[clamp(26px,3.6vw,36px)] text-cream">
              Same strips as Cameras in the app.
            </h3>
            <p className="mt-2 text-[15px] text-muted">
              Icons, stock codes, and graded sample photos — exported from Filmsera&apos;s Look
              Lab pipeline.
            </p>
          </Reveal>
          <CameraCatalogPreview />
          <div className="mt-8 text-center">
            <Link href="/looks/" className="font-semibold text-brass hover:underline">
              Browse all 25 cameras →
            </Link>
          </div>
        </section>

        {/* How it works — real App Store screens */}
        <section className="bg-[linear-gradient(180deg,transparent,rgba(230,180,80,0.05),transparent)] py-16">
          <Reveal className="mx-auto max-w-[700px] px-5 text-center">
            <span className="inline-flex rounded-full border border-[rgba(230,180,80,0.25)] bg-[rgba(230,180,80,0.14)] px-3.5 py-1.5 font-mono text-[11.5px] font-bold uppercase tracking-[0.2em] text-brass">
              How it works
            </span>
            <h2 className="font-display mt-4 text-[clamp(30px,4.4vw,46px)]">
              How a night becomes a Film.
            </h2>
          </Reveal>
          <HowItWorks />
        </section>

        {/* Recap */}
        <RecapShowcase />

        {/* Feature bento */}
        <section id="reveal" className="mx-auto max-w-[1120px] px-5 py-16">
          <Reveal className="mb-8 text-center">
            <h2 className="font-display text-[clamp(30px,4.4vw,46px)]">One app. Every angle.</h2>
          </Reveal>
          <FeatureBento />
        </section>

        {/* Use cases with photos */}
        <section className="mx-auto max-w-[1120px] px-5 py-10">
          <Reveal className="text-center">
            <h2 className="font-display text-3xl">Made for nights that matter.</h2>
          </Reveal>
          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            {[
              {
                label: "Wedding",
                href: "/blog/shared-camera-roll-at-a-wedding.html",
                img: "/shots/samples/hug.jpg",
              },
              {
                label: "Party",
                href: "/blog/disposable-camera-party-playbook.html",
                img: "/shots/samples/party.jpg",
              },
              {
                label: "Trip",
                href: "/blog/one-trip-one-film.html",
                img: "/shots/samples/paris.jpg",
              },
            ].map((item) => (
              <a
                key={item.label}
                href={item.href}
                className="group relative overflow-hidden rounded-[22px] border border-hair"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={item.img}
                  alt={item.label}
                  className="aspect-[4/3] w-full object-cover transition duration-500 group-hover:scale-[1.03]"
                  loading="lazy"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
                <div className="absolute bottom-0 p-5 font-display text-2xl text-cream">
                  {item.label}
                </div>
              </a>
            ))}
          </div>
        </section>

        {/* Pricing */}
        <section id="pricing" className="mx-auto max-w-[1120px] px-5 py-16">
          <Reveal className="mx-auto mb-10 max-w-[700px] text-center">
            <span className="inline-flex rounded-full border border-[rgba(230,180,80,0.25)] bg-[rgba(230,180,80,0.14)] px-3.5 py-1.5 font-mono text-[11.5px] font-bold uppercase tracking-[0.2em] text-brass">
              Pricing
            </span>
            <h2 className="font-display mt-4 text-[clamp(30px,4.4vw,46px)] text-cream">
              Free to shoot. Pro when you want more.
            </h2>
            <p className="mt-3 text-[17px] text-muted">
              Download, host a Film, and invite your people for free. Guests never pay.
            </p>
          </Reveal>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="flex flex-col rounded-[22px] border border-hair bg-surface p-6">
              <div className="font-mono text-[11px] font-bold uppercase tracking-[0.2em] text-brass">
                Free
              </div>
              <div className="font-display mt-2 text-[40px] leading-none text-cream">$0</div>
              <p className="mt-3 text-[15px] text-muted">For everyone, forever.</p>
              <ul className="mt-5 space-y-2 text-[15px] text-muted">
                <li>5 free cameras, including Disposable and VHS</li>
                <li>Host and join shared Films</li>
                <li>Unlimited Guests</li>
                <li>Timed Reveal and Recap reels</li>
              </ul>
            </div>
            <div className="relative flex flex-col rounded-[22px] border border-[rgba(230,180,80,0.5)] bg-surface p-6 shadow-[0_24px_60px_-30px_rgba(230,180,80,0.5)]">
              <div className="absolute -top-3 left-6 rounded-full bg-brass px-3 py-1 font-mono text-[10px] font-bold uppercase tracking-[0.15em] text-brass-deep">
                3-day free trial
              </div>
              <div className="font-mono text-[11px] font-bold uppercase tracking-[0.2em] text-brass">
                Film Pro
              </div>
              <div className="font-display mt-2 text-[40px] leading-none text-cream">
                $34.99<span className="text-[16px] text-muted"> / year</span>
              </div>
              <p className="mt-3 text-[15px] text-muted">
                Also $1.99 / week or $5.99 / month. Start with a 3-day free trial.
              </p>
              <ul className="mt-5 space-y-2 text-[15px] text-muted">
                <li>All 25 cameras and premium Look packs</li>
                <li>Every Recap style</li>
                <li>Look Lab custom looks</li>
                <li>Cancel anytime in your Apple Account</li>
              </ul>
            </div>
            <div className="flex flex-col rounded-[22px] border border-hair bg-surface p-6">
              <div className="font-mono text-[11px] font-bold uppercase tracking-[0.2em] text-brass">
                Event Pass
              </div>
              <div className="font-display mt-2 text-[40px] leading-none text-cream">
                $7.99<span className="text-[16px] text-muted"> once</span>
              </div>
              <p className="mt-3 text-[15px] text-muted">One-time, for a single Film.</p>
              <ul className="mt-5 space-y-2 text-[15px] text-muted">
                <li>HD Recap for that Film</li>
                <li>No watermark</li>
                <li>No subscription needed</li>
                <li>Perfect for a one-off wedding or trip</li>
              </ul>
            </div>
          </div>
          <p className="mt-6 text-center text-[13px] text-muted">
            Prices shown in USD and may vary by region. You confirm the exact price in the App
            Store before anything is charged.
          </p>
          <div className="mt-8 flex justify-center">
            <AppStoreBadge />
          </div>
        </section>

        {/* FAQ */}
        <section id="faq" className="px-5 py-16">
          <Reveal className="mb-6 text-center">
            <h2 className="font-display text-[clamp(30px,4.4vw,46px)]">Good to know.</h2>
          </Reveal>
          <FaqAccordion />
        </section>

        {/* Footer CTA */}
        <section className="mx-auto max-w-[1120px] px-5 pb-16">
          <Reveal>
            <div className="relative overflow-hidden rounded-[30px] border border-hair">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="/shots/samples/beach.jpg"
                alt=""
                className="absolute inset-0 h-full w-full object-cover opacity-30"
              />
              <div className="absolute inset-0 bg-[linear-gradient(135deg,rgba(10,8,7,0.92),rgba(26,18,6,0.85))]" />
              <div className="relative px-7 py-12 text-center">
                <h2 className="font-display text-[clamp(28px,4.4vw,44px)]">Download Filmsera</h2>
                <p className="mt-3 text-muted">
                  25 Looks. Shared Films. Timed Reveal. Host the night — then open every Frame
                  together.
                </p>
                <div className="mt-6 flex flex-col items-center justify-center gap-4 sm:flex-row">
                  <AppStoreBadge />
                  <DesktopQr />
                </div>
              </div>
            </div>
          </Reveal>
        </section>
      </main>

      <footer className="relative z-[2] border-t border-hair py-10 text-sm text-muted">
        <div className="mx-auto flex max-w-[1120px] flex-wrap items-center justify-between gap-4 px-5">
          <div className="font-display text-2xl text-cream">✦ Filmsera</div>
          <div className="flex flex-wrap gap-5">
            <Link href="/looks/">Look Lab</Link>
            <Link href="/vs/">Compare</Link>
            <Link href="/blog/">Journal</Link>
            <a href="/privacy.html">Privacy</a>
            <a href="/terms.html">Terms</a>
            <a href="/support.html">Support</a>
          </div>
          <div>© 2026 Filmsera</div>
        </div>
      </footer>
    </>
  );
}
