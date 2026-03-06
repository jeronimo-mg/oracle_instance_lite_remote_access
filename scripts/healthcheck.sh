#!/bin/bash
# Script de Monitoramento Inteligente: Verifica processos locais e túneis
DIR="/home/opc/litemode"
LOG="/home/opc/litemode/healthcheck.log"

# 1. Verifica os processos essenciais
pgrep -f "weston --backend=vnc" > /dev/null
WESTON_OK=$?

pgrep -f "novnc_proxy.*6080" > /dev/null
NOVNC_OK=$?

pgrep -f "python3 src/api/main.py" > /dev/null
API_OK=$?

# 2. Verifica se existem túneis cloudflared ativos para as portas 8001 e 6080
pgrep -f "cloudflared.*8001" > /dev/null
TUNNEL_API_OK=$?

pgrep -f "cloudflared.*6080" > /dev/null
TUNNEL_VNC_OK=$?

# 3. Avalia a saúde geral
if [ $WESTON_OK -ne 0 ] || [ $NOVNC_OK -ne 0 ] || [ $API_OK -ne 0 ] || [ $TUNNEL_API_OK -ne 0 ] || [ $TUNNEL_VNC_OK -ne 0 ]; then
    echo "[$(date)] FALHA DETECTADA: Weston:$WESTON_OK, noVNC:$NOVNC_OK, API:$API_OK, TunnelAPI:$TUNNEL_API_OK, TunnelVNC:$TUNNEL_VNC_OK. Reiniciando..." >> $LOG
    /home/opc/litemode/scripts/start-all.sh >> $LOG 2>&1
else
    # Logar saúde apenas a cada hora
    if [ $(date +%M) -lt 05 ]; then
        echo "[$(date)] Sistema e túneis saudáveis." >> $LOG
    fi
fi
