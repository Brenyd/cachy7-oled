#!/usr/bin/env bash
# Shortcut for:  cachy7-oled uninstall   (restores your pre-theme setup, then deletes the files)
exec bash "$(dirname "$(readlink -f "$0")")/cachy7-oled" uninstall "$@"
