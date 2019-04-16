import numpy
import math


class Poligono:

    def __init__(self, nome):
        self.pontos = []  # lista de pontos [x, y, z]
        self.nome = nome
        self.tipo = ""

    def getNome(self):
        return self.nome
    
    def getTipo(self):
        return self.tipo
    
    def setTipo(self, tipo):
        self.tipo = tipo

    def addPonto(self, x, y):
        self.pontos.append([x, y, 1])

    def transformar(self, matriz):
        pontosTemp = []
        for i in self.pontos:
            p = numpy.array([i[0] , i[1], 1])
            p = p.dot(matriz)
            pontosTemp.append(p)
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
        matr = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        self.transformar(matr)

    def escalona(self, sx, sy):  # em torno do centro do objeto
        centro = self.centroGeo()

        matr = numpy.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

        praOrig = numpy.array([[1, 0, 0], [0, 1, 0], [-int(centro[0]), -int(centro[1]), 1]])
        volta = numpy.array([[1, 0, 0], [0, 1, 0], [int(centro[0]), int(centro[1]), 1]])
        matr = praOrig.dot(matr).dot(volta)

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
    
    def drawToViewport(self, ctx, viewport):
        ponto1 = viewport.transforma(self.pontos[0][0],self.pontos[0][1])
        ctx.move_to(ponto1[0], ponto1[1])
        if int(len(self.pontos)) == 1:
            ctx.rel_line_to(1,1)
        else:
            for ponto in self.pontos:  # 1st interation does move_to and line_to to same point
                x2, y2 = ponto[0], ponto[1]
                ponto2 = viewport.transforma(x2, y2)
                ctx.line_to(ponto2[0],ponto2[1])
        ctx.close_path()
        ctx.stroke()
        print(self.tipo)


# class ErroAddPonto(Exception):
#     pass


# class Ponto(Poligono):

#     def __init__(self, nome, x, y):
#         super().__init__(nome)
#         Poligono.addPonto(self, x, y)

#     def addPonto(self, x, y):
#         raise ErroAddPonto("Não é possivel adicionar mais um ponto")


# class Reta(Poligono):

#     def __init__(self, nome, x1, y1, x2, y2):
#         super().__init__(nome)
#         Poligono.addPonto(self, x1, y1)
#         Poligono.addPonto(self, x2, y2)

#     def addPonto(self, x, y):
#         raise ErroAddPonto("Não é possivel adicionar mais um ponto")