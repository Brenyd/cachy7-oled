#!/usr/bin/env python3
"""Compose a 1920x1080 preview of the whole theme from the real theme files
(frames rendered by element id like KSvg does; start menu mirrors MenuView.qml)."""
import json

R = "/home/claude/Cachy7-OLED/"
IC = R + "icons/Cachy7/scalable/"
IMG = R + "plasma/plasmoids/org.cachy7.startmenu/contents/images/"
svgs = {
    "panel": R + "plasma/desktoptheme/cachy7-oled/widgets/panel-background.svg",
    "tasks": R + "plasma/desktoptheme/cachy7-oled/widgets/tasks.svg",
    "dialog": R + "plasma/desktoptheme/cachy7-oled/dialogs/background.svg",
    "tip": R + "plasma/desktoptheme/cachy7-oled/widgets/tooltip.svg",
    "deco": R + "aurorae/themes/Cachy7OLED/decoration.svg",
    "close": R + "aurorae/themes/Cachy7OLED/close.svg",
    "min": R + "aurorae/themes/Cachy7OLED/minimize.svg",
    "max": R + "aurorae/themes/Cachy7OLED/maximize.svg",
}
js = open("/home/claude/build/framesvg.js").read()
mounts = "".join(f"mountSvg({json.dumps(k)}, {json.dumps(open(v).read())});" for k, v in svgs.items())


def ic(cat, name):
    return f"file://{IC}{cat}/{name}.svg"


ICONS = {
    "folder": ic("places", "folder"), "docs": ic("places", "folder-documents"), "pics": ic("places", "folder-pictures"),
    "music": ic("places", "folder-music"), "videos": ic("places", "folder-videos"), "dl": ic("places", "folder-download"),
    "desk": ic("places", "user-desktop"), "home": ic("places", "user-home"), "trash": ic("places", "user-trash"),
    "trashfull": ic("places", "user-trash-full"), "net": ic("places", "network-workgroup"),
    "pc": ic("devices", "computer"), "hdd": ic("devices", "drive-harddisk"), "usb": ic("devices", "drive-removable-media"),
    "term": ic("apps", "utilities-terminal"), "settings": ic("apps", "preferences-system"), "fm": ic("apps", "system-file-manager"),
    "web": ic("apps", "internet-web-browser"), "user": ic("apps", "user-identity"), "txt": ic("mimetypes", "text-x-generic"),
    "orb_logo": ic("places", "start-here"),
}

CSS = """
*{box-sizing:border-box} body{margin:0;width:1920px;height:1080px;position:relative;overflow:hidden;
 font-family:'Noto Sans','Inter',sans-serif;font-size:13px;color:#e8eaed;background:#000 url(file:///home/claude/Cachy7-OLED/wallpapers/Cachy7OLED/contents/images/1920x1080.png) center/cover}
.abs{position:absolute}
.hl{border-radius:3px;border:1px solid rgba(143,204,255,.6);
 background:linear-gradient(rgba(128,194,255,.34),rgba(71,143,242,.22) 48%,rgba(36,102,217,.22) 52%,rgba(51,133,255,.40))}
.app{display:flex;align-items:center;gap:10px;height:40px;padding:0 8px;font-weight:600}
.app.small{height:28px;font-weight:400}
.app img{width:32px;height:32px}
.place{height:29px;line-height:29px;padding-left:9px;color:#fff}
.sep{height:1px;background:rgba(255,255,255,.14);margin:6px 9px}
.dicon{width:96px;text-align:center;font-size:12px;color:#fff;text-shadow:0 1px 3px #000,0 0 8px #000}
.dicon img{width:52px;height:52px;display:block;margin:0 auto 4px}
.fm-side div{display:flex;align-items:center;gap:8px;height:26px;padding-left:10px;font-size:12.5px}
.fm-side img{width:18px;height:18px}
.grid{display:flex;flex-wrap:wrap;align-items:flex-start;align-content:flex-start;gap:14px 10px;padding:16px}
.grid div{width:100px;text-align:center;font-size:12px;padding:6px 2px;border-radius:3px}
.grid img{width:64px;height:64px;display:block;margin:0 auto 4px}
"""


def html():
    I = ICONS
    desktop_icons = "".join(
        f'<div class="dicon abs" style="left:18px;top:{18+i*100}px"><img src="{I[k]}">{t}</div>'
        for i, (k, t) in enumerate([("pc", "Computer"), ("home", "Home"), ("trash", "Trash"), ("net", "Network")])
    )
    side = "".join(f'<div class="{"hl" if t=="Documents" else ""}"><img src="{I[k]}">{t}</div>' for k, t in [
        ("home", "Home"), ("desk", "Desktop"), ("docs", "Documents"), ("dl", "Downloads"), ("music", "Music"),
        ("pics", "Pictures"), ("videos", "Videos"), ("trash", "Trash"), ("pc", "Computer"), ("hdd", "NVMe 1TB"), ("usb", "USB Drive")])
    grid = "".join(f'<div class="{"hl" if t=="Projects" else ""}"><img src="{I[k]}">{t}</div>' for k, t in [
        ("folder", "Projects"), ("pics", "Screenshots"), ("music", "Soundtracks"), ("videos", "Clips"),
        ("folder", "Notes"), ("dl", "Installers"), ("txt", "readme.txt"), ("txt", "todo.md"), ("folder", "Backups")])

    pinned = [("web", "Web Browser"), ("fm", "Dolphin"), ("term", "Konsole"), ("settings", "System Settings")]
    freq = [("folder", "Steam"), ("pics", "Gwenview"), ("music", "Elisa"), ("txt", "Kate"), ("videos", "Haruna")]
    left = "".join(f'<div class="app {"hl" if t=="Konsole" else ""}"><img src="{I[k]}">{t}</div>' for k, t in pinned)
    left += '<div class="sep"></div>'
    left += "".join(f'<div class="app" style="font-weight:400"><img src="{I[k]}">{t}</div>' for k, t in freq)
    places = ["<b>gamer</b>", "Documents", "Pictures", "Music", "Videos", "Downloads", "SEP", "Computer", "System Settings", "Terminal", "Run…"]
    right = "".join('<div class="sep" style="margin:7px 6px;background:rgba(255,255,255,.16)"></div>' if p == "SEP"
                    else f'<div class="place {"hl" if p=="Documents" else ""}">{p}</div>' for p in places)

    MW, MH = 468, 540   # 26 x 30 grid units
    mx, my = 4, 1080 - 40 - MH - 16 - 6
    menu = f"""
<div class="abs" style="left:{mx+8}px;top:{my+8}px;width:{MW}px;height:{MH}px;display:flex;gap:7px">
  <div style="width:{round(MW*.63)}px;background:#000;border:1px solid rgba(255,255,255,.13);border-radius:4px;padding:5px;display:flex;flex-direction:column;gap:4px">
    <div style="flex:1">{left}</div>
    <div class="sep" style="margin:0 9px"></div>
    <div style="height:30px;line-height:30px;padding-left:11px;font-weight:700">&#9656;&nbsp; All Programs</div>
    <div style="height:30px;border-radius:3px;background:#0b0d11;border:1px solid rgba(110,178,255,.85);padding:0 10px;line-height:28px;color:rgba(255,255,255,.42);display:flex;justify-content:space-between">Search programs and files <span style="opacity:.75">&#128269;&#xFE0E;</span></div>
  </div>
  <div style="flex:1;border-radius:4px;border:1px solid rgba(255,255,255,.07);padding:6px;display:flex;flex-direction:column;
       background:linear-gradient(rgba(33,51,77,.6),rgba(13,20,31,.5) 55%,rgba(5,8,13,.5))">
    <div style="width:65px;height:65px;margin:4px auto 9px;border-radius:6px;border:1px solid rgba(255,255,255,.45);padding:4px;
         background:linear-gradient(rgba(255,255,255,.35),rgba(128,166,204,.25),rgba(51,77,115,.45))"><img src="{I['docs']}" style="width:100%;height:100%"></div>
    {right}
    <div style="flex:1"></div>
    <div style="display:flex;margin:0 0 3px 4px">
      <div style="height:27px;line-height:25px;padding:0 13px;border-radius:3px 0 0 3px;border:1px solid rgba(255,255,255,.3);
           background:linear-gradient(rgba(255,255,255,.22),rgba(255,255,255,.10) 48%,rgba(0,0,0,.3) 52%,rgba(64,115,179,.3))">Shut down</div>
      <div style="height:27px;width:27px;line-height:25px;text-align:center;border-radius:0 3px 3px 0;border:1px solid rgba(255,255,255,.3);border-left:none;
           background:linear-gradient(rgba(255,255,255,.22),rgba(255,255,255,.10) 48%,rgba(0,0,0,.3) 52%,rgba(64,115,179,.3))">&#9656;</div>
    </div>
  </div>
</div>"""

    # taskbar
    taskicons = [("web", "focus"), ("fm", "normal"), ("term", "hover"), ("settings", None), ("folder", "normal")]
    tb = ""
    x = 52
    for k, st in taskicons:
        tb += f"JSFRAME('tasks','{st}',{x},1042,58,38)" if st else ""
        tb += f'<img class="abs" src="{I[k]}" style="left:{x+13}px;top:1047px;width:32px;height:32px">'
        x += 60
    tray = ('<svg class="abs" style="left:1700px;top:1050px" width="110" height="20" viewBox="0 0 110 20" fill="#e8eaed">'
            '<path d="M2,7h4l5-4v14l-5-4H2z M14,6q3,4 0,8 M17,4q5,6 0,12" stroke="#e8eaed" stroke-width="1.4" fill-rule="evenodd"/>'
            '<path d="M38,15 a2,2 0 1 0 0.01,0 M31,10 a10,10 0 0 1 14,0 M28,7 a14,14 0 0 1 20,0" stroke="#e8eaed" stroke-width="1.6" fill="none"/>'
            '<rect x="62" y="5" width="20" height="10" rx="2" fill="none" stroke="#e8eaed" stroke-width="1.4"/><rect x="64" y="7" width="13" height="6" fill="#3fcf6e"/><rect x="82" y="8" width="2" height="4"/>'
            '<path d="M95,6 l5,5 l5,-5" stroke="#e8eaed" stroke-width="1.6" fill="none"/></svg>')
    clock = '<div class="abs" style="left:1818px;top:1045px;width:80px;text-align:center;font-size:12.5px;line-height:16px">7:42 PM<br>10/17/2026</div>'
    peek = '<div class="abs" style="left:1906px;top:1041px;width:14px;height:39px;border-left:1px solid rgba(255,255,255,.25);background:linear-gradient(90deg,rgba(255,255,255,.10),rgba(255,255,255,.02))"></div>'
    orb = (f'<div class="abs" style="left:6px;top:1041px;width:38px;height:38px">'
           f'<img class="abs" src="file://{IMG}orb-base.svg" style="width:38px">'
           f'<img class="abs" src="file://{IMG}orb-glow.svg" style="width:38px">'
           f'<img class="abs" src="{I["orb_logo"]}" style="left:7.5px;top:7.5px;width:23px">'
           f'<img class="abs" src="file://{IMG}orb-gloss.svg" style="width:38px"></div>')

    # window: Dolphin-like, positioned right
    wx, wy, ww, wh = 640, 90, 1060, 700
    P, TOP = 10, 38
    win_inner = f"""
<div class="abs" style="left:{wx+P+6}px;top:{wy+TOP}px;width:{ww-2*(P+6)}px;height:{wh-TOP-P-6}px;background:#000;display:flex;flex-direction:column">
  <div style="height:36px;display:flex;align-items:center;gap:10px;padding:0 10px;border-bottom:1px solid rgba(255,255,255,.08);background:#050608">
    <span style="opacity:.8">&#9664;&nbsp; &#9654;</span>
    <div style="flex:1;height:24px;border:1px solid rgba(255,255,255,.18);border-radius:3px;line-height:22px;padding-left:8px;background:#0b0d11">
      <img src="{I['docs']}" style="width:16px;vertical-align:-3px"> &nbsp;gamer &#9656; Documents</div>
    <div style="width:220px;height:24px;border:1px solid rgba(255,255,255,.18);border-radius:3px;line-height:22px;padding-left:8px;background:#0b0d11;color:rgba(255,255,255,.4);font-style:italic">Search Documents</div>
  </div>
  <div style="flex:1;display:flex">
    <div class="fm-side" style="width:190px;padding-top:8px;border-right:1px solid rgba(255,255,255,.08)">{side}</div>
    <div class="grid" style="flex:1">{grid}</div>
  </div>
  <div style="height:24px;line-height:24px;padding-left:10px;font-size:12px;color:#9aa3ae;border-top:1px solid rgba(255,255,255,.08)">9 items &nbsp;·&nbsp; 412 GB free</div>
</div>
<img class="abs" src="{I['fm']}" style="left:{wx+P+8}px;top:{wy+P+3}px;width:18px">
<div class="abs" style="left:{wx+P+32}px;top:{wy+P+4}px;color:#fff;font-size:13px">Documents — Dolphin</div>"""
    bx = wx + ww - P - 6
    btns = f"JSELEM('close','active-center',{bx-43},{wy+P+1},43,19)JSELEM('max','active-center',{bx-43-26},{wy+P+1},26,19)JSELEM('min','active-center',{bx-43-52},{wy+P+1},26,19)"

    # inactive konsole window behind
    kx, ky, kw, kh = 470, 300, 640, 380
    kon = f"""<div class="abs" style="left:{kx+P+6}px;top:{ky+TOP}px;width:{kw-2*(P+6)}px;height:{kh-TOP-P-6}px;background:#000;font:13px 'Liberation Mono',monospace;padding:8px;color:#d0d4da;line-height:19px">
<span style="color:#3fe39f">gamer@ps5</span>:<span style="color:#6fb4ff">~</span>$ fastfetch<br>OS: CachyOS x86_64<br>DE: Plasma 6<br>Theme: Cachy7 OLED<br><span style="color:#3fe39f">gamer@ps5</span>:<span style="color:#6fb4ff">~</span>$ &#9608;</div>
<img class="abs" src="{I['term']}" style="left:{kx+P+8}px;top:{ky+P+3}px;width:18px">
<div class="abs" style="left:{kx+P+32}px;top:{ky+P+4}px;color:#969696;font-size:13px">~ : bash — Konsole</div>"""
    kbx = kx + kw - P - 6
    kbtns = f"JSELEM('close','inactive-center',{kbx-43},{ky+P+1},43,19)JSELEM('max','inactive-center',{kbx-43-26},{ky+P+1},26,19)JSELEM('min','inactive-center',{kbx-43-52},{ky+P+1},26,19)"

    # tooltip over terminal task
    tip = "JSFRAME('tip','',150,996,150,34)" + '<div class="abs" style="left:150px;top:996px;width:150px;height:34px;line-height:34px;text-align:center;font-size:12.5px">Konsole</div>'

    order = [
        ("raw", desktop_icons),
        ("js", f"JSFRAME('deco','decoration-inactive',{kx},{ky},{kw},{kh})" + kbtns), ("raw", kon),
        ("js", f"JSFRAME('deco','decoration',{wx},{wy},{ww},{wh})" + btns), ("raw", win_inner),
        ("js", "JSFRAME('panel','',0,1040,1920,40,{top:true,bottom:false,left:false,right:false})"),
        ("js", tb), ("raw", orb + tray + clock + peek),
        ("js", f"JSFRAME('dialog','',{mx},{my},{MW+16},{MH+16})"), ("raw", menu),
    ]
    parts = []
    for kind, s in order:
        if kind == "raw":
            parts.append("s+=" + json.dumps(s) + ";")
        else:
            import re
            # mix of JS calls and raw html
            tokens = re.split(r"(JSFRAME\([^)]*\)|JSELEM\([^)]*\))", s)
            for t in tokens:
                if not t:
                    continue
                if t.startswith("JSFRAME("):
                    parts.append("s+=frame(" + t[8:] + ";")
                elif t.startswith("JSELEM("):
                    parts.append("s+=elem(" + t[7:] + ";")
                else:
                    parts.append("s+=" + json.dumps(t) + ";")
    script = "\n".join(parts)
    return f"""<html><head><style>{CSS}</style></head><body><div id=root></div>
<script>{js}
{mounts}
let s='';
{script}
document.getElementById('root').innerHTML=s;
</script></body></html>"""


if __name__ == "__main__":
    open("/home/claude/preview/desktop.html", "w").write(html())
    print("ok")
