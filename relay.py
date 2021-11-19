#!/usr/bin/env python3
"""
    Control classes/functions to operater relays
"""
from typing import Dict

from GPIO.gpio import GPIOPin
from RPi import GPIO


class Relay:
    """Represens a relay that controls electrical equipment"""

    _device_type = None

    def __init__(self, gpio_pin: GPIOPin, device_id: str):
        self.gpio_pin = gpio_pin
        self.device_id = device_id
        if not self._device_type:
            raise ValueError("Device type unknown")

    def on(self):
        """Turns on the relay"""
        print(f"Turning {self.device_id} on")
        self.gpio_pin.output(GPIO.LOW)

    def off(self):
        """Turns of the relay"""
        print(f"Turning {self.device_id} off")
        self.gpio_pin.output(GPIO.HIGH)

    def toggle(self):
        """Toggles the relay on/off"""
        self.gpio_pin.output(not self.gpio_pin.input())

    @classmethod
    def get_relay(cls, plant_config: Dict, device_id: str):
        """Returns a Relay for the specified device"""
        return cls(
            GPIOPin(plant_config["relays"][plant_config[cls._device_type][device_id]]),
            device_id,
        )
