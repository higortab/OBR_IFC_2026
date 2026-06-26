from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
 
from mapa import Mapa
from movimento import Movimento
from navegacao import Navegacao
from resgate import Resgate
 
# ------------------------
 
ev3 = EV3Brick()
 
motorE = Motor(Port.B)
motorD = Motor(Port.A)
 
robot = DriveBase(motorE, motorD, 56, 114)
 
ultra = UltrasonicSensor(Port.S2)
cor   = ColorSensor(Port.S1)
 
# ------------------------
 
mapa = Mapa()
mov  = Movimento(robot)
nav  = Navegacao(robot, ultra, cor, mapa, mov)
res  = Resgate(robot, ultra, cor, mapa, mov)
 
# ------------------------
# FASE 1 — Mapeamento
# ------------------------
 
nav.mapear()
nav.zigzag()
 
print("Mapeamento concluido!")
print("Bolinhas:", mapa.bolinhas)
print("Zona verde:", mapa.zona_verde)
print("Zona vermelha:", mapa.zona_vermelha)
 
# ------------------------
# FASE 2 — Resgate
# ------------------------
 
res.executar(nav)
 