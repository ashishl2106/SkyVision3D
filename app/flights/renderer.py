"""Flight path and aircraft rendering."""

import asyncio
from typing import Optional, List, Any
from loguru import logger
import moderngl as mgl
import glm
import numpy as np

from app.config import Config
from app.renderer.shader_manager import ShaderManager
from app.renderer.mesh_manager import MeshManager
from app.renderer.camera import Camera


class FlightRenderer:
    """Renders flight paths and aircraft."""

    def __init__(self, config: Config, shader_manager: ShaderManager, mesh_manager: MeshManager):
        """Initialize flight renderer.
        
        Args:
            config: Application configuration
            shader_manager: Shader manager instance
            mesh_manager: Mesh manager instance
        """
        self.config = config
        self.shader_manager = shader_manager
        self.mesh_manager = mesh_manager
        self.flight_program: Optional[mgl.Program] = None
        self.path_program: Optional[mgl.Program] = None
        self.aircraft_vao: Optional[mgl.VertexArray] = None
        self.path_vao: Optional[mgl.VertexArray] = None

    async def initialize(self) -> None:
        """Initialize flight rendering systems."""
        try:
            logger.info("Initializing flight renderer...")
            
            self.flight_program = self.shader_manager.load_shader(
                "flight",
                "flights/vertex.glsl",
                "flights/fragment.glsl"
            )
            
            self.path_program = self.shader_manager.load_shader(
                "flight_path",
                "flights/path_vertex.glsl",
                "flights/path_fragment.glsl"
            )
            
            logger.info("Flight renderer initialized")

        except Exception as e:
            logger.exception(f"Failed to initialize flight renderer: {e}")
            raise

    async def shutdown(self) -> None:
        """Shutdown flight renderer."""
        if self.aircraft_vao:
            self.aircraft_vao.release()
        if self.path_vao:
            self.path_vao.release()

    async def render(self, camera: Camera, flights: List[Any]) -> None:
        """Render flights.
        
        Args:
            camera: Camera instance
            flights: List of flight objects
        """
        if not flights:
            return

        try:
            for flight in flights:
                await self._render_flight_path(flight, camera)
                await self._render_aircraft(flight, camera)

        except Exception as e:
            logger.exception(f"Error rendering flights: {e}")

    async def _render_flight_path(self, flight: Any, camera: Camera) -> None:
        """Render flight path.
        
        Args:
            flight: Flight object
            camera: Camera instance
        """
        if not self.path_program or not hasattr(flight, 'path_points') or not flight.path_points:
            return

        self.path_program.use()
        
        self.path_program['view'].write(glm.value_ptr(camera.get_view_matrix()))
        self.path_program['projection'].write(glm.value_ptr(camera.get_projection_matrix()))
        self.path_program['color'].write(glm.value_ptr(flight.path_color if hasattr(flight, 'path_color') else glm.vec4(1, 1, 1, 1)))
        
        # Create line geometry from path points
        path_vertices = np.array(flight.path_points, dtype=np.float32)
        
        if self.path_vao:
            self.path_vao.render(mgl.LINE_STRIP)

    async def _render_aircraft(self, flight: Any, camera: Camera) -> None:
        """Render aircraft.
        
        Args:
            flight: Flight object
            camera: Camera instance
        """
        if not self.flight_program:
            return

        self.flight_program.use()
        
        # Create model matrix for aircraft
        model = glm.translate(glm.mat4(1.0), flight.position)
        
        # Rotate to match flight direction
        if hasattr(flight, 'direction'):
            direction = glm.normalize(flight.direction)
            # Calculate rotation based on direction
            up = glm.vec3(0, 1, 0)
            if abs(glm.dot(direction, up)) < 0.99:
                right = glm.normalize(glm.cross(direction, up))
                new_up = glm.cross(right, direction)
        
        model = glm.scale(model, glm.vec3(flight.scale if hasattr(flight, 'scale') else 1.0))
        
        self.flight_program['model'].write(glm.value_ptr(model))
        self.flight_program['view'].write(glm.value_ptr(camera.get_view_matrix()))
        self.flight_program['projection'].write(glm.value_ptr(camera.get_projection_matrix()))
        self.flight_program['color'].write(glm.value_ptr(flight.color if hasattr(flight, 'color') else glm.vec4(1, 1, 1, 1)))
        
        if self.aircraft_vao:
            self.aircraft_vao.render()
