class Clipping:

    # clipa um dicionario de retas por vez
    def clipRetas(self, retas, janela):
        return self._cohenSutherland(retas, janela)


    # clipa um dicionario de poligonos por vez
    def clipPoligonos(self, poligonos, janela):
        return self._sutherlandHodgman(poligonos, janela)


    # clipa um dicionario de pontos por vez
    def clipPontos(self, pontos, janela):
        pontosClipados = {}
        for pontoNome in pontos:
            ponto = pontos[pontoNome]
            if ponto[0] > janela.getMax()[0] or ponto[0] < janela.getMin()[0] or \
                    ponto[1] > janela.getMax()[1] or ponto[1] < janela.getMin()[1]:
                pass  # este ponto nao sera desenhado
            else:
                pontosClipados[pontoNome] = ponto
        return pontosClipados

    # clipa um dicionario de curvas de bezier por vez
    def clipBezier(self, curvas, janela):
        curvasClipadas = {}
        for curvaNome in curvas:
            curva = curvas[curvaNome]
            novaCurva = []
            for ponto in curva:
                if ponto[0] > janela.getMax()[0] or ponto[0] < janela.getMin()[0] or \
                        ponto[1] > janela.getMax()[1] or ponto[1] < janela.getMin()[1]:
                    break  # este ponto nao sera desenhado, e nem os seguintes
                else:
                    novaCurva.append(ponto)
            if curva:
                curvasClipadas[curvaNome] = curva
        return curvasClipadas


    ''' Clipping de retas pelo metodo de Cohen-Sutherland'''


    # clipa um dicionario de retas por vez
    def _cohenSutherland(self, retas, janela):
        esquerda = 0x1
        direita = 0x2
        baixo = 0x4
        cima = 0x8

        retasclipadas = {}
        for _ in range(0, 2):  # pode ser necessario clipar 0, 1 ou 2 pontos, logo passamos 2x

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
                        pontoClipado = self._clipEsquerdaReta(retas[retanome], janela)
                    elif codigo & 0x2 == 0x2:
                        pontoClipado = self._clipDireitaReta(retas[retanome], janela)
                    elif codigo & 0x8 == 0x8:
                        pontoClipado = self._clipCimaReta(retas[retanome], janela)
                    else:  # codigo & 0x4 == 0x4:
                        pontoClipado = self._clipBaixoReta(retas[retanome], janela)

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


    def _clipEsquerdaReta(self, reta, janela):
        m = (reta[1][1] - reta[0][1]) / (reta[1][0] - reta[0][0])
        ye = m * (janela.getMin()[0] - reta[1][0]) + reta[1][1]
        return [janela.getMin()[0], ye]


    def _clipDireitaReta(self, reta, janela):
        yd = reta[0][1] + (reta[1][1] - reta[0][1]) * (janela.getMax()[0] - reta[0][0]) / (reta[1][0] - reta[0][0])
        return [janela.getMax()[0], yd]


    def _clipCimaReta(self, reta, janela):
        x = reta[0][0] + (reta[1][0] - reta[0][0]) * (janela.getMax()[1] - reta[0][1]) / (reta[1][1] - reta[0][1])
        return [x, janela.getMax()[1]]


    def _clipBaixoReta(self, reta, janela):
        x = reta[0][0] + (reta[1][0] - reta[0][0]) * (janela.getMin()[1] - reta[0][1]) / (reta[1][1] - reta[0][1])
        return [x, janela.getMin()[1]]


    ''' Clipping de poligonos pelo metodo de Sutherland-Hodgman'''


    # clipa um dicionario de poligonos por vez
    def _sutherlandHodgman(self, poligonos, janela):
        poligonosClipados = {}
        for poliNome in poligonos:
            poligonosClipados[poliNome] = self._sutherlandHodgman1poli(poligonos[poliNome], janela)
        return poligonosClipados


    # clipa um poligono por vez (lista de pontos)
    def _sutherlandHodgman1poli(self, poligono, janela):
        poligono = self._clipEsquerdaPoli(poligono, janela)
        poligono = self._clipCimaPoli(poligono, janela)
        poligono = self._clipDireitaPoli(poligono, janela)
        poligono = self._clipBaixoPoli(poligono, janela)
        return poligono


    def _clipEsquerdaPoli(self, poligono, janela):
        poligonoClipado = []
        for i in range(0, len(poligono)):
            pontoAtual = poligono[i]
            pontoAnterior = poligono[(i - 1) % len(poligono)]

            if pontoAtual[0] >= janela.getMin()[0]:  # dentro
                if pontoAnterior[0] < janela.getMin()[0]:  # fora
                    intersecao = self._clipEsquerdaReta([pontoAtual, pontoAnterior], janela)
                    poligonoClipado.append(intersecao)
                poligonoClipado.append(pontoAtual)
            elif pontoAnterior[0] >= janela.getMin()[0]:  # dentro
                intersecao = self._clipEsquerdaReta([pontoAtual, pontoAnterior], janela)
                poligonoClipado.append(intersecao)
        return poligonoClipado


    def _clipDireitaPoli(self, poligono, janela):
        poligonoClipado = []
        for i in range(0, len(poligono)):
            pontoAtual = poligono[i]
            pontoAnterior = poligono[(i - 1) % len(poligono)]

            if pontoAtual[0] <= janela.getMax()[0]:  # dentro
                if pontoAnterior[0] > janela.getMax()[0]:  # fora
                    intersecao = self._clipDireitaReta([pontoAtual, pontoAnterior], janela)
                    poligonoClipado.append(intersecao)
                poligonoClipado.append(pontoAtual)
            elif pontoAnterior[0] <= janela.getMax()[0]:  # dentro
                intersecao = self._clipDireitaReta([pontoAtual, pontoAnterior], janela)
                poligonoClipado.append(intersecao)
        return poligonoClipado


    def _clipCimaPoli(self, poligono, janela):
        poligonoClipado = []
        for i in range(0, len(poligono)):
            pontoAtual = poligono[i]
            pontoAnterior = poligono[(i - 1) % len(poligono)]

            if pontoAtual[1] <= janela.getMax()[1]:  # dentro
                if pontoAnterior[1] > janela.getMax()[1]:  # fora
                    intersecao = self._clipCimaReta([pontoAtual, pontoAnterior], janela)
                    poligonoClipado.append(intersecao)
                poligonoClipado.append(pontoAtual)
            elif pontoAnterior[1] <= janela.getMax()[1]:  # dentro
                intersecao = self._clipCimaReta([pontoAtual, pontoAnterior], janela)
                poligonoClipado.append(intersecao)
        return poligonoClipado


    def _clipBaixoPoli(self, poligono, janela):
        poligonoClipado = []
        for i in range(0, len(poligono)):
            pontoAtual = poligono[i]
            pontoAnterior = poligono[(i - 1) % len(poligono)]

            if pontoAtual[1] >= janela.getMin()[1]:  # dentro
                if pontoAnterior[1] < janela.getMin()[1]:  # fora
                    intersecao = self._clipBaixoReta([pontoAtual, pontoAnterior], janela)
                    poligonoClipado.append(intersecao)
                poligonoClipado.append(pontoAtual)
            elif pontoAnterior[1] >= janela.getMin()[1]:  # dentro
                intersecao = self._clipBaixoReta([pontoAtual, pontoAnterior], janela)
                poligonoClipado.append(intersecao)
        return poligonoClipado
