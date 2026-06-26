# fake_pybricks.py
# Imita o pybricks para testar no PC sem o robô


class Color:
    GRAY = "GRAY"
    BLACK = "BLACK"
    GREEN = "GREEN"
    RED = "RED"
    NONE = None


class FakeMotor:
    """Imita um motor do EV3"""
    def __init__(self):
        self._angle = 0

    def angle(self):
        # Sempre retorna 999 para simular que o robô já andou 1 célula
        return 999

    def reset(self):
        self._angle = 0


class FakeDrive:
    """Imita o DriveBase do EV3"""
    def __init__(self):
        self.left_motor = FakeMotor()

    def drive(self, velocidade, curva):
        pass  # não faz nada no PC

    def stop(self):
        pass

    def turn(self, graus):
        pass

    def reset(self):
        self.left_motor.reset()


class FakeUltrasonic:
    """
    Imita o sensor de distância.
    Você passa uma lista de distâncias e ele vai retornando uma por vez.
    Quando acabar a lista, repete a última.
    """
    def __init__(self, distancias):
        self.distancias = distancias
        self.i = 0

    def distance(self):
        d = self.distancias[self.i]
        if self.i < len(self.distancias) - 1:
            self.i += 1
        return d


class FakeColorSensor:
    """
    Imita o sensor de cor.
    Você passa uma lista de cores e ele vai retornando uma por vez.
    Use Color.GRAY, Color.BLACK, Color.GREEN, Color.RED ou None.
    """
    def __init__(self, cores):
        self.cores = cores
        self.i = 0

    def color(self):
        c = self.cores[self.i]
        if self.i < len(self.cores) - 1:
            self.i += 1
        return c


# Módulos do pybricks que o código importa mas não usa diretamente nos testes
class Port:
    A = "A"
    B = "B"
    S1 = "S1"
    S2 = "S2"


def wait(ms):
    pass  # no PC não precisa esperar