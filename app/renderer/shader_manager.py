"""Shader management and compilation."""

from pathlib import Path
from typing import Dict, Optional
from loguru import logger
import moderngl as mgl


class ShaderManager:
    """Manages shader compilation and caching."""

    def __init__(self, ctx: mgl.Context):
        """Initialize shader manager.
        
        Args:
            ctx: ModernGL context
        """
        self.ctx = ctx
        self.programs: Dict[str, mgl.Program] = {}
        self.shader_dir = Path("assets/shaders")

    def load_shader(self, name: str, vertex_path: str, fragment_path: str) -> mgl.Program:
        """Load and compile a shader program.
        
        Args:
            name: Shader program name
            vertex_path: Path to vertex shader
            fragment_path: Path to fragment shader
            
        Returns:
            Compiled shader program
        """
        if name in self.programs:
            return self.programs[name]

        try:
            vertex_src = self._read_shader_file(vertex_path)
            fragment_src = self._read_shader_file(fragment_path)
            
            program = self.ctx.program(
                vertex_shader=vertex_src,
                fragment_shader=fragment_src
            )
            
            self.programs[name] = program
            logger.info(f"Loaded shader: {name}")
            return program

        except Exception as e:
            logger.exception(f"Failed to load shader {name}: {e}")
            raise

    def load_shader_with_geometry(self, name: str, vertex_path: str, geometry_path: str, fragment_path: str) -> mgl.Program:
        """Load and compile a shader program with geometry shader.
        
        Args:
            name: Shader program name
            vertex_path: Path to vertex shader
            geometry_path: Path to geometry shader
            fragment_path: Path to fragment shader
            
        Returns:
            Compiled shader program
        """
        if name in self.programs:
            return self.programs[name]

        try:
            vertex_src = self._read_shader_file(vertex_path)
            geometry_src = self._read_shader_file(geometry_path)
            fragment_src = self._read_shader_file(fragment_path)
            
            program = self.ctx.program(
                vertex_shader=vertex_src,
                geometry_shader=geometry_src,
                fragment_shader=fragment_src
            )
            
            self.programs[name] = program
            logger.info(f"Loaded shader: {name}")
            return program

        except Exception as e:
            logger.exception(f"Failed to load shader {name}: {e}")
            raise

    def get_program(self, name: str) -> Optional[mgl.Program]:
        """Get a loaded shader program.
        
        Args:
            name: Shader program name
            
        Returns:
            Shader program or None
        """
        return self.programs.get(name)

    def _read_shader_file(self, path: str) -> str:
        """Read shader source from file.
        
        Args:
            path: Path to shader file
            
        Returns:
            Shader source code
        """
        file_path = self.shader_dir / path
        
        if not file_path.exists():
            logger.warning(f"Shader file not found: {file_path}")
            return ""
        
        with open(file_path, 'r') as f:
            return f.read()

    def release_all(self) -> None:
        """Release all shader programs."""
        for program in self.programs.values():
            program.release()
        self.programs.clear()
        logger.info("Released all shaders")
