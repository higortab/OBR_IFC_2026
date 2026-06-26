from pybricks.tools import wait
from pybricks.parameters import Color


class Navegacao:

    def __init__(self, robot, ultra, cor, mapa, movimento):

        self.robot = robot
        self.ultra = ultra
        self.cor = cor

        self.mapa = mapa
        self.mov = movimento

        self.DIST = 120

    # ------------------------

    
    def verificar(self):
        c = self.cor.color()

        if c == Color.GRAY:
            self.mapa.registrar_bolinha("cinza")
        elif c == Color.BLACK:
            self.mapa.registrar_bolinha("preta")
        elif c == Color.GREEN:
            self.mapa.definir_zona_verde()
        elif c == Color.RED:
            self.mapa.definir_zona_vermelha()


    # ------------------------

    def ir_ate_parede(self):

        self.robot.drive(150, 0)

        while self.ultra.distance() > self.DIST:

            self.verificar()

        self.robot.stop()

    # ------------------------

    def mapear(self):

        self.ir_ate_parede()

        for _ in range(4):

            # anda enquanto não chega na parede
            while self.ultra.distance() > self.DIST:

                self.mov.andar_1_celula()
                self.mapa.mover()

                self.verificar()

                # 🚨 segurança portas
                if self.cor.color() in ["GRAY", "BLACK"] and self.ultra.distance() < 100:

                    self.robot.stop()
                    self.robot.drive(-100, 0)
                    wait(400)

                    self.mov.virar_90(True)
                    self.mapa.virar_direita()

                    break

            self.mov.virar_90(True)
            self.mapa.virar_direita()

    # ------------------------

    def zigzag(self, linhas=20):

        for i in range(linhas):

            while self.ultra.distance() > self.DIST:

                self.mov.andar_1_celula()
                self.mapa.mover()
                self.verificar()

            if i % 2 == 0:
                self.mov.virar_90(True)
                self.mov.andar_1_celula()
                self.mov.virar_90(True)

            else:
                self.mov.virar_90(False)
                self.mov.andar_1_celula()
                self.mov.virar_90(False)