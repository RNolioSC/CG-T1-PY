import re
from DisplayFile import DisplayFile
from Figuras import Poligono

class DescritorOBj:
  def __init__(self):
    self.DisplayFile = DisplayFile()

  def importFile(self, path):
    self.DisplayFile.limpar()
    vertices = dict()
    vertice_counter = 0
    nome = ""

    self.file = open(path, "r+")  # read and write

    for line in self.file:
      if(line[0] == "v"): # store vertices in a dictionary
        vertice_counter += 1
        vertices[vertice_counter] = line

      elif(line[0] == "o"):
        match = re.findall(r"\S+", line)
        nome = match[1]
      
      elif(line[0] == "p"):
        match = re.findall(r"\S+", line)
        vertice_for_point = vertices[float(match[1])]
        match = re.findall(r"\S+", vertice_for_point)
        coord = [float(match[1]), float(match[2]) ]

        p1 = Poligono(nome)
        p1.addPonto(coord[0], coord[1])
        p1.setTipo("ponto")
        self.DisplayFile.addObjeto(p1)
      
      elif(line[0] == "l"):
        match = re.findall(r"\S+", line)
        l = Poligono(nome)

        for item in match:
          if(item != "l"):
            vertice_for_point = vertices[float(item)]
            match = re.findall(r"\S+", vertice_for_point)
            coord = [float(match[1]), float(match[2])]
            l.addPonto(coord[0], coord[1])

        if int(len(l.getPontos())) > 2:
            l.setTipo("poligono")
        elif int(len(l.getPontos())) == 2:
            l.setTipo("reta")
        self.DisplayFile.addObjeto(l)
  
  def exportFile(self, path):
    output_file = open(path, "w+") # write, overwrite and create if needed
    temp = "" # this variable holds the objects related to the vertices
    vertice_counter = 0

    for obj in DisplayFile.objetos:
      tipo_obj = obj.getTipo()
      pontos_m = obj.getPontosMundo()

      if(tipo_obj == "ponto"):
        vertice_counter += 1
        output_file.write("v {} {} 0\n".format(pontos_m[0][0], pontos_m[0][1]))
        
        temp += "o {}\n".format(obj.getNome())
        temp += "p {}\n".format(vertice_counter)
      
      elif(tipo_obj == "linha"):
        vertice_counter += 1
        output_file.write("v {} {} 0\n".format(pontos_m[0][0], pontos_m[0][1]))
        vertice_counter += 1
        output_file.write("v {} {} 0\n".format(pontos_m[1][0], pontos_m[1][1]))
        
        temp += "o {}\n".format(obj.getNome())
        temp += "l {} {}\n".format(vertice_counter-1, vertice_counter)
      
      elif(tipo_obj == "poligono"):
        temp += "o {}\n".format(obj.getNome())
        temp += "l"

        for ponto in pontos_m:
          vertice_counter += 1
          output_file.write("v {} {} 0\n".format(ponto[0], ponto[1]))
          temp += " {}".format(vertice_counter)
        temp += "\n"

    output_file.write("{}\n".format(temp))
    output_file.close()
