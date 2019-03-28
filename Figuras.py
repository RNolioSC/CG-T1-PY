import numpy
import math


class Poligono:

    def __init__(self, nome):
        self.pontos = []  # lista de pontos [x, y, z]
        self.nome = nome

    def addPonto(self, x, y):
        self.pontos.append([x, y, 1])

    def transformar(self, matriz):
        # TODO: assert para testes, remover na versao final
        # verifica se o argumento passado é do tipo 'numpy.matrix'
        assert type(matriz).__name__ == "matrix"

        pontosTemp = []
        for i in self.pontos:
            # numpy permite multiplicar diretamente. logo, transformamos em array de pontos
            pontosTemp.append(numpy.asarray(i*matriz))
        self.pontos = pontosTemp

    def centroGeo(self):
        x = 0
        y = 0
        for ponto in self.pontos:
            x += ponto[0]
            y += ponto[1]
        x = x/len(self.pontos)
        y = y/len(self.pontos)
        return [x, y, 1]

    def translacao(self, dx, dy):
        matr = numpy.matrix([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        self.transformar(matr)

    def escalona(self, sx, sy):  # em torno do centro do objeto
        centro = self.centroGeo()

        matr = numpy.matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

        praOrig = numpy.matrix([[1, 0, 0], [0, 1, 0], [-centro[0], -centro[1], 1]])
        volta = numpy.matrix([[1, 0, 0], [0, 1, 0], [centro[0], centro[1], 1]])
        matr = praOrig * matr * volta

        self.transformar(matr)

    # ao redor do centro do objeto. agulo em graus
    # retorna uma  numpy.matrix
    def rotacionaObj(self, angle):
        centro = self.centroGeo()
        angle = math.radians(-angle)

        # matriz para rotacionar ao redor do centro do mundo
        matrRot = numpy.matrix([[math.cos(angle), -math.sin(angle), 0],
                                [math.sin(angle),  math.cos(angle), 0],
                                [0, 0, 1]])

        praOrig = numpy.matrix([[1, 0, 0], [0, 1, 0], [-centro[0], -centro[1], 1]])
        volta = numpy.matrix([[1, 0, 0], [0, 1, 0], [centro[0], centro[1], 1]])
        matrRot = praOrig*matrRot*volta

        self.transformar(matrRot)

    # ao redor do centro do mundo. agulo em graus
    # retorna uma  numpy.matrix
    def rotacionaMundo(self, angle):
        centro = self.centroGeo()
        angle = math.radians(-angle)

        # matriz para rotacionar ao redor do centro do mundo
        matrRot = numpy.matrix([[math.cos(angle), -math.sin(angle), 0],
                                [math.sin(angle), math.cos(angle), 0],
                                [0, 0, 1]])

        self.transformar(matrRot)

    # args: em torno deste ponto. agulo em graus
    # retorna uma numpy.matrix
    def rotacionaPonto(self, x, y, angle):
        centro = self.centroGeo()
        angle = math.radians(-angle)

        # matriz para rotacionar ao redor do centro do mundo
        matrRot = numpy.matrix([[math.cos(angle), -math.sin(angle), 0],
                                [math.sin(angle), math.cos(angle), 0],
                                [0, 0, 1]])

        praPonto = numpy.matrix([[1, 0, 0], [0, 1, 0], [-x, -y, 1]])
        volta = numpy.matrix([[1, 0, 0], [0, 1, 0], [x, y, 1]])
        matrRot = praPonto * matrRot * volta

        self.transformar(matrRot)


class ErroAddPonto(Exception):
    pass


class Ponto(Poligono):

    def __init__(self, nome, x, y):
        super().__init__(nome)
        Poligono.addPonto(self, x, y)

    def addPonto(self, x, y):
        raise ErroAddPonto("Não é possivel adicionar mais um ponto")


class Reta(Poligono):

    def __init__(self, nome, x1, y1, x2, y2):
        super().__init__(nome)
        Poligono.addPonto(self, x1, y1)
        Poligono.addPonto(self, x2, y2)

    def addPonto(self, x, y):
        raise ErroAddPonto("Não é possivel adicionar mais um ponto")
