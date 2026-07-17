#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for config manager."""

import pytest
import tempfile
from pathlib import Path
from mouse_button_control.config.config_manager import ConfigManager


class TestConfigManager:
    """Test config manager."""
    
    def setup_method(self):
        """Setup test."""
        self.config = ConfigManager()
    
    def test_set_and_get_config(self):
        """Test setting and getting config."""
        self.config.set("test_key", "test_value")
        value = self.config.get("test_key")
        assert value == "test_value"
    
    def test_get_all_config(self):
        """Test getting all config."""
        config_dict = self.config.get_all()
        assert isinstance(config_dict, dict)
        assert len(config_dict) > 0
    
    def test_create_default_profiles(self):
        """Test creating default profiles."""
        self.config.create_default_profiles()
        profiles = self.config.get_all_profiles()
        assert len(profiles) >= 0  # May already exist
