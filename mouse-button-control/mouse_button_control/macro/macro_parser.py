"""Macro parser for parsing macro definitions."""

from typing import Dict, List, Any, Optional
import json


class MacroParser:
    """Parses macro definitions."""

    @staticmethod
    def parse_macro(macro_def: str) -> Optional[List[Dict[str, Any]]]:
        """Parse macro definition string."""
        try:
            # Try to parse as JSON first
            return json.loads(macro_def)
        except json.JSONDecodeError:
            # Try to parse as simple format: action1(value1) -> action2(value2)
            return MacroParser._parse_simple_format(macro_def)

    @staticmethod
    def _parse_simple_format(macro_def: str) -> Optional[List[Dict[str, Any]]]:
        """Parse simple macro format."""
        try:
            actions = []
            parts = macro_def.split("->")
            
            for part in parts:
                part = part.strip()
                if "(" in part and ")" in part:
                    action_type = part[:part.index("(")].strip()
                    action_value = part[part.index("(") + 1:part.index(")")].strip()
                    actions.append({
                        "type": action_type,
                        "value": action_value,
                        "delay": 0,
                    })
            
            return actions if actions else None
        except Exception as e:
            print(f"Error parsing macro: {e}")
            return None

    @staticmethod
    def serialize_macro(actions: List[Dict[str, Any]]) -> str:
        """Serialize macro to JSON string."""
        return json.dumps(actions, indent=2)
