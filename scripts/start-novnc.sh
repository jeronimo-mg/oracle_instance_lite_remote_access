#!/bin/bash
# Start noVNC proxy targeting Weston

# Default VNC port is 5900 (Weston)
# Listen on 6080
novnc_proxy \
    --vnc localhost:5900 \
    --listen 6080 \
    --web /usr/share/novnc
