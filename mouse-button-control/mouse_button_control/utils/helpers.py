"""Helper functions."""

import subprocess
import os
from pathlib import Path


def run_command(command: str, shell: bool = False) -> bool:
    """Execute a shell command."""
    try:
        if shell:
            subprocess.Popen(command, shell=True)
        else:
            subprocess.Popen(command.split())
        return True
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return False


def open_file(file_path: str) -> bool:
    """Open a file with default application."""
    try:
        file_path = Path(file_path).expanduser().absolute()
        if file_path.exists():
            subprocess.Popen(["xdg-open", str(file_path)])
            return True
        return False
    except Exception as e:
        print(f"Erro ao abrir arquivo: {e}")
        return False


def open_folder(folder_path: str) -> bool:
    """Open a folder with default file manager."""
    try:
        folder_path = Path(folder_path).expanduser().absolute()
        if folder_path.exists():
            subprocess.Popen(["xdg-open", str(folder_path)])
            return True
        return False
    except Exception as e:
        print(f"Erro ao abrir pasta: {e}")
        return False


def get_active_window() -> str:
    """Get the active window name."""
    try:
        result = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowname"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def get_active_application() -> str:
    """Get the active application name."""
    try:
        result = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowname"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        window_name = result.stdout.strip()
        # Extract application name from window title
        if " - " in window_name:
            return window_name.split(" - ")[0]
        return window_name
    except Exception:
        return ""


def expand_path(path: str) -> str:
    """Expand user path and environment variables."""
    return os.path.expandvars(os.path.expanduser(path))
