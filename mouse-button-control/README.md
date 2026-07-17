# Mouse Button Control for Linux

Uma aplicação completa e moderna para personalizar botões do mouse, teclado e atalhos globais no Linux, inspirada no X-Mouse Button Control do Windows.

## 🎯 Funcionalidades Principais

### Detecção de Dispositivos
- ✅ Detecção automática de todos os mouses conectados
- ✅ Suporte a múltiplos mouses simultaneamente
- ✅ Monitoramento de conexão/desconexão de dispositivos

### Configuração de Botões
- ✅ Reatribuição de funções dos botões
- ✅ Macros personalizadas
- ✅ Simulação de pressionamento de teclas
- ✅ Execução de comandos do terminal
- ✅ Abertura de programas
- ✅ Abertura de arquivos e pastas

### Controle de Sistema
- ✅ Controle de volume
- ✅ Controle de reprodução de mídia
- ✅ Bloqueio de botões específicos
- ✅ Repetição automática de teclas
- ✅ Clique duplo automático
- ✅ Auto click configurável

### Perfis e Automação
- ✅ Perfis diferentes (Jogos, Trabalho, Uso Comum)
- ✅ Troca automática de perfil por aplicativo
- ✅ Camadas de configuração avançadas
- ✅ Sistema de backup

### Compatibilidade
- ✅ Suporte nativo para Wayland
- ✅ Suporte nativo para X11
- ✅ Inicialização com o sistema
- ✅ Ícone na bandeja do sistema

### Recursos Avançados
- ✅ Editor visual de macros
- ✅ Atrasos em milissegundos
- ✅ Detecção de combinações de teclas
- ✅ Atalhos globais
- ✅ Sequências complexas de comandos
- ✅ Logs detalhados de ações
- ✅ Interface em português

## 🔧 Tecnologias

- **Python 3.12+**
- **PyQt6** - Interface gráfica moderna
- **pynput** - Captura de entrada
- **evdev** - Acesso a dispositivos Linux
- **pyautogui** - Automação
- **SQLite** - Armazenamento local
- **DBus** - Integração com sistema
- **systemd** - Inicialização automática

## 📋 Estrutura do Projeto

```
mouse-button-control/
├── README.md
├── LICENSE
├── setup.py
├── requirements.txt
├── mouse_button_control/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config_manager.py
│   │   ├── database.py
│   │   └── defaults.py
│   ├── device/
│   │   ├── __init__.py
│   │   ├── device_manager.py
│   │   ├── device_listener.py
│   │   └── evdev_handler.py
│   ├── macro/
│   │   ├── __init__.py
│   │   ├── macro_engine.py
│   │   ├── macro_parser.py
│   │   └── action_executor.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── tabs/
│   │   │   ├── __init__.py
│   │   │   ├── profiles_tab.py
│   │   │   ├── buttons_tab.py
│   │   │   ├── macros_tab.py
│   │   │   ├── keyboard_tab.py
│   │   │   ├── automation_tab.py
│   │   │   ├── settings_tab.py
│   │   │   └── logs_tab.py
│   │   ├── dialogs/
│   │   │   ├── __init__.py
│   │   │   ├── macro_editor.py
│   │   │   ├── button_mapper.py
│   │   │   ├── profile_manager.py
│   │   │   └── import_export.py
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   ├── system_tray.py
│   │   │   └── custom_widgets.py
│   │   └── resources/
│   │       ├── __init__.py
│   │       ├── icons.py
│   │       └── styles.qss
│   ├── automation/
│   │   ├── __init__.py
│   │   ├── profile_switcher.py
│   │   ├── app_detector.py
│   │   └── scheduler.py
│   ├── system/
│   │   ├── __init__.py
│   │   ├── wayland_support.py
│   │   ├── x11_support.py
│   │   ├── dbus_manager.py
│   │   └── system_integration.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── helpers.py
│   │   └── constants.py
│   └── i18n/
│       ├── __init__.py
│       ├── pt_BR.py
│       └── en_US.py
├── tests/
│   ├── __init__.py
│   ├── test_device_manager.py
│   ├── test_macro_engine.py
│   └── test_config_manager.py
├── docs/
│   ├── installation.md
│   ├── usage.md
│   ├── development.md
│   └── architecture.md
└── .github/
    └── workflows/
        └── ci.yml
```

## 🚀 Instalação

### Dependências do Sistema
```bash
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-dev python3-pip \
    libdbus-1-dev libglib2.0-dev libx11-dev libxrandr-dev \
    libxi-dev libinput-dev udev
```

### Instalação do Projeto
```bash
git clone https://github.com/raposapro291-maker/mouse-button-control.git
cd mouse-button-control
pip install -r requirements.txt
```

### Executar
```bash
python -m mouse_button_control.main
```

## 📖 Documentação

- [Instalação Detalhada](docs/installation.md)
- [Guia de Uso](docs/usage.md)
- [Guia de Desenvolvimento](docs/development.md)
- [Arquitetura do Projeto](docs/architecture.md)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**raposapro291-maker**

## ⭐ Agradecimentos

Inspirado no X-Mouse Button Control do Windows, desenvolvido para oferecer funcionalidades semelhantes e avançadas no Linux.

---

**Última atualização:** 2026-07-17
