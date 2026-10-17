import QtQuick
import org.kde.plasma.plasmoid
import org.kde.kirigami as Kirigami

// Shows the CachyOS logo: user setting > logo copied in by the installer
// (logo.svg / logo.png) > icon theme "cachyos" > start-here-kde.
Item {
    id: logo

    readonly property string setting: Plasmoid.configuration.logo || ""
    readonly property bool settingIsPath: setting.indexOf("/") >= 0
    property int attempt: 0   // 0 = svg, 1 = png, 2 = give up on files

    readonly property bool useIcon: (setting.length > 0 && !settingIsPath) || attempt >= 2

    onSettingChanged: attempt = 0

    Image {
        id: img
        anchors.fill: parent
        visible: !logo.useIcon && status === Image.Ready
        fillMode: Image.PreserveAspectFit
        smooth: true
        mipmap: true
        sourceSize.width: width * 2
        sourceSize.height: height * 2
        source: {
            if (logo.useIcon) {
                return ""
            }
            if (logo.settingIsPath) {
                return logo.setting.indexOf("file:") === 0 ? logo.setting : "file://" + logo.setting
            }
            return Qt.resolvedUrl(logo.attempt === 0 ? "../images/logo.svg" : "../images/logo.png")
        }
        onStatusChanged: {
            if (status === Image.Error) {
                logo.attempt = logo.settingIsPath ? 2 : logo.attempt + 1
            }
        }
    }

    Kirigami.Icon {
        anchors.fill: parent
        visible: logo.useIcon
        source: (logo.setting.length > 0 && !logo.settingIsPath) ? logo.setting : "cachyos"
        fallback: "start-here-kde"
    }
}
