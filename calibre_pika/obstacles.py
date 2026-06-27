# ============================================================
# obstacles.py — Desvio de obstáculo
# ============================================================
#
# FLUXO DO DESVIO (sempre pelo lado DIREITO conforme solicitado):
#
#   [Ultrassônico detecta objeto ≤ DISTANCIA_OBSTACULO_MM]
#          ↓
#   Para
#   Dá ré RE_OBSTACULO_MM (2 cm)
#          ↓
#   Avança AVANCO_LATERAL_OBSTACULO_MM para a frente (em linha reta)
#          ↓
#   Gira ANGULO_DESVIO_OBSTACULO_GRAUS à esquerda (75°)
#   (isso faz o robô ir em diagonal contornando o obstáculo pela direita)
#          ↓
#   Anda até o sensor ESQUERDO encontrar a linha preta novamente
#          ↓
#   Para e retoma o segue linha
#
# ============================================================

from pybricks.tools import wait, StopWatch

from config import (
    DISTANCIA_OBSTACULO_MM,
    RE_OBSTACULO_MM,
    AVANCO_LATERAL_OBSTACULO_MM,
    ANGULO_DESVIO_OBSTACULO_GRAUS,
    VELOCIDADE_DESVIO,
    VELOCIDADE_BUSCA_LINHA,
    TIMEOUT_BUSCA_LINHA_MS,
)
from sensors import (
    obstaculo_detectado,
    esquerdo_na_linha,
)
from motors import (
    parar,
    andar_distancia_mm,
    girar_esquerda_graus,
    set_velocidade,
)


# ============================================================
# Função principal de desvio
# ============================================================

def executar_desvio_obstaculo() -> None:
    """
    Executa a sequência completa de desvio de obstáculo pelo lado direito.

    Deve ser chamada imediatamente ao detectar obstáculo.
    Ao retornar, o robô está sobre a linha e pronto para retomar
    o segue linha.
    """
    # 1. Para o robô com segurança
    parar()
    wait(100)

    # 2. Dá ré para abrir espaço de manobra
    andar_distancia_mm(-RE_OBSTACULO_MM, velocidade=VELOCIDADE_DESVIO)
    wait(80)

    # 3. Avança lateralmente para posicionar ao lado do obstáculo
    #    (anda reto para passar pela lateral do obstáculo)
    andar_distancia_mm(AVANCO_LATERAL_OBSTACULO_MM, velocidade=VELOCIDADE_DESVIO)
    wait(80)

    # 4. Gira à esquerda para apontar em diagonal contornando o obstáculo
    girar_esquerda_graus(ANGULO_DESVIO_OBSTACULO_GRAUS,
                         velocidade=VELOCIDADE_DESVIO)
    wait(80)

    # 5. Anda em diagonal até o sensor esquerdo encontrar a linha novamente
    _buscar_linha_apos_desvio()

    # 6. Para e deixa o segue linha retomar
    parar()


def _buscar_linha_apos_desvio() -> None:
    """
    Anda em frente devagar até o sensor ESQUERDO ver a linha preta.

    Como o robô está em diagonal (75° à esquerda em relação à linha),
    o sensor esquerdo será o primeiro a cruzar a linha.

    Timeout de segurança: para após TIMEOUT_BUSCA_LINHA_MS ms.
    """
    sw = StopWatch()
    set_velocidade(VELOCIDADE_BUSCA_LINHA, VELOCIDADE_BUSCA_LINHA)

    while not esquerdo_na_linha():
        if sw.time() > TIMEOUT_BUSCA_LINHA_MS:
            # Segurança: não fica em loop eterno
            break
        wait(10)

    parar()


# ============================================================
# Verificação de obstáculo (wrapper para uso no loop principal)
# ============================================================

def checar_e_desviar() -> bool:
    """
    Verifica se há obstáculo à frente e executa o desvio se necessário.

    Retorna:
        True  → havia obstáculo, desvio foi executado
        False → sem obstáculo, nada foi feito
    """
    if obstaculo_detectado(DISTANCIA_OBSTACULO_MM):
        executar_desvio_obstaculo()
        return True
    return False