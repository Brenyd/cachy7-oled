/*
 * Cachy7 Start Menu - a Windows 7 style launcher for Plasma 6.
 * The kicker models are created at runtime so that small changes in
 * Plasma's private launcher API degrade gracefully instead of breaking
 * the whole widget.
 */
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.plasma5support as P5Support
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: root

    property QtObject rootModel: null
    property QtObject allAppsModel: null
    property int allAppsRow: -1
    property QtObject frequentModel: null
    property QtObject runnerModel: null
    readonly property QtObject favoritesModel: rootModel ? rootModel.favoritesModel : null

    preferredRepresentation: compactRepresentation
    compactRepresentation: CompactOrb {}
    fullRepresentation: MenuView {}

    toolTipMainText: i18n("Start")
    toolTipSubText: ""

    // ---- process runner -------------------------------------------------
    P5Support.DataSource {
        id: executable
        engine: "executable"
        connectedSources: []
        onNewData: (sourceName, data) => disconnectSource(sourceName)
    }

    function run(cmd) {
        executable.connectSource(cmd)
    }

    readonly property var powerCommands: ({
        "shutdown": "dbus-send --session --type=method_call --dest=org.kde.Shutdown /Shutdown org.kde.Shutdown.logoutAndShutdown",
        "reboot": "dbus-send --session --type=method_call --dest=org.kde.Shutdown /Shutdown org.kde.Shutdown.logoutAndReboot",
        "logout": "dbus-send --session --type=method_call --dest=org.kde.Shutdown /Shutdown org.kde.Shutdown.logout",
        "lock": "dbus-send --session --type=method_call --dest=org.freedesktop.ScreenSaver /ScreenSaver org.freedesktop.ScreenSaver.Lock",
        "suspend": "systemctl suspend",
        "switchuser": "dbus-send --session --type=method_call --dest=org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.openSwitchUserDialog"
    })

    function power(kind) {
        root.expanded = false
        if (powerCommands[kind]) {
            run(powerCommands[kind])
        }
    }

    // ---- launching ------------------------------------------------------
    function launch(model, row) {
        if (!model || row < 0) {
            return
        }
        try {
            model.trigger(row, "", null)
        } catch (e) {
            console.warn("Cachy7 start menu: launch failed:", e)
        }
        root.expanded = false
    }

    function isFavorite(id) {
        if (!favoritesModel || !id) {
            return false
        }
        try {
            return favoritesModel.isFavorite(id)
        } catch (e) {
            return false
        }
    }

    function toggleFavorite(id) {
        if (!favoritesModel || !id) {
            return
        }
        try {
            if (favoritesModel.isFavorite(id)) {
                favoritesModel.removeFavorite(id)
            } else {
                favoritesModel.addFavorite(id, -1)
            }
        } catch (e) {
            console.warn("Cachy7 start menu: favorite change failed:", e)
        }
    }

    // ---- model setup ----------------------------------------------------
    function tryCreate(qml, name) {
        try {
            return Qt.createQmlObject(qml, root, name)
        } catch (e) {
            console.warn("Cachy7 start menu: could not create " + name + ":", e)
            return null
        }
    }

    function setIfExists(obj, props) {
        for (const key in props) {
            try {
                if (obj[key] !== undefined) {
                    obj[key] = props[key]
                }
            } catch (e) {
                console.warn("Cachy7 start menu: property " + key + " not set:", e)
            }
        }
    }

    function pickAllApps() {
        if (!rootModel) {
            return
        }
        // "All Applications" is the biggest group, whatever its row is.
        let best = null
        let bestRow = -1
        let bestCount = -1
        for (let i = 0; i < rootModel.count; ++i) {
            const m = rootModel.modelForRow(i)
            if (m && m.count !== undefined && m.count > bestCount) {
                best = m
                bestRow = i
                bestCount = m.count
            }
        }
        allAppsModel = best
        allAppsRow = bestRow
    }

    function refreshModels() {
        if (!rootModel) {
            return
        }
        try {
            rootModel.refresh()
        } catch (e) {
            console.warn("Cachy7 start menu: refresh failed:", e)
        }
        pickAllApps()
    }

    function initFavorites() {
        const fm = favoritesModel
        if (!fm) {
            return
        }
        try {
            fm.initForClient("org.cachy7.startmenu.favorites.instance-" + Plasmoid.id)
            if (!Plasmoid.configuration.favoritesPortedToKAstats) {
                if (fm.count < 1) {
                    fm.portOldFavorites(Plasmoid.configuration.favorites)
                }
                Plasmoid.configuration.favoritesPortedToKAstats = true
            }
        } catch (e) {
            console.warn("Cachy7 start menu: favorites init failed:", e)
        }
    }

    Connections {
        target: root.rootModel
        ignoreUnknownSignals: true
        function onRefreshed() { root.pickAllApps() }
        function onCountChanged() { root.pickAllApps() }
    }

    onExpandedChanged: {
        if (expanded && !allAppsModel) {
            refreshModels()
        }
    }

    Component.onCompleted: {
        try {
            root.hideOnWindowDeactivate = true
        } catch (e) {
        }

        rootModel = tryCreate("import org.kde.plasma.private.kicker as Kicker\nKicker.RootModel { autoPopulate: false }", "cachy7RootModel")
        if (rootModel) {
            setIfExists(rootModel, {
                "appletInterface": root,
                "flat": true,
                "sorted": true,
                "showSeparators": false,
                "showAllApps": true,
                "showAllAppsCategorized": false,
                "showRecentApps": false,
                "showRecentDocs": false,
                "showPowerSession": false,
                "showFavoritesPlaceholder": false
            })
            initFavorites()
            refreshModels()
        }

        frequentModel = tryCreate("import org.kde.plasma.private.kicker as Kicker\nKicker.RecentUsageModel { shownItems: Kicker.RecentUsageModel.OnlyApps; ordering: Kicker.RecentUsageModel.Popular }", "cachy7FrequentModel")

        runnerModel = tryCreate("import org.kde.plasma.private.kicker as Kicker\nKicker.RunnerModel { mergeResults: true }", "cachy7RunnerModel")
        if (runnerModel) {
            setIfExists(runnerModel, {
                "appletInterface": root,
                "favoritesModel": favoritesModel
            })
        }
    }
}
