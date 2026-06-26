"""Earth rendering with terrain and atmosphere."""

import asyncio
from typing import Optional
from loguru import logger
import moderngl as mgl
import glm
import numpy as np

from app.config import Config
from app.renderer.shader_manager import ShaderManager
from app.renderer.texture_manager import TextureManager
from app.renderer.camera import Camera


class EarthRenderer:
    """Renders the Earth with terrain and atmosphere effects."""

    def __init__(self, config: Config, shader_manager: ShaderManager, texture_manager: TextureManager):
        """Initialize Earth renderer.
        
        Args:
            config: Application configuration
            shader_manager: Shader manager instance
            texture_manager: Texture manager instance
        """
        self.config = config
        self.shader_manager = shader_manager
        self.texture_manager = texture_manager
        self.earth_program: Optional[mgl.Program] = None
        self.atmosphere_program: Optional[mgl.Program] = None
        self.earth_vao: Optional[mgl.VertexArray] = None
        self.atmosphere_vao: Optional[mgl.VertexArray] = None
        self.earth_model = glm.mat4(1.0)
        self.earth_texture: Optional[mgl.Texture] = None
        self.normal_texture: Optional[mgl.Texture] = None
        self.night_texture: Optional[mgl.Texture] = None

    async def initialize(self) -> None:
        """Initialize Earth rendering systems."""
        try:
            logger.info("Initializing Earth renderer...")
            
            self.earth_program = self.shader_manager.load_shader(
                "earth",
                "earth/vertex.glsl",
                "earth/fragment.glsl"
            )
            
            self.atmosphere_program = self.shader_manager.load_shader(
                "atmosphere",
                "atmosphere/vertex.glsl",
                "atmosphere/fragment.glsl"
            )
            
            self.earth_texture = self.texture_manager.load_texture(
                "earth_diffuse",
                "earth/earth_diffuse.jpg",
                srgb=True
            )
            
            self.normal_texture = self.texture_manager.load_texture(
                "earth_normal",
                "earth/earth_normal.jpg"
            )
            
            self.night_texture = self.texture_manager.load_texture(
                "earth_night",
                "earth/earth_night.jpg",
                srgb=True
            )
            
            logger.info("Earth renderer initialized")

        except Exception as e:
            logger.exception(f"Failed to initialize Earth renderer: {e}")
            raise

    async def shutdown(self) -> None:
        """Shutdown Earth renderer."""
        if self.earth_vao:
            self.earth_vao.release()
        if self.atmosphere_vao:
            self.atmosphere_vao.release()

    async def render(self, camera: Camera) -> None:
        """Render the Earth.
        
        Args:
            camera: Camera instance
        """
        if not self.earth_program or not self.earth_texture:
            return

        try:
            self.earth_program.use()
            
            self.earth_program['model'].write(glm.value_ptr(self.earth_model))
            self.earth_program['view'].write(glm.value_ptr(camera.get_view_matrix()))
            self.earth_program['projection'].write(glm.value_ptr(camera.get_projection_matrix()))
            
            self.earth_texture.use(0)
            self.earth_program['earth_texture'] = 0
            
            if self.normal_texture:
                self.normal_texture.use(1)
                self.earth_program['normal_texture'] = 1
            
            if self.night_texture:
                self.night_texture.use(2)
                self.earth_program['night_texture'] = 2
            
            if self.earth_vao:
                self.earth_vao.render()
            
            if self.config.earth.atmosphere_enabled and self.atmosphere_program:
                await self._render_atmosphere(camera)

        except Exception as e:
            logger.exception(f"Error rendering Earth: {e}")

    async def _render_atmosphere(self, camera: Camera) -> None:
        """Render atmosphere effect.
        
        Args:
            camera: Camera instance
        """
        if not self.atmosphere_program:
            return

        self.atmosphere_program.use()
        
        atmosphere_model = glm.scale(self.earth_model, glm.vec3(1.05))
        self.atmosphere_program['model'].write(glm.value_ptr(atmosphere_model))
        self.atmosphere_program['view'].write(glm.value_ptr(camera.get_view_matrix()))
        self.atmosphere_program['projection'].write(glm.value_ptr(camera.get_projection_matrix()))
        
        if self.atmosphere_vao:
            self.atmosphere_vao.render()
