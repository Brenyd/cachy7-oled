import QtQuick
import org.kde.plasma.components as PC3
import org.kde.kirigami as Kirigami

// Win7 "Shut down" style glass button.
Rectangle {
    id: btn

    property string text: ""
    signal clicked()

    implicitWidth: label.implicitWidth + Kirigami.Units.gridUnit * 1.4
    implicitHeight: label.implicitHeight + Kirigami.Units.smallSpacing * 2.5
    radius: 3
    border.width: 1
    border.color: area.containsMouse ? Qt.rgba(0.6, 0.83, 1, 0.85) : Qt.rgba(1, 1, 1, 0.30)

    gradient: Gradient {
        GradientStop { position: 0.0; color: area.containsMouse ? Qt.rgba(0.62, 0.83, 1, 0.75) : Qt.rgba(1, 1, 1, 0.22) }
        GradientStop { position: 0.48; color: area.containsMouse ? Qt.rgba(0.27, 0.56, 0.88, 0.75) : Qt.rgba(1, 1, 1, 0.10) }
        GradientStop { position: 0.52; color: area.containsMouse ? Qt.rgba(0.10, 0.35, 0.70, 0.80) : Qt.rgba(0, 0, 0, 0.30) }
        GradientStop { position: 1.0; color: area.containsMouse ? Qt.rgba(0.25, 0.60, 1, 0.85) : Qt.rgba(0.25, 0.45, 0.70, 0.30) }
    }

    PC3.Label {
        id: label
        anchors.centerIn: parent
        text: btn.text
        color: "#ffffff"
        textFormat: Text.PlainText
    }

    MouseArea {
        id: area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: btn.clicked()
    }
}
