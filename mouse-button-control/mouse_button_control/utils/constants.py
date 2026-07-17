"""Constants and enumerations."""

from enum import Enum

# Display Servers
SUPPORTED_DISPLAYS = ["X11", "WAYLAND"]

# Mouse Button Names
BUTTON_NAMES = {
    "left": "Botão Esquerdo",
    "right": "Botão Direito",
    "middle": "Botão do Meio",
    "scroll_up": "Roda para Cima",
    "scroll_down": "Roda para Baixo",
    "scroll_left": "Roda para Esquerda",
    "scroll_right": "Roda para Direita",
    "button_4": "Botão 4 (Avanço)",
    "button_5": "Botão 5 (Recuo)",
    "button_6": "Botão 6",
    "button_7": "Botão 7",
    "button_8": "Botão 8",
    "button_9": "Botão 9",
}

# Action Types
class ActionTypes(str, Enum):
    """Action types for button mapping."""
    NONE = "none"
    KEY = "key"
    COMMAND = "command"
    MACRO = "macro"
    MEDIA = "media"
    VOLUME = "volume"
    DISABLE = "disable"
    OPEN_FILE = "open_file"
    OPEN_FOLDER = "open_folder"
    OPEN_APP = "open_app"

ACTION_TYPES = [item.value for item in ActionTypes]

# Media Actions
MEDIA_ACTIONS = {
    "play_pause": "Reproduzir/Pausar",
    "next": "Próxima Faixa",
    "previous": "Faixa Anterior",
    "stop": "Parar",
}

# Volume Actions
VOLUME_ACTIONS = {
    "mute": "Mutar",
    "increase": "Aumentar Volume",
    "decrease": "Diminuir Volume",
}

# Profile Types
PROFILE_TYPES = {
    "default": "Padrão",
    "gaming": "Jogos",
    "work": "Trabalho",
    "custom": "Personalizado",
}

# System Config Paths
CONFIG_DIR = "~/.config/mouse-button-control"
DATABASE_FILE = "~/.config/mouse-button-control/config.db"
LOGS_DIR = "~/.config/mouse-button-control/logs"
PROFILES_DIR = "~/.config/mouse-button-control/profiles"
BACKUP_DIR = "~/.config/mouse-button-control/backups"

# Timing
DEFAULT_DOUBLE_CLICK_DELAY = 300  # ms
DEFAULT_REPEAT_DELAY = 50  # ms
DEFAULT_AUTO_CLICK_INTERVAL = 100  # ms

# Limits
MAX_MACRO_ACTIONS = 100
MAX_SEQUENCE_LENGTH = 1000
MAX_REPEAT_COUNT = 10000

# Key Modifiers
KEY_MODIFIERS = {
    "ctrl": "Control",
    "alt": "Alt",
    "shift": "Shift",
    "super": "Super",
    "meta": "Meta",
}
