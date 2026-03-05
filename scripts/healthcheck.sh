#!/bin/bash
# Script para monitorar se o LiteMode está online
DIR="/home/opc/litemode"
LOG="/home/opc/litemode/healthcheck.log"

check_url() {
    URL=$(grep -oE "https://[a-zA-Z0-9.-]+\.trycloudflare\.com" $1 | tail -n 1)
    if [ -z "$URL" ]; then
        return 1
    fi
    # Tenta pingar o URL via curl
    curl -s --head --request GET "$URL" | grep "200 OK" > /dev/null
    return $?
}

# Verifica túnel do Dashboard e do VNC
check_url "$DIR/tunnel.log"
DASH_OK=$?
check_url "$DIR/tunnel-vnc.log"
VNC_OK=$?

if [ $DASH_OK -ne 0 ] || [ $VNC_OK -ne 0 ]; then
    echo "[$(date)] URLs fora do ar ou não encontradas. Reiniciando serviços..." >> $LOG
    /home/opc/litemode/scripts/start-all.sh >> $LOG 2>&1
else
    echo "[$(date)] Serviços saudáveis." >> $LOG
fi
