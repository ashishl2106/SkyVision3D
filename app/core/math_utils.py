"""Mathematical utilities for 3D graphics."""

import math
import glm
from typing import Tuple
import numpy as np


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation.
    
    Args:
        a: Start value
        b: End value
        t: Interpolation factor (0-1)
        
    Returns:
        Interpolated value
    """
    return a + (b - a) * t


def slerp(a: glm.quat, b: glm.quat, t: float) -> glm.quat:
    """Spherical linear interpolation between quaternions.
    
    Args:
        a: Start quaternion
        b: End quaternion
        t: Interpolation factor (0-1)
        
    Returns:
        Interpolated quaternion
    """
    return glm.slerp(a, b, t)


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians.
    
    Args:
        degrees: Angle in degrees
        
    Returns:
        Angle in radians
    """
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees.
    
    Args:
        radians: Angle in radians
        
    Returns:
        Angle in degrees
    """
    return math.degrees(radians)


def create_rotation_quaternion(axis: glm.vec3, angle: float) -> glm.quat:
    """Create rotation quaternion.
    
    Args:
        axis: Rotation axis
        angle: Rotation angle in radians
        
    Returns:
        Quaternion representing the rotation
    """
    return glm.angleAxis(angle, axis)


def spherical_to_cartesian(latitude: float, longitude: float, radius: float) -> glm.vec3:
    """Convert spherical coordinates to Cartesian.
    
    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        radius: Radius from center
        
    Returns:
        Cartesian coordinates
    """
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)
    
    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.sin(lat_rad)
    z = radius * math.cos(lat_rad) * math.sin(lon_rad)
    
    return glm.vec3(x, y, z)


def cartesian_to_spherical(pos: glm.vec3) -> Tuple[float, float, float]:
    """Convert Cartesian coordinates to spherical.
    
    Args:
        pos: Cartesian position
        
    Returns:
        Tuple of (latitude, longitude, radius) in degrees and units
    """
    x, y, z = pos.x, pos.y, pos.z
    radius = math.sqrt(x*x + y*y + z*z)
    
    if radius == 0:
        return 0.0, 0.0, 0.0
    
    latitude = math.degrees(math.asin(y / radius))
    longitude = math.degrees(math.atan2(z, x))
    
    return latitude, longitude, radius


def normalize_angle(angle: float) -> float:
    """Normalize angle to -180 to 180 degrees.
    
    Args:
        angle: Angle in degrees
        
    Returns:
        Normalized angle
    """
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def distance_between_coordinates(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates on Earth using Haversine formula.
    
    Args:
        lat1: First latitude in degrees
        lon1: First longitude in degrees
        lat2: Second latitude in degrees
        lon2: Second longitude in degrees
        
    Returns:
        Distance in kilometers
    """
    EARTH_RADIUS = 6371.0
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    return EARTH_RADIUS * c


def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate bearing between two coordinates.
    
    Args:
        lat1: First latitude in degrees
        lon1: First longitude in degrees
        lat2: Second latitude in degrees
        lon2: Second longitude in degrees
        
    Returns:
        Bearing in degrees (0-360)
    """
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    
    x = math.sin(dlon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
    
    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360
