"""Database management system."""

import sqlite3
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class DatabaseManager:
    """Manages SQLite database for configurations and profiles."""

    def __init__(self, db_path: str = None):
        """Initialize database manager."""
        if db_path is None:
            db_path = Path.home() / ".config" / "mouse-button-control" / "config.db"
        else:
            db_path = Path(db_path)

        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self) -> None:
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Config table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT,
                type TEXT DEFAULT 'string',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Profiles table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT DEFAULT 'custom',
                description TEXT,
                data JSON,
                active BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Devices table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT,
                vendor_id TEXT,
                product_id TEXT,
                serial_number TEXT,
                connected BOOLEAN DEFAULT 1,
                data JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Button mappings table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS button_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                device_id INTEGER,
                button_name TEXT NOT NULL,
                action_type TEXT,
                action_value TEXT,
                double_click BOOLEAN DEFAULT 0,
                repeat BOOLEAN DEFAULT 0,
                repeat_interval INTEGER DEFAULT 50,
                hold_duration INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(profile_id) REFERENCES profiles(id),
                FOREIGN KEY(device_id) REFERENCES devices(id)
            )
        """
        )

        # Macros table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS macros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                actions JSON,
                trigger_type TEXT,
                trigger_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(profile_id) REFERENCES profiles(id)
            )
        """
        )

        # Hotkeys table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS hotkeys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                key_combination TEXT NOT NULL,
                action_type TEXT,
                action_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(profile_id) REFERENCES profiles(id)
            )
        """
        )

        # App auto-switch rules table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS app_auto_switch (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                app_name TEXT NOT NULL,
                app_path TEXT,
                window_title TEXT,
                enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(profile_id) REFERENCES profiles(id)
            )
        """
        )

        # Action logs table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT,
                action_value TEXT,
                device_name TEXT,
                button_name TEXT,
                profile_name TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_profiles_active ON profiles(active)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_button_mappings_profile ON button_mappings(profile_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_macros_profile ON macros(profile_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_hotkeys_profile ON hotkeys(profile_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_action_logs_timestamp ON action_logs(timestamp)")

        conn.commit()
        conn.close()

    def set_config(self, key: str, value: Any, value_type: str = "string") -> bool:
        """Set configuration value."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "REPLACE INTO config (key, value, type) VALUES (?, ?, ?)",
                (key, str(value), value_type),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error setting config: {e}")
            return False

    def get_config(self, key: str) -> Optional[Any]:
        """Get configuration value."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT value, type FROM config WHERE key = ?", (key,))
            row = cursor.fetchone()
            conn.close()
            if row:
                value, value_type = row
                if value_type == "boolean":
                    return value.lower() == "true"
                elif value_type == "integer":
                    return int(value)
                elif value_type == "float":
                    return float(value)
                return value
            return None
        except Exception as e:
            print(f"Error getting config: {e}")
            return None

    def save_profile(self, profile: Dict[str, Any]) -> Optional[int]:
        """Save or update profile."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if "id" in profile and profile["id"]:
                cursor.execute(
                    """
                    UPDATE profiles SET name=?, type=?, description=?, data=?, updated_at=CURRENT_TIMESTAMP
                    WHERE id=?
                    """,
                    (profile["name"], profile.get("type"), profile.get("description"), 
                     json.dumps(profile), profile["id"]),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO profiles (name, type, description, data)
                    VALUES (?, ?, ?, ?)
                    """,
                    (profile["name"], profile.get("type"), profile.get("description"), 
                     json.dumps(profile)),
                )
            conn.commit()
            profile_id = cursor.lastrowid
            conn.close()
            return profile_id
        except Exception as e:
            print(f"Error saving profile: {e}")
            return None

    def get_profile(self, profile_id: int) -> Optional[Dict[str, Any]]:
        """Get profile by ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM profiles WHERE id = ?", (profile_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None

    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """Get all profiles."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, type, active FROM profiles ORDER BY name")
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting profiles: {e}")
            return []

    def delete_profile(self, profile_id: int) -> bool:
        """Delete profile."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False

    def set_active_profile(self, profile_id: int) -> bool:
        """Set active profile."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE profiles SET active = 0")
            cursor.execute("UPDATE profiles SET active = 1 WHERE id = ?", (profile_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error setting active profile: {e}")
            return False

    def get_active_profile(self) -> Optional[int]:
        """Get active profile ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM profiles WHERE active = 1 LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            return row[0] if row else None
        except Exception as e:
            print(f"Error getting active profile: {e}")
            return None

    def log_action(self, action_type: str, action_value: str = "", device_name: str = "", 
                   button_name: str = "", profile_name: str = "") -> bool:
        """Log an action."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO action_logs (action_type, action_value, device_name, button_name, profile_name)
                VALUES (?, ?, ?, ?, ?)
                """,
                (action_type, action_value, device_name, button_name, profile_name),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error logging action: {e}")
            return False
