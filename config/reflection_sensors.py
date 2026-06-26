#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor

def classify_reflection(value):
  if value <= 15:
    return 0
  return 1


class ReflectionDetector:
  """BLACK = 0; WHITE = 1"""

  def __init__(self, portL, portR):
    self._left_sensor = ColorSensor(portL)
    self._right_sensor = ColorSensor(portR)
    self._last = (1, 1)

  def update(self):
    self._last = (
      classify_reflection(self._left_sensor.reflection()),
      classify_reflection(self._right_sensor.reflection()),
    )
    return self._last

  def is_on_line(self):
    return self._last[0] == 0 or self._last[1] == 0

  def raw(self):
    return self._left_sensor.reflection(), self._right_sensor.reflection()
