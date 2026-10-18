#!/usr/bin/env python3
"""Render the start menu's states (mirrors MenuView.qml) to PNGs for review."""
import json
import os
import sys

R = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".") + "/"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/preview"
IC = R + "icons/Cachy7/scalable/"
TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
from shot import shot  # noqa: E402


def ic(cat, name):
    return f"file://{IC}{cat}/{name}.svg"


I = {
    "web": ic("apps", "internet-web-browser"), "fm": ic("apps", "system-file-manager"), "term": ic("apps", "utilities-terminal"),
    "settings": ic("apps", "preferences-system"), "folder": ic("places", "folder"), "pics": ic("places", "folder-pictures"),
    "music": ic("places", "folder-music"), "videos": ic("places", "folder-videos"), "txt": ic("mimetypes", "text-x-generic"),
    "disc": ic("devices", "media-optical"), "pc": ic("devices", "computer"), "hdd": ic("devices", "drive-harddisk"),
    "net": ic("places", "network-workgroup"), "user": ic("apps", "user-identity"), "docs": ic("places", "folder-documents"),
    "dl": ic("places", "folder-download"), "usb": ic("devices", "drive-removable-media"),
}

CATS = [  # name, badge stand-in, apps
    ("Development", "term", [("Kate", "txt"), ("Konsole", "term")]),
    ("Games", "disc", [("Heroic Games Launcher", "disc"), ("Lutris", "disc"), ("ProtonUp-Qt", "settings"), ("RetroArch", "disc"), ("Steam", "disc")]),
    ("Graphics", "pics", [("Gwenview", "pics"), ("Krita", "pics"), ("Spectacle", "pics")]),
    ("Internet", "web", [("Discord", "net"), ("Firefox", "web"), ("KDE Connect", "net")]),
    ("Multimedia", "music", [("Elisa", "music"), ("Haruna Media Player", "videos"), ("OBS Studio", "videos")]),
    ("Office", "docs", [("LibreOffice Writer", "txt"), ("Okular", "txt")]),
    ("Settings", "settings", [("System Settings", "settings")]),
    ("System", "pc", [("Dolphin", "fm"), ("KSysGuard", "pc"), ("Octopi", "hdd"), ("Partition Manager", "hdd")]),
    ("Utilities", "usb", [("Ark", "folder"), ("KCalc", "txt"), ("Kate", "txt"), ("Spectacle", "pics")]),
]

CSS = """
*{box-sizing:border-box} body{margin:0;background:#000;font-family:'Noto Sans','Inter',sans-serif;font-size:13px;color:#f2f4f7}
.abs{position:absolute}
.hl{border-radius:3px;border:1px solid rgba(143,204,255,.6);
 background:linear-gradient(rgba(128,194,255,.34),rgba(71,143,242,.22) 48%,rgba(36,102,217,.22) 52%,rgba(51,133,255,.40))}
.row{display:flex;align-items:center;gap:10px;padding:0 7px;border:1px solid transparent;border-radius:3px}
.big{height:40px}.big img.i{width:32px;height:32px}
.sm{height:30px}.sm img.i{width:22px;height:22px}
.ico{position:relative;display:inline-block;line-height:0}
.badge{position:absolute;width:13px;height:13px;right:-3px;bottom:-2px}
.sub{font-size:11px;color:#9aa3ae}
.place{height:29px;line-height:27px;padding-left:9px;color:#fff;border:1px solid transparent;border-radius:3px}
.sep{height:1px;background:rgba(255,255,255,.14);margin:6px 9px}
.tree{position:relative;padding-left:23px}
.tree:before{content:'';position:absolute;left:15px;top:2px;bottom:2px;width:1px;background:rgba(143,204,255,.30)}
.glass-btn{height:27px;line-height:25px;border:1px solid rgba(255,255,255,.3);
 background:linear-gradient(rgba(255,255,255,.22),rgba(255,255,255,.10) 48%,rgba(0,0,0,.3) 52%,rgba(64,115,179,.3))}
"""


def app_row(name, icon, big=False, hl=False, bold=False, sub=""):
    cls = "row big" if big else "row sm"
    if hl:
        cls += " hl"
    label = f'<div style="font-weight:{700 if bold else 400}">{name}' + (f'<div class="sub">{sub}</div>' if sub else "") + "</div>"
    return f'<div class="{cls}"><img class="i" src="{I[icon]}">{label}</div>'


def cat_row(name, badge, open_, hl=False):
    cls = "row sm" + (" hl" if hl else "")
    return (f'<div class="{cls}"><span class="ico"><img class="i" src="{I["folder"]}" style="width:22px;height:22px">'
            f'<img class="badge" src="{I[badge]}"></span><span style="font-weight:{700 if open_ else 400}">{name}</span></div>')


def left_column(state):
    if state == "home":
        pinned = [("Web Browser", "web"), ("Dolphin", "fm"), ("Konsole", "term"), ("System Settings", "settings")]
        freq = [("Steam", "disc"), ("Gwenview", "pics"), ("Elisa", "music"), ("Kate", "txt"), ("Haruna Media Player", "videos")]
        body = "".join(app_row(n, i, big=True, bold=True, hl=(n == "Konsole")) for n, i in pinned)
        body += '<div class="sep"></div>' + "".join(app_row(n, i, big=True) for n, i in freq)
        bottom = "&#9656;&nbsp; All Programs"
        search = '<span style="color:rgba(255,255,255,.42)">Search programs and files</span>'
    elif state in ("all", "open"):
        openset = {"Games", "Internet"} if state == "open" else set()
        body = ""
        for name, badge, apps in CATS:
            body += cat_row(name, badge, name in openset, hl=(state == "all" and name == "Games"))
            if name in openset:
                body += '<div class="tree">' + "".join(
                    app_row(n, i, hl=(n == "Steam")) for n, i in apps) + "</div>"
        bottom = "&#9666;&nbsp; Back"
        search = '<span style="color:rgba(255,255,255,.42)">Search programs and files</span>'
    else:  # search
        res = [("Firefox", "web", "Web Browser"), ("Filelight", "hdd", "Disk Usage Analyzer"),
               ("Find Files/Folders", "fm", "KFind"), ("Fish shell", "term", "Command line")]
        body = "".join(app_row(n, i, big=True, sub=s, hl=(k == 0)) for k, (n, i, s) in enumerate(res))
        bottom = None
        search = '<span>fi<span style="border-left:1px solid #fff;margin-left:1px"></span></span>'
    allrow = f'<div style="height:30px;line-height:30px;padding-left:11px;font-weight:700">{bottom}</div>' if bottom else ""
    return f"""
  <div style="width:295px;background:#000;border:1px solid rgba(255,255,255,.13);border-radius:4px;padding:5px;display:flex;flex-direction:column;gap:4px">
    <div style="flex:1;overflow:hidden;display:flex;flex-direction:column;gap:1px">{body}</div>
    <div class="sep" style="margin:0 9px"></div>
    {allrow}
    <div style="height:30px;border-radius:3px;background:#0b0d11;border:1px solid rgba(110,178,255,.85);padding:0 10px;line-height:28px;display:flex;justify-content:space-between">{search}<span style="opacity:.75">&#9906;</span></div>
  </div>"""


def right_column(hover):
    places = ["<b>gamer</b>", "Documents", "Pictures", "Music", "Videos", "Downloads", "SEP", "Computer", "System Settings", "Terminal", "Run…"]
    icons = {"Documents": "docs", "Pictures": "pics", "Music": "music", "Videos": "videos", "Downloads": "dl",
             "Computer": "pc", "System Settings": "settings", "Terminal": "term"}
    pic = I[icons[hover]] if hover else I["user"]
    rows = "".join('<div class="sep" style="margin:7px 6px;background:rgba(255,255,255,.16)"></div>' if p == "SEP"
                   else f'<div class="place {"hl" if p == hover else ""}">{p}</div>' for p in places)
    return f"""
  <div style="flex:1;border-radius:4px;border:1px solid rgba(255,255,255,.07);padding:6px;display:flex;flex-direction:column;
       background:linear-gradient(rgba(33,51,77,.6),rgba(13,20,31,.5) 55%,rgba(5,8,13,.5))">
    <div style="width:65px;height:65px;margin:4px auto 9px;border-radius:6px;border:1px solid rgba(255,255,255,.45);padding:4px;
         background:linear-gradient(rgba(255,255,255,.35),rgba(128,166,204,.25),rgba(51,77,115,.45))"><img src="{pic}" style="width:100%;height:100%"></div>
    {rows}
    <div style="flex:1"></div>
    <div style="display:flex;margin:0 0 3px 4px">
      <div class="glass-btn" style="padding:0 13px;border-radius:3px 0 0 3px">Shut down</div>
      <div class="glass-btn" style="width:27px;text-align:center;border-radius:0 3px 3px 0;border-left:none">&#9656;</div>
    </div>
  </div>"""


def page(state, hover):
    js = open(os.path.join(TOOLS, "framesvg.js")).read()
    dlg = open(R + "plasma/desktoptheme/cachy7-oled/dialogs/background.svg").read()
    wp = R + "wallpapers/Cachy7OLED/contents/images/1920x1080.png"
    menu = f'<div class="abs" style="left:28px;top:28px;width:468px;height:540px;display:flex;gap:7px">{left_column(state)}{right_column(hover)}</div>'
    return f"""<html><head><style>{CSS}</style></head>
<body style="width:524px;height:596px;position:relative;overflow:hidden;background:#000 url(file://{wp}) 0 -420px/1920px 1080px">
<div id=f></div>{menu}
<script>{js}
mountSvg('dlg', {json.dumps(dlg)});
document.getElementById('f').innerHTML = frame('dlg','',20,20,484,556);
</script></body></html>"""


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    states = [("1-home", "home", "Documents"), ("2-all-programs", "all", None),
              ("3-categories-open", "open", None), ("4-search", "search", "Terminal")]
    for fname, st, hov in states:
        html = os.path.join(OUT, f"menu-{fname}.html")
        open(html, "w").write(page(st, hov))
        shot(html, os.path.join(OUT, f"menu-{fname}.png"), 524, 596, 1.5, full_page=False)
    print("rendered", len(states), "states to", OUT)
