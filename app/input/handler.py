"""Input handling for keyboard and mouse."""

from typing import Callable, Dict, Optional
from loguru import logger
import pygame


class InputHandler:
    """Handles keyboard and mouse input."""

    def __init__(self):
        """Initialize input handler."""
        self.key_callbacks: Dict[int, Callable] = {}
        self.mouse_callbacks: Dict[str, Callable] = {}
        self.pressed_keys = set()
        self.mouse_pos = (0, 0)
        self.mouse_delta = (0, 0)
        self.last_mouse_pos = (0, 0)

    def register_key_callback(self, key: int, callback: Callable) -> None:
        """Register a callback for a key.
        
        Args:
            key: Pygame key constant
            callback: Function to call when key is pressed
        """
        self.key_callbacks[key] = callback
        logger.debug(f"Registered key callback for key {key}")

    def register_mouse_callback(self, event_type: str, callback: Callable) -> None:
        """Register a callback for mouse event.
        
        Args:
            event_type: Type of mouse event ('move', 'click', 'scroll')
            callback: Function to call on mouse event
        """
        self.mouse_callbacks[event_type] = callback
        logger.debug(f"Registered mouse callback for {event_type}")

    def handle_event(self, event: pygame.event.EventType) -> None:
        """Handle a pygame event.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
            if event.key in self.key_callbacks:
                self.key_callbacks[event.key]()
        
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)
        
        elif event.type == pygame.MOUSEMOTION:
            self.last_mouse_pos = self.mouse_pos
            self.mouse_pos = event.pos
            self.mouse_delta = (
                self.mouse_pos[0] - self.last_mouse_pos[0],
                self.mouse_pos[1] - self.last_mouse_pos[1]
            )
            if 'move' in self.mouse_callbacks:
                self.mouse_callbacks['move'](self.mouse_pos, self.mouse_delta)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 'click' in self.mouse_callbacks:
                self.mouse_callbacks['click'](event.button, self.mouse_pos)
        
        elif event.type == pygame.MOUSEWHEEL:
            if 'scroll' in self.mouse_callbacks:
                self.mouse_callbacks['scroll'](event.y)

    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed.
        
        Args:
            key: Pygame key constant
            
        Returns:
            True if key is pressed
        """
        return key in self.pressed_keys

    def get_mouse_pos(self) -> tuple:
        """Get current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return self.mouse_pos

    def get_mouse_delta(self) -> tuple:
        """Get mouse movement delta.
        
        Returns:
            Tuple of (dx, dy) movement
        """
        return self.mouse_delta
