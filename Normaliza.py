from DisplayFile import DisplayFile
from Variaveis import clipping_border_size as cbz

display_file = DisplayFile()

class Normaliza:
  a,b = -1, 1

  def setWindow(self, window):
    Normaliza.window = window

  def normalize(self, x, y):
    # x' = (b-a) * ((x - min) / (max - min)) + a
    window = Normaliza.window
    a,b = self.a, self.b
    wmin_x, wmax_x = window.getMin()[0] + cbz, window.getMax()[0] - cbz
    wmin_y, wmax_y = window.getMin()[1] + cbz, window.getMax()[1] - cbz

    # print("(Transform) Window at ({},{}) ({},{})".format(wmin_x, wmin_y, wmax_x, wmax_y))

    new_x = (b-a) * ((x - wmin_x) / (wmax_x - wmin_x)) + a
    new_y = (b-a) * ((y - wmin_y) / (wmax_y - wmin_y)) + a

    return [new_x, new_y]

  def denormalize(self, x, y):
    # x' = (b-a) * ((x - min) / (max - min)) + a
    window = Normaliza.window
    a_x, b_x = window.getMin()[0] + cbz, window.getMax()[0] - cbz
    a_y, b_y = window.getMin()[1] + cbz, window.getMax()[1] - cbz
    
    # print("wmin = ({},{})".format(window.getMin()["x"], window.getMin()["y"]))
    # print("wmax = ({},{})\n".format(window.getMax()["x"], window.getMax()["y"]))

    wmin, wmax = -1, 1

    new_x = (b_x-a_x) * ((x - wmin) / (wmax - wmin)) + a_x
    new_y = (b_y-a_y) * ((y - wmin) / (wmax - wmin)) + a_y

    return [new_x, new_y]

  def denormalizeList(self, pontos_normalizados):
    coords = []
    for i in range(len(pontos_normalizados)):
      coords.append(self.denormalize(pontos_normalizados[i][0], pontos_normalizados[i][1]))
    return coords

  def normalizeList(self, pontos_desnormalizados):
    coords = []
    for i in range(len(pontos_desnormalizados)):
      coords.append(self.normalize(pontos_desnormalizados[i][0], pontos_desnormalizados[i][1]))
    return coords
