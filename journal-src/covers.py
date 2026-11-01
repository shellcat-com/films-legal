"""
covers.py — generative, on-brand SVG cover art for The Journal.

Each cover is a 1200x630 vector composition (doubles as an og:image) drawn in
the Films palette: brass/cream linework on a warm-dark ground, a soft radial
glow, a faint film-grain overlay, a 1px hairline frame, and a small brass Daybreak
mark. No raster photos, no baked text — purely abstract editorial art so the set
feels cohesive but every post gets a distinct image.

A motif is a function (rng, a, b) -> svg markup string, where `a` is the primary
accent and `b` a secondary tone. Determinism comes from a per-slug seed so a
given post always renders the same cover.
"""

import math
import random
from pathlib import Path

W, H = 1200, 630
BG = "#0A0807"
CREAM = "#F4ECDD"
HAIR = "rgba(245,232,210,0.10)"

MARK = (Path(__file__).resolve().parents[1] / "brand/filmsera-mark.svg").read_text().strip()
MARK = MARK.replace("<svg ", '<svg width="100" height="100" ', 1)


# ----------------------------------------------------------------------------- helpers
def rng_for(seed):
    r = random.Random()
    r.seed(seed)
    return r


def _f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def line(x1, y1, x2, y2, stroke, w=2, opacity=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" '
            f'stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" '
            f'opacity="{opacity}"{d}/>')


def circle(cx, cy, r, stroke=None, fill="none", w=2, opacity=1):
    s = f' stroke="{stroke}" stroke-width="{w}"' if stroke else ""
    return f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r)}" fill="{fill}"{s} opacity="{opacity}"/>'


def rrect(x, y, w, h, r, stroke=None, fill="none", sw=2, opacity=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" '
            f'rx="{_f(r)}" fill="{fill}"{s} opacity="{opacity}"/>')


# ----------------------------------------------------------------------------- motifs
def m_filmstrip(rng, a, b, reel=False):
    cx, cy = W / 2, H / 2
    rot = rng.uniform(-10, -6)
    out = [f'<g transform="rotate({_f(rot)} {cx} {cy})">']
    sw, sh = 1180, 240
    sx, sy = cx - sw / 2, cy - sh / 2
    out.append(rrect(sx, sy, sw, sh, 14, stroke=a, fill="rgba(230,180,80,0.05)", sw=2.5))
    # sprocket holes top & bottom
    n = 16
    for i in range(n):
        hx = sx + 26 + i * (sw - 52) / (n - 1)
        out.append(rrect(hx - 11, sy + 16, 22, 30, 5, fill="none", stroke=a, sw=1.6, opacity=.55))
        out.append(rrect(hx - 11, sy + sh - 46, 22, 30, 5, fill="none", stroke=a, sw=1.6, opacity=.55))
    # frames
    fy, fh = sy + 60, sh - 120
    frames = 5
    fw = (sw - 120) / frames
    for i in range(frames):
        fx = sx + 60 + i * fw
        op = .10 + .06 * ((i + 1) % 3)
        out.append(rrect(fx + 6, fy, fw - 12, fh, 4, fill=a, opacity=op))
        out.append(rrect(fx + 6, fy, fw - 12, fh, 4, stroke=CREAM, sw=1, opacity=.18))
    out.append("</g>")
    if reel:
        out.append(circle(cx, cy, 52, fill="rgba(10,8,7,0.85)", stroke=a, w=2.5))
        out.append(f'<path d="M{_f(cx-16)} {_f(cy-24)} L{_f(cx+30)} {_f(cy)} '
                    f'L{_f(cx-16)} {_f(cy+24)} Z" fill="{a}"/>')
    return "".join(out)


def m_reel(rng, a, b):
    return m_filmstrip(rng, a, b, reel=True)


def m_aperture(rng, a, b, blades=7):
    cx, cy = W / 2, H / 2
    R, r = 200, 96
    out = [circle(cx, cy, R + 26, stroke=a, w=1.4, opacity=.25)]
    out.append(circle(cx, cy, R, stroke=a, w=2.4, opacity=.9))
    start = rng.uniform(0, math.tau)
    pts = []
    for i in range(blades):
        ang = start + i * math.tau / blades
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    # iris polygon
    poly = " ".join(f"{_f(x)},{_f(y)}" for x, y in pts)
    out.append(f'<polygon points="{poly}" fill="rgba(230,180,80,0.07)" stroke="{a}" stroke-width="2"/>')
    # blades: connect inner vertices to ring tangentially
    for i in range(blades):
        x, y = pts[i]
        ang = start + i * math.tau / blades + math.tau / blades * .5
        ox, oy = cx + R * math.cos(ang), cy + R * math.sin(ang)
        out.append(line(x, y, ox, oy, a, 1.6, .6))
    out.append(circle(cx, cy, 4, fill=a))
    return "".join(out)


def m_lightleak(rng, a, b):
    out = []
    out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#leak)"/>')
    # streaks
    for i in range(3):
        x = rng.uniform(200, 1000)
        wdt = rng.uniform(26, 70)
        out.append(f'<rect x="{_f(x)}" y="-40" width="{_f(wdt)}" height="{H+80}" '
                    f'transform="rotate({_f(rng.uniform(-18,-8))} {_f(x)} {H/2})" '
                    f'fill="{a}" opacity="{_f(rng.uniform(.05,.12))}"/>')
    out.append(circle(rng.uniform(820, 1000), rng.uniform(120, 240), 150,
                      fill="url(#bloom)", opacity=.8))
    return "".join(out)


def m_grainfield(rng, a, b):
    out = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#vgrain)"/>']
    out.append(circle(W * .72, H * .42, 168, stroke=a, w=1.6, opacity=.3))
    out.append(circle(W * .72, H * .42, 168, fill="url(#bloom)", opacity=.5))
    for _ in range(520):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        rr = rng.uniform(.6, 2.0)
        op = rng.uniform(.04, .22)
        col = a if rng.random() < .35 else CREAM
        out.append(f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{_f(rr)}" fill="{col}" opacity="{_f(op)}"/>')
    return "".join(out)


def m_developtray(rng, a, b):
    cx, cy = W * .56, H * .52
    out = []
    for i in range(7):
        rr = 60 + i * 46
        out.append(f'<ellipse cx="{_f(cx)}" cy="{_f(cy)}" rx="{_f(rr*1.35)}" ry="{_f(rr)}" '
                   f'fill="none" stroke="{a}" stroke-width="{_f(2.2-i*0.18)}" opacity="{_f(.5-i*0.05)}"/>')
    # a floating print
    out.append(rrect(cx - 230, cy - 150, 150, 180, 8, fill="rgba(244,236,221,0.06)", stroke=CREAM, sw=1.4, opacity=.5))
    out.append(rrect(cx - 218, cy - 138, 126, 132, 4, fill=a, opacity=.12))
    return "".join(out)


def m_swatches(rng, a, b):
    cx, cy = W / 2, H / 2
    tones = ["#3A2A14", "#6E4A1E", "#A9712C", b, a, "#F0CF8C", CREAM]
    out = []
    n = len(tones)
    for i, t in enumerate(tones):
        off = (i - (n - 1) / 2)
        x = cx + off * 92 - 84
        y = cy + off * 10 - 110
        out.append(f'<g transform="rotate({_f(off*3)} {_f(x+84)} {_f(y+110)})">')
        out.append(rrect(x, y, 168, 220, 14, fill=t, opacity=.92))
        out.append(rrect(x, y, 168, 220, 14, stroke="rgba(245,232,210,0.18)", sw=1))
        out.append(rrect(x + 14, y + 170, 140, 36, 6, fill="rgba(10,8,7,0.35)"))
        out.append("</g>")
    return "".join(out)


def m_camera(rng, a, b):
    cx, cy = W / 2, H / 2 + 10
    bw, bh = 460, 280
    x, y = cx - bw / 2, cy - bh / 2
    out = [rrect(x, y, bw, bh, 26, fill="rgba(244,236,221,0.04)", stroke=a, sw=2.4)]
    # top strip
    out.append(rrect(x + 40, y - 26, 150, 34, 8, fill="rgba(230,180,80,0.10)", stroke=a, sw=1.8))
    # lens
    out.append(circle(cx, cy + 14, 92, stroke=a, w=2.4))
    out.append(circle(cx, cy + 14, 64, stroke=a, w=1.8, opacity=.7))
    out.append(circle(cx, cy + 14, 34, fill="rgba(230,180,80,0.12)", stroke=a, w=1.6))
    out.append(circle(cx - 18, cy - 6, 12, fill=CREAM, opacity=.5))
    # viewfinder + flash
    out.append(rrect(x + 32, y + 28, 70, 46, 8, stroke=a, sw=1.8, opacity=.8))
    out.append(circle(x + bw - 70, y + 52, 22, stroke=a, w=1.8, fill="rgba(244,236,221,0.10)"))
    out.append(rrect(x + bw - 150, y + bh - 60, 70, 26, 6, fill=a, opacity=.5))
    return "".join(out)


def m_halation(rng, a, b):
    cx, cy = W * .54, H * .48
    out = [circle(cx, cy, 240, fill="url(#bloom)")]
    for i, rr in enumerate((40, 78, 120, 170)):
        out.append(circle(cx, cy, rr, stroke=a, w=2.2 - i * .4, opacity=.7 - i * .14))
    out.append(circle(cx, cy, 16, fill=CREAM))
    # streaks
    for ang in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        x2 = cx + 300 * math.cos(ang)
        y2 = cy + 300 * math.sin(ang)
        out.append(line(cx, cy, x2, y2, a, 1.4, .25))
    return "".join(out)


def m_clock(rng, a, b):
    cx, cy = W / 2, H / 2
    R = 190
    out = [circle(cx, cy, R, stroke=a, w=2.4)]
    out.append(circle(cx, cy, R + 22, stroke=a, w=1, opacity=.22))
    for i in range(60):
        ang = i * math.tau / 60 - math.pi / 2
        r1 = R - (16 if i % 5 == 0 else 8)
        out.append(line(cx + r1 * math.cos(ang), cy + r1 * math.sin(ang),
                        cx + R * math.cos(ang), cy + R * math.sin(ang),
                        a, 2 if i % 5 == 0 else 1, .8 if i % 5 == 0 else .4))
    # remaining-time arc
    a0, a1 = -math.pi / 2, -math.pi / 2 + math.radians(rng.uniform(120, 250))
    out.append(f'<path d="M {_f(cx)} {_f(cy-R+30)} A {_f(R-30)} {_f(R-30)} 0 '
               f'{1 if (a1-a0)>math.pi else 0} 1 '
               f'{_f(cx+(R-30)*math.cos(a1))} {_f(cy+(R-30)*math.sin(a1))}" '
               f'fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round" opacity=".9"/>')
    # hands
    out.append(line(cx, cy, cx, cy - 110, CREAM, 4, .9))
    out.append(line(cx, cy, cx + 86, cy + 30, CREAM, 3, .7))
    out.append(circle(cx, cy, 7, fill=a))
    return "".join(out)


def m_envelope(rng, a, b):
    cx, cy = W / 2, H / 2
    ew, eh = 420, 280
    x, y = cx - ew / 2, cy - eh / 2
    out = [rrect(x, y, ew, eh, 14, fill="rgba(244,236,221,0.04)", stroke=a, sw=2.4)]
    out.append(f'<path d="M{_f(x)} {_f(y+8)} L{_f(cx)} {_f(cy+30)} L{_f(x+ew)} {_f(y+8)}" '
               f'fill="none" stroke="{a}" stroke-width="2.2" opacity=".85"/>')
    out.append(f'<path d="M{_f(x)} {_f(y+eh-8)} L{_f(cx-60)} {_f(cy+10)}" stroke="{a}" '
               f'stroke-width="1.6" opacity=".4"/>')
    out.append(f'<path d="M{_f(x+ew)} {_f(y+eh-8)} L{_f(cx+60)} {_f(cy+10)}" stroke="{a}" '
               f'stroke-width="1.6" opacity=".4"/>')
    # Daybreak wax seal
    out.append(circle(cx, cy + 34, 30, fill="rgba(230,180,80,0.16)", stroke=a, w=1.6))
    out.append(f'<g transform="translate({_f(cx-15)} {_f(cy+19)}) scale(0.3)">{MARK}</g>')
    return "".join(out)


def m_route(rng, a, b):
    pts = [(160, 470), (430, 300), (700, 410), (1010, 200)]
    d = f"M{pts[0][0]} {pts[0][1]} "
    for i in range(1, len(pts)):
        px, py = pts[i - 1]
        x, y = pts[i]
        mx = (px + x) / 2
        d += f"C {mx} {py} {mx} {y} {x} {y} "
    out = [f'<path d="{d}" fill="none" stroke="{a}" stroke-width="2.6" '
           f'stroke-dasharray="2 14" stroke-linecap="round" opacity=".9"/>']
    for i, (x, y) in enumerate(pts):
        big = i == 0 or i == len(pts) - 1
        out.append(f'<g transform="translate({x} {y})">')
        out.append(circle(0, -2, 16 if big else 11, fill="rgba(10,8,7,0.9)", stroke=a, w=2.2))
        out.append(circle(0, -2, 4, fill=a))
        out.append("</g>")
    return "".join(out)


def m_printer(rng, a, b):
    cx = W / 2
    # slot
    out = [rrect(cx - 280, 150, 560, 40, 12, fill="rgba(244,236,221,0.05)", stroke=a, sw=2)]
    out.append(line(cx - 250, 170, cx + 250, 170, a, 1.4, .4))
    # emerging print
    px, py, pw, ph = cx - 170, 200, 340, 300
    out.append(rrect(px, py, pw, ph, 8, fill=CREAM, opacity=.10))
    out.append(rrect(px, py, pw, ph, 8, stroke=CREAM, sw=1.6, opacity=.5))
    out.append(rrect(px + 22, py + 22, pw - 44, ph - 90, 4, fill=a, opacity=.16))
    out.append(rrect(px + 22, py + 22, pw - 44, ph - 90, 4, stroke=a, sw=1.2, opacity=.5))
    return "".join(out)


def m_contactsheet(rng, a, b):
    cols, rows = 5, 3
    gw, gh = 180, 130
    gap = 16
    tw = cols * gw + (cols - 1) * gap
    th = rows * gh + (rows - 1) * gap
    ox, oy = (W - tw) / 2, (H - th) / 2
    out = []
    hot = {(rng.randint(0, cols - 1), rng.randint(0, rows - 1)) for _ in range(3)}
    for r in range(rows):
        for c in range(cols):
            x = ox + c * (gw + gap)
            y = oy + r * (gh + gap)
            on = (c, r) in hot
            out.append(rrect(x, y, gw, gh, 6,
                             fill=(a if on else "rgba(244,236,221,0.04)"),
                             opacity=(.16 if on else 1),
                             stroke=a, sw=1.6))
            out.append(rrect(x, y, gw, gh, 6, stroke=a, sw=1.6, opacity=.6 if on else .4))
            # sprocket dots
            for k in range(4):
                hx = x + 16 + k * (gw - 32) / 3
                out.append(circle(hx, y - 7, 2.4, fill=a, opacity=.4))
    return "".join(out)


def m_rings(rng, a, b):
    cx, cy = W / 2, H / 2
    d = 95
    out = [circle(cx - d, cy, 150, stroke=a, w=2.6, opacity=.9),
           circle(cx + d, cy, 150, stroke=CREAM, w=2.2, opacity=.6),
           circle(cx - d, cy, 150, fill="url(#bloom)", opacity=.3)]
    # Daybreak at the overlap
    out.append(f'<g transform="translate({_f(cx-22)} {_f(cy-22)}) scale(0.44)">{MARK}</g>')
    return "".join(out)


def m_horizon(rng, a, b):
    out = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#leak)"/>']
    hy = H * .62
    out.append(circle(W * .5, hy - 30, 120, fill="url(#bloom)", opacity=.9))
    out.append(circle(W * .5, hy - 30, 120, stroke=a, w=1.8, opacity=.5))
    out.append(line(0, hy, W, hy, a, 1.6, .5))
    for i in range(5):
        yy = hy + 24 + i * 22
        out.append(line(W * .5 - (60 + i * 70), yy, W * .5 + (60 + i * 70), yy, a, 1.2, .3 - i * .04))
    return "".join(out)


def m_prism(rng, a, b):
    cx, cy = W / 2, H / 2
    # incoming beam
    out = [line(120, cy - 70, cx - 70, cy, CREAM, 2.4, .7)]
    # triangle
    tri = f"{_f(cx)},{_f(cy-90)} {_f(cx-78)},{_f(cy+70)} {_f(cx+78)},{_f(cy+70)}"
    out.append(f'<polygon points="{tri}" fill="rgba(244,236,221,0.05)" stroke={chr(34)}{CREAM}{chr(34)} stroke-width="2" opacity=".7"/>')
    # split bands
    bands = ["#F0CF8C", a, "#D9663C", b, "#8A6BA0", "#6E84A3"]
    for i, col in enumerate(bands):
        ay = cy - 30 + i * 16
        out.append(line(cx + 40, cy, 1080, ay, col, 5, .8))
    return "".join(out)


def m_hourglass(rng, a, b):
    cx, cy = W / 2, H / 2
    top = f"M{cx-130} {cy-150} L{cx+130} {cy-150} L{cx+8} {cy} L{cx-8} {cy} Z"
    bot = f"M{cx-8} {cy} L{cx+8} {cy} L{cx+130} {cy+150} L{cx-130} {cy+150} Z"
    out = [f'<path d="{top}" fill="rgba(230,180,80,0.05)" stroke="{a}" stroke-width="2.4"/>',
           f'<path d="{bot}" fill="rgba(230,180,80,0.05)" stroke="{a}" stroke-width="2.4"/>']
    out.append(f'<path d="M{cx-118} {cy-138} L{cx+118} {cy-138} L{cx+4} {cy-14} L{cx-4} {cy-14} Z" fill="{a}" opacity=".22"/>')
    out.append(f'<path d="M{cx-90} {cy+138} L{cx+90} {cy+138} L{cx+4} {cy+70} L{cx-4} {cy+70} Z" fill="{a}" opacity=".3"/>')
    for i in range(7):
        out.append(circle(cx + rng.uniform(-3, 3), cy + 8 + i * 16, 2.4, fill=a, opacity=.7))
    out.append(line(cx - 150, cy - 150, cx + 150, cy - 150, a, 3, .9))
    out.append(line(cx - 150, cy + 150, cx + 150, cy + 150, a, 3, .9))
    return "".join(out)


def m_sparkburst(rng, a, b):
    cx, cy = W / 2, H / 2
    out = [circle(cx, cy, 210, fill="url(#bloom)", opacity=.5)]
    n = 22
    for i in range(n):
        ang = i * math.tau / n + rng.uniform(-.04, .04)
        r0 = 70
        r1 = 150 + (70 if i % 2 == 0 else 0) + rng.uniform(0, 30)
        out.append(line(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang),
                        cx + r1 * math.cos(ang), cy + r1 * math.sin(ang),
                        a, 2 if i % 2 == 0 else 1.2, .8 if i % 2 == 0 else .4))
    out.append(f'<g transform="translate({_f(cx-44)} {_f(cy-44)}) scale(0.88)">{MARK}</g>')
    return "".join(out)


MOTIFS = {
    "filmstrip": m_filmstrip, "reel": m_reel, "aperture": m_aperture,
    "lightleak": m_lightleak, "grainfield": m_grainfield, "developtray": m_developtray,
    "swatches": m_swatches, "camera": m_camera, "halation": m_halation, "clock": m_clock,
    "envelope": m_envelope, "route": m_route, "printer": m_printer,
    "contactsheet": m_contactsheet, "rings": m_rings, "horizon": m_horizon,
    "prism": m_prism, "hourglass": m_hourglass, "sparkburst": m_sparkburst,
}


# ----------------------------------------------------------------------------- assembly
def cover_svg(slug, motif, accent="#E6B450", accent2="#C8852F"):
    rng = rng_for(slug)
    fn = MOTIFS.get(motif, m_grainfield)
    glow_x = rng.uniform(38, 62)
    defs = f'''<defs>
    <radialGradient id="glow" cx="{_f(glow_x)}%" cy="20%" r="90%">
      <stop offset="0%" stop-color="#1B140C"/>
      <stop offset="46%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="#060504"/>
    </radialGradient>
    <radialGradient id="bloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.55"/>
      <stop offset="55%" stop-color="{accent}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="leak" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{accent2}" stop-opacity="0.30"/>
      <stop offset="40%" stop-color="{BG}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#060504" stop-opacity="0.1"/>
    </linearGradient>
    <linearGradient id="vgrain" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{accent2}" stop-opacity="0.22"/>
      <stop offset="60%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="#060504"/>
    </linearGradient>
    <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/></filter>
  </defs>'''
    body = fn(rng, accent, accent2)
    return f'''<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img">
  {defs}
  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>
  {body}
  <rect x="0" y="0" width="{W}" height="{H}" filter="url(#grain)" opacity="0.05" style="mix-blend-mode:overlay"/>
  <rect x="14" y="14" width="{W-28}" height="{H-28}" rx="20" fill="none" stroke="{HAIR}" stroke-width="1"/>
  <g transform="translate({W-60} {H-60}) scale(0.30)" opacity="0.9">{MARK}</g>
</svg>'''


# small in-content divider (film strip) — reused inside articles
def divider_svg(accent="#E6B450"):
    holes = "".join(
        f'<rect x="{14+i*36}" y="4" width="20" height="10" rx="2.5" fill="none" stroke="{accent}" stroke-width="1.2" opacity="0.55"/>'
        for i in range(8))
    holes2 = holes.replace('y="4"', 'y="34"')
    return (f'<svg viewBox="0 0 300 48" xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="6" y="0" width="288" height="48" rx="6" fill="none" stroke="{accent}" stroke-width="1.4" opacity="0.5"/>'
            f'{holes}{holes2}'
            f'<g transform="translate(138 12) scale(0.24)">{MARK}</g>'
            f'</svg>')
