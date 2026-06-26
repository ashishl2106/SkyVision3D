"""Mesh management and generation."""

from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
import numpy as np
import moderngl as mgl


@dataclass
class Mesh:
    """Simple mesh data structure."""
    vertices: np.ndarray
    indices: np.ndarray
    normals: np.ndarray
    uvs: Optional[np.ndarray] = None
    vao: Optional[mgl.VertexArray] = None


class MeshManager:
    """Manages mesh creation and caching."""

    def __init__(self):
        """Initialize mesh manager."""
        self.meshes: Dict[str, Mesh] = {}

    def create_sphere(self, name: str, radius: float = 1.0, segments: int = 32, rings: int = 16) -> Mesh:
        """Create a sphere mesh.
        
        Args:
            name: Mesh name
            radius: Sphere radius
            segments: Number of longitude segments
            rings: Number of latitude rings
            
        Returns:
            Sphere mesh
        """
        vertices = []
        indices = []
        normals = []
        uvs = []

        for ring in range(rings + 1):
            lat0 = np.pi * (-0.5 + float(ring - 1) / rings)
            lat1 = np.pi * (-0.5 + float(ring) / rings)

            sin_lat0 = np.sin(lat0)
            cos_lat0 = np.cos(lat0)
            sin_lat1 = np.sin(lat1)
            cos_lat1 = np.cos(lat1)

            for seg in range(segments + 1):
                lon = 2 * np.pi * float(seg) / segments
                sin_lon = np.sin(lon)
                cos_lon = np.cos(lon)

                x = cos_lat1 * cos_lon
                y = sin_lat1
                z = cos_lat1 * sin_lon

                vertices.extend([radius * x, radius * y, radius * z])
                normals.extend([x, y, z])
                uvs.extend([float(seg) / segments, float(ring) / rings])

        for ring in range(rings):
            a0 = ring * (segments + 1)
            a1 = a0 + segments + 1

            for seg in range(segments):
                indices.extend([a0, a1, a0 + 1])
                indices.extend([a1, a1 + 1, a0 + 1])
                a0 += 1
                a1 += 1

        mesh = Mesh(
            vertices=np.array(vertices, dtype=np.float32),
            indices=np.array(indices, dtype=np.uint32),
            normals=np.array(normals, dtype=np.float32),
            uvs=np.array(uvs, dtype=np.float32)
        )
        
        self.meshes[name] = mesh
        return mesh

    def create_cube(self, name: str, size: float = 1.0) -> Mesh:
        """Create a cube mesh.
        
        Args:
            name: Mesh name
            size: Cube size
            
        Returns:
            Cube mesh
        """
        s = size / 2
        vertices = [
            -s, -s, -s, s, -s, -s, s, s, -s, -s, s, -s,
            -s, -s, s, s, -s, s, s, s, s, -s, s, s,
            -s, -s, -s, -s, s, -s, -s, s, s, -s, -s, s,
            s, -s, -s, s, s, -s, s, s, s, s, -s, s,
            -s, s, -s, s, s, -s, s, s, s, -s, s, s,
            -s, -s, -s, s, -s, -s, s, -s, s, -s, -s, s,
        ]

        indices = list(range(len(vertices) // 3))
        normals = [0] * len(vertices)

        mesh = Mesh(
            vertices=np.array(vertices, dtype=np.float32),
            indices=np.array(indices, dtype=np.uint32),
            normals=np.array(normals, dtype=np.float32)
        )
        
        self.meshes[name] = mesh
        return mesh

    def get_mesh(self, name: str) -> Optional[Mesh]:
        """Get a mesh.
        
        Args:
            name: Mesh name
            
        Returns:
            Mesh or None
        """
        return self.meshes.get(name)
