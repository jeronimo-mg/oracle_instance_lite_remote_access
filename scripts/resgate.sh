#!/bin/bash
# Script de Resgate LiteMode
export WAYLAND_DISPLAY=wayland-1
export XDG_RUNTIME_DIR=/tmp/weston-runtime
echo "Resgatando janelas..."
pkill -f weston-desktop-shell
echo "Layout resetado. Verifique sua tela agora!"
