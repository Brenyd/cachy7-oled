#!/usr/bin/env python3
"""Cachy7 app icons: Win7-era glossy dark tiles with bright, 80s-style striped
emblems. Every emblem is an original pictogram of what the app does - no
brand logos are reproduced.

Output: icons/Cachy7/scalable/apps/<icon-name>.svg for every icon name an app
uses, plus cachy7-app-<slug>.svg for apps whose .desktop file points at an
image path (those get re-pointed by the installer)."""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Doc, f  # noqa: E402

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
THEME = os.path.join(ROOT, "icons/Cachy7-Apps")
OUT = os.path.join(THEME, "scalable/apps")

INDEX = """[Icon Theme]
Name=Cachy7 Apps
Comment=Cachy7 icons plus Win7-era glossy app icons
Inherits=Cachy7,breeze-dark,breeze,hicolor
Example=steam
DisplayDepth=32
FollowsColorScheme=false

Directories=scalable/apps

[scalable/apps]
Size=48
MinSize=16
MaxSize=512
Context=Applications
Type=Scalable
"""

# ---------------------------------------------------------------------------
# palettes: hard-edged horizontal stripes, top to bottom
# ---------------------------------------------------------------------------
PAL = {
    "rainbow": ["#61bb46", "#fdb827", "#f5821f", "#e03a3e", "#963d97", "#009ddc"],
    "sunset": ["#ffe14d", "#ffb13b", "#ff7a3d", "#f2445e", "#c2368f"],
    "ocean": ["#7cf3ff", "#3fc8ff", "#2e8bff", "#5b5bff", "#9a4dff"],
    "lime": ["#e8ff6a", "#9bef3f", "#34d17a", "#14b39a"],
    "fire": ["#fff06a", "#ffc23a", "#ff7f2a", "#f2382f"],
    "ice": ["#ffffff", "#cff4ff", "#8fd8ff", "#5aa9ff"],
    "candy": ["#ff9ae6", "#ff5fc4", "#c94dff", "#7a5cff"],
    "gold": ["#fff3b0", "#ffd34d", "#f5a623", "#c77a12"],
    "mint": ["#cffff0", "#7ff5d0", "#25d7b0", "#0fa3a0"],
    "silver": ["#ffffff", "#d9dee6", "#a9b3c1", "#7b8796"],
    "red": ["#ff9c8a", "#ff5a4e", "#e02b3a", "#a8122e"],
    "violet": ["#e9c6ff", "#c48bff", "#9a5cff", "#6a3de0"],
    "amber": ["#ffe9a8", "#ffc56b", "#f29a38", "#c86a1c"],
    "wood": ["#f2c48d", "#d99a5b", "#b8733a", "#8a5126"],
    "toxic": ["#f4ff7a", "#c6f53a", "#7fd61f", "#3fa12a"],
    "steel": ["#e6edf5", "#b7c4d4", "#8496ad", "#5a6b82"],
    "sky": ["#d9f6ff", "#9fe2ff", "#5cc4ff", "#2f95f0"],
    "pink": ["#ffd0e6", "#ff8fc1", "#ff4f9a", "#d6286f"],
}
ACCENT = {k: v[len(v) // 2] for k, v in PAL.items()}


class Icon:
    def __init__(self, a, b, accent=None):
        self.d = Doc()
        self.a_name, self.b_name = a, b
        self.accent = accent or ACCENT[a]
        self.A = self.stripes(PAL[a])
        self.B = self.stripes(PAL[b])

    def stripes(self, cols, y0=10, y1=40):
        n = len(cols)
        st = []
        for i, c in enumerate(cols):
            st.append((i / n, c, 1))
            st.append(((i + 1) / n - 0.0001, c, 1))
        return self.d.grad(st, 0, y0, 0, y1)

    def vgrad(self, c1, c2, y0, y1):
        return self.d.grad([(0, c1, 1), (1, c2, 1)], 0, y0, 0, y1)

    # draw a shape with the bold dark outline that makes the 80s look pop
    def s(self, path, fill, outline=True, w=2.2, extra=""):
        if outline:
            self.d.add(f'<path d="{path}" fill="none" stroke="#000000" stroke-opacity="0.85" '
                       f'stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')
        self.d.add(f'<path d="{path}" fill="{fill}" {extra}/>')

    def line(self, path, color, w=1.6, op=1.0, cap="round"):
        self.d.add(f'<path d="{path}" fill="none" stroke="{color}" stroke-opacity="{op}" '
                   f'stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"/>')

    def raw(self, s):
        self.d.add(s)


# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------
def R(x, y, w, h, r=0):
    if r <= 0:
        return f"M{f(x)},{f(y)} h{f(w)} v{f(h)} h{f(-w)} Z"
    r = min(r, w / 2, h / 2)
    return (f"M{f(x+r)},{f(y)} h{f(w-2*r)} a{f(r)},{f(r)} 0 0 1 {f(r)},{f(r)} v{f(h-2*r)} "
            f"a{f(r)},{f(r)} 0 0 1 {f(-r)},{f(r)} h{f(-(w-2*r))} a{f(r)},{f(r)} 0 0 1 {f(-r)},{f(-r)} "
            f"v{f(-(h-2*r))} a{f(r)},{f(r)} 0 0 1 {f(r)},{f(-r)} Z")


def C(cx, cy, r):
    return f"M{f(cx-r)},{f(cy)} a{f(r)},{f(r)} 0 1 0 {f(2*r)},0 a{f(r)},{f(r)} 0 1 0 {f(-2*r)},0 Z"


def E(cx, cy, rx, ry):
    return f"M{f(cx-rx)},{f(cy)} a{f(rx)},{f(ry)} 0 1 0 {f(2*rx)},0 a{f(rx)},{f(ry)} 0 1 0 {f(-2*rx)},0 Z"


def P(*pts):
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + " Z"


def star(cx, cy, ro, ri, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return P(*pts)


def gear(cx, cy, ro, ri, n=8, hole=0):
    pts = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        da = 2 * math.pi / n
        for a, r in ((a0, ri), (a0 + da * 0.18, ro), (a0 + da * 0.5, ro), (a0 + da * 0.68, ri)):
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    p = P(*pts)
    if hole:
        p += " " + C(cx, cy, hole)
    return p


# ---------------------------------------------------------------------------
# tile (Win7 glass on OLED black)
# ---------------------------------------------------------------------------
def tile_back(I):
    d = I.d
    sh = d.rgrad([(0, "#000000", 0.55), (1, "#000000", 0)], 24, 45, 20,
                 transform="translate(24 45) scale(1 0.14) translate(-24 -45)")
    d.add(f'<ellipse cx="24" cy="45" rx="20" ry="2.8" fill="{sh}"/>')
    body = I.vgrad("#1c2230", "#030406", 3, 45)
    d.add(f'<path d="{R(2.5,2.5,43,42,9.5)}" fill="#000000"/>')
    d.add(f'<path d="{R(3,3,42,41,9)}" fill="{body}"/>')
    glow = d.rgrad([(0, I.accent, 0.55), (1, I.accent, 0)], 24, 44, 24,
                   transform="translate(24 44) scale(1 0.6) translate(-24 -44)")
    d.add(f'<path d="{R(3,3,42,41,9)}" fill="{glow}"/>')
    rim = d.grad([(0, "#ffffff", 0.45), (0.5, "#ffffff", 0.08), (1, I.accent, 0.75)], 0, 3, 0, 44)
    d.add(f'<path d="{R(3,3,42,41,9)} {R(4,4,40,39,8)}" fill-rule="evenodd" fill="{rim}"/>')


def tile_front(I):
    d = I.d
    gl = d.grad([(0, "#ffffff", 0.30), (1, "#ffffff", 0.03)], 0, 4, 0, 22)
    d.add(f'<path d="M4,13 a9,9 0 0 1 9,-9 h22 a9,9 0 0 1 9,9 v6 Q24,15 4,23 Z" fill="{gl}"/>')


# ---------------------------------------------------------------------------
# emblems (all original pictograms)
# ---------------------------------------------------------------------------
def g_terminal(I, flash=False):
    I.s(R(9, 11, 30, 25, 3), "#06080b")
    I.s(R(9, 11, 30, 6, 3), I.A, outline=False)
    I.raw(f'<path d="{R(9,15,30,2)}" fill="#06080b"/>')
    I.s("M13,22 L19,25.5 L13,29", "none", outline=False)
    I.line("M13.5,22 L19,25.5 L13.5,29", "#000", 4.2)
    I.line("M13.5,22 L19,25.5 L13.5,29", I.B, 2.6)
    I.s(R(21, 28, 10, 2.6, 0.8), I.B)
    if flash:
        I.s(P((31, 18), (26, 27), (30, 27), (27, 35), (34, 24), (30, 24), (33, 18)), I.A)


def g_box(I, zip_=False, roller=False):
    I.s(R(10, 19, 28, 19, 2), I.A)
    I.s(P((8, 14), (40, 14), (38, 20), (10, 20)), I.B)
    if zip_:
        I.raw(f'<path d="{R(22.5,14,3,24)}" fill="#1a1a1a"/>')
        for y in range(16, 37, 3):
            I.raw(f'<path d="{R(21.5,y,5,1.2)}" fill="#e6e6e6"/>')
        I.s(R(21, 23, 6, 5, 1), "#d9dee6")
    if roller:
        I.s(R(14, 24, 20, 7, 3.5), "#d9dee6")
        I.line("M18,24 v7 M22,24 v7 M26,24 v7 M30,24 v7", "#7b8796", 1)


def g_wave(I, bars=(4, 9, 15, 11, 18, 8, 13, 6, 10, 4)):
    n = len(bars)
    w = 26 / n
    for i, h in enumerate(bars):
        x = 11 + i * w
        I.s(R(x + 0.4, 25 - h / 2, w - 0.8, h, (w - 0.8) / 2), I.A if i % 2 == 0 else I.B, w=1.6)


def g_d20(I):
    pts = [(24, 9), (37, 16.5), (37, 31.5), (24, 39), (11, 31.5), (11, 16.5)]
    I.s(P(*pts), I.A)
    I.s(P((24, 15), (32, 29), (16, 29)), I.B)
    I.line("M24,9 L24,15 M37,16.5 L32,29 M37,31.5 L32,29 M24,39 L32,29 M24,39 L16,29 M11,31.5 L16,29 M11,16.5 L16,29 M11,16.5 L24,15 M37,16.5 L24,15",
           "#000", 1.1, 0.7)
    I.raw('<text x="24" y="27.3" font-family="sans-serif" font-weight="900" font-size="7" text-anchor="middle" fill="#1a0f2a">20</text>')


def g_globe(I, ring=None):
    I.s(C(24, 24, 13), I.A)
    I.line("M11,24 H37 M24,11 V37", "#000", 1.2, 0.6)
    I.line("M24,11 C17,15 17,33 24,37 M24,11 C31,15 31,33 24,37", "#000", 1.2, 0.6)
    I.line("M13,17.5 H35 M13,30.5 H35", "#000", 1.2, 0.6)
    if ring == "orbit":
        I.line("M8,30 C14,40 38,32 40,18", "#000", 4, 0.9)
        I.line("M8,30 C14,40 38,32 40,18", I.B, 2.4)
        I.s(star(39.5, 18, 3.6, 1.5), I.B, w=1.4)
    elif ring == "chrome":
        I.raw(f'<path d="{C(24,24,15.5)} {C(24,24,12.6)}" fill-rule="evenodd" fill="{I.B}" stroke="#000" stroke-opacity=".85" stroke-width="1.4"/>')
    elif ring == "lock":
        I.s(R(28, 28, 12, 10, 2), I.B)
        I.line("M30.5,28 v-3 a3.5,3.5 0 0 1 7,0 v3", "#000", 3.6)
        I.line("M30.5,28 v-3 a3.5,3.5 0 0 1 7,0 v3", "#d9dee6", 2)


def g_controller(I, accent_btn=True):
    p = ("M14,17 H34 C39,17 42,22 42,28 C42,34 39,37 36,37 C33,37 32,33 29,31 H19 "
         "C16,33 15,37 12,37 C9,37 6,34 6,28 C6,22 9,17 14,17 Z")
    I.s(p, I.A)
    I.s("M12,22 h3 v3 h3 v3 h-3 v3 h-3 v-3 h-3 v-3 h3 Z", "#10131a", w=1)
    if accent_btn:
        for (x, y) in ((33, 22), (36.5, 25.5), (29.5, 25.5), (33, 29)):
            I.s(C(x, y, 1.9), I.B, w=1)


def g_disc(I, x=24, y=24, r=13):
    I.s(C(x, y, r), I.A)
    I.raw(f'<path d="{C(x,y,r*0.42)}" fill="{I.B}" stroke="#000" stroke-opacity=".8" stroke-width="1"/>')
    I.raw(f'<path d="{C(x,y,r*0.14)}" fill="#05070a"/>')
    I.line(f"M{f(x-r*0.72)},{f(y-r*0.35)} A{f(r*0.8)},{f(r*0.8)} 0 0 1 {f(x-r*0.2)},{f(y-r*0.78)}", "#ffffff", 1.4, 0.7)


def g_monitor(I, screen=None):
    I.s(R(8, 10, 32, 22, 2.5), "#0c0f14")
    I.raw(f'<path d="{R(10.5,12.5,27,17)}" fill="{screen or I.A}"/>')
    I.s(P((20, 32), (28, 32), (30, 37), (18, 37)), I.B)
    I.s(R(14, 36.5, 20, 2.6, 1.3), I.B)


def g_folder(I):
    I.s("M9,14 h9 l3,3 h17 a2,2 0 0 1 2,2 v17 a2,2 0 0 1 -2,2 h-27 a2,2 0 0 1 -2,-2 v-20 a2,2 0 0 1 2,-2 z", I.B)
    I.s(P((8, 21), (40, 21), (38.5, 38), (9.5, 38)), I.A)


def g_doc(I, x=13, y=9, w=21, h=29, lines=True, fill=None):
    I.s(f"M{x},{y} h{w-6} l6,6 v{h-6} h{-w} Z", fill or "#f4f6f8")
    I.s(f"M{x+w-6},{y} v6 h6 Z", "#c3cad2", w=1.2)
    if lines:
        for k, yy in enumerate(range(y + 10, y + h - 3, 4)):
            I.raw(f'<path d="{R(x+3, yy, w-6 - (6 if k % 3 == 2 else 0), 2, 1)}" fill="{I.A}"/>')


def g_gear(I, cx=24, cy=24, ro=13, ri=10, fill=None):
    I.s(gear(cx, cy, ro, ri, 9, hole=4.5), fill or I.A, extra='fill-rule="evenodd"')
    I.raw(f'<path d="{C(cx,cy,2.6)}" fill="{I.B}"/>')


def g_padlock(I, x=14, y=21, w=20, h=17):
    I.line(f"M{x+4},{y} v-4 a6,6 0 0 1 12,0 v4", "#000", 6)
    I.line(f"M{x+4},{y} v-4 a6,6 0 0 1 12,0 v4", "#d9dee6", 3.6)
    I.s(R(x, y, w, h, 3), I.A)
    I.s(f"M{x+w/2-2},{y+h/2+4} l1,-5 a2.6,2.6 0 1 1 2,0 l1,5 z", "#10131a", w=1)


def g_speaker(I, waves=2):
    I.s(P((10, 20), (16, 20), (24, 13), (24, 35), (16, 28), (10, 28)), I.A)
    for k in range(waves):
        r = 6 + k * 5
        I.line(f"M{28+k*0.5},{24-r*0.75} A{r},{r} 0 0 1 {28+k*0.5},{24+r*0.75}", "#000", 4.2)
        I.line(f"M{28+k*0.5},{24-r*0.75} A{r},{r} 0 0 1 {28+k*0.5},{24+r*0.75}", I.B, 2.4)


def g_play(I, circle=True):
    if circle:
        I.s(C(24, 24, 14), I.A)
        I.s(P((20, 16.5), (32, 24), (20, 31.5)), "#ffffff")
    else:
        I.s(P((15, 12), (36, 24), (15, 36)), I.A)


def g_film(I, x=9, y=13, w=30, h=22):
    I.s(R(x, y, w, h, 2), "#14171c")
    for k in range(6):
        I.raw(f'<path d="{R(x+2+k*4.8, y+1.5, 2.6, 2.2, .5)}" fill="#e6e9ee"/>')
        I.raw(f'<path d="{R(x+2+k*4.8, y+h-3.7, 2.6, 2.2, .5)}" fill="#e6e9ee"/>')
    I.raw(f'<path d="{R(x+2,y+5,w-4,h-10)}" fill="{I.A}"/>')


def g_arrow_down(I, x=24, y=24, s=1.0, fill=None):
    I.s(P((x-4*s, y-12*s), (x+4*s, y-12*s), (x+4*s, y-1*s), (x+9*s, y-1*s), (x, y+10*s), (x-9*s, y-1*s), (x-4*s, y-1*s)), fill or I.A)


def g_arrow_up(I, x=24, y=24, s=1.0, fill=None):
    I.s(P((x-4*s, y+12*s), (x+4*s, y+12*s), (x+4*s, y+1*s), (x+9*s, y+1*s), (x, y-10*s), (x-9*s, y+1*s), (x-4*s, y+1*s)), fill or I.A)


def g_cycle(I, cx=24, cy=24, r=11):
    for a0 in (0, 180):
        a1, a2 = math.radians(a0 + 20), math.radians(a0 + 150)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        path = f"M{f(x1)},{f(y1)} A{r},{r} 0 0 1 {f(x2)},{f(y2)}"
        I.line(path, "#000", 6.4)
        I.line(path, I.A if a0 == 0 else I.B, 4.2)
        ah = math.radians(a0 + 150)
        tx, ty = cx + r * math.cos(ah), cy + r * math.sin(ah)
        dx, dy = -math.sin(ah), math.cos(ah)
        nx, ny = math.cos(ah), math.sin(ah)
        I.s(P((tx + dx*5, ty + dy*5), (tx + nx*5 - dx*1, ty + ny*5 - dy*1), (tx - nx*5 - dx*1, ty - ny*5 - dy*1)),
            I.A if a0 == 0 else I.B, w=1.6)


def g_bars(I):
    for i, h in enumerate((9, 16, 12, 22, 18)):
        I.s(R(10 + i * 6, 37 - h, 4.6, h, 1), I.A if i % 2 else I.B, w=1.6)
    I.line("M9,37.5 H39", "#d9dee6", 1.4)


def g_graph(I):
    I.s(R(9, 11, 30, 26, 3), "#06080b")
    I.line("M11,30 L17,24 L21,27 L27,16 L31,22 L37,14", "#000", 4.4)
    I.line("M11,30 L17,24 L21,27 L27,16 L31,22 L37,14", I.A, 2.6)
    I.line("M11,34 H37", I.B, 1.6)


def g_chip(I, label=None):
    for k in range(5):
        for (x, y, w, h) in ((14 + k * 4.5, 8, 1.8, 5), (14 + k * 4.5, 35, 1.8, 5), (8, 14 + k * 4.5, 5, 1.8), (35, 14 + k * 4.5, 5, 1.8)):
            I.raw(f'<path d="{R(x,y,w,h)}" fill="#c9cfd8"/>')
    I.s(R(12, 12, 24, 24, 3), I.A)
    I.s(R(17, 17, 14, 14, 2), I.B, w=1.4)
    if label:
        I.raw(f'<text x="24" y="28.4" font-family="sans-serif" font-weight="900" font-size="9" text-anchor="middle" fill="#10131a">{label}</text>')


def g_pie(I):
    I.s(C(24, 24, 13), I.A)
    I.s("M24,24 L24,11 A13,13 0 0 1 36.4,28 Z", I.B, w=1.4)
    I.s("M24,24 L36.4,28 A13,13 0 0 1 20,36.4 Z", "#ffffff", w=1.4)


def g_layers(I):
    for k, fill in enumerate((I.B, I.A, I.B)):
        y = 30 - k * 7
        I.s(P((24, y - 7), (39, y), (24, y + 7), (9, y)), fill)


def g_list(I, pencil=False):
    I.s(R(10, 9, 24, 30, 2.5), "#f4f6f8")
    for k in range(5):
        y = 14 + k * 5
        I.raw(f'<path d="{R(13,y,3,3,0.6)}" fill="{I.B}"/>')
        I.raw(f'<path d="{R(18,y+0.5,13,2,1)}" fill="{I.A}"/>')
    if pencil:
        I.s(P((29, 38), (38, 22), (42, 24), (33, 40), (28.5, 41.5)), I.B, w=1.6)


def g_pencil(I, x=0, y=0):
    I.s(P((14+x, 38+y), (34+x, 14+y), (39+x, 18+y), (19+x, 42+y), (12.5+x, 43.5+y)), I.A)
    I.s(P((34+x, 14+y), (36+x, 11.5+y), (41+x, 15.5+y), (39+x, 18+y)), "#ff8fb0", w=1.4)


def g_camera(I):
    I.s("M10,17 h7 l2,-4 h10 l2,4 h7 a2,2 0 0 1 2,2 v15 a2,2 0 0 1 -2,2 h-28 a2,2 0 0 1 -2,-2 v-15 a2,2 0 0 1 2,-2 z", I.A)
    I.s(C(24, 26, 7.5), "#10131a")
    I.raw(f'<path d="{C(24,26,4.8)}" fill="{I.B}"/>')
    I.raw(f'<path d="{C(22.3,24.3,1.4)}" fill="#ffffff" fill-opacity=".85"/>')


def g_photo(I):
    I.s(R(8, 12, 32, 24, 2), "#f4f6f8")
    I.raw(f'<path d="{R(10.5,14.5,27,19)}" fill="{I.A}"/>')
    I.s("M10.5,33.5 L19,24 L25,30 L29,26 L37.5,33.5 Z", I.B, w=1.4)
    I.raw(f'<path d="{C(31,19.5,2.6)}" fill="#ffffff"/>')


def g_brush(I):
    I.s(E(22, 26, 13, 11), I.A, extra='fill-rule="evenodd"')
    for (x, y, c) in ((15, 22, "#ff5a4e"), (20, 18, "#ffd34d"), (27, 18.5, "#34d17a"), (30, 25, "#3fc8ff")):
        I.raw(f'<path d="{C(x,y,2.4)}" fill="{c}" stroke="#000" stroke-opacity=".6" stroke-width=".8"/>')
    I.raw(f'<path d="{C(18,31,3)}" fill="#06080b"/>')
    I.s(P((27, 33), (40, 12), (42.5, 13.5), (30, 35)), I.B, w=1.6)


def g_calc(I):
    I.s(R(12, 8, 24, 32, 3), I.A)
    I.s(R(15, 11, 18, 7, 1.2), "#0b1a10", w=1)
    I.raw('<text x="31.5" y="16.9" font-family="monospace" font-weight="700" font-size="6" text-anchor="end" fill="#7dff9a">1984</text>')
    for r in range(3):
        for c in range(3):
            I.raw(f'<path d="{R(15+c*6.2,21+r*6,4.6,4,1)}" fill="{I.B}" stroke="#000" stroke-opacity=".6" stroke-width=".7"/>')


def g_phone_link(I):
    I.s(R(8, 13, 20, 14, 2), I.B)
    I.s(R(5, 27, 26, 3, 1.4), I.B)
    I.s(R(30, 14, 11, 20, 2.4), I.A)
    I.raw(f'<path d="{R(32,17,7,13)}" fill="#0c0f14"/>')
    I.line("M20,36 C24,40 30,40 34,37", "#000", 3.4)
    I.line("M20,36 C24,40 30,40 34,37", "#ffffff", 1.8)


def g_remote(I):
    g_monitor(I)
    I.s(P((22, 15), (32, 21), (27.5, 22), (30, 27), (28, 28), (25.5, 23), (22, 26)), "#ffffff", w=1.4)


def g_cube(I):
    I.s(P((24, 9), (38, 16), (24, 23), (10, 16)), I.B)
    I.s(P((10, 16), (24, 23), (24, 39), (10, 32)), I.A)
    I.s(P((38, 16), (24, 23), (24, 39), (38, 32)), "#ffffff", extra='fill-opacity=".85"')


def g_wallet(I):
    I.s(R(8, 14, 32, 22, 3), I.A)
    I.s(R(26, 20, 14, 10, 2.5), I.B)
    I.raw(f'<path d="{C(31,25,1.8)}" fill="#10131a"/>')


def g_smile(I):
    I.s(C(24, 24, 14), I.A)
    I.raw(f'<path d="{E(19,20,2,3)} {E(29,20,2,3)}" fill="#10131a"/>')
    I.line("M16.5,27 Q24,35 31.5,27", "#10131a", 2.6)


def g_tag(I):
    I.s("M10,12 h14 l15,15 l-12,12 l-15,-15 z", I.A)
    I.raw(f'<path d="{C(16,18,2.4)}" fill="#10131a"/>')
    g_pencil(I, 2, -2)


def g_wrench(I, x=0, y=0, fill=None):
    I.s(f"M{30+x},{9+y} a7,7 0 0 0 -6,10 l-14,14 a2.8,2.8 0 0 0 4,4 l14,-14 a7,7 0 0 0 10,-6 l-4,2 l-3,-3 l2,-4 z", fill or I.B)


def g_printer(I, scan=False):
    if scan:
        I.s(P((9, 22), (39, 22), (39, 33), (9, 33)), I.A)
        I.s(P((9, 22), (39, 22), (36, 15), (12, 15)), I.B)
        I.line("M12,27.5 H36", "#ffffff", 1.6)
        return
    I.s(R(15, 9, 18, 9, 1), "#f4f6f8")
    I.s(R(8, 17, 32, 14, 3), I.A)
    I.s(R(14, 27, 20, 12, 1), "#f4f6f8")
    I.raw(f'<path d="{R(17,31,14,1.6)} {R(17,34.5,10,1.6)}" fill="{I.B}"/>')
    I.raw(f'<path d="{C(34.5,21.5,1.6)}" fill="#7dff9a"/>')


def g_scroll(I, emblem=None):
    I.s(R(12, 12, 24, 24), I.A)
    for y in (11, 37):
        I.s(R(9, y - 3, 30, 6, 3), I.B)
    for yy in (17, 21, 25, 29):
        I.raw(f'<path d="{R(15,yy,18 - (6 if yy == 29 else 0),1.6,.8)}" fill="#3a2410" fill-opacity=".55"/>')
    if emblem == "sword":
        I.s(P((33, 11), (35, 13), (22, 31), (20, 29)), "#e6edf5", w=1.6)
        I.s(R(16, 30, 7, 2.4, 1), "#ffd34d", w=1.2)
    elif emblem == "snow":
        I.s(P((14, 32), (21, 20), (25, 26), (28, 22), (35, 32)), "#ffffff", w=1.6)
    elif emblem == "mushroom":
        I.s("M18,24 a6,6 0 0 1 12,0 z", "#c48bff", w=1.4)
        I.s(R(22.5, 24, 3, 8, 1), "#f2c48d", w=1.2)
    elif emblem == "orb":
        I.s(C(24, 24, 6), "#7cf3ff", w=1.4)
        I.raw(f'<path d="{C(22,22,1.6)}" fill="#ffffff"/>')
    elif emblem == "gear":
        g_gear(I, 24, 24, 7.5, 5.6, fill="#c9cfd8")
    elif emblem == "pencil":
        I.s(P((17, 32), (29, 18), (32, 21), (20, 35), (16, 36)), "#ffd34d", w=1.4)
    elif emblem == "map":
        I.line("M15,30 C19,22 25,30 33,18", "#e02b3a", 1.8)
        I.raw(f'<path d="{C(33,18,1.8)}" fill="#e02b3a"/>')


def g_gasmask(I, visor=None):
    I.s("M24,9 C33,9 38,15 38,23 C38,30 34,36 24,39 C14,36 10,30 10,23 C10,15 15,9 24,9 Z", I.A)
    I.s(E(18, 21, 4.5, 4), visor or I.B, w=1.6)
    I.s(E(30, 21, 4.5, 4), visor or I.B, w=1.6)
    I.s(C(24, 32, 5), "#2a2e35")
    for k in range(3):
        I.raw(f'<path d="{R(20.5,29.5+k*2,7,0.9)}" fill="#8a929e"/>')


def g_vr(I):
    I.s("M8,19 a4,4 0 0 1 4,-4 h24 a4,4 0 0 1 4,4 v11 a4,4 0 0 1 -4,4 h-7 l-3,-4 h-4 l-3,4 h-7 a4,4 0 0 1 -4,-4 z", I.A)
    I.s(E(17.5, 24, 4.5, 4), I.B, w=1.4)
    I.s(E(30.5, 24, 4.5, 4), I.B, w=1.4)


def g_helmet(I, horns=False):
    if horns:
        I.s("M12,22 C6,20 5,12 8,8 C9,14 12,17 16,18 Z", "#f4f6f8", w=1.6)
        I.s("M36,22 C42,20 43,12 40,8 C39,14 36,17 32,18 Z", "#f4f6f8", w=1.6)
    I.s("M10,28 C10,18 16,12 24,12 C32,12 38,18 38,28 Z", I.A)
    I.s(R(7, 27, 34, 5, 2.5), I.B)
    if horns:
        I.s(R(22, 13, 4, 14, 1), I.B, w=1.4)


def g_crown(I):
    I.s(P((9, 33), (9, 16), (16, 24), (24, 12), (32, 24), (39, 16), (39, 33)), I.A)
    I.s(R(9, 31, 30, 6, 1), I.B)
    for x, c in ((16, "#e02b3a"), (24, "#2e8bff"), (32, "#34d17a")):
        I.raw(f'<path d="{C(x,34,1.8)}" fill="{c}" stroke="#000" stroke-opacity=".6" stroke-width=".8"/>')


def g_ball(I):
    I.s(C(24, 24, 14), "#f4f6f8")
    I.s(P((24, 18), (29, 21.5), (27, 27.5), (21, 27.5), (19, 21.5)), "#10131a", w=1)
    for (x1, y1, x2, y2) in ((24, 18, 24, 10.5), (29, 21.5, 36.5, 19), (27, 27.5, 31.5, 34.5), (21, 27.5, 16.5, 34.5), (19, 21.5, 11.5, 19)):
        I.line(f"M{x1},{y1} L{x2},{y2}", "#10131a", 1.4)
    I.raw(f'<path d="{C(24,24,14)} {C(24,24,12.4)}" fill-rule="evenodd" fill="{I.A}"/>')


def g_glove(I):
    I.s("M13,20 C13,13 18,10 24,10 C31,10 36,14 36,21 L36,28 C36,32 33,35 29,35 L18,35 C15,35 13,33 13,30 Z", I.A)
    I.s("M13,25 C8,25 8,18 13,18", I.A, w=2)
    I.s(R(15, 34, 19, 6, 1.5), I.B)
    I.line("M20,16 C22,20 22,24 20,27", "#000", 1.2, 0.5)


def g_guitar(I, amp=False):
    if amp:
        I.s(R(8, 12, 32, 26, 3), "#14171c")
        I.raw(f'<path d="{R(10.5,14.5,27,6,1)}" fill="{I.A}"/>')
        for k in range(4):
            I.raw(f'<path d="{C(14+k*6.6,17.5,1.4)}" fill="#10131a"/>')
        I.s(R(11, 23, 26, 12.5, 1.5), I.B, w=1.2)
        for k in range(5):
            I.raw(f'<path d="{R(12,24.5+k*2.3,24,0.8)}" fill="#000" fill-opacity=".35"/>')
        return
    I.s(P((26, 22), (36, 8), (39, 10), (29, 24)), I.B, w=1.8)
    I.s("M22,18 C25,18 27,21 26,24 C30,25 32,29 30,34 C28,39 20,41 14,38 C9,35 8,29 11,25 C13,23 16,23 17,22 C18,19 20,18 22,18 Z", I.A)
    I.raw(f'<path d="{C(20,30,2.6)}" fill="#10131a"/>')


def g_slide(I):
    I.s("M10,12 h8 C18,24 28,26 38,30 v6 C24,34 12,28 10,12 Z", I.A)
    for k in range(3):
        I.s(E(16 + k * 9, 38, 4, 1.6), "#7cf3ff", w=1.2)


def g_tank(I):
    I.s(R(8, 29, 32, 8, 4), "#2a2e35")
    for k in range(5):
        I.raw(f'<path d="{C(12.5+k*5.7,33,1.8)}" fill="#8a929e"/>')
    I.s(P((10, 29), (38, 29), (35, 23), (13, 23)), I.A)
    I.s(R(17, 16, 14, 8, 3), I.B)
    I.s(R(30, 18, 11, 3, 1), I.B, w=1.6)


def g_chef(I):
    I.s("M14,26 C8,25 8,16 14,16 C14,10 22,8 25,13 C28,8 37,10 35,17 C41,17 41,26 34,26 Z", "#f4f6f8")
    I.s(R(15, 25, 18, 7, 1), "#f4f6f8")
    I.s(E(26, 37, 11, 3.4), I.A)
    I.s(R(36, 35.5, 7, 2.6, 1.2), I.B, w=1.4)


def g_raft(I):
    I.s("M6,34 C12,31 16,37 24,34 C32,31 36,37 42,34 V40 H6 Z", "#2e8bff", w=1.6)
    for k in range(5):
        I.s(R(10 + k * 5.6, 28, 5, 5, 1.2), I.A, w=1.2)
    I.line("M24,28 V10", "#000", 3)
    I.line("M24,28 V10", "#c48b5b", 1.6)
    I.s(P((25, 11), (36, 24), (25, 24)), I.B, w=1.6)


def g_sprout(I):
    I.s(P((10, 30), (38, 30), (35, 40), (13, 40)), I.B)
    I.line("M24,30 V18", "#000", 3.6)
    I.line("M24,30 V18", "#34d17a", 2)
    I.s("M24,22 C18,22 14,18 14,12 C20,12 24,16 24,22 Z", I.A, w=1.8)
    I.s("M24,19 C30,19 34,15 34,9 C28,9 24,13 24,19 Z", I.A, w=1.8)


def g_dog_tags(I):
    I.line("M16,8 L22,22 M32,8 L26,22", "#c9cfd8", 1.4)
    I.s(R(13, 21, 13, 18, 5), I.A)
    I.s(R(23, 19, 13, 18, 5), I.B)
    I.raw(f'<path d="{R(26,25,7,1.4)} {R(26,28.5,7,1.4)} {R(26,32,5,1.4)}" fill="#10131a" fill-opacity=".6"/>')


def g_binoculars(I):
    I.s(C(16, 29, 8), I.A)
    I.s(C(32, 29, 8), I.A)
    I.s(R(13, 12, 7, 14, 2), I.B)
    I.s(R(28, 12, 7, 14, 2), I.B)
    I.s(R(20, 18, 8, 5, 1), "#2a2e35", w=1.2)
    for x in (16, 32):
        I.raw(f'<path d="{C(x,29,4.4)}" fill="#7cf3ff"/><path d="{C(x-1.5,27.5,1.2)}" fill="#ffffff"/>')


def g_cartridge(I):
    I.s(P((11, 9), (37, 9), (37, 37), (34, 40), (14, 40), (11, 37)), I.A)
    I.s(R(14, 13, 20, 14, 1.5), I.B, w=1.4)
    for k in range(5):
        I.raw(f'<path d="{R(15+k*3.8,33,2,4)}" fill="#10131a" fill-opacity=".55"/>')


def g_handheld(I, wide=False, dual=False):
    if dual:
        I.s(R(11, 7, 26, 16, 2.5), I.B)
        I.raw(f'<path d="{R(14,10,20,10)}" fill="#7cf3ff"/>')
        I.s(R(11, 24, 26, 17, 2.5), I.A)
        I.raw(f'<path d="{R(17,27,14,8)}" fill="#7cf3ff"/>')
        return
    if wide:
        I.s(R(5, 15, 38, 19, 9), I.A)
        I.s(R(14, 18, 20, 13, 1.5), "#0c0f14", w=1.2)
        I.raw(f'<path d="{R(15.5,19.5,17,10)}" fill="{I.B}"/>')
        I.s("M8.5,23.5 h2 v-2 h2 v2 h2 v2 h-2 v2 h-2 v-2 h-2 z", "#10131a", w=0.8)
        I.raw(f'<path d="{C(37.5,22,1.4)} {C(37.5,27.5,1.4)} {C(35,24.7,1.4)} {C(40,24.7,1.4)}" fill="#10131a"/>')


def g_arcade(I, coin=False):
    I.s(P((14, 7), (34, 7), (34, 12), (37, 21), (37, 41), (11, 41), (11, 21), (14, 12)), I.A)
    I.s(R(15, 9, 18, 4, 1), I.B, w=1)
    I.s(R(15, 15, 18, 12, 1), "#0c0f14", w=1.2)
    I.raw(f'<path d="{R(16.5,16.5,15,9)}" fill="{I.B}"/>')
    I.s(R(12, 28, 24, 4, 1), "#2a2e35", w=1.2)
    I.line("M19,28 V25", "#000", 2.2)
    I.raw(f'<path d="{C(19,24.5,1.8)}" fill="#e02b3a"/><path d="{C(28,29.5,1.2)} {C(31.5,29.5,1.2)}" fill="#ffd34d"/>')
    if coin:
        I.raw(f'<path d="{R(22,34,4,4,.6)}" fill="#ffd34d" stroke="#000" stroke-opacity=".6" stroke-width=".8"/>')


def g_joystick(I):
    I.s(E(24, 35, 14, 5), I.A)
    I.s(R(8, 30, 32, 5), I.A, outline=False)
    I.s(E(24, 30, 14, 5), I.B)
    I.line("M24,30 L28,15", "#000", 4.2)
    I.line("M24,30 L28,15", "#c9cfd8", 2.4)
    I.s(C(28.5, 13.5, 4.6), "#e02b3a")
    I.raw(f'<path d="{C(27,12,1.4)}" fill="#ffffff" fill-opacity=".8"/>')


def g_magnify(I, x=0, y=0):
    I.line(f"M{30+x},{30+y} L{39+x},{39+y}", "#000", 6.4)
    I.line(f"M{30+x},{30+y} L{39+x},{39+y}", I.B, 4)
    I.s(C(22 + x, 22 + y, 10), I.A)
    I.raw(f'<path d="{C(22+x,22+y,6.8)}" fill="#cff4ff"/><path d="{C(20+x,19.5+y,2)}" fill="#ffffff"/>')


def g_cursor(I):
    I.s(P((15, 9), (35, 27), (26, 28), (31, 38), (27, 40), (22, 30), (15, 36)), I.A)


def g_two_pads(I):
    for (dx, dy, fill) in ((-4, -6, I.B), (4, 6, I.A)):
        p = (f"M{14+dx},{17+dy} H{30+dx} C{34+dx},{17+dy} {36+dx},{21+dy} {36+dx},{25+dy} "
             f"C{36+dx},{29+dy} {33+dx},{31+dy} {31+dx},{31+dy} L{27+dx},{27+dy} H{17+dx} L{13+dx},{31+dy} "
             f"C{11+dx},{31+dy} {8+dx},{29+dy} {8+dx},{25+dy} C{8+dx},{21+dy} {10+dx},{17+dy} {14+dx},{17+dy} Z")
        I.s(p, fill)


def g_wifi(I, x=24, y=24):
    for k, r in enumerate((4, 8, 12)):
        path = f"M{x-r*0.8},{y-r*0.6} A{r},{r} 0 0 1 {x+r*0.8},{y-r*0.6}"
        I.line(path, "#000", 4.4)
        I.line(path, I.B, 2.6)
    I.s(C(x, y + 1, 2), I.B, w=1.2)


def g_tree(I):
    I.s(R(21.5, 28, 5, 11, 1), "#b8733a")
    I.s(C(24, 20, 12), I.A)
    for (x, y) in ((18, 18), (29, 16), (24, 25), (31, 24), (17, 26)):
        I.s(C(x, y, 2.2), "#e02b3a", w=1)


def g_rocket(I):
    I.s("M24,7 C30,12 32,20 30,30 H18 C16,20 18,12 24,7 Z", I.A)
    I.s(C(24, 19, 3.6), "#7cf3ff", w=1.4)
    I.s(P((18, 24), (12, 33), (18, 31)), I.B, w=1.6)
    I.s(P((30, 24), (36, 33), (30, 31)), I.B, w=1.6)
    I.s(P((20, 30), (28, 30), (24, 40)), "#ff7f2a", w=1.6)


def g_shield(I, sword=False):
    I.s("M24,8 L37,13 V23 C37,31 31,37 24,40 C17,37 11,31 11,23 V13 Z", I.A)
    I.s("M24,12 L33,15.5 V23 C33,29 29,33 24,35.5 Z", I.B, w=1.2)
    if sword:
        I.s(P((23, 6), (25, 6), (25, 30), (23, 30)), "#e6edf5", w=1.4)
        I.s(R(18, 27, 12, 3, 1), "#ffd34d", w=1.2)


def g_wand(I, hat=False):
    if hat:
        I.s("M24,6 C28,14 31,22 34,32 H14 C17,22 20,14 24,6 Z", I.A)
        I.s(E(24, 33, 15, 4), I.B)
        for (x, y, r) in ((22, 17, 2.4), (27, 25, 1.8), (19, 27, 1.4)):
            I.s(star(x, y, r * 1.6, r * 0.7), "#ffe14d", w=1)
        return
    I.s(P((10, 38), (30, 18), (33, 21), (13, 41)), "#2a2e35", w=1.6)
    I.raw(f'<path d="{P((28,20),(30,18),(33,21),(31,23))}" fill="#f4f6f8"/>')
    I.s(star(34, 14, 6, 2.6), I.A, w=1.6)


def g_wineglass(I):
    I.s("M14,9 H34 C34,20 30,26 24,26 C18,26 14,20 14,9 Z", "#f4f6f8", extra='fill-opacity=".9"')
    I.s("M15.5,15 H32.5 C32,21 29,25 24,25 C19,25 16,21 15.5,15 Z", I.A, w=1.2)
    I.s(R(22.5, 26, 3, 10), "#f4f6f8", w=1.4)
    I.s(E(24, 37.5, 8, 2.4), "#f4f6f8", w=1.4)


def g_atom_up(I):
    for rot in (0, 60, 120):
        I.raw(f'<ellipse cx="24" cy="26" rx="13" ry="5" fill="none" stroke="#000" stroke-opacity=".8" stroke-width="3.8" transform="rotate({rot} 24 26)"/>')
        I.raw(f'<ellipse cx="24" cy="26" rx="13" ry="5" fill="none" stroke="{I.B}" stroke-width="2" transform="rotate({rot} 24 26)"/>')
    g_arrow_up(I, 24, 22, 0.75)


def g_seal(I):
    pts = []
    for i in range(24):
        r = 14 if i % 2 == 0 else 12.4
        a = 2 * math.pi * i / 24
        pts.append((24 + r * math.cos(a), 24 + r * math.sin(a)))
    I.s(P(*pts), I.A)
    I.s(C(24, 24, 8.5), I.B, w=1.4)
    I.s(P((24, 18.5), (29.5, 21.5), (29.5, 26.5), (24, 29.5), (18.5, 26.5), (18.5, 21.5)), "#ffffff", w=1.2)


def g_subtitles(I):
    I.s(R(7, 11, 34, 22, 3), "#0c0f14")
    I.raw(f'<path d="{R(9.5,13.5,29,17)}" fill="{I.B}" fill-opacity=".55"/>')
    I.s(R(11, 25, 18, 3, 1.5), "#ffe14d", w=1.2)
    I.s(R(31, 25, 6, 3, 1.5), "#ffffff", w=1.2)
    I.s(P((15, 33), (21, 33), (16, 39)), "#0c0f14", w=1.4)


def g_lever(I):
    I.s(R(9, 30, 30, 9, 2), I.B)
    I.line("M24,32 L33,12", "#000", 5)
    I.line("M24,32 L33,12", "#c9cfd8", 3)
    I.s(C(33.5, 11, 5), I.A)


def g_hand(I):
    I.s("M17,38 C12,34 10,29 10,25 C10,23 12,22 14,24 L16,27 V13 a2,2 0 0 1 4,0 V22 V10 a2,2 0 0 1 4,0 V22 V11 a2,2 0 0 1 4,0 V23 V15 a2,2 0 0 1 4,0 V28 C32,34 29,38 25,38 Z", I.A)
    I.line("M35,10 C38,12 39,15 38,18 M38,8 C42,11 43,16 41,20", I.B, 1.8)


def g_package(I, arrow=None):
    I.s(P((24, 9), (39, 16), (39, 32), (24, 39), (9, 32), (9, 16)), I.A)
    I.s(P((24, 9), (39, 16), (24, 23), (9, 16)), I.B)
    I.line("M24,23 V39", "#000", 1.2, 0.6)
    if arrow == "down":
        g_arrow_down(I, 31, 31, 0.55, "#7dff9a")
    elif arrow == "cycle":
        I.s(C(32, 32, 7.5), "#10131a", w=1.4)
        I.line("M28,30 A4.5,4.5 0 0 1 36,30 M36,34 A4.5,4.5 0 0 1 28,34", "#7cf3ff", 1.6)


def g_clock(I, chip=False):
    if chip:
        g_chip(I)
        I.s(C(24, 24, 6.5), "#f4f6f8", w=1.2)
        I.line("M24,24 V20 M24,24 L27,26", "#10131a", 1.4)
        return
    I.s(C(24, 24, 13), I.A)
    I.s(C(24, 24, 10), "#f4f6f8", w=1.2)
    I.line("M24,24 V16.5 M24,24 L29.5,27", "#10131a", 2)


def g_shell(I):
    I.s("M24,38 C14,38 8,31 9,22 C10,14 17,9 24,9 C31,9 38,14 39,22 C40,31 34,38 24,38 Z", I.A)
    for x in (16, 20, 24, 28, 32):
        I.line(f"M24,37 L{x},{12 + abs(x-24)*0.55}", "#000", 1.2, 0.55)
    I.s(R(19, 35, 10, 5, 2), I.B, w=1.4)


def g_stream(I):
    g_monitor(I)
    I.s(P((20, 16), (30, 21), (20, 26)), "#ffffff", w=1.4)
    I.line("M34,9 C37,11 38,14 37,17 M37,7 C41,10 42,15 40,19", I.B, 1.8)


def g_tv(I, mark=None):
    I.line("M18,9 L23,14 M30,9 L25,14", "#c9cfd8", 1.6)
    I.s(R(7, 14, 34, 24, 4), I.B)
    I.s(R(10, 17, 22, 18, 3), "#0c0f14", w=1.2)
    I.raw(f'<path d="{R(11.5,18.5,19,15,2)}" fill="{I.A}"/>')
    I.raw(f'<path d="{C(36.5,21,1.8)} {C(36.5,27,1.8)}" fill="#10131a"/>')
    if mark == "spiral":
        I.line("M21,26 a1.5,1.5 0 1 1 1.5,1.5 a3.2,3.2 0 1 1 -3,-3.3 a5,5 0 1 1 5,5", "#ffffff", 1.3)
    elif mark == "play":
        I.s(P((18, 21.5), (25.5, 26), (18, 30.5)), "#ffffff", w=1.2)
    elif mark == "pad":
        I.s("M15,23 h12 c3,0 4,3 4,5 c0,2 -1,3 -2,3 l-2,-2 h-8 l-2,2 c-1,0 -2,-1 -2,-3 c0,-2 1,-5 4,-5 z", "#ffffff", w=1)


def g_vinyl(I):
    I.s(C(24, 24, 14), "#0c0f14")
    for r in (11.5, 9.5, 7.5):
        I.raw(f'<path d="{C(24,24,r)}" fill="none" stroke="#3a3f48" stroke-width=".7"/>')
    I.raw(f'<path d="{C(24,24,5.2)}" fill="{I.A}"/><path d="{C(24,24,1.2)}" fill="#0c0f14"/>')
    I.line("M14,14 A14,14 0 0 1 22,10.2", "#ffffff", 1.4, 0.6)
    I.line("M37,8 L32,22", "#000", 3.4)
    I.line("M37,8 L32,22", I.B, 1.8)


def g_chat(I, headset=False):
    I.s("M10,10 h20 a4,4 0 0 1 4,4 v10 a4,4 0 0 1 -4,4 h-12 l-6,6 v-6 h-2 a4,4 0 0 1 -4,-4 v-10 a4,4 0 0 1 4,-4 z", I.A)
    I.s("M24,22 h14 a3,3 0 0 1 3,3 v8 a3,3 0 0 1 -3,3 h-1 v5 l-5,-5 h-8 a3,3 0 0 1 -3,-3 v-8 a3,3 0 0 1 3,-3 z", I.B)
    I.raw(f'<path d="{C(15,19,1.6)} {C(20,19,1.6)} {C(25,19,1.6)}" fill="#10131a"/>')


def g_swarm(I):
    for (x, y) in ((14, 14), (34, 14), (24, 34)):
        I.s(C(x, y, 5.2), I.B, w=1.6)
    I.line("M14,14 L34,14 L24,34 Z", "#000", 3.6)
    I.line("M14,14 L34,14 L24,34 Z", "#c9cfd8", 1.6)
    g_arrow_down(I, 24, 22, 0.55)


def g_tunnel(I):
    for k, r in enumerate((14, 10.5, 7)):
        I.s(C(24, 24, r), I.A if k % 2 == 0 else I.B, w=1.6)
    g_padlock(I, 18.5, 23.5, 11, 9)


def g_nodes(I):
    I.line("M13,15 C22,15 22,33 35,33 M13,33 C22,33 26,15 35,15", "#000", 3.6)
    I.line("M13,15 C22,15 22,33 35,33 M13,33 C22,33 26,15 35,15", "#c9cfd8", 1.8)
    for (x, y, c) in ((12, 15, I.A), (12, 33, I.A), (36, 15, I.B), (36, 33, I.B)):
        I.s(R(x - 5, y - 4, 10, 8, 2), c, w=1.6)


def g_book(I, q=False):
    I.s("M8,12 C14,10 20,11 24,14 C28,11 34,10 40,12 V36 C34,34 28,35 24,38 C20,35 14,34 8,36 Z", I.A)
    I.line("M24,14 V38", "#000", 1.4, 0.7)
    for k in range(3):
        I.raw(f'<path d="{R(11,17+k*4,10,1.4,.7)} {R(27,17+k*4,10,1.4,.7)}" fill="#10131a" fill-opacity=".45"/>')
    if q:
        I.s(C(36, 34, 6), I.B, w=1.4)
        I.raw('<text x="36" y="37.2" font-family="sans-serif" font-weight="900" font-size="9" text-anchor="middle" fill="#10131a">?</text>')


def g_window_pencil(I):
    I.s(R(7, 9, 30, 24, 2.5), "#0c0f14")
    I.raw(f'<path d="{R(7,9,30,5,2)}" fill="{I.B}"/><path d="{R(10,17,10,13,1)} {R(22,17,12,5,1)}" fill="{I.A}"/>')
    g_pencil(I, 4, 0)


def g_bubbles_lang(I):
    I.s("M8,9 h18 a3,3 0 0 1 3,3 v10 a3,3 0 0 1 -3,3 h-11 l-5,5 v-5 h-2 a3,3 0 0 1 -3,-3 v-10 a3,3 0 0 1 3,-3 z", I.A)
    I.raw('<text x="16.5" y="21.5" font-family="serif" font-weight="900" font-size="12" text-anchor="middle" fill="#10131a">A</text>')
    I.s("M22,21 h18 a3,3 0 0 1 3,3 v9 a3,3 0 0 1 -3,3 h-2 v5 l-5,-5 h-11 a3,3 0 0 1 -3,-3 v-9 a3,3 0 0 1 3,-3 z", I.B)
    I.raw('<text x="31" y="33" font-family="serif" font-weight="900" font-size="10" text-anchor="middle" fill="#10131a">&#x3042;</text>')


def g_dbus(I):
    I.s(C(24, 12, 5), I.A, w=1.6)
    for x in (12, 24, 36):
        I.line(f"M24,17 L{x},29", "#000", 3.2)
        I.line(f"M24,17 L{x},29", "#c9cfd8", 1.4)
        I.s(R(x - 5, 29, 10, 8, 2), I.B, w=1.6)


def g_webcam(I, rec=False):
    I.s(C(24, 20, 11), I.A)
    I.s(C(24, 20, 6.5), "#0c0f14", w=1.2)
    I.raw(f'<path d="{C(24,20,3.6)}" fill="{I.B}"/><path d="{C(22.6,18.6,1.1)}" fill="#ffffff"/>')
    I.s(P((18, 30), (30, 30), (34, 39), (14, 39)), "#2a2e35", w=1.4)
    if rec:
        I.s(C(36, 34, 4.5), "#ff3b3b", w=1.4)


def g_sliders(I):
    for k, (x, y) in enumerate(((14, 26), (24, 17), (34, 30))):
        I.line(f"M{x},11 V37", "#000", 4)
        I.line(f"M{x},11 V37", "#c9cfd8", 2)
        I.s(R(x - 4, y - 3, 8, 6, 1.6), I.A if k != 1 else I.B, w=1.6)


def g_record(I):
    I.s(C(24, 24, 14), I.A)
    I.s(C(24, 24, 9), "#0c0f14", w=1.2)
    I.s(C(24, 24, 5.5), "#ff3b3b", w=1)
    I.raw(f'<path d="{C(22.5,22.5,1.5)}" fill="#ffffff" fill-opacity=".8"/>')


def g_clapper(I):
    I.s(R(9, 20, 30, 19, 2), "#14171c")
    I.raw(f'<path d="{R(11,24,26,13)}" fill="{I.A}"/>')
    I.s(P((8, 13), (38, 8), (39, 14), (9, 19)), "#f4f6f8", w=1.8)
    for k in range(4):
        x = 12 + k * 7
        I.raw(f'<path d="{P((x,12.3),(x+3.5,11.7),(x+5.5,17.4),(x+2,18))}" fill="#14171c"/>')
    I.s(P((19, 27), (28, 30.5), (19, 34)), "#ffffff", w=1.2)


def g_isotope(I):
    I.s(R(11, 7, 26, 34, 3), I.B)
    I.s(R(15, 7, 18, 8), "#c9cfd8", w=1.2)
    g_disc(I, 24, 28, 9)


def g_topology(I):
    I.s(R(18, 8, 12, 9, 2), I.A, w=1.6)
    I.line("M24,17 V22 M12,22 H36 M12,22 V28 M24,22 V28 M36,22 V28", "#000", 3.4)
    I.line("M24,17 V22 M12,22 H36 M12,22 V28 M24,22 V28 M36,22 V28", "#c9cfd8", 1.6)
    for x in (12, 24, 36):
        I.s(R(x - 5, 28, 10, 10, 2), I.B, w=1.6)


def g_info_chip(I):
    g_chip(I)
    I.s(C(24, 24, 6.5), "#f4f6f8", w=1.2)
    I.raw('<text x="24" y="27.6" font-family="serif" font-weight="900" font-style="italic" font-size="10" text-anchor="middle" fill="#2e8bff">i</text>')


def g_doc_diff(I):
    g_doc(I, 8, 10, 17, 25)
    g_doc(I, 23, 13, 17, 25)
    I.raw(f'<path d="{R(26,26,11,2.2,1)}" fill="#ff5a4e"/><path d="{R(11,26,11,2.2,1)}" fill="#34d17a"/>')


def g_textcursor(I, label):
    I.s(R(7, 12, 34, 24, 3), "#0c0f14")
    I.raw(f'<text x="21" y="29" font-family="monospace" font-weight="900" font-size="13" text-anchor="middle" fill="{I.A}">{label}</text>')
    I.s(R(31, 17, 3, 14, 0.5), I.B, w=1)


def g_key(I, label):
    I.s(R(8, 10, 32, 28, 5), "#2a2e35")
    I.s(R(11, 12, 26, 21, 4), I.A, w=1.4)
    I.raw(f'<text x="24" y="26.5" font-family="sans-serif" font-weight="900" font-size="9.5" text-anchor="middle" fill="#10131a">{label}</text>')


def g_kart(I):
    I.s("M8,30 C8,24 12,21 18,21 H26 L30,16 H35 L36,21 C40,22 41,26 41,30 Z", I.A)
    I.s(R(22, 13, 3, 9, 1), "#2a2e35", w=1.2)
    for x in (14, 34):
        I.s(C(x, 32, 5.2), "#14171c")
        I.raw(f'<path d="{C(x,32,2.2)}" fill="#c9cfd8"/>')
    for k in range(4):
        I.raw(f'<path d="{R(9+k*3,8,3,3)} {R(12+k*3,11,3,3)}" fill="#ffffff"/>')
        I.raw(f'<path d="{R(12+k*3,8,3,3)} {R(9+k*3,11,3,3)}" fill="#10131a"/>')


def g_speedshoe(I):
    for k, y in enumerate((17, 23, 29)):
        I.line(f"M5,{y} H{14 - k*2}", I.B, 2.2)
    I.s("M14,30 C14,22 18,17 24,17 L28,22 C33,23 40,25 42,29 V34 H14 Z", I.A)
    I.s(R(14, 33, 28, 4, 1.6), "#f4f6f8", w=1.4)
    I.line("M22,22 L26,25 M20,25 L24,28", "#ffffff", 1.4)


def g_retro_tv_pad(I):
    g_tv(I, "pad")


def g_backup_disc(I):
    g_disc(I, 20, 24, 12)
    I.s(C(34, 33, 7.5), "#10131a", w=1.4)
    I.line("M30,31 A4.6,4.6 0 0 1 38,31 M38,35 A4.6,4.6 0 0 1 30,35", "#7dff9a", 1.8)


def g_unlock(I):
    I.line("M18,22 v-5 a6,6 0 0 1 12,0", "#000", 6)
    I.line("M18,22 v-5 a6,6 0 0 1 12,0", "#d9dee6", 3.6)
    I.s(R(12, 22, 20, 16, 3), I.A)
    I.s("M33,22 C38,22 40,26 37,29 C40,31 38,35 34,34 C35,37 31,39 29,36", I.B, w=1.6)


def g_pickaxe(I, puzzle=False):
    I.s(P((12, 38), (31, 19), (34, 22), (15, 41)), "#b8733a", w=1.8)
    I.s("M16,12 C24,8 34,9 40,16 L37,18 C32,14 26,13 20,15 Z", I.A)
    I.s("M40,16 C42,22 40,30 34,36 L32,33 C36,28 37,23 36.5,19 Z", I.A)
    if puzzle:
        I.s("M8,8 h6 a2.5,2.5 0 1 1 5,0 h6 v6 a2.5,2.5 0 1 0 0,5 v6 h-17 z", I.B, w=1.6)


def g_block_pick(I):
    I.s(P((24, 9), (38, 16), (24, 23), (10, 16)), "#c9cfd8")
    I.s(P((10, 16), (24, 23), (24, 39), (10, 32)), "#8a929e")
    I.s(P((38, 16), (24, 23), (24, 39), (38, 32)), "#5f6772")
    for (x, y) in ((15, 25), (19, 31), (30, 27), (33, 21)):
        I.raw(f'<path d="{R(x,y,3,3)}" fill="{I.A}"/>')
    I.s(P((26, 40), (40, 26), (42, 28), (28, 42)), "#b8733a", w=1.4)
    I.s("M35,23 C39,21 43,22 45,25 L43,26 C41,25 39,25 37,26 Z", I.B, w=1.2)


def g_photo_spark(I):
    g_camera(I)
    I.s(star(37, 11, 5.5, 2), "#ffe14d", w=1.4)
    I.s(star(12, 11, 3.2, 1.2), "#ffffff", w=1)


def g_mods_stack(I):
    for k, fill in enumerate((I.B, I.A, I.B)):
        I.s(R(10 + k * 2, 30 - k * 8, 24, 7, 2), fill, w=1.8)
    g_arrow_down(I, 35, 18, 0.5, "#7dff9a")


def g_hp_tool(I):
    g_printer(I)
    g_wrench(I, 6, 4, fill="#c9cfd8")


def g_snowcap(I):
    I.s(R(8, 12, 32, 24, 3), I.A)


def g_target(I):
    I.s(C(24, 24, 13), I.A)
    I.s(C(24, 24, 8.5), "#0c0f14", w=1.2)
    I.s(C(24, 24, 4), I.B, w=1.2)
    I.line("M24,6 V14 M24,34 V42 M6,24 H14 M34,24 H42", "#000", 3.4)
    I.line("M24,6 V14 M24,34 V42 M6,24 H14 M34,24 H42", "#f4f6f8", 1.6)


def g_console_disc(I):
    I.s(R(8, 22, 32, 15, 2.5), I.A)
    I.raw(f'<path d="{R(11,26,16,2.4,1)}" fill="#10131a"/><path d="{C(34,30,2.2)}" fill="#7dff9a"/>')
    g_disc(I, 24, 15, 8)


def g_ocean_disc(I):
    g_disc(I)
    I.line("M13,30 C17,27 20,33 24,30 C28,27 31,33 35,30", "#ffffff", 1.8)


# ---------------------------------------------------------------------------
# app table: label, icon names (or a path marker), emblem, palette A, palette B
# ---------------------------------------------------------------------------
L = lambda fn, *a, **k: (lambda I: fn(I, *a, **k))  # noqa: E731

APPS = [
    ("Alacritty", ["Alacritty"], L(g_terminal, flash=True), "fire", "sunset"),
    ("Ark", ["ark", "org.kde.ark"], L(g_box, zip_=True), "wood", "amber"),
    ("Audacity", ["org.audacityteam.Audacity", "audacity"], g_wave, "ocean", "candy"),
    ("Baldur's Gate 3", ["steam_icon_1086940"], g_d20, "violet", "gold"),
    ("BB Launcher", ["@bb_launcher"], L(g_tv, "pad"), "red", "steel"),
    ("Boxes", ["org.gnome.Boxes"], g_cube, "sky", "ocean"),
    ("Brave", ["brave-desktop", "brave-browser", "brave"], L(g_globe, "lock"), "sunset", "silver"),
    ("Browning African Safari", ["@browning_african_safari"], g_binoculars, "amber", "wood"),
    ("btop++", ["btop"], g_bars, "lime", "ocean"),
    ("Btrfs Assistant", ["btrfs-assistant"], g_layers, "ice", "ocean"),
    ("CachyOS Hello", ["org.cachyos.hello", "cachyos-hello"], g_hand, "mint", "ocean"),
    ("CachyOS Kernel Manager", ["org.cachyos.KernelManager"], L(g_chip, "K"), "mint", "ocean"),
    ("CachyOS Package Installer", ["cachyos-pi"], L(g_package, "down"), "mint", "sky"),
    ("Cachy-Update", ["cachy-update-blue", "cachy-update", "arch-update"], L(g_package, "cycle"), "sky", "mint"),
    ("CoD: World at War", ["steam_icon_10090"], L(g_helmet), "toxic", "steel"),
    ("chiaki-ng", ["io.github.streetpea.Chiaki4deck"], L(g_tv, "pad"), "ocean", "sky"),
    ("CMake", ["CMakeSetup", "cmake-gui", "cmake"], L(g_wrench), "rainbow", "steel"),
    ("Creamlinux", ["@creamlinux"], g_unlock, "pink", "ice"),
    ("Crusader Kings III", ["steam_icon_1158310"], g_crown, "gold", "red"),
    ("CurseForge", ["@curseforge"], L(g_pickaxe, puzzle=True), "steel", "fire"),
    ("Discord", ["discord"], g_chat, "violet", "ocean"),
    ("Dolphin Emulator", ["org.DolphinEmu.dolphin-emu"], g_ocean_disc, "ocean", "ice"),
    ("Dolphin", ["org.kde.dolphin", "system-file-manager"], g_folder, "gold", "amber"),
    ("Eden", ["@eden"], g_tree, "lime", "red"),
    ("eFootball", ["steam_icon_1665460"], g_ball, "lime", "ice"),
    ("Emoji Selector", ["preferences-desktop-emoticons"], g_smile, "gold", "sunset"),
    ("Enderal", ["steam_icon_976620"], L(g_scroll, "orb"), "amber", "violet"),
    ("Epic Games Launcher", ["@epic_games_launcher"], g_rocket, "silver", "steel"),
    ("Fallout 3", ["steam_icon_22370"], L(g_gasmask, "#7dff9a"), "toxic", "lime"),
    ("Fallout 4 VR", ["steam_icon_611660"], L(g_gasmask, "#7cf3ff"), "steel", "ocean"),
    ("Fallout: New Vegas", ["steam_icon_22380"], L(g_gasmask, "#ffc56b"), "amber", "sunset"),
    ("Filelight", ["filelight"], g_pie, "rainbow", "ocean"),
    ("File Roller", ["org.gnome.FileRoller", "file-roller"], L(g_box, roller=True), "amber", "wood"),
    ("Firefox", ["firefox"], L(g_globe, "orbit"), "ocean", "fire"),
    ("Flatseal", ["com.github.tchx84.Flatseal"], g_seal, "red", "ice"),
    ("Gang Beasts", ["steam_icon_285900"], g_glove, "red", "steel"),
    ("Gaupol", ["io.otsaloma.gaupol"], g_subtitles, "sunset", "ocean"),
    ("Gear Lever", ["it.mijorus.gearlever"], g_lever, "red", "steel"),
    ("GIMP", ["gimp"], g_brush, "wood", "violet"),
    ("Google Chrome", ["google-chrome"], L(g_globe, "chrome"), "sky", "silver"),
    ("GParted", ["gparted"], g_pie, "sunset", "ice"),
    ("Grub Customizer", ["grub-customizer"], L(g_list, pencil=True), "lime", "violet"),
    ("guitarix", ["gx_head", "guitarix"], L(g_guitar, amp=True), "fire", "steel"),
    ("Gwenview", ["gwenview"], g_photo, "sky", "lime"),
    ("lstopo", ["hwloc", "lstopo"], g_topology, "violet", "ocean"),
    ("Haruna", ["haruna"], g_clapper, "candy", "ocean"),
    ("Heroic Games Launcher", ["com.heroicgameslauncher.hgl"], L(g_shield, sword=True), "ocean", "ice"),
    ("HP Device Manager", ["@hp_device_manager"], g_hp_tool, "sky", "ocean"),
    ("HP Scan", ["@hp_scan"], L(g_printer, scan=True), "sky", "ice"),
    ("Hypnotix", ["hypnotix"], L(g_tv, "spiral"), "candy", "violet"),
    ("Info Center", ["hwinfo"], g_info_chip, "ocean", "sky"),
    ("IPTVnator", ["@iptvnator"], L(g_tv, "play"), "red", "sunset"),
    ("ISO Image Writer", ["org.kde.isoimagewriter"], g_isotope, "ocean", "silver"),
    ("ISO Master", ["@isomaster"], L(g_magnify), "silver", "sky"),
    ("Jackify", ["com.jackify.app", "@jackify"], g_mods_stack, "violet", "candy"),
    ("Kate", ["kate", "org.kde.kate"], L(g_doc), "ocean", "sky"),
    ("KCalc", ["accessories-calculator", "kcalc"], g_calc, "steel", "sunset"),
    ("KDE Connect", ["kdeconnect", "org.kde.kdeconnect"], g_phone_link, "mint", "sky"),
    ("KDE Partition Manager", ["partitionmanager"], g_pie, "ocean", "lime"),
    ("System Settings", ["preferences-system", "systemsettings"], g_gear, "steel", "ocean"),
    ("Konsole", ["utilities-terminal", "org.kde.konsole", "konsole"], g_terminal, "lime", "mint"),
    ("KRDC", ["krdc"], g_remote, "sky", "ocean"),
    ("KRename", ["krename"], g_tag, "amber", "sky"),
    ("KWalletManager", ["kwalletmanager"], g_wallet, "wood", "gold"),
    ("KWrite", ["kwrite"], L(g_pencil), "sunset", "ice"),
    ("Lutris", ["net.lutris.Lutris", "lutris"], g_joystick, "amber", "steel"),
    ("Manage Printing", ["cups"], g_printer, "steel", "ocean"),
    ("Mario Kart DX GP", ["@mario_kart_dx_gp"], g_kart, "red", "fire"),
    ("Meld", ["org.gnome.Meld", "meld"], g_doc_diff, "violet", "ice"),
    ("melonDS", ["net.kuribo64.melonDS"], L(g_handheld, dual=True), "pink", "silver"),
    ("Menu Editor", ["kmenuedit"], L(g_list, pencil=True), "sky", "fire"),
    ("Mesen", ["MesenIcon", "mesen"], g_cartridge, "red", "steel"),
    ("Micro", ["micro"], L(g_textcursor, "µ"), "lime", "ice"),
    ("Minecraft Bedrock Launcher", ["io.mrarm.mcpelauncher"], g_block_pick, "toxic", "steel"),
    ("MKVToolNix", ["mkvtoolnix-gui"], lambda I: (g_film(I), g_wrench(I, 6, 6, "#c9cfd8")), "ocean", "steel"),
    ("mpv", ["mpv"], L(g_play), "violet", "candy"),
    ("Nemo", ["nemo"], g_folder, "lime", "gold"),
    ("OBS Studio", ["com.obsproject.Studio", "obs"], g_record, "steel", "silver"),
    ("OpenMW CS", ["openmw-cs"], L(g_scroll, "pencil"), "amber", "wood"),
    ("OpenMW Launcher", ["openmw"], L(g_scroll, "mushroom"), "amber", "violet"),
    ("Overcooked", ["steam_icon_448510"], g_chef, "red", "steel"),
    ("Parsec", ["@parsec", "parsecd"], g_stream, "ocean", "candy"),
    ("PhotoCraft", ["ai.storyteller.photocraft", "@photocraft"], g_photo_spark, "candy", "gold"),
    ("PipeASIO Settings", ["pipeasio"], g_sliders, "fire", "ocean"),
    ("Plex", ["tv.plex.PlexDesktop"], lambda I: (g_film(I), I.s(P((20, 18), (29, 24), (20, 30)), "#ffffff", w=1.2)), "gold", "amber"),
    ("PortProton", ["ru.linux_gaming.PortProton"], g_wineglass, "red", "silver"),
    ("PPSSPP", ["org.ppsspp.PPSSPP"], L(g_handheld, wide=True), "silver", "ocean"),
    ("PrimeHack", ["io.github.shiiion.primehack"], g_target, "fire", "lime"),
    ("Private Internet Access", ["piavpn"], g_tunnel, "lime", "steel"),
    ("Protontricks", ["com.github.Matoking.protontricks"], L(g_wand, hat=True), "violet", "ocean"),
    ("ProtonUp-Qt", ["net.davidotek.pupgui2"], g_atom_up, "fire", "sky"),
    ("PS5Upload", ["@ps5upload"], lambda I: (g_monitor(I, I.B), g_arrow_up(I, 24, 21, 0.62, I.A)), "ice", "ocean"),
    ("qBittorrent", ["qbittorrent", "org.qbittorrent.qBittorrent"], g_swarm, "sky", "ocean"),
    ("qpwgraph", ["org.rncbc.qpwgraph", "qpwgraph"], g_nodes, "fire", "ocean"),
    ("Qt Assistant", ["assistant"], L(g_book, q=True), "lime", "sky"),
    ("Qt D-Bus Viewer", ["qdbusviewer"], g_dbus, "lime", "steel"),
    ("Qt Linguist", ["linguist"], g_bubbles_lang, "lime", "ice"),
    ("Qt V4L2 Test", ["qv4l2"], L(g_webcam), "steel", "lime"),
    ("Qt V4L2 Capture", ["qvidcap"], L(g_webcam, rec=True), "steel", "ocean"),
    ("Qt Widgets Designer", ["designer"], g_window_pencil, "lime", "ocean"),
    ("Raft", ["steam_icon_648800"], g_raft, "wood", "ice"),
    ("Refresher", ["@refresher"], g_cycle, "mint", "sky"),
    ("Remmina", ["org.remmina.Remmina", "remmina"], g_remote, "red", "steel"),
    ("RetroArch", ["org.libretro.RetroArch", "retroarch"], g_joystick, "rainbow", "steel"),
    ("Rocksmith 2014", ["steam_icon_221680"], g_guitar, "fire", "steel"),
    ("SchedExt Manager", ["org.cachyos.scx-manager"], L(g_clock, chip=True), "mint", "steel"),
    ("ScummVM", ["org.scummvm.ScummVM", "scummvm"], lambda I: (g_magnify(I, -2, -2), g_cursor_small(I)), "lime", "violet"),
    ("Shelly", ["shelly", "com.shellyorg.shelly"], g_shell, "pink", "ocean"),
    ("Slippi Launcher", ["@slippi_launcher"], g_two_pads, "lime", "violet"),
    ("Spectacle", ["spectacle"], g_camera, "candy", "ocean"),
    ("Spotify", ["spotify-client", "spotify"], g_vinyl, "lime", "silver"),
    ("Stardew Valley", ["steam_icon_413150"], g_sprout, "lime", "wood"),
    ("Steam", ["steam"], lambda I: (g_controller(I), I.line("M34,13 C34,9 38,9 38,6 M28,13 C28,10 31,9 31,6", "#ffffff", 1.6, 0.85)), "steel", "ocean"),
    ("SteamVR", ["steam_icon_250820"], g_vr, "steel", "ocean"),
    ("Supermodel", ["com.supermodel3.Supermodel"], L(g_arcade), "ocean", "fire"),
    ("System Monitor", ["utilities-system-monitor", "org.kde.plasma-systemmonitor"], g_graph, "lime", "sky"),
    ("Tekno Parrot", ["@teknoparrot", "teknoparrot"], L(g_arcade, coin=True), "lime", "red"),
    ("Tenacity", ["tenacity"], L(g_wave, (6, 12, 8, 18, 14, 10, 16, 7, 11, 5)), "fire", "gold"),
    ("TES: Arena", ["steam_icon_1812290"], L(g_scroll, "map"), "amber", "red"),
    ("TES III: Morrowind", ["steam_icon_22320"], L(g_scroll, "mushroom"), "wood", "violet"),
    ("TES V: Skyrim SE", ["steam_icon_489830"], L(g_scroll, "snow"), "steel", "ice"),
    ("The Simpsons Game (Recomp)", ["@simpsons_recompiled"], g_retro_tv_pad, "gold", "sky"),
    ("TinyWiiBackupManager", ["@tinywiibackupmanager"], g_backup_disc, "silver", "sky"),
    ("Unleashed Recompiled", ["io.github.hedge_dev.unleashedrecomp"], g_speedshoe, "red", "sky"),
    ("UXTerm / XTerm", ["xterm-color_48x48", "xterm"], L(g_terminal), "silver", "lime"),
    ("Valheim", ["steam_icon_892970"], L(g_helmet, horns=True), "steel", "wood"),
    ("Vim", ["gvim", "vim"], L(g_key, "ESC"), "lime", "steel"),
    ("Virtual Machine Manager", ["virt-manager"], lambda I: (g_monitor(I), g_cube_small(I)), "ocean", "steel"),
    ("VLC", ["vlc"], g_clapper, "fire", "sunset"),
    ("Volume Control", ["org.pulseaudio.pavucontrol", "pavucontrol"], g_speaker, "sky", "lime"),
    ("vrmonitor", ["application-x-vrmonitor"], lambda I: (g_vr(I), g_wifi(I, 24, 13)), "steel", "lime"),
    ("WARDOGS", ["steam_icon_1867240"], g_tank, "toxic", "steel"),
    ("Waterpark Simulator", ["steam_icon_3293260"], g_slide, "sunset", "ocean"),
    ("Wii Backup Fusion", ["@wii_backup_fusion"], g_backup_disc, "ice", "lime"),
    ("Winetricks", ["winetricks"], g_wand, "candy", "ocean"),
    ("xemu", ["app.xemu.xemu"], g_console_disc, "toxic", "lime"),
]


def g_cursor_small(I):
    I.s(P((30, 26), (40, 35), (35.5, 35.5), (38, 40.5), (36, 41.5), (33.5, 36.5), (30, 39.5)), "#ffffff", w=1.6)


def g_cube_small(I):
    I.s(P((24, 14), (31, 17.5), (24, 21), (17, 17.5)), "#ffffff", w=1.2)
    I.s(P((17, 17.5), (24, 21), (24, 28), (17, 24.5)), I.B, w=1.2)
    I.s(P((31, 17.5), (24, 21), (24, 28), (31, 24.5)), "#c9cfd8", w=1.2)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build():
    import shutil
    if os.path.isdir(THEME):
        shutil.rmtree(THEME)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(THEME, "index.theme"), "w") as fh:
        fh.write(INDEX)
    manifest = []
    for label, names, emblem, a, b in APPS:
        I = Icon(a, b)
        tile_back(I)
        emblem(I)
        tile_front(I)
        svg = I.d.svg(48, 48)
        files = []
        for n in names:
            fn = ("cachy7-app-" + n[1:]) if n.startswith("@") else n
            with open(os.path.join(OUT, fn + ".svg"), "w") as fh:
                fh.write(svg)
            files.append(fn)
        manifest.append({"label": label, "icons": files})
    with open(os.path.join(ROOT, "tools", "appicons.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    print(len(APPS), "app icons,", sum(len(m["icons"]) for m in manifest), "files")


if __name__ == "__main__":
    build()
