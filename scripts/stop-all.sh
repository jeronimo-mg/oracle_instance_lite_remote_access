#!/bin/bash
# Script para parar todos os serviços do LiteMode
echo "Parando serviços do LiteMode..."
sudo systemctl stop weston novnc 2>/dev/null
pkill -f "weston --backend=vnc"
pkill -f "novnc_proxy"
pkill -f "websockify"
pkill -f "api/main.py"
pkill -f "cloudflared tunnel"
rm -f /home/opc/litemode/tunnel-vnc.log
echo "Serviços parados."
