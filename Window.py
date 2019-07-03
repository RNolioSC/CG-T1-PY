from Normaliza import Normaliza
from DisplayFile import DisplayFile

class Window:
  def __init__(self, x_min, y_min, x_max, y_max):
    Window.x_min = x_min
    Window.y_min = y_min
    Window.x_max = x_max
    Window.y_max = y_max
    Window.normaliza = Normaliza()
    Window.display_file = DisplayFile()

  def getMin(self):
    return [Window.x_min, Window.y_min]

  def getMax(self):
    return [Window.x_max, Window.y_max]

  def getLargura(self):
    return Window.x_max - Window.x_min
  
  def getAltura(self):
    return Window.y_max - Window.y_min
  
  def getCentro(self):
    largura, altura = self.getLargura(), self.getAltura()
    centro_x = (largura / 2) + Window.x_min
    centro_y = (altura / 2) + Window.y_min
    return [centro_x, centro_y]

  def zoom(self, porcentagem):
    for i in Window.display_file.getObjetos():
      i.scaleNormalizedCoords(porcentagem)

  def setMin(self, x, y):
    Window.x_min = x
    Window.y_min = y
  
  def setMax(self, x, y):
    Window.x_max = x
    Window.y_max = y

  def move(self, x, y):
    obj_coords = []

    # get normalized coordenates for all objects and denormalize them
    for i in Window.display_file.getObjetos():
      norm_coords = i.getPontosNormalizados()
      obj_coords.append(Window.normaliza.denormalizeList(norm_coords))

    Window.x_min += x
    Window.y_min += y
    Window.x_max += x
    Window.y_max += y

    objetos = Window.display_file.getObjetos()

    # renormalize all coords after the window has been resized
    for i in range(len(objetos)):
      objetos[i].pontos_normalizados = Window.normaliza.normalizeList(obj_coords[i])

  def rotate(self, angulo):
    for i in Window.display_file.getObjetos():
      i.rotateNormalizedCoords(angulo)


class Viewport(Window):
  def __init__(self, x_min, y_min, x_max, y_max):
    super().__init__(x_min, y_min, x_max, y_max)
    self.normaliza = Normaliza()
  
  def setWindow(self, window):
    self.window = window

  def transforma(self, x, y):
    xw_min, yw_min = self.window.getMin()[0], self.window.getMin()[1]
    xw_max, yw_max = self.window.getMax()[0], self.window.getMax()[1]

    xvp_min, yvp_min = self.x_min, self.y_min
    xvp_max, yvp_max = self.x_max, self.y_max

    denormalized_point = self.normaliza.denormalize(x, y)

    xvp = ((denormalized_point[0] - xw_min)/(xw_max - xw_min)) * (xvp_max - xvp_min)
    yvp = (1 - ((denormalized_point[1] - yw_min)/(yw_max - yw_min))) * (yvp_max - yvp_min)
    return [xvp, yvp]