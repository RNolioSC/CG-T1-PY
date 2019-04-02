import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo
from math import pi
import sys

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()
    def on_buttonNovoObjeto_clicked(self, *args):
        window = builder.get_object("janelaNovoObjeto")
        window.show_all()
    def on_buttonCriarDesenhar_clicked(self, *args):
        print("cria e desenha")
    def on_buttonDeletarObjeto_clicked(self, *args):
        print("deleta objeto")
    def on_buttonTransformarObjeto_clicked(self, *args):
        window = builder.get_object("janelaTransformarObjeto")
        window.show_all()
    def on_buttonUp_clicked(self, *args):
        print("move para cima")
    def on_buttonLeft_clicked(self, *args):
        print("move para esquerda")
    def on_buttonDown_clicked(self, *args):
        print("move para baixo")
    def on_buttonRight_clicked(self, *args):
        print("move para direita")
    def on_ButtonIn_clicked(self, *args):
        print("zoom in")
    def on_buttonOut_clicked(self, *args):
        print("zoom out")
    def on_buttonTransladar_clicked(self, *args):
        print("transladar")
    def on_buttonEscalonar_clicked(self, *args):
        print("escalonar")
    def on_buttonRotacionar_clicked(self, *args):
        print("rotacionar")


builder = Gtk.Builder()
builder.add_from_file("CG_T1P1/interface.glade")
builder.connect_signals(Handler())

window = builder.get_object("janelaPrincipal")
window.show_all()

Gtk.main()