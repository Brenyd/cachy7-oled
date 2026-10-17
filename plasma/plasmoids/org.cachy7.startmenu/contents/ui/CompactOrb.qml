import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore

// The glass start orb. Layers: base sphere, hover glow, distro logo, gloss.
MouseArea {
    id: orb

    readonly property bool vertical: Plasmoid.formFactor === PlasmaCore.Types.Vertical
    readonly property bool lit: containsMouse || root.expanded
    property bool wasExpanded: false

    Layout.minimumWidth: vertical ? -1 : height
    Layout.maximumWidth: vertical ? -1 : height
    Layout.minimumHeight: vertical ? width : -1
    Layout.maximumHeight: vertical ? width : -1

    hoverEnabled: true
    acceptedButtons: Qt.LeftButton
    onPressed: wasExpanded = root.expanded
    onClicked: root.expanded = !wasExpanded

    Item {
        id: sphere
        anchors.centerIn: parent
        width: Math.max(8, Math.min(orb.width, orb.height) - 2)
        height: width
        scale: orb.pressed ? 0.94 : 1.0
        Behavior on scale { NumberAnimation { duration: 90 } }

        Image {
            anchors.fill: parent
            source: Qt.resolvedUrl("../images/orb-base.svg")
            sourceSize.width: width * 2
            sourceSize.height: height * 2
            smooth: true
        }
        Image {
            anchors.fill: parent
            source: Qt.resolvedUrl("../images/orb-glow.svg")
            sourceSize.width: width * 2
            sourceSize.height: height * 2
            opacity: orb.lit ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: 220; easing.type: Easing.OutQuad } }
        }
        LogoItem {
            anchors.centerIn: parent
            width: parent.width * 0.6
            height: width
        }
        Image {
            anchors.fill: parent
            source: Qt.resolvedUrl("../images/orb-gloss.svg")
            sourceSize.width: width * 2
            sourceSize.height: height * 2
            smooth: true
        }
    }
}
