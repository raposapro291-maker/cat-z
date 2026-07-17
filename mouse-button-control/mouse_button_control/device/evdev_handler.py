"""Direct evdev handler for Linux input devices."""

import os
import struct
from pathlib import Path
from typing import Optional, Dict, List
from threading import Thread


class EvdevHandler:
    """Handles Linux evdev input devices directly."""

    # Event types
    EV_KEY = 0x01
    EV_REL = 0x02
    EV_ABS = 0x03
    
    # Button codes
    BTN_LEFT = 0x110
    BTN_RIGHT = 0x111
    BTN_MIDDLE = 0x112
    BTN_SIDE = 0x113
    BTN_EXTRA = 0x114
    BTN_FORWARD = 0x115
    BTN_BACK = 0x116

    def __init__(self):
        """Initialize evdev handler."""
        self.devices = {}
        self.event_fd = {}
        self.threads = {}
        self.running = False

    def find_mice(self) -> List[Dict[str, str]]:
        """Find all mouse devices."""
        mice = []
        event_dir = Path("/dev/input")
        
        if not event_dir.exists():
            return mice
        
        for event_file in sorted(event_dir.glob("event*")):
            try:
                fd = os.open(str(event_file), os.O_RDONLY | os.O_NONBLOCK)
                
                # Try to get device name
                name = self._get_device_name(fd)
                if "mouse" in name.lower() or "trackpad" in name.lower():
                    mice.append({
                        "path": str(event_file),
                        "name": name,
                        "fd": fd
                    })
                else:
                    os.close(fd)
            except:
                pass
        
        return mice

    def _get_device_name(self, fd: int) -> str:
        """Get device name from file descriptor."""
        try:
            # EVIOCGNAME ioctl
            import fcntl
            EVIOCGNAME = 0x80FF4506
            name = fcntl.ioctl(fd, EVIOCGNAME, b"\0" * 256)
            return name.decode().rstrip("\0")
        except:
            return "Unknown"

    def start(self) -> None:
        """Start listening to devices."""
        self.running = True
        mice = self.find_mice()
        
        for mouse in mice:
            self.devices[mouse["path"]] = mouse
            thread = Thread(target=self._listen_device, args=(mouse["path"],))
            thread.daemon = True
            thread.start()
            self.threads[mouse["path"]] = thread

    def stop(self) -> None:
        """Stop listening to devices."""
        self.running = False
        for fd in self.event_fd.values():
            try:
                os.close(fd)
            except:
                pass

    def _listen_device(self, device_path: str) -> None:
        """Listen to a specific device."""
        try:
            fd = os.open(device_path, os.O_RDONLY | os.O_NONBLOCK)
            self.event_fd[device_path] = fd
            
            while self.running:
                try:
                    event_data = os.read(fd, 24)
                    if event_data:
                        self._parse_event(event_data, device_path)
                except BlockingIOError:
                    import time
                    time.sleep(0.01)
        except Exception as e:
            print(f"Error listening to {device_path}: {e}")

    def _parse_event(self, event_data: bytes, device_path: str) -> None:
        """Parse input event."""
        if len(event_data) < 24:
            return
        
        # Unpack event: sec, usec, type, code, value
        sec, usec, event_type, code, value = struct.unpack("=llHHI", event_data)
        
        if event_type == self.EV_KEY:
            self._handle_key_event(code, value, device_path)
        elif event_type == self.EV_REL:
            self._handle_rel_event(code, value, device_path)

    def _handle_key_event(self, code: int, value: int, device_path: str) -> None:
        """Handle key/button event."""
        button_names = {
            self.BTN_LEFT: "left",
            self.BTN_RIGHT: "right",
            self.BTN_MIDDLE: "middle",
            self.BTN_SIDE: "button_4",
            self.BTN_EXTRA: "button_5",
            self.BTN_FORWARD: "button_6",
            self.BTN_BACK: "button_7",
        }
        
        if code in button_names:
            event_type = "press" if value == 1 else "release"
            print(f"Device: {device_path}, Button: {button_names[code]}, Event: {event_type}")

    def _handle_rel_event(self, code: int, value: int, device_path: str) -> None:
        """Handle relative motion event."""
        if code == 0:  # X axis
            print(f"Device: {device_path}, X: {value}")
        elif code == 1:  # Y axis
            print(f"Device: {device_path}, Y: {value}")
