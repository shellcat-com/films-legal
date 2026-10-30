# -*- coding: utf-8 -*-
"""
posts.py — The Journal manifest.

One entry per article, in display order (the first entry is the featured post,
the rest run newest -> oldest in the grid). Body copy lives in
journal-src/content/<slug>.html. Category sets the cover accent palette.
"""

# category -> (accent, accent2) for cover art + the filter pills
CATS = {
    "The Craft":   ("#E6B450", "#C8852F"),
    "Hosting":     ("#E6B450", "#D9663C"),
    "The Reveal":  ("#EBC169", "#B98A4A"),
    "Culture":     ("#D9C39A", "#A9824E"),
    "Field Guide": ("#E6B450", "#C98A3A"),
}

# order matters: [0] is featured; remainder render newest -> oldest
POSTS = [
    dict(
        slug="best-disposable-camera-apps-for-weddings-2026",
        title="Best Disposable Camera Apps for Weddings in 2026",
        cat="Hosting", date="2026-07-18", read=11, motif="rings",
        dek="An honest comparison for couples who want every guest's angle.",
        excerpt="Filmsera, Once, POV, Scene, Dazz — what actually matters for a wedding Film: Looks, Reveal, guest join, and Recap.",
    ),
    dict(
        slug="disposable-vs-vhs-vs-super8-which-look",
        title="Disposable vs VHS vs 8mm: Which Look for Which Night",
        cat="Field Guide", date="2026-07-17", read=8, motif="swatches",
        dek="A practical picker for Filmsera's camera shelf.",
        excerpt="Party flash, dance-floor grit, or soft home-movie grain — match the Look to the night before you Host the Film.",
    ),
    dict(
        slug="how-to-run-filmsera-at-your-wedding",
        title="How to Run a Filmsera Film at Your Wedding Reception",
        cat="Hosting", date="2026-07-16", read=9, motif="envelope",
        dek="Host checklist: Look, QR, memory captain, Reveal.",
        excerpt="Create the Film, pick a Look, print the join code, and let Guests fill the roll until Reveal.",
    ),
    dict(
        slug="what-makes-a-photo-feel-like-film",
        title="What Actually Makes a Photo Feel Like Film",
        cat="The Craft", date="2026-06-10", read=8, motif="grainfield",
        dek="Grain is the easy part. The feeling lives in how film fails.",
        excerpt="A digital sensor records light perfectly. Film never did — and that imperfection is exactly what your eye reads as warmth, depth, and memory.",
    ),
    dict(
        slug="grain-halation-light-leaks-explained",
        title="Grain, Halation & Light Leaks, Explained",
        cat="The Craft", date="2026-06-03", read=7, motif="lightleak",
        dek="The three accidents that became the whole aesthetic.",
        excerpt="Halation is the red bloom around a bright window. Grain is silver clumping in the dark. Here's where each one comes from — and how to use them on purpose.",
    ),
    dict(
        slug="the-case-for-not-seeing-the-photo-right-away",
        title="The Case for Not Seeing the Photo Right Away",
        cat="The Reveal", date="2026-05-27", read=7, motif="aperture",
        dek="The screen on the back of the camera quietly changed how we live a night.",
        excerpt="When you can review every frame, you stop being present. Removing the screen isn't a gimmick — it gives the evening back to the people in it.",
    ),
    dict(
        slug="shared-camera-roll-at-a-wedding",
        title="How to Run a Shared Camera Roll at a Wedding",
        cat="Hosting", date="2026-05-20", read=9, motif="rings",
        dek="Your guests already hold the best angles in the room. Here's how to collect them.",
        excerpt="The photographer gets the aisle. Your friends get everything else — the back-table laughter, the dance-floor chaos. A shared film gathers it all into one roll.",
    ),
    dict(
        slug="your-first-film-five-minute-setup",
        title="Your First Film: A Five-Minute Setup Guide",
        cat="Field Guide", date="2026-05-13", read=6, motif="sparkburst",
        dek="From download to invite link, before your coffee goes cold.",
        excerpt="Name it, pick a look, set the reveal, share one link. A walkthrough of every choice the setup screen asks you to make — and the ones worth slowing down for.",
    ),
    dict(
        slug="field-guide-to-your-film-looks",
        title="A Field Guide to Your Film Looks (and When to Reach for Each)",
        cat="The Craft", date="2026-05-06", read=9, motif="swatches",
        dek="Twenty-five cameras on one shelf. A short note on what each one is for.",
        excerpt="Disposable for a party, Super 8 for golden hour, instant for portraits. A practical map of the looks, grouped by the moment they were built to flatter.",
    ),
    dict(
        slug="from-roll-to-recap",
        title="From Roll to Recap: Turning a Film Into a Reel Worth Sharing",
        cat="The Reveal", date="2026-04-29", read=7, motif="reel",
        dek="Forty photos is an album. The right twelve, set to music, is a memory.",
        excerpt="A Recap isn't a slideshow of everything — it's an edit. How to choose the frames, pick a pace, and let a roll become something people actually rewatch.",
    ),
    dict(
        slug="collecting-guest-photos-without-chaos",
        title="Collecting Guest Photos Without the Group-Chat Chaos",
        cat="Hosting", date="2026-04-22", read=7, motif="contactsheet",
        dek="The shared album link always dies by Tuesday. There's a better way.",
        excerpt="Three hundred unsorted photos, compressed by the group chat, half of them screenshots. Here's why the usual methods fail and what to do instead.",
    ),
    dict(
        slug="the-quiet-comeback-of-the-disposable-camera",
        title="The Quiet Comeback of the Disposable Camera",
        cat="Culture", date="2026-04-15", read=8, motif="camera",
        dek="A $15 plastic box outsold itself a hundredfold. The reasons are worth reading.",
        excerpt="Disposables were supposed to be a relic. Instead they're back at weddings, festivals, and dinner tables — and not only for the look.",
    ),
    dict(
        slug="golden-hour-vs-blue-hour",
        title="Golden Hour vs. Blue Hour: Shooting With the Light You're Given",
        cat="The Craft", date="2026-04-08", read=7, motif="horizon",
        dek="The two best hours of the day are an hour apart. Know which one you're in.",
        excerpt="Golden hour flatters skin and casts long shadows. Blue hour turns a city electric. A practical guide to reading — and using — the light at the edges of the day.",
    ),
    dict(
        slug="choosing-the-right-reveal-time",
        title="Choosing the Right Reveal Time for Your Event",
        cat="Hosting", date="2026-04-01", read=6, motif="clock",
        dek="Ten minutes, midnight, or a week later — the wait shapes the whole experience.",
        excerpt="Reveal too soon and it's just a camera. Reveal too late and the moment cools. How to match the wait to the occasion, from a house party to a honeymoon.",
    ),
    dict(
        slug="why-a-new-generation-loves-film",
        title="Why a New Generation Fell Back in Love With Film",
        cat="Culture", date="2026-03-25", read=8, motif="sparkburst",
        dek="The people who never loaded a roll are the ones reviving it. That's the tell.",
        excerpt="It isn't nostalgia for them — it's novelty. A look at why the most digital generation ever went looking for friction, limits, and the wait.",
    ),
    dict(
        slug="disposable-camera-party-playbook",
        title="The Disposable Camera Party: A Host's Playbook",
        cat="Hosting", date="2026-03-18", read=8, motif="camera",
        dek="One look, one reveal time, and a rule about phones. That's the whole format.",
        excerpt="The shared disposable is the easiest party game you'll ever run and the one people talk about for weeks. Here's how to set it up so it actually lands.",
    ),
    dict(
        slug="why-anticipation-makes-a-memory-stick",
        title="Why Anticipation Makes a Memory Stick",
        cat="The Reveal", date="2026-03-11", read=7, motif="hourglass",
        dek="The wait isn't dead time. It's the part your brain remembers best.",
        excerpt="There's a reason a developed roll hits harder than a camera roll. A short tour through what waiting does to attention, dopamine, and the way we hold a moment.",
    ),
    dict(
        slug="privacy-by-design",
        title="Privacy by Design: How Films Keeps Your Roll Yours",
        cat="Field Guide", date="2026-03-04", read=6, motif="aperture",
        dek="A shared camera only works if everyone trusts where the photos go.",
        excerpt="Who can see your film, what happens before the reveal, and why your photos aren't training anything. The plain-language version of how we handle your roll.",
    ),
    dict(
        slug="color-grading-101",
        title="Color Grading 101: How to Read a Film Stock",
        cat="The Craft", date="2026-02-25", read=8, motif="prism",
        dek="Every film stock is an opinion about color. Learn to read the opinion.",
        excerpt="Why Portra whispers and Velvia shouts. How shadows, highlights, and skin tones reveal a stock's character — and how to pick the one that fits your scene.",
    ),
    dict(
        slug="one-trip-one-film",
        title="One Trip, One Film: Capturing a Group Vacation Together",
        cat="Hosting", date="2026-02-18", read=7, motif="route",
        dek="Six phones, six camera rolls, zero shared memories. Fix it before you leave.",
        excerpt="The best trip photos are the ones your friends took of you. A shared film turns six fractured camera rolls into one story you all actually keep.",
    ),
    dict(
        slug="the-quiet-power-of-a-shared-point-of-view",
        title="The Quiet Power of a Shared Point of View",
        cat="The Reveal", date="2026-02-11", read=6, motif="rings",
        dek="The same night, seen through everyone's eyes at once.",
        excerpt="You only ever see a moment from where you stood. A shared roll hands you the angles you missed — including the ones you're in.",
    ),
    dict(
        slug="a-short-history-of-the-disposable-camera",
        title="A Short History of the Disposable Camera",
        cat="Culture", date="2026-02-04", read=8, motif="filmstrip",
        dek="From a 1986 throwaway to a cultural object. How the cheapest camera won.",
        excerpt="Fujifilm called it the Utsurun-Desu — 'it takes pictures.' Forty years later the disposable is a wedding fixture and a TikTok genre. The story of how.",
    ),
    dict(
        slug="ten-creative-prompts-for-your-film",
        title="Ten Creative Prompts for Your Next Shared Film",
        cat="Field Guide", date="2026-01-28", read=6, motif="contactsheet",
        dek="Hand everyone a theme and watch a roll come alive.",
        excerpt="A shared film is better with a small constraint. Ten prompts — from 'someone's hands' to 'the last song' — that turn a random roll into a collection.",
    ),
    dict(
        slug="why-36-shots-makes-you-better",
        title="Why 36 Shots Makes You a Better Photographer",
        cat="The Craft", date="2026-01-21", read=7, motif="contactsheet",
        dek="Infinite frames taught us to stop looking. A limit gives the looking back.",
        excerpt="When every shot is free, none of them matter. Capping the roll forces the one decision that actually improves a photo: whether to take it at all.",
    ),
    dict(
        slug="how-to-write-a-film-invitation",
        title="How to Write a Film Invitation People Actually Open",
        cat="Hosting", date="2026-01-14", read=6, motif="envelope",
        dek="The invite is the first frame of the night. Don't waste it on 'hey join this.'",
        excerpt="A good film invitation sets the tone before anyone takes a photo. What to say, what to leave a mystery, and why the countdown does half the work.",
    ),
    dict(
        slug="what-we-lost-when-photos-became-instant",
        title="What We Lost When Every Photo Became Instant",
        cat="The Reveal", date="2026-01-07", read=8, motif="halation",
        dek="We gained infinite photos and misplaced the reason to take them.",
        excerpt="The instant preview was a miracle that quietly cost us something: the shoebox, the surprise, the single frame you couldn't redo. An honest accounting.",
    ),
    dict(
        slug="film-vs-digital-was-never-a-war",
        title="Film vs. Digital: It Was Never Really a War",
        cat="Culture", date="2025-12-17", read=8, motif="prism",
        dek="One is a tool. The other is a tool. The fight was always about feeling.",
        excerpt="Digital didn't kill film and film won't kill digital. They answer different questions. A clear-eyed look at what each is genuinely better at.",
    ),
    dict(
        slug="from-screen-to-paper-printing",
        title="From Screen to Paper: Printing Your Developed Film",
        cat="Field Guide", date="2025-12-10", read=7, motif="printer",
        dek="A photo on your phone is a file. A photo on the wall is a memory.",
        excerpt="The reveal shouldn't be the end of the roll. A practical guide to prints, sizes, paper, and the small ritual of putting a night on paper.",
    ),
]
