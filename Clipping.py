class Clipping:

    def clipReta(self, reta):
        return self._cohenSutherland(reta)


    def clipPoligono(self, poligono):
        return self._sutherlandHodgman(poligono)


    def clipBezierBSpline(self, curva, window = False):
        curvaClipada = []
        novaCurva = []
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        for ponto in curva:
            if (ponto[0] > xw_max or ponto[0] < xw_min or
                ponto[1] > yw_max or ponto[1] < yw_min):
                break  # este ponto nao sera desenhado, e nem os seguintes
            else:
                novaCurva.append(ponto)
        if curva:
            curvaClipada = curva
        return curvaClipada


    ''' Clipping de retas pelo metodo de Cohen-Sutherland'''


    def _cohenSutherland(self, reta, window = False):
        esquerda = 0x1
        direita = 0x2
        baixo = 0x4
        cima = 0x8

        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        retaclipada = []

        for _ in range(0, 2):  # pode ser necessario clipar 0, 1 ou 2 pontos, logo passamos 2x
            codigos = []

            for ponto in reta:
                codigo = 0
                # para y
                if ponto[1] > yw_max:
                    codigo += cima
                elif ponto[1] < yw_min:
                    codigo += baixo

                # para x
                if ponto[0] > xw_max:
                    codigo += direita
                elif ponto[0] < xw_min:
                    codigo += esquerda
                codigos.append(codigo)

            if codigos[0] & codigos[1] != 0:
                pass  # descartamos
            elif codigos[0] | codigos[1] == 0:
                retaclipada = reta  # desenhamos
            else:  # calculamos a intersecao

                if codigos[0] != 0:  # determina o ponto a ser clipado
                    codigo = codigos[0]
                else:
                    codigo = codigos[1]

                pontoClipado = ['Erro']  # sinaliza erros
                if codigo & 0x1 == 0x1:
                    pontoClipado = self._clipEsquerdaReta(reta)
                elif codigo & 0x2 == 0x2:
                    pontoClipado = self._clipDireitaReta(reta)
                elif codigo & 0x8 == 0x8:
                    pontoClipado = self._clipCimaReta(reta)
                else:  # codigo & 0x4 == 0x4:
                    pontoClipado = self._clipBaixoReta(reta)

                if codigo == codigos[0]:
                    retaclipada = [pontoClipado, reta[1]]
                else:
                    retaclipada = [reta[0], pontoClipado]
            reta = retaclipada

        # caso os pontos de uma reta estejam em direcoes perpendiculares, podemos ter clipado uma reta que esta
        # completamente fora da window. Neste caso, o algoritmo vai gerar retas fora da window. As removemos.
        result = []
        desenhar = True
        for ponto in reta:
            for coord in ponto:
                if coord > 1 or coord < -1:
                    desenhar = False
                    break
        if desenhar:
            result = reta

        return result


    def _clipEsquerdaReta(self, reta, window = False):
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        m = (reta[1][1] - reta[0][1]) / (reta[1][0] - reta[0][0])
        ye = m * (xw_min - reta[1][0]) + reta[1][1]
        return [xw_min, ye]


    def _clipDireitaReta(self, reta, window = False):
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        yd = reta[0][1] + (reta[1][1] - reta[0][1]) * (xw_max - reta[0][0]) / (reta[1][0] - reta[0][0])
        return [xw_max, yd]


    def _clipCimaReta(self, reta, window = False):
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        x = reta[0][0] + (reta[1][0] - reta[0][0]) * (yw_max - reta[0][1]) / (reta[1][1] - reta[0][1])
        return [x, yw_max]


    def _clipBaixoReta(self, reta, window = False):
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        x = reta[0][0] + (reta[1][0] - reta[0][0]) * (yw_min - reta[0][1]) / (reta[1][1] - reta[0][1])
        return [x, yw_min]


    ''' Clipping de poligonos pelo metodo de Sutherland-Hodgman'''


    def _sutherlandHodgman(self, poligono, window = False):
        poligonoClipado = []
        poligonoClipado = self._clipEsquerdaPoli(poligono)
        poligonoClipado = self._clipCimaPoli(poligonoClipado)
        poligonoClipado = self._clipDireitaPoli(poligonoClipado)
        poligonoClipado = self._clipBaixoPoli(poligonoClipado)
        return poligonoClipado


    def _clipEsquerdaPoli(self, poligono, window = False):
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        poligonoClipado = []
        for i in range(0, len(poligono)):
            pontoAtual = poligono[i]
            pontoAnterior = poligono[(i - 1) % len(poligono)]

            if pontoAtual[0] >= xw_min:  # dentro
                if pontoAnterior[0] < xw_min:  # fora
                    intersecao = self._clipEsquerdaReta([pontoAtual, pontoAnterior])
                    poligonoClipado.append(intersecao)
                poligonoClipado.append(pontoAtual)
            elif pontoAnterior[0] >= xw_min:  # dentro
                intersecao = self._clipEsquerdaReta([pontoAtual, pontoAnterior])
                poligonoClipado.append(intersecao)
        return poligonoClipado


    def _clipDireitaPoli(self, poligono, window = False):
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        poligonoClipado = []
        for i in range(0, len(poligono)):
            pontoAtual = poligono[i]
            pontoAnterior = poligono[(i - 1) % len(poligono)]

            if pontoAtual[0] <= xw_max:  # dentro
                if pontoAnterior[0] > xw_max:  # fora
                    intersecao = self._clipDireitaReta([pontoAtual, pontoAnterior])
                    poligonoClipado.append(intersecao)
                poligonoClipado.append(pontoAtual)
            elif pontoAnterior[0] <= xw_max:  # dentro
                intersecao = self._clipDireitaReta([pontoAtual, pontoAnterior])
                poligonoClipado.append(intersecao)
        return poligonoClipado


    def _clipCimaPoli(self, poligono, window = False):
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        poligonoClipado = []
        for i in range(0, len(poligono)):
            pontoAtual = poligono[i]
            pontoAnterior = poligono[(i - 1) % len(poligono)]

            if pontoAtual[1] <= yw_max:  # dentro
                if pontoAnterior[1] > yw_max:  # fora
                    intersecao = self._clipCimaReta([pontoAtual, pontoAnterior])
                    poligonoClipado.append(intersecao)
                poligonoClipado.append(pontoAtual)
            elif pontoAnterior[1] <= yw_max:  # dentro
                intersecao = self._clipCimaReta([pontoAtual, pontoAnterior])
                poligonoClipado.append(intersecao)
        return poligonoClipado


    def _clipBaixoPoli(self, poligono, window = False):
        if(not window):
            xw_min, xw_max = -1, 1
            yw_min, yw_max = -1, 1
        else:
            xw_min, yw_min = window.getMin()[0] + 10, window.getMin()[1] + 10
            xw_max, yw_max = window.getMax()[0] + 10, window.getMax()[1] + 10

        poligonoClipado = []
        for i in range(0, len(poligono)):
            pontoAtual = poligono[i]
            pontoAnterior = poligono[(i - 1) % len(poligono)]

            if pontoAtual[1] >= yw_min:  # dentro
                if pontoAnterior[1] < yw_min:  # fora
                    intersecao = self._clipBaixoReta([pontoAtual, pontoAnterior])
                    poligonoClipado.append(intersecao)
                poligonoClipado.append(pontoAtual)
            elif pontoAnterior[1] >= yw_min:  # dentro
                intersecao = self._clipBaixoReta([pontoAtual, pontoAnterior])
                poligonoClipado.append(intersecao)
        return poligonoClipado
