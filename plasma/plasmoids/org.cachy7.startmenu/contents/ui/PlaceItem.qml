import QtQuick
import QtQuick.Layouts
import org.kde.plasma.components as PC3
import org.kde.kirigami as Kirigami

// Right-column link (Documents, Pictures, Computer, ...), text only like Win7.
Item {
    id: place

    property string text: ""
    property string iconName: ""
    property bool bold: false

    signal activated()
    signal hovered(bool on)

    Layout.fillWidth: true
    implicitHeight: label.implicitHeight + Kirigami.Units.smallSpacing * 3

    GlassHighlight {
        anchors.fill: parent
        visible: area.containsMouse
    }

    PC3.Label {
        id: label
        anchors.fill: parent
        anchors.leftMargin: Kirigami.Units.smallSpacing * 2
        anchors.rightMargin: Kirigami.Units.smallSpacing
        verticalAlignment: Text.AlignVCenter
        text: place.text
        elide: Text.ElideRight
        textFormat: Text.PlainText
        color: "#ffffff"
        font.bold: place.bold
    }

    MouseArea {
        id: area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: place.activated()
        onContainsMouseChanged: place.hovered(containsMouse)
    }
}
