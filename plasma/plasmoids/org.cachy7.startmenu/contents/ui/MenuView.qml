import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QQC2
import QtCore
import org.kde.plasma.plasmoid
import org.kde.plasma.components as PC3
import org.kde.kirigami as Kirigami
import org.kde.coreaddons as KCoreAddons

// The Windows 7 style two-column start menu.
Item {
    id: menu

    readonly property real gu: Kirigami.Units.gridUnit
    Layout.minimumWidth: gu * 25
    Layout.preferredWidth: gu * 26
    Layout.minimumHeight: gu * 28
    Layout.preferredHeight: gu * 30

    property bool showAll: false
    property var openCats: []

    function toggleCat(name) {
        const list = openCats.slice()
        const i = list.indexOf(name)
        if (i >= 0) {
            list.splice(i, 1)
        } else {
            list.push(name)
        }
        openCats = list
    }
    property string hoverIcon: ""
    readonly property string view: searchField.text.length > 0 ? "search" : (showAll ? "all" : "home")
    readonly property QtObject results: (root.runnerModel && root.runnerModel.count > 0) ? root.runnerModel.modelForRow(0) : null
    readonly property int favCount: root.favoritesModel ? root.favoritesModel.count : 0
    readonly property int freqCount: (root.frequentModel && Plasmoid.configuration.showFrequent)
        ? Math.min(root.frequentModel.count, Plasmoid.configuration.maxFrequent) : 0

    KCoreAddons.KUser {
        id: kuser
    }

    function reset() {
        searchField.text = ""
        showAll = false
        hoverIcon = ""
        openCats = []
        allTree.contentY = 0
        searchField.forceActiveFocus()
    }

    function openLocation(loc) {
        Qt.openUrlExternally(StandardPaths.writableLocation(loc))
        root.expanded = false
    }

    function openUrl(url) {
        Qt.openUrlExternally(url)
        root.expanded = false
    }

    function runCommand(cmd) {
        root.run(cmd)
        root.expanded = false
    }

    function activeList() {
        return view === "search" ? resultsList : null
    }

    function launchCurrent() {
        const list = activeList()
        if (!list) {
            return
        }
        const row = list.currentIndex >= 0 ? list.currentIndex : 0
        root.launch(menu.results, row)
    }

    // Hover enter on the next link can arrive before hover leave on the previous one,
    // so a link only clears the picture if it is still showing its own icon.
    function setHover(icon, on) {
        if (on) {
            hoverClear.stop()
            hoverIcon = icon
        } else if (hoverIcon === icon) {
            hoverClear.restart()
        }
    }

    Timer {
        id: hoverClear
        interval: 160
        onTriggered: menu.hoverIcon = ""
    }

    function openContext(favId) {
        if (!favId) {
            return
        }
        ctxMenu.favId = favId
        ctxMenu.popup()
    }

    Connections {
        target: root
        function onExpandedChanged() {
            if (root.expanded) {
                menu.reset()
            }
        }
    }

    Component.onCompleted: Qt.callLater(reset)

    RowLayout {
        anchors.fill: parent
        spacing: Math.round(menu.gu * 0.4)

        // ================= left column: programs ==================
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: Math.round(menu.width * 0.63)
            color: "#000000"
            radius: 4
            border.width: 1
            border.color: Qt.rgba(1, 1, 1, 0.13)

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Math.round(menu.gu * 0.3)
                spacing: Math.round(menu.gu * 0.25)

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    // --- pinned + frequently used ---
                    Flickable {
                        id: homeView
                        anchors.fill: parent
                        visible: menu.view === "home"
                        clip: true
                        contentHeight: homeCol.implicitHeight
                        boundsBehavior: Flickable.StopAtBounds

                        ColumnLayout {
                            id: homeCol
                            width: homeView.width
                            spacing: 1

                            Repeater {
                                model: root.favoritesModel
                                delegate: AppItem {
                                    Layout.fillWidth: true
                                    text: model.display || ""
                                    iconSource: model.decoration
                                    bold: true
                                    onActivated: root.launch(root.favoritesModel, index)
                                    onMenuRequested: menu.openContext(model.favoriteId)
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                Layout.topMargin: Math.round(menu.gu * 0.25)
                                Layout.bottomMargin: Math.round(menu.gu * 0.25)
                                Layout.leftMargin: menu.gu * 0.5
                                Layout.rightMargin: menu.gu * 0.5
                                implicitHeight: 1
                                color: Qt.rgba(1, 1, 1, 0.14)
                                visible: menu.favCount > 0 && menu.freqCount > 0
                            }

                            Repeater {
                                model: (Plasmoid.configuration.showFrequent && root.frequentModel) ? root.frequentModel : null
                                delegate: AppItem {
                                    Layout.fillWidth: true
                                    visible: index < Plasmoid.configuration.maxFrequent
                                    text: model.display || ""
                                    iconSource: model.decoration
                                    onActivated: root.launch(root.frequentModel, index)
                                    onMenuRequested: menu.openContext(model.favoriteId)
                                }
                            }

                            PC3.Label {
                                Layout.fillWidth: true
                                Layout.margins: menu.gu
                                visible: menu.favCount === 0 && menu.freqCount === 0
                                wrapMode: Text.WordWrap
                                horizontalAlignment: Text.AlignHCenter
                                color: "#9aa3ae"
                                text: i18n("Right-click any program in All Programs to pin it here.")
                            }
                        }
                    }

                    // --- All Programs: Win7-style folders that expand in place ---
                    Flickable {
                        id: allTree
                        anchors.fill: parent
                        visible: menu.view === "all"
                        clip: true
                        contentHeight: treeCol.implicitHeight
                        boundsBehavior: Flickable.StopAtBounds
                        QQC2.ScrollBar.vertical: PC3.ScrollBar {}

                        ColumnLayout {
                            id: treeCol
                            width: allTree.width
                            spacing: 1

                            Repeater {
                                model: root.rootModel
                                delegate: ColumnLayout {
                                    id: cat
                                    Layout.fillWidth: true
                                    spacing: 1

                                    readonly property string catName: model.display || ""
                                    readonly property bool open: menu.openCats.indexOf(catName) >= 0
                                    readonly property QtObject apps: (open && root.rootModel) ? root.rootModel.modelForRow(index) : null
                                    visible: index !== root.allAppsRow && catName.length > 0

                                    AppItem {
                                        Layout.fillWidth: true
                                        text: cat.catName
                                        iconSource: cat.open ? "folder-open" : "folder"
                                        badgeSource: model.decoration
                                        iconSize: Kirigami.Units.iconSizes.smallMedium
                                        bold: cat.open
                                        onActivated: menu.toggleCat(cat.catName)
                                    }

                                    Item {
                                        Layout.fillWidth: true
                                        visible: cat.open
                                        implicitHeight: appsCol.implicitHeight

                                        // tree guide line, like Win7's expanded folders
                                        Rectangle {
                                            x: Math.round(menu.gu * 0.85)
                                            width: 1
                                            height: parent.height - 4
                                            y: 2
                                            color: Qt.rgba(0.56, 0.80, 1.0, 0.30)
                                        }

                                        ColumnLayout {
                                            id: appsCol
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.leftMargin: Math.round(menu.gu * 1.3)
                                            spacing: 1

                                            Repeater {
                                                model: cat.apps
                                                delegate: AppItem {
                                                    Layout.fillWidth: true
                                                    text: model.display || ""
                                                    iconSource: model.decoration
                                                    iconSize: Kirigami.Units.iconSizes.smallMedium
                                                    onActivated: root.launch(cat.apps, index)
                                                    onMenuRequested: menu.openContext(model.favoriteId)
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // --- search results ---
                    ListView {
                        id: resultsList
                        anchors.fill: parent
                        visible: menu.view === "search"
                        model: menu.results
                        clip: true
                        currentIndex: 0
                        boundsBehavior: Flickable.StopAtBounds
                        highlightMoveDuration: 0
                        QQC2.ScrollBar.vertical: PC3.ScrollBar {}
                        delegate: AppItem {
                            width: ListView.view.width
                            text: model.display || ""
                            subText: model.description || ""
                            iconSource: model.decoration
                            highlighted: ListView.isCurrentItem
                            onActivated: root.launch(menu.results, index)
                            onMenuRequested: menu.openContext(model.favoriteId)
                        }

                        PC3.Label {
                            anchors.centerIn: parent
                            visible: resultsList.count === 0
                            color: "#9aa3ae"
                            text: i18n("No items match your search.")
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.leftMargin: menu.gu * 0.5
                    Layout.rightMargin: menu.gu * 0.5
                    implicitHeight: 1
                    color: Qt.rgba(1, 1, 1, 0.14)
                }

                // All Programs / Back
                Item {
                    Layout.fillWidth: true
                    implicitHeight: allLabel.implicitHeight + Kirigami.Units.smallSpacing * 3
                    visible: menu.view !== "search"

                    GlassHighlight {
                        anchors.fill: parent
                        visible: allArea.containsMouse
                    }
                    PC3.Label {
                        id: allLabel
                        anchors.fill: parent
                        anchors.leftMargin: menu.gu * 0.6
                        verticalAlignment: Text.AlignVCenter
                        color: "#ffffff"
                        font.bold: true
                        text: menu.showAll ? "◂  " + i18n("Back") : "▸  " + i18n("All Programs")
                    }
                    MouseArea {
                        id: allArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            menu.showAll = !menu.showAll
                            menu.openCats = []
                            allTree.contentY = 0
                            searchField.forceActiveFocus()
                        }
                    }
                }

                PC3.TextField {
                    id: searchField
                    Layout.fillWidth: true
                    placeholderText: i18n("Search programs and files")
                    color: "#f2f4f7"
                    placeholderTextColor: Qt.rgba(1, 1, 1, 0.42)
                    rightPadding: menu.gu * 1.6
                    background: Rectangle {
                        radius: 3
                        color: "#0b0d11"
                        border.width: 1
                        border.color: searchField.activeFocus ? Qt.rgba(0.43, 0.70, 1, 0.85) : Qt.rgba(1, 1, 1, 0.22)
                    }

                    Kirigami.Icon {
                        source: "search"
                        anchors.right: parent.right
                        anchors.rightMargin: Kirigami.Units.smallSpacing * 1.5
                        anchors.verticalCenter: parent.verticalCenter
                        width: Kirigami.Units.iconSizes.small
                        height: width
                        opacity: 0.75
                    }

                    onTextChanged: {
                        if (root.runnerModel) {
                            root.runnerModel.query = text
                        }
                        resultsList.currentIndex = 0
                    }

                    Keys.onPressed: event => {
                        const list = menu.activeList()
                        if (event.key === Qt.Key_Down) {
                            if (list) {
                                list.currentIndex = Math.min(list.currentIndex + 1, list.count - 1)
                                list.positionViewAtIndex(list.currentIndex, ListView.Contain)
                            }
                            event.accepted = true
                        } else if (event.key === Qt.Key_Up) {
                            if (list) {
                                list.currentIndex = Math.max(list.currentIndex - 1, 0)
                                list.positionViewAtIndex(list.currentIndex, ListView.Contain)
                            }
                            event.accepted = true
                        } else if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter) {
                            menu.launchCurrent()
                            event.accepted = true
                        } else if (event.key === Qt.Key_Escape) {
                            if (text.length > 0) {
                                text = ""
                            } else if (menu.showAll) {
                                menu.showAll = false
                            } else {
                                root.expanded = false
                            }
                            event.accepted = true
                        }
                    }
                }
            }
        }

        // ================= right column: places & power ==================
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 4
            border.width: 1
            border.color: Qt.rgba(1, 1, 1, 0.07)
            gradient: Gradient {
                GradientStop { position: 0.0; color: Qt.rgba(0.13, 0.20, 0.30, 0.60) }
                GradientStop { position: 0.55; color: Qt.rgba(0.05, 0.08, 0.12, 0.50) }
                GradientStop { position: 1.0; color: Qt.rgba(0.02, 0.03, 0.05, 0.50) }
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Math.round(menu.gu * 0.35)
                spacing: 0

                // user picture frame; shows the hovered link's icon like Win7
                Rectangle {
                    id: avatarFrame
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: Math.round(menu.gu * 0.2)
                    Layout.bottomMargin: Math.round(menu.gu * 0.5)
                    implicitWidth: Math.round(menu.gu * 3.6)
                    implicitHeight: implicitWidth
                    radius: 6
                    border.width: 1
                    border.color: Qt.rgba(1, 1, 1, 0.45)
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: Qt.rgba(1, 1, 1, 0.35) }
                        GradientStop { position: 0.5; color: Qt.rgba(0.5, 0.65, 0.8, 0.25) }
                        GradientStop { position: 1.0; color: Qt.rgba(0.2, 0.3, 0.45, 0.45) }
                    }

                    Image {
                        id: face
                        anchors.fill: parent
                        anchors.margins: 4
                        source: kuser.faceIconUrl
                        visible: menu.hoverIcon === "" && status === Image.Ready
                        fillMode: Image.PreserveAspectCrop
                        sourceSize.width: width * 2
                        sourceSize.height: height * 2
                        smooth: true
                    }
                    Kirigami.Icon {
                        id: frameIcon
                        anchors.fill: parent
                        anchors.margins: 4
                        visible: !face.visible
                        source: menu.hoverIcon !== "" ? menu.hoverIcon : "user-identity"
                        onSourceChanged: iconFade.restart()

                        NumberAnimation {
                            id: iconFade
                            target: frameIcon
                            property: "opacity"
                            from: 0.25
                            to: 1
                            duration: 140
                            easing.type: Easing.OutQuad
                        }
                    }
                }

                PlaceItem {
                    text: kuser.fullName || kuser.loginName
                    iconName: "user-home"
                    bold: true
                    onActivated: menu.openLocation(StandardPaths.HomeLocation)
                    onHovered: on => menu.setHover(iconName, on)
                }
                PlaceItem {
                    text: i18n("Documents")
                    iconName: "folder-documents"
                    onActivated: menu.openLocation(StandardPaths.DocumentsLocation)
                    onHovered: on => menu.setHover(iconName, on)
                }
                PlaceItem {
                    text: i18n("Pictures")
                    iconName: "folder-pictures"
                    onActivated: menu.openLocation(StandardPaths.PicturesLocation)
                    onHovered: on => menu.setHover(iconName, on)
                }
                PlaceItem {
                    text: i18n("Music")
                    iconName: "folder-music"
                    onActivated: menu.openLocation(StandardPaths.MusicLocation)
                    onHovered: on => menu.setHover(iconName, on)
                }
                PlaceItem {
                    text: i18n("Videos")
                    iconName: "folder-videos"
                    onActivated: menu.openLocation(StandardPaths.MoviesLocation)
                    onHovered: on => menu.setHover(iconName, on)
                }
                PlaceItem {
                    text: i18n("Downloads")
                    iconName: "folder-download"
                    onActivated: menu.openLocation(StandardPaths.DownloadLocation)
                    onHovered: on => menu.setHover(iconName, on)
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.topMargin: Math.round(menu.gu * 0.3)
                    Layout.bottomMargin: Math.round(menu.gu * 0.3)
                    Layout.leftMargin: menu.gu * 0.3
                    Layout.rightMargin: menu.gu * 0.3
                    implicitHeight: 1
                    color: Qt.rgba(1, 1, 1, 0.16)
                }

                PlaceItem {
                    text: i18n("Computer")
                    iconName: "computer"
                    onActivated: menu.openUrl("file:///")
                    onHovered: on => menu.setHover(iconName, on)
                }
                PlaceItem {
                    text: i18n("System Settings")
                    iconName: "preferences-system"
                    onActivated: menu.runCommand("systemsettings")
                    onHovered: on => menu.setHover(iconName, on)
                }
                PlaceItem {
                    text: i18n("Terminal")
                    iconName: "utilities-terminal"
                    onActivated: menu.runCommand("konsole")
                    onHovered: on => menu.setHover(iconName, on)
                }
                PlaceItem {
                    text: i18n("Run…")
                    iconName: "system-run"
                    onActivated: menu.runCommand("krunner")
                    onHovered: on => menu.setHover(iconName, on)
                }

                Item {
                    Layout.fillHeight: true
                }

                RowLayout {
                    Layout.alignment: Qt.AlignLeft
                    Layout.leftMargin: Math.round(menu.gu * 0.2)
                    Layout.bottomMargin: Math.round(menu.gu * 0.15)
                    spacing: 0

                    GlassButton {
                        id: shutdownButton
                        text: i18n("Shut down")
                        onClicked: root.power("shutdown")
                    }
                    GlassButton {
                        id: powerArrow
                        text: "▸"
                        implicitWidth: implicitHeight
                        onClicked: powerMenu.popup(powerArrow, 0, powerArrow.height)
                    }
                }
            }
        }
    }

    PC3.Menu {
        id: powerMenu
        PC3.MenuItem { text: i18n("Switch user"); icon.name: "system-switch-user"; onTriggered: root.power("switchuser") }
        PC3.MenuItem { text: i18n("Log off"); icon.name: "system-log-out"; onTriggered: root.power("logout") }
        PC3.MenuItem { text: i18n("Lock"); icon.name: "system-lock-screen"; onTriggered: root.power("lock") }
        PC3.MenuSeparator {}
        PC3.MenuItem { text: i18n("Restart"); icon.name: "system-reboot"; onTriggered: root.power("reboot") }
        PC3.MenuItem { text: i18n("Sleep"); icon.name: "system-suspend"; onTriggered: root.power("suspend") }
    }

    PC3.Menu {
        id: ctxMenu
        property string favId: ""
        PC3.MenuItem {
            text: root.isFavorite(ctxMenu.favId) ? i18n("Unpin from Start Menu") : i18n("Pin to Start Menu")
            icon.name: root.isFavorite(ctxMenu.favId) ? "window-unpin" : "window-pin"
            onTriggered: root.toggleFavorite(ctxMenu.favId)
        }
    }
}
