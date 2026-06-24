#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait

ev3 = EV3Brick()

# ========== SENSORES ==========
sensor_esquerdo = ColorSensor(Port.S3)
sensor_meio = ColorSensor(Port.S1)
sensor_direito = ColorSensor(Port.S4)

# ========== MOTORES ==========
# Motores invertidos
motor_esquerdo = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.A, Direction.COUNTERCLOCKWISE)

# ========== CONSTANTES ==========
BASE_SPEED = 200      # Velocidade base
KP = 1.5              # Ganho proporcional
PONTO_MEDIO = 50      # Ponto médio (preto=0, branco=100)

# ========== LOOP PRINCIPAL ==========
while True:
    # Leitura dos sensores
    left = sensor_esquerdo.reflection()
    meio = sensor_meio.reflection()
    right = sensor_direito.reflection()
    
    # Calcula o erro (quanto o sensor do meio está longe do ponto médio)
    erro = meio - PONTO_MEDIO
    
    # Correção proporcional
    correcao = KP * erro
    
    # Velocidades dos motores
    vel_e = BASE_SPEED + correcao
    vel_d = BASE_SPEED - correcao
    
    # Limita as velocidades entre 0 e 500
    if vel_e < 0:
        vel_e = 0
    if vel_e > 500:
        vel_e = 500
    if vel_d < 0:
        vel_d = 0
    if vel_d > 500:
        vel_d = 500
    
    # Aplica as velocidades
    motor_esquerdo.run(vel_e)
    motor_direito.run(vel_d)
    
    # Mostra os valores no visor
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "E: " + str(left))
    ev3.screen.draw_text(0, 50, "M: " + str(meio))
    ev3.screen.draw_text(0, 80, "D: " + str(right))
    
    # Pequeno delay para não sobrecarregar
    wait(50)