#!/bin/bash
# Start Weston with VNC backend

# Set runtime directory
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/tmp/weston-runtime}
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"

# Basic Weston configuration
# We use kiosk-shell.so for a simplified UI (no title bars etc.?)
# Or desktop-shell.so for a standard desktop.
# OL10 likely has desktop-shell.so.

# Launch weston
weston \
    --backend=vnc \
    --shell=desktop-shell.so \
    --config=/home/opc/litemode/configs/weston.ini \
    --port=5900 \
    --width=1280 \
    --height=1024 \
    --disable-transport-layer-security \
    --log=/tmp/weston.log
