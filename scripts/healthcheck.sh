#!/bin/bash
# Script de Monitoramento Inteligente: Verifica processos locais em vez de URLs externas
DIR="/home/opc/litemode"
LOG="/home/opc/litemode/healthcheck.log"

# Função para verificar se um processo está ativo
check_process() {
    pgrep -f "$1" > /dev/null
    return $?
}

# 1. Verifica os processos essenciais usando caminhos precisos
pgrep -f "weston --backend=vnc" > /dev/null
WESTON_OK=$?

pgrep -f "novnc_proxy.*6080" > /dev/null
NOVNC_OK=$?

pgrep -f "python3 src/api/main.py" > /dev/null
API_OK=$?

# 2. Avalia a saúde geral
# echo "DEBUG: Weston:$WESTON_OK, noVNC:$NOVNC_OK, API:$API_OK" >> /tmp/hc_debug.log
if [ $WESTON_OK -ne 0 ] || [ $NOVNC_OK -ne 0 ] || [ $API_OK -ne 0 ]; then
    echo "[$(date)] FALHA DETECTADA: Weston:$WESTON_OK, noVNC:$NOVNC_OK, API:$API_OK. Reiniciando..." >> $LOG
    /home/opc/litemode/scripts/start-all.sh >> $LOG 2>&1
else
    # Opcional: apenas logar sucessos a cada hora para não encher o log
    if [ $(date +%M) -lt 05 ]; then
        echo "[$(date)] Sistema saudável (processos ativos)." >> $LOG
    fi
fi
