"""Frame timing and FPS management."""

import time
from loguru import logger


class FrameTimer:
    """Manages frame timing and FPS calculation."""

    def __init__(self, target_fps: int = 60):
        """Initialize frame timer.
        
        Args:
            target_fps: Target frames per second
        """
        self.target_fps = target_fps
        self.target_frame_time = 1.0 / target_fps
        self.last_time = time.perf_counter()
        self.frame_count = 0
        self.fps = 0.0
        self.frame_times = []
        self.max_frame_history = 60
        self.low_fps_threshold = target_fps * 0.8
        self.performance_warnings = False

    def tick(self):
        """Update timer and return delta time.
        
        Returns:
            Delta time in seconds
        """
        current_time = time.perf_counter()
        dt = current_time - self.last_time
        self.last_time = current_time

        self.frame_count += 1
        self.frame_times.append(dt)

        if len(self.frame_times) > self.max_frame_history:
            self.frame_times.pop(0)

        if self.frame_count % 30 == 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0

            if self.fps < self.low_fps_threshold and self.performance_warnings:
                logger.warning(f"Low FPS detected: {self.fps:.1f} FPS")

        return min(dt, 0.1)

    def get_fps(self):
        """Get current FPS.
        
        Returns:
            Current frames per second
        """
        return self.fps

    def get_frame_time_ms(self):
        """Get current frame time in milliseconds.
        
        Returns:
            Frame time in milliseconds
        """
        return (1.0 / self.fps * 1000) if self.fps > 0 else 0
