"""Device listener for mouse input."""

from pynput import mouse, keyboard
from typing import Callable, Optional, Dict
from threading import Thread, Event


class DeviceListener:
    """Listens to mouse and keyboard input."""

    def __init__(self):
        """Initialize device listener."""
        self.mouse_listener = None
        self.keyboard_listener = None
        self.mouse_callbacks = []
        self.keyboard_callbacks = []
        self.stop_event = Event()
        self.is_listening = False

    def register_mouse_callback(self, callback: Callable) -> None:
        """Register mouse callback."""
        self.mouse_callbacks.append(callback)

    def register_keyboard_callback(self, callback: Callable) -> None:
        """Register keyboard callback."""
        self.keyboard_callbacks.append(callback)

    def _on_move(self, x: int, y: int) -> None:
        """Handle mouse move."""
        for callback in self.mouse_callbacks:
            try:
                callback("move", {"x": x, "y": y})
            except Exception as e:
                print(f"Error in mouse move callback: {e}")

    def _on_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        """Handle mouse click."""
        button_name = str(button).lower().split(".")[1]
        event_type = "press" if pressed else "release"
        
        for callback in self.mouse_callbacks:
            try:
                callback(event_type, {"button": button_name, "x": x, "y": y})
            except Exception as e:
                print(f"Error in mouse click callback: {e}")

    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """Handle mouse scroll."""
        direction = "up" if dy > 0 else "down"
        
        for callback in self.mouse_callbacks:
            try:
                callback("scroll", {"direction": direction, "x": x, "y": y})
            except Exception as e:
                print(f"Error in mouse scroll callback: {e}")

    def _on_key_press(self, key: keyboard.Key) -> None:
        """Handle key press."""
        try:
            key_name = key.char if hasattr(key, "char") else str(key).split(".")[1]
        except:
            key_name = str(key)
        
        for callback in self.keyboard_callbacks:
            try:
                callback("press", {"key": key_name})
            except Exception as e:
                print(f"Error in keyboard press callback: {e}")

    def _on_key_release(self, key: keyboard.Key) -> None:
        """Handle key release."""
        try:
            key_name = key.char if hasattr(key, "char") else str(key).split(".")[1]
        except:
            key_name = str(key)
        
        for callback in self.keyboard_callbacks:
            try:
                callback("release", {"key": key_name})
            except Exception as e:
                print(f"Error in keyboard release callback: {e}")

    def start(self) -> None:
        """Start listening to input."""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.stop_event.clear()
        
        self.mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll,
        )
        self.mouse_listener.start()
        
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release,
        )
        self.keyboard_listener.start()

    def stop(self) -> None:
        """Stop listening to input."""
        if not self.is_listening:
            return
        
        self.is_listening = False
        self.stop_event.set()
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
