import numpy
import math
from Clipping import Clipping
from Normaliza import Normaliza

class Poligono:

    def __init__(self, nome):
        self.pontos_m = []
        self.pontos_normalizados = []  # lista de pontos [x, y, z]
        self.nome = nome
        self.tipo = ""
        self.normaliza = Normaliza()

    def getNome(self):
        return self.nome
    
    def getTipo(self):
        return self.tipo

    def getPontosMundo(self):
        return self.pontos_m
    
    def getPontosNormalizados(self):
        return self.pontos_normalizados

    def setTipo(self, tipo):
        self.tipo = tipo

    def addPonto(self, x, y):
        self.pontos_m.append([x, y, 1])
        self.pontos_normalizados.append(self.normaliza.normalize(x, y))

    def scaleNormalizedCoords(self, porcentagem):
        centro = self.normaliza.denormalize(0,0)  # get world coordenates for current viewport center
        self.escalona(porcentagem, porcentagem, centro)
    
    def rotateNormalizedCoords(self, angulo):
        centro = self.normaliza.denormalize(0,0)  # get world coordenates for current viewport center
        self.rotacionaObj(angulo, centro)

    def transformar(self, matriz):
        pontosTemp = []
        pontos_desnormalizados = self.normaliza.denormalizeList(self.pontos_normalizados)
        for i in range(len(self.pontos_normalizados)):
            p = numpy.array([pontos_desnormalizados[i][0] , pontos_desnormalizados[i][1], 1])
            p = p.dot(matriz)
            pontosTemp.append(p)
            self.setPontosMundo(i, p[0], p[1])
        self.pontos_normalizados = self.normaliza.normalizeList(pontosTemp)

    def centroGeo(self):
        x = 0
        y = 0
        pontos_desnormalizados = self.normaliza.denormalizeList(self.pontos_normalizados)
        for ponto in pontos_desnormalizados:
            x += ponto[0]
            y += ponto[1]
        x = x/len(pontos_desnormalizados)
        y = y/len(pontos_desnormalizados)
        return [x, y, 1]

    def translacao(self, dx, dy):
        matr = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        self.transformar(matr)

    def escalona(self, sx, sy, centro):  # em torno do centro do objeto
        matr = numpy.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

        praOrig = numpy.array([[1, 0, 0], [0, 1, 0], [-int(centro[0]), -int(centro[1]), 1]])
        volta = numpy.array([[1, 0, 0], [0, 1, 0], [int(centro[0]), int(centro[1]), 1]])
        matr = praOrig.dot(matr).dot(volta)

        self.transformar(matr)

    # ao redor do centro do objeto. agulo em graus
    # retorna uma  numpy.matrix
    def rotacionaObj(self, angle, centro):
        angle = math.radians(-angle)

        # matriz para rotacionar ao redor do centro do mundo
        matrRot = numpy.array([[math.cos(angle), -math.sin(angle), 0],
                                [math.sin(angle),  math.cos(angle), 0],
                                [0, 0, 1]])

        praOrig = numpy.array([[1, 0, 0], [0, 1, 0], [-centro[0], -centro[1], 1]])
        volta = numpy.array([[1, 0, 0], [0, 1, 0], [centro[0], centro[1], 1]])
        matrRot = praOrig.dot(matrRot).dot(volta)

        self.transformar(matrRot)

    # ao redor do centro do mundo. agulo em graus
    # retorna uma  numpy.matrix
    def rotacionaMundo(self, angle):
        angle = math.radians(-angle)

        # matriz para rotacionar ao redor do centro do mundo
        matrRot = numpy.array([[math.cos(angle), -math.sin(angle), 0],
                                [math.sin(angle), math.cos(angle), 0],
                                [0, 0, 1]])

        self.transformar(matrRot)

    # args: em torno deste ponto. agulo em graus
    # retorna uma numpy.matrix
    def rotacionaPonto(self, x, y, angle):
        angle = math.radians(-angle)

        # matriz para rotacionar ao redor do centro do mundo
        matrRot = numpy.array([[math.cos(angle), -math.sin(angle), 0],
                                [math.sin(angle), math.cos(angle), 0],
                                [0, 0, 1]])

        praPonto = numpy.array([[1, 0, 0], [0, 1, 0], [-x, -y, 1]])
        volta = numpy.array([[1, 0, 0], [0, 1, 0], [x, y, 1]])
        matrRot = praPonto.dot(matrRot).dot(volta)

        self.transformar(matrRot)

    def setPontosMundo(self, i, x, y):
        self.pontos_m[i] = [ x, y ]
        self.pontos_normalizados[i] = self.normaliza.normalize(x, y)

    def normalizaPontos(self):
        for i in range(len(self.pontos_m)):
            x, y = self.pontos_m[i][0], self.pontos_m[i][1]
            self.pontos_normalizados[i] = self.normaliza.normalize(x, y)
    
    def drawToViewport(self, ctx, viewport):
        clipping = Clipping()
        ponto1 = viewport.transforma(self.pontos_normalizados[0][0],self.pontos_normalizados[0][1])
        ctx.move_to(ponto1[0], ponto1[1])
        if int(len(self.pontos_normalizados)) == 1:
            # if clipping.clipPonto(self.pontos_normalizados[0], viewport) != None:
            if (self.pontos_normalizados[0][0] >= -1 and self.pontos_normalizados[0][0] <= 1
                and self.pontos_normalizados[0][1] >= -1 and self.pontos_normalizados[0][1] <= 1):
                ctx.rel_line_to(1,1)
                ctx.stroke()
        else:
            if self.getTipo() == "reta":
                pontos_clipados = clipping.clipReta(self.pontos_normalizados)
            elif self.getTipo() == "poligono":
                pontos_clipados = clipping.clipPoligono(self.pontos_normalizados)
            
            if pontos_clipados:
                ponto1 = viewport.transforma(pontos_clipados[0][0],pontos_clipados[0][1])
                ctx.move_to(ponto1[0], ponto1[1])
                
                for ponto in pontos_clipados:
                    x2, y2 = ponto[0], ponto[1]
                    ponto2 = viewport.transforma(x2, y2)
                    ctx.line_to(ponto2[0],ponto2[1])
                
                ctx.close_path()
                ctx.stroke()
        print(self.tipo)