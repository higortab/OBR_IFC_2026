#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor


def classify_reflection(value):
  # Generico: preto <= 15, branco > 15 (baseado nos testes: preto 4-7, branco 51-58)
  if value <= 15:
    return 0
  return 1


class ReflectionDetector:
  """BLACK = 0; WHITE = 1"""

  def __init__(self, portL, portR):
    self._left_sensor = ColorSensor(portL)
    self._right_sensor = ColorSensor(portR)

  def update(self):
    """
    Chama a cada iteracao do loop principal.
    Retorna uma tupla (esquerdo, direito) com 0 ou 1 para cada sensor.
    """
    return classify_reflection(self._left_sensor.reflection()), classify_reflection(
      self._right_sensor.reflection()
    )

  def is_on_line(self):
    """Retorna True se qualquer sensor lateral estiver sobre a linha preta"""
    left, right = self.update()
    return left == 0 or right == 0

  def raw(self):
    """Retorna os valores brutos de reflexao de cada sensor, util para debug"""
    return self._left_sensor.reflection(), self._right_sensor.reflection()
