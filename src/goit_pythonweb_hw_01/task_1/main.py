"""
Task 1 — Abstract Factory Pattern Implementation

This module defines an abstract vehicle system using the Factory Method pattern.
Includes abstract base classes for Vehicle and VehicleFactory, and concrete implementations
for US and EU specifications of cars and motorcycles.
"""

from abc import ABC, abstractmethod
import logging

from goit_pythonweb_hw_01.utils.logging_config import setup_logging

logger = logging.getLogger("goit_pythonweb_hw_01.task_1")


class Vehicle(ABC):
    """Abstract base class representing a generic vehicle."""

    def __init__(self, make: str, model: str, region_spec: str) -> None:
        """
        Initialize a vehicle.

        Args:
            make: The manufacturer of the vehicle.
            model: The model of the vehicle.
            region_spec: The regional specification (e.g., 'US Spec', 'EU Spec').
        """
        self.make = make
        self.model = model
        self.region_spec = region_spec

    def __str__(self) -> str:
        return f"{self.make} {self.model} ({self.region_spec})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(make={self.make!r}, model={self.model!r}, region_spec={self.region_spec!r})"
        )

    @abstractmethod
    def start_engine(self) -> None:
        """Start the vehicle's engine."""
        pass


class VehicleFactory(ABC):
    """Abstract factory for creating vehicles."""

    def __init__(self, region_spec: str) -> None:
        """
        Initialize the factory with a regional specification.

        Args:
            region_spec: A string indicating the regional spec (e.g., 'US Spec').
        """
        self.region_spec = region_spec

    @abstractmethod
    def create_car(self, make: str, model: str) -> Vehicle:
        """Create a car instance with the given make and model."""
        pass

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Vehicle:
        """Create a motorcycle instance with the given make and model."""
        pass


class Car(Vehicle):
    """Class representing a car."""

    def start_engine(self) -> None:
        """Start the car's engine."""
        logger.info("%s: Engine started", self)


class Motorcycle(Vehicle):
    """Class representing a motorcycle."""

    def start_engine(self) -> None:
        """Start the motorcycle's engine."""
        logger.info("%s: Engine fired up", self)


class USVehicleFactory(VehicleFactory):
    """Factory for creating US-spec vehicles."""

    def __init__(self) -> None:
        super().__init__("US Spec")

    def create_car(self, make: str, model: str) -> Vehicle:
        """Create a US-spec car."""
        return Car(make, model, self.region_spec)

    def create_motorcycle(self, make: str, model: str) -> Vehicle:
        """Create a US-spec motorcycle."""
        return Motorcycle(make, model, self.region_spec)


class EUVehicleFactory(VehicleFactory):
    """Factory for creating EU-spec vehicles."""

    def __init__(self) -> None:
        super().__init__("EU Spec")

    def create_car(self, make: str, model: str) -> Vehicle:
        """Create an EU-spec car."""
        return Car(make, model, self.region_spec)

    def create_motorcycle(self, make: str, model: str) -> Vehicle:
        """Create an EU-spec motorcycle."""
        return Motorcycle(make, model, self.region_spec)


def main():
    """Run example usage of the abstract factory pattern for vehicles."""
    setup_logging()

    factory_us = USVehicleFactory()
    factory_eu = EUVehicleFactory()

    vehicle1 = factory_eu.create_car("Toyota", "Corolla")
    vehicle2 = factory_us.create_motorcycle("Harley-Davidson", "Sportster")

    vehicle1.start_engine()
    vehicle2.start_engine()


if __name__ == "__main__":
    main()
