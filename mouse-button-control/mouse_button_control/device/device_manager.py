"""Device manager for mouse detection and handling."""

import os
from typing import Dict, List, Optional, Callable
from pynput import mouse
from pathlib import Path


class DeviceManager:
    """Manages input devices (mice)."""

    def __init__(self):
        """Initialize device manager."""
        self.devices = {}
        self.listeners = {}
        self.callbacks = []
        self.scan_devices()

    def scan_devices(self) -> List[Dict[str, str]]:
        """Scan for connected devices."""
        devices = []
        
        try:
            # Check /proc/bus/input/devices for mouse devices
            if Path("/proc/bus/input/devices").exists():
                with open("/proc/bus/input/devices", "r") as f:
                    content = f.read()
                    
                lines = content.split("\n")
                current_device = {}
                
                for line in lines:
                    if line.startswith("I:"):
                        if current_device:
                            devices.append(current_device)
                        current_device = {}
                    
                    if line.startswith("N:"):
                        current_device["name"] = line.split('"')[1]
                    elif line.startswith("P:"):
                        current_device["phys"] = line.split("=")[1].strip()
                    elif line.startswith("H:"):
                        handlers = line.split("=")[1].strip().split()
                        if any("mouse" in h or "event" in h for h in handlers):
                            current_device["is_mouse"] = True
                
                if current_device and current_device.get("is_mouse"):
                    devices.append(current_device)
        except Exception as e:
            print(f"Error scanning devices: {e}")
        
        self.devices = {device["name"]: device for device in devices}
        return devices

    def get_devices(self) -> Dict[str, Dict[str, str]]:
        """Get all connected devices."""
        return self.devices

    def get_device(self, device_name: str) -> Optional[Dict[str, str]]:
        """Get device by name."""
        return self.devices.get(device_name)

    def register_callback(self, callback: Callable) -> None:
        """Register callback for device events."""
        self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable) -> None:
        """Unregister callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def _notify_callbacks(self, event_type: str, device_name: str = "", data: Dict = None) -> None:
        """Notify all registered callbacks."""
        if data is None:
            data = {}
        
        for callback in self.callbacks:
            try:
                callback(event_type, device_name, data)
            except Exception as e:
                print(f"Error in callback: {e}")

    def start_monitoring(self) -> None:
        """Start monitoring devices."""
        self._notify_callbacks("monitoring_started")

    def stop_monitoring(self) -> None:
        """Stop monitoring devices."""
        self._notify_callbacks("monitoring_stopped")
