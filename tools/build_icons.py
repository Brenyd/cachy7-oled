#!/usr/bin/env python3
"""Cachy7 icon theme: Win7-flavoured glossy icons (scalable, 48px grid).
Inherits breeze-dark for everything not drawn here."""
import math
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import Doc, f  # noqa: E402

OUT = (sys.argv[1] if len(sys.argv) > 1 else "/home/claude/Cachy7-OLED") + "/icons/Cachy7/"


def save(cat, names, d):
    text = d.svg(48, 48)
    first = None
    for n in names if isinstance(names, (list, tuple)) else [names]:
        p = os.path.join(OUT, "scalable", cat, n + ".svg")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(text)
        first = first or p
    return first


def lg(d, stops, x1=0, y1=0, x2=0, y2=48):
    return d.grad([(o, c, a) for o, c, a in stops], x1, y1, x2, y2)


def S(c, a=1):
    return (c, a)


def stops(*pairs):
    out = []
    for p in pairs:
        o, c = p[0], p[1]
        a = p[2] if len(p) > 2 else 1
        out.append((o, c, a))
    return out


# ---------------------------------------------------------------------------
# shared pieces
# ---------------------------------------------------------------------------

def shadow(d, cx=24, cy=44, rx=19, ry=2.6, a=0.45):
    g = d.rgrad([(0, "#000000", a), (1, "#000000", 0)], cx, cy, rx,
                transform=f"translate({cx} {cy}) scale(1 {f(ry/rx)}) translate({-cx} {-cy})")
    d.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{g}"/>')


def paper(d, x, y, w, h, rot=0, lines=True):
    g = lg(d, stops((0, "#ffffff"), (1, "#dfe3e8")), 0, y, 0, y + h)
    t = f' transform="rotate({rot} {f(x+w/2)} {f(y+h/2)})"' if rot else ""
    s = f'<g{t}><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="0.6" fill="#7a7f87" fill-opacity="0.5"/>'
    s += f'<rect x="{f(x+0.5)}" y="{f(y+0.5)}" width="{f(w-1)}" height="{f(h-1)}" fill="{g}"/>'
    if lines:
        yy = y + 3
        while yy < y + h - 2.5:
            s += f'<rect x="{f(x+3)}" y="{f(yy)}" width="{f(w-6)}" height="0.8" fill="#8fa6c2" fill-opacity="0.75"/>'
            yy += 2.4
    s += "</g>"
    d.add(s)


def folder_back(d):
    g = lg(d, stops((0, "#e8b84a"), (1, "#b07a1c")), 0, 7, 0, 42)
    d.add(
        f'<path d="M6,7.5 h11 a1.5,1.5 0 0 1 1.2,0.6 l2.4,3 h20.9 a2,2 0 0 1 2,2 v26.4 a2,2 0 0 1 -2,2 '
        f'h-35.5 a2,2 0 0 1 -2,-2 v-30 a2,2 0 0 1 2,-2 z" fill="#6b4608"/>'
    )
    d.add(
        f'<path d="M6.3,8.3 h10.5 a1.2,1.2 0 0 1 1,0.5 l2.5,3.1 h21.2 a1.4,1.4 0 0 1 1.4,1.4 v26.1 '
        f'a1.4,1.4 0 0 1 -1.4,1.4 h-35.2 a1.4,1.4 0 0 1 -1.4,-1.4 v-29.7 a1.4,1.4 0 0 1 1.4,-1.4 z" fill="{g}"/>'
    )
    d.add('<rect x="6.5" y="13.5" width="35" height="26" rx="1" fill="#5a3a06" fill-opacity="0.35"/>')


def folder_front(d, tint=None):
    top, mid, bot = ("#fde9ad", "#f4cb5d", "#dea12b") if not tint else tint
    g = lg(d, stops((0, top), (0.55, mid), (1, bot)), 0, 19, 0, 42)
    edge = "M4.5,18.8 h39 a1.6,1.6 0 0 1 1.6,1.8 l-1.9,18.6 a2,2 0 0 1 -2,1.8 h-34.4 a2,2 0 0 1 -2,-1.8 l-1.9,-18.6 a1.6,1.6 0 0 1 1.6,-1.8 z"
    d.add(f'<path d="{edge}" fill="#7d5309"/>')
    d.add(
        f'<path d="M4.7,19.6 h38.6 a1,1 0 0 1 1,1.1 l-1.85,18.4 a1.4,1.4 0 0 1 -1.4,1.3 h-34.1 '
        f'a1.4,1.4 0 0 1 -1.4,-1.3 l-1.85,-18.4 a1,1 0 0 1 1,-1.1 z" fill="{g}"/>'
    )
    gl = lg(d, stops((0, "#ffffff", 0.55), (1, "#ffffff", 0.0)), 0, 19.6, 0, 29)
    d.add(f'<path d="M4.9,20.2 h38.2 l-0.9,8.6 q-18,-2.6 -36.4,0 z" fill="{gl}"/>')
    d.add('<rect x="5.2" y="19.8" width="37.6" height="0.7" fill="#ffffff" fill-opacity="0.85"/>')


def emblem_badge(d, cx, cy, r, c1, c2):
    g = d.rgrad([(0, c1, 1), (1, c2, 1)], cx, cy - r * 0.4, r * 1.3)
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r+0.8)}" fill="#000000" fill-opacity="0.35"/>')
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/>')
    gl = lg(d, stops((0, "#ffffff", 0.75), (1, "#ffffff", 0)), 0, cy - r, 0, cy)
    d.add(f'<ellipse cx="{f(cx)}" cy="{f(cy-r*0.45)}" rx="{f(r*0.78)}" ry="{f(r*0.5)}" fill="{gl}"/>')


def globe(d, cx, cy, r):
    g = d.rgrad([(0, "#9fe0ff", 1), (0.55, "#2b8be0", 1), (1, "#0b3c8a", 1)], cx - r * 0.3, cy - r * 0.35, r * 1.35)
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r+0.6)}" fill="#062a5c"/>')
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/>')
    k = r / 10.0
    land = lg(d, stops((0, "#a8ef6b"), (1, "#2f9b2f")), 0, cy - r, 0, cy + r)

    def P(x, y):
        return f"{f(cx + x*k)},{f(cy + y*k)}"
    d.add(
        f'<path d="M{P(-7,-5)} C{P(-4,-8)} {P(-1,-7)} {P(0,-5)} C{P(1,-3)} {P(-2,-2)} {P(-1,0)} '
        f'C{P(0,2)} {P(-3,4)} {P(-4,7)} C{P(-7,4)} {P(-9,-1)} {P(-7,-5)} Z" fill="{land}"/>'
    )
    d.add(
        f'<path d="M{P(2,-8)} C{P(5,-8)} {P(8,-5)} {P(8,-2)} C{P(6,-1)} {P(5,1)} {P(6,3)} '
        f'C{P(5,6)} {P(2,7)} {P(2,4)} C{P(3,2)} {P(1,0)} {P(2,-2)} C{P(3,-4)} {P(1,-6)} {P(2,-8)} Z" fill="{land}"/>'
    )
    gl = lg(d, stops((0, "#ffffff", 0.7), (1, "#ffffff", 0)), 0, cy - r, 0, cy + r * 0.1)
    d.add(f'<ellipse cx="{f(cx)}" cy="{f(cy-r*0.42)}" rx="{f(r*0.72)}" ry="{f(r*0.48)}" fill="{gl}"/>')


def house(d, cx, cy, s, color="#ffffff"):
    def P(x, y):
        return f"{f(cx+x*s)},{f(cy+y*s)}"
    d.add(
        f'<path d="M{P(0,-5)} L{P(5.5,0)} L{P(4,0)} L{P(4,4.5)} L{P(1.3,4.5)} L{P(1.3,1.5)} L{P(-1.3,1.5)} '
        f'L{P(-1.3,4.5)} L{P(-4,4.5)} L{P(-4,0)} L{P(-5.5,0)} Z" fill="{color}"/>'
    )


def person(d, cx, cy, s, color="#ffffff", a=1):
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy-2.6*s)}" r="{f(2.4*s)}" fill="{color}" fill-opacity="{a}"/>')
    d.add(
        f'<path d="M{f(cx-4.6*s)},{f(cy+4.6*s)} C{f(cx-4.6*s)},{f(cy+0.3*s)} {f(cx-2.5*s)},{f(cy-0.2*s)} {f(cx)},{f(cy-0.2*s)} '
        f'C{f(cx+2.5*s)},{f(cy-0.2*s)} {f(cx+4.6*s)},{f(cy+0.3*s)} {f(cx+4.6*s)},{f(cy+4.6*s)} Z" fill="{color}" fill-opacity="{a}"/>'
    )


def down_arrow(d, cx, cy, s):
    g = lg(d, stops((0, "#b9f58a"), (0.5, "#4cc93c"), (1, "#1f8a22")), 0, cy - 6 * s, 0, cy + 6 * s)

    def P(x, y):
        return f"{f(cx+x*s)},{f(cy+y*s)}"
    path = f"M{P(-2.6,-6)} L{P(2.6,-6)} L{P(2.6,0)} L{P(6,0)} L{P(0,6.5)} L{P(-6,0)} L{P(-2.6,0)} Z"
    d.add(f'<path d="{path}" fill="none" stroke="#0d4a10" stroke-width="1.6" stroke-linejoin="round"/>')
    d.add(f'<path d="{path}" fill="{g}"/>')
    d.add(f'<path d="M{P(-2,-5.4)} L{P(2,-5.4)} L{P(2,-1)} L{P(-2,-1)} Z" fill="#ffffff" fill-opacity="0.35"/>')


def music_note(d, cx, cy, s, color):
    d.add(
        f'<path d="M{f(cx-1*s)},{f(cy+3*s)} V{f(cy-5*s)} L{f(cx+5*s)},{f(cy-6.5*s)} V{f(cy+1.8*s)}" '
        f'fill="none" stroke="{color}" stroke-width="{f(1.3*s)}"/>'
    )
    d.add(f'<ellipse cx="{f(cx-2.6*s)}" cy="{f(cy+3.2*s)}" rx="{f(2*s)}" ry="{f(1.5*s)}" fill="{color}"/>')
    d.add(f'<ellipse cx="{f(cx+3.4*s)}" cy="{f(cy+2*s)}" rx="{f(2*s)}" ry="{f(1.5*s)}" fill="{color}"/>')


def disc(d, cx, cy, r):
    g = d.rgrad([(0, "#ffffff", 1), (0.45, "#d7dde6", 1), (1, "#9aa6b5", 1)], cx - r * 0.3, cy - r * 0.3, r * 1.4)
    rb = d.grad(
        [(0, "#ff9ad5", 0.0), (0.35, "#8fd3ff", 0.55), (0.5, "#b9ff9a", 0.5), (0.65, "#ffe28a", 0.55), (1, "#ff9ad5", 0.0)],
        cx - r, cy - r, cx + r, cy + r,
    )
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r+0.5)}" fill="#5c6673"/>')
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/>')
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{rb}"/>')
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.3)}" fill="#e9edf2" stroke="#8b96a3" stroke-width="0.6"/>')
    d.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.12)}" fill="#3b4048"/>')


def photo(d, x, y, w, h, rot):
    t = f' transform="rotate({rot} {f(x+w/2)} {f(y+h/2)})"'
    sky = lg(d, stops((0, "#2a7fe0"), (1, "#a9dcff")), 0, y, 0, y + h)
    hill = lg(d, stops((0, "#8fe05a"), (1, "#2c8a2a")), 0, y + h * 0.5, 0, y + h)
    s = f'<g{t}><rect x="{f(x-0.5)}" y="{f(y-0.5)}" width="{f(w+1)}" height="{f(h+1)}" fill="#6e7680" fill-opacity="0.6"/>'
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="#ffffff"/>'
    ix, iy, iw, ih = x + 1.5, y + 1.5, w - 3, h - 3
    s += f'<rect x="{f(ix)}" y="{f(iy)}" width="{f(iw)}" height="{f(ih)}" fill="{sky}"/>'
    s += f'<circle cx="{f(ix+iw*0.75)}" cy="{f(iy+ih*0.28)}" r="{f(ih*0.13)}" fill="#fff6b0"/>'
    s += (f'<path d="M{f(ix)},{f(iy+ih*0.72)} Q{f(ix+iw*0.3)},{f(iy+ih*0.45)} {f(ix+iw*0.55)},{f(iy+ih*0.68)} '
          f'T{f(ix+iw)},{f(iy+ih*0.6)} V{f(iy+ih)} H{f(ix)} Z" fill="{hill}"/>')
    s += "</g>"
    d.add(s)


def film(d, x, y, w, h, rot):
    t = f' transform="rotate({rot} {f(x+w/2)} {f(y+h/2)})"'
    s = f'<g{t}><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="0.8" fill="#1d2127"/>'
    fr = lg(d, stops((0, "#5ab2ff"), (1, "#1b4f9c")), 0, y, 0, y + h)
    s += f'<rect x="{f(x+3)}" y="{f(y+2)}" width="{f(w-6)}" height="{f(h-4)}" fill="{fr}"/>'
    yy = y + 1.2
    while yy < y + h - 1.5:
        s += f'<rect x="{f(x+0.8)}" y="{f(yy)}" width="1.4" height="1.2" fill="#e9edf2"/>'
        s += f'<rect x="{f(x+w-2.2)}" y="{f(yy)}" width="1.4" height="1.2" fill="#e9edf2"/>'
        yy += 2.6
    s += f'<path d="M{f(x+w/2-2)},{f(y+h/2-3)} L{f(x+w/2+3)},{f(y+h/2)} L{f(x+w/2-2)},{f(y+h/2+3)} Z" fill="#ffffff" fill-opacity="0.9"/>'
    s += "</g>"
    d.add(s)


def mini_screen(d, x, y, w, h):
    g = lg(d, stops((0, "#0b3c91"), (0.6, "#2c86e6"), (1, "#7fd0ff")), x, y, x + w, y + h)
    d.add(f'<rect x="{f(x-0.6)}" y="{f(y-0.6)}" width="{f(w+1.2)}" height="{f(h+1.2)}" rx="1" fill="#10151c"/>')
    d.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{g}"/>')
    d.add(f'<path d="M{f(x)},{f(y+h*0.7)} Q{f(x+w*0.5)},{f(y+h*0.2)} {f(x+w)},{f(y+h*0.35)} V{f(y+h*0.5)} '
          f'Q{f(x+w*0.5)},{f(y+h*0.4)} {f(x)},{f(y+h)} Z" fill="#ffffff" fill-opacity="0.3"/>')


# ---------------------------------------------------------------------------
# folders
# ---------------------------------------------------------------------------

def folder(content=None, emblem=None):
    d = Doc()
    shadow(d, 24, 42.6, 20, 2.2, 0.5)
    folder_back(d)
    if content == "docs":
        paper(d, 10, 11, 22, 18, -6)
        paper(d, 15, 10, 23, 19, 3)
    elif content == "pictures":
        paper(d, 10, 12, 22, 16, -4, lines=False)
        photo(d, 14, 8.5, 23, 17, 6)
    elif content == "music":
        paper(d, 9, 13, 24, 16, -3, lines=False)
        disc(d, 26, 17, 9.5)
    elif content == "videos":
        paper(d, 9, 13, 24, 16, -3, lines=False)
        film(d, 14, 9, 22, 15, -5)
    elif content == "desktop":
        mini_screen(d, 12, 10.5, 24, 15)
    else:
        paper(d, 10, 11.5, 28, 18, -2)
    folder_front(d)
    if emblem == "download":
        down_arrow(d, 24, 30.5, 1.05)
    elif emblem == "home":
        emblem_badge(d, 24, 30.5, 6.6, "#9fe3ff", "#1d73c9")
        house(d, 24, 30.2, 0.95)
    elif emblem == "network":
        globe(d, 24, 30.5, 6.4)
    elif emblem == "user":
        emblem_badge(d, 24, 30.5, 6.6, "#8ff0dc", "#118a78")
        person(d, 24, 31.2, 1.0)
    elif emblem == "music":
        music_note(d, 24, 30.5, 1.05, "#7a5208")
    return d


# ---------------------------------------------------------------------------
# devices / apps
# ---------------------------------------------------------------------------

def computer():
    d = Doc()
    shadow(d, 24, 44, 15, 2, 0.5)
    base = lg(d, stops((0, "#f4f6f8"), (1, "#8b949e")), 0, 38, 0, 44)
    d.add(f'<path d="M14,43.5 Q14,40 18,39.5 H30 Q34,40 34,43.5 Z" fill="{base}" stroke="#4b525b" stroke-width="0.6"/>')
    neck = lg(d, stops((0, "#5c636c"), (0.5, "#c9cfd6"), (1, "#5c636c")), 20, 0, 28, 0)
    d.add(f'<rect x="20.5" y="34" width="7" height="6" fill="{neck}"/>')
    bez = lg(d, stops((0, "#3a3f46"), (0.5, "#0d0f12"), (1, "#000000")), 0, 5, 0, 36)
    d.add('<rect x="3" y="5" width="42" height="31" rx="2.5" fill="#000000"/>')
    d.add(f'<rect x="3.6" y="5.6" width="40.8" height="29.8" rx="2" fill="{bez}"/>')
    scr = lg(d, stops((0, "#0a2d73"), (0.55, "#1e6fd0"), (1, "#69c3ff")), 6, 8, 42, 32)
    d.add(f'<rect x="6" y="8" width="36" height="24" fill="{scr}"/>')
    d.add('<path d="M6,26 Q20,12 42,15 V19 Q22,17 6,32 Z" fill="#ffffff" fill-opacity="0.28"/>')
    d.add('<path d="M6,30 Q24,18 42,22 V23.5 Q24,21 6,32 Z" fill="#19d3b4" fill-opacity="0.35"/>')
    gl = lg(d, stops((0, "#ffffff", 0.25), (1, "#ffffff", 0)), 0, 5, 0, 20)
    d.add(f'<path d="M3.6,7.6 a2,2 0 0 1 2,-2 h36.8 a2,2 0 0 1 2,2 v6 Q24,10 3.6,16 Z" fill="{gl}"/>')
    d.add('<circle cx="24" cy="34" r="0.6" fill="#5ad1ff"/>')
    return d


def trash(full=False):
    d = Doc()
    shadow(d, 24, 44, 14, 2.2, 0.5)
    body = lg(d, stops((0, "#cfe4f7", 0.55), (0.5, "#8fb3d6", 0.35), (1, "#5d82a8", 0.6)), 12, 0, 36, 0)
    if full:
        for (x, y, r, rot) in [(18, 12, 5, -10), (27, 11, 5.5, 15), (23, 8, 4.5, 0), (31, 14, 4, 30)]:
            g = lg(d, stops((0, "#ffffff"), (1, "#c9ced6")), 0, y - r, 0, y + r)
            d.add(f'<path transform="rotate({rot} {x} {y})" d="M{x-r},{y} q1,-{r} {r},-{r} q{r*0.8},0.5 {r},{r*0.6} '
                  f'q0.5,{r*0.9} -{r*0.9},{r*0.6} q-{r*0.7},0.6 -{r*1.1},-{r*0.6} z" fill="{g}" stroke="#8b93a0" stroke-width="0.5"/>')
    d.add(f'<path d="M11,12 H37 L34.2,42 a1.5,1.5 0 0 1 -1.5,1.3 H15.3 a1.5,1.5 0 0 1 -1.5,-1.3 Z" fill="{body}" stroke="#e8f3ff" stroke-opacity="0.85" stroke-width="0.8"/>')
    for i in range(6):
        x0 = 14.5 + i * 3.8
        x1 = 16.2 + i * 3.1
        d.add(f'<path d="M{f(x0)},14 L{f(x1)},41" stroke="#ffffff" stroke-opacity="0.35" stroke-width="0.9"/>')
    if full:
        d.add('<path d="M15,30 q4,-5 9,-1 q5,-4 9,1 l-0.9,10 h-16.2 z" fill="#ffffff" fill-opacity="0.55"/>')
    rim = lg(d, stops((0, "#ffffff"), (1, "#9fb8d0")), 0, 9, 0, 14)
    d.add(f'<ellipse cx="24" cy="12" rx="13.4" ry="2.6" fill="{rim}" stroke="#5d7894" stroke-width="0.7"/>')
    d.add('<ellipse cx="24" cy="12" rx="11.4" ry="1.6" fill="#36506b" fill-opacity="0.75"/>')
    gl = lg(d, stops((0, "#ffffff", 0.0), (0.3, "#ffffff", 0.55), (0.45, "#ffffff", 0)), 11, 0, 37, 0)
    d.add(f'<path d="M12,14 H36 L33.5,41 H14.5 Z" fill="{gl}"/>')
    return d


def harddisk():
    d = Doc()
    shadow(d, 24, 41, 20, 2.4, 0.5)
    top = lg(d, stops((0, "#ffffff"), (1, "#c3cad2")), 0, 13, 0, 25)
    d.add(f'<path d="M8,14 H40 L45,24 H3 Z" fill="{top}" stroke="#6c747e" stroke-width="0.7"/>')
    front = lg(d, stops((0, "#a8b1bb"), (0.5, "#6f7884"), (1, "#3f464f")), 0, 24, 0, 38)
    d.add(f'<path d="M3,24 H45 V36 a2,2 0 0 1 -2,2 H5 a2,2 0 0 1 -2,-2 Z" fill="{front}" stroke="#3a4048" stroke-width="0.7"/>')
    d.add('<rect x="6" y="28" width="26" height="1.2" fill="#2a2f35" fill-opacity="0.6"/>')
    d.add('<rect x="6" y="31" width="26" height="1.2" fill="#2a2f35" fill-opacity="0.6"/>')
    led = d.rgrad([(0, "#d6ffb0", 1), (1, "#33c22a", 1)], 39, 30.5, 2.2)
    d.add(f'<circle cx="39" cy="31" r="1.9" fill="{led}" stroke="#1d5e17" stroke-width="0.5"/>')
    d.add('<rect x="3.5" y="24.4" width="41" height="0.8" fill="#ffffff" fill-opacity="0.6"/>')
    return d


def usb():
    d = Doc()
    shadow(d, 24, 43, 12, 2, 0.5)
    body = lg(d, stops((0, "#4ea6ff"), (0.48, "#1d6fd0"), (0.5, "#0e4fa0"), (1, "#2b7fe0")), 14, 0, 34, 0)
    d.add('<rect x="18" y="4" width="12" height="11" rx="1" fill="#c9cfd6" stroke="#6c747e" stroke-width="0.7"/>')
    d.add('<rect x="20.5" y="7" width="2.5" height="2.5" fill="#5c636c"/><rect x="25" y="7" width="2.5" height="2.5" fill="#5c636c"/>')
    d.add(f'<rect x="14" y="14" width="20" height="28" rx="4" fill="{body}" stroke="#062f66" stroke-width="0.8"/>')
    d.add('<rect x="15.5" y="15.5" width="8" height="25" rx="3" fill="#ffffff" fill-opacity="0.22"/>')
    d.add('<circle cx="24" cy="36" r="1.4" fill="#9ff0ff"/>')
    return d


def optical():
    d = Doc()
    shadow(d, 24, 44, 16, 2, 0.45)
    disc(d, 24, 23.5, 19)
    return d


def terminal():
    d = Doc()
    shadow(d, 24, 44, 19, 2, 0.5)
    d.add('<rect x="3.5" y="7" width="41" height="34" rx="3" fill="#000000" stroke="#8fb6e0" stroke-opacity="0.6" stroke-width="0.8"/>')
    tb = lg(d, stops((0, "#5d6f88"), (0.48, "#2b3646"), (0.5, "#141a22"), (1, "#1e2836")), 0, 7, 0, 14)
    d.add(f'<path d="M3.9,10 a2.6,2.6 0 0 1 2.6,-2.6 h35 a2.6,2.6 0 0 1 2.6,2.6 v4 h-40.2 z" fill="{tb}"/>')
    d.add('<rect x="35" y="9" width="7" height="3.4" rx="0.8" fill="#c94b3a"/>')
    d.add('<path d="M9,20 L15,24 L9,28" fill="none" stroke="#3fe39f" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    d.add('<rect x="17" y="27" width="10" height="2.4" rx="0.6" fill="#e8eaed"/>')
    gl = lg(d, stops((0, "#ffffff", 0.12), (1, "#ffffff", 0)), 0, 14, 0, 30)
    d.add(f'<rect x="4" y="14" width="40" height="12" fill="{gl}"/>')
    return d


def gear_path(cx, cy, R, r, n, tooth=0.45):
    pts = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        da = 2 * math.pi / n
        for (a, rad) in [(a0, r), (a0 + da * (0.5 - tooth / 2) * 0.9, R), (a0 + da * (0.5 + tooth / 2) * 1.0, R), (a0 + da * 0.95, r)]:
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + " Z"


def settings():
    d = Doc()
    shadow(d, 24, 44, 18, 2, 0.5)
    tile = lg(d, stops((0, "#6fc0ff"), (0.48, "#2a7fd8"), (0.5, "#1563bd"), (1, "#2f8ef0")), 0, 4, 0, 42)
    d.add('<rect x="4" y="4" width="40" height="38" rx="6" fill="#06285a"/>')
    d.add(f'<rect x="4.8" y="4.8" width="38.4" height="36.4" rx="5.3" fill="{tile}"/>')
    metal = lg(d, stops((0, "#ffffff"), (0.5, "#cfd6de"), (1, "#7d8896")), 0, 10, 0, 38)
    gp = gear_path(24, 23.5, 13, 10, 10)
    d.add(f'<path d="{gp}" fill="#203247" fill-opacity="0.45" transform="translate(0.6 1)"/>')
    d.add(f'<path d="{gp} M30,23.5 a6,6 0 1 0 -12,0 a6,6 0 1 0 12,0 Z" fill-rule="evenodd" fill="{metal}" stroke="#55606d" stroke-width="0.6"/>')
    d.add('<circle cx="24" cy="23.5" r="3.4" fill="#19d3b4"/>')
    gl = lg(d, stops((0, "#ffffff", 0.5), (1, "#ffffff", 0)), 0, 5, 0, 22)
    d.add(f'<path d="M5,10 a5,5 0 0 1 5,-5 h28 a5,5 0 0 1 5,5 v6 Q24,12 5,20 Z" fill="{gl}"/>')
    return d


def file_manager():
    d = Doc()
    shadow(d, 24, 44, 19, 2.2, 0.5)
    # Explorer-style: folders standing in a glass holder
    g1 = lg(d, stops((0, "#f0c860"), (1, "#b07a1c")), 0, 6, 0, 30)
    g2 = lg(d, stops((0, "#fde9ad"), (1, "#e1a62e")), 0, 10, 0, 34)
    d.add(f'<path d="M9,10 h9 l2,2.5 h14 a1.5,1.5 0 0 1 1.5,1.5 V32 H7.5 V11.5 a1.5,1.5 0 0 1 1.5,-1.5 z" fill="{g1}" stroke="#6b4608" stroke-width="0.7"/>')
    d.add(f'<path d="M15,6 h9 l2,2.5 h14 a1.5,1.5 0 0 1 1.5,1.5 V30 H13.5 V7.5 a1.5,1.5 0 0 1 1.5,-1.5 z" fill="{g2}" stroke="#7d5309" stroke-width="0.7"/>')
    paper(d, 17, 11, 21, 14, 0)
    holder = lg(d, stops((0, "#bfe3ff", 0.75), (0.48, "#5aa7ec", 0.65), (0.5, "#2f7fd2", 0.75), (1, "#1a5fb0", 0.9)), 0, 24, 0, 42)
    d.add(f'<path d="M4,24 H44 L41.5,41 a2,2 0 0 1 -2,1.7 H8.5 a2,2 0 0 1 -2,-1.7 Z" fill="{holder}" stroke="#0b3a7a" stroke-width="0.8"/>')
    d.add('<rect x="5" y="24.6" width="38" height="0.9" fill="#ffffff" fill-opacity="0.8"/>')
    return d


def browser():
    d = Doc()
    shadow(d, 24, 44, 15, 2, 0.5)
    globe(d, 24, 23, 19)
    return d


def network():
    d = Doc()
    shadow(d, 24, 44, 19, 2, 0.5)
    globe(d, 24, 18, 13)
    for x in (6, 30):
        mini_screen(d, x + 1, 30, 11, 7.5)
    d.add('<path d="M12.5,30 V27 H35.5 V30" fill="none" stroke="#9fb8d0" stroke-width="1.2"/>')
    return d


def user_identity():
    d = Doc()
    shadow(d, 24, 44, 17, 2, 0.5)
    frame = lg(d, stops((0, "#ffffff"), (1, "#aeb7c2")), 0, 4, 0, 44)
    d.add(f'<rect x="4" y="4" width="40" height="40" rx="4" fill="{frame}" stroke="#4b525b" stroke-width="0.7"/>')
    bg = lg(d, stops((0, "#1fe0c0"), (0.6, "#0d8f9a"), (1, "#0b3c74")), 0, 7, 0, 41)
    d.add(f'<rect x="7" y="7" width="34" height="34" rx="2" fill="{bg}"/>')
    person(d, 24, 28, 2.5, "#ffffff", 0.92)
    d.add('<path d="M7,9 a2,2 0 0 1 2,-2 h30 a2,2 0 0 1 2,2 v8 Q24,12 7,22 Z" fill="#ffffff" fill-opacity="0.25"/>')
    return d


def text_generic():
    d = Doc()
    shadow(d, 24, 44.5, 13, 1.6, 0.4)
    g = lg(d, stops((0, "#ffffff"), (1, "#dfe3e8")), 0, 3, 0, 44)
    d.add(f'<path d="M10,3.5 H31 L39,11.5 V43.5 H10 Z" fill="{g}" stroke="#7a7f87" stroke-width="0.8"/>')
    d.add('<path d="M31,3.5 V11.5 H39 Z" fill="#c4cad2" stroke="#7a7f87" stroke-width="0.8" stroke-linejoin="round"/>')
    for i in range(10):
        wdt = 22 if i % 4 != 3 else 14
        d.add(f'<rect x="13.5" y="{f(15 + i*2.6)}" width="{wdt}" height="1" fill="#6f8fb5" fill-opacity="0.8"/>')
    return d


def orb_fallback():
    """Used as start-here when no distro logo is found on the system."""
    d = Doc()
    body = d.rgrad([(0, "#20303f", 1), (0.7, "#05080b", 1), (1, "#000000", 1)], 24, 30, 22)
    d.add('<circle cx="24" cy="24" r="22" fill="#000000"/>')
    d.add(f'<circle cx="24" cy="24" r="21" fill="{body}"/>')
    rim = d.rgrad([(0.75, "#19d3b4", 0), (0.97, "#19d3b4", 0.9), (1, "#3b8eea", 0)], 24, 24, 21)
    d.add(f'<circle cx="24" cy="24" r="21" fill="{rim}"/>')
    d.add('<path d="M24,13 a11,11 0 1 0 9.5,5.5" fill="none" stroke="#19d3b4" stroke-width="3.2" stroke-linecap="round"/>')
    d.add('<circle cx="35.5" cy="13.5" r="2" fill="#3b8eea"/><circle cx="31" cy="9.5" r="1.3" fill="#19d3b4"/>')
    gl = lg(d, stops((0, "#ffffff", 0.55), (1, "#ffffff", 0)), 0, 3, 0, 22)
    d.add(f'<ellipse cx="24" cy="13" rx="15" ry="9.5" fill="{gl}"/>')
    return d


INDEX = """[Icon Theme]
Name=Cachy7
Comment=Windows 7 inspired glossy icons for the Cachy7 OLED theme
Inherits=breeze-dark,breeze,hicolor
Example=folder
DisplayDepth=32
LinkOverlay=link
LockOverlay=lockoverlay
ZipOverlay=zipoverlay
DesktopDefault=48
ToolbarDefault=22
MainToolbarDefault=22
SmallDefault=16
PanelDefault=48
DialogDefault=32
FollowsColorScheme=false

Directories=scalable/places,scalable/devices,scalable/apps,scalable/mimetypes

[scalable/places]
Size=48
MinSize=16
MaxSize=512
Context=Places
Type=Scalable

[scalable/devices]
Size=48
MinSize=16
MaxSize=512
Context=Devices
Type=Scalable

[scalable/apps]
Size=48
MinSize=16
MaxSize=512
Context=Applications
Type=Scalable

[scalable/mimetypes]
Size=48
MinSize=16
MaxSize=512
Context=MimeTypes
Type=Scalable
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    with open(OUT + "index.theme", "w") as fh:
        fh.write(INDEX)
    save("places", ["folder", "folder-open", "folder-blue", "folder-yellow"], folder())
    save("mimetypes", ["inode-directory"], folder())
    save("places", ["folder-documents", "folder-text"], folder("docs"))
    save("places", ["folder-pictures", "folder-images"], folder("pictures"))
    save("places", ["folder-music", "folder-sound"], folder("music"))
    save("places", ["folder-videos", "folder-video"], folder("videos"))
    save("places", ["folder-download", "folder-downloads"], folder(None, "download"))
    save("places", ["user-desktop", "folder-desktop"], folder("desktop"))
    save("places", ["user-home", "folder-home"], folder("docs", "home"))
    save("places", ["folder-remote", "folder-network", "folder-publicshare"], folder(None, "network"))
    save("places", ["user-trash", "trash-empty"], trash(False))
    save("places", ["user-trash-full", "trash-full"], trash(True))
    save("places", ["network-workgroup", "network-server"], network())
    save("places", ["start-here", "start-here-kde", "start-here-kde-plasma", "distributor-logo"], orb_fallback())
    save("devices", ["computer", "computer-laptop"], computer())
    save("devices", ["drive-harddisk", "drive-harddisk-root", "drive-harddisk-solidstate"], harddisk())
    save("devices", ["drive-removable-media", "drive-removable-media-usb", "drive-removable-media-usb-pendrive", "media-flash"], usb())
    save("devices", ["media-optical", "drive-optical", "media-optical-audio"], optical())
    save("apps", ["utilities-terminal", "org.kde.konsole", "konsole", "terminal"], terminal())
    save("apps", ["preferences-system", "systemsettings"], settings())
    save("apps", ["system-file-manager", "org.kde.dolphin", "dolphin"], file_manager())
    save("apps", ["internet-web-browser", "web-browser"], browser())
    save("apps", ["user-identity", "system-users"], user_identity())
    save("mimetypes", ["text-x-generic", "text-plain", "application-text"], text_generic())
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("icons written:", n)


if __name__ == "__main__":
    main()
