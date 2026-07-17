# Instalação

## Requisitos do Sistema

- **Python 3.12+**
- **Linux** (testado em Ubuntu 22.04+, Fedora 38+, Debian 12+)
- **Wayland ou X11**
- Acesso a dispositivos de entrada (`/dev/input/`)

## Dependências do Sistema

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-dev python3-pip \
    libdbus-1-dev libglib2.0-dev libx11-dev libxrandr-dev \
    libxi-dev libinput-dev udev xdotool
```

### Fedora/RHEL
```bash
sudo dnf install -y python3.12 python3.12-devel dbus-devel \
    glib2-devel libX11-devel libXrandr-devel libXi-devel \
    libinput-devel systemd-devel xdotool
```

### Arch Linux
```bash
sudo pacman -S python python-pip dbus glib libx11 libxrandr \
    libxi libinput udev xdotool
```

## Instalação da Aplicação

### Opção 1: Instalação Local

```bash
# Clonar repositório
git clone https://github.com/raposapro291-maker/cat-z.git
cd cat-z/mouse-button-control

# Criar ambiente virtual
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows (se aplicável)

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python -m mouse_button_control.main
```

### Opção 2: Instalação Global

```bash
git clone https://github.com/raposapro291-maker/cat-z.git
cd cat-z/mouse-button-control

# Instalar como pacote
sudo pip install -e .

# Executar
mouse-button-control
```

### Opção 3: Instalação via Pip (quando publicado)

```bash
pip install mouse-button-control
mouse-button-control
```

## Configuração Inicial

### 1. Permissões de Acesso a Dispositivos

A aplicação precisa acessar `/dev/input/`. Para evitar usar `sudo`:

```bash
# Adicionar usuário ao grupo input
sudo usermod -a -G input $USER

# Aplicar mudanças (reiniciar sessão ou executar)
newgrp input
```

### 2. Inicialização Automática

A aplicação cria automaticamente um arquivo `.desktop` em `~/.config/autostart/`

Para desabilitar:
```bash
rm ~/.config/autostart/mouse-button-control.desktop
```

### 3. Primeira Execução

```bash
mouse-button-control
```

A aplicação criará:
- `~/.config/mouse-button-control/config.db` - Banco de dados
- `~/.config/mouse-button-control/logs/` - Arquivos de log
- `~/.config/mouse-button-control/profiles/` - Perfis salvos
- `~/.config/mouse-button-control/backups/` - Backups automáticos

## Troubleshooting

### Erro: "Permission denied" ao acessar `/dev/input/`

```bash
# Opção 1: Usar sudo (não recomendado)
sudo mouse-button-control

# Opção 2: Adicionar ao grupo input
sudo usermod -a -G input $USER
newgrp input
```

### Erro: "No module named 'PyQt6'"

```bash
pip install PyQt6==6.7.1
```

### Erro: "Cannot connect to D-Bus"

```bash
# Reiniciar serviço D-Bus
sudo systemctl restart dbus
```

### Wayland não detectado

Verifique se você está usando Wayland:
```bash
echo $XDG_SESSION_TYPE
# Deve retornar "wayland" ou "x11"
```

## Desinstalação

### Remover arquivos de configuração

```bash
rm -rf ~/.config/mouse-button-control
rm ~/.config/autostart/mouse-button-control.desktop
```

### Desinstalar pacote

```bash
pip uninstall mouse-button-control
```

## Próximos Passos

- Consulte [Guia de Uso](usage.md) para aprender a usar a aplicação
- Consulte [Desenvolvimento](development.md) para contribuir
