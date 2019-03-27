
class Poligono:

    def __init__(self):
        self.pontos = []  # lista de pontos [x, y, z]

    def addPonto(self, x, y, z):
        self.pontos.append([x, y, z])


class ErroAddPonto(Exception):
    pass


class Ponto(Poligono):

    def __init__(self, x, y, z):
        super().__init__()
        Poligono.addPonto(self, x, y, z)

    def addPonto(self, x, y, z):
        raise ErroAddPonto("Não é possivel adicionar mais um ponto")


class Reta(Poligono):

    def __init__(self, x1, y1, z1, x2, y2, z2):
        super().__init__()
        Poligono.addPonto(self, x1, y1, z1)
        Poligono.addPonto(self, x2, y2, z2)

    def addPonto(self, x, y, z):
        raise ErroAddPonto("Não é possivel adicionar mais um ponto")
