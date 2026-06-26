#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port

ultra = UltrasonicSensor(Port.S2)

# Configuração
START_DISTANCE = 180  # começa a suspeitar
CONFIRM_DISTANCE = 70  # obstáculo já está bem próximo
MAX_CONFIRM_MM = 80  # deve confirmar em até 80 mm percorridos


class UltrasonicDetector:
  def __init__(self):
    self.reset()

  def reset(self):
    self._state = "IDLE"
    self._start_distance_mm = 0
    self._last_reading = None

  def update(self, traveled_mm):
    """
    traveled_mm = distância total percorrida pelo robô.
    Retorna:
        None
        "OBSTACLE"
    """

    reading = ultra.distance()

    # ---------- Estado IDLE ----------

    if self._state == "IDLE":
      if reading <= START_DISTANCE:
        self._state = "CHECKING"
        self._start_distance_mm = traveled_mm
        self._last_reading = reading

      return None

    # ---------- Estado CHECKING ----------

    traveled = traveled_mm - self._start_distance_mm

    # Confirmou obstáculo:
    # continua aproximando do objeto
    if reading <= CONFIRM_DISTANCE and reading <= self._last_reading:
      self.reset()
      return "OBSTACLE"

    # Sumiu rapidamente
    # provavelmente lombada
    if reading > START_DISTANCE:
      self.reset()
      return None

    # Ficou muito tempo praticamente igual
    # provavelmente rampa
    if traveled >= MAX_CONFIRM_MM:
      self.reset()
      return None

    self._last_reading = reading

    return None

  def raw(self):
    return ultra.distance()
