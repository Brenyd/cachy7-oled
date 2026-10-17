#!/usr/bin/env python3
"""Start orb layers + wallpaper source SVG."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import Doc  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/Cachy7-OLED"
IMG = OUT + "/plasma/plasmoids/org.cachy7.startmenu/contents/images/"
TEAL, BLUE = "#19d3b4", "#3b8eea"


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(s)


def orb_base():
    d = Doc()
    body = d.rgrad([(0, "#14394a", 1), (0.55, "#061018", 1), (1, "#000000", 1)], 32, 44, 34)
    rim = d.rgrad([(0.80, TEAL, 0), (0.93, TEAL, 0.55), (0.985, BLUE, 0.9), (1, BLUE, 0)], 32, 32, 30)
    low = d.rgrad([(0, TEAL, 0.55), (1, TEAL, 0)], 32, 56, 22,
                  transform="translate(32 56) scale(1 0.55) translate(-32 -56)")
    d.add('<circle cx="32" cy="32" r="31.5" fill="#000000"/>')
    d.add('<circle cx="32" cy="32" r="31" fill="#ffffff" fill-opacity="0.32"/>')
    d.add(f'<circle cx="32" cy="32" r="30" fill="{body}"/>')
    d.add(f'<circle cx="32" cy="32" r="30" fill="{low}"/>')
    d.add(f'<circle cx="32" cy="32" r="30" fill="{rim}"/>')
    return d.svg(64, 64)


def orb_glow():
    d = Doc()
    g = d.rgrad([(0, "#7af3ff", 0.85), (0.5, TEAL, 0.45), (1, BLUE, 0)], 32, 50, 30,
                transform="translate(32 50) scale(1 0.8) translate(-32 -50)")
    rim = d.rgrad([(0.86, "#9fe9ff", 0), (0.97, "#c8f6ff", 0.95), (1, "#9fe9ff", 0)], 32, 32, 30.5)
    d.add(f'<circle cx="32" cy="32" r="30" fill="{g}"/>')
    d.add(f'<circle cx="32" cy="32" r="30.5" fill="{rim}"/>')
    return d.svg(64, 64)


def orb_gloss():
    d = Doc()
    g = d.grad([(0, "#ffffff", 0.42), (0.75, "#ffffff", 0.04), (1, "#ffffff", 0)], 0, 3, 0, 32)
    d.add(f'<path d="M6,26 C6,12 18,3.5 32,3.5 C46,3.5 58,12 58,26 C50,22 42,21 32,21 C22,21 14,22 6,26 Z" fill="{g}"/>')
    d.add('<ellipse cx="32" cy="58.5" rx="12" ry="1.8" fill="#ffffff" fill-opacity="0.18"/>')
    return d.svg(64, 64)


def wallpaper_svg():
    # Rendered by Chromium to PNG (filters are fine here; Plasma only sees the PNG).
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs>
 <filter id="b40" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
 <filter id="b12" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
 <filter id="b3" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter>
 <linearGradient id="r1" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset="0.35" stop-color="{BLUE}" stop-opacity="0.9"/>
  <stop offset="0.7" stop-color="{TEAL}" stop-opacity="0.9"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>
 <linearGradient id="r2" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#7cc4ff" stop-opacity="0"/><stop offset="0.5" stop-color="#bfe6ff" stop-opacity="1"/>
  <stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>
 <radialGradient id="glow" cx="1300" cy="760" r="900" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="#0b2a3a" stop-opacity="0.55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1920" height="1080" fill="#000"/>
<rect width="1920" height="1080" fill="url(#glow)"/>
<g fill="none" stroke-linecap="round">
 <path d="M-100,900 C400,820 700,520 1100,560 S1700,860 2050,600" stroke="url(#r1)" stroke-width="150" opacity="0.35" filter="url(#b40)"/>
 <path d="M-100,960 C450,880 760,610 1150,640 S1750,900 2050,700" stroke="url(#r1)" stroke-width="60" opacity="0.55" filter="url(#b12)"/>
 <path d="M-100,930 C420,850 730,570 1120,600 S1720,880 2050,650" stroke="url(#r2)" stroke-width="6" opacity="0.85" filter="url(#b3)"/>
 <path d="M-100,1000 C500,930 820,700 1200,720 S1800,960 2050,780" stroke="url(#r2)" stroke-width="3" opacity="0.55" filter="url(#b3)"/>
 <path d="M200,1080 C600,980 900,780 1300,800 S1800,1000 2050,900" stroke="url(#r1)" stroke-width="40" opacity="0.30" filter="url(#b12)"/>
</g>
</svg>"""


if __name__ == "__main__":
    write(IMG + "orb-base.svg", orb_base())
    write(IMG + "orb-glow.svg", orb_glow())
    write(IMG + "orb-gloss.svg", orb_gloss())
    write(os.path.join(OUT, "tools", "wallpaper.svg"), wallpaper_svg())
    print("orb + wallpaper svg written")
