"""Automatic profile switching based on active application."""

import subprocess
import time
from typing import Optional, Callable, Dict, List
from threading import Thread, Event


class ProfileSwitcher:
    """Automatically switches profiles based on active application."""

    def __init__(self, config_manager=None):
        """Initialize profile switcher."""
        self.config_manager = config_manager
        self.app_profile_map = {}  # app_name -> profile_id
        self.current_app = ""
        self.current_profile = None
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = Event()
        self.on_profile_changed = None

    def register_app_profile(self, app_name: str, profile_id: int) -> None:
        """Register an app to profile mapping."""
        self.app_profile_map[app_name.lower()] = profile_id

    def start_monitoring(self) -> None:
        """Start monitoring active application."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.stop_event.clear()
        self.monitor_thread = Thread(target=self._monitor_app, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self) -> None:
        """Stop monitoring."""
        self.monitoring = False
        self.stop_event.set()
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

    def _monitor_app(self) -> None:
        """Monitor active application."""
        while self.monitoring and not self.stop_event.is_set():
            try:
                active_app = self._get_active_app()
                if active_app.lower() != self.current_app.lower():
                    self.current_app = active_app
                    profile_id = self.app_profile_map.get(active_app.lower())
                    
                    if profile_id and profile_id != self.current_profile:
                        self.current_profile = profile_id
                        if self.on_profile_changed:
                            self.on_profile_changed(profile_id)
                
                time.sleep(1)  # Check every second
            except Exception as e:
                print(f"Error monitoring app: {e}")
                time.sleep(1)

    def _get_active_app(self) -> str:
        """Get the currently active application."""
        try:
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            window_name = result.stdout.strip()
            
            # Try to extract app name
            if " - " in window_name:
                return window_name.split(" - ")[0]
            return window_name
        except Exception:
            return ""

    def get_profile_for_app(self, app_name: str) -> Optional[int]:
        """Get profile for application."""
        return self.app_profile_map.get(app_name.lower())

    def get_app_mappings(self) -> Dict[str, int]:
        """Get all app to profile mappings."""
        return self.app_profile_map.copy()
