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

### Serviços Automatizados (Systemd)
O projeto inclui unidades do systemd para garantir que os serviços iniciem automaticamente no boot e se recuperem de falhas:
- **`litemode-autostart.service`**: Gerencia a inicialização completa de todos os componentes (Weston, noVNC, API e Túneis).
- **Ambiente Configurado**: Garante que o shell `bash` seja carregado com o ambiente do usuário (`PATH`, `HOME`, `SHELL`) corretamente definido para evitar problemas no prompt do terminal remoto.

## 📂 Transferência de Arquivos
O Dashboard permite a troca de arquivos entre sua máquina local e a instância remota:
- **Upload:** Os arquivos enviados pelo Dashboard são salvos na pasta `uploads/` na raiz do projeto.
- **Download:** Qualquer arquivo colocado manualmente na pasta `uploads/` da instância aparecerá no Dashboard para download em sua máquina local.

## 🔒 Segurança e Acesso

O LiteMode agora inclui proteção por senha para o Dashboard e utiliza túneis para evitar a exposição de portas.

### Configuração de Senha do Dashboard
Por padrão, o Dashboard é protegido pela senha `admin123`. Você pode alterar essa senha definindo a variável de ambiente `DASHBOARD_PASSWORD`.

1. **Alteração Temporária (Sessão Atual):**
   ```bash
   export DASHBOARD_PASSWORD="sua_nova_senha"
   ./scripts/start-all.sh
   ```

2. **Alteração Permanente (Recomendado):**
   Edite seu arquivo `~/.bashrc` ou adicione a variável diretamente no arquivo de serviço do systemd em `systemd/litemode-autostart.service`:
   ```ini
   Environment="DASHBOARD_PASSWORD=sua_nova_senha"
   ```

### Acesso ao Desktop Remoto (VNC)
O acesso ao Desktop via noVNC utiliza o link público gerado pelo Cloudflare. Para segurança adicional, o acesso é feito através de uma URL dinâmica e única a cada inicialização, enviada para o seu e-mail configurado.

---
Desenvolvido para uso pessoal e gerenciamento remoto eficiente.
