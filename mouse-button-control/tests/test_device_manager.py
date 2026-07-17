#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for device manager."""

import pytest
from mouse_button_control.device.device_manager import DeviceManager


class TestDeviceManager:
    """Test device manager."""
    
    def setup_method(self):
        """Setup test."""
        self.device_manager = DeviceManager()
    
    def test_scan_devices(self):
        """Test device scanning."""
        devices = self.device_manager.scan_devices()
        assert isinstance(devices, list)
    
    def test_get_devices(self):
        """Test getting devices."""
        devices = self.device_manager.get_devices()
        assert isinstance(devices, dict)
    
    def test_register_callback(self):
        """Test callback registration."""
        def callback(event_type, device_name, data):
            pass
        
        self.device_manager.register_callback(callback)
        assert callback in self.device_manager.callbacks
    
    def test_unregister_callback(self):
        """Test callback unregistration."""
        def callback(event_type, device_name, data):
            pass
        
        self.device_manager.register_callback(callback)
        self.device_manager.unregister_callback(callback)
        assert callback not in self.device_manager.callbacks
