#!/bin/bash
# Script para iniciar todos os serviços do LiteMode de forma limpa

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR/.."

echo "Iniciando LiteMode..."

# 1. Parar tudo primeiro
./scripts/stop-all.sh

# 2. Iniciar Weston
echo "Iniciando Desktop (Weston)..."
nohup ./scripts/start-weston.sh > /tmp/weston_start.log 2>&1 &
sleep 2

# 3. Iniciar noVNC
echo "Iniciando Web Interface (noVNC)..."
nohup ./scripts/start-novnc.sh > /tmp/novnc_start.log 2>&1 &
sleep 2

# 4. Iniciar API
echo "Iniciando Management API..."
nohup ./scripts/start-api.sh > /tmp/api_start.log 2>&1 &
sleep 2

# 5. Iniciar Túneis Cloudflare
echo "Iniciando Túneis Cloudflare..."
./scripts/run-tunnel.sh
nohup cloudflared tunnel --url http://127.0.0.1:6080 > /home/opc/litemode/tunnel-vnc.log 2>&1 &
sleep 10

# 6. Mostrar URLs e Salvar na Área de Trabalho
echo "Aguardando geração dos links dinâmicos..."
for i in {1..30}; do
    URL_DASH=$(grep -oE "https://[a-zA-Z0-9.-]+\.trycloudflare\.com" /home/opc/litemode/tunnel.log | tail -n 1)
    URL_VNC=$(grep -oE "https://[a-zA-Z0-9.-]+\.trycloudflare\.com" /home/opc/litemode/tunnel-vnc.log | tail -n 1)
    [ ! -z "$URL_DASH" ] && [ ! -z "$URL_VNC" ] && break
    sleep 1
done

# Garantir que o Desktop existe e salvar o link
mkdir -p /home/opc/Desktop
echo -e "--- LITEMODE DASHBOARD ---\n\n$URL_DASH\n" > /home/opc/Desktop/LINKS.txt
chmod 666 /home/opc/Desktop/LINKS.txt

echo "----------------------------------------------------------------"
echo "LiteMode iniciado com sucesso!"
echo "Acesse o Dashboard em: $URL_DASH"
echo "Acesse o Desktop em: $URL_VNC/vnc.html"
echo "----------------------------------------------------------------"
