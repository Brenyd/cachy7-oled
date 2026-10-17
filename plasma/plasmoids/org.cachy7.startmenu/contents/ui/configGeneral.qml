import QtQuick
import QtQuick.Controls as QQC2
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.SimpleKCM {
    property alias cfg_logo: logoField.text
    property alias cfg_showFrequent: frequentBox.checked
    property alias cfg_maxFrequent: frequentSpin.value

    Kirigami.FormLayout {
        QQC2.TextField {
            id: logoField
            Kirigami.FormData.label: i18n("Orb logo:")
            placeholderText: i18n("Automatic (CachyOS logo)")
        }
        QQC2.Label {
            text: i18n("Icon name (e.g. cachyos) or a full path to an SVG/PNG.")
            opacity: 0.7
            font: Kirigami.Theme.smallFont
        }
        QQC2.CheckBox {
            id: frequentBox
            Kirigami.FormData.label: i18n("Left column:")
            text: i18n("Show frequently used apps")
        }
        QQC2.SpinBox {
            id: frequentSpin
            Kirigami.FormData.label: i18n("How many:")
            from: 0
            to: 20
            enabled: frequentBox.checked
        }
    }
}
