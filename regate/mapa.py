class Mapa:

    def __init__(self):

        self.x = 0
        self.y = 0

        self.direcao = 1  # começa indo para frente

        # movimento por direção
        self.dx = [0, 1, 0, -1]
        self.dy = [-1, 0, 1, 0]

        self.visitados = {(0, 0)}

        self.bolinhas = {
            "cinza": [],
            "preta": []
        }

        self.zona_verde = None
        self.zona_vermelha = None

    # ------------------------

    def mover(self):

        self.x += self.dx[self.direcao]
        self.y += self.dy[self.direcao]

        self.visitados.add((self.x, self.y))

    # ------------------------
    def ja_visitado(self):
     return (self.x, self.y) in self.visitados

    def virar_direita(self):
        self.direcao = (self.direcao + 1) % 4

    def virar_esquerda(self):
        self.direcao = (self.direcao - 1) % 4

    # ------------------------

    def registrar_bolinha(self, cor):

        pos = (self.x, self.y)

        if pos not in self.bolinhas[cor]:
            self.bolinhas[cor].append(pos)

    # ------------------------

    def definir_zona_verde(self):
        self.zona_verde = (self.x, self.y)

    def definir_zona_vermelha(self):
        self.zona_vermelha = (self.x, self.y)

    def remover_bolinha(self, cor, pos):
     if pos in self.bolinhas[cor]:
        self.bolinhas[cor].remove(pos)