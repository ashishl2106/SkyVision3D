"""Main application class managing the overall lifecycle."""

import asyncio
import time
from typing import Optional
from loguru import logger

from app.config import Config
from app.renderer.engine import RenderEngine
from app.core.input_handler import InputHandler
from app.core.timer import FrameTimer
from app.flights.manager import FlightManager
from app.planets.manager import PlanetManager
from app.capture.camera import CameraCapture


class Application:
    """Main application managing rendering and game loop."""

    def __init__(self, config: Config):
        """Initialize the application."""
        self.config = config
        self.render_engine: Optional[RenderEngine] = None
        self.input_handler: Optional[InputHandler] = None
        self.frame_timer = FrameTimer(config.display.target_fps)
        self.flight_manager: Optional[FlightManager] = None
        self.planet_manager: Optional[PlanetManager] = None
        self.camera_capture: Optional[CameraCapture] = None
        self.running = False

    async def initialize(self) -> bool:
        """Initialize all application systems."""
        try:
            logger.info("Initializing application systems...")

            self.render_engine = RenderEngine(self.config)
            await self.render_engine.initialize()

            self.input_handler = InputHandler(self.config)
            self.flight_manager = FlightManager(self.config)
            self.planet_manager = PlanetManager(self.config)

            if self.config.video_capture.enabled:
                self.camera_capture = CameraCapture(self.config)
                await self.camera_capture.initialize()

            logger.info("Application initialization complete")
            return True

        except Exception as e:
            logger.exception(f"Failed to initialize application: {e}")
            return False

    async def shutdown(self) -> None:
        """Shutdown all application systems."""
        logger.info("Shutting down application...")

        if self.camera_capture:
            await self.camera_capture.shutdown()

        if self.render_engine:
            await self.render_engine.shutdown()

        logger.info("Application shutdown complete")

    async def update(self, dt: float) -> None:
        """Update application state."""
        if self.input_handler:
            self.input_handler.update(dt)

        if self.flight_manager:
            await self.flight_manager.update(dt)

        if self.planet_manager:
            await self.planet_manager.update(dt)

        if self.camera_capture:
            await self.camera_capture.update(dt)

    async def render(self) -> None:
        """Render current frame."""
        if self.render_engine:
            capture_frame = None
            if self.camera_capture:
                capture_frame = self.camera_capture.get_current_frame()

            await self.render_engine.render(
                flights=self.flight_manager.get_flights() if self.flight_manager else [],
                planets=self.planet_manager.get_planets() if self.planet_manager else [],
                capture_frame=capture_frame,
            )

    async def run(self) -> None:
        """Main application loop."""
        if not await self.initialize():
            return

        self.running = True
        logger.info("Starting main application loop")

        try:
            while self.running:
                dt = self.frame_timer.tick()
                await self.update(dt)
                await self.render()

                if self.input_handler and self.input_handler.should_quit:
                    self.running = False

                await asyncio.sleep(0.001)

        except Exception as e:
            logger.exception(f"Error in main loop: {e}")
        finally:
            await self.shutdown()
