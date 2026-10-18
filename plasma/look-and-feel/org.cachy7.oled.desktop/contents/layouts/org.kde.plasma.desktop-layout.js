// Cachy7 OLED: a Windows 7 style taskbar.
// [orb] [pinned/running icons ..........] [tray] [clock] [show desktop]

var panel = new Panel
panel.location = "bottom"
panel.height = 34
panel.hiding = "none"
try { panel.floating = false } catch (e) {}

var menu = panel.addWidget("org.cachy7.startmenu")
menu.currentConfigGroup = ["Shortcuts"]
menu.writeConfig("global", "Alt+F1")

var tasks = panel.addWidget("org.kde.plasma.icontasks")
tasks.currentConfigGroup = ["General"]
tasks.writeConfig("launchers", [
    "preferred://filemanager",
    "preferred://browser",
    "applications:org.kde.konsole.desktop"
])
tasks.writeConfig("showOnlyCurrentDesktop", false)

panel.addWidget("org.kde.plasma.marginsseparator")

panel.addWidget("org.kde.plasma.systemtray")

var clock = panel.addWidget("org.kde.plasma.digitalclock")
clock.currentConfigGroup = ["Appearance"]
clock.writeConfig("showDate", true)
clock.writeConfig("dateDisplayFormat", "BelowTime")
clock.writeConfig("dateFormat", "shortDate")

// Win7's "peek at desktop" strip in the far corner
panel.addWidget("org.kde.plasma.showdesktop")

// The wallpaper is set by 'cachy7-oled apply' so it works for user and system installs.
