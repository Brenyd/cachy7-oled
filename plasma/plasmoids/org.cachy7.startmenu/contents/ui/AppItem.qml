import QtQuick
import QtQuick.Layouts
import org.kde.plasma.components as PC3
import org.kde.kirigami as Kirigami

Item {
    id: item

    property string text: ""
    property var iconSource
    property string subText: ""
    property int iconSize: Kirigami.Units.iconSizes.medium
    property bool highlighted: false
    property bool bold: false

    signal activated()
    signal menuRequested()

    implicitWidth: Kirigami.Units.gridUnit * 10
    implicitHeight: Math.max(iconSize, textCol.implicitHeight) + Kirigami.Units.smallSpacing * 2

    GlassHighlight {
        anchors.fill: parent
        visible: area.containsMouse || item.highlighted
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Kirigami.Units.smallSpacing * 1.5
        anchors.rightMargin: Kirigami.Units.smallSpacing
        spacing: Kirigami.Units.smallSpacing * 2

        Kirigami.Icon {
            source: item.iconSource
            Layout.preferredWidth: item.iconSize
            Layout.preferredHeight: item.iconSize
            Layout.alignment: Qt.AlignVCenter
        }

        ColumnLayout {
            id: textCol
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter
            spacing: 0

            PC3.Label {
                text: item.text
                Layout.fillWidth: true
                elide: Text.ElideRight
                textFormat: Text.PlainText
                color: "#f2f4f7"
                font.bold: item.bold
            }
            PC3.Label {
                visible: item.subText.length > 0
                text: item.subText
                Layout.fillWidth: true
                elide: Text.ElideRight
                textFormat: Text.PlainText
                color: "#9aa3ae"
                font: Kirigami.Theme.smallFont
            }
        }
    }

    MouseArea {
        id: area
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onClicked: ev => {
            if (ev.button === Qt.RightButton) {
                item.menuRequested()
            } else {
                item.activated()
            }
        }
    }
}
