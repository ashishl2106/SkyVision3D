"""Planet rendering system."""

import asyncio
from typing import Optional, List, Any
from loguru import logger
import moderngl as mgl
import glm
import numpy as np

from app.config import Config
from app.renderer.shader_manager import ShaderManager
from app.renderer.texture_manager import TextureManager
from app.renderer.camera import Camera


class PlanetRenderer:
    """Renders planets in the scene."""

    def __init__(self, config: Config, shader_manager: ShaderManager, texture_manager: TextureManager):
        """Initialize planet renderer.
        
        Args:
            config: Application configuration
            shader_manager: Shader manager instance
            texture_manager: Texture manager instance
        """
        self.config = config
        self.shader_manager = shader_manager
        self.texture_manager = texture_manager
        self.planet_program: Optional[mgl.Program] = None
        self.planet_vaos: dict = {}
        self.planet_textures: dict = {}

    async def initialize(self) -> None:
        """Initialize planet rendering systems."""
        try:
            logger.info("Initializing planet renderer...")
            
            self.planet_program = self.shader_manager.load_shader(
                "planet",
                "planets/vertex.glsl",
                "planets/fragment.glsl"
            )
            
            logger.info("Planet renderer initialized")

        except Exception as e:
            logger.exception(f"Failed to initialize planet renderer: {e}")
            raise

    async def shutdown(self) -> None:
        """Shutdown planet renderer."""
        for vao in self.planet_vaos.values():
            if vao:
                vao.release()
        self.planet_vaos.clear()

    async def render(self, camera: Camera, planets: List[Any]) -> None:
        """Render planets.
        
        Args:
            camera: Camera instance
            planets: List of planet objects
        """
        if not self.planet_program or not planets:
            return

        try:
            self.planet_program.use()
            
            for planet in planets:
                await self._render_planet(planet, camera)

        except Exception as e:
            logger.exception(f"Error rendering planets: {e}")

    async def _render_planet(self, planet: Any, camera: Camera) -> None:
        """Render a single planet.
        
        Args:
            planet: Planet object
            camera: Camera instance
        """
        if not self.planet_program:
            return

        model = glm.translate(glm.mat4(1.0), planet.position)
        model = glm.scale(model, glm.vec3(planet.radius))
        
        self.planet_program['model'].write(glm.value_ptr(model))
        self.planet_program['view'].write(glm.value_ptr(camera.get_view_matrix()))
        self.planet_program['projection'].write(glm.value_ptr(camera.get_projection_matrix()))
        
        # Load texture if needed
        if planet.name not in self.planet_textures and planet.texture_path:
            self.planet_textures[planet.name] = self.texture_manager.load_texture(
                planet.name,
                planet.texture_path,
                srgb=True
            )
        
        if planet.name in self.planet_textures:
            texture = self.planet_textures[planet.name]
            if texture:
                texture.use(0)
                self.planet_program['planet_texture'] = 0
        
        # Render planet geometry
        if planet.name in self.planet_vaos:
            vao = self.planet_vaos[planet.name]
            if vao:
                vao.render()
