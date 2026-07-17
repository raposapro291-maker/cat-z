"""Configuration manager."""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from .database import DatabaseManager
from .defaults import DEFAULT_CONFIG, DEFAULT_PROFILE


class ConfigManager:
    """Manages application configuration."""

    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = Path.home() / ".config" / "mouse-button-control"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.db = DatabaseManager()
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Load default configuration."""
        for key, value in DEFAULT_CONFIG.items():
            if self.db.get_config(key) is None:
                value_type = type(value).__name__
                self.db.set_config(key, value, value_type)

    def set(self, key: str, value: Any) -> bool:
        """Set configuration value."""
        value_type = type(value).__name__
        return self.db.set_config(key, value, value_type)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        value = self.db.get_config(key)
        return value if value is not None else default

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        config = {}
        for key in DEFAULT_CONFIG.keys():
            config[key] = self.get(key)
        return config

    def save_profile(self, profile: Dict[str, Any]) -> Optional[int]:
        """Save profile."""
        return self.db.save_profile(profile)

    def get_profile(self, profile_id: int) -> Optional[Dict[str, Any]]:
        """Get profile."""
        return self.db.get_profile(profile_id)

    def get_all_profiles(self) -> list:
        """Get all profiles."""
        return self.db.get_all_profiles()

    def delete_profile(self, profile_id: int) -> bool:
        """Delete profile."""
        return self.db.delete_profile(profile_id)

    def set_active_profile(self, profile_id: int) -> bool:
        """Set active profile."""
        return self.db.set_active_profile(profile_id)

    def get_active_profile(self) -> Optional[int]:
        """Get active profile ID."""
        return self.db.get_active_profile()

    def create_default_profiles(self) -> None:
        """Create default profiles if they don't exist."""
        profiles = self.get_all_profiles()
        if not profiles:
            for profile_type in ["default", "gaming", "work"]:
                profile = DEFAULT_PROFILE.copy()
                profile["type"] = profile_type
                if profile_type == "gaming":
                    profile["name"] = "Jogos"
                elif profile_type == "work":
                    profile["name"] = "Trabalho"
                self.save_profile(profile)

    def export_profile(self, profile_id: int, export_path: str) -> bool:
        """Export profile to JSON file."""
        try:
            profile = self.get_profile(profile_id)
            if profile:
                export_path = Path(export_path).expanduser()
                with open(export_path, "w") as f:
                    json.dump(profile, f, indent=2)
                return True
        except Exception as e:
            print(f"Error exporting profile: {e}")
        return False

    def import_profile(self, import_path: str) -> Optional[int]:
        """Import profile from JSON file."""
        try:
            import_path = Path(import_path).expanduser()
            with open(import_path, "r") as f:
                profile = json.load(f)
            return self.save_profile(profile)
        except Exception as e:
            print(f"Error importing profile: {e}")
        return None

    def backup_config(self, backup_path: str = None) -> bool:
        """Backup configuration database."""
        try:
            if backup_path is None:
                backup_dir = self.config_dir / "backups"
                backup_dir.mkdir(exist_ok=True)
                from datetime import datetime
                backup_path = backup_dir / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            import shutil
            shutil.copy(self.db.db_path, backup_path)
            return True
        except Exception as e:
            print(f"Error backing up config: {e}")
            return False
