#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Direction

# Circunferencia da roda: 175.9mm
MM_PER_DEGREE = 175.9 / 360  # 1 grau = 175.9 / 360 = 0.488mm

# Velocidade
BASE_SPEED = 150  # Velocidade normal
TURN_SPEED = 70  # Troca de direção, muito ruim pra caranguejo

# Distância
SWEEP_DISTANCE = 20  # Distância da diagonal percorrida


def degrees_to_mm(degrees):
  return degrees * MM_PER_DEGREE


class MotionMotors:
  def __init__(self, portL, portR):
    self._left_motor = Motor(portL, Direction.COUNTERCLOCKWISE)
    self._right_motor = Motor(portR, Direction.COUNTERCLOCKWISE)

    """Reseta os encoders ao iniciar a classe"""
    self._left_motor.reset_angle(0)
    self._right_motor.reset_angle(0)

  @property
  def left(self):
    return self._left_motor

  @property
  def right(self):
    return self._right_motor

  def get_average_angle(self):
    """Usa a media dos encoders dos dois motores como referencia de distancia"""
    return (self._left_motor.angle() + self._right_motor.angle()) / 2

  def move_forward(self, speed):
    self._left_motor.run(speed)
    self._right_motor.run(speed)

  def stop(self):
    self._left_motor.stop()
    self._right_motor.stop()

  def run(self, left_speed, right_speed):
    self._left_motor.run(left_speed)
    self._right_motor.run(right_speed)
