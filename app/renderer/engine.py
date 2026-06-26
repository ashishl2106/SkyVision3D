"""OpenGL rendering engine."""

import asyncio
from typing import Optional, List, Any
from loguru import logger
import moderngl as mgl
import numpy as np

from app.config import Config
from app.renderer.shader_manager import ShaderManager
from app.renderer.texture_manager import TextureManager
from app.renderer.mesh_manager import MeshManager
from app.renderer.camera import Camera
from app.earth.renderer import EarthRenderer
from app.planets.renderer import PlanetRenderer
from app.flights.renderer import FlightRenderer
from app.capture.renderer import CaptureRenderer


class RenderEngine:
    """Main rendering engine using ModernGL."""

    def __init__(self, config: Config):
        """Initialize the render engine.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.ctx: Optional[mgl.Context] = None
        self.shader_manager: Optional[ShaderManager] = None
        self.texture_manager: Optional[TextureManager] = None
        self.mesh_manager: Optional[MeshManager] = None
        self.camera: Optional[Camera] = None
        self.earth_renderer: Optional[EarthRenderer] = None
        self.planet_renderer: Optional[PlanetRenderer] = None
        self.flight_renderer: Optional[FlightRenderer] = None
        self.capture_renderer: Optional[CaptureRenderer] = None
        self.framebuffer: Optional[mgl.Framebuffer] = None
        self.frame_count = 0

    async def initialize(self) -> None:
        """Initialize rendering systems."""
        try:
            logger.info("Initializing render engine...")
            
            self.ctx = mgl.create_context()
            self.ctx.enable(mgl.DEPTH_TEST)
            self.ctx.enable(mgl.CULL_FACE)
            
            if self.config.display.msaa_samples > 1:
                self.ctx.enable(mgl.MULTISAMPLE)
            
            self.shader_manager = ShaderManager(self.ctx)
            self.texture_manager = TextureManager(self.config)
            self.mesh_manager = MeshManager()
            
            self.camera = Camera(self.config)
            
            self.earth_renderer = EarthRenderer(self.config, self.shader_manager, self.texture_manager)
            await self.earth_renderer.initialize()
            
            self.planet_renderer = PlanetRenderer(self.config, self.shader_manager, self.texture_manager)
            await self.planet_renderer.initialize()
            
            self.flight_renderer = FlightRenderer(self.config, self.shader_manager, self.mesh_manager)
            await self.flight_renderer.initialize()
            
            self.capture_renderer = CaptureRenderer(self.config, self.shader_manager)
            await self.capture_renderer.initialize()
            
            logger.info(f"Render engine initialized: {self.ctx.info['GL_RENDERER']}")

        except Exception as e:
            logger.exception(f"Failed to initialize render engine: {e}")
            raise

    async def shutdown(self) -> None:
        """Shutdown rendering systems."""
        logger.info("Shutting down render engine...")
        
        if self.earth_renderer:
            await self.earth_renderer.shutdown()
        if self.planet_renderer:
            await self.planet_renderer.shutdown()
        if self.flight_renderer:
            await self.flight_renderer.shutdown()
        if self.capture_renderer:
            await self.capture_renderer.shutdown()

    async def render(self, flights: List[Any] = None, planets: List[Any] = None, capture_frame: Optional[np.ndarray] = None) -> None:
        """Render a frame.
        
        Args:
            flights: List of flight objects
            planets: List of planet objects
            capture_frame: Video capture frame
        """
        if not self.ctx:
            return
        
        try:
            width = self.config.display.resolution.width
            height = self.config.display.resolution.height
            
            self.ctx.clear(0.0, 0.0, 0.0, 1.0)
            self.ctx.viewport = (0, 0, width, height)
            
            if self.earth_renderer:
                await self.earth_renderer.render(self.camera)
            
            if self.planet_renderer and planets:
                await self.planet_renderer.render(self.camera, planets)
            
            if self.flight_renderer and flights:
                await self.flight_renderer.render(self.camera, flights)
            
            if self.capture_renderer and capture_frame is not None:
                await self.capture_renderer.render(capture_frame)
            
            self.frame_count += 1

        except Exception as e:
            logger.exception(f"Render error: {e}")
