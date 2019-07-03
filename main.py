import gi
import cairo
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Figuras import Poligono
from Handler import Handler

def main():
  builder = Gtk.Builder()
  builder.add_from_file("interface.glade")

  window = builder.get_object("janelaPrincipal")
  window.show_all()

  window_object = builder.get_object("janelaNovoObjeto")
  window_object.connect("delete-event", lambda w, e: w.hide() or True)

  window_transform_object = builder.get_object("janelaTransformarObjeto")
  window_transform_object.connect("delete-event", lambda w, e: w.hide() or True)

  window_choose_file = builder.get_object("janelaEscolherObj")
  window_choose_file.connect("delete-event", lambda w, e: w.hide() or True)

  drawing_area = builder.get_object("myDrawingArea")

  builder.connect_signals(Handler(builder, drawing_area))

  Gtk.main()

if __name__ == "__main__":
  main()