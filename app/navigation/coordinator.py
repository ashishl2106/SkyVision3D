"""Coordinate system and navigation."""

from typing import Optional, Tuple
from dataclasses import dataclass
from loguru import logger
import glm
import math


@dataclass
class Coordinate:
    """Geographic coordinate (latitude, longitude, altitude)."""
    latitude: float  # -90 to 90 degrees
    longitude: float  # -180 to 180 degrees
    altitude: float = 0.0  # meters above sea level

    def __str__(self) -> str:
        return f"Lat: {self.latitude:.4f}°, Lon: {self.longitude:.4f}°, Alt: {self.altitude:.0f}m"

    def to_cartesian(self, planet_radius: float = 6371000.0) -> glm.vec3:
        """Convert to 3D Cartesian coordinates.
        
        Args:
            planet_radius: Planet radius in meters
            
        Returns:
            3D position vector
        """
        lat_rad = math.radians(self.latitude)
        lon_rad = math.radians(self.longitude)
        
        r = planet_radius + self.altitude
        
        x = r * math.cos(lat_rad) * math.cos(lon_rad)
        y = r * math.sin(lat_rad)
        z = r * math.cos(lat_rad) * math.sin(lon_rad)
        
        return glm.vec3(x, y, z)

    @staticmethod
    def from_cartesian(position: glm.vec3, planet_radius: float = 6371000.0) -> 'Coordinate':
        """Convert from 3D Cartesian coordinates.
        
        Args:
            position: 3D position vector
            planet_radius: Planet radius in meters
            
        Returns:
            Coordinate object
        """
        x, y, z = position.x, position.y, position.z
        
        latitude = math.degrees(math.asin(y / glm.length(position)))
        longitude = math.degrees(math.atan2(z, x))
        altitude = glm.length(position) - planet_radius
        
        return Coordinate(latitude, longitude, altitude)


class CoordinateNavigator:
    """Handles coordinate selection and navigation."""

    def __init__(self):
        """Initialize coordinate navigator."""
        self.selected_coordinate: Optional[Coordinate] = None
        self.target_coordinate: Optional[Coordinate] = None
        self.navigation_active = False
        self.navigation_progress = 0.0
        self.navigation_duration = 5.0  # seconds
        self.camera_distance = 100000000.0  # 100,000 km

    def select_coordinate(self, latitude: float, longitude: float, altitude: float = 0.0) -> None:
        """Select a coordinate.
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            altitude: Altitude in meters
        """
        self.selected_coordinate = Coordinate(latitude, longitude, altitude)
        logger.info(f"Selected coordinate: {self.selected_coordinate}")

    def goto_coordinate(self, latitude: float, longitude: float, altitude: float = 0.0, duration: float = 5.0) -> None:
        """Navigate to a coordinate.
        
        Args:
            latitude: Target latitude in degrees
            longitude: Target longitude in degrees
            altitude: Target altitude in meters
            duration: Navigation duration in seconds
        """
        self.target_coordinate = Coordinate(latitude, longitude, altitude)
        self.navigation_active = True
        self.navigation_progress = 0.0
        self.navigation_duration = duration
        logger.info(f"Navigating to: {self.target_coordinate}")

    def goto_selected(self, duration: float = 5.0) -> None:
        """Navigate to selected coordinate.
        
        Args:
            duration: Navigation duration in seconds
        """
        if self.selected_coordinate:
            self.goto_coordinate(
                self.selected_coordinate.latitude,
                self.selected_coordinate.longitude,
                self.selected_coordinate.altitude,
                duration
            )
        else:
            logger.warning("No coordinate selected")

    def cancel_navigation(self) -> None:
        """Cancel current navigation."""
        self.navigation_active = False
        self.target_coordinate = None
        logger.info("Navigation cancelled")

    def update(self, delta_time: float) -> Tuple[Optional[Coordinate], float]:
        """Update navigation.
        
        Args:
            delta_time: Time since last update in seconds
            
        Returns:
            Tuple of (current coordinate, progress 0-1)
        """
        if not self.navigation_active or not self.target_coordinate:
            return None, 0.0

        self.navigation_progress += delta_time / self.navigation_duration
        
        if self.navigation_progress >= 1.0:
            self.navigation_active = False
            self.navigation_progress = 1.0
            return self.target_coordinate, 1.0
        
        # Linear interpolation for now
        # TODO: Add easing functions
        return self.target_coordinate, self.navigation_progress

    def get_selected(self) -> Optional[Coordinate]:
        """Get selected coordinate.
        
        Returns:
            Selected coordinate or None
        """
        return self.selected_coordinate

    def get_target(self) -> Optional[Coordinate]:
        """Get target coordinate.
        
        Returns:
            Target coordinate or None
        """
        return self.target_coordinate

    def is_navigating(self) -> bool:
        """Check if currently navigating.
        
        Returns:
            True if navigating
        """
        return self.navigation_active

    def get_navigation_progress(self) -> float:
        """Get navigation progress.
        
        Returns:
            Progress 0-1
        """
        return self.navigation_progress
