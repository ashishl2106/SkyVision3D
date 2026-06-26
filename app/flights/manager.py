"""Flight data management."""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from loguru import logger
import glm


@dataclass
class Flight:
    """Flight data structure."""
    id: str
    callsign: str
    position: glm.vec3
    direction: glm.vec3 = field(default_factory=lambda: glm.vec3(1, 0, 0))
    speed: float = 500.0
    altitude: float = 10000.0
    color: glm.vec4 = field(default_factory=lambda: glm.vec4(1, 1, 1, 1))
    path_points: List[glm.vec3] = field(default_factory=list)
    path_color: glm.vec4 = field(default_factory=lambda: glm.vec4(1, 1, 0, 0.5))
    scale: float = 1.0
    active: bool = True


class FlightManager:
    """Manages flight data and updates."""

    def __init__(self):
        """Initialize flight manager."""
        self.flights: Dict[str, Flight] = {}
        self.max_path_points = 1000

    def add_flight(self, flight: Flight) -> None:
        """Add a flight.
        
        Args:
            flight: Flight object
        """
        self.flights[flight.id] = flight
        logger.info(f"Added flight: {flight.callsign} ({flight.id})")

    def remove_flight(self, flight_id: str) -> None:
        """Remove a flight.
        
        Args:
            flight_id: Flight ID
        """
        if flight_id in self.flights:
            del self.flights[flight_id]
            logger.info(f"Removed flight: {flight_id}")

    def get_flight(self, flight_id: str) -> Optional[Flight]:
        """Get a flight by ID.
        
        Args:
            flight_id: Flight ID
            
        Returns:
            Flight object or None
        """
        return self.flights.get(flight_id)

    def get_all_flights(self) -> List[Flight]:
        """Get all flights.
        
        Returns:
            List of flight objects
        """
        return list(self.flights.values())

    def get_active_flights(self) -> List[Flight]:
        """Get all active flights.
        
        Returns:
            List of active flight objects
        """
        return [f for f in self.flights.values() if f.active]

    def update_flight(self, flight_id: str, delta_time: float) -> None:
        """Update flight position.
        
        Args:
            flight_id: Flight ID
            delta_time: Time since last update
        """
        flight = self.get_flight(flight_id)
        if not flight or not flight.active:
            return
        
        # Update position based on direction and speed
        movement = flight.direction * flight.speed * delta_time
        flight.position += movement
        
        # Add to path
        if not flight.path_points or glm.distance(flight.path_points[-1], flight.position) > 1.0:
            flight.path_points.append(flight.position)
            if len(flight.path_points) > self.max_path_points:
                flight.path_points.pop(0)

    def update_all_flights(self, delta_time: float) -> None:
        """Update all flights.
        
        Args:
            delta_time: Time since last update
        """
        for flight_id in list(self.flights.keys()):
            self.update_flight(flight_id, delta_time)

    def clear_all(self) -> None:
        """Clear all flights."""
        self.flights.clear()
        logger.info("Cleared all flights")
