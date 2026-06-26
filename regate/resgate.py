# resgate.py
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Color
from pybricks.tools import wait

# ============================================================
# AJUSTES — mude esses números conforme os testes no robô
# ============================================================

GRAUS_FECHAR_GARRA  = 30    # graus que o motor C gira para fechar a garra
GRAUS_ABRIR_GARRA   = 30  # graus que o motor C gira para abrir a garra
GRAUS_VOLTAR_SENSOR = -30    # graus para devolver o sensor de cor à posição original

DIST_PEGAR          = 60    # distância em mm para parar perto da bolinha (4 cm)
DIST_ZONA           = 40    # distância em mm para parar perto da zona

VELOCIDADE_GARRA    = 100   # velocidade do motor da garra (graus/s)
VELOCIDADE_NAV      = 150   # velocidade de navegação
GRAUS_AJUSTE_GARRA  = 15    # leve giro pra esquerda para alinhar a garra (à direita do robô)
ESPERA_GARRA_MS     = 500   # tempo de espera após girar o motor da garra (ms)

# ============================================================


class Resgate:

    def __init__(self, robot, ultra, cor, mapa, mov):
        self.robot = robot
        self.ultra = ultra
        self.cor   = cor
        self.mapa  = mapa
        self.mov   = mov

        self.motor_garra   = Motor(Port.C)
        self.entregues     = 0
        self.total_bolinhas = 3  # total de bolinhas no campo

    # --------------------------------------------------------
    # GARRA
    # --------------------------------------------------------

    def fechar_garra(self):
        """Gira o motor C para ativar o mecanismo de fechar"""
        self.motor_garra.run_angle(VELOCIDADE_GARRA, GRAUS_FECHAR_GARRA)
        wait(ESPERA_GARRA_MS)
        self.motor_garra.run_angle(VELOCIDADE_GARRA, -GRAUS_VOLTAR_SENSOR)

    def abrir_garra(self):
        """Gira o motor C para ativar o mecanismo de abrir (soltar a bolinha)"""
        self.motor_garra.run_angle(VELOCIDADE_GARRA, GRAUS_ABRIR_GARRA)
        wait(ESPERA_GARRA_MS)
        self.motor_garra.run_angle(VELOCIDADE_GARRA, -GRAUS_ABRIR_GARRA)

    # --------------------------------------------------------
    # NAVEGAÇÃO
    # --------------------------------------------------------

    def _virar_para(self, direcao_alvo):
        """Vira o robô até estar olhando para a direção desejada (0=N,1=L,2=S,3=O)"""
        while self.mapa.direcao != direcao_alvo:
            self.mov.virar_90(True)
            self.mapa.virar_direita()

    def _andar_ate(self, alvo_x, alvo_y):
        """
        Navega pelo grid até (alvo_x, alvo_y).
        Primeiro acerta X, depois Y.
        Para se encontrar parede antes de chegar.
        """
        # Acerta X
        if self.mapa.x < alvo_x:
            self._virar_para(1)  # leste
            while self.mapa.x < alvo_x and self.ultra.distance() > DIST_ZONA:
                self.mov.andar_1_celula()
                self.mapa.mover()
        elif self.mapa.x > alvo_x:
            self._virar_para(3)  # oeste
            while self.mapa.x > alvo_x and self.ultra.distance() > DIST_ZONA:
                self.mov.andar_1_celula()
                self.mapa.mover()

        # Acerta Y
        if self.mapa.y < alvo_y:
            self._virar_para(2)  # sul
            while self.mapa.y < alvo_y and self.ultra.distance() > DIST_ZONA:
                self.mov.andar_1_celula()
                self.mapa.mover()
        elif self.mapa.y > alvo_y:
            self._virar_para(0)  # norte
            while self.mapa.y > alvo_y and self.ultra.distance() > DIST_ZONA:
                self.mov.andar_1_celula()
                self.mapa.mover()

    # --------------------------------------------------------
    # PEGAR BOLINHA
    # --------------------------------------------------------

    def _aproximar_bolinha(self):
        """Avança até ficar a DIST_PEGAR da bolinha"""
        self.robot.drive(VELOCIDADE_NAV, 0)
        while self.ultra.distance() > DIST_PEGAR:
            pass
        self.robot.stop()

    def pegar_bolinha(self, pos):
        """
        Vai até a posição da bolinha, lê a cor com o sensor S1,
        alinha a garra e fecha.
        Retorna a cor da bolinha ('cinza' ou 'preta'), ou None se falhar.
        """
        alvo_x, alvo_y = pos

        # Vai até a célula da bolinha pelo grid
        self._andar_ate(alvo_x, alvo_y)

        # Avança devagar até ficar a 4cm
        self._aproximar_bolinha()

        # Lê a cor com o sensor S1 (antes de pegar)
        cor_lida = self.cor.color()

        if cor_lida == Color.GRAY:
            cor = "cinza"
        elif cor_lida == Color.BLACK:
            cor = "preta"
        else:
            cor = "cinza"  # cor desconhecida — trata como cinza por segurança

        # Leve giro para esquerda para alinhar a garra (que fica à direita)
        self.robot.turn(-GRAUS_AJUSTE_GARRA)
        wait(200)

        # Fecha a garra
        self.fechar_garra()

        # Remove do mapa
        self.mapa.remover_bolinha(cor, (alvo_x, alvo_y))

        return cor

    # --------------------------------------------------------
    # ENTREGAR BOLINHA NA ZONA
    # --------------------------------------------------------

    def entregar(self, cor):
        """Leva a bolinha para a zona correta e abre a garra"""
        if cor == "cinza":
            zona = self.mapa.zona_verde
        else:
            zona = self.mapa.zona_vermelha

        # Vai até a zona pelo grid
        self._andar_ate(zona[0], zona[1])

        # Aproxima da zona usando o sensor de distância
        self.robot.drive(VELOCIDADE_NAV, 0)
        while self.ultra.distance() > DIST_ZONA:
            pass
        self.robot.stop()

        # Solta a bolinha
        self.abrir_garra()
        self.entregues += 1

    # --------------------------------------------------------
    # SAIR PELA FITA PRETA
    # --------------------------------------------------------

    def sair_pela_fita(self):
        """Anda até achar a fita preta no chão e para"""
        self.robot.drive(VELOCIDADE_NAV, 0)
        while self.cor.color() != Color.BLACK:
            pass
        self.robot.stop()

    # --------------------------------------------------------
    # MISSÃO COMPLETA
    # --------------------------------------------------------

    def executar(self, nav):
        """
        Fluxo completo de resgate:

        1. Faz o perímetro (já feito no main antes de chamar aqui)
        2. Inicia o zigue-zague linha por linha
        3. Ao detectar uma bolinha durante o zigue-zague:
              - Para na linha atual
              - Vai pegar a bolinha
              - Lê a cor com o sensor S1
              - Leva para a zona correta
              - Volta para o início da linha atual
              - Continua o zigue-zague
        4. Quando entregar as 3 bolinhas, acha a fita preta e sai
        """
        linhas = 10  # mesmo valor do zigzag

        for i in range(linhas):

            if self.entregues >= self.total_bolinhas:
                break

            # Guarda o início da linha atual para poder voltar depois
            inicio_linha_x = self.mapa.x
            inicio_linha_y = self.mapa.y

            # Anda pela linha até a parede
            while self.ultra.distance() > nav.DIST:

                self.mov.andar_1_celula()
                self.mapa.mover()
                nav.verificar()  # detecta cor no chão

                # Verificar se achou uma bolinha nova
                bolinha_pos = None
                cor_bolinha  = None

                if self.mapa.bolinhas["cinza"]:
                    bolinha_pos = self.mapa.bolinhas["cinza"][-1]
                    cor_bolinha = "cinza"
                elif self.mapa.bolinhas["preta"]:
                    bolinha_pos = self.mapa.bolinhas["preta"][-1]
                    cor_bolinha = "preta"

                if bolinha_pos is not None:
                    # Achou uma bolinha — vai buscar
                    cor_real = self.pegar_bolinha(bolinha_pos)
                    self.entregar(cor_real)

                    if self.entregues >= self.total_bolinhas:
                        break

                    # Volta para o início da linha atual e recomeça ela
                    self._andar_ate(inicio_linha_x, inicio_linha_y)

            if self.entregues >= self.total_bolinhas:
                break

            # Vira para a próxima linha (igual ao zigzag)
            if i % 2 == 0:
                self.mov.virar_90(True)
                self.mapa.virar_direita()
                self.mov.andar_1_celula()
                self.mapa.mover()
                self.mov.virar_90(True)
                self.mapa.virar_direita()
            else:
                self.mov.virar_90(False)
                self.mapa.virar_esquerda()
                self.mov.andar_1_celula()
                self.mapa.mover()
                self.mov.virar_90(False)
                self.mapa.virar_esquerda()

        # Todas entregues — sai pela fita preta
        self.sair_pela_fita()