#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for macro engine."""

import pytest
from mouse_button_control.macro.macro_engine import MacroEngine


class TestMacroEngine:
    """Test macro engine."""
    
    def setup_method(self):
        """Setup test."""
        self.engine = MacroEngine()
    
    def test_add_macro(self):
        """Test adding macro."""
        actions = [
            {"type": "key", "value": "a", "delay": 0},
            {"type": "key", "value": "b", "delay": 100},
        ]
        result = self.engine.add_macro("test_macro", actions)
        assert result is True
    
    def test_get_macro(self):
        """Test getting macro."""
        actions = [{"type": "key", "value": "a", "delay": 0}]
        self.engine.add_macro("test_macro", actions)
        
        retrieved = self.engine.get_macro("test_macro")
        assert retrieved == actions
    
    def test_delete_macro(self):
        """Test deleting macro."""
        actions = [{"type": "key", "value": "a", "delay": 0}]
        self.engine.add_macro("test_macro", actions)
        
        result = self.engine.delete_macro("test_macro")
        assert result is True
        assert self.engine.get_macro("test_macro") is None
    
    def test_record_macro(self):
        """Test recording macro."""
        self.engine.record_start()
        self.engine.record_action("key", "a")
        self.engine.record_action("key", "b")
        actions = self.engine.record_stop()
        
        assert len(actions) == 2
        assert actions[0]["value"] == "a"
        assert actions[1]["value"] == "b"
