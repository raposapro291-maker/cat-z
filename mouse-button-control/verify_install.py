#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick test runner to verify installation."""

import sys
from pathlib import Path

print("\n╔═══════════════════════════════════════════════════════════╗")
print("║  Mouse Button Control - Installation Verification         ║")
print("╚═══════════════════════════════════════════════════════════╝\n")

# Check Python version
print("🐍 Verificando versão Python...")
if sys.version_info < (3, 12):
    print(f"❌ Python 3.12+ necessário. Encontrado: {sys.version}")
    sys.exit(1)
print(f"✅ Python {sys.version.split()[0]} OK\n")

# Check dependencies
print("📦 Verificando dependências...")
dependencies = [
    ("PyQt6", "PyQt6"),
    ("pynput", "pynput"),
    ("PIL", "Pillow"),
    ("psutil", "psutil"),
]

for import_name, package_name in dependencies:
    try:
        __import__(import_name)
        print(f"  ✅ {package_name}")
    except ImportError:
        print(f"  ❌ {package_name} - não instalado")
        sys.exit(1)

print("\n🗂️  Verificando estrutura de diretórios...")
required_dirs = [
    "mouse_button_control",
    "mouse_button_control/config",
    "mouse_button_control/device",
    "mouse_button_control/macro",
    "mouse_button_control/ui",
    "mouse_button_control/automation",
    "mouse_button_control/system",
    "mouse_button_control/utils",
    "mouse_button_control/i18n",
]

for dir_name in required_dirs:
    if Path(dir_name).exists():
        print(f"  ✅ {dir_name}/")
    else:
        print(f"  ❌ {dir_name}/ - não encontrado")
        sys.exit(1)

print("\n🎯 Testando módulos principais...")
try:
    from mouse_button_control.config import ConfigManager
    print("  ✅ ConfigManager")
    
    from mouse_button_control.device import DeviceManager
    print("  ✅ DeviceManager")
    
    from mouse_button_control.macro import MacroEngine
    print("  ✅ MacroEngine")
    
    from mouse_button_control.automation import ProfileSwitcher
    print("  ✅ ProfileSwitcher")
    
    from mouse_button_control.ui import MainWindow
    print("  ✅ MainWindow")
except Exception as e:
    print(f"  ❌ Erro ao importar: {e}")
    sys.exit(1)

print("\n📁 Verificando arquivos de configuração...")
config_path = Path.home() / ".config" / "mouse-button-control"
if config_path.exists():
    print(f"  ✅ Config em {config_path}")
else:
    print(f"  ⚠️  Config não existe (será criada na primeira execução)")

print("\n╔═══════════════════════════════════════════════════════════╗")
print("║              ✨ Tudo OK! ✨                                ║")
print("╠═══════════════════════════════════════════════════════════╣")
print("║                                                           ║")
print("║ Você pode executar agora:                                 ║")
print("║   python -m mouse_button_control.main                    ║")
print("║                                                           ║")
print("║ Ou com o atalho (após instalação):                        ║")
print("║   mouse-button-control                                   ║")
print("║                                                           ║")
print("╚═══════════════════════════════════════════════════════════╝\n")
