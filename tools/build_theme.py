#!/usr/bin/env python3
"""Generates: color scheme, Plasma style (desktoptheme), Aurorae window decoration."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import Doc, Ring, Interior, nine_slice, rgba, f  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/Cachy7-OLED"
AUTHOR = [{"Name": "Cachy7 OLED"}]


def w(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


WHITE = "#ffffff"
BLACK = "#000000"
AERO = "#3b8eea"
AERO_GLOW = "#6fb4ff"

# ---------------------------------------------------------------------------
# Color scheme (OLED black + Aero blue)
# ---------------------------------------------------------------------------
COLORS = """[ColorEffects:Disabled]
Color=56,56,56
ColorAmount=0
ColorEffect=0
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color=112,111,110
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate=22,32,46
BackgroundNormal=16,18,22
DecorationFocus=59,142,234
DecorationHover=111,180,255
ForegroundActive=111,180,255
ForegroundInactive=138,143,152
ForegroundLink=79,163,255
ForegroundNegative=255,85,85
ForegroundNeutral=242,179,61
ForegroundNormal=232,234,237
ForegroundPositive=63,207,110
ForegroundVisited=164,128,255

[Colors:Complementary]
BackgroundAlternate=10,12,16
BackgroundNormal=0,0,0
DecorationFocus=59,142,234
DecorationHover=111,180,255
ForegroundActive=111,180,255
ForegroundInactive=138,143,152
ForegroundLink=79,163,255
ForegroundNegative=255,85,85
ForegroundNeutral=242,179,61
ForegroundNormal=232,234,237
ForegroundPositive=63,207,110
ForegroundVisited=164,128,255

[Colors:Header]
BackgroundAlternate=8,10,13
BackgroundNormal=0,0,0
DecorationFocus=59,142,234
DecorationHover=111,180,255
ForegroundActive=111,180,255
ForegroundInactive=138,143,152
ForegroundLink=79,163,255
ForegroundNegative=255,85,85
ForegroundNeutral=242,179,61
ForegroundNormal=232,234,237
ForegroundPositive=63,207,110
ForegroundVisited=164,128,255

[Colors:Header][Inactive]
BackgroundAlternate=8,10,13
BackgroundNormal=0,0,0
DecorationFocus=59,142,234
DecorationHover=111,180,255
ForegroundActive=111,180,255
ForegroundInactive=120,124,130
ForegroundLink=79,163,255
ForegroundNegative=255,85,85
ForegroundNeutral=242,179,61
ForegroundNormal=180,184,190
ForegroundPositive=63,207,110
ForegroundVisited=164,128,255

[Colors:Selection]
BackgroundAlternate=22,80,150
BackgroundNormal=30,102,188
DecorationFocus=59,142,234
DecorationHover=111,180,255
ForegroundActive=255,255,255
ForegroundInactive=200,220,245
ForegroundLink=210,232,255
ForegroundNegative=255,150,150
ForegroundNeutral=255,210,130
ForegroundNormal=255,255,255
ForegroundPositive=150,240,180
ForegroundVisited=220,200,255

[Colors:Tooltip]
BackgroundAlternate=14,18,24
BackgroundNormal=6,8,11
DecorationFocus=59,142,234
DecorationHover=111,180,255
ForegroundActive=111,180,255
ForegroundInactive=138,143,152
ForegroundLink=79,163,255
ForegroundNegative=255,85,85
ForegroundNeutral=242,179,61
ForegroundNormal=232,234,237
ForegroundPositive=63,207,110
ForegroundVisited=164,128,255

[Colors:View]
BackgroundAlternate=9,10,12
BackgroundNormal=0,0,0
DecorationFocus=59,142,234
DecorationHover=111,180,255
ForegroundActive=111,180,255
ForegroundInactive=138,143,152
ForegroundLink=79,163,255
ForegroundNegative=255,85,85
ForegroundNeutral=242,179,61
ForegroundNormal=232,234,237
ForegroundPositive=63,207,110
ForegroundVisited=164,128,255

[Colors:Window]
BackgroundAlternate=10,12,15
BackgroundNormal=0,0,0
DecorationFocus=59,142,234
DecorationHover=111,180,255
ForegroundActive=111,180,255
ForegroundInactive=138,143,152
ForegroundLink=79,163,255
ForegroundNegative=255,85,85
ForegroundNeutral=242,179,61
ForegroundNormal=232,234,237
ForegroundPositive=63,207,110
ForegroundVisited=164,128,255

[General]
ColorScheme=Cachy7OLED
Name=Cachy7 OLED
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground=0,0,0
activeBlend=255,255,255
activeForeground=255,255,255
inactiveBackground=0,0,0
inactiveBlend=150,150,150
inactiveForeground=150,150,150
"""


def color_scheme():
    w("color-schemes/Cachy7OLED.colors", COLORS)


# ---------------------------------------------------------------------------
# Plasma style
# ---------------------------------------------------------------------------
PT = "plasma/desktoptheme/cachy7-oled/"


def glass_stops(top_a, mid_a, low_a, bottom_rgb, bottom_a, split=0.48):
    """Win7 'split gloss': bright upper half, hard step, glow at the bottom."""
    return [
        (0.0, WHITE, top_a),
        (split, WHITE, mid_a),
        (split + 0.02, WHITE, low_a),
        (1.0, bottom_rgb, bottom_a),
    ]


def panel_background(solid=False):
    d = Doc()
    k = 1.0 if solid else 0.0
    L = T = R = B = 4
    mh = 32  # so the gloss split lands around the middle of a ~40px taskbar
    H = T + mh + B
    g = d.grad(
        [
            (0.0, "#1b2230", 0.82 + 0.18 * k),
            (0.46, "#0b0e14", 0.84 + 0.16 * k),
            (0.50, "#000000", 0.88 + 0.12 * k),
            (1.0, "#000000", 0.92 + 0.08 * k),
        ],
        0, 0, 0, H,
    )
    layers = [
        Interior(2, 1, g),
        Ring(0, 1, 3, rgba(255, 255, 255, 0.24)),
        Ring(1, 1, 2, rgba(110, 175, 255, 0.16)),
    ]
    W, H = nine_slice(d, "", L, T, R, B, layers, mh=mh)
    return d.svg(W, H)


TASK_STATES = {
    # name: (outer ring, inner ring, top_a, mid_a, low_a, bottom color, bottom alpha)
    "normal": (rgba(255, 255, 255, 0.27), rgba(255, 255, 255, 0.09), 0.15, 0.07, 0.00, "#5aa0ff", 0.12),
    "minimized": (rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.04), 0.06, 0.03, 0.00, "#5aa0ff", 0.05),
    "focus": (rgba(255, 255, 255, 0.45), rgba(255, 255, 255, 0.20), 0.30, 0.15, 0.04, "#4f9dff", 0.38),
    "hover": (rgba(150, 205, 255, 0.60), rgba(255, 255, 255, 0.22), 0.24, 0.12, 0.05, "#3f9bff", 0.55),
    "normal-hover": (rgba(150, 205, 255, 0.60), rgba(255, 255, 255, 0.22), 0.24, 0.12, 0.05, "#3f9bff", 0.55),
    "focus-hover": (rgba(175, 220, 255, 0.75), rgba(255, 255, 255, 0.30), 0.32, 0.16, 0.07, "#4fa8ff", 0.70),
    "minimized-hover": (rgba(150, 205, 255, 0.50), rgba(255, 255, 255, 0.18), 0.20, 0.10, 0.04, "#3f9bff", 0.45),
    "launcher-hover": (rgba(150, 205, 255, 0.45), rgba(255, 255, 255, 0.16), 0.18, 0.09, 0.03, "#3f9bff", 0.40),
    "attention": (rgba(255, 196, 110, 0.85), rgba(255, 240, 200, 0.35), 0.30, 0.18, 0.10, "#ff8a00", 0.85),
    "attention-hover": (rgba(255, 210, 140, 0.95), rgba(255, 245, 215, 0.45), 0.36, 0.22, 0.12, "#ff9a20", 0.95),
}


def tasks_svg():
    d = Doc()
    L = T = R = B = 4
    mw, mh = 28, 28
    oy = 0
    Wmax = 0
    for name, (outer, inner, ta, ma, la, brgb, ba) in TASK_STATES.items():
        H = T + mh + B
        g = d.grad(glass_stops(ta, ma, la, brgb, ba), 0, oy, 0, oy + H)
        layers = [
            Interior(2, 1, g),
            Ring(0, 1, 3, outer),
            Ring(1, 1, 2, inner),
        ]
        W, H = nine_slice(d, name, L, T, R, B, layers, ox=0, oy=oy, mw=mw, mh=mh)
        Wmax = max(Wmax, W)
        oy += H + 4
    return d.svg(Wmax, oy)


def dialog_like(corner, glass_w, rad, center_alpha=0.96, glass=True):
    """Win7 'glass frame' popup: light outer edge, blue-black glass band,
    dark separator + faint highlight, OLED-black content area."""
    d = Doc()
    c = corner
    mh = 60
    H = c * 2 + mh
    band = d.grad(
        [(0, "#2a3c56", 0.94), (0.5, "#141d2a", 0.94), (1, "#0b1018", 0.94)], 0, 0, 0, H
    ) if glass else rgba(0, 0, 0, center_alpha)
    layers = [
        Interior(c, 0, rgba(0, 0, 0, center_alpha)),
        Ring(0, 1, rad, rgba(255, 255, 255, 0.30)),
        Ring(1, glass_w, rad - 1, band),
        Ring(1, 1, rad - 1, rgba(140, 195, 255, 0.18)),
        Ring(1 + glass_w, 1, max(rad - 1 - glass_w, 0), rgba(0, 0, 0, 0.95)),
        Ring(2 + glass_w, 1, max(rad - 2 - glass_w, 0), rgba(255, 255, 255, 0.10)),
    ]
    W, H = nine_slice(d, "", c, c, c, c, layers, mh=mh)
    return d.svg(W, H)


def widget_background():
    d = Doc()
    c = 8
    layers = [
        Interior(2, 5, rgba(0, 0, 0, 0.90)),
        Ring(0, 1, 7, rgba(255, 255, 255, 0.16)),
        Ring(1, 1, 6, rgba(110, 175, 255, 0.07)),
    ]
    W, H = nine_slice(d, "", c, c, c, c, layers)
    return d.svg(W, H)


def plasma_style():
    meta = {
        "KPlugin": {
            "Authors": AUTHOR,
            "Description": "Windows 7 Aero inspired glass taskbar on an OLED-black base, with a CachyOS twist",
            "Id": "cachy7-oled",
            "License": "GPL-2.0-or-later",
            "Name": "Cachy7 OLED",
            "Version": "1.0",
        },
        "X-Plasma-API-Minimum-Version": "6.0",
    }
    w(PT + "metadata.json", json.dumps(meta, indent=2) + "\n")
    w(PT + "colors", COLORS)
    w(
        PT + "plasmarc",
        "[ContrastEffect]\nenabled=true\ncontrast=0.25\nintensity=0.6\nsaturation=1.6\n\n"
        "[BlurBehindEffect]\nenabled=true\n\n[AdaptiveTransparency]\nenabled=true\n",
    )
    w(PT + "widgets/panel-background.svg", panel_background())
    w(PT + "solid/widgets/panel-background.svg", panel_background(solid=True))
    w(PT + "opaque/widgets/panel-background.svg", panel_background(solid=True))
    w(PT + "widgets/tasks.svg", tasks_svg())
    w(PT + "dialogs/background.svg", dialog_like(8, 5, 7))
    w(PT + "solid/dialogs/background.svg", dialog_like(8, 5, 7, center_alpha=1.0))
    w(PT + "opaque/dialogs/background.svg", dialog_like(8, 5, 7, center_alpha=1.0))
    w(PT + "widgets/tooltip.svg", dialog_like(5, 2, 4))
    w(PT + "solid/widgets/tooltip.svg", dialog_like(5, 2, 4, center_alpha=1.0))
    w(PT + "widgets/background.svg", widget_background())
    w(PT + "solid/widgets/background.svg", widget_background())


# ---------------------------------------------------------------------------
# Aurorae decoration
# ---------------------------------------------------------------------------
AU = "aurorae/themes/Cachy7OLED/"
P = 10          # shadow padding
BORDER = 6      # visible frame thickness
TITLE_EDGE_TOP, TITLE_H, TITLE_EDGE_BOTTOM = 1, 22, 5
TOPB = TITLE_EDGE_TOP + TITLE_H + TITLE_EDGE_BOTTOM  # 28
RAD = 6


def deco_set(d, prefix, active, oy):
    L = R = B = P + BORDER
    T = P + TOPB
    mh = 20
    H = T + mh + B
    if active:
        tone = [(0, "#232c3a"), (0.42, "#141922"), (0.46, "#07090c"), (1, "#020203")]
    else:
        tone = [(0, "#16191e"), (0.42, "#0d0f12"), (0.46, "#060607"), (1, "#020202")]
    # absolute stops: title starts at y=P, ends at y=T, the rest is OLED black
    stops = [(P / H, tone[0][1], 1)]
    for o, c in tone[1:]:
        stops.append(((P + o * TOPB) / H, c, 1))
    stops.append((T / H + 0.001, BLACK, 1))
    stops.append((1, BLACK, 1))
    stops = [(0, tone[0][1], 1)] + stops
    g = d.grad(stops, 0, oy, 0, oy + H)

    k = 1.0 if active else 0.6
    layers = [Interior(P + 2, RAD - 2, g)]
    for i in range(P):
        a = 0.30 * k * ((i + 1) / P) ** 2.2
        layers.append(Ring(i, 1, RAD + (P - i), rgba(0, 0, 0, a)))
    layers += [
        Ring(P, 1, RAD, rgba(255, 255, 255, 0.32 if active else 0.24)),
        Ring(P + 1, 1, RAD - 1, rgba(120, 180, 255, 0.24) if active else rgba(255, 255, 255, 0.05)),
        Ring((P + BORDER - 1, T - 1, P + BORDER - 1, P + BORDER - 1), 1, 0,
             rgba(255, 255, 255, 0.12 if active else 0.10)),
    ]
    W, H = nine_slice(d, prefix, L, T, R, B, layers, oy=oy, mh=mh)
    return W, H


def deco_max_set(d, prefix, active, oy):
    mh = 24
    H = mh + 2
    if active:
        g = d.grad([(0, "#1f2733", 1), (0.46, "#11161d", 1), (0.5, "#06080a", 1), (1, "#000000", 1)], 0, oy + 1, 0, oy + 1 + mh)
    else:
        g = d.grad([(0, "#14171b", 1), (0.46, "#0b0d10", 1), (0.5, "#050506", 1), (1, "#000000", 1)], 0, oy + 1, 0, oy + 1 + mh)
    layers = [Interior(0, 0, g)]
    W, H = nine_slice(d, prefix, 1, 1, 1, 1, layers, oy=oy, mh=mh)
    return W, H


def decoration_svg():
    d = Doc()
    oy = 0
    Wm = 0
    for prefix, active, fn in [
        ("decoration", True, deco_set),
        ("decoration-inactive", False, deco_set),
        ("decoration-maximized", True, deco_max_set),
        ("decoration-maximized-inactive", False, deco_max_set),
    ]:
        W, H = fn(d, prefix, active, oy)
        Wm = max(Wm, W)
        oy += H + 6
    return d.svg(Wm, oy)


# Win7 caption buttons --------------------------------------------------------
BTN_W, BTN_H, CLOSE_W = 26, 19, 43
STATES = ["active", "hover", "pressed", "inactive", "deactivated"]


def btn_shape(x, y, w_, h, round_left, round_right, r=5):
    """Top edge flat (buttons hang from the window top), chosen bottom corners rounded."""
    x1, y1 = x + w_, y + h
    p = f"M{f(x)},{f(y)} L{f(x1)},{f(y)} "
    if round_right:
        p += f"L{f(x1)},{f(y1-r)} A{r},{r} 0 0 1 {f(x1-r)},{f(y1)} "
    else:
        p += f"L{f(x1)},{f(y1)} "
    if round_left:
        p += f"L{f(x+r)},{f(y1)} A{r},{r} 0 0 1 {f(x)},{f(y1-r)} "
    else:
        p += f"L{f(x)},{f(y1)} "
    return p + "Z"


def palette(kind, state):
    """Return (stops for body, outer edge color, inner highlight alpha, glow color/alpha, glyph color)."""
    if kind == "close":
        P_ = {
            "active": ([(0, "#f2a594"), (0.48, "#cf5a45"), (0.5, "#b12e19"), (1, "#d84a2c")], "#2a0703", 0.40, ("#ff7a45", 0.55), "#ffffff"),
            "hover": ([(0, "#ffc0ad"), (0.48, "#ea6d52"), (0.5, "#d23a1c"), (1, "#ff6a2c")], "#3a0a03", 0.55, ("#ffd27a", 0.75), "#ffffff"),
            "pressed": ([(0, "#c86a58"), (0.48, "#9c3221"), (0.5, "#7e1a0a"), (1, "#a8321a")], "#1e0402", 0.20, ("#ff5a2a", 0.40), "#f0f0f0"),
            "inactive": ([(0, "#3a3f48"), (0.48, "#22262d"), (0.5, "#15181d"), (1, "#1b1e24")], "#000000", 0.18, ("#ffffff", 0.0), "#9da3ad"),
            "deactivated": ([(0, "#2a2d33"), (0.48, "#1b1d21"), (0.5, "#121316"), (1, "#16181b")], "#000000", 0.10, ("#ffffff", 0.0), "#5d626a"),
        }
    else:
        P_ = {
            "active": ([(0, "#4b5566"), (0.48, "#2a313c"), (0.5, "#151a21"), (1, "#1d2530")], "#000000", 0.30, ("#5aa6ff", 0.25), "#ffffff"),
            "hover": ([(0, "#a9d4ff"), (0.48, "#4a93df"), (0.5, "#1f5fae"), (1, "#3c9cff")], "#03122a", 0.50, ("#7ad0ff", 0.80), "#ffffff"),
            "pressed": ([(0, "#5d87b4"), (0.48, "#2b5d93"), (0.5, "#163e6e"), (1, "#245e9e")], "#020a18", 0.20, ("#4aa0ff", 0.50), "#e8eef6"),
            "inactive": ([(0, "#30343b"), (0.48, "#1f2227"), (0.5, "#131518"), (1, "#181a1e")], "#000000", 0.16, ("#ffffff", 0.0), "#9da3ad"),
            "deactivated": ([(0, "#24272c"), (0.48, "#18191c"), (0.5, "#101113"), (1, "#141518"), ], "#000000", 0.08, ("#ffffff", 0.0), "#55595f"),
        }
    return P_[state]


def glyph(kind, cx, cy, color):
    """Bold Win7 glyph with a dark outline for legibility."""
    out = []
    if kind == "close":
        s, t = 4.6, 1.55
        d_ = (
            f"M{f(cx-s)},{f(cy-s+t)} L{f(cx-s+t)},{f(cy-s)} L{f(cx)},{f(cy-t)} L{f(cx+s-t)},{f(cy-s)} "
            f"L{f(cx+s)},{f(cy-s+t)} L{f(cx+t)},{f(cy)} L{f(cx+s)},{f(cy+s-t)} L{f(cx+s-t)},{f(cy+s)} "
            f"L{f(cx)},{f(cy+t)} L{f(cx-s+t)},{f(cy+s)} L{f(cx-s)},{f(cy+s-t)} L{f(cx-t)},{f(cy)} Z"
        )
        out.append(f'<path d="{d_}" fill="none" stroke="#000000" stroke-opacity="0.55" stroke-width="1.6" stroke-linejoin="round"/>')
        out.append(f'<path d="{d_}" fill="{color}"/>')
    elif kind == "minimize":
        d_ = f"M{f(cx-4.5)},{f(cy+1.5)} h9 v3 h-9 Z"
        out.append(f'<path d="{d_}" fill="none" stroke="#000000" stroke-opacity="0.55" stroke-width="1.6"/>')
        out.append(f'<path d="{d_}" fill="{color}"/>')
    elif kind == "maximize":
        d_ = (f"M{f(cx-5)},{f(cy-4)} h10 v8.5 h-10 Z M{f(cx-4)},{f(cy-1.5)} v5 h8 v-5 Z")
        out.append(f'<path d="{d_}" fill="none" stroke="#000000" stroke-opacity="0.55" stroke-width="1.6"/>')
        out.append(f'<path d="{d_}" fill-rule="evenodd" fill="{color}"/>')
    elif kind == "restore":
        back = f"M{f(cx-2.5)},{f(cy-5)} h8 v7 h-2 v-3.5 h-6 Z"
        front = f"M{f(cx-5.5)},{f(cy-1.5)} h8 v6.5 h-8 Z M{f(cx-4.5)},{f(cy+0.5)} v3 h6 v-3 Z"
        for d_, rule in ((back, "nonzero"), (front, "evenodd")):
            out.append(f'<path d="{d_}" fill="none" stroke="#000000" stroke-opacity="0.55" stroke-width="1.6"/>')
            out.append(f'<path d="{d_}" fill-rule="{rule}" fill="{color}"/>')
    return "".join(out)


def button_svg(kind):
    d = Doc()
    width = CLOSE_W if kind == "close" else BTN_W
    rl = kind == "minimize"
    rr = kind == "close"
    pal_kind = "close" if kind == "close" else "caption"
    y = 0
    for st in STATES:
        stops, edge, hi_a, (glow_c, glow_a), gcol = palette(pal_kind, st)
        body = d.grad([(o, c, 1) for o, c in stops], 0, y, 0, y + BTN_H)
        glow = d.rgrad([(0, glow_c, glow_a), (1, glow_c, 0)], width / 2, y + BTN_H, width * 0.55,
                       transform=f"translate(0 {f(y+BTN_H)}) scale(1 0.55) translate(0 {f(-(y+BTN_H))})")
        hi = d.grad([(0, WHITE, hi_a), (1, WHITE, hi_a * 0.25)], 0, y, 0, y + BTN_H)
        shape = btn_shape(0, y, width, BTN_H, rl, rr)
        inner = btn_shape(1, y, width - 2, BTN_H - 1, rl, rr, r=4)
        inner2 = btn_shape(2, y + 1, width - 4, BTN_H - 3, rl, rr, r=3)
        parts = [
            f'<rect x="0" y="{y}" width="{width}" height="{BTN_H}" fill="#000000" fill-opacity="0"/>',
            f'<path d="{shape}" fill="{edge}" fill-opacity="0.85"/>',
            f'<path d="{inner}" fill="{body}"/>',
            f'<path d="{inner}" fill="{glow}"/>',
            f'<path d="{inner} {inner2}" fill-rule="evenodd" fill="{hi}"/>',
        ]
        g_kind = kind
        parts.append(glyph(g_kind, width / 2, y + BTN_H / 2 - 0.5, gcol))
        d.add(f'<g id="{st}-center">' + "".join(parts) + "</g>")
        y += BTN_H + 3
    return d.svg(width, y)


def aurorae():
    w(AU + "decoration.svg", decoration_svg())
    for kind in ("close", "minimize", "maximize", "restore"):
        w(AU + f"{kind}.svg", button_svg(kind))
    w(
        AU + "Cachy7OLEDrc",
        f"""[General]
ActiveTextColor=255,255,255
InactiveTextColor=150,150,150
TitleAlignment=Left
TitleVerticalAlignment=Center
Animation=120
Shadow=true
DecorationPosition=0

[Layout]
BorderLeft={BORDER}
BorderRight={BORDER}
BorderBottom={BORDER}
TitleEdgeTop={TITLE_EDGE_TOP}
TitleEdgeBottom={TITLE_EDGE_BOTTOM}
TitleEdgeLeft=6
TitleEdgeRight=6
TitleEdgeTopMaximized=0
TitleEdgeBottomMaximized=2
TitleEdgeLeftMaximized=4
TitleEdgeRightMaximized=0
TitleBorderLeft=6
TitleBorderRight=8
TitleHeight={TITLE_H}
ButtonWidth={BTN_W}
ButtonWidthMinimize={BTN_W}
ButtonWidthMaximizeRestore={BTN_W}
ButtonWidthClose={CLOSE_W}
ButtonHeight={BTN_H}
ButtonSpacing=0
ButtonMarginTop=0
ExplicitButtonSpacer=8
PaddingTop={P}
PaddingBottom={P}
PaddingLeft={P}
PaddingRight={P}
""",
    )
    w(
        AU + "metadata.desktop",
        """[Desktop Entry]
Name=Cachy7 OLED
Comment=Windows 7 Aero inspired glass frame on OLED black
X-KDE-PluginInfo-Author=Cachy7 OLED
X-KDE-PluginInfo-Name=Cachy7OLED
X-KDE-PluginInfo-Version=1.0
X-KDE-PluginInfo-License=GPL
X-Plasma-API=declarativeappletscript
""",
    )
    w(
        AU + "metadata.json",
        json.dumps(
            {"KPlugin": {"Authors": AUTHOR, "Id": "Cachy7OLED", "Name": "Cachy7 OLED",
                         "Description": "Windows 7 Aero inspired glass frame on OLED black",
                         "License": "GPL-2.0-or-later", "Version": "1.0"}},
            indent=2,
        ) + "\n",
    )


if __name__ == "__main__":
    color_scheme()
    plasma_style()
    aurorae()
    print("theme parts written to", OUT)
