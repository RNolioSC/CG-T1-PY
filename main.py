import gi
import cairo
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Figuras import Poligono

class DisplayFile:
  objetos = []
  builder = None
  listaObjetos = None

  def addObjeto(self, objeto):
    self.objetos.append(objeto)
    DisplayFile.listaObjetos.append([objeto.getNome(), objeto.getTipo()])

  def getObjetos(self):
    return self.objetos

  def setBuilder(self, builder):
    DisplayFile.builder = builder
    DisplayFile.listaObjetos = self.builder.get_object("listaObjetos")

  def removeObjeto(self, nome_objeto):
    for i, o in enumerate(DisplayFile.objetos):
      if o.nome == nome_objeto:
        del DisplayFile.objetos[i]
        break

  def getObjeto(self, nome_objeto):
    for i, o in enumerate(DisplayFile.objetos):
      if o.nome == nome_objeto:
        return DisplayFile.objetos[i]


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


class Handler:
    display_file = DisplayFile()
    pontos = []

    def __init__(self, builder, drawing_area):
        self.builder = builder
        self.drawing_area = drawing_area
        
        da_largura = self.drawing_area.get_allocation().width
        da_altura = self.drawing_area.get_allocation().height

        self.tree_view = self.builder.get_object("treeObjetos")
        self.window = Window(0, 0, da_largura, da_altura)
        self.viewport = Viewport(0, 0, da_largura, da_altura)
        self.viewport.setWindow(self.window)
        self.display_file.setBuilder(builder)

    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_buttonNovoObjeto_clicked(self, *args):
        self.pontos = []
        window_object = builder.get_object("janelaNovoObjeto")
        window_object.show_all()

    def on_buttonCriarDesenharPonto_clicked(self, *args):
        name_entry = builder.get_object("entryNomeObjeto")
        x_entry = builder.get_object("spinXPonto")
        y_entry = builder.get_object("spinYPonto")
        p = Poligono(name_entry.get_text()) 
        p.addPonto(int(x_entry.get_text()), int(y_entry.get_text()))
        p.setTipo("ponto")

        self.display_file.addObjeto(p)
        window_object.hide()

    def on_buttonCriarDesenharReta_clicked(self, *args):
        name_entry = builder.get_object("entryNomeObjeto")
        x_entry = builder.get_object("spinXInicialReta")
        y_entry = builder.get_object("spinYInicialReta")
        x_final_entry = builder.get_object("spinXFinalReta")
        y_final_entry = builder.get_object("spinYFinalReta")
        p = Poligono(name_entry.get_text()) 
        p.addPonto(int(x_entry.get_text()), int(y_entry.get_text()))
        p.addPonto(int(x_final_entry.get_text()), int(y_final_entry.get_text()))
        p.setTipo("reta")
        
        self.display_file.addObjeto(p)
        window_object.hide()

    def on_buttonAdicionarPontoPoligono_clicked(self, *args):
        x_entry = builder.get_object("spinXPoligono")
        y_entry = builder.get_object("spinYPoligono")
        self.pontos.append([x_entry.get_text(), y_entry.get_text(), 1])
        print('Ponto - x: {}, y: {} adicionado'.format(int(x_entry.get_text()), int(y_entry.get_text())))

    def on_buttonCriarDesenharPoligono_clicked(self, *args):
        name_entry = builder.get_object("entryNomeObjeto")
        p = Poligono(name_entry.get_text())
        
        for ponto in self.pontos:
            p.addPonto(int(ponto[0]), int(ponto[1]))

        if int(len(self.pontos)) > 2:
            p.setTipo("poligono")
        elif int(len(self.pontos)) == 2:
            p.setTipo("reta")
        else:
            p.setTipo("ponto")

        self.display_file.addObjeto(p)
        window_object.hide()

    def on_buttonDeletarObjeto_clicked(self, *args):
        print("deleta objeto")
        self.redraw(drawing_area)

    def on_buttonTransformarObjeto_clicked(self, *args):
        window_transform_object = builder.get_object("janelaTransformarObjeto")
        window_transform_object.show_all()

    def on_buttonUp_clicked(self, *args):
        passo = builder.get_object("spinPasso")
        self.window.move(0, int(passo.get_text()))
        self.redraw(drawing_area)

    def on_buttonLeft_clicked(self, *args):
        passo = builder.get_object("spinPasso")
        self.window.move(-int(passo.get_text()), 0)
        self.redraw(drawing_area)

    def on_buttonDown_clicked(self, *args):
        passo = builder.get_object("spinPasso")
        self.window.move(0, -int(passo.get_text()))
        self.redraw(drawing_area)

    def on_buttonRight_clicked(self, *args):
        passo = builder.get_object("spinPasso")
        self.window.move(int(passo.get_text()), 0)
        self.redraw(drawing_area)

    def on_ButtonIn_clicked(self, *args):
        passo = builder.get_object("spinPasso")
        porcentagem = 1 + (int(passo.get_text()) / 100)
        self.window.zoom(porcentagem)
        self.redraw(drawing_area)

    def on_buttonOut_clicked(self, *args):
        passo = builder.get_object("spinPasso")
        porcentagem = 1 - (int(passo.get_text()) / 100)
        self.window.zoom(porcentagem)
        self.redraw(drawing_area)

    def on_buttonTransladar_clicked(self, *args):
        print("transladar")
        self.redraw(drawing_area)

    def on_buttonEscalonar_clicked(self, *args):
        print("escalonar")
        self.redraw(drawing_area)

    def on_buttonRotacionar_clicked(self, *args):
        print("rotacionar")
        self.redraw(drawing_area)

    def drawBackground(self, drawing_area, ctx, *args):
        ctx.set_source_rgb(255, 255, 255)  # color white
        ctx.paint()

    def on_myDrawingArea_draw(self, drawing_area, ctx, *args):
        self.drawBackground(drawing_area, ctx)
        ctx.set_source_rgb(0, 0, 0)  # color black
        
        for objeto in self.display_file.getObjetos():
            print('Desenhando objeto "{}"'.format(objeto.getNome()))
            objeto.drawToViewport(ctx, self.viewport)
            
    def redraw(self, drawing_area, *args):
        drawing_area.queue_draw()
  

builder = Gtk.Builder()
builder.add_from_file("interface.glade")

window = builder.get_object("janelaPrincipal")
window.show_all()

window_object = builder.get_object("janelaNovoObjeto")
window_object.connect("delete-event", lambda w, e: w.hide() or True)

window_transform_object = builder.get_object("janelaTransformarObjeto")
window_transform_object.connect("delete-event", lambda w, e: w.hide() or True)

drawing_area = builder.get_object("myDrawingArea")

builder.connect_signals(Handler(builder, drawing_area))

Gtk.main()