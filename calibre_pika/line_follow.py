# ============================================================
# line_follow.py — Segue linha com PID + integração dos módulos
# ============================================================
#
# LOOP PRINCIPAL:
#
#   A cada iteração:
#   1. Verifica obstáculo (ultrassônico) → desvia se necessário
#   2. Verifica estado dos sensores laterais:
#      a. AMBOS veem preto cruzando → encruzilhada completa
#      b. APENAS UM vê preto cruzando → possível curva de 90°
#      c. NENHUM vê preto → gap passageiro → segue reto
#      d. NORMAL → aplica PID
#   3. Aplica correção PID nos motores
#
# ============================================================

from pybricks.tools import wait, StopWatch

from config import (
    KP, KI, KD,
    VELOCIDADE_BASE,
    VELOCIDADE_MINIMA,
    TIMEOUT_GAP_MS,
    TIMEOUT_BUSCA_LINHA_MS,
    LIMIAR_PRETO,
)
from sensors import (
    erro_pid,
    esquerdo_na_linha,
    direito_na_linha,
    ler_esquerdo_raw,
    ler_direito_raw,
)
from motors import (
    curva_pid,
    parar,
    andar_frente,
    set_velocidade,
)
from intersection import (
    detectar_tipo_encruzilhada,
    tratar_encruzilhada,
    tratar_curva_sem_marcacao,
)
from obstacles import checar_e_desviar


# ============================================================
# Estado interno do PID
# ============================================================

class EstadoPID:
    """Mantém o estado acumulado do controlador PID entre iterações."""
    def __init__(self):
        self.integral    = 0.0
        self.ultimo_erro = 0.0

    def resetar(self):
        self.integral    = 0.0
        self.ultimo_erro = 0.0


# ============================================================
# Detecção de encruzilhada com debounce
# ============================================================

class DetectorEncruzilhada:
    """
    Detecta quando os sensores laterais encontram uma linha cruzando.

    Para evitar falsos positivos, exige que os dois sensores vejam
    preto por pelo menos DEBOUNCE_MS milissegundos consecutivos.
    """
    DEBOUNCE_MS = 60   # tempo mínimo para confirmar evento (ajuste se necessário)

    def __init__(self):
        self._sw_ambos   = StopWatch()
        self._sw_um      = StopWatch()
        self._ativo_ambos = False
        self._ativo_um    = False
        self._lado_um     = None

    def atualizar(self) -> tuple:
        """
        Retorna (tipo, lado):
            tipo = 'ambos' | 'esquerdo' | 'direito' | None
            lado = 'esquerdo' | 'direito' | None (só relevante para tipo != 'ambos')

        Retorna None quando não há evento confirmado.
        """
        e = esquerdo_na_linha()
        d = direito_na_linha()

        # --- Ambos veem preto (encruzilhada ou gap) ---
        if e and d:
            if not self._ativo_ambos:
                self._ativo_ambos = True
                self._sw_ambos.reset()
            elif self._sw_ambos.time() >= self.DEBOUNCE_MS:
                self._ativo_ambos = False
                self._ativo_um    = False
                return ('ambos', None)
        else:
            self._ativo_ambos = False

        # --- Apenas um vê preto (curva de 90° ou T) ---
        if e and not d:
            lado = 'esquerdo'
        elif d and not e:
            lado = 'direito'
        else:
            lado = None

        if lado is not None:
            if not self._ativo_um or self._lado_um != lado:
                self._ativo_um  = True
                self._lado_um   = lado
                self._sw_um.reset()
            elif self._sw_um.time() >= self.DEBOUNCE_MS:
                self._ativo_um = False
                return (lado, lado)
        else:
            self._ativo_um = False
            self._lado_um  = None

        return (None, None)


# ============================================================
# Gap — ambos sensores perderam a linha temporariamente
# ============================================================

def _tratar_gap(pid: EstadoPID) -> None:
    """
    Quando ambos os sensores perdem a linha e nenhuma encruzilhada
    foi confirmada (gap na linha), anda reto por TIMEOUT_GAP_MS ms
    esperando a linha voltar. Usa o último erro do PID para manter
    a direção.
    """
    sw = StopWatch()
    while sw.time() < TIMEOUT_GAP_MS:
        # Mantém a última correção suavemente
        curva_pid(
            pid.ultimo_erro, KP * 0.3, 0.0, 0.0,
            pid.integral, pid.ultimo_erro,
            VELOCIDADE_BASE
        )
        if esquerdo_na_linha() or direito_na_linha():
            break   # linha encontrada, sai do gap
        wait(10)


# ============================================================
# Loop principal do segue linha
# ============================================================

def iniciar_segue_linha() -> None:
    """
    Loop principal do robô.

    Executa indefinidamente. Para interromper, pressione o botão
    central do EV3 (o loop não implementa parada automática
    pois o segue linha deve durar toda a rodada de 5 minutos).
    """
    pid      = EstadoPID()
    detector = DetectorEncruzilhada()

    # Pequena espera antes de iniciar
    wait(500)
    andar_frente()

    while True:

        # --------------------------------------------------
        # 1. Verificação de obstáculo (prioridade máxima)
        # --------------------------------------------------
        if checar_e_desviar():
            # Após desvio, reseta PID para não acumular erro antigo
            pid.resetar()
            wait(100)
            continue

        # --------------------------------------------------
        # 2. Verificação de encruzilhadas / curvas especiais
        # --------------------------------------------------
        tipo, lado = detector.atualizar()

        if tipo == 'ambos':
            # Encruzilhada completa ou gap
            parar()
            resultado = tratar_encruzilhada()
            pid.resetar()
            # Se foi gap, o loop retoma normalmente
            # Se foi curva, o robô já está posicionado na nova direção
            wait(80)
            continue

        elif tipo in ('esquerdo', 'direito') and tipo is not None:
            # Apenas um sensor viu — possível curva de 90° sem marcação
            parar()
            tratar_curva_sem_marcacao(lado_que_viu=lado)
            pid.resetar()
            wait(80)
            continue

        # --------------------------------------------------
        # 3. Gap passageiro: ambos os sensores no branco,
        #    mas sem confirmação de encruzilhada ainda
        # --------------------------------------------------
        e_raw = ler_esquerdo_raw()
        d_raw = ler_direito_raw()

        ambos_no_branco = (e_raw > 70) and (d_raw > 70)
        if ambos_no_branco:
            _tratar_gap(pid)
            continue

        # --------------------------------------------------
        # 4. Segue linha normal com PID
        # --------------------------------------------------
        erro = erro_pid()
        pid.integral, pid.ultimo_erro = curva_pid(
            erro, KP, KI, KD,
            pid.integral, pid.ultimo_erro,
            VELOCIDADE_BASE
        )

        wait(10)   # pequena pausa para não sobrecarregar o processador