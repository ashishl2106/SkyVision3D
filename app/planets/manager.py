"""Planet data management."""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from loguru import logger
import glm


@dataclass
class Planet:
    """Planet data structure."""
    id: str
    name: str
    position: glm.vec3
    radius: float
    color: glm.vec4 = field(default_factory=lambda: glm.vec4(0.5, 0.5, 1, 1))
    texture_path: Optional[str] = None
    rotation_speed: float = 0.0
    rotation_axis: glm.vec3 = field(default_factory=lambda: glm.vec3(0, 1, 0))
    atmosphere: bool = False
    rings: bool = False


class PlanetManager:
    """Manages planet data."""

    def __init__(self):
        """Initialize planet manager."""
        self.planets: Dict[str, Planet] = {}
        self._initialize_default_planets()

    def _initialize_default_planets(self) -> None:
        """Initialize default planets."""
        # Earth
        earth = Planet(
            id="earth",
            name="Earth",
            position=glm.vec3(0, 0, 0),
            radius=6371000.0,
            color=glm.vec4(0.2, 0.6, 1, 1),
            texture_path="earth/earth_diffuse.jpg",
            rotation_speed=0.00007,
            atmosphere=True
        )
        self.add_planet(earth)
        
        # Sun
        sun = Planet(
            id="sun",
            name="Sun",
            position=glm.vec3(150000000000, 0, 0),
            radius=696000000.0,
            color=glm.vec4(1, 1, 0, 1),
            texture_path="sun/sun_diffuse.jpg"
        )
        self.add_planet(sun)
        
        # Moon
        moon = Planet(
            id="moon",
            name="Moon",
            position=glm.vec3(384400000, 0, 0),
            radius=1737400.0,
            color=glm.vec4(0.8, 0.8, 0.8, 1),
            texture_path="moon/moon_diffuse.jpg"
        )
        self.add_planet(moon)

    def add_planet(self, planet: Planet) -> None:
        """Add a planet.
        
        Args:
            planet: Planet object
        """
        self.planets[planet.id] = planet
        logger.info(f"Added planet: {planet.name} ({planet.id})")

    def remove_planet(self, planet_id: str) -> None:
        """Remove a planet.
        
        Args:
            planet_id: Planet ID
        """
        if planet_id in self.planets:
            del self.planets[planet_id]
            logger.info(f"Removed planet: {planet_id}")

    def get_planet(self, planet_id: str) -> Optional[Planet]:
        """Get a planet by ID.
        
        Args:
            planet_id: Planet ID
            
        Returns:
            Planet object or None
        """
        return self.planets.get(planet_id)

    def get_planet_by_name(self, name: str) -> Optional[Planet]:
        """Get a planet by name.
        
        Args:
            name: Planet name
            
        Returns:
            Planet object or None
        """
        for planet in self.planets.values():
            if planet.name.lower() == name.lower():
                return planet
        return None

    def get_all_planets(self) -> List[Planet]:
        """Get all planets.
        
        Returns:
            List of planet objects
        """
        return list(self.planets.values())

    def update_planets(self, delta_time: float) -> None:
        """Update planet rotations.
        
        Args:
            delta_time: Time since last update
        """
        for planet in self.planets.values():
            if planet.rotation_speed > 0:
                # Update rotation
                pass

    def clear_all(self) -> None:
        """Clear all planets."""
        self.planets.clear()
        logger.info("Cleared all planets")
