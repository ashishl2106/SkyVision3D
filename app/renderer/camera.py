"""Camera system for 3D rendering."""

import glm
import math
from app.config import Config


class Camera:
    """Camera for 3D scene viewing."""

    def __init__(self, config: Config):
        """Initialize camera.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.position = glm.vec3(0.0, 0.0, config.camera.initial_distance)
        self.target = glm.vec3(0.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.fov = config.camera.fov
        self.aspect = config.display.resolution.width / config.display.resolution.height
        self.near = config.camera.near_plane
        self.far = config.camera.far_plane
        self.distance = config.camera.initial_distance
        self.latitude = 0.0
        self.longitude = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

    def get_view_matrix(self) -> glm.mat4:
        """Get view matrix.
        
        Returns:
            View matrix
        """
        return glm.lookAt(self.position, self.target, self.up)

    def get_projection_matrix(self) -> glm.mat4:
        """Get projection matrix.
        
        Returns:
            Projection matrix
        """
        return glm.perspective(glm.radians(self.fov), self.aspect, self.near, self.far)

    def update_position(self, latitude: float, longitude: float, distance: float) -> None:
        """Update camera position using spherical coordinates.
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            distance: Distance from center
        """
        self.latitude = latitude
        self.longitude = longitude
        self.distance = distance
        
        lat_rad = math.radians(latitude)
        lon_rad = math.radians(longitude)
        
        x = distance * math.cos(lat_rad) * math.cos(lon_rad)
        y = distance * math.sin(lat_rad)
        z = distance * math.cos(lat_rad) * math.sin(lon_rad)
        
        self.position = glm.vec3(x, y, z)

    def orbit(self, delta_lat: float, delta_lon: float) -> None:
        """Orbit camera around target.
        
        Args:
            delta_lat: Latitude change
            delta_lon: Longitude change
        """
        self.update_position(
            self.latitude + delta_lat,
            self.longitude + delta_lon,
            self.distance
        )

    def zoom(self, factor: float) -> None:
        """Zoom camera in/out.
        
        Args:
            factor: Zoom factor
        """
        new_distance = self.distance * factor
        new_distance = max(
            self.config.camera.min_distance,
            min(self.config.camera.max_distance, new_distance)
        )
        self.update_position(self.latitude, self.longitude, new_distance)

    def pan(self, delta_x: float, delta_y: float) -> None:
        """Pan camera.
        
        Args:
            delta_x: X pan amount
            delta_y: Y pan amount
        """
        right = glm.normalize(glm.cross(self.target - self.position, self.up))
        self.target += right * delta_x + self.up * delta_y
        self.position += right * delta_x + self.up * delta_y
