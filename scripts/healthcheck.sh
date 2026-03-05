#!/bin/bash
# Script de Monitoramento Inteligente: Verifica processos locais em vez de URLs externas
DIR="/home/opc/litemode"
LOG="/home/opc/litemode/healthcheck.log"

# Função para verificar se um processo está ativo
check_process() {
    pgrep -f "$1" > /dev/null
    return $?
}

# 1. Verifica os processos essenciais
check_process "weston --backend=vnc"
WESTON_OK=$?

check_process "novnc_proxy"
NOVNC_OK=$?

check_process "api/main.py"
API_OK=$?

check_process "cloudflared tunnel"
TUNNEL_OK=$?

# 2. Avalia a saúde geral
if [ $WESTON_OK -ne 0 ] || [ $NOVNC_OK -ne 0 ] || [ $API_OK -ne 0 ] || [ $TUNNEL_OK -ne 0 ]; then
    echo "[$(date)] FALHA DETECTADA: Weston:$WESTON_OK, noVNC:$NOVNC_OK, API:$API_OK, Tunnel:$TUNNEL_OK. Reiniciando..." >> $LOG
    /home/opc/litemode/scripts/start-all.sh >> $LOG 2>&1
else
    # Opcional: apenas logar sucessos a cada hora para não encher o log
    if [ $(date +%M) -lt 05 ]; then
        echo "[$(date)] Sistema saudável (processos ativos)." >> $LOG
    fi
fi
