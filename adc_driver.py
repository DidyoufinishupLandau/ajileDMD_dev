# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 17/07/2023

Reads data from Raspberry Pi Pico

"""

import serial
import time
from typing import Union


class raspberry_pico_adc:
    """Class defined to wrap Raspberry Pi Pico ADC controller."""
    ser: serial.Serial()
    _points: int
    _delay: int

    def __init__(self, com: str):
        # Set up interface
        self.ser = serial.Serial(com, 128000, xonxoff=True)
        # initialize the number of points
        self._points = 0
        self._delay = 0

    def read(self):
        ser_bytes = self.ser.readline()
        # Read the data (looks for terminating character '/r/n')
        return str(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))

    def write(self, text: Union[str, bytes] = ""):
        # Write data to serial port
        if type(text) is str:
            # convert string to bytes
            text = bytes(text, "utf-8")
        self.ser.write(text)

    # COMMANDS
    def led(self, state: bool) -> bool:
        if state:
            self.write(b"LED_ON\n")
        else:
            self.write(b"LED_OFF\n")
        return state

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, no: int):
        self._points = no
        self.ser.write(f"_N_{no}\n")

    @property
    def delay(self) -> int:
        return self._delay

    @delay.setter
    def delay(self, d: int):
        self._delay = d
        # delay in us
        self.write(f"_D_{d}\n")

    def start(self):
        self.ser.write(b"_S_TRUE\n")

    def info(self):
        self.ser.write(b"INFO\n")
        # There are 3 values to be printed
        for i in range(3):
            print(str(self.read()).replace("\\r\\n", ""))

    def Get_data(self) -> list:
        li: list = []
        self.write(b"_GD_\n")
        time.sleep(0.001)

        while True:
            text = self.read()
            if "END" in text:
                return li
            else:
                li.append(text)

    def reset(self):
        self.write(b"RESTART\n")

    def test(self) -> str:
        self.write(b"TEST\n")
        return self.read()

    # Check if is ready to acquire the data
    @property
    def is_ready(self) -> bool:
        self.write(b"_DR_\n")
        ret = self.read()
        return "READY" in ret
