#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait

from config.motors import Motors
from config.rgb_sensor import RgbDetector
from config.reflection_sensors import ReflectionDetector
from config.ultrasonic import UltrasonicDetector

ev3 = EV3Brick()

motors = Motors(Port.C, Port.A)
rgb = RgbDetector(Port.S1)
sensors = ReflectionDetector(Port.S3, Port.S4)
ultrasonic = UltrasonicDetector(Port.S2)

while True:
  color = rgb.raw_color()

  ev3.screen.clear()
  ev3.screen.draw_text(0, 0, str(color))

  wait(100)
