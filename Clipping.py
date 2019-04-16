class Window:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def getMin(self):
        return [self.x_min, self.y_min]

    def getMax(self):
        return [self.x_max, self.y_max]


# clipa um dicionario de retas por vez
def clipRetas(retas, janela):
    return _cohenSutherland(retas, janela)


# clipa um dicionario de poligonos por vez
def clipPoligonos(poligonos, janela):
    return _sutherlandHodgman(poligonos, janela)


# clipa um dicionario de pontos por vez
def clipPontos(pontos, janela):
    pontosClipados = {}
    for pontoNome in pontos:
        ponto = pontos[pontoNome]
        if ponto[0] > janela.getMax()[0] or ponto[0] < janela.getMin()[0] or \
                ponto[1] > janela.getMax()[1] or ponto[1] < janela.getMin()[1]:
            pass  # este ponto nao sera desenhado
        else:
            pontosClipados[pontoNome] = ponto
    return pontosClipados


''' Clipping de retas pelo metodo de Cohen-Sutherland'''


# clipa um dicionario de retas por vez
def _cohenSutherland(retas, janela):
    esquerda = 0x1
    direita = 0x2
    baixo = 0x4
    cima = 0x8

    retasclipadas = {}
    for i in range(0, 2):  # pode ser necessario clipar 0, 1 ou 2 pontos, logo passamos 2x

        for retanome in retas:  # A, B, C, ...
            codigos = []

            for ponto in retas[retanome]:
                codigo = 0
                # para y
                if ponto[1] > janela.getMax()[1]:
                    codigo += cima
                elif ponto[1] < janela.getMin()[1]:
                    codigo += baixo

                # para x
                if ponto[0] > janela.getMax()[0]:
                    codigo += direita
                elif ponto[0] < janela.getMin()[0]:
                    codigo += esquerda
                codigos.append(codigo)

            if codigos[0] & codigos[1] != 0:
                pass  # descartamos
            elif codigos[0] | codigos[1] == 0:
                retasclipadas[retanome] = retas[retanome]  # desenhamos
            else:  # calculamos a intersecao

                if codigos[0] != 0:  # determina o ponto a ser clipado
                    codigo = codigos[0]
                else:
                    codigo = codigos[1]

                pontoClipado = ['Erro']  # sinaliza erros
                if codigo & 0x1 == 0x1:
                    pontoClipado = _clipEsquerdaReta(retas[retanome], janela)
                elif codigo & 0x2 == 0x2:
                    pontoClipado = _clipDireitaReta(retas[retanome], janela)
                elif codigo & 0x8 == 0x8:
                    pontoClipado = _clipCimaReta(retas[retanome], janela)
                else:  # codigo & 0x4 == 0x4:
                    pontoClipado = _clipBaixoReta(retas[retanome], janela)

                if codigo == codigos[0]:
                    retasclipadas[retanome] = [pontoClipado, retas[retanome][1]]
                else:
                    retasclipadas[retanome] = [retas[retanome][0], pontoClipado]
        # atualizando pra proxima iteracao
        for reta in retasclipadas:
            retas[reta] = retasclipadas[reta]

    # caso os pontos de uma reta estejam em direcoes perpendiculares, podemos ter clipado uma reta que esta
    # completamente fora da window. Neste caso, o algoritmo vai gerar retas fora da window. As removemos.
    result = {}
    for retanome in retas:
        reta = retas[retanome]
        desenhar = True
        for ponto in reta:
            for coord in ponto:
                if coord > 1 or coord < -1:
                    desenhar = False
                    break
        if desenhar:
            result[retanome] = retas[retanome]

    return result


def _clipEsquerdaReta(reta, janela):
    m = (reta[1][1] - reta[0][1]) / (reta[1][0] - reta[0][0])
    ye = m * (janela.getMin()[0] - reta[1][0]) + reta[1][1]
    return [janela.getMin()[0], ye]


def _clipDireitaReta(reta, janela):
    yd = reta[0][1] + (reta[1][1] - reta[0][1]) * (janela.getMax()[0] - reta[0][0]) / (reta[1][0] - reta[0][0])
    return [janela.getMax()[0], yd]


def _clipCimaReta(reta, janela):
    x = reta[0][0] + (reta[1][0] - reta[0][0]) * (janela.getMax()[1] - reta[0][1]) / (reta[1][1] - reta[0][1])
    return [x, janela.getMax()[1]]


def _clipBaixoReta(reta, janela):
    x = reta[0][0] + (reta[1][0] - reta[0][0]) * (janela.getMin()[1] - reta[0][1]) / (reta[1][1] - reta[0][1])
    return [x, janela.getMin()[1]]


''' Clipping de poligonos pelo metodo de Sutherland-Hodgman'''


# clipa um dicionario de poligonos por vez
def _sutherlandHodgman(poligonos, janela):
    poligonosClipados = {}
    for poliNome in poligonos:
        poligonosClipados[poliNome] = _sutherlandHodgman1poli(poligonos[poliNome], janela)
    return poligonosClipados


# clipa um poligono por vez (lista de pontos)
def _sutherlandHodgman1poli(poligono, janela):
    poligono = _clipEsquerdaPoli(poligono, janela)
    poligono = _clipCimaPoli(poligono, janela)
    poligono = _clipDireitaPoli(poligono, janela)
    poligono = _clipBaixoPoli(poligono, janela)
    return poligono


def _clipEsquerdaPoli(poligono, janela):
    poligonoClipado = []
    for i in range(0, len(poligono)):
        pontoAtual = poligono[i]
        pontoAnterior = poligono[(i - 1) % len(poligono)]

        if pontoAtual[0] >= janela.getMin()[0]:  # dentro
            if pontoAnterior[0] < janela.getMin()[0]:  # fora
                intersecao = _clipEsquerdaReta([pontoAtual, pontoAnterior], janela)
                poligonoClipado.append(intersecao)
            poligonoClipado.append(pontoAtual)
        elif pontoAnterior[0] >= janela.getMin()[0]:  # dentro
            intersecao = _clipEsquerdaReta([pontoAtual, pontoAnterior], janela)
            poligonoClipado.append(intersecao)
    return poligonoClipado


def _clipDireitaPoli(poligono, janela):
    poligonoClipado = []
    for i in range(0, len(poligono)):
        pontoAtual = poligono[i]
        pontoAnterior = poligono[(i - 1) % len(poligono)]

        if pontoAtual[0] <= janela.getMax()[0]:  # dentro
            if pontoAnterior[0] > janela.getMax()[0]:  # fora
                intersecao = _clipDireitaReta([pontoAtual, pontoAnterior], janela)
                poligonoClipado.append(intersecao)
            poligonoClipado.append(pontoAtual)
        elif pontoAnterior[0] <= janela.getMax()[0]:  # dentro
            intersecao = _clipDireitaReta([pontoAtual, pontoAnterior], janela)
            poligonoClipado.append(intersecao)
    return poligonoClipado


def _clipCimaPoli(poligono, janela):
    poligonoClipado = []
    for i in range(0, len(poligono)):
        pontoAtual = poligono[i]
        pontoAnterior = poligono[(i - 1) % len(poligono)]

        if pontoAtual[1] <= janela.getMax()[1]:  # dentro
            if pontoAnterior[1] > janela.getMax()[1]:  # fora
                intersecao = _clipCimaReta([pontoAtual, pontoAnterior], janela)
                poligonoClipado.append(intersecao)
            poligonoClipado.append(pontoAtual)
        elif pontoAnterior[1] <= janela.getMax()[1]:  # dentro
            intersecao = _clipCimaReta([pontoAtual, pontoAnterior], janela)
            poligonoClipado.append(intersecao)
    return poligonoClipado


def _clipBaixoPoli(poligono, janela):
    poligonoClipado = []
    for i in range(0, len(poligono)):
        pontoAtual = poligono[i]
        pontoAnterior = poligono[(i - 1) % len(poligono)]

        if pontoAtual[1] >= janela.getMin()[1]:  # dentro
            if pontoAnterior[1] < janela.getMin()[1]:  # fora
                intersecao = _clipBaixoReta([pontoAtual, pontoAnterior], janela)
                poligonoClipado.append(intersecao)
            poligonoClipado.append(pontoAtual)
        elif pontoAnterior[1] >= janela.getMin()[1]:  # dentro
            intersecao = _clipBaixoReta([pontoAtual, pontoAnterior], janela)
            poligonoClipado.append(intersecao)
    return poligonoClipado
