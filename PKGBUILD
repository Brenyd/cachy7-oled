# Build from inside the unpacked Cachy7-OLED folder:  makepkg -si
# Remove:  cachy7-oled revert   (as your user)  then  sudo pacman -R cachy7-oled-theme
pkgname=cachy7-oled-theme
pkgver=1.1
pkgrel=1
pkgdesc="Windows 7 Aero inspired, OLED-black theme for KDE Plasma 6 with CachyOS branding"
arch=('any')
license=('GPL-2.0-or-later')
depends=('plasma-workspace' 'kwin' 'breeze-icons')
install=cachy7-oled.install

package() {
    cd "$startdir"
    bash ./cachy7-oled install-files --dest "$pkgdir/usr/share" --bin "$pkgdir/usr/bin"
}
