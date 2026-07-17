"""Action executor for macros and button mappings."""

import time
import subprocess
from pathlib import Path
from pynput import keyboard, mouse
from typing import Dict, List, Any, Optional


class ActionExecutor:
    """Executes configured actions."""

    def __init__(self):
        """Initialize action executor."""
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Mouse()
        self.last_action_time = 0

    def execute_action(self, action_type: str, action_value: str) -> bool:
        """Execute an action."""
        try:
            if action_type == "none":
                return True
            elif action_type == "key":
                return self._execute_key_action(action_value)
            elif action_type == "command":
                return self._execute_command(action_value)
            elif action_type == "open_file":
                return self._open_file(action_value)
            elif action_type == "open_folder":
                return self._open_folder(action_value)
            elif action_type == "open_app":
                return self._open_app(action_value)
            elif action_type == "media":
                return self._execute_media_action(action_value)
            elif action_type == "volume":
                return self._execute_volume_action(action_value)
            else:
                return False
        except Exception as e:
            print(f"Error executing action: {e}")
            return False

    def _execute_key_action(self, key_combo: str) -> bool:
        """Execute keyboard action."""
        try:
            keys = key_combo.split("+")
            modifiers = []
            main_key = None
            
            for key in keys:
                key = key.strip().lower()
                if key in ["ctrl", "control"]:
                    modifiers.append(keyboard.Key.ctrl)
                elif key in ["alt"]:
                    modifiers.append(keyboard.Key.alt)
                elif key in ["shift"]:
                    modifiers.append(keyboard.Key.shift)
                elif key in ["super", "meta"]:
                    modifiers.append(keyboard.Key.cmd)
                else:
                    main_key = key
            
            # Press modifiers
            for mod in modifiers:
                self.keyboard_controller.press(mod)
            
            # Press main key
            if main_key:
                try:
                    # Try to get key from pynput
                    key_obj = getattr(keyboard.Key, main_key)
                except AttributeError:
                    # Fall back to character
                    key_obj = main_key
                
                self.keyboard_controller.press(key_obj)
                time.sleep(0.05)
                self.keyboard_controller.release(key_obj)
            
            # Release modifiers
            for mod in reversed(modifiers):
                self.keyboard_controller.release(mod)
            
            return True
        except Exception as e:
            print(f"Error executing key action: {e}")
            return False

    def _execute_command(self, command: str) -> bool:
        """Execute shell command."""
        try:
            subprocess.Popen(command, shell=True)
            return True
        except Exception as e:
            print(f"Error executing command: {e}")
            return False

    def _open_file(self, file_path: str) -> bool:
        """Open file."""
        try:
            file_path = Path(file_path).expanduser()
            if file_path.exists():
                subprocess.Popen(["xdg-open", str(file_path)])
                return True
            return False
        except Exception as e:
            print(f"Error opening file: {e}")
            return False

    def _open_folder(self, folder_path: str) -> bool:
        """Open folder."""
        try:
            folder_path = Path(folder_path).expanduser()
            if folder_path.exists():
                subprocess.Popen(["xdg-open", str(folder_path)])
                return True
            return False
        except Exception as e:
            print(f"Error opening folder: {e}")
            return False

    def _open_app(self, app_name: str) -> bool:
        """Open application."""
        try:
            subprocess.Popen(app_name.split())
            return True
        except Exception as e:
            print(f"Error opening app: {e}")
            return False

    def _execute_media_action(self, action: str) -> bool:
        """Execute media control action."""
        media_keys = {
            "play_pause": keyboard.Key.media_play_pause,
            "next": keyboard.Key.media_next,
            "previous": keyboard.Key.media_previous,
            "stop": keyboard.Key.media_stop,
        }
        
        if action in media_keys:
            try:
                key = media_keys[action]
                self.keyboard_controller.press(key)
                time.sleep(0.05)
                self.keyboard_controller.release(key)
                return True
            except Exception as e:
                print(f"Error executing media action: {e}")
                return False
        return False

    def _execute_volume_action(self, action: str) -> bool:
        """Execute volume control action."""
        volume_keys = {
            "mute": keyboard.Key.media_volume_mute,
            "increase": keyboard.Key.media_volume_up,
            "decrease": keyboard.Key.media_volume_down,
        }
        
        if action in volume_keys:
            try:
                key = volume_keys[action]
                self.keyboard_controller.press(key)
                time.sleep(0.05)
                self.keyboard_controller.release(key)
                return True
            except Exception as e:
                print(f"Error executing volume action: {e}")
                return False
        return False

    def execute_macro(self, macro_actions: List[Dict[str, Any]]) -> bool:
        """Execute a sequence of actions."""
        try:
            for action in macro_actions:
                action_type = action.get("type")
                action_value = action.get("value", "")
                delay = action.get("delay", 0)
                
                if delay > 0:
                    time.sleep(delay / 1000.0)
                
                if not self.execute_action(action_type, action_value):
                    return False
            
            return True
        except Exception as e:
            print(f"Error executing macro: {e}")
            return False
