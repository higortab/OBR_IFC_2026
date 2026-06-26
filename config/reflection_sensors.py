#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port

# Declara a configuração dos sensores simples
sensors = {
  "left": ColorSensor(Port.S3),
  "right": ColorSensor(Port.S4),
}


def classify_reflection(value):
  # Generico: preto <= 15, branco > 15 (baseado nos testes: preto 4-7, branco 51-58)
  if value <= 15:
    return 0
  return 1


class ReflectionDetector:
  """BLACK = 0; WHITE = 1"""

  def update(self):
    """
    Chama a cada iteracao do loop principal.
    Retorna uma tupla (esquerdo, direito) com 0 ou 1 para cada sensor.
    """
    return classify_reflection(sensors["left"].reflection()), classify_reflection(
      sensors["right"].reflection()
    )

  def is_on_line(self):
    """Retorna True se qualquer sensor lateral estiver sobre a linha preta"""
    left, right = self.update()
    return left == 0 or right == 0

  def raw(self):
    """Retorna os valores brutos de reflexao de cada sensor, util para debug"""
    return sensors["left"].reflection(), sensors["right"].reflection()
