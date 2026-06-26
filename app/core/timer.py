"""Frame timing and FPS management."""

from loguru import logger
import time


class FrameTimer:
    """Manages frame timing and FPS."""

    def __init__(self, target_fps: int = 60):
        """Initialize frame timer.
        
        Args:
            target_fps: Target frames per second
        """
        self.target_fps = target_fps
        self.target_frame_time = 1.0 / target_fps
        self.frame_count = 0
        self.fps = 0.0
        self.delta_time = 0.0
        self.last_time = time.time()
        self.last_fps_update = time.time()
        self.frame_times = []
        self.max_frame_history = 100

    def tick(self) -> None:
        """Update frame timing."""
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_count += 1
        self.frame_times.append(self.delta_time)
        
        if len(self.frame_times) > self.max_frame_history:
            self.frame_times.pop(0)
        
        # Update FPS every second
        if current_time - self.last_fps_update >= 1.0:
            self.fps = self.frame_count / (current_time - self.last_fps_update)
            self.frame_count = 0
            self.last_fps_update = current_time
            logger.debug(f"FPS: {self.fps:.2f}")

    def get_delta_time(self) -> float:
        """Get delta time since last frame.
        
        Returns:
            Delta time in seconds
        """
        return self.delta_time

    def get_fps(self) -> float:
        """Get current FPS.
        
        Returns:
            Current frames per second
        """
        return self.fps

    def get_average_frame_time(self) -> float:
        """Get average frame time.
        
        Returns:
            Average frame time in seconds
        """
        if not self.frame_times:
            return 0.0
        return sum(self.frame_times) / len(self.frame_times)

    def should_sleep(self) -> bool:
        """Check if frame should sleep for frame rate limiting.
        
        Returns:
            True if should sleep
        """
        elapsed = time.time() - self.last_time
        return elapsed < self.target_frame_time

    def sleep_remaining_frame_time(self) -> None:
        """Sleep for remaining frame time."""
        elapsed = time.time() - self.last_time
        remaining = self.target_frame_time - elapsed
        if remaining > 0:
            time.sleep(remaining)
