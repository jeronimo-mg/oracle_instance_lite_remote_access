#!/bin/bash
# Script para parar todos os serviços do LiteMode
echo "Parando serviços do LiteMode..."

# 1. Tentar parar via systemctl
sudo systemctl stop weston novnc 2>/dev/null

# 2. Tentar parar processos graciosamente (SIGTERM)
pkill -f "weston --backend=vnc"
pkill -f "novnc_proxy"
pkill -f "websockify"
pkill -f "api/main.py"
pkill -f "cloudflared tunnel"

sleep 1

# 3. Forçar parada se ainda houver algo (SIGKILL)
pkill -9 -f "weston --backend=vnc"
pkill -9 -f "novnc_proxy"
pkill -9 -f "api/main.py"
pkill -9 -f "cloudflared tunnel"

# 4. Limpar arquivos temporários
rm -f /home/opc/litemode/tunnel.log
rm -f /home/opc/litemode/tunnel-vnc.log

# 5. Aguardar liberação das portas (VNC: 5900, noVNC: 6080, API: 8001)
echo "Aguardando liberação de portas..."
for port in 5900 6080 8001; do
    while sudo ss -tulpn | grep -q ":$port "; do
        echo "Aguardando porta $port ser liberada..."
        sleep 1
    done
done

echo "Serviços parados e portas liberadas."
