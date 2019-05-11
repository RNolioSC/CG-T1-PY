class Curva2:  # curvas de bezier com blending

    @staticmethod
    def curvaBezier(pontos, qdadePontos):  # lista de pontos para a curva e qdadePontos que ela tera

        if len(pontos) % 3 != 1:
            raise Exception("Não é possível gerar uma curva de bezier: quantidade inesperada de pontos")

        curva = []  # lista de pontos
        while len(pontos) > 1:
            p1 = pontos.pop(0)
            p2 = pontos.pop(0)
            p3 = pontos.pop(0)
            p4 = pontos[0]  # este ponto sera o novo p1 na proxima iteracao, logo nao removemos

            cx = 3 * (p2[0] - p1[0])
            cy = 3 * (p2[1] - p1[1])
            bx = 3 * (p3[0] - p2[0]) - cx
            by = 3 * (p3[1] - p2[1]) - cy
            ax = (p4[0] - p1[0]) - (cx + bx)
            ay = (p4[1] - p1[1]) - (cy + by)

            i = 0
            t = 0
            while i < qdadePontos:
                x = p1[0] + t * (cx + t * (bx + t * ax))
                y = p1[1] + t * (cy + t * (by + t * ay))

                curva.append([x, y])

                t += 1 / qdadePontos
                i += 1
                
        return curva
