import QtQuick

// "Starting CachyOS" - a nod to the Windows 7 boot screen, on pure black.
Rectangle {
    id: root
    color: "#000000"

    property int stage

    onStageChanged: {
        if (stage >= 1 && content.opacity === 0 && !intro.running) {
            intro.start()
        }
    }

    Item {
        id: content
        anchors.centerIn: parent
        anchors.verticalCenterOffset: -height * 0.15
        width: 420
        height: 300
        opacity: 0

        Image {
            id: glow
            anchors.centerIn: logoBox
            width: logoBox.width * 2.2
            height: width
            source: "images/glow.svg"
            sourceSize.width: width
            sourceSize.height: height
            opacity: 0.35

            SequentialAnimation on opacity {
                running: true
                loops: Animation.Infinite
                NumberAnimation { to: 0.9; duration: 1400; easing.type: Easing.InOutSine }
                NumberAnimation { to: 0.35; duration: 1400; easing.type: Easing.InOutSine }
            }
        }

        Item {
            id: logoBox
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 40
            width: 128
            height: 128

            property int attempt: 0
            readonly property var candidates: ["images/logo.svg", "images/logo.png", "images/orb.svg"]

            Image {
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                smooth: true
                sourceSize.width: 256
                sourceSize.height: 256
                source: logoBox.candidates[Math.min(logoBox.attempt, 2)]
                onStatusChanged: {
                    if (status === Image.Error && logoBox.attempt < 2) {
                        logoBox.attempt += 1
                    }
                }
            }
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: logoBox.bottom
            anchors.topMargin: 56
            text: "Starting CachyOS"
            color: "#e8eaed"
            font.pixelSize: 24
            font.weight: Font.Light
        }
    }

    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 36
        text: "Cachy7 OLED"
        color: "#3a3f46"
        font.pixelSize: 13
        opacity: content.opacity
    }

    OpacityAnimator {
        id: intro
        target: content
        from: 0
        to: 1
        duration: 900
        easing.type: Easing.OutCubic
    }
}
