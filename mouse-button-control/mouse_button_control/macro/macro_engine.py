"""Macro engine for recording and executing macros."""

import time
from typing import Dict, List, Any, Optional, Callable
from .action_executor import ActionExecutor


class MacroEngine:
    """Engine for macro management and execution."""

    def __init__(self):
        """Initialize macro engine."""
        self.macros = {}
        self.executor = ActionExecutor()
        self.recording = False
        self.recorded_actions = []
        self.last_action_time = 0

    def record_start(self) -> None:
        """Start recording a macro."""
        self.recording = True
        self.recorded_actions = []
        self.last_action_time = time.time()

    def record_stop(self) -> List[Dict[str, Any]]:
        """Stop recording and return recorded actions."""
        self.recording = False
        return self.recorded_actions

    def record_action(self, action_type: str, action_value: str = "") -> None:
        """Record an action."""
        if not self.recording:
            return
        
        current_time = time.time()
        delay = int((current_time - self.last_action_time) * 1000)
        
        action = {
            "type": action_type,
            "value": action_value,
            "delay": max(0, delay),
        }
        
        self.recorded_actions.append(action)
        self.last_action_time = current_time

    def add_macro(self, macro_name: str, actions: List[Dict[str, Any]]) -> bool:
        """Add or update a macro."""
        try:
            self.macros[macro_name] = actions
            return True
        except Exception as e:
            print(f"Error adding macro: {e}")
            return False

    def get_macro(self, macro_name: str) -> Optional[List[Dict[str, Any]]]:
        """Get macro by name."""
        return self.macros.get(macro_name)

    def execute_macro(self, macro_name: str) -> bool:
        """Execute a macro."""
        macro = self.get_macro(macro_name)
        if macro:
            return self.executor.execute_macro(macro)
        return False

    def execute_macro_sequence(self, macro_name: str, repeat: int = 1) -> bool:
        """Execute macro multiple times."""
        try:
            for _ in range(repeat):
                if not self.execute_macro(macro_name):
                    return False
            return True
        except Exception as e:
            print(f"Error executing macro sequence: {e}")
            return False

    def delete_macro(self, macro_name: str) -> bool:
        """Delete a macro."""
        try:
            if macro_name in self.macros:
                del self.macros[macro_name]
                return True
            return False
        except Exception as e:
            print(f"Error deleting macro: {e}")
            return False

    def get_all_macros(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all macros."""
        return self.macros.copy()
