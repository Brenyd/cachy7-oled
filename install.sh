#!/usr/bin/env bash
# Shortcut for:  ./cachy7-oled install [--layout|--no-layout] [--logo FILE] [--no-apply]
exec bash "$(dirname "$(readlink -f "$0")")/cachy7-oled" install "$@"
