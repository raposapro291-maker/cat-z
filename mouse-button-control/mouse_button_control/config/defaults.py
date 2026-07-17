"""Default configuration values."""

DEFAULT_CONFIG = {
    "display_server": "auto",
    "start_on_boot": True,
    "minimize_to_tray": True,
    "theme": "dark",
    "language": "pt_BR",
    "auto_save_interval": 60,
    "enable_logs": True,
    "log_level": "INFO",
    "mouse_sensitivity": 1.0,
    "auto_profile_switch": True,
}

DEFAULT_PROFILE = {
    "name": "Padrão",
    "type": "default",
    "buttons": {},
    "hotkeys": {},
    "macros": {},
    "auto_switches": [],
    "enabled": True,
}

DEFAULT_BUTTON_CONFIG = {
    "action_type": "none",
    "action_value": "",
    "double_click": False,
    "repeat": False,
    "repeat_interval": 50,
    "hold_duration": 0,
}
