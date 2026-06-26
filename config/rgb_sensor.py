#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port

# Declara a configuração dos sensor rgb
sensor = ColorSensor(Port.S1)

# Distancia minima percorrida para confirmar cada cor (em mm)
MIN_DIST = {
  "GREEN": 10,
  "RED": 10,
  "BLACK": 5,
  "WHITE": 5,
  "SILVER": 5,
}


def classify_rgb(r, g, b):
  if r > 15 and g < 10:
    return "RED"
  if g > 10 and b < 8:
    return "GREEN"
  if r + g + b < 10:
    return "BLACK"
  if b > g and b > r:
    return "WHITE"
  return "SILVER"


class RgbDetector:
  def __init__(self):
    self._current_color = None
    self._start_angle = 0
    self._confirmed_color = None

  def update(self, distance_mm):
    """
    Chama a cada iteracao do loop principal passando os valores RGB do sensor.
    Retorna a cor confirmada ou None se ainda nao confirmou.
    """
    r, g, b = sensor.rgb()
    color = classify_rgb(r, g, b)

    # Reseta o contador de distancia quando a cor muda
    if color != self._current_color:
      self._current_color = color
      self._start_distance = distance_mm
      self._confirmed_color = None

    # Confirma a cor se passou da distancia minima
    traveled = distance_mm - self._start_distance

    if traveled >= MIN_DIST[color]:
      self._confirmed_color = color

    return self._confirmed_color

  def raw_color(self):
    """Retorna a classificacao imediata sem confirmacao, util para debug"""
    r, g, b = sensor.rgb()
    return classify_rgb(r, g, b)

  def reset(self):
    """Reseta o estado do detector"""
    self._current_color = None
    self._confirmed_color = None
    self._start_distance = 0
