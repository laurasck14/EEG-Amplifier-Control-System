#!/usr/bin/env python3
''' Laura Santa Cruz Kaster
include functionalities....
'''
import sys, os, re
from datetime import datetime

class Sensor:
    def __init__(self, tag: str):
        """
        Initialize a sensor with a tag (e.g., "frontal", "occipital").
        :param tag: The scalp position of the sensor.
        """
        self.tag = tag

    def __repr__(self):
        return f"Sensor(tag='{self.tag}')"

class Amplifier:
    def __init__(self, serial_number: str, model: str, manufacturer: str, next_maintenance: datetime, sampling_rate: int, gain: int):
        """
        Initialize an amplifier with basic information and default settings.
        :param serial_number: The unique serial number of the amplifier.
        :param model: The model name or string of the amplifier.
        :param manufacturer: The manufacturer name of the amplifier.
        :param next_maintenance: The date for the next planned maintenance.
        :param sampling_rate: The sampling rate of the amplifier (256, 512, or 1024 Hz).
        :param gain: The gain level of the amplifier (1 to 100).
        """
        self.serial_number = serial_number
        self.model = model
        self.manufacturer = manufacturer
        self.next_maintenance = next_maintenance
        self.sampling_rate = sampling_rate
        self.gain = gain
        self.sensors = []
        self.is_on = False  # Power status: Off by default

    def add_sensor(self, sensor: Sensor):
        """Associate a sensor with the amplifier."""
        self.sensors.append(sensor)

    def remove_sensor(self, sensor: Sensor):
        """Remove a sensor from the amplifier."""
        self.sensors.remove(sensor)

    def set_gain(self, gain: int):
        """
        Adjust the gain level of the amplifier.
        :param gain: New gain level within [1, 100].
        """
        if 1 <= gain <= 100:
            self.gain = gain
        else:
            raise ValueError("Gain must be between 1 and 100.")

    def set_sampling_rate(self, rate: int):
        """
        Adjust the sampling rate of the amplifier.
        :param rate: New sampling rate (typically 256, 512, or 1024 Hz).
        """
        if rate in [256, 512, 1024]:
            self.sampling_rate = rate
        else:
            raise ValueError("Invalid sampling rate. Choose 256, 512, or 1024 Hz.")

    def toggle_power(self):
        """Toggle the power state (on/off) of the amplifier."""
        self.is_on = not self.is_on

    def __repr__(self):
        return f"Amplifier(serial_number={self.serial_number}, model={self.model}, manufacturer={self.manufacturer}, sampling_rate={self.sampling_rate}Hz, gain={self.gain}, is_on={self.is_on}, sensors={self.sensors})"
    

class EEGAmplifierControlSystem:
    def __init__(self):
        """Initialize the control system with an empty list of amplifiers."""
        self.amplifiers = []

    def register_amplifier(self, amplifier: Amplifier):
        """Add a new amplifier to the system."""
        self.amplifiers.append(amplifier)

    def remove_amplifier(self, serial_number: str):
        """Remove an amplifier from the system by its serial number."""
        self.amplifiers = [amp for amp in self.amplifiers if amp.serial_number != serial_number]

    def list_amplifiers(self):
        """Return a list of all currently registered amplifiers."""
        return self.amplifiers

    def search_amplifier(self, serial_number=None, model=None, manufacturer=None):
        """
        Search for amplifiers by serial number, model, or manufacturer.
        :param serial_number: Search by serial number.
        :param model: Search by model string.
        :param manufacturer: Search by manufacturer.
        :return: A list of amplifiers matching the search criteria.
        """
        results = self.amplifiers
        if serial_number:
            results = [amp for amp in results if amp.serial_number == serial_number]
        if model:
            results = [amp for amp in results if amp.model == model]
        if manufacturer:
            results = [amp for amp in results if amp.manufacturer == manufacturer]
        return results

if __name__ == "__main__":
    control_system = EEGAmplifierControlSystem()

    # Create a new amplifier
    amp1 = Amplifier(serial_number="12345", model="AmpX", manufacturer="NeuroTech", next_maintenance=datetime(2025, 10, 1), sampling_rate=512, gain=50)
    control_system.register_amplifier(amp1)

    # Add sensors to the amplifier
    sensor1 = Sensor("frontal")
    sensor2 = Sensor("occipital")
    amp1.add_sensor(sensor1)
    amp1.add_sensor(sensor2)

    # Adjust the gain and sampling rate
    amp1.set_gain(75)
    amp1.set_sampling_rate(1024)

    # Power on the amplifier
    amp1.toggle_power()

    # List all amplifiers
    print(f"Hola: {control_system.list_amplifiers()}")

    # Search for an amplifier by model
    search_results = control_system.search_amplifier(model="AmpX")
    print(f"Search: {search_results}")

    # Remove an amplifier by serial number
    control_system.remove_amplifier("12345")
    print(control_system.list_amplifiers())