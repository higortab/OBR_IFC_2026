# ============================================================
# config.py — Todas as variáveis ajustáveis do robô OBR 2026
# ============================================================

# --- Portas dos motores ---
MOTOR_ESQUERDO_PORT = 'A'
MOTOR_DIREITO_PORT  = 'C'

# --- Portas dos sensores ---
SENSOR_COR_ESQUERDO_PORT = 3   # Refletância apenas
SENSOR_COR_DIREITO_PORT  = 4   # Refletância apenas
SENSOR_COR_MEIO_PORT     = 1   # RGB completo
SENSOR_ULTRASSONICO_PORT = 2

# --- Inversão dos motores ---
# True = inverte a direção do motor (motores montados invertidos)
MOTOR_ESQUERDO_INVERTIDO = True
MOTOR_DIREITO_INVERTIDO  = True

# --- Calibração dos sensores laterais (refletância 0-100) ---
CALIBRACAO = {
    'esquerdo': {'preto': 0, 'branco': 100, 'medio': 50},
    'direito':  {'preto': 0, 'branco': 100, 'medio': 50},
}

# Limiar abaixo do qual considera "preto" (linha)
LIMIAR_PRETO = 30
# Limiar acima do qual considera "branco" (fundo)
LIMIAR_BRANCO = 70

# --- Thresholds RGB do sensor do meio ---
# Usado para detectar verde (fita marcadora de interseção)
RGB_VERDE_MIN_G   = 80    # canal G mínimo para ser verde
RGB_VERDE_MAX_R   = 80    # canal R máximo para ser verde
RGB_VERDE_MAX_B   = 80    # canal B máximo para ser verde
# Usado para detectar preto (linha)
RGB_PRETO_MAX     = 40    # todos os canais abaixo disso = preto
# Usado para detectar branco (fundo)
RGB_BRANCO_MIN    = 150   # todos os canais acima disso = branco

# --- Velocidade base e limites ---
VELOCIDADE_BASE   = 200   # -1000 a 1000 (EV3 MicroPython)
VELOCIDADE_MINIMA = 80    # velocidade mínima para curvas
VELOCIDADE_MAX    = 400

# --- PID do segue linha ---
KP = 1.2    # Proporcional  — aumentar = reação mais brusca
KI = 0.02   # Integral      — aumentar = corrige desvio acumulado
KD = 0.8    # Derivativo    — aumentar = suaviza oscilações

# --- Geometria do robô (em mm) ---
LARGURA_ROBO_MM      = 195   # de roda a roda
COMPRIMENTO_ROBO_MM  = 195   # frente para trás

# --- Distância do sensor do meio aos laterais (em mm) ---
# Altere aqui se reposicionar o sensor
DISTANCIA_MEIO_LATERAIS_MM = 75

# --- Fita verde de interseção (manual OBR: 2,5 cm x 2,5 cm) ---
FITA_VERDE_LADO_MM = 25

# --- Ângulo de verificação diagonal do sensor do meio ---
# Calculado: arctan(largura/2 / distancia_meio) = arctan(97.5/75) ≈ 52°
# Altere se a fita aparecer numa posição diferente durante os testes
ANGULO_VERIFICACAO_DIAGONAL_GRAUS = 52

# Avanço após a verificação diagonal antes de iniciar a curva (mm)
AVANCO_POS_VERIFICACAO_MM = 20

# --- Obstáculo ---
# Distância em mm para considerar obstáculo detectado
DISTANCIA_OBSTACULO_MM        = 30   # 3 cm
# Dimensão do obstáculo (manual: min 3x5 cm, max 10x25 cm — usamos 6x6 cm)
OBSTACULO_LARGURA_MM          = 60
OBSTACULO_COMPRIMENTO_MM      = 60
# Ré inicial ao detectar obstáculo (mm)
RE_OBSTACULO_MM               = 20   # 2 cm
# Avanço lateral para passar ao lado do obstáculo (mm)
# = metade da largura do robô + metade do obstáculo + margem
# = 97,5 + 30 + 20 = 147,5 → arredondado
AVANCO_LATERAL_OBSTACULO_MM   = 60   # andar reto antes de virar
# Ângulo de desvio (graus) — vira à esquerda para contornar pelo lado direito
ANGULO_DESVIO_OBSTACULO_GRAUS = 75
# Velocidade reduzida durante manobra de desvio
VELOCIDADE_DESVIO             = 150

# --- Curva de 90° sem marcação ---
# Após detectar interseção (ambos laterais veem preto cruzando),
# o robô avança para o sensor do meio chegar ao ponto e verificar.
# Se a linha some (curva de 90°), tenta avançar antes de girar.
AVANCO_VERIFICACAO_CURVA_MM   = 150  # 15 cm
# Velocidade de busca da linha após curva
VELOCIDADE_BUSCA_LINHA        = 120

# --- Beco sem saída ---
# Tempo máximo (ms) entre a detecção do 1º e 2º verde para
# considerar beco sem saída (dois verdes em sequência)
INTERVALO_DUPLO_VERDE_MS      = 800

# --- Gap (lacuna na linha) ---
# Tempo máximo (ms) que os sensores podem ficar sem ver preto
# antes de considerar gap (e não falha de progresso)
TIMEOUT_GAP_MS                = 500

# --- Timeouts gerais ---
TIMEOUT_BUSCA_LINHA_MS        = 3000  # tempo máximo buscando linha