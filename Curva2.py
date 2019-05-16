import numpy


# curvas de bezier com blending
def curvaBezier(pontos, qdadePontos):
    # lista de pontos para a curva e qdadePontos que ela tera. lista de pontos eh destruida.

    if not (len(pontos) % 3 == 1 and len(pontos) > 3):
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


# B-spline com Forward Differences.
def bSpline(pontos):  # lista de pontos para a curva

    if len(pontos) < 4:
        raise Exception("Não é possível gerar uma b-spline: quantidade insuficiente de pontos")

    delta = 0.2
    delta2 = delta * delta
    delta3 = delta2 * delta

    T = numpy.array([[0, 0, 0, 1],
                     [delta3, delta2, delta, 0],
                     [6 * delta3, 2 * delta2, 0, 0],
                     [6 * delta3, 0, 0, 0]])

    C = numpy.array([[-1.0, 3, -3, 1],  # 1.0 para que seja declarado como array de float
                     [3, -6, 3, 0],
                     [-3, 0, 3, 0],
                     [1, 4, 1, 0]])
    C *= (1 / 6)

    curva = []
    for j in range(len(pontos) - 3):
        p0 = pontos[j]
        p1 = pontos[j + 1]
        p2 = pontos[j + 2]
        p3 = pontos[j + 3]

        Cx = []
        Cy = []
        for i in range(4):
            Cxi = (p0[0] * C[i][0]) + (p1[0] * C[i][1]) + (p2[0] * C[i][2]) + (p3[0] * C[i][3])
            Cx.append(Cxi)
            Cyi = (p0[1] * C[i][0]) + (p1[1] * C[i][1]) + (p2[1] * C[i][2]) + (p3[1] * C[i][3])
            Cy.append(Cyi)

        rx = []
        ry = []
        for i in range(4):
            rxi = (Cx[0] * T[i][0]) + (Cx[1] * T[i][1]) + (Cx[2] * T[i][2]) + (Cx[3] * T[i][3])
            rx.append(rxi)
            ryi = (Cy[0] * T[i][0]) + (Cy[1] * T[i][1]) + (Cy[2] * T[i][2]) + (Cy[3] * T[i][3])
            ry.append(ryi)

        x = rx.pop(0)
        deltaX = rx.pop(0)
        delta2X = rx.pop(0)
        delta3X = rx.pop(0)

        y = ry.pop(0)
        deltaY = ry.pop(0)
        delta2Y = ry.pop(0)
        delta3Y = ry.pop(0)

        xVelho = x
        yVellho = y

        for i in range(5):
            x += deltaX
            deltaX += delta2X
            delta2X += delta3X

            y += deltaY
            deltaY += delta2Y
            delta2Y += delta3Y

            curva.append([xVelho, yVellho])
            curva.append([x, y])

            xVelho = x
            yVellho = y

    return curva
