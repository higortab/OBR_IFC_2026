#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction

# Declara a configuração dos motores
motors = {
  "left": Motor(Port.C, Direction.COUNTERCLOCKWISE),
  "right": Motor(Port.A, Direction.COUNTERCLOCKWISE),
}

# Circunferencia da roda: 175.9mm
MM_PER_DEGREE = 175.9 / 360  # 1 grau = 175.9 / 360 = 0.488mm

# Velocidade
BASE_SPEED = 150  # Velocidade normal
TURN_SPEED = 70  # Troca de direção

# Distância
SWEEP_DISTANCE = 20  # Distância da diagonal percorrida


def degrees_to_mm(degrees):
  return degrees * MM_PER_DEGREE


class Motors:
  def __init__(self):
    """Reseta os encoders ao iniciar a classe"""
    motors["left"].reset_angle(0)
    motors["right"].reset_angle(0)

  def get_average_angle(self):
    """Usa a media dos encoders dos dois motores como referencia de distancia"""
    return (motors["left"].angle() + motors["right"].angle()) / 2

  def move_forward(self, speed):
    motors["left"].run(speed)
    motors["right"].run(speed)
    
  def stop(self):
    motors["left"].stop()
    motors["right"].stop()

  # def change_diagonal()
