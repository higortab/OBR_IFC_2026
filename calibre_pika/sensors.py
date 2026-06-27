# ============================================================
# sensors.py — Leituras dos sensores
# ============================================================

from pybricks.hubs        import EV3Brick
from pybricks.ev3devices  import (ColorSensor, UltrasonicSensor)
from pybricks.parameters  import Port

from config import (
    SENSOR_COR_ESQUERDO_PORT,
    SENSOR_COR_DIREITO_PORT,
    SENSOR_COR_MEIO_PORT,
    SENSOR_ULTRASSONICO_PORT,
    LIMIAR_PRETO,
    LIMIAR_BRANCO,
    RGB_VERDE_MIN_G,
    RGB_VERDE_MAX_R,
    RGB_VERDE_MAX_B,
    RGB_PRETO_MAX,
    RGB_BRANCO_MIN,
)

# --- Mapeamento de porta inteira para objeto Port ---
_PORT_MAP = {
    1: Port.S1,
    2: Port.S2,
    3: Port.S3,
    4: Port.S4,
}

# --- Instâncias dos sensores (inicializadas uma única vez) ---
_sensor_esquerdo     = ColorSensor(_PORT_MAP[SENSOR_COR_ESQUERDO_PORT])
_sensor_direito      = ColorSensor(_PORT_MAP[SENSOR_COR_DIREITO_PORT])
_sensor_meio         = ColorSensor(_PORT_MAP[SENSOR_COR_MEIO_PORT])
_sensor_ultrasonico  = UltrasonicSensor(_PORT_MAP[SENSOR_ULTRASSONICO_PORT])


# ============================================================
# Sensores laterais — refletância (0-100)
# ============================================================

def ler_esquerdo_raw() -> int:
    """Retorna valor bruto de refletância do sensor esquerdo (0-100)."""
    return _sensor_esquerdo.reflection()


def ler_direito_raw() -> int:
    """Retorna valor bruto de refletância do sensor direito (0-100)."""
    return _sensor_direito.reflection()


def esquerdo_na_linha() -> bool:
    """True se o sensor esquerdo estiver sobre a linha preta."""
    return ler_esquerdo_raw() < LIMIAR_PRETO


def direito_na_linha() -> bool:
    """True se o sensor direito estiver sobre a linha preta."""
    return ler_direito_raw() < LIMIAR_PRETO


def esquerdo_no_branco() -> bool:
    """True se o sensor esquerdo estiver sobre fundo branco."""
    return ler_esquerdo_raw() > LIMIAR_BRANCO


def direito_no_branco() -> bool:
    """True se o sensor direito estiver sobre fundo branco."""
    return ler_direito_raw() > LIMIAR_BRANCO


def erro_pid() -> float:
    """
    Calcula o erro para o controlador PID do segue linha.

    Convenção:
      - Negativo → robô desviou para a direita (deve corrigir para esquerda)
      - Positivo → robô desviou para a esquerda (deve corrigir para direita)
      - Zero     → robô está centralizado na linha

    Usa a diferença entre sensor esquerdo e direito normalizada para [-1, 1].
    """
    ve = ler_esquerdo_raw()
    vd = ler_direito_raw()
    # diferença: positivo = esquerdo lê mais branco (robô foi para a esquerda)
    return float(ve - vd) / 100.0


# ============================================================
# Sensor do meio — RGB completo
# ============================================================

def ler_meio_rgb() -> tuple:
    """
    Retorna tupla (R, G, B) do sensor central.
    Valores aproximados 0-255 dependendo da iluminação ambiente.
    """
    return _sensor_meio.rgb()


def meio_ve_verde() -> bool:
    """
    True se o sensor do meio detectar a fita verde de marcação.
    Critério: G alto, R e B abaixo dos limiares definidos em config.
    """
    r, g, b = ler_meio_rgb()
    return (g > RGB_VERDE_MIN_G) and (r < RGB_VERDE_MAX_R) and (b < RGB_VERDE_MAX_B)


def meio_ve_preto() -> bool:
    """True se o sensor do meio detectar linha preta."""
    r, g, b = ler_meio_rgb()
    return (r < RGB_PRETO_MAX) and (g < RGB_PRETO_MAX) and (b < RGB_PRETO_MAX)


def meio_ve_branco() -> bool:
    """True se o sensor do meio detectar fundo branco."""
    r, g, b = ler_meio_rgb()
    return (r > RGB_BRANCO_MIN) and (g > RGB_BRANCO_MIN) and (b > RGB_BRANCO_MIN)


# ============================================================
# Sensor ultrassônico
# ============================================================

def ler_distancia_mm() -> int:
    """
    Retorna a distância frontal em milímetros medida pelo sensor
    ultrassônico. Retorna 2550 se nenhum objeto for detectado.
    """
    d = _sensor_ultrasonico.distance()
    return d if d is not None else 2550


def obstaculo_detectado(distancia_limiar_mm: int) -> bool:
    """
    True se houver um objeto a menos de `distancia_limiar_mm` mm.

    Parâmetro:
        distancia_limiar_mm: distância em mm abaixo da qual
                             considera obstáculo (vem de config.DISTANCIA_OBSTACULO_MM)
    """
    return ler_distancia_mm() <= distancia_limiar_mm