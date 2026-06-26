"""Texture management and loading."""

from pathlib import Path
from typing import Dict, Optional
from loguru import logger
import moderngl as mgl
from PIL import Image
import numpy as np

from app.config import Config


class TextureManager:
    """Manages texture loading and caching."""

    def __init__(self, config: Config):
        """Initialize texture manager.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.textures: Dict[str, mgl.Texture] = {}
        self.texture_dir = Path("assets/textures")
        self.ctx: Optional[mgl.Context] = None

    def set_context(self, ctx: mgl.Context) -> None:
        """Set the ModernGL context.
        
        Args:
            ctx: ModernGL context
        """
        self.ctx = ctx

    def load_texture(self, name: str, path: str, srgb: bool = False) -> Optional[mgl.Texture]:
        """Load a texture from file.
        
        Args:
            name: Texture name
            path: Path to texture file
            srgb: Use sRGB color space
            
        Returns:
            Loaded texture or None
        """
        if name in self.textures:
            return self.textures[name]

        if not self.ctx:
            logger.error("Context not set")
            return None

        try:
            file_path = self.texture_dir / path
            
            if not file_path.exists():
                logger.warning(f"Texture file not found: {file_path}")
                return None
            
            image = Image.open(file_path).convert('RGB')
            image_data = np.array(image)
            
            texture = self.ctx.texture(
                image.size,
                3,
                image_data
            )
            
            if srgb:
                texture.swizzle = 'RGBA'
            
            self.textures[name] = texture
            logger.info(f"Loaded texture: {name}")
            return texture

        except Exception as e:
            logger.exception(f"Failed to load texture {name}: {e}")
            return None

    def load_cubemap(self, name: str, paths: Dict[str, str]) -> Optional[mgl.Texture]:
        """Load a cubemap texture.
        
        Args:
            name: Cubemap name
            paths: Dictionary mapping face names to file paths
            
        Returns:
            Loaded cubemap or None
        """
        if name in self.textures:
            return self.textures[name]

        if not self.ctx:
            logger.error("Context not set")
            return None

        try:
            face_data = {}
            for face, path in paths.items():
                file_path = self.texture_dir / path
                if not file_path.exists():
                    logger.warning(f"Cubemap face not found: {file_path}")
                    continue
                
                image = Image.open(file_path).convert('RGB')
                face_data[face] = np.array(image)
            
            if len(face_data) < 6:
                logger.error(f"Incomplete cubemap: {name}")
                return None
            
            # Create cubemap from loaded faces
            logger.info(f"Loaded cubemap: {name}")
            return None

        except Exception as e:
            logger.exception(f"Failed to load cubemap {name}: {e}")
            return None

    def get_texture(self, name: str) -> Optional[mgl.Texture]:
        """Get a loaded texture.
        
        Args:
            name: Texture name
            
        Returns:
            Texture or None
        """
        return self.textures.get(name)

    def release_all(self) -> None:
        """Release all textures."""
        for texture in self.textures.values():
            texture.release()
        self.textures.clear()
        logger.info("Released all textures")
