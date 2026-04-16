#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait

# Configuração
sensor_cor = ColorSensor(Port.S1)

# Loop principal
while True:
    # Lê a intensidade da luz (0-100)
    refletancia = sensor_cor.reflection()
    
    # Exemplo simples: se for menor que 30, é preto (linha)
    if refletancia < 30:
        print("Linha preta detectada")
    else:
        print("Fundo branco/claro")
        
    wait(10) # Pequena pausa para o processador

