# Arquitetura do Projeto

## Visão Geral

Mouse Button Control é uma aplicação modular construída em Python com PyQt6 para interface gráfica.

## Diagrama de Camadas

```
┌─────────────────────────────────────┐
│        Interface Gráfica (UI)       │ PyQt6 + QSS Styling
│  ┌────────────────────────────────┐ │
│  │  MainWindow                    │ │
│  │  ├─ ProfilesTab               │ │
│  │  ├─ ButtonsTab                │ │
│  │  ├─ MacrosTab                 │ │
│  │  ├─ KeyboardTab               │ │
│  │  ├─ AutomationTab             │ │
│  │  ├─ SettingsTab               │ │
│  │  └─ LogsTab                   │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
┌─────────────────────────────────────┐
│     Camada de Lógica de Negócio     │
│  ┌────────────────────────────────┐ │
│  │  ConfigManager                 │ │
│  │  MacroEngine                   │ │
│  │  ProfileSwitcher               │ │
│  │  DeviceManager                 │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
┌─────────────────────────────────────┐
│     Camada de Acesso a Dados        │
│  ┌────────────────────────────────┐ │
│  │  DatabaseManager (SQLite)      │ │
│  │  - Profiles                    │ │
│  │  - Configurations              │ │
│  │  - Button Mappings             │ │
│  │  - Macros                      │ │
│  │  - Action Logs                 │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
┌─────────────────────────────────────┐
│        Camada de Sistema             │
│  ┌────────────────────────────────┐ │
│  │  DeviceListener (pynput)       │ │
│  │  ActionExecutor                │ │
│  │  SystemIntegration             │ │
│  │  AppDetector                   │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
     Linux Kernel
  /dev/input/  D-Bus  X11/Wayland
```

## Módulos Principais

### 1. Config (`config/`)

**Responsabilidade:** Gerenciar configurações e persistência de dados.

**Componentes:**
- `ConfigManager`: Interface de alto nível para configurações
- `DatabaseManager`: Gerencia SQLite database
- `defaults.py`: Configurações padrão

**Fluxo:**
```
ConfigManager
    ↓
DatabaseManager
    ↓
sqlite3 (config.db)
```

### 2. Device (`device/`)

**Responsabilidade:** Detectar e gerenciar dispositivos de entrada.

**Componentes:**
- `DeviceManager`: Gerencia dispositivos conectados
- `DeviceListener`: Escuta eventos de mouse/teclado
- `EvdevHandler`: Acesso direto a evdev (Linux)

**Fluxo:**
```
DeviceManager (scan devices)
    ↓
/proc/bus/input/devices
    ↓
DeviceListener (listen events)
    ↓
pynput callbacks
```

### 3. Macro (`macro/`)

**Responsabilidade:** Gravar e executar macros.

**Componentes:**
- `MacroEngine`: Engine para gravação e execução
- `ActionExecutor`: Executa ações individuais
- `MacroParser`: Parse definições de macro

**Fluxo:**
```
MacroEngine
    ├─ record_start()
    ├─ record_action()
    ├─ record_stop() → actions[]
    └─ execute_macro(actions[])
        ↓
    ActionExecutor
        ├─ execute_key_action()
        ├─ execute_command()
        ├─ execute_media_action()
        └─ execute_volume_action()
```

### 4. Automation (`automation/`)

**Responsabilidade:** Automação de troca de perfil.

**Componentes:**
- `ProfileSwitcher`: Troca perfil automaticamente
- `AppDetector`: Detecta aplicação ativa

**Fluxo:**
```
ProfileSwitcher
    ↓
_monitor_app() (thread)
    ↓
AppDetector.get_active_app()
    ↓
xdotool getactivewindow
    ↓
Compara com app_profile_map
    ↓
ConfigManager.set_active_profile()
```

### 5. UI (`ui/`)

**Responsabilidade:** Interface gráfica.

**Componentes:**
- `MainWindow`: Janela principal com abas
- `tabs/`: Cada aba é um módulo separado
- `dialogs/`: Diálogos específicos
- `widgets/`: Widgets customizados

**Estrutura:**
```
MainWindow
    ├─ ProfilesTab
    ├─ ButtonsTab
    ├─ MacrosTab
    ├─ KeyboardTab
    ├─ AutomationTab
    ├─ SettingsTab
    └─ LogsTab
        ↓ (usa)
    ConfigManager
    MacroEngine
    DeviceManager
    ProfileSwitcher
```

### 6. System (`system/`)

**Responsabilidade:** Integração com sistema Linux.

**Componentes:**
- `SystemIntegration`: Detecção de display server, autostart, etc.

**Funcionalidades:**
- Detectar X11 vs Wayland
- Setup de autostart
- Integração D-Bus

## Fluxo de Dados

### Execução de Botão

```
1. DeviceListener.on_click()
   ↓
2. Callback para MainWindow/Engine
   ↓
3. Buscar mapeamento do botão
   ConfigManager.get_button_mapping(button)
   ↓
4. Executar ação
   ActionExecutor.execute_action(action_type, action_value)
   ↓
5. Logar ação
   DatabaseManager.log_action()
   ↓
6. Atualizar UI (se aplicável)
```

### Auto-Troca de Perfil

```
1. ProfileSwitcher._monitor_app() (thread)
   ↓
2. AppDetector.get_active_app()
   ↓
3. Comparar com app_profile_map
   ↓
4. Se mudou:
   a. ConfigManager.set_active_profile(new_id)
   b. Notificar UI via signal
   ↓
5. Logar mudança
```

### Salvar Configuração

```
1. Usuário modifica algo na UI
   ↓
2. UI emite signal com dados
   ↓
3. ConfigManager.save_profile(profile)
   ↓
4. DatabaseManager.save_profile(profile)
   ↓
5. Gravar em SQLite
   ↓
6. Mostrar confirmação na UI
   ↓
7. Auto-backup (a cada 60s)
```

## Thread Safety

- **DeviceListener**: Roda em thread separada (pynput)
- **ProfileSwitcher**: Roda em thread separada
- **Main Thread**: PyQt6 event loop
- **Communication**: Sinais Qt (thread-safe)

## Padrões de Design

### Singleton
```python
class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Observer
```python
# ProfileSwitcher notifica mudança de perfil
self.on_profile_changed = callback
self.on_profile_changed(profile_id)
```

### Command Pattern
```python
action = {
    "type": "key",
    "value": "ctrl+c"
}
executor.execute_action(action["type"], action["value"])
```

## Extensibilidade

### Adicionar Novo Tipo de Ação

```python
# Em ActionExecutor
def _execute_custom_action(self, value: str) -> bool:
    # Implementar
    pass

def execute_action(self, action_type: str, action_value: str) -> bool:
    # ...
    elif action_type == "custom":
        return self._execute_custom_action(action_value)
```

### Adicionar Novo Tipo de Aba

```python
# Criar novo arquivo em ui/tabs/
# tabs/custom_tab.py

class CustomTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        pass

# Em MainWindow
from .tabs.custom_tab import CustomTab
self.tabs.addTab(CustomTab(), "Customizada")
```

## Performance

- **Device Polling**: 10ms de intervalo
- **Profile Monitoring**: 1s de intervalo
- **Auto-save**: 60s de intervalo
- **Log Rotation**: Diário por arquivo

## Segurança

- Acesso a `/dev/input/` requer grupo `input`
- Senhas não armazenadas
- Executáveis apenas com permissão do usuário
- Comandos não executam com escalação

