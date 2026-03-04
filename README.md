# Oracle Instance Lite Remote Access

Este projeto implementa o "Lite Mode" do [easi-remote-access](https://github.com/jeronimo-mg/easi-remote-access) em uma instância Linux (Oracle Cloud), fornecendo um desktop remoto rápido acessível via navegador.

## 🚀 Visão Geral

O objetivo principal é oferecer um ambiente de desktop leve e acessível via web, utilizando tecnologias modernas como Weston (Wayland), noVNC e túneis seguros para acesso remoto sem a necessidade de abrir portas no firewall.

## ✨ Principais Características

- **noVNC Web Client:** Acesso ao desktop diretamente pelo navegador.
- **Weston (Wayland):** Compositor moderno e leve com suporte nativo a VNC.
- **Cloudflare Tunnel:** Acesso público seguro através de túneis.
- **Tailscale:** Rede privada para acesso seguro ao painel de controle e serviços.
- **Dashboard React:** Interface de usuário construída com React/Vite para gerenciar a instância.
- **API Python (FastAPI):** Backend para gerenciar serviços e configurações.

## 🏗️ Arquitetura do Projeto

O projeto está organizado da seguinte forma:

- `dashboard/`: Frontend em React para gerenciamento.
- `src/api/`: Backend em Python para controle de serviços.
- `scripts/`: Scripts utilitários para iniciar Weston, noVNC, túneis e API.
- `systemd/`: Unidades de serviço para gerenciar o ciclo de vida do sistema.
- `configs/`: Configurações do ambiente (ex: `weston.ini`).

## 🛠️ Como Iniciar

### Pré-requisitos
- Python 3.x
- Node.js & npm
- Tailscale (opcional, para rede privada)
- Cloudflared (opcional, para túnel público)

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/jeronimo-mg/oracle_instance_lite_remote_access.git
   cd oracle_instance_lite_remote_access
   ```

2. Configure o Dashboard:
   ```bash
   cd dashboard
   npm install
   npm run build
   ```

3. Configure a API:
   ```bash
   # Recomenda-se o uso de ambiente virtual
   pip install -r requirements.txt # Se houver
   ```

### Executando os Serviços
Você pode iniciar todos os componentes de uma vez usando o script principal:

1. Iniciar tudo:
   ```bash
   ./scripts/start-all.sh
   ```
   *O script irá configurar o ambiente, iniciar os serviços e exibir os URLs de acesso (Dashboard e Desktop) gerados via Cloudflare Tunnel.*

2. Parar tudo:
   ```bash
   ./scripts/stop-all.sh
   ```

### Scripts Individuais (Opcional)
Se preferir gerenciar os componentes manualmente:
- Iniciar Desktop (Weston): `./scripts/start-weston.sh`
- Iniciar Web VNC: `./scripts/start-novnc.sh`
- Iniciar API: `./scripts/start-api.sh`
- Iniciar Túnel API: `./scripts/run-tunnel.sh`

## 🔒 Segurança
O projeto utiliza túneis e redes privadas para evitar a exposição direta de portas sensíveis à internet. Certifique-se de configurar corretamente seu token do Cloudflare ou sua rede Tailscale.

---
Desenvolvido para uso pessoal e gerenciamento remoto eficiente.
