#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import UltrasonicSensor, Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait

ev3 = EV3Brick()
sensor = UltrasonicSensor(Port.S2)

motors = {
  "left": Motor(Port.C, Direction.COUNTERCLOCKWISE),
  "right": Motor(Port.A, Direction.COUNTERCLOCKWISE),
}

anterior = sensor.distance()

motors["left"].run(150)
motors["right"].run(150)

while True:
  atual = sensor.distance()
  delta = atual - anterior

  ev3.screen.clear()
  ev3.screen.draw_text(0, 0, "Dist: {} mm".format(atual))
  ev3.screen.draw_text(0, 25, "Delta: {} mm".format(delta))

  print("Dist:", atual, "Delta:", delta)

  anterior = atual

  wait(100)

# #!/usr/bin/env pybricks-micropython
# from pybricks.hubs import EV3Brick
# from pybricks.tools import wait

# from config.motors import Motors, degrees_to_mm
# from config.reflection_sensors import ReflectionDetector
# from config.rgb_sensor import RgbDetector
# # from config.ultrasonic import UltrasonicDetector

# # Declara variaveis
# ev3 = EV3Brick()

# motors = Motors()

# reflection = ReflectionDetector()
# rgb = RgbDetector()
# # ultrasonic = UltrasonicDetector()

# # Ações iniciais
# ev3.screen.clear()
# motors.move_forward()

# # Loop
# while True:
#   # Varre sensores
#   # center = rgb.update(degrees_to_mm(motors.get_average_angle()))
#   # if not center:
#   #   center = rgb.raw_color()

#   # left, right = reflection.update()


#   wait(50)
