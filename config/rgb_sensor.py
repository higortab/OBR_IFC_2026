#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor

# Distancia minima percorrida para confirmar cada cor (em mm)
COLORS = {
  "green": (2, 19, 18),
  "white": (35, 50, 81),
  "silver": (14, 18, 60),
  "red": (30, 2, 6),
  "black": (0, 0, 0),
}

# Quanto menor, mais exigente.
# Ajuste nos testes.
LIMIT = 0.12


def normalize(rgb):
  r, g, b = rgb

  total = r + g + b

  if total == 0:
    return (0.0, 0.0, 0.0)

  return (
    r / total,
    g / total,
    b / total,
  )


def distance(a, b):
  return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


# Normaliza todas as cores apenas uma vez
NORMALIZED_COLORS = {name: normalize(rgb) for name, rgb in COLORS.items()}


def classify(rgb):
  rgb = normalize(rgb)

  best_name = None
  best_distance = float("inf")

  for name, reference in NORMALIZED_COLORS.items():
    d = distance(rgb, reference)

    if d < best_distance:
      best_distance = d
      best_name = name

  if best_distance > LIMIT:
    return "unknown"

  return best_name


class RgbDetector:
  def __init__(self, port):
    self._sensor = ColorSensor(port)

  def raw_color(self):
    """Retorna a classificacao imediata sem confirmacao, util para debug"""
    return classify(self._sensor.rgb())
