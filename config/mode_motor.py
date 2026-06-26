#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Direction
# from pybricks.tools import wait

BASE_SPEED = 150
SUPER_SPEED = 360

LINE_DEGREES = 0
RESCUE_DEGREES = 120
CLAW_DEGREES = 10


class ModeMotor:
  def __init__(self, port):
    self._motor = Motor(port, Direction.COUNTERCLOCKWISE)
    self._motor.reset_angle(0)

  @property
  def motor(self):
    return self._motor

  def line_mode(self):
    """modo segue linha"""
    self._motor.run_target(BASE_SPEED, LINE_DEGREES)

  def rescue_mode(self):
    """modo resgate"""
    self._motor.run_target(BASE_SPEED, RESCUE_DEGREES)

  def activate_claw(self):
    """Acionar garra"""
    self._motor.run_angle(SUPER_SPEED, CLAW_DEGREES)
    self._motor.run_target(BASE_SPEED, RESCUE_DEGREES)
