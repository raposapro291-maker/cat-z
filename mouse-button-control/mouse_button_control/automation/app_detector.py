"""Application detector for finding active applications."""

import subprocess
from typing import Optional, List


class AppDetector:
    """Detects active application and window information."""

    @staticmethod
    def get_active_window() -> Optional[str]:
        """Get active window name."""
        try:
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            return result.stdout.strip()
        except Exception:
            return None

    @staticmethod
    def get_active_app() -> Optional[str]:
        """Get active application name."""
        try:
            window_name = AppDetector.get_active_window()
            if not window_name:
                return None
            
            # Extract app name from window title
            if " - " in window_name:
                return window_name.split(" - ")[0]
            return window_name
        except Exception:
            return None

    @staticmethod
    def get_active_window_pid() -> Optional[int]:
        """Get PID of active window."""
        try:
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowpid"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            return int(result.stdout.strip())
        except Exception:
            return None

    @staticmethod
    def get_running_processes() -> List[str]:
        """Get list of running processes."""
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            processes = []
            for line in result.stdout.split("\n")[1:]:  # Skip header
                parts = line.split()
                if len(parts) > 10:
                    processes.append(parts[10])
            return processes
        except Exception:
            return []

    @staticmethod
    def is_app_running(app_name: str) -> bool:
        """Check if application is running."""
        try:
            result = subprocess.run(
                ["pgrep", "-f", app_name],
                capture_output=True,
                timeout=1,
            )
            return result.returncode == 0
        except Exception:
            return False
