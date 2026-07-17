#!/bin/bash
# Mouse Button Control - Quick Install Script

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Mouse Button Control for Linux - Installation Script     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION=$VERSION_ID
else
    echo "❌ Sistema operacional não identificado"
    exit 1
fi

echo "🔍 Detectado: $OS $VERSION"
echo ""

# Install system dependencies
echo "📦 Instalando dependências do sistema..."

case $OS in
    ubuntu|debian)
        sudo apt-get update
        sudo apt-get install -y python3.12 python3.12-dev python3-pip \
            libdbus-1-dev libglib2.0-dev libx11-dev libxrandr-dev \
            libxi-dev libinput-dev udev xdotool
        ;;
    fedora|rhel|centos)
        sudo dnf install -y python3.12 python3.12-devel dbus-devel \
            glib2-devel libX11-devel libXrandr-devel libXi-devel \
            libinput-devel systemd-devel xdotool
        ;;
    arch|manjaro)
        sudo pacman -Sy --noconfirm python python-pip dbus glib libx11 \
            libxrandr libxi libinput udev xdotool
        ;;
    *)
        echo "❌ Sistema operacional não suportado: $OS"
        exit 1
        ;;
esac

echo "✅ Dependências instaladas"
echo ""

# Setup user permissions
echo "🔐 Configurando permissões de acesso a dispositivos..."
sudo usermod -a -G input $USER
echo "⚠️  Você precisa fazer logout e login novamente para aplicar as permissões"
echo ""

# Create virtual environment
echo "🔧 Criando ambiente virtual..."
python3.12 -m venv venv
source venv/bin/activate
echo "✅ Ambiente virtual criado"
echo ""

# Install Python dependencies
echo "📚 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependências Python instaladas"
echo ""

# Create config directories
echo "📁 Criando diretórios de configuração..."
mkdir -p ~/.config/mouse-button-control/{logs,profiles,backups}
echo "✅ Diretórios criados"
echo ""

# Setup autostart
echo "🚀 Configurando inicialização automática..."
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/mouse-button-control.desktop << 'EOF'
[Desktop Entry]
Type=Application
Exec=mouse-button-control
Name=Mouse Button Control
Comment=Advanced mouse button customization
StartupNotify=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
EOF
echo "✅ Inicialização automática configurada"
echo ""

# Run first time setup
echo "🎯 Executando primeira vez..."
python -m mouse_button_control.main &
PID=$!
sleep 3
kill $PID 2>/dev/null || true

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✨ Instalação Concluída! ✨                    ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║                                                            ║"
echo "║ Para executar:                                           ║"
echo "║   source venv/bin/activate                               ║"
echo "║   mouse-button-control                                   ║"
echo "║                                                            ║"
echo "║ ⚠️  IMPORTANTE: Faça logout/login para aplicar permissões ║"
echo "║                                                            ║"
echo "┑ Documentação: docs/installation.md                       ║"
echo "║ Guia de Uso: docs/usage.md                                ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
