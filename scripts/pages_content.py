# -*- coding: utf-8 -*-
"""
pages_content.py: copy for scripts/build-pages.py.

Rules for this file (see the product-marketing context):
- Plain words. No invented reviews, ratings, user counts or press.
- Guest join (web join is live, 2026-11-03): guests join from the Filmsera app
  on iPhone OR from any phone's browser (iPhone Safari, Android Chrome) with no
  app and no account. Be precise: browser guests shoot photos only (no video),
  and the full 25 film looks render live only in the iPhone app. Hosts create
  films in the iPhone app.
- Competitor facts must carry a source and the date they were checked.
- PRICING below is the pricing the owner approved on 2026-11-01 and that the
  live app (4.2) enforces (Camera/Core/FilmTier.swift, convex/tiers.ts):
  Free film 10 guests (20 if the host has Film Pro); Party Pass $7.99 (30),
  Celebration Pass $24.99 (100, video clips), Wedding Pass $49.99 (250, video
  clips); Keep Photos 1 Year $4.99; Film Pro $34.99/yr, $5.99/mo or $1.99/wk
  with a 3-day trial. Keep the site in step with the app; never claim
  "no guest limit".
- Photo storage wording (Q_SAVE) must match privacy.html and terms.html word
  for word (STORAGE_RULE below).
"""

UPDATED = "2026-11-03"
UPDATED_PRETTY = "November 3, 2026"
CHECKED = "November 2, 2026"  # competitor facts checked on this date

# Plain App Store URL. TODO(CPP): the custom product pages are WAITING_FOR_REVIEW.
# Once Apple approves them, point each landing page's CTA at its ppid URL
# (see CPP_URLS) instead of APP_STORE.
APP_STORE = "https://apps.apple.com/app/id6781880091"
CPP_URLS = {
    "weddings": "https://apps.apple.com/app/id6781880091?ppid=2f7af816-668d-45cb-8ec8-927ef7d33c8f",
    "parties": "https://apps.apple.com/app/id6781880091?ppid=89ef7cea-7fb3-4b71-9854-377c086777af",
    "holiday-parties": "https://apps.apple.com/app/id6781880091?ppid=47ab65d6-e1c9-43d5-880a-896c4477cb21",
    "vintage-film-camera": "https://apps.apple.com/app/id6781880091?ppid=8fd1c7a0-5a59-4691-8277-124e80143ebd",
}


def cpp_todo(slug):
    return (f"<!-- TODO(CPP): custom product page is in Apple review. When approved, "
            f"switch this page's App Store links to {CPP_URLS[slug]} -->\n")


def a(href, label):
    return f'<a class="inl" href="{href}">{label}</a>'


# ---------------------------------------------------------------------------
# PRICING: the live app's pricing (approved 2026-11-01, re-checked 2026-11-11). Keep every price on
# the site in this block.
# ---------------------------------------------------------------------------
PRICING = {
    "free_short": "Hosting a film for up to 10 guests is free, and guests never pay",
    "event_pass": "$7.99",
    "party": "$7.99",
    "celebration": "$24.99",
    "wedding": "$49.99",
    "keep_year": "$4.99",
    "pro": "$1.99 a week (with a 3-day free trial), $5.99 a month or $34.99 a year",
}


def pricing_block():
    return f'''
  <div class="price-grid">
    <div class="price"><div class="tier">Free</div><div class="amt">$0</div>
      <ul><li>Host and join shared films</li><li>Up to 10 guests per film</li><li>5 free cameras, including Disposable and VHS</li><li>Timed reveal and recap reels</li></ul></div>
    <div class="price"><div class="tier">Film passes</div><div class="amt">from {PRICING["party"]} once</div>
      <ul><li>One-time, for a single film, no subscription</li><li>Party {PRICING["party"]}: up to 30 guests</li><li>Celebration {PRICING["celebration"]}: up to 100 guests, plus video clips</li><li>Wedding {PRICING["wedding"]}: up to 250 guests, plus video clips</li><li>Every pass: HD recap, no watermark, photos kept 1 year</li></ul></div>
    <div class="price"><div class="tier">Filmsera Pro</div><div class="amt">$34.99/yr</div>
      <ul><li>Or $5.99 a month, or $1.99 a week with a 3-day free trial</li><li>All 25 cameras and premium look packs</li><li>HD recaps with every style and song</li><li>Your free films hold 20 guests</li><li>Cancel anytime in your Apple Account</li></ul></div>
  </div>
  <p class="fine">Guests never pay. Prices in USD as listed on the US App Store on {UPDATED_PRETTY}; the App Store shows your local price before anything is charged.</p>
'''


# ---------------------------------------------------------------------------
# Reusable FAQ answers (question, answer-html). Answers are self-contained.
# ---------------------------------------------------------------------------
Q_GUEST_APP = ("Do guests need to download the app?",
               "No. Guests can join from the free Filmsera app on iPhone, or right in their phone's "
               "browser with no app and no account: they type a name and start shooting. Browser guests "
               "take photos only (no video), and the full film looks render live in the iPhone app. "
               "Guests never pay.")
Q_ANDROID = ("Does Filmsera work on Android?",
             "Yes, for guests. Android guests join and shoot in their phone's browser, with no app or "
             "account. Browser guests take photos only (no video). Hosting a film and the 25 live film "
             "looks need the Filmsera app on iPhone (iOS 17 or later); video clips also need a Celebration or Wedding film.")
Q_GUESTS_PAY = ("Do guests pay anything?",
                "No. Guests never pay. They join with the free app and shoot into the host's film.")
Q_JOIN = ("How do guests join a film?",
          "The host shares the film's QR code, an invite link, or a short join code. Guests scan or tap it "
          "on their phone. With Filmsera installed on iPhone, the film opens in the app; otherwise guests "
          "can join right in the browser by typing a name.")
# Guest limits from Camera/Core/FilmTier.swift and convex/tiers.ts.
Q_GUEST_LIMIT = ("How many guests can join one film?",
                 "A free film holds up to 10 guests, or 20 if the host has Filmsera Pro. For more, the host "
                 f"buys a one-time pass for that film: Party ({PRICING['party']}, up to 30 guests), Celebration "
                 f"({PRICING['celebration']}, up to 100) or Wedding ({PRICING['wedding']}, up to 250). The host can "
                 "upgrade a film to a bigger pass later. Guests join from the iPhone app or from any phone's browser.")
Q_PRICE = ("How much does Filmsera cost?",
           "Hosting a film for up to 10 guests and joining films are free. Bigger films use a one-time pass: "
           f"Party {PRICING['party']} (30 guests), Celebration {PRICING['celebration']} (100 guests, video clips) or "
           f"Wedding {PRICING['wedding']} (250 guests, video clips). Every pass adds an HD recap without a "
           "watermark and keeps the photos for 1 year. Filmsera Pro, a subscription at "
           f"{PRICING['pro']}, unlocks all 25 cameras and every recap style, and lets your free films hold 20 guests. "
           "Prices are in USD.")
Q_ONE_TIME = ("Is it a subscription or a one-time purchase?",
              "Both exist, and both are optional. Filmsera Pro is an auto-renewing subscription you can "
              "cancel in your Apple Account. Film passes (Party, Celebration, Wedding) are one-time purchases "
              "for a single film and never renew.")
Q_REFUND = ("How do refunds work?",
            "Purchases go through Apple, so refunds do too. Request one at "
            '<a class="inl" href="https://reportaproblem.apple.com/" rel="noopener">reportaproblem.apple.com</a>.')
Q_EARLY = ("Can I see the photos before the reveal?",
           "No. Photos stay hidden while everyone shoots, like a real disposable camera. When the reveal "
           "time arrives, the whole film appears at once for everyone in it. The host can reveal early "
           "if the group can't wait.")
Q_WHO_SEES = ("Who can see the photos?",
              "Only people in the film. Films are invite-only, and the photos appear for everyone in the "
              "film at the reveal, each tagged with who took it.")
# Same words as privacy.html ("Data retention") and terms.html ("Film passes").
# Rule from the app's Convex code (convex/tiers.ts, convex/purchases.ts,
# convex/films.ts retentionOnReveal): free film 30 days after reveal; any film pass
# or film.keep.year = 1 year; Film Pro does not change it; pre-4.2 films never purged.
STORAGE_RULE = ("Photos and clips in a shared film are kept on our servers for 30 days from the reveal. If the host buys a film pass (Party, Celebration or Wedding) or Keep Photos 1 Year for that film, they are kept for 1 year from the reveal. Film Pro does not change how long a film's photos are kept. Films created before Filmsera 4.2 are not removed automatically. Photos you save to your iPhone are not affected.")
Q_SAVE = ("Can I save the photos?",
          "Yes. After the reveal you can save photos to your iPhone and share the recap reel. "
          + STORAGE_RULE + " Save anything you want to keep. The "
          f"{a('/privacy.html', 'Privacy Policy')} has the details.")
Q_PRIVACY = ("Does Filmsera show ads, track me or train AI on my photos?",
             "No. Filmsera shows no ads, uses no third-party tracking, and does not use your photos to "
             f"train AI models. The {a('/privacy.html', 'Privacy Policy')} explains what is stored and why.")
Q_DELETE = ("Can I delete my account?",
            "Yes, from inside the app. The " + a('/privacy.html', 'Privacy Policy') +
            " explains what is removed and when.")
Q_LANGS = ("What languages is Filmsera in?",
           "Filmsera is available in 21 languages, and you can switch language inside the app.")

OPEN_SCREENS = {
    "create": {"label": "Create a film", "line": "Start a shared film for your event: pick a look, set the reveal time, and share one QR code with your guests."},
    "films": {"label": "your films", "line": "See the films you host or have joined, and the countdown to each reveal."},
    "camera": {"label": "the camera", "line": "Shoot through 25 film looks, from disposable flash to VHS, rendered live in the viewfinder."},
    "templates": {"label": "Templates", "line": "Lay out your photos in ready-made templates and frames."},
    "booth": {"label": "Photo Booth", "line": "Shoot four-shot photo booth strips with the people next to you."},
}

# 25 cameras that ship in the app: (slug for /looks/<slug>.html, name, one line)
LOOKS = [
    ("dzfilm", "DZ Film", "Clean modern film"), ("disposable", "Disposable", "Harsh flash, warm grain"),
    ("instant", "Instant", "Wide white border"), ("vhs", "VHS", "Scan lines and timecode"),
    ("eightmm", "8mm", "Home-movie grain"), ("digicam", "Digicam", "Early-2000s digicam"),
    ("note", "Notebook", "Handwritten date"), ("oldiphone", "Pocket Cam", "First-gen phone camera"),
    ("slide", "Slide", "Saturated slide film"), ("sprocket", "Sprocket 35", "35mm with sprockets"),
    ("glow", "Glow", "Halation bloom"), ("d3d", "Anaglyph", "Red-and-blue 3D"),
    ("instasqc", "Pastel Square", "Square instant"), ("sixteenmm", "16mm", "Newsreel grain"),
    ("camcorder", "Camcorder", "Green timecode"), ("kino", "Kino", "Anamorphic bars"),
    ("s67", "Heirloom", "Medium format"), ("grf", "Noir", "Street black-and-white"),
    ("original", "Original", "Drugstore prints"), ("college", "Yearbook", "Direct flash"),
    ("noga", "Light Leak", "Wild light leaks"), ("gulf", "Sunbleached", "Faded '70s"),
    ("vfone", "Keychain", "Tiny-lens charm"), ("tam", "Toy Cam", "Tunnel vignette"),
    ("ne135", "Midnight", "Cool night stock"),
]
assert len(LOOKS) == 25


# Look pages whose icon lives under a different shots/cameras/<dir> (as in site/src/lib/site.ts).
ICON_DIR = {"digicam": "digi", "camcorder": "dcr", "sprocket": "cpm35"}


def looks_grid(slugs=None):
    items = [l for l in LOOKS if slugs is None or l[0] in slugs]
    cells = "".join(
        f'<a class="look" href="/looks/{s}.html"><img src="/shots/cameras/{ICON_DIR.get(s, s)}/icon.png" alt="" width="40" height="40" loading="lazy" />'
        f'<span><b>{n}</b><small>{d}</small></span></a>' for s, n, d in items)
    return f'<div class="looks-grid">{cells}</div>'


def cards(items):
    return '<div class="cards">' + "".join(
        f'<a class="card" href="{h}"><strong>{t}</strong><span>{d}</span></a>' for h, t, d in items) + "</div>"


IPHONE_CHECK = f'''
  <h2>Guests on any phone</h2>
  <p>The host creates the film in the Filmsera app on iPhone. <strong>Guests can join from any phone.</strong> With the free Filmsera app on iPhone they get the full experience: 25 film looks live in the viewfinder, video clips and recaps. Everyone else, Android included, scans the same QR code and joins in the phone's browser, with no app and no account: they type a name and shoot.</p>
  <p>Browser guests take photos only (no video), with a light film grade rather than the live looks. Their photos land in the same roll and reveal with everyone else's. Our {a('/vs/', 'side-by-side comparison')} shows how this compares with other event cameras.</p>
'''

APP = {"@id": "https://getfilmsera.cam/#app"}


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def weddings():
    faqs = [
        ("How do wedding guests join?", "Put the film's QR code on the welcome sign and table cards. Guests scan it with their phone camera and join in the browser with no app or account, or in the free Filmsera app on iPhone for the live film looks and video. The host can also share an invite link or a short code."),
        ("When should the wedding photos reveal?", "Most couples pick the morning after, so everyone wakes up to the whole night at once. You set the reveal time when you create the film, and the host can reveal early if the group can't wait."),
        Q_GUEST_LIMIT,
        Q_ANDROID,
        Q_SAVE,
    ]
    sections = cpp_todo("weddings") + f'''
  <h2>How it works at a wedding</h2>
  <ol class="steps">
    <li><strong>Create the film.</strong> Name it for the day, pick one film look for the whole roll, and set the reveal time.</li>
    <li><strong>Print the QR code.</strong> Put it on the welcome sign, table cards or the bar, anywhere guests actually look.</li>
    <li><strong>Guests shoot.</strong> Every photo goes into the same roll, unseen. Nobody can scroll back through the night.</li>
    <li><strong>Reveal the morning after.</strong> The whole wedding appears at once, for everyone, each shot tagged with who took it.</li>
  </ol>

  <h2>What you get</h2>
  <ul>
    <li><strong>Every angle in one place:</strong> the dance floor, the speeches, the table you never got to visit.</li>
    <li><strong>Who took what:</strong> every photo is tagged with the guest who shot it.</li>
    <li><strong>A recap reel:</strong> a vertical video with music, sized for Stories and Reels.</li>
    <li><strong>A reveal countdown:</strong> a Live Activity on the lock screen counts down to the reveal.</li>
    <li><strong>One look for the day:</strong> choose from 25 film looks; the whole roll shares it, so the photos feel like one set.</li>
  </ul>

  <h2>Pricing for weddings</h2>
  {pricing_block()}
{IPHONE_CHECK}
  <h2>Day-of checklist</h2>
  <p>Ask one friend (not the couple) to be the memory captain: they announce the film at the welcome, point to the QR code, and remind tables during dinner. The {a('/guides/wedding-guest-photo-plan.html', 'printable wedding guest photo plan')} has the full checklist and a QR table sign.</p>
  <p>More reading: {a('/blog/how-to-run-filmsera-at-your-wedding.html', 'how to run a Filmsera film at your reception')} and {a('/blog/shared-camera-roll-at-a-wedding.html', 'why a shared camera roll works at a wedding')}.</p>
  <h2>Other occasions</h2>
  {cards([("/parties/", "Parties and birthdays", "One camera for the whole party."), ("/holiday-parties/", "Holiday parties", "Friendsgiving to New Year's Eve."), ("/how-it-works/", "How it works", "Every step, with app screens."), ("/faq/", "FAQ", "Guests, pricing, reveal, privacy.")])}
'''
    return dict(
        slug="weddings", file="weddings/index.html", path="/weddings/", nav_active="/weddings/",
        title="Wedding Disposable Camera App with QR Code | Filmsera",
        desc="Give every wedding guest a disposable camera on their phone. Share one QR code, keep photos hidden until the reveal, and get every angle in one roll.",
        pill="Weddings", h1="A disposable camera for every wedding guest",
        dek="One shared roll for the whole wedding. Guests shoot on their own phones, and nobody sees a photo until the reveal.",
        answer=("Filmsera turns every guest's phone into a shared disposable camera for your wedding. "
                "Guests scan one QR code and shoot into the same roll, and the photos stay hidden until the "
                "reveal time you pick, often the morning after. Then the whole day appears at once, tagged "
                f"with who took each shot. {PRICING['free_short']}."),
        crumbs=[("Weddings", "/weddings/")], app_argument="/open/create",
        sections=sections, faqs=faqs, faq_title="Wedding questions",
        band=("Get Filmsera for your wedding", "Create the film. Print the QR. Reveal it together. Guests join from any phone."),
    )


def parties():
    faqs = [
        ("What kind of parties is Filmsera for?", "Birthdays, house parties, bachelorette and bachelor weekends, reunions and trips: any night where everyone has their phone out and the photos usually end up scattered across group chats."),
        ("Can a film last a whole weekend?", "Yes. You set the reveal time when you create the film, so a bachelorette weekend can run for days and reveal on the drive home."),
        Q_GUEST_LIMIT,
        Q_GUEST_APP,
        Q_ANDROID,
    ]
    sections = cpp_todo("parties") + f'''
  <h2>Birthdays and house parties</h2>
  <p>Make one film for the night and put the QR code by the drinks. Everyone shoots, nobody checks, and the roll reveals the next morning, when the group chat is already wondering what happened. For the moments when people squeeze together, Photo Booth mode shoots four-shot strips.</p>

  <h2>Bachelorette and bachelor weekends</h2>
  <p>One film can cover the whole trip. Set the reveal for the drive home or the Monday after, so the weekend lands all at once. Every shot is tagged with who took it, so you always know whose blurry dance-floor photo is whose.</p>

  <h2>Pick a look for the night</h2>
  <p>The host picks one look and the whole roll shares it. Harsh disposable flash for a house party, VHS for a nineties birthday, a crunchy early-2000s digicam for the dance floor.</p>
  {looks_grid({"disposable", "vhs", "digicam", "instant"})}
  <p>Still deciding? Read {a('/blog/disposable-vs-vhs-vs-super8-which-look.html', 'Disposable vs VHS vs 8mm: which look for which night')}.</p>

  <h2>A recap reel for Stories</h2>
  <p>After the reveal, Filmsera cuts the roll into a vertical recap reel with music, sized for Stories and Reels.</p>

  <h2>Pricing</h2>
  {pricing_block()}
{IPHONE_CHECK}
  <h2>More ideas</h2>
  {cards([("/holiday-parties/", "Holiday parties", "Friendsgiving, the office party, New Year's Eve."), ("/weddings/", "Weddings", "Every guest's angle in one roll."), ("/blog/disposable-camera-party-playbook.html", "The party playbook", "Run a disposable-camera night."), ("/how-it-works/", "How it works", "Every step, with app screens.")])}
'''
    return dict(
        slug="parties", file="parties/index.html", path="/parties/", nav_active="/parties/",
        title="Disposable Camera App for Parties & Birthdays | Filmsera",
        desc="One shared disposable camera for birthdays, house parties and bachelorette weekends. Everyone shoots on their own phone, then the roll develops at once.",
        pill="Parties & birthdays", h1="One disposable camera for the whole party",
        dek="Everyone shoots on their own phone into one shared roll, then the whole night develops at once.",
        answer=("Filmsera is a shared disposable camera for parties. The host creates a film and shares a QR "
                "code; guests shoot on their own phones, and nobody sees a photo until the reveal. Then the "
                f"whole party appears at once, tagged with who took each shot. {PRICING['free_short']}."),
        crumbs=[("Parties", "/parties/")], app_argument="/open/create",
        sections=sections, faqs=faqs, faq_title="Party questions",
        band=("One camera for the whole party", "Share the QR. Let everyone shoot. Reveal it together. Guests join from any phone."),
    )


def holiday():
    faqs = [
        ("What's a good reveal time for a holiday party?", "Pick a moment the group will share: midnight on New Year's Eve, the morning after the office party, or Boxing Day morning for a Christmas get-together. You set it when you create the film."),
        ("Can we use Filmsera instead of renting a photo booth?", "For many parties, yes. Photo Booth mode in the Filmsera iPhone app shoots four-shot strips, and the strips go into the same film as everyone else's photos."),
        Q_GUEST_LIMIT,
        Q_GUEST_APP,
        Q_ANDROID,
    ]
    sections = cpp_todo("holiday-parties") + f'''
  <h2>One film for every holiday gathering</h2>
  <h3>Friendsgiving</h3>
  <p>Shoot the table before it's demolished. Reveal the next morning, with the leftovers.</p>
  <h3>The office party</h3>
  <p>Put the QR code by the coat rack. Reveal the following morning, so the photos arrive with coffee.</p>
  <h3>Christmas with family</h3>
  <p>Every cousin, every angle. Reveal on Boxing Day morning and send the recap to the family group chat.</p>
  <h3>New Year's Eve</h3>
  <p>The classic: set the reveal for midnight and open the whole night as the year turns.</p>

  <h2>Photo Booth strips, no rental</h2>
  <p>Photo Booth mode in the Filmsera iPhone app shoots four-shot strips. Squeeze in, count down, and the strip lands in the shared film with everything else.</p>

  <h2>A recap for the group chat</h2>
  <p>After the reveal, Filmsera makes a vertical recap reel with music, ready to share with the people who couldn't make it.</p>

  <h2>Pricing</h2>
  {pricing_block()}
{IPHONE_CHECK}
  <h2>Plan the rest of the season</h2>
  {cards([("/parties/", "Parties and birthdays", "One camera for the whole party."), ("/weddings/", "Weddings", "Every guest's angle in one roll."), ("/vintage-film-camera/", "Vintage film camera", "25 looks for everyday shooting."), ("/faq/", "FAQ", "Guests, pricing, reveal, privacy.")])}
'''
    return dict(
        slug="holiday-parties", file="holiday-parties/index.html", path="/holiday-parties/", nav_active="",
        title="Holiday Party Photo App: One Shared Camera | Filmsera",
        desc="A shared camera for Christmas parties, Friendsgiving and New Year's Eve. Guests shoot on their own phones and the whole roll develops together at midnight.",
        pill="Holiday parties", h1="A shared camera for the holiday party",
        dek="Friendsgiving, the office party, Christmas and New Year's Eve: one roll for everyone, revealed together.",
        answer=("Filmsera gives a holiday party one shared camera. Guests scan a QR code and shoot on their own "
                "phones, in the app or the browser, and every photo stays hidden until the reveal time you pick, like midnight on New "
                f"Year's Eve. Then the whole night appears at once. {PRICING['free_short']}."),
        crumbs=[("Holiday parties", "/holiday-parties/")], app_argument="/open/create",
        sections=sections, faqs=faqs, faq_title="Holiday party questions",
        band=("One camera for the holidays", "Create a film, share the QR, reveal at midnight. Guests join from any phone."),
    )


def vintage():
    faqs = [
        ("How many film looks does Filmsera have?", "25. They range from disposable flash, 35mm, instant and 8mm to VHS, camcorder and early-2000s digicam, and each one renders live in the viewfinder as you shoot."),
        ("Which looks are free?", "Five cameras are free, including Disposable and VHS. Filmsera Pro unlocks all 25 and the premium look packs."),
        ("Can I shoot video?", "Yes. Hold the shutter to record a short clip through the current look."),
        ("Do I need friends to use it?", "No. The camera works on its own for everyday photos. Shared films are there when you want to shoot an event together."),
        Q_PRICE,
    ]
    item_list = {
        "@type": "ItemList", "@id": "https://getfilmsera.cam/vintage-film-camera/#looks",
        "name": "Filmsera film looks", "numberOfItems": 25,
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                             "url": f"https://getfilmsera.cam/looks/{s}.html"} for i, (s, n, _) in enumerate(LOOKS)],
    }
    sections = cpp_todo("vintage-film-camera") + f'''
  <h2>The looks shelf</h2>
  <p>Every camera below renders live in the iPhone viewfinder, so you frame the shot already looking like film. Tap one to see sample photos.</p>
  {looks_grid()}
  <p>Browse them all with sample strips in the {a('/looks/', 'Look Lab')}.</p>

  <h2>What makes it look like film</h2>
  <p>Grain, halation and light leaks are applied as you shoot, not added afterwards. Each camera has its own color, contrast and quirks: the flash falloff of a disposable, the scan lines of a VHS tape, the white border of an instant print. The Journal goes deeper in {a('/blog/what-makes-a-photo-feel-like-film.html', 'what actually makes a photo feel like film')} and {a('/blog/grain-halation-light-leaks-explained.html', 'grain, halation and light leaks, explained')}.</p>

  <h2>Hold for video</h2>
  <p>Hold the shutter to record a short clip through the same look. VHS clips look like tape, 8mm clips look like home movies.</p>

  <h2>Free and Pro</h2>
  <p>Five cameras are free, including Disposable and VHS. Filmsera Pro unlocks all 25 and every recap style for {PRICING['pro']}. Cancel anytime in your Apple Account. Prices in USD as listed on the US App Store on {UPDATED_PRETTY}.</p>

  <h2>Shoot it with friends</h2>
  <p>The same camera powers shared films: a whole group shoots into one roll and nobody sees a photo until the reveal. See {a('/how-it-works/', 'how shared films work')}.</p>
  {cards([("/parties/", "Parties and birthdays", "One camera for the whole party."), ("/weddings/", "Weddings", "Every guest's angle in one roll."), ("/vs/dazz.html", "Filmsera vs Dazz", "Solo vintage camera apps compared."), ("/faq/", "FAQ", "Pricing, privacy and more.")])}
'''
    return dict(
        slug="vintage-film-camera", file="vintage-film-camera/index.html", path="/vintage-film-camera/", nav_active="",
        title="Vintage Film Camera App for iPhone: 25 Looks | Filmsera",
        desc="Shoot disposable flash, 35mm, instant, 8mm, VHS and digicam looks live in your iPhone viewfinder. Grain, halation and light leaks rendered as you shoot.",
        pill="Vintage film camera", h1="A vintage film camera on your iPhone",
        dek="25 film looks, rendered live in the viewfinder. Disposable flash tonight, VHS tomorrow.",
        answer=("Filmsera includes 25 film looks that render live in the iPhone viewfinder: disposable flash, "
                "35mm, instant, 8mm, VHS and digicam among them. Grain, halation and light leaks are applied "
                "as you shoot, not added afterwards. Five cameras are free; Filmsera Pro unlocks all 25."),
        crumbs=[("Vintage film camera", "/vintage-film-camera/")], app_argument="/open/camera",
        sections=sections, faqs=faqs, faq_title="Camera questions", extra_ld=[item_list],
        band=("25 cameras. One pocket.", "Free on the App Store, with 5 cameras included. iPhone, iOS 17 or later."),
    )


def how_it_works():
    steps = [
        ("01-start.png", "Create a film", "The host names the film, picks one of 25 film looks for the whole roll, sets the roll size and chooses when it reveals.",
         "Filmsera home screen listing active shared films and past albums"),
        ("06-group.png", "Invite your guests", "Share the film's QR code, an invite link or a short join code. Print the QR on a sign or send the link to the group chat.",
         "A shared film in Filmsera with invite and camera buttons"),
        ("02-looks.png", "Guests join from any phone", "Scanning the code opens the film in the free Filmsera app on iPhone, or right in the phone's browser, with no app and no account: guests type a name and shoot. Browser guests take photos only; video and the live film looks are in the app. Guests never pay.",
         "The Filmsera camera with a strip of film looks to choose from"),
        ("03-capture.png", "Everyone shoots", "Photos go straight into the shared roll and stay hidden, like a real disposable. In the app, hold the shutter for a short clip, or switch to Photo Booth for four-shot strips.",
         "Shooting a party through the Disposable look in the Filmsera camera"),
        ("05-reveal.png", "The reveal", "A countdown runs until the reveal time, including a Live Activity on the lock screen. Then the whole roll develops at once, each photo tagged with who took it.",
         "A film developing in Filmsera, with a countdown and a reveal-now button"),
        ("08-recap.png", "Recap and save", "Filmsera cuts the roll into a vertical recap reel with music for Stories and Reels. Save the photos and the reel to your iPhone.",
         "The Filmsera recap screen with style choices and save and share buttons"),
    ]
    step_html = "".join(
        f'<div class="shot-step"><img src="/shots/screens/{img}" alt="{alt}" width="150" height="325" loading="lazy" />'
        f'<div><h3>{i}. {t}</h3><p>{d}</p></div></div>' for i, (img, t, d, alt) in enumerate(steps, 1))
    howto = {
        "@type": "HowTo", "@id": "https://getfilmsera.cam/how-it-works/#howto",
        "name": "How to run a shared disposable camera with Filmsera",
        "step": [{"@type": "HowToStep", "position": i, "name": t, "text": d,
                  "image": f"https://getfilmsera.cam/shots/screens/{img}"} for i, (img, t, d, _) in enumerate(steps, 1)],
    }
    faqs = [Q_GUEST_APP, Q_ANDROID, Q_JOIN, Q_EARLY]
    sections = f'''
  <h2>Six steps, start to reveal</h2>
  <div class="shot-steps">{step_html}</div>

  <h2>What the host controls</h2>
  <ul>
    <li><strong>The look:</strong> one of 25 film looks, shared by the whole roll.</li>
    <li><strong>The reveal time:</strong> the end of the night, the morning after, or days later. The host can also reveal early.</li>
    <li><strong>The roll size:</strong> how many shots each guest gets, so every photo counts.</li>
    <li><strong>Who's in:</strong> films are invite-only; only people with the code or link can join, and the host can remove a guest and their photos.</li>
  </ul>

  <h2>What guests need</h2>
  <p>Any phone with a camera and a web browser, Android included: guests join in the browser with no app and no account, and shoot photos. For the full experience (25 live film looks, video clips and recaps), guests use the free Filmsera app on an iPhone (iOS 17 or later). Guests never pay.</p>

  <h2>Privacy</h2>
  <p>Films are invite-only. Filmsera shows no ads, uses no third-party tracking, and does not use your photos to train AI models. Details are in the {a('/privacy.html', 'Privacy Policy')}.</p>

  <h2>Where to next</h2>
  {cards([("/weddings/", "Weddings", "Every guest's angle in one roll."), ("/parties/", "Parties and birthdays", "One camera for the whole party."), ("/faq/", "FAQ", "Guests, pricing, reveal, privacy."), ("/vs/", "Compare apps", "Filmsera, POV, Lense and Once.")])}
'''
    return dict(
        slug="how-it-works", file="how-it-works/index.html", path="/how-it-works/", nav_active="/how-it-works/",
        title="How Filmsera Works: A Shared Disposable Camera App",
        desc="Create a film, share a QR code or link, let every guest shoot on their phone, then reveal the whole roll at once. Here is each step, with what guests see.",
        pill="How it works", h1="How Filmsera works",
        dek="From creating a film to the morning-after reveal, step by step.",
        answer=("Filmsera is a shared disposable camera app for iPhone. A host creates a film for an event and "
                "guests join by QR code, link or short code. Everyone shoots from their own phone, and the "
                "photos stay hidden until the reveal time the host picks. Then the whole roll appears at "
                "once, tagged with who took each shot."),
        crumbs=[("How it works", "/how-it-works/")], app_argument="/open/create",
        sections=sections, faqs=faqs, faq_title="Quick answers", extra_ld=[howto],
        band=("Host your first film", "Free on the App Store. Hosts use the iPhone app; guests join from any phone."),
    )


FAQ_GROUPS = [
    ("Guests", [Q_GUEST_APP, Q_ANDROID, Q_GUESTS_PAY, Q_JOIN, Q_GUEST_LIMIT]),
    ("Pricing", [Q_PRICE, Q_ONE_TIME, Q_REFUND]),
    ("The reveal", [Q_EARLY, Q_WHO_SEES]),
    ("Photos", [Q_SAVE, ("Is there video?", "Yes. Hold the shutter to record a short clip through the current film look.")]),
    ("Privacy and account", [Q_PRIVACY, Q_DELETE, Q_LANGS]),
]


def faq_page():
    blocks = []
    all_faqs = []
    for title, items in FAQ_GROUPS:
        all_faqs.extend(items)
        inner = "".join(f"<details><summary>{q}</summary><p>{a_}</p></details>" for q, a_ in items)
        blocks.append(f'<h2>{title}</h2>\n<div class="faq">{inner}</div>')
    sections = "\n".join(blocks) + f'''
  <h2>Still have a question?</h2>
  <p>Email {a('mailto:support@getfilmsera.cam', 'support@getfilmsera.cam')} or visit {a('/support.html', 'Support')}. For the step-by-step, see {a('/how-it-works/', 'how Filmsera works')}.</p>
'''
    p = dict(
        slug="faq", file="faq/index.html", path="/faq/", nav_active="/faq/",
        title="Filmsera FAQ: Guests, Pricing, Reveal, Privacy",
        desc="Answers about Filmsera: do guests need the app, Android support, guest limits and prices, when photos reveal, how long photos are kept, and privacy.",
        pill="FAQ", h1="Filmsera questions, answered",
        dek="Plain answers about guests, pricing, the reveal, your photos and privacy.",
        crumbs=[("FAQ", "/faq/")], app_argument="/open/create",
        sections=sections, faqs=[],
        band=("Ready to host?", "Free on the App Store. Hosts use the iPhone app; guests join from any phone."),
    )
    # FAQPage schema for all groups (visible text above matches exactly).
    p["extra_ld"] = [{
        "@type": "FAQPage", "@id": "https://getfilmsera.cam/faq/#faq",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _text(a_)}}
                       for q, a_ in all_faqs],
    }]
    return p


def _text(fragment):
    import html as _h
    import re as _re
    return _h.unescape(_re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", "", fragment))).strip()


# ---------------------------------------------------------------------------
# Comparisons. Facts checked on the competitors' US App Store pages and sites
# on 2026-11-02. Lead with what each competitor does better. No adjectives
# about competitors; state only what the cited source says.
# ---------------------------------------------------------------------------
SRC = {
    "pov_as": ("POV on the US App Store", "https://apps.apple.com/us/app/pov-disposable-camera-events/id1636032890"),
    "pov_pricing": ("pov.camera/pricing", "https://pov.camera/pricing"),
    "lense_as": ("Lense on the US App Store", "https://apps.apple.com/us/app/lense-disposable-event-camera/id6444442256"),
    "lense_site": ("lense.app", "https://lense.app/"),
    "once_as": ("Once on the US App Store", "https://apps.apple.com/us/app/once-disposable-camera-event/id6754265953"),
    "filmsera_as": ("Filmsera on the US App Store", "https://apps.apple.com/app/id6781880091"),
}


def sources(keys):
    lis = "".join(f'<li><a class="inl" href="{SRC[k][1]}" rel="noopener">{SRC[k][0]}</a></li>' for k in keys)
    return f'<h2>Sources</h2>\n  <p class="fine">All competitor details checked on {CHECKED}. Prices are in USD as listed on the US App Store and can change; check each app\'s own page before you buy.</p>\n  <ul class="sources">{lis}</ul>'


# The live app's pricing in the Filmsera column.
FS_PRICE_CELL = (f"Free to host and join, up to 10 guests per film (20 with Pro). One-time film passes: Party "
                 f"{PRICING['party']} (30 guests), Celebration {PRICING['celebration']} (100) or Wedding {PRICING['wedding']} (250), "
                 "each with an HD recap and no watermark. Filmsera Pro subscription for all 25 cameras.")


def table(rows, cols):
    th = "".join(f"<th>{c}</th>" for c in ["", *cols])
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def apps_ld(path, others):
    items = [{"@type": "ListItem", "position": 1, "item": {"@type": "SoftwareApplication", "name": "Filmsera", "operatingSystem": "iOS", "url": "https://getfilmsera.cam/"}}]
    for i, (n, os_, u) in enumerate(others, start=2):
        items.append({"@type": "ListItem", "position": i, "item": {"@type": "SoftwareApplication", "name": n, "operatingSystem": os_, "url": u}})
    return {"@type": "ItemList", "@id": f"https://getfilmsera.cam{path}#apps", "name": "Apps compared", "itemListElement": items}


def vs_pov():
    rows = [
        ("Guests need the app?", "<strong>No.</strong> Guests can join in any phone's browser with no app or account (photos only). The free iPhone app adds the live film looks, plus video clips on Celebration and Wedding films.", "No. &ldquo;Guests can scan a code or tap on a link and don't have to download this app to participate.&rdquo; (App Store)"),
        ("Platforms", "Hosts: iPhone app (iOS 17 or later). Guests: iPhone app or any phone's browser, Android included.", "iOS app, Android app, web app and App Clip are offered on pov.camera/pricing."),
        ("Free tier", "Free to host, up to 10 guests per film (20 with Pro).", "Up to 10 guests free (pov.camera/pricing)."),
        ("Paid options", FS_PRICE_CELL, "App Store lists &ldquo;More Participants&rdquo; purchases from $4.99 to $89.99 and &ldquo;Gold&rdquo; at $54.99. The list doesn't say which guest count each price covers; pov.camera/pricing offers 25 to 251+ guests."),
        ("Photo reveal", "Hidden until the host's reveal time; host can reveal early.", "&ldquo;The gallery can reveal during the event or you can make people wait until the next day.&rdquo; (App Store)"),
        ("Film looks", "25 film looks rendered live in the viewfinder.", "The App Store description doesn't list film-look presets."),
        ("Recap video", "Vertical recap reel with music.", "Not mentioned in the App Store description."),
    ]
    sections = f'''
  <h2>The short version</h2>
  <p>Both let guests join from a code or link without installing anything, Android included. <strong>POV is the better fit when the host isn't on iPhone:</strong> it offers host apps for iOS, Android and the web, while Filmsera films are created in the iPhone app. <strong>Filmsera is the better fit when the host has an iPhone</strong> and you want live film looks and video for guests using the app, a recap reel, and free hosting for up to 10 guests.</p>
  <h2>Side by side</h2>
  {table(rows, ["Filmsera", "POV"])}
  <h2>How guests join</h2>
  <p><strong>POV:</strong> guests scan a code or tap a link and can take part without downloading the app, according to its App Store listing. pov.camera also lists an App Clip.</p>
  <p><strong>Filmsera:</strong> guests scan the QR code or tap the invite link. With Filmsera on iPhone it opens in the app; on any other phone, or without the app, guests join in the browser by typing a name, with no account. Browser guests take photos only (no video).</p>
  <h2>Choose POV if…</h2>
  <ul><li>The host uses Android or wants to run the event from the web.</li><li>You want an App Clip option for iPhone guests.</li></ul>
  <h2>Choose Filmsera if…</h2>
  <ul><li>The host has an iPhone, and guests may use any phone.</li><li>You want the roll shot through a film look, live in the viewfinder of the iPhone app.</li><li>You want a recap reel for Stories and Reels.</li></ul>
  {sources(["pov_as", "pov_pricing", "filmsera_as"])}
  <p>See also: {a('/vs/lense.html', 'Filmsera vs Lense')}, {a('/vs/once.html', 'Filmsera vs Once')}, {a('/vs/', 'all comparisons')}.</p>
'''
    faqs = [
        ("Do POV guests need the app?", "Not according to POV's App Store listing: &ldquo;Guests can scan a code or tap on a link and don't have to download this app to participate.&rdquo; Filmsera guests don't either: they can join in any phone's browser with no account (photos only), or use the free iPhone app for live film looks and video."),
        ("Is there a POV alternative with film looks?", "Filmsera is a shared disposable camera with 25 film looks rendered live in the iPhone viewfinder. Guests without the app can still join in their phone's browser and shoot photos; the live looks and video are in the iPhone app, and hosts create films on iPhone."),
    ]
    return dict(
        slug="vs-pov", file="vs/pov.html", path="/vs/pov.html", nav_active="/vs/",
        title="Filmsera vs POV: Prices, Guest Join & Reveal Compared",
        desc="Filmsera vs POV, side by side: browser guest join, platforms, prices, reveal, film looks and recap reels. Facts from both App Store pages, checked Nov 2026.",
        pill="Comparison", h1="Filmsera vs POV",
        dek=f"Two shared event cameras, compared on facts. Prices and features checked {CHECKED}.",
        crumbs=[("Compare", "/vs/"), ("Filmsera vs POV", "/vs/pov.html")],
        sections=sections, faqs=faqs, faq_title="Questions",
        extra_ld=[apps_ld("/vs/pov.html", [("POV", "iOS, Android, Web", "https://pov.camera/")])],
        band=("Try Filmsera", "Free to host on iPhone. Guests join from any phone."),
    )


def vs_lense():
    rows = [
        ("Guests need the app?", "<strong>No.</strong> Guests can join in any phone's browser with no app or account (photos only). The free iPhone app adds the live film looks, plus video clips on Celebration and Wedding films.", "No. &ldquo;The guests don't need to download any app to take pictures!&rdquo; (App Store)"),
        ("Android guests", "Yes, in the browser, with no app or account (photos only).", "&ldquo;Lense works on both iPhone and Android devices!&rdquo; (lense.app)"),
        ("Free tier", "Free to host, up to 10 guests per film (20 with Pro).", "&ldquo;You can try the Lense camera for free by creating an event for up to 7 guests.&rdquo; (lense.app)"),
        ("Paid options", FS_PRICE_CELL, "App Store list: Max 25 guests $4.99, 50 $14.99, 100 $34.99, 150 $44.99. With unlimited shots: 25 $14.99, 50 $24.99, 100 $44.99, 150 $54.99, 200 $69.99. Video Uploads $9.99."),
        ("Photo reveal", "Hidden until the host's reveal time; host can reveal early.", "&ldquo;Customize the delay to your preference, whether it's a few hours, days, or even weeks.&rdquo; (App Store)"),
        ("Storage", f"Limited time after the reveal; see the {a('/privacy.html', 'Privacy Policy')}.", "&ldquo;Remain available for 12 months from your event start date.&rdquo; (lense.app)"),
        ("Film looks", "25 film looks rendered live in the viewfinder.", "&ldquo;Disposable camera effect&rdquo; (App Store)."),
        ("Extras", "Recap reel with music, Photo Booth strips, reveal Live Activity.", "Live photo display on a TV or projector (lense.app); guests can upload from their camera roll (App Store)."),
    ]
    sections = f'''
  <h2>The short version</h2>
  <p>Both let guests on iPhone and Android take photos without downloading an app. <strong>Lense is the better fit when you want extras around the event:</strong> a live photo display for a TV or projector, and camera-roll uploads. <strong>Filmsera is the better fit when the host has an iPhone</strong> and you want 25 live film looks and video for guests using the app, a recap reel, and free hosting for up to 10 guests.</p>
  <h2>Side by side</h2>
  {table(rows, ["Filmsera", "Lense"])}
  <h2>Price by guest count</h2>
  <p>Lense's App Store list prices a 100-guest event at $34.99, or $44.99 with unlimited shots. A free Filmsera film holds up to 10 guests; a 100-guest film takes the {PRICING['celebration']} Celebration Pass, which adds video clips, an HD recap without a watermark and 1-year storage.</p>
  <h2>Choose Lense if…</h2>
  <ul><li>You want photos on a big screen during the event.</li><li>Guests should be able to add photos from their camera roll.</li><li>The host isn't on iPhone (Lense's App Store app is listed for iPhone, and its website says it works on both platforms).</li></ul>
  <h2>Choose Filmsera if…</h2>
  <ul><li>The host has an iPhone, and guests may use any phone.</li><li>You want the roll shot through a film look, live in the viewfinder of the iPhone app.</li><li>You want a recap reel for Stories and Reels.</li></ul>
  {sources(["lense_as", "lense_site", "filmsera_as"])}
  <p>See also: {a('/vs/pov.html', 'Filmsera vs POV')}, {a('/vs/once.html', 'Filmsera vs Once')}, {a('/vs/', 'all comparisons')}.</p>
'''
    faqs = [
        ("Does Lense work for Android guests?", "Lense's website says it &ldquo;works on both iPhone and Android devices,&rdquo; and its App Store listing says guests don't need to download an app. Filmsera guests can also join in any phone's browser, Android included, with no app or account (photos only)."),
        ("How long does Lense keep photos?", "Lense's website says photos and videos remain available for 12 months from the event start date."),
    ]
    return dict(
        slug="vs-lense", file="vs/lense.html", path="/vs/lense.html", nav_active="/vs/",
        title="Filmsera vs Lense: Disposable Camera Apps Compared",
        desc="How Filmsera and Lense compare for weddings and parties: guest join, Android support, prices by guest count, storage and reveal. Checked Nov 2026.",
        pill="Comparison", h1="Filmsera vs Lense",
        dek=f"Two shared event cameras, compared on facts. Prices and features checked {CHECKED}.",
        crumbs=[("Compare", "/vs/"), ("Filmsera vs Lense", "/vs/lense.html")],
        sections=sections, faqs=faqs, faq_title="Questions",
        extra_ld=[apps_ld("/vs/lense.html", [("Lense", "iOS", "https://lense.app/")])],
        band=("Try Filmsera", "Free to host on iPhone. Guests join from any phone."),
    )


def vs_once():
    rows = [
        ("Guests need the app?", "<strong>No.</strong> Guests can join in any phone's browser with no app or account (photos only). The free iPhone app adds the live film looks, plus video clips on Celebration and Wedding films.", "No. &ldquo;Guests can join with or without the app via App Clip.&rdquo; (App Store)"),
        ("Platforms", "Hosts: iPhone app (iOS 17 or later). Guests: iPhone app or any phone's browser, Android included.", "The App Store listing covers Apple devices; it doesn't mention Android. App Clips run on iPhone."),
        ("Free tier", "Free to host, up to 10 guests per film (20 with Pro).", "None listed. The smallest App Store purchase is &ldquo;Film: 10 participants&rdquo; at $1.99."),
        ("Paid options", FS_PRICE_CELL, "App Store list: Film 10 participants $1.99, 25 $4.99, 50 $14.99, 100 $29.99, 150 $49.99. Unlimited shots: 50 $24.99, 100 $39.99. Add-ons from $3.99."),
        ("Photo reveal", "Hidden until the host's reveal time; host can reveal early.", "&ldquo;Unlock photos at event end or a custom time.&rdquo; (App Store)"),
        ("Film looks", "25 film looks rendered live in the viewfinder.", "&ldquo;Subtle, tasteful looks that keep skin tones and ambience true.&rdquo; (App Store)"),
        ("Downloads", "Save photos and the recap reel to your iPhone.", "&ldquo;Save full galleries to your device or archive them for later.&rdquo; (App Store)"),
    ]
    sections = f'''
  <h2>The short version</h2>
  <p>Both let guests join without installing a full app: Once through an App Clip, Filmsera in the phone's browser, which also works on Android. <strong>Once is the better fit if you want an App Clip on iPhone</strong> and per-event pricing by participant count. <strong>Filmsera is the better fit when guests use mixed phones</strong>, or you want 25 live film looks and video for guests using the app, a recap reel, and free hosting for up to 10 guests.</p>
  <h2>Side by side</h2>
  {table(rows, ["Filmsera", "Once"])}
  <h2>How guests join</h2>
  <p><strong>Once:</strong> guests join through an App Clip, a small part of the app that runs without a full install, or with the full app.</p>
  <p><strong>Filmsera:</strong> guests scan the QR code or tap the invite link. With Filmsera on iPhone it opens in the app; on any other phone, or without the app, guests join in the browser by typing a name, with no account. Browser guests take photos only (no video).</p>
  <h2>Choose Once if…</h2>
  <ul><li>You want iPhone guests to join through an App Clip.</li><li>You want to pay per event by participant count.</li></ul>
  <h2>Choose Filmsera if…</h2>
  <ul><li>Some guests use Android: they can join in the browser.</li><li>You want a distinct film look, live in the viewfinder of the iPhone app.</li><li>You want a recap reel for Stories and Reels.</li></ul>
  {sources(["once_as", "filmsera_as"])}
  <p>See also: {a('/vs/pov.html', 'Filmsera vs POV')}, {a('/vs/lense.html', 'Filmsera vs Lense')}, {a('/vs/', 'all comparisons')}.</p>
'''
    faqs = [
        ("Do Once guests need the app?", "Once's App Store listing says &ldquo;Guests can join with or without the app via App Clip.&rdquo; Filmsera guests can join in any phone's browser with no account (photos only), or in the free iPhone app."),
        ("Is Once free?", "Once's App Store listing doesn't show a free tier; its smallest listed purchase is a 10-participant film for $1.99."),
    ]
    return dict(
        slug="vs-once", file="vs/once.html", path="/vs/once.html", nav_active="/vs/",
        title="Filmsera vs Once: Shared Disposable Cameras Compared",
        desc="Filmsera vs Once for weddings and parties: App Clip guest join, prices by participant count, reveal timing, film looks and recaps. Checked Nov 2026.",
        pill="Comparison", h1="Filmsera vs Once",
        dek=f"Two shared event cameras, compared on facts. Prices and features checked {CHECKED}.",
        crumbs=[("Compare", "/vs/"), ("Filmsera vs Once", "/vs/once.html")],
        sections=sections, faqs=faqs, faq_title="Questions",
        extra_ld=[apps_ld("/vs/once.html", [("Once", "iOS", SRC["once_as"][1])])],
        band=("Try Filmsera", "Free to host on iPhone. Guests join from any phone."),
    )


def vs_hub():
    rows = [
        ("Guests need the app?", "No (browser join, photos only; app adds live looks, and video on Celebration and Wedding films)", "No", "No", "No (App Clip)"),
        ("Android guests", "Yes (browser)", "Android app offered", "Yes", "Not mentioned"),
        ("Host platform", "iPhone app", "iOS, Android and web apps", "iPhone app (App Store); website says iPhone and Android", "Apple devices"),
        ("Free tier", "Free to host, up to 10 guests (20 with Pro)", "Up to 10 guests", "Trial event, up to 7 guests", "None listed"),
        ("Paid (App Store, USD)", f"Film passes {PRICING['party']} (30 guests) to {PRICING['wedding']} (250); Pro subscription", "$4.99–$89.99 participant purchases", "$4.99 (25 guests) to $69.99 (200, unlimited shots)", "$1.99 (10) to $49.99 (150)"),
        ("Delayed reveal", "Yes", "Yes", "Yes", "Yes"),
        ("Live film looks", "25", "Not listed", "Disposable effect", "&ldquo;Subtle, tasteful looks&rdquo;"),
    ]
    sections = f'''
  <h2>Event cameras at a glance</h2>
  <p>All four let guests join without installing a full app. Filmsera guests join in any phone's browser, Android included, with no account; browser guests shoot photos only, and the iPhone app adds the live film looks (and video clips on Celebration and Wedding films). Filmsera hosts create films in the iPhone app. Filmsera's strengths are 25 live film looks, a recap reel, and free hosting for up to 10 guests. Competitor details checked {CHECKED}.</p>
  {table(rows, ["Filmsera", "POV", "Lense", "Once"])}
  <p class="fine">Sources and exact wording are on each comparison page. Prices are as listed on the US App Store on {CHECKED} and can change.</p>
  <h2>Detailed comparisons</h2>
  {cards([("/vs/pov.html", "Filmsera vs POV", "Guest join, platforms, prices and reveal."), ("/vs/lense.html", "Filmsera vs Lense", "Android guests, prices by guest count, storage."), ("/vs/once.html", "Filmsera vs Once", "App Clip join, per-participant prices, looks.")])}
  <h2>Solo film cameras</h2>
  <p>Looking for a vintage camera for your own photos rather than a shared event roll?</p>
  {cards([("/vs/dazz.html", "Filmsera vs Dazz", "Solo vintage camera apps."), ("/vs/daze.html", "Filmsera vs Daze", "Texture for individual shooting."), ("/vintage-film-camera/", "Filmsera's 25 looks", "Every camera, live in the viewfinder.")])}
  {sources(["pov_as", "pov_pricing", "lense_as", "lense_site", "once_as", "filmsera_as"])}
'''
    return dict(
        slug="vs", file="vs/index.html", path="/vs/", nav_active="/vs/", page_type="CollectionPage",
        title="POV Alternatives: Disposable Camera Apps Compared",
        desc="Comparing disposable camera apps for events: Filmsera, POV, Lense and Once. Guest join, Android support, prices by guest count and reveal, side by side.",
        pill="Comparisons", h1="Disposable camera apps, compared",
        dek=f"Filmsera, POV, Lense and Once side by side, with sources. Checked {CHECKED}.",
        crumbs=[("Compare", "/vs/")],
        sections=sections, faqs=[],
        extra_ld=[apps_ld("/vs/", [("POV", "iOS, Android, Web", "https://pov.camera/"), ("Lense", "iOS", "https://lense.app/"), ("Once", "iOS", SRC["once_as"][1])])],
        band=("Try Filmsera", "Free to host on iPhone. Guests join from any phone."),
    )


def pages():
    return [weddings(), parties(), holiday(), vintage(), how_it_works(), faq_page(),
            vs_hub(), vs_pov(), vs_lense(), vs_once()]
