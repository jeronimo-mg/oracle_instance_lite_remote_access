#!/bin/bash
# Script para iniciar todos os serviços do LiteMode de forma limpa

LOCKFILE="/tmp/litemode-start.lock"

# Evitar execuções simultâneas
if [ -e $LOCKFILE ]; then
    PID=$(cat $LOCKFILE)
    if ps -p $PID > /dev/null; then
        echo "ERRO: Já existe uma instância de start-all.sh rodando (PID: $PID)."
        exit 1
    fi
fi
echo $$ > $LOCKFILE

# Garantir remoção do lockfile ao sair
trap "rm -f $LOCKFILE" EXIT

export SHELL=/bin/bash
export PATH=/home/opc/.local/bin:/home/opc/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR/.."

echo "Iniciando LiteMode... [$(date)]"

# 1. Parar tudo primeiro
./scripts/stop-all.sh

# 2. Iniciar Weston
echo "Iniciando Desktop (Weston)..."
nohup ./scripts/start-weston.sh > /tmp/weston_start.log 2>&1 &
sleep 5

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
nohup cloudflared tunnel --protocol http2 --url http://127.0.0.1:6080 > /home/opc/litemode/tunnel-vnc.log 2>&1 &
sleep 10

# 6. Mostrar URLs e Salvar na Área de Trabalho
echo "Aguardando geração dos links dinâmicos..."
for i in {1..30}; do
    URL_DASH=$(grep -oE "https://[a-zA-Z0-9.-]+\.trycloudflare\.com" /home/opc/litemode/tunnel.log | tail -n 1)
    URL_VNC=$(grep -oE "https://[a-zA-Z0-9.-]+\.trycloudflare\.com" /home/opc/litemode/tunnel-vnc.log | tail -n 1)
    [ ! -z "$URL_DASH" ] && [ ! -z "$URL_VNC" ] && break
    sleep 1
done

# 7. Verificar se os processos principais estão realmente vivos
WESTON_RUNNING=$(pgrep -f "weston --backend=vnc")
API_RUNNING=$(pgrep -f "api/main.py")

if [ -z "$WESTON_RUNNING" ] || [ -z "$API_RUNNING" ]; then
    echo "ERRO: Falha ao iniciar serviços críticos (Weston ou API)." >> /home/opc/litemode/start-all.log
    exit 1
fi

# Garantir que o Desktop existe e salvar o link
mkdir -p /home/opc/Desktop
echo -e "--- LITEMODE DASHBOARD ---\n\n$URL_DASH\n" > /home/opc/Desktop/LINKS.txt
chmod 666 /home/opc/Desktop/LINKS.txt

# 8. Enviar Notificação por E-mail
echo "Enviando notificação por e-mail..."
if [ -z "$URL_DASH" ] || [ -z "$URL_VNC" ]; then
    echo "ERRO: Uma ou ambas as URLs não foram encontradas após 30 segundos." >> /home/opc/litemode/start-all.log
else
    python3 /home/opc/litemode/scripts/send_email.py "$URL_DASH" "$URL_VNC" >> /home/opc/litemode/start-all.log 2>&1
fi

echo "----------------------------------------------------------------"
echo "LiteMode iniciado com sucesso! [$(date)]" >> /home/opc/litemode/start-all.log
echo "LiteMode iniciado com sucesso!"
echo "Acesse o Dashboard em: $URL_DASH"
echo "Acesse o Desktop em: $URL_VNC/vnc.html"
echo "----------------------------------------------------------------"
