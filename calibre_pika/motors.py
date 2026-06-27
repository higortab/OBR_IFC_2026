# ============================================================
# motors.py — Movimentos base do robô
# ============================================================

from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction

from config import (
    MOTOR_ESQUERDO_PORT,
    MOTOR_DIREITO_PORT,
    MOTOR_ESQUERDO_INVERTIDO,
    MOTOR_DIREITO_INVERTIDO,
    LARGURA_ROBO_MM,
    VELOCIDADE_BASE,
)
import math

# --- Mapeamento porta → objeto Port ---
_PORT_MAP = {
    'A': Port.A,
    'B': Port.B,
    'C': Port.C,
    'D': Port.D,
}

# --- Direção conforme inversão configurada ---
def _direcao(invertido: bool) -> Direction:
    return Direction.COUNTERCLOCKWISE if invertido else Direction.CLOCKWISE

# --- Instâncias dos motores ---
_motor_esq = Motor(
    _PORT_MAP[MOTOR_ESQUERDO_PORT],
    positive_direction=_direcao(MOTOR_ESQUERDO_INVERTIDO)
)
_motor_dir = Motor(
    _PORT_MAP[MOTOR_DIREITO_PORT],
    positive_direction=_direcao(MOTOR_DIREITO_INVERTIDO)
)

# Diâmetro estimado das rodas em mm (EV3 roda padrão = 56 mm)
# Ajuste se usar rodas diferentes
DIAMETRO_RODA_MM = 56.0
CIRCUNFERENCIA_RODA_MM = math.pi * DIAMETRO_RODA_MM  # ≈ 175.9 mm


# ============================================================
# Funções internas de conversão
# ============================================================

def _mm_para_graus(distancia_mm: float) -> float:
    """Converte distância linear (mm) em graus de rotação do motor."""
    return (distancia_mm / CIRCUNFERENCIA_RODA_MM) * 360.0


def _angulo_para_graus_motor(angulo_graus: float) -> float:
    """
    Converte ângulo de rotação do robô (graus) em graus de rotação
    de cada roda, considerando a largura entre rodas.
    """
    arco = (angulo_graus / 360.0) * math.pi * LARGURA_ROBO_MM
    return _mm_para_graus(arco)


# ============================================================
# Funções públicas de movimento
# ============================================================

def set_velocidade(vel_esq: int, vel_dir: int) -> None:
    """
    Define velocidade diretamente nos dois motores.
    Valores em graus/segundo (-1000 a 1000).
    """
    _motor_esq.run(vel_esq)
    _motor_dir.run(vel_dir)


def parar() -> None:
    """Para os dois motores (brake)."""
    _motor_esq.brake()
    _motor_dir.brake()


def andar_frente(velocidade: int = None) -> None:
    """Anda para frente com a velocidade configurada."""
    v = velocidade if velocidade is not None else VELOCIDADE_BASE
    set_velocidade(v, v)


def andar_re(velocidade: int = None) -> None:
    """Anda para trás com a velocidade configurada."""
    v = velocidade if velocidade is not None else VELOCIDADE_BASE
    set_velocidade(-v, -v)


def andar_distancia_mm(distancia_mm: float, velocidade: int = None) -> None:
    """
    Anda uma distância específica em mm e para.
    Positivo = frente, Negativo = ré.
    """
    v = velocidade if velocidade is not None else VELOCIDADE_BASE
    graus = _mm_para_graus(abs(distancia_mm))
    sinal = 1 if distancia_mm >= 0 else -1
    _motor_esq.run_angle(v, sinal * graus, wait=False)
    _motor_dir.run_angle(v, sinal * graus, wait=True)
    parar()


def girar_direita_graus(angulo: float, velocidade: int = None) -> None:
    """
    Gira o robô no próprio eixo para a direita pelo ângulo dado (graus).
    Motor esquerdo avança, motor direito recua.
    """
    v = velocidade if velocidade is not None else VELOCIDADE_BASE
    graus_motor = _angulo_para_graus_motor(angulo)
    _motor_esq.run_angle(v,  graus_motor, wait=False)
    _motor_dir.run_angle(v, -graus_motor, wait=True)
    parar()


def girar_esquerda_graus(angulo: float, velocidade: int = None) -> None:
    """
    Gira o robô no próprio eixo para a esquerda pelo ângulo dado (graus).
    Motor direito avança, motor esquerdo recua.
    """
    v = velocidade if velocidade is not None else VELOCIDADE_BASE
    graus_motor = _angulo_para_graus_motor(angulo)
    _motor_esq.run_angle(v, -graus_motor, wait=False)
    _motor_dir.run_angle(v,  graus_motor, wait=True)
    parar()


def girar_180(velocidade: int = None) -> None:
    """Gira o robô 180° no próprio eixo (beco sem saída)."""
    girar_direita_graus(180, velocidade)


def curva_pid(erro: float, kp: float, ki: float, kd: float,
              integral: float, ultimo_erro: float,
              velocidade_base: int) -> tuple:
    """
    Aplica correção PID e define velocidade de cada motor.

    Retorna:
        (integral_atualizado, ultimo_erro_atualizado)

    O chamador deve usar set_velocidade() com os valores calculados aqui.
    Este método retorna diretamente as velocidades calculadas.
    """
    integral    = integral + erro
    derivativo  = erro - ultimo_erro

    correcao = (kp * erro) + (ki * integral) + (kd * derivativo)

    vel_esq = int(velocidade_base + correcao)
    vel_dir = int(velocidade_base - correcao)

    # Limita as velocidades dentro dos limites do motor
    vel_esq = max(-1000, min(1000, vel_esq))
    vel_dir = max(-1000, min(1000, vel_dir))

    set_velocidade(vel_esq, vel_dir)

    return integral, erro