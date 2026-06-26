"""Input handling for keyboard, mouse, and touch."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable, Dict, List

from app.config import Config


class InputType(Enum):
    """Input event types."""
    KEY_DOWN = 1
    KEY_UP = 2
    MOUSE_MOVE = 3
    MOUSE_DOWN = 4
    MOUSE_UP = 5
    SCROLL = 6
    TOUCH_DOWN = 7
    TOUCH_UP = 8
    TOUCH_MOVE = 9


@dataclass
class MouseState:
    """Current mouse state."""
    x: float = 0.0
    y: float = 0.0
    left_pressed: bool = False
    right_pressed: bool = False
    middle_pressed: bool = False
    scroll_delta: float = 0.0


@dataclass
class TouchPoint:
    """Single touch point."""
    id: int
    x: float
    y: float
    pressure: float = 1.0


@dataclass
class KeyboardState:
    """Current keyboard state."""
    pressed_keys: set = field(default_factory=set)


class InputHandler:
    """Handles all input events."""

    def __init__(self, config: Config):
        """Initialize input handler.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.mouse = MouseState()
        self.keyboard = KeyboardState()
        self.touch_points: Dict[int, TouchPoint] = {}
        self.should_quit = False
        self.callbacks: Dict[InputType, List[Callable]] = {}
        self.camera_target_distance = config.camera.initial_distance
        self.camera_rotation = (0.0, 0.0)
        self.camera_pan = (0.0, 0.0)

    def register_callback(self, event_type: InputType, callback: Callable) -> None:
        """Register callback for input event.
        
        Args:
            event_type: Type of input event
            callback: Callback function
        """
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append(callback)

    def on_mouse_move(self, x: float, y: float) -> None:
        """Handle mouse movement.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        if self.mouse.left_pressed:
            delta_x = x - self.mouse.x
            delta_y = y - self.mouse.y
            self.camera_rotation = (
                self.camera_rotation[0] + delta_y * self.config.camera.orbit_sensitivity * 0.01,
                self.camera_rotation[1] + delta_x * self.config.camera.orbit_sensitivity * 0.01,
            )
        elif self.mouse.right_pressed:
            delta_x = x - self.mouse.x
            delta_y = y - self.mouse.y
            self.camera_pan = (
                self.camera_pan[0] + delta_x * self.config.camera.pan_sensitivity,
                self.camera_pan[1] + delta_y * self.config.camera.pan_sensitivity,
            )

        self.mouse.x = x
        self.mouse.y = y

    def on_mouse_down(self, button: int) -> None:
        """Handle mouse button press.
        
        Args:
            button: Mouse button (0=left, 1=middle, 2=right)
        """
        if button == 0:
            self.mouse.left_pressed = True
        elif button == 1:
            self.mouse.middle_pressed = True
        elif button == 2:
            self.mouse.right_pressed = True

    def on_mouse_up(self, button: int) -> None:
        """Handle mouse button release.
        
        Args:
            button: Mouse button (0=left, 1=middle, 2=right)
        """
        if button == 0:
            self.mouse.left_pressed = False
        elif button == 1:
            self.mouse.middle_pressed = False
        elif button == 2:
            self.mouse.right_pressed = False

    def on_scroll(self, delta: float) -> None:
        """Handle mouse scroll.
        
        Args:
            delta: Scroll delta
        """
        self.camera_target_distance *= (1.0 - delta * self.config.camera.zoom_sensitivity * 0.1)
        self.camera_target_distance = max(
            self.config.camera.min_distance,
            min(self.config.camera.max_distance, self.camera_target_distance)
        )

    def on_key_down(self, key: str) -> None:
        """Handle key press.
        
        Args:
            key: Key name
        """
        self.keyboard.pressed_keys.add(key.lower())

        if key.lower() == "escape":
            self.should_quit = True
        elif key.lower() == "f":
            pass
        elif key.lower() == "p":
            pass
        elif key.lower() == "m":
            self.config.museum_mode.enabled = not self.config.museum_mode.enabled
        elif key.lower() == "s":
            pass

    def on_key_up(self, key: str) -> None:
        """Handle key release.
        
        Args:
            key: Key name
        """
        self.keyboard.pressed_keys.discard(key.lower())

    def on_touch_down(self, touch_id: int, x: float, y: float) -> None:
        """Handle touch start.
        
        Args:
            touch_id: Touch point ID
            x: X coordinate
            y: Y coordinate
        """
        self.touch_points[touch_id] = TouchPoint(touch_id, x, y)

    def on_touch_up(self, touch_id: int) -> None:
        """Handle touch end.
        
        Args:
            touch_id: Touch point ID
        """
        if touch_id in self.touch_points:
            del self.touch_points[touch_id]

    def on_touch_move(self, touch_id: int, x: float, y: float) -> None:
        """Handle touch move.
        
        Args:
            touch_id: Touch point ID
            x: X coordinate
            y: Y coordinate
        """
        if touch_id in self.touch_points:
            self.touch_points[touch_id].x = x
            self.touch_points[touch_id].y = y

    def is_key_pressed(self, key: str) -> bool:
        """Check if key is currently pressed.
        
        Args:
            key: Key name
            
        Returns:
            True if key is pressed
        """
        return key.lower() in self.keyboard.pressed_keys

    def update(self, dt: float) -> None:
        """Update input state.
        
        Args:
            dt: Delta time in seconds
        """
        self.mouse.scroll_delta = 0.0

        for event_type, callbacks in self.callbacks.items():
            for callback in callbacks:
                callback()
