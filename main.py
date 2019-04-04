import gi
import cairo
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Figuras import Poligono, Reta, Ponto

class DisplayFile:
  objects = []
  builder = None
  objectList = None

  def addObject(self, object):
    self.objects.append(object)
    #DisplayFile.objectList.append([object.getNome(), object.__class__.__name__])

  def getObjects(self):
    return self.objects

  def setBuilder(self, builder):
    DisplayFile.builder = builder
    DisplayFile.objectList = self.builder.get_object("ObjectList")

  def removeObject(self, object_name):
    for i, o in enumerate(DisplayFile.objects):
      if o.name == object_name:
        del DisplayFile.objects[i]
        break

  def getObject(self, object_name):
    for i, o in enumerate(DisplayFile.objects):
      if o.name == object_name:
        return DisplayFile.objects[i]

class Handler:
    display_file = DisplayFile()
    draw_counter = 0

    def onDestroy(self, *args):
        Gtk.main_quit()
    def on_buttonNovoObjeto_clicked(self, *args):
        window_object = builder.get_object("janelaNovoObjeto")
        window_object.show_all()
    def on_buttonCriarDesenhar_clicked(self, *args):
        print("cria e desenha")
        name_entry = builder.get_object("entryNomeObjeto")
        x_entry = builder.get_object("spinXPonto")
        y_entry = builder.get_object("spinYPonto")
        p1 = Poligono(name_entry.get_text()) 
        p1.addPonto(int(x_entry.get_text()), int(y_entry.get_text()))

        self.display_file.addObject(p1)
        window_object.hide()
        #self.redraw(drawing_area)
    def on_buttonDeletarObjeto_clicked(self, *args):
        print("deleta objeto")
        self.redraw(drawing_area)
    def on_buttonTransformarObjeto_clicked(self, *args):
        window_transform_object = builder.get_object("janelaTransformarObjeto")
        window_transform_object.show_all()
    def on_buttonUp_clicked(self, *args):
        print("move para cima")
        self.redraw(drawing_area)
    def on_buttonLeft_clicked(self, *args):
        print("move para esquerda")
        self.redraw(drawing_area)
    def on_buttonDown_clicked(self, *args):
        print("move para baixo")
        self.redraw(drawing_area)
    def on_buttonRight_clicked(self, *args):
        print("move para direita")
        self.redraw(drawing_area)
    def on_ButtonIn_clicked(self, *args):
        print("zoom in")
        self.redraw(drawing_area)
    def on_buttonOut_clicked(self, *args):
        print("zoom out")
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
        
        for i in self.display_file.getObjects():
            print('Drawing object "{}"'.format(i.getNome()))
            i.drawToViewport(ctx)

            self.draw_counter += 1
            print("draw() #{0}".format(self.draw_counter))
    def redraw(self, drawing_area, *args):
        drawing_area.queue_draw()
    
  

builder = Gtk.Builder()
builder.add_from_file("interface.glade")
builder.connect_signals(Handler())

window = builder.get_object("janelaPrincipal")
window.show_all()

window_object = builder.get_object("janelaNovoObjeto")
window_object.connect("delete-event", lambda w, e: w.hide() or True)

window_transform_object = builder.get_object("janelaTransformarObjeto")
window_transform_object.connect("delete-event", lambda w, e: w.hide() or True)

drawing_area = builder.get_object("myDrawingArea")


Gtk.main()