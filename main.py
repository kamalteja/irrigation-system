#!/usr/bin/env python3
"""
    Runs the irrigation system
"""
import json
import os
import sys
from datetime import datetime

from GPIO.gpio import IOBoard

from plant import Plants

PLANT_CONFIG = f"{os.path.dirname(os.path.abspath(__file__))}/plant_config.json"


def main():
    """Irrigation system"""
    with IOBoard():
        while True:
            with open(PLANT_CONFIG, "r") as r_handle:
                plant_config = json.load(r_handle)
                for plant in Plants(plant_config=plant_config):
                    plant.water()


if __name__ == "__main__":
    sys.exit(main())
