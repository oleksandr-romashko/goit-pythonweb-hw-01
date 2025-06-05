import logging

from goit_pythonweb_hw_01.utils.logging_config import setup_logging


class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def start_engine(self):
        print(f"{self.make} {self.model}: Engine started")


class Motorcycle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def start_engine(self):
        print(f"{self.make} {self.model}: Engine started")


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger("task 1")

    vehicle1 = Car("Toyota", "Corolla")
    vehicle1.start_engine()

    vehicle2 = Motorcycle("Harley-Davidson", "Sportster")
    vehicle2.start_engine()
