from abc import ABC


class Figuras(ABC):  # clase abstrata

    def __init__(self):
        self.pontos = []  # lista de pontos [x, y, z]

    def addPonto(self, x, y, z):
        self.pontos.append([x, y, z])


class ErroAddPonto(Exception):
    pass


class Ponto(Figuras):

    def __init__(self, x, y, z):
        super().__init__()
        Figuras.addPonto(self, x, y, z)

    def addPonto(self, x, y, z):
        raise ErroAddPonto("Não é possivel adicionar mais um ponto")


class Reta(Figuras):

    def __init__(self, x1, y1, z1, x2, y2, z2):
        super().__init__()
        Figuras.addPonto(self, x1, y1, z1)
        Figuras.addPonto(self, x2, y2, z2)

    def addPonto(self, x, y, z):
        raise ErroAddPonto("Não é possivel adicionar mais um ponto")


class Poligono(Figuras):
    pass
