# ============================================================
# intersection.py — Lógica de encruzilhadas e beco sem saída
# ============================================================
#
# FLUXO GERAL:
#
#   [Ambos laterais veem preto cruzando]
#          ↓
#   Avança DISTANCIA_MEIO_LATERAIS_MM (sensor do meio chega ao ponto)
#          ↓
#   Gira ANGULO_VERIFICACAO_DIAGONAL_GRAUS para a ESQUERDA
#   → verifica verde
#   → volta ao centro
#   Gira ANGULO_VERIFICACAO_DIAGONAL_GRAUS para a DIREITA
#   → verifica verde
#   → volta ao centro
#          ↓
#   Decisão:
#     nenhum verde  → gap, avança reto (reencontra linha)
#     só esquerda   → vira 90° esquerda + avança AVANCO_POS_VERIFICACAO_MM
#     só direita    → vira 90° direita  + avança AVANCO_POS_VERIFICACAO_MM
#     ambos verdes  → beco sem saída → gira 180°
#
# CURVA DE 90° SEM MARCAÇÃO (apenas UM lateral vê cruzando):
#   Avança AVANCO_VERIFICACAO_CURVA_MM
#   → sensor do meio vê preto? → realinha e continua
#   → não vê preto? → volta, gira para o lado que tinha preto, continua
#
# ============================================================

from pybricks.tools import wait
import math

from config import (
    DISTANCIA_MEIO_LATERAIS_MM,
    ANGULO_VERIFICACAO_DIAGONAL_GRAUS,
    AVANCO_POS_VERIFICACAO_MM,
    AVANCO_VERIFICACAO_CURVA_MM,
    VELOCIDADE_BASE,
    VELOCIDADE_BUSCA_LINHA,
    INTERVALO_DUPLO_VERDE_MS,
    LARGURA_ROBO_MM,
)
from sensors  import (
    esquerdo_na_linha,
    direito_na_linha,
    meio_ve_verde,
    meio_ve_preto,
)
from motors   import (
    andar_distancia_mm,
    girar_esquerda_graus,
    girar_direita_graus,
    girar_180,
    parar,
    set_velocidade,
)


# ============================================================
# Verificação diagonal do sensor do meio
# ============================================================

def _verificar_lado_esquerdo() -> bool:
    """
    Gira para a esquerda o ângulo diagonal configurado,
    verifica se há verde, depois retorna ao centro.
    """
    girar_esquerda_graus(ANGULO_VERIFICACAO_DIAGONAL_GRAUS,
                         velocidade=VELOCIDADE_BUSCA_LINHA)
    wait(80)
    verde = meio_ve_verde()
    girar_direita_graus(ANGULO_VERIFICACAO_DIAGONAL_GRAUS,
                        velocidade=VELOCIDADE_BUSCA_LINHA)
    return verde


def _verificar_lado_direito() -> bool:
    """
    Gira para a direita o ângulo diagonal configurado,
    verifica se há verde, depois retorna ao centro.
    """
    girar_direita_graus(ANGULO_VERIFICACAO_DIAGONAL_GRAUS,
                        velocidade=VELOCIDADE_BUSCA_LINHA)
    wait(80)
    verde = meio_ve_verde()
    girar_esquerda_graus(ANGULO_VERIFICACAO_DIAGONAL_GRAUS,
                         velocidade=VELOCIDADE_BUSCA_LINHA)
    return verde


# ============================================================
# Função principal: encruzilhada completa (ambos laterais)
# ============================================================

def tratar_encruzilhada() -> str:
    """
    Chamada quando AMBOS os sensores laterais detectam a linha cruzando.

    1. Avança para que o sensor do meio chegue ao ponto.
    2. Verifica verde à esquerda e à direita.
    3. Executa a manobra adequada.

    Retorna string com a ação executada:
        'gap'       → sem verde, seguiu reto
        'esquerda'  → virou à esquerda
        'direita'   → virou à direita
        'beco'      → girou 180°
    """
    # Avança para o sensor do meio chegar ao ponto da encruzilhada
    andar_distancia_mm(DISTANCIA_MEIO_LATERAIS_MM, velocidade=VELOCIDADE_BASE)

    # Verifica cada lado (esquerda primeiro, depois direita)
    verde_esq = _verificar_lado_esquerdo()
    verde_dir = _verificar_lado_direito()

    if verde_esq and verde_dir:
        # Beco sem saída: dois verdes → 180°
        girar_180(velocidade=VELOCIDADE_BUSCA_LINHA)
        # Pequeno avanço para alinhar com a linha de volta
        andar_distancia_mm(AVANCO_POS_VERIFICACAO_MM, velocidade=VELOCIDADE_BASE)
        return 'beco'

    elif verde_esq and not verde_dir:
        # Vira à esquerda
        girar_esquerda_graus(90, velocidade=VELOCIDADE_BUSCA_LINHA)
        andar_distancia_mm(AVANCO_POS_VERIFICACAO_MM, velocidade=VELOCIDADE_BASE)
        return 'esquerda'

    elif verde_dir and not verde_esq:
        # Vira à direita
        girar_direita_graus(90, velocidade=VELOCIDADE_BUSCA_LINHA)
        andar_distancia_mm(AVANCO_POS_VERIFICACAO_MM, velocidade=VELOCIDADE_BASE)
        return 'direita'

    else:
        # Nenhum verde → gap → segue reto
        # O segue linha vai reencontrar a linha automaticamente
        return 'gap'


# ============================================================
# Curva de 90° sem marcação (apenas UM lateral vê cruzando)
# ============================================================

def tratar_curva_sem_marcacao(lado_que_viu: str) -> None:
    """
    Chamada quando APENAS UM sensor lateral detecta linha cruzando,
    indicando possível curva de 90° sem marcação verde.

    Parâmetro:
        lado_que_viu: 'esquerdo' ou 'direito' — qual lateral viu a linha cruzar.

    Fluxo:
        1. Avança AVANCO_VERIFICACAO_CURVA_MM.
        2. Se sensor do meio vê preto → linha encontrada, realinha e retorna.
        3. Se não vê preto → volta, gira para o lado_que_viu, retoma segue linha.
    """
    # Avança tentando encontrar a continuação da linha
    andar_distancia_mm(AVANCO_VERIFICACAO_CURVA_MM,
                       velocidade=VELOCIDADE_BASE)

    if meio_ve_preto():
        # Linha encontrada à frente — realinha suavemente
        # O segue linha retoma o controle normalmente
        return

    # Linha não encontrada → volta e gira para o lado correto
    andar_distancia_mm(-AVANCO_VERIFICACAO_CURVA_MM,
                       velocidade=VELOCIDADE_BASE)

    # Aguarda sensor do meio ver preto (ponto de referência para girar)
    _buscar_preto_re()

    if lado_que_viu == 'esquerdo':
        girar_esquerda_graus(90, velocidade=VELOCIDADE_BUSCA_LINHA)
    else:
        girar_direita_graus(90, velocidade=VELOCIDADE_BUSCA_LINHA)

    andar_distancia_mm(AVANCO_POS_VERIFICACAO_MM, velocidade=VELOCIDADE_BASE)


def _buscar_preto_re() -> None:
    """
    Anda devagar para trás até o sensor do meio encontrar preto.
    Usado para reposicionar antes de girar numa curva sem marcação.
    Timeout: para depois de 2 segundos para evitar loop infinito.
    """
    from pybricks.tools import StopWatch
    sw = StopWatch()
    set_velocidade(-VELOCIDADE_BUSCA_LINHA, -VELOCIDADE_BUSCA_LINHA)
    while not meio_ve_preto():
        if sw.time() > 2000:
            break
        wait(10)
    parar()


# ============================================================
# Detecção de estado de encruzilhada
# ============================================================

def detectar_tipo_encruzilhada() -> str:
    """
    Verifica o estado atual dos sensores laterais e classifica:

    Retorna:
        'ambos'     → ambos laterais veem preto (encruzilhada completa / gap)
        'esquerdo'  → apenas esquerdo vê preto cruzando (curva ou T)
        'direito'   → apenas direito vê preto cruzando (curva ou T)
        'normal'    → nenhum evento especial
    """
    e = esquerdo_na_linha()
    d = direito_na_linha()

    if e and d:
        return 'ambos'
    elif e and not d:
        return 'esquerdo'
    elif d and not e:
        return 'direito'
    return 'normal'