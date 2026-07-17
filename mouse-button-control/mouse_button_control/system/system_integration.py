"""System integration utilities."""

import os
import subprocess
from pathlib import Path
from typing import Optional


class SystemIntegration:
    """Handles system integration."""

    @staticmethod
    def get_display_server() -> Optional[str]:
        """Detect display server (X11 or Wayland)."""
        if os.environ.get("WAYLAND_DISPLAY"):
            return "wayland"
        elif os.environ.get("DISPLAY"):
            return "x11"
        return None

    @staticmethod
    def setup_autostart(app_name: str = "mouse-button-control") -> bool:
        """Setup autostart on login."""
        try:
            autostart_dir = Path.home() / ".config" / "autostart"
            autostart_dir.mkdir(parents=True, exist_ok=True)
            
            desktop_file = autostart_dir / f"{app_name}.desktop"
            
            content = f"""
[Desktop Entry]
Type=Application
Exec=mouse-button-control
Name=Mouse Button Control
Comment=Advanced mouse button customization
StartupNotify=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
"""
            
            with open(desktop_file, "w") as f:
                f.write(content.strip())
            
            return True
        except Exception as e:
            print(f"Error setting up autostart: {e}")
            return False

    @staticmethod
    def remove_autostart(app_name: str = "mouse-button-control") -> bool:
        """Remove autostart entry."""
        try:
            desktop_file = Path.home() / ".config" / "autostart" / f"{app_name}.desktop"
            if desktop_file.exists():
                desktop_file.unlink()
            return True
        except Exception as e:
            print(f"Error removing autostart: {e}")
            return False

    @staticmethod
    def is_autostart_enabled(app_name: str = "mouse-button-control") -> bool:
        """Check if autostart is enabled."""
        desktop_file = Path.home() / ".config" / "autostart" / f"{app_name}.desktop"
        return desktop_file.exists()

    @staticmethod
    def get_dbus_session_bus_address() -> Optional[str]:
        """Get D-Bus session bus address."""
        try:
            result = subprocess.run(
                ["dbus-uuidgen"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            return result.stdout.strip()
        except Exception:
            return None

    @staticmethod
    def get_session_type() -> Optional[str]:
        """Get session type from environment."""
        return os.environ.get("XDG_SESSION_TYPE")
