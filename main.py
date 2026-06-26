#!/usr/bin/env pybricks-micropython

from pybricks.tools import wait

from config.motors import motors, BASE_SPEED, TURN_SPEED
from config.reflection_sensors import ReflectionDetector
from config.rgb_sensor import RgbDetector
from config.motors import average_angle, degrees_to_mm

reflection = ReflectionDetector()
rgb = RgbDetector()

while True:
  # Distância percorrida (para confirmar a cor)
  distance = degrees_to_mm(average_angle())

  # Detecta verde pelo sensor central
  color = rgb.update(distance)

  if color == "GREEN":
    motors["left"].stop()
    motors["right"].stop()
    print("VERDE")
    break

  left, right = reflection.update()

  # BLACK = 0
  # WHITE = 1

  if left == 0 and right == 0:
    # Os dois sensores sobre a linha
    motors["left"].run(BASE_SPEED)
    motors["right"].run(BASE_SPEED)

  elif left == 0:
    # Linha à esquerda
    motors["left"].run(BASE_SPEED - TURN_SPEED)
    motors["right"].run(BASE_SPEED + TURN_SPEED)

  elif right == 0:
    # Linha à direita
    motors["left"].run(BASE_SPEED + TURN_SPEED)
    motors["right"].run(BASE_SPEED - TURN_SPEED)

  else:
    # Nenhum sensor vê a linha.
    # Continua reto por enquanto.
    motors["left"].run(BASE_SPEED)
    motors["right"].run(BASE_SPEED)

  wait(10)
