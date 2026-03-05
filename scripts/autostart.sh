#!/bin/bash
# Script de autostart para exibir o link do Dashboard no Desktop Remoto

# Aguarda o ambiente Wayland estar disponível
sleep 3

# Função para buscar o link no log MAIS RECENTE do Cloudflare
get_url() {
    grep -oE "https://[a-zA-Z0-9.-]+\.trycloudflare\.com" /home/opc/litemode/tunnel.log | tail -n 1
}

# Aguarda até 30 segundos pelo link ser gerado
for i in {1..30}; do
    URL=$(get_url)
    [ ! -z "$URL" ] && break
    sleep 1
done

[ -z "$URL" ] && URL="Aguardando link do Cloudflare..."

# Abre o terminal de uso geral (em background)
/usr/bin/weston-terminal &

# Abre o terminal exibindo o link (este trava a execução do script até ser fechado)
/usr/bin/weston-terminal --command="bash -c \"clear; echo -e '\n\n   --- LITEMODE DASHBOARD LINK ---\n\n   $URL\n\n   (Copie este link para seu navegador local)\n\n'; read -p 'Pressione Enter para fechar esta janela de aviso...'\""
