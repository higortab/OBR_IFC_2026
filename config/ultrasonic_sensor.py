#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import UltrasonicSensor

START_DISTANCE = 180
CONFIRM_DISTANCE = 70
MAX_CONFIRM_MM = 80
OSCILLATION_TOLERANCE = 10


class UltrasonicDetector:
  def __init__(self, port):
    self._ultra = UltrasonicSensor(port)
    self.reset()

  def reset(self):
    self._state = "IDLE"
    self._start_distance_mm = 0
    self._last_reading = float("inf")

  def update(self, traveled_mm):
    reading = self._ultra.distance()

    if self._state == "IDLE":
      if reading <= START_DISTANCE:
        self._state = "CHECKING"
        self._start_distance_mm = traveled_mm
        self._last_reading = reading
      return False

    traveled = traveled_mm - self._start_distance_mm

    if (
      reading <= CONFIRM_DISTANCE
      and reading <= self._last_reading + OSCILLATION_TOLERANCE
    ):
      self.reset()
      return True

    if reading > START_DISTANCE:
      self.reset()
      return False

    if traveled >= MAX_CONFIRM_MM:
      self.reset()
      return False

    if reading < self._last_reading:
      self._last_reading = reading

    return False

  def raw(self):
    return self._ultra.distance()
