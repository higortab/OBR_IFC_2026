#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Button
from pybricks.tools import wait

from config.motion_motors import MotionMotors
from config.mode_motor import ModeMotor

from config.rgb_sensor import RgbDetector
from config.reflection_sensors import ReflectionDetector
from config.ultrasonic_sensor import UltrasonicDetector

# from resgate import Resgate

ev3 = EV3Brick()

motion = MotionMotors(Port.C, Port.A)
mode = ModeMotor(Port.B)

rgb = RgbDetector(Port.S1)
sensors = ReflectionDetector(Port.S3, Port.S4)
ultrasonic = UltrasonicDetector(Port.S2)

mode.rescue_mode()

while True:
  if Button.CENTER in ev3.buttons.pressed():
    mode.activate_claw()
    # Espera soltar o botão antes de continuar
    while Button.CENTER not in ev3.buttons.pressed():
      pass

  color = rgb.raw()

  ev3.screen.clear()
  ev3.screen.draw_text(0, 0, str(mode.motor.angle()))

  wait(100)
