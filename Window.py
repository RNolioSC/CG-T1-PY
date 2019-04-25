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

  def getLargura(self):
    return self.x_max - self.x_min
  
  def getAltura(self):
    return self.y_max - self.y_min
  
  def getCentro(self):
    largura, altura = self.getLargura(), self.getAltura()
    return [largura/2, altura/2]

  def zoom(self, porcentagem):
    nova_altura = self.getAltura() / porcentagem
    nova_largura =  self.getLargura() / porcentagem
    
    novo_x_min = (nova_largura - self.getCentro()[0]) / 2
    novo_y_min = (nova_altura - self.getCentro()[1]) / 2
    self.setMin(novo_x_min, novo_y_min)

    novo_x_max = (self.getCentro()[0] + nova_largura) / 2
    novo_y_max = (self.getCentro()[1] + nova_altura) / 2
    self.setMax(novo_x_max, novo_y_max)

  def setMin(self, x, y):
    self.x_min = x
    self.y_min = y
  
  def setMax(self, x, y):
    self.x_max = x
    self.y_max = y

  def move(self, x, y):
    self.x_min += x
    self.y_min += y
    self.x_max += x
    self.y_max += y
    

class Viewport(Window):
  def __init__(self, x_min, y_min, x_max, y_max):
    super().__init__(x_min, y_min, x_max, y_max)
  
  def setWindow(self, window):
    self.window = window

  def transforma(self, x, y):
    xw_min, yw_min = self.window.getMin()[0], self.window.getMin()[1]
    xw_max, yw_max = self.window.getMax()[0], self.window.getMax()[1]

    xvp_min, yvp_min = self.x_min, self.y_min
    xvp_max, yvp_max = self.x_max, self.y_max

    xvp = ((x - xw_min)/(xw_max - xw_min)) * (xvp_max - xvp_min)
    yvp = (1 - ((y - yw_min)/(yw_max - yw_min))) * (yvp_max - yvp_min)
    return [xvp, yvp]