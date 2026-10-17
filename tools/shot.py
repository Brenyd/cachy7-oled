#!/usr/bin/env python3
"""Render an HTML file (or string) to PNG with headless Chromium."""
import sys
from playwright.sync_api import sync_playwright


def shot(html_path, out_png, width=1600, height=1000, scale=1, full_page=True):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": width, "height": height}, device_scale_factor=scale)
        pg.goto("file://" + html_path)
        pg.wait_for_timeout(400)
        errs = pg.evaluate("window.__errors || []")
        pg.screenshot(path=out_png, full_page=full_page)
        b.close()
        return errs


if __name__ == "__main__":
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
    s = float(sys.argv[5]) if len(sys.argv) > 5 else 1
    print(shot(sys.argv[1], sys.argv[2], w, h, s))
