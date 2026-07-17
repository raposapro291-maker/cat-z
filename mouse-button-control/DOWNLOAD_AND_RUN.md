# Como Baixar e Executar Mouse Button Control

## 🚀 Instalação Rápida (Recomendado)

### 1. Clone o Repositório

```bash
git clone https://github.com/raposapro291-maker/cat-z.git
cd cat-z/mouse-button-control
git checkout mouse-button-control
```

### 2. Execute o Script de Instalação

```bash
chmod +x install.sh
./install.sh
```

O script vai:
- ✅ Instalar dependências do sistema
- ✅ Configurar permissões de acesso a dispositivos
- ✅ Criar ambiente virtual Python
- ✅ Instalar dependências Python
- ✅ Criar diretórios de configuração
- ✅ Configurar inicialização automática

### 3. Logout e Login

⚠️ **IMPORTANTE**: Para aplicar as permissões de acesso aos mouses:

```bash
# Logout e faça login novamente, ou:
newgrp input
```

### 4. Executar a Aplicação

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar
mouse-button-control

# Ou
python -m mouse_button_control.main
```

---

## 📦 Instalação Manual

Se o script de instalação não funcionar:

### 1. Instalar Dependências do Sistema

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-dev python3-pip \
    libdbus-1-dev libglib2.0-dev libx11-dev libxrandr-dev \
    libxi-dev libinput-dev udev xdotool
```

**Fedora/RHEL:**
```bash
sudo dnf install -y python3.12 python3.12-devel dbus-devel \
    glib2-devel libX11-devel libXrandr-devel libXi-devel \
    libinput-devel systemd-devel xdotool
```

**Arch:**
```bash
sudo pacman -Sy python python-pip dbus glib libx11 \
    libxrandr libxi libinput udev xdotool
```

### 2. Configurar Permissões

```bash
sudo usermod -a -G input $USER
newgrp input
```

### 3. Criar Ambiente Virtual

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependências Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Criar Diretórios de Configuração

```bash
mkdir -p ~/.config/mouse-button-control/{logs,profiles,backups}
```

### 6. Executar

```bash
python -m mouse_button_control.main
```

---

## ✅ Verificar Instalação

Antes de executar, verifique se tudo está correto:

```bash
python verify_install.py
```

Deve mostrar:
```
✅ Python 3.12 OK
✅ PyQt6
✅ pynput
✅ Pillow
✅ psutil
✅ Todos os módulos
```

---

## 🐛 Troubleshooting

### Erro: "Permission denied" ao acessar `/dev/input/`

```bash
# Verificar se está no grupo input
groups $USER

# Se não estiver:
sudo usermod -a -G input $USER
newgrp input
```

### Erro: "No module named 'PyQt6'"

```bash
# Certifique-se que está no venv ativado
source venv/bin/activate
pip install PyQt6==6.7.1
```

### Mouse não responde

1. Verifique se a aplicação está rodando
2. Veja os logs em `~/.config/mouse-button-control/logs/`
3. Reinicie a aplicação

### D-Bus error

```bash
# Reiniciar serviço D-Bus
sudo systemctl restart dbus
```

---

## 🎮 Primeira Execução

Na primeira vez que executar:

1. A aplicação cria automaticamente os perfis padrão (Padrão, Jogos, Trabalho)
2. Um banco de dados SQLite é criado em `~/.config/mouse-button-control/config.db`
3. Arquivos de log são criados em `~/.config/mouse-button-control/logs/`
4. Backups automáticos começam a ser feitos a cada 60s

---

## 🔄 Atualizar para Versão Mais Recente

```bash
cd cat-z/mouse-button-control
git pull origin mouse-button-control
pip install --upgrade -r requirements.txt
python -m mouse_button_control.main
```

---

## 📚 Documentação Adicional

- **Instalação Detalhada**: [docs/installation.md](docs/installation.md)
- **Guia de Uso**: [docs/usage.md](docs/usage.md)
- **Desenvolvimento**: [docs/development.md](docs/development.md)
- **Arquitetura**: [docs/architecture.md](docs/architecture.md)

---

## 🆘 Precisa de Ajuda?

1. Consulte a documentação em `docs/`
2. Verifique os logs em `~/.config/mouse-button-control/logs/`
3. Abra uma issue no GitHub
4. Veja as FAQ no README

---

**Aproveite seu Mouse Button Control! 🎉**
