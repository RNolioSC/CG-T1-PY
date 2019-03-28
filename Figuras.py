import numpy

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
        return None  # TODO como calcular os extremos para o centro geo?


    # arg:  m se no centro do mundo
    #       o se no centro do objeto
    # retorna uma  numpy.matrix
    def matrRotaciona(self, arg):
        matr = numpy.matrix()
        if arg == 'm':
            pass
        elif arg == 'o':
            pass
        self.transformar(matr)

    # args:  em torno deste ponto
    # retorna uma numpy.matrix
    def matrRotaciona(self, x, y):
        matr = numpy.matrix()
        self.transformar(matr)


class ErroAddPonto(Exception):
    pass


class Ponto(Poligono):

    def __init__(self, nome, x, y):
        super().__init__(nome)
        Poligono.addPonto(self, x, y)

    def addPonto(self, x, y):
        raise ErroAddPonto("Não é possivel adicionar mais um ponto")

    def centroGeo(self):
        return self.pontos[0]


class Reta(Poligono):

    def __init__(self, nome, x1, y1, x2, y2):
        super().__init__(nome)
        Poligono.addPonto(self, x1, y1)
        Poligono.addPonto(self, x2, y2)

    def addPonto(self, x, y):
        raise ErroAddPonto("Não é possivel adicionar mais um ponto")

    def centroGeo(self):
        x = (self.pontos[0][0] + self.pontos[1][0]) / 2
        y = (self.pontos[0][1] + self.pontos[1][1]) / 2
        return [x, y, 1]
