"""Tiny SVG helpers that only emit features QtSvg (Plasma/KSvg/Aurorae) renders:
paths, rects, linear/radial gradients, fill-opacity, evenodd. No filters/clips/masks
in anything Plasma itself renders."""

def f(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


class Doc:
    def __init__(self):
        self.defs = []
        self.body = []
        self._gid = 0

    def grad(self, stops, x1=0, y1=0, x2=0, y2=1, units="userSpaceOnUse", gid=None):
        """stops: list of (offset, color, opacity)."""
        self._gid += 1
        gid = gid or f"g{self._gid}"
        st = "".join(
            f'<stop offset="{f(o)}" stop-color="{c}" stop-opacity="{f(a)}"/>' for o, c, a in stops
        )
        self.defs.append(
            f'<linearGradient id="{gid}" gradientUnits="{units}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}">{st}</linearGradient>'
        )
        return f"url(#{gid})"

    def rgrad(self, stops, cx, cy, r, fx=None, fy=None, units="userSpaceOnUse", gid=None, transform=None):
        self._gid += 1
        gid = gid or f"r{self._gid}"
        st = "".join(
            f'<stop offset="{f(o)}" stop-color="{c}" stop-opacity="{f(a)}"/>' for o, c, a in stops
        )
        fxy = ""
        if fx is not None:
            fxy = f' fx="{f(fx)}" fy="{f(fy)}"'
        tr = f' gradientTransform="{transform}"' if transform else ""
        self.defs.append(
            f'<radialGradient id="{gid}" gradientUnits="{units}" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"{fxy}{tr}>{st}</radialGradient>'
        )
        return f"url(#{gid})"

    def add(self, s):
        self.body.append(s)

    def svg(self, w, h, extra_attrs=""):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{f(w)}" height="{f(h)}" viewBox="0 0 {f(w)} {f(h)}"{extra_attrs}>\n'
            f"<defs>{''.join(self.defs)}</defs>\n" + "\n".join(self.body) + "\n</svg>\n"
        )


def paint(fill):
    """fill = '#rrggbb' | ('#rrggbb', alpha) | 'url(#id)'"""
    if isinstance(fill, tuple):
        return f'fill="{fill[0]}" fill-opacity="{f(fill[1])}"'
    return f'fill="{fill}"'


def rgba(r, g, b, a):
    return (f"#{r:02x}{g:02x}{b:02x}", a)


# ---------------------------------------------------------------------------
# 9-slice frame generator (Plasma FrameSvg / Aurorae decoration layout).
# Every piece is a <g id=...> whose geometric bounds are exactly the piece rect,
# guaranteed by a transparent bounding rect.
# ---------------------------------------------------------------------------

class Ring:
    def __init__(self, insets, w, rad, fill):
        self.insets = insets if isinstance(insets, (tuple, list)) else (insets,) * 4
        self.w, self.rad, self.fill = w, rad, fill


class Interior:
    def __init__(self, insets, rad, fill):
        self.insets = insets if isinstance(insets, (tuple, list)) else (insets,) * 4
        self.rad, self.fill = rad, fill


def _region(name, ins, rad, geo):
    """Path (string) of the rounded rect with insets `ins` and radius `rad`
    intersected with piece `name`, or None if empty."""
    W, H, L, T, R, B, ox, oy = geo
    l, t, r, b = ins
    mw, mh = W - L - R, H - T - B

    def P(x, y):
        return f"{f(x + ox)},{f(y + oy)}"

    def rect(x0, y0, x1, y1):
        if x1 - x0 <= 1e-6 or y1 - y0 <= 1e-6:
            return None
        return f"M{P(x0,y0)} L{P(x1,y0)} L{P(x1,y1)} L{P(x0,y1)} Z"

    if name == "center":
        assert l <= L and t <= T and r <= R and b <= B, "layer does not cover center"
        return rect(L, T, L + mw, T + mh)
    if name == "top":
        return rect(L, max(t, 0), L + mw, T) if t < T else None
    if name == "bottom":
        return rect(L, T + mh, L + mw, H - b) if b < B else None
    if name == "left":
        return rect(l, T, L, T + mh) if l < L else None
    if name == "right":
        return rect(L + mw, T, W - r, T + mh) if r < R else None

    # corners, built in top-left space then mirrored
    if name == "topleft":
        il, it, PW, PH, mx, my = l, t, L, T, False, False
    elif name == "topright":
        il, it, PW, PH, mx, my = r, t, R, T, True, False
    elif name == "bottomleft":
        il, it, PW, PH, mx, my = l, b, L, B, False, True
    else:
        il, it, PW, PH, mx, my = r, b, R, B, True, True
    if il >= PW or it >= PH:
        return None
    rr = min(rad, PW - il, PH - it)

    def M(x, y):
        X = W - x if mx else x
        Y = H - y if my else y
        return P(X, Y)

    sweep = 0 if (mx ^ my) else 1
    if rr <= 0:
        return f"M{M(il,PH)} L{M(il,it)} L{M(PW,it)} L{M(PW,PH)} Z"
    return (
        f"M{M(il,PH)} L{M(il,it+rr)} A{f(rr)},{f(rr)} 0 0 {sweep} {M(il+rr,it)} "
        f"L{M(PW,it)} L{M(PW,PH)} Z"
    )


PIECES = ["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]


def nine_slice(doc, prefix, L, T, R, B, layers, ox=0, oy=0, mw=20, mh=20, only=None):
    """Append a full frame set to doc. Returns (W, H) of the frame canvas."""
    W, H = L + mw + R, T + mh + B
    geo = (W, H, L, T, R, B, ox, oy)
    rects = {
        "topleft": (0, 0, L, T), "top": (L, 0, mw, T), "topright": (L + mw, 0, R, T),
        "left": (0, T, L, mh), "center": (L, T, mw, mh), "right": (L + mw, T, R, mh),
        "bottomleft": (0, T + mh, L, B), "bottom": (L, T + mh, mw, B), "bottomright": (L + mw, T + mh, R, B),
    }
    for name in PIECES:
        if only and name not in only:
            continue
        x, y, w, h = rects[name]
        pid = f"{prefix}-{name}" if prefix else name
        parts = [f'<rect x="{f(x+ox)}" y="{f(y+oy)}" width="{f(w)}" height="{f(h)}" fill="#000000" fill-opacity="0"/>']
        for lay in layers:
            if isinstance(lay, Interior):
                p = _region(name, lay.insets, lay.rad, geo)
                if p:
                    parts.append(f'<path d="{p}" {paint(lay.fill)}/>')
            else:
                outer = _region(name, lay.insets, lay.rad, geo)
                if not outer:
                    continue
                ii = tuple(v + lay.w for v in lay.insets)
                inner = _region(name, ii, max(lay.rad - lay.w, 0), geo)
                d = outer + (" " + inner if inner else "")
                parts.append(f'<path d="{d}" fill-rule="evenodd" {paint(lay.fill)}/>')
        doc.add(f'<g id="{pid}">' + "".join(parts) + "</g>")
    return W, H
