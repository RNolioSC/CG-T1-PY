import gi
import cairo
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from DisplayFile import DisplayFile
from Window import Window, Viewport
from Figuras import Poligono
from DescritorOBj import DescritorOBj
from Normaliza import Normaliza
from Variaveis import clipping_border_size as cbz

class Handler:
    display_file = DisplayFile()
    pontos = []

    def __init__(self, builder, drawing_area):
        self.builder = builder
        self.drawing_area = drawing_area
        self.normaliza = Normaliza()
        self.descritorOBj = DescritorOBj()
        self.window_object = builder.get_object("janelaNovoObjeto")
        self.window_transform_object = builder.get_object("janelaTransformarObjeto")
        self.window_choose_file = builder.get_object("janelaEscolherObj")
        
        da_largura = self.drawing_area.get_allocation().width
        da_altura = self.drawing_area.get_allocation().height

        self.tree_view = self.builder.get_object("treeObjetos")
        self.window = Window(-cbz, -cbz, da_largura - cbz, da_altura - cbz)
        self.viewport = Viewport(-cbz, -cbz, da_largura - cbz, da_altura - cbz)
        
        self.normaliza.setWindow(self.window)
        self.viewport.setWindow(self.window)
        self.display_file.setBuilder(builder)

        self.radio_rotacionar_mundo = self.builder.get_object("radioRotacionarMundo")
        self.radio_rotacionar_objeto = self.builder.get_object("radioRotacionarObjeto")
        self.radio_rotacionar_ponto = self.builder.get_object("radioRotacionarPonto")

    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_buttonNovoObjeto_clicked(self, *args):
        self.pontos = []
        window_object = self.builder.get_object("janelaNovoObjeto")
        window_object.show_all()

    def on_buttonCriarDesenharPonto_clicked(self, *args):
        name_entry = self.builder.get_object("entryNomeObjeto")
        x_entry = self.builder.get_object("spinXPonto")
        y_entry = self.builder.get_object("spinYPonto")
        p = Poligono(name_entry.get_text()) 
        p.addPonto(int(x_entry.get_text()), int(y_entry.get_text()))
        p.setTipo("ponto")

        self.display_file.addObjeto(p)
        self.window_object.hide()

    def on_buttonCriarDesenharReta_clicked(self, *args):
        name_entry = self.builder.get_object("entryNomeObjeto")
        x_entry = self.builder.get_object("spinXInicialReta")
        y_entry = self.builder.get_object("spinYInicialReta")
        x_final_entry = self.builder.get_object("spinXFinalReta")
        y_final_entry = self.builder.get_object("spinYFinalReta")
        p = Poligono(name_entry.get_text()) 
        p.addPonto(int(x_entry.get_text()), int(y_entry.get_text()))
        p.addPonto(int(x_final_entry.get_text()), int(y_final_entry.get_text()))
        p.setTipo("reta")
        
        self.display_file.addObjeto(p)
        self.window_object.hide()

    def on_buttonAdicionarPontoPoligono_clicked(self, *args):
        x_entry = self.builder.get_object("spinXPoligono")
        y_entry = self.builder.get_object("spinYPoligono")
        self.pontos.append([x_entry.get_text(), y_entry.get_text(), 1])
        print('Ponto - x: {}, y: {} adicionado'.format(int(x_entry.get_text()), int(y_entry.get_text())))

    def on_buttonCriarDesenharPoligono_clicked(self, *args):
        name_entry = self.builder.get_object("entryNomeObjeto")
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
        self.window_object.hide()

    def on_buttonDeletarObjeto_clicked(self, *args):
        obj_lista, i = self.tree_view.get_selection().get_selected()
        if i != None:
          self.display_file.removeObjeto(obj_lista[i][0])
          obj_lista.remove(i)
          self.redraw(self.drawing_area)

    def on_buttonTransformarObjeto_clicked(self, *args):
        _, i = self.tree_view.get_selection().get_selected()
        if i != None:
          window_transform_object = self.builder.get_object("janelaTransformarObjeto")
          window_transform_object.show_all()

    def on_buttonUp_clicked(self, *args):
        passo = self.builder.get_object("spinPasso")
        self.window.move(0, int(passo.get_text()))
        self.redraw(self.drawing_area)

    def on_buttonLeft_clicked(self, *args):
        passo = self.builder.get_object("spinPasso")
        self.window.move(-int(passo.get_text()), 0)
        self.redraw(self.drawing_area)

    def on_buttonDown_clicked(self, *args):
        passo = self.builder.get_object("spinPasso")
        self.window.move(0, -int(passo.get_text()))
        self.redraw(self.drawing_area)

    def on_buttonRight_clicked(self, *args):
        passo = self.builder.get_object("spinPasso")
        self.window.move(int(passo.get_text()), 0)
        self.redraw(self.drawing_area)

    def on_ButtonIn_clicked(self, *args):
        passo = self.builder.get_object("spinPasso")
        porcentagem = 1 + (int(passo.get_text()) / 100)
        self.window.zoom(porcentagem)
        self.redraw(self.drawing_area)

    def on_buttonOut_clicked(self, *args):
        passo = self.builder.get_object("spinPasso")
        porcentagem = 1 - (int(passo.get_text()) / 100)
        self.window.zoom(porcentagem)
        self.redraw(self.drawing_area)

    def on_buttonRotacionaEsquerda_clicked(self, *args):
        angulo = int(self.builder.get_object("spinAnguloWindow").get_text())
        self.window.rotate(angulo)
        self.redraw(self.drawing_area)

    def on_buttonRotacionaDireita_clicked(self, *args):
        angulo = int(self.builder.get_object("spinAnguloWindow").get_text())
        self.window.rotate(-angulo)
        self.redraw(self.drawing_area)

    def on_buttonTransladar_clicked(self, *args):
        obj_lista, i = self.tree_view.get_selection().get_selected()
        obj = self.display_file.getObjeto(obj_lista[i][0])
        dx = self.builder.get_object("spinXVetorTrans")
        dy = self.builder.get_object("spinYVetorTrans")
        obj.translacao(int(dx.get_text()), int(dy.get_text()))
        self.window_transform_object.hide()
        self.redraw(self.drawing_area)

    def on_buttonEscalonar_clicked(self, *args):
        obj_lista, i = self.tree_view.get_selection().get_selected()
        obj = self.display_file.getObjeto(obj_lista[i][0])
        dx = self.builder.get_object("spinXFatorEscala")
        dy = self.builder.get_object("spinYFatorEscala")
        centro = obj.centroGeo()
        obj.escalona(int(dx.get_text()), int(dy.get_text()), centro)
        self.window_transform_object.hide()
        self.redraw(self.drawing_area)

    def on_buttonRotacionar_clicked(self, *args):
        obj_lista, i = self.tree_view.get_selection().get_selected()
        obj = self.display_file.getObjeto(obj_lista[i][0])
        angulo = self.builder.get_object("spinAngulo")
        if self.radio_rotacionar_mundo.get_active():
          obj.rotacionaMundo(int(angulo.get_text()))
        elif self.radio_rotacionar_objeto.get_active():
          centro = obj.centroGeo()
          obj.rotacionaObj(int(angulo.get_text()), centro)
        elif self.radio_rotacionar_ponto.get_active():
          dx = self.builder.get_object("spinXRotacionarPonto")
          dy = self.builder.get_object("spinYRotacionarPonto")
          obj.rotacionaPonto(int(dx.get_text()), int(dy.get_text()), int(angulo.get_text()))
        self.window_transform_object.hide()
        self.redraw(self.drawing_area)

    def on_buttonImportarObj_clicked(self, *args):
        self.window_choose_file.show_all()

    def on_buttonExportarObj_clicked(self, *args):
        self.descritorOBj.exportFile("./file.obj")

    def on_buttonAbrirArquivo_clicked(self, *args):
        file_path = self.window_choose_file.get_filename()
        self.descritorOBj.importFile(file_path)
        self.window_choose_file.hide()

    def on_buttonCancelarImportacao_clicked(self, *args):
        self.window_choose_file.hide()

    def drawBackground(self, drawing_area, ctx, *args):
        ctx.set_source_rgb(255, 255, 255)  # color white
        ctx.paint()

    def drawClippingBorder(self, drawing_area, ctx, *args):
        ctx.set_line_width(2)
        ctx.set_source_rgb(255, 0, 0) # color red

        ctx.move_to(cbz, cbz)
        ctx.line_to(self.window.getLargura() - cbz, cbz)
        ctx.line_to(self.window.getLargura() - cbz, self.window.getAltura() - cbz)
        ctx.line_to(cbz, self.window.getAltura() - cbz)

        ctx.close_path()
        ctx.stroke()

    def on_myDrawingArea_draw(self, drawing_area, ctx, *args):
        self.drawBackground(drawing_area, ctx)
        ctx.set_line_width(2)
        ctx.set_source_rgb(0, 0, 0)  # color black
        
        for objeto in self.display_file.getObjetos():
            print('Desenhando objeto "{}"'.format(objeto.getNome()))
            objeto.drawToViewport(ctx, self.viewport)
        
        ctx.stroke()
        self.drawClippingBorder(drawing_area, ctx)
            
    def redraw(self, drawing_area, *args):
        drawing_area.queue_draw()