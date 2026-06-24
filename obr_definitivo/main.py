#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.robotics import DriveBase

ev3 = EV3Brick()

# Sensores
sensor_esquerdo = ColorSensor(Port.S3)
sensor_meio = ColorSensor(Port.S1)
sensor_direito = ColorSensor(Port.S4)


sensor_distancia = UltrasonicSensor(Port.S2)

# Motores
motor_esquerdo = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.A, Direction.COUNTERCLOCKWISE)

# DriveBase para movimentos mais fáceis
robo = DriveBase(motor_esquerdo, motor_direito, 56, 114)  # Ajuste diâmetro e distância entre rodas

# ========== CONSTANTES ==========
BASE_SPEED = 200
TURN_SPEED = 100
KP = 1.5
LIMIAR_OBSTACULO = 150  # mm - distância para detectar obstáculo

# ========== FUNÇÃO PARA SEGUIR LINHA ==========
def seguir_linha(velocidade_base=BASE_SPEED):
    """Segue a linha usando PID (usa sua calibração)"""
    left = sensor_esquerdo.reflection()
    meio = sensor_meio.reflection()
    right = sensor_direito.reflection()
    
    # Usa os valores calibrados se disponíveis
    try:
        from util_sensores import ler_todos_sensores
        left, meio, right = ler_todos_sensores(sensor_esquerdo, sensor_meio, sensor_direito)
    except:
        pass  # Usa valores brutos se não tiver calibração
    
    # Ponto médio (ajuste conforme sua calibração)
    ponto_medio = 50
    erro = meio - ponto_medio
    
    # Correção proporcional
    correcao = KP * erro
    
    # Velocidades
    vel_e = velocidade_base + correcao
    vel_d = velocidade_base - correcao
    
    # Limita velocidades
    if vel_e < 0: vel_e = 0
    if vel_e > 500: vel_e = 500
    if vel_d < 0: vel_d = 0
    if vel_d > 500: vel_d = 500
    
    motor_esquerdo.run(vel_e)
    motor_direito.run(vel_d)
    
    return left, meio, right

# ========== FUNÇÕES PARA TRANSPOR PERIGOS ==========

def transpor_obstaculo():
    """Desvia de um obstáculo fixo na linha (20 pontos)"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "OBSTACULO DETECTADO")
    
    # Para o robô
    motor_esquerdo.stop()
    motor_direito.stop()
    wait(500)
    
    # 1. Desvia para a direita
    motor_esquerdo.run(TURN_SPEED)
    motor_direito.run(-TURN_SPEED)
    wait(600)  # Ajuste conforme o tamanho do robô
    
    # 2. Anda reto contornando
    motor_esquerdo.run(BASE_SPEED)
    motor_direito.run(BASE_SPEED)
    wait(800)
    
    # 3. Volta para a linha (vira à esquerda)
    motor_esquerdo.run(-TURN_SPEED)
    motor_direito.run(TURN_SPEED)
    wait(600)
    
    # 4. Procura a linha
    while sensor_meio.reflection() > 60:  # Enquanto não achar a linha preta
        motor_esquerdo.run(50)
        motor_direito.run(50)
        wait(50)
    
    ev3.screen.draw_text(0, 50, "OBSTACULO SUPERADO!")
    wait(500)

def transpor_gap():
    """Atravessa uma lacuna na linha (10 pontos)"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "GAP DETECTADO")
    
    # Mantém velocidade constante para atravessar
    motor_esquerdo.run(BASE_SPEED)
    motor_direito.run(BASE_SPEED)
    wait(1000)  # Ajuste conforme o tamanho do gap (máx 15cm)
    
    # Verifica se ainda está na linha
    if sensor_meio.reflection() > 50:
        # Se perdeu, tenta achar a linha
        motor_esquerdo.run(100)
        motor_direito.run(100)
        wait(500)
    
    ev3.screen.draw_text(0, 50, "GAP SUPERADO!")

def transpor_rampa():
    """Sobe ou desce uma rampa (10 pontos por ladrilho)"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "RAMPA DETECTADA")
    
    # Aumenta velocidade e potência para subir
    motor_esquerdo.run(300)
    motor_direito.run(300)
    wait(1500)  # Ajuste conforme tamanho da rampa
    
    # Volta à velocidade normal
    motor_esquerdo.run(BASE_SPEED)
    motor_direito.run(BASE_SPEED)
    wait(500)
    
    ev3.screen.draw_text(0, 50, "RAMPA SUPERADA!")

def transpor_gangorra():
    """Atravessa uma gangorra (20 pontos)"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "GANGORRA DETECTADA")
    
    # Abordagem: ir devagar para equilibrar
    motor_esquerdo.run(100)
    motor_direito.run(100)
    wait(2000)  # Tempo para atravessar
    
    # Verifica se está equilibrado
    # (O robô pode usar giroscópio aqui se tiver)
    
    ev3.screen.draw_text(0, 50, "GANGORRA SUPERADA!")

def transpor_lombada():
    """Passa por redutores de velocidade (10 pontos por ladrilho)"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "LOMBADA DETECTADA")
    
    # Reduz velocidade para passar
    motor_esquerdo.run(150)
    motor_direito.run(150)
    wait(500)
    
    # Volta à velocidade normal
    motor_esquerdo.run(BASE_SPEED)
    motor_direito.run(BASE_SPEED)
    
    ev3.screen.draw_text(0, 50, "LOMBADA SUPERADA!")

def identificar_intersecao():
    """
    Identifica se é interseção com marcação verde, sem marcação ou beco sem saída
    Retorna: 'esquerda', 'direita', 'reto', 'retorno'
    """
    # Lê os sensores
    left = sensor_esquerdo.reflection()
    meio = sensor_meio.reflection()
    right = sensor_direito.reflection()
    
    # Se todos detectam preto, é uma interseção
    if left < 30 and meio < 30 and right < 30:
        ev3.screen.clear()
        ev3.screen.draw_text(0, 20, "INTERSECAO!")
        
        # Verifica marcador verde (precisa de sensor de cor adicional)
        # Por enquanto, vamos considerar que se tiver marcador, é 'esquerda'
        # Ajuste conforme seu robô detecta a cor verde
        
        # Padrão: virar à esquerda
        return 'esquerda'
    
    return None

def transpor_intersecao(direcao):
    """Segue a direção indicada na interseção"""
    ev3.screen.draw_text(0, 40, "VIRANDO: " + direcao.upper())
    
    if direcao == 'esquerda':
        motor_esquerdo.run(-TURN_SPEED)
        motor_direito.run(TURN_SPEED)
        wait(800)
        
    elif direcao == 'direita':
        motor_esquerdo.run(TURN_SPEED)
        motor_direito.run(-TURN_SPEED)
        wait(800)
        
    elif direcao == 'retorno':
        motor_esquerdo.run(-TURN_SPEED)
        motor_direito.run(TURN_SPEED)
        wait(1600)  # Curva mais longa para fazer o retorno
        
    else:  # reto
        motor_esquerdo.run(BASE_SPEED)
        motor_direito.run(BASE_SPEED)
        wait(500)
    
    ev3.screen.draw_text(0, 60, "INTERSECAO SUPERADA!")
    wait(500)

def transpor_passagem():
    """Atravessa uma passagem laranja (0 pontos, mas precisa superar)"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "PASSAGEM DETECTADA")
    
    # Passagem é só uma estrutura, anda reto
    motor_esquerdo.run(BASE_SPEED)
    motor_direito.run(BASE_SPEED)
    wait(1000)
    
    ev3.screen.draw_text(0, 50, "PASSAGEM SUPERADA!")

# ========== DETECTOR DE PERIGOS ==========

def detectar_perigo():
    """
    Detecta qual perigo está à frente do robô
    Retorna: 'obstaculo', 'gap', 'rampa', 'gangorra', 'lombada', 'intersecao', 'passagem', 'nenhum'
    """
    # Detecção de obstáculo por ultrassom
    distancia = sensor_distancia.distance()
    if distancia < LIMIAR_OBSTACULO and distancia > 50:
        # Verifica se não é uma rampa ou passagem
        return 'obstaculo'
    
    # Detecção de gap - quando todos os sensores veem branco
    left = sensor_esquerdo.reflection()
    meio = sensor_meio.reflection()
    right = sensor_direito.reflection()
    
    if left > 70 and meio > 70 and right > 70:
        # Verifica se é um gap (todos viram branco de repente)
        return 'gap'
    
    # Detecção de interseção - todos veem preto
    if left < 30 and meio < 30 and right < 30:
        return 'intersecao'
    
    # Detecção de lombada - o robô trepida (usar giroscópio se tiver)
    # Por enquanto, só detecta pela leitura dos sensores
    if meio < 20 and left > 50 and right > 50:
        return 'lombada'
    
    return 'nenhum'

# ========== LOOP PRINCIPAL ==========

def main():
    """Loop principal com detecção de perigos"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "INICIANDO RESGATE")
    
    # Flag para controle de progresso
    perigos_superados = 0
    
    while True:
        # 1. Segue a linha normalmente
        seguir_linha(BASE_SPEED)
        
        # 2. Verifica se detectou algum perigo
        perigo = detectar_perigo()
        
        if perigo != 'nenhum':
            # Para o robô antes de agir
            motor_esquerdo.stop()
            motor_direito.stop()
            wait(200)
            
            # 3. Executa a ação para o perigo detectado
            if perigo == 'obstaculo':
                transpor_obstaculo()
                perigos_superados += 20
                
            elif perigo == 'gap':
                transpor_gap()
                perigos_superados += 10
                
            elif perigo == 'rampa':
                transpor_rampa()
                perigos_superados += 10
                
            elif perigo == 'gangorra':
                transpor_gangorra()
                perigos_superados += 20
                
            elif perigo == 'lombada':
                transpor_lombada()ectar_perigo()
        
        if perigo != 'nenhum':
            # Para o robô antes de agir
            motor_esquerdo.stop()
            motor_direito.stop()
            wait(200)
            
            # 3. Executa a ação para o perigo detectado
            if perigo == 'obstaculo':
                transpor_obstaculo()
                peri
                perigos_superados += 10
                
            elif perigo == 'intersecao':
                direcao = identificar_intersecao()
                if direcao:
                    transpor_intersecao(direcao)
                    perigos_superados += 10
                
            elif perigo == 'passagem':
                transpor_passagem()
                # Não pontua
            
            # Mostra pontuação parcial
            ev3.screen.clear()
            ev3.screen.draw_text(0, 10, "PONTOS: " + str(perigos_superados))
            ev3.screen.draw_text(0, 30, "PERIGO: " + perigo.upper())
            wait(500)
        
        # Pequeno delay para não sobrecarregar
        wait(50)

# Executa o programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Para os motores ao interromper
        motor_esquerdo.stop()
        motor_direito.stop()
        ev3.screen.clear()
        ev3.screen.draw_text(0, 20, "PROGRAMA PARADO")