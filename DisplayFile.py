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

  def limpar(self):
    DisplayFile.listaObjetos.clear()
    for i, _ in enumerate(DisplayFile.objetos):
      del DisplayFile.objetos[i]

  def getObjeto(self, nome_objeto):
    for i, o in enumerate(DisplayFile.objetos):
      if o.nome == nome_objeto:
        return DisplayFile.objetos[i]