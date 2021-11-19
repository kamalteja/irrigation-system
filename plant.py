#!/usr/bin/env python3
"""
    Control classes/functions to operater pump and solenoid valves
"""

import datetime
import time
from typing import Any, Dict

from relay import Relay


class SolenoidValve(Relay):
    """Represents a solenoid valve"""
    _device_type = "valves"


class Pump(Relay):
    """Represents a pump"""
    _device_type = "pumps"


class Plant:
    """Represents a plant"""

    def __init__(
        self, name: str, solenoid_valve: SolenoidValve, water_level: str, pump: Pump
    ):
        self.name = name
        self.solenoid_valve = solenoid_valve
        self.water_level = water_level
        self.pump = pump

    @classmethod
    def parse_obj(cls, plant_obj: Dict):
        """Method to parse json object representing a plant"""
        return cls(
            name=plant_obj["name"],
            solenoid_valve=plant_obj["valve"],
            water_level=plant_obj.get("water_level", "10s"),
            pump=plant_obj["pump"],
        )

    def water(self):
        """Turns the valve to let the water in"""
        # Turn on valve
        try:
            self.solenoid_valve.on()
            time.sleep(1)
            self.pump.on()
            time.sleep(self.get_water_time(self.water_level))
        finally:
            self.pump.off()
            self.solenoid_valve.off()

    @staticmethod
    def get_water_time(water_level: str) -> int:
        """Calculates the time to water a plant"""
        try:
            date_time = datetime.datetime.strptime(water_level, "%Ss")
            s_time = date_time.second
        except ValueError as error:
            print("Unknown water_level supplied", error)
            print("Defaulting to 10 seconds")
            s_time = 10
        return s_time


class Plants:
    """Represents collection of plants"""

    def __init__(self, plant_config: Dict[str, Any]):
        self._plant_config = plant_config
        if "plants" not in self._plant_config:
            raise ValueError("No plants supplied")

    def __iter__(self):
        """Iterates through plants in plant_config and yields Plant"""
        for plant in self._plant_config["plants"]:
            plant["valve"] = SolenoidValve.get_relay(self._plant_config, plant["valve"])
            plant["pump"] = Pump.get_relay(self._plant_config, plant["pump"])
            yield Plant.parse_obj(plant_obj=plant)
