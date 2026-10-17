import QtQuick

// Aero-style selection: blue glass with a bright edge.
Rectangle {
    radius: 3
    border.width: 1
    border.color: Qt.rgba(0.56, 0.80, 1.0, 0.60)
    gradient: Gradient {
        GradientStop { position: 0.0; color: Qt.rgba(0.50, 0.76, 1.0, 0.34) }
        GradientStop { position: 0.48; color: Qt.rgba(0.28, 0.56, 0.95, 0.22) }
        GradientStop { position: 0.52; color: Qt.rgba(0.14, 0.40, 0.85, 0.22) }
        GradientStop { position: 1.0; color: Qt.rgba(0.20, 0.52, 1.0, 0.40) }
    }
}
