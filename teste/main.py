#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Color, Direction, Button
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase

# Inicializa o brick
ev3 = EV3Brick()

# Configuração dos motores
motor_esquerdo = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.A, Direction.CLOCKWISE)

# Configuração do robô (ajuste conforme seu robô)
DIAMETRO_RODA = 56  # mm
DISTANCIA_ENTRE_RODAS = 120  # mm
robo = DriveBase(motor_esquerdo, motor_direito, DIAMETRO_RODA, DISTANCIA_ENTRE_RODAS)

# Configuração dos sensores de cor
sensor_esquerdo = ColorSensor(Port.S3)
sensor_direito = ColorSensor(Port.S4)
sensor_meio = ColorSensor(Port.S1)  # Recuado para trás

# Configuração do sensor ultrassônico
sensor_ultrasonico = UltrasonicSensor(Port.S2)

# Constantes para detecção de linha
LIMIAR_LINHA = 20  # Ajuste conforme calibração
VELOCIDADE_BASE = 150  # mm/s
GANHO_PROPORTIONAL = 1.2
VELOCIDADE_MINIMA = 50  # Velocidade mínima para manter o robô em movimento

# Variáveis globais
tentativas = 0
checkpoints_atingidos = 0

def ler_sensores():
    """Retorna os valores dos três sensores de cor."""
    return {
        'esquerdo': sensor_esquerdo.reflection(),
        'meio': sensor_meio.reflection(),
        'direito': sensor_direito.reflection()
    }

def detectar_linha(reflexao):
    """Retorna True se o sensor estiver sobre a linha preta."""
    return reflexao < LIMIAR_LINHA

def seguir_linha(erro_anterior=0):
    """Controle PID simples para seguir a linha."""
    # Lê os sensores laterais
    esq = sensor_esquerdo.reflection()
    dir = sensor_direito.reflection()
    
    # Calcula o erro (diferença entre os sensores)
    erro = esq - dir
    erro_corrigido = erro * GANHO_PROPORTIONAL
    
    # Aplica a correção
    velocidade_esq = VELOCIDADE_BASE - erro_corrigido
    velocidade_dir = VELOCIDADE_BASE + erro_corrigido
    
    # Limita a velocidade
    velocidade_esq = max(VELOCIDADE_MINIMA, min(300, velocidade_esq))
    velocidade_dir = max(VELOCIDADE_MINIMA, min(300, velocidade_dir))
    
    # Move o robô
    motor_esquerdo.run(velocidade_esq)
    motor_direito.run(velocidade_dir)
    
    return erro

def detectar_intersecao():
    """Detecta quando o sensor do meio encontra a linha."""
    return detectar_linha(sensor_meio.reflection())

def detectar_obstaculo():
    """Detecta obstáculo com o sensor ultrassônico."""
    try:
        distancia = sensor_ultrasonico.distance()
        return distancia is not None and distancia < 150  # 15 cm
    except:
        return False

def desviar_obstaculo():
    """Desvia do obstáculo e retorna à linha."""
    ev3.screen.clear()
    ev3.screen.print("Obstaculo!")
    
    # Para o robô
    robo.stop()
    wait(500)
    
    # Tenta desviar para a direita primeiro
    robo.straight(30)  # Avança um pouco
    robo.turn(-60)  # Gira 60° para a direita
    robo.straight(120)  # Avança
    robo.turn(60)  # Gira de volta para a esquerda
    robo.straight(80)  # Avança para tentar encontrar a linha
    robo.turn(60)  # Gira mais para a esquerda
    robo.straight(100)  # Avança
    robo.turn(-60)  # Gira de volta
    
    # Verifica se encontrou a linha
    if not detectar_linha(sensor_esquerdo.reflection()) and not detectar_linha(sensor_direito.reflection()):
        # Se não encontrou, tenta o outro lado
        robo.turn(-180)
        robo.straight(30)
        robo.turn(60)
        robo.straight(120)
        robo.turn(-60)
        robo.straight(80)
        robo.turn(-60)
        robo.straight(100)
        robo.turn(60)
    
    return True

def passar_gap():
    """
    Detecta e supera gaps.
    O gap é identificado quando os dois sensores laterais perdem a linha.
    """
    esq = sensor_esquerdo.reflection()
    dir = sensor_direito.reflection()
    
    if esq > LIMIAR_LINHA and dir > LIMIAR_LINHA:
        # Perdeu a linha, provavelmente um gap
        ev3.screen.clear()
        ev3.screen.print("Gap!")
        
        # Mantém a direção por um curto período para atravessar
        robo.straight(50)
        wait(300)
        
        # Procura a linha novamente
        contador = 0
        while contador < 20:
            robo.straight(10)
            esq = sensor_esquerdo.reflection()
            dir = sensor_direito.reflection()
            if esq < LIMIAR_LINHA or dir < LIMIAR_LINHA:
                return True
            contador += 1
            wait(50)
        
        return True
    return False

def passar_lombada():
    """Detecta e passa lombadas."""
    # Lombada é detectada como uma mudança brusca na reflexão
    esq = sensor_esquerdo.reflection()
    dir = sensor_direito.reflection()
    
    # Se a linha parece "mais larga" (ambos os sensores detectam linha simultaneamente)
    if esq < LIMIAR_LINHA and dir < LIMIAR_LINHA:
        ev3.screen.clear()
        ev3.screen.print("Lombada!")
        # Apenas continua
        return True
    return False

def detectar_beco_sem_saida():
    """Detecta beco sem saída (linha que vira para trás)."""
    # Detecta quando os dois sensores laterais estão na linha
    esq = sensor_esquerdo.reflection()
    dir = sensor_direito.reflection()
    meio = sensor_meio.reflection()
    
    # Se está no meio da linha e há linha à frente
    if esq < LIMIAR_LINHA and dir < LIMIAR_LINHA and meio < LIMIAR_LINHA:
        ev3.screen.clear()
        ev3.screen.print("Beco sem saida!")
        
        # Tenta seguir a linha contínua
        robo.straight(50)
        
        # Verifica se é realmente um beco (linha para trás)
        if sensor_esquerdo.reflection() > LIMIAR_LINHA and sensor_direito.reflection() > LIMIAR_LINHA:
            # É um beco, vira 180°
            robo.turn(180)
            return True
    return False

def detectar_intersecao_com_marcacao():
    """Detecta interseção com marcação verde."""
    # Verifica se há uma marcação verde (você precisa implementar a detecção de cor)
    # Por enquanto, vamos detectar como uma interseção normal
    return detectar_intersecao()

def verificar_checkpoint():
    """Verifica se atingiu um checkpoint."""
    # Atingiu checkpoint quando passou por um número de ladrilhos
    # Você pode implementar a lógica específica de checkpoint aqui
    return False

def verificar_fita_prateada():
    """Verifica se chegou à entrada da sala de resgate (fita prateada)."""
    # A fita prateada reflete mais que a linha preta
    esq = sensor_esquerdo.reflection()
    dir = sensor_direito.reflection()
    
    # Valores altos indicam superfície prateada
    return esq > 80 and dir > 80

def executar_falha_progresso():
    """Executa o procedimento de falha de progresso."""
    global tentativas
    tentativas += 1
    ev3.screen.clear()
    ev3.screen.print("Falha " + str(tentativas))
    
    # Para o robô
    robo.stop()
    wait(1000)
    
    # Aqui você pode implementar a lógica para voltar ao último checkpoint
    # Por enquanto, apenas aguarda e continua
    return True

def navegar_ate_sala_resgate():
    """
    Função principal de navegação até a sala de resgate.
    Retorna True se chegou à sala de resgate.
    """
    global tentativas, checkpoints_atingidos
    
    ev3.screen.clear()
    ev3.screen.print("Navegando...")
    
    tempo_inicio = StopWatch()
    tempo_parado = StopWatch()
    em_intersecao = False  # Variável local inicializada aqui
    erro_anterior = 0
    
    while tempo_inicio.time() < 300000:  # 5 minutos
        try:
            # Lê os sensores
            esq = sensor_esquerdo.reflection()
            dir = sensor_direito.reflection()
            meio = sensor_meio.reflection()
            
            # Detecta e desvia de obstáculo (prioridade máxima)
            if detectar_obstaculo():
                if desviar_obstaculo():
                    tempo_parado.reset()
                    continue
                else:
                    # Não conseguiu desviar, tenta novamente
                    continue
            
            # Detecta gap
            if esq > LIMIAR_LINHA and dir > LIMIAR_LINHA:
                if passar_gap():
                    tempo_parado.reset()
                    continue
            
            # Detecta lombada
            if esq < LIMIAR_LINHA and dir < LIMIAR_LINHA and meio > LIMIAR_LINHA:
                if passar_lombada():
                    tempo_parado.reset()
                    continue
            
            # Detecta beco sem saída
            if esq < LIMIAR_LINHA and dir < LIMIAR_LINHA and meio < LIMIAR_LINHA:
                if detectar_beco_sem_saida():
                    tempo_parado.reset()
                    continue
            
            # Detecta interseção
            if meio < LIMIAR_LINHA:
                if not em_intersecao:
                    em_intersecao = True
                    ev3.screen.clear()
                    ev3.screen.print("Intersecao!")
                    # Decide qual caminho seguir (reto por padrão)
                    # Você pode adicionar lógica para detectar marcação verde
                    tempo_parado.reset()
            else:
                em_intersecao = False
            
            # Segue a linha normalmente
            erro_anterior = seguir_linha(erro_anterior)
            
            # Verifica se chegou à sala de resgate
            if verificar_fita_prateada():
                ev3.screen.clear()
                ev3.screen.print("Sala Resgate!")
                robo.stop()
                return True
            
            # Verifica se o robô está parado há muito tempo (falha de progresso)
            if tempo_parado.time() > 10000:  # 10 segundos
                executar_falha_progresso()
                tempo_parado.reset()
            
            wait(10)
            
        except Exception as e:
            ev3.screen.clear()
            ev3.screen.print("Erro: " + str(e))
            wait(1000)
            continue
    
    # Tempo esgotado
    ev3.screen.clear()
    ev3.screen.print("Tempo esgotado!")
    return False

def main():
    """Função principal do programa."""
    ev3.screen.clear()
    ev3.screen.print("Iniciando...")
    
    # Pequena pausa inicial
    wait(2000)
    
    # Inicia navegação
    chegou = navegar_ate_sala_resgate()
    
    if chegou:
        ev3.screen.clear()
        ev3.screen.print("Sala Resgate OK!")
    else:
        ev3.screen.clear()
        ev3.screen.print("Falha!")
    
    # Loop infinito para manter o programa rodando
    while True:
        wait(100)

if __name__ == "__main__":
    main()