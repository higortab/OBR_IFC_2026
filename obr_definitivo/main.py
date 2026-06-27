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
motor_esquerdo = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)

# ========== CONSTANTES AJUSTADAS PARA CURVAS ==========
BASE_SPEED = 150          # Reduzido para fazer curvas (era 200)
KP = 2.5                  # Aumentado para curvas mais fechadas (era 1.5)
PONTO_MEDIO = 50
VELOCIDADE_MINIMA = 50    # Velocidade mínima para não parar nas curvas

# ========== VARIÁVEIS PARA CONTROLE ==========
erro_anterior = 0
derivada = 0

# ========== LOOP PRINCIPAL ==========
while True:
    # Leitura dos sensores
    left = sensor_esquerdo.reflection()
    meio = sensor_meio.reflection()
    right = sensor_direito.reflection()
    
    # DETECTA CURVA (quando os sensores laterais veem preto)
    curva_detectada = False
    if left < 30 and right > 70:
        # Curva à esquerda
        curva_detectada = True
        ev3.screen.draw_text(0, 90, "CURVA ESQUERDA!")
    elif right < 30 and left > 70:
        # Curva à direita
        curva_detectada = True
        ev3.screen.draw_text(0, 90, "CURVA DIREITA!")
    
    # Calcula o erro
    erro = meio - PONTO_MEDIO
    
    # Ajusta KP para curvas (mais agressivo)
    if curva_detectada:
        kp_curva = KP * 1.5  # Aumenta ainda mais na curva
        velocidade_curva = BASE_SPEED * 0.7  # Reduz velocidade na curva
    else:
        kp_curva = KP
        velocidade_curva = BASE_SPEED
    
    # Correção proporcional
    correcao = kp_curva * erro
    
    # Velocidades dos motores
    vel_e = velocidade_curva + correcao
    vel_d = velocidade_curva - correcao
    
    # GARANTE QUE OS MOTORES NÃO PAREM NAS CURVAS
    # Se um motor for negativo, ele pode parar - ajustamos isso
    if vel_e < VELOCIDADE_MINIMA and vel_e > 0:
        vel_e = VELOCIDADE_MINIMA
    if vel_d < VELOCIDADE_MINIMA and vel_d > 0:
        vel_d = VELOCIDADE_MINIMA
    
    # Limita as velocidades máximas
    if vel_e > 500:
        vel_e = 500
    if vel_d > 500:
        vel_d = 500
    
    # Aplica as velocidades
    motor_esquerdo.run(vel_e)
    motor_direito.run(vel_d)
    
    # Mostra os valores no visor
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "E: " + str(left))
    ev3.screen.draw_text(0, 40, "M: " + str(meio))
    ev3.screen.draw_text(0, 60, "D: " + str(right))
    ev3.screen.draw_text(0, 80, "Correcao: " + str(correcao))
    
    if curva_detectada:
        ev3.screen.draw_text(0, 110, ">>> CURVA <<<")
    
    wait(50)