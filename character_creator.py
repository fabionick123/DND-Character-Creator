import json
from stat import FILE_ATTRIBUTE_ARCHIVE

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

import requests

'''!!! No vamos a meter ni multiclases ni subclases !!!'''

root = Tk()
frm = ttk.Frame(root, padding=30)
frm.grid()

BASE_URL = "https://www.dnd5eapi.co/api/2014/"

root.title("DnD")
root.geometry("800x500")

nombre = None
clase = None
info_clase = None
competencias_habilidades = []
competencias_herramientas = []

# Hay que cambiar cosas para que se manejen
# los inputs en Tkinter

opciones_clases =[] ##Usarlo en el campo de opciones de clase para que aparezcan en un menú desplegable y poner un botón de confirmar al lado.
ttk.Label(frm, text="Introduce nombre:").grid(column=0, row=0)
nombre_entry = ttk.Entry(frm, width=30)
nombre_entry.grid(column=0, row=1)

def set_nombre():
    ##Lo mismo pero con el nombre
    print(nombre_entry.get())
    nombre = nombre_entry.get()
    print(nombre)

opciones_clases =[] ##Usarlo en el campo de opciones de clase y poner un botón de confirmar al lado.
opciones = requests.get(BASE_URL + "classes/").json()["results"]
print("Clases disponibles:\n")
for opcion in opciones:
    opciones_clases.append(opcion["name"])

clase_combobox=Combobox(frm, values=opciones_clases, state="readonly")
clase_combobox.grid(column=0, row=3)

def set_clase(): ##funcion a la que llamar al pulsar el botón
    ##Recoger clase escogida en Tkinter y meterla en la variable clase
    print(clase_combobox.get())
    clase = clase_combobox.get()
    info_clase = requests.get(BASE_URL + "classes/" + clase.lower()).json()
    print(info_clase)
    # mostrar_competencias()
    pass

clase_verificar = ttk.Button(frm, text="Verificar Clase", command=set_clase)
clase_verificar.grid(column=1, row=3)

def mostrar_competencias():
    competencias_posibles = info_clase["proficiency_choices"]
    competencias_posibles_nombres = []
    for competencia in competencias_posibles:
        for skill in competencia["from"]["options"]:
            competencias_posibles_nombres.append(skill["item"]["name"])
        for i in range(competencia["choose"]):
            ##Pintar un ttk.combobox con competencias_posibles_nombres
            boton_competencia = ttk.Combobox(frm, values=competencias_posibles_nombres, state="readonly")
            boton_competencia.grid(column=0, row=4 + i)


'''ENCIMA LO QUE SE USA PARA TKINTER'''

def elegir_competencias(info):
    competencias_posibles = info["proficiency_choices"]
    competencias_posibles_nombres = []

    for competencia in competencias_posibles:
        print(competencia["desc"] + "\n")
        competencias_posibles_nombres.clear()
        for skill in competencia["from"]["options"]:
            print(skill["item"]["name"])
            competencias_posibles_nombres.append(skill["item"]["name"])
        for i in range(competencia["choose"]): ##Número de competencias que tiene que elegir
            competencia_valida = False
            competencia_elegida = input(f"Introduzca competencia #{i + 1}:\n>>> ")
            if competencia_elegida in list(map(lambda x: x["from"]["options"]["item"]["name"], competencia)):
                competencia_valida = True
            while not competencia_valida:
                competencia_elegida = input(f"Competencia inválida. Introduzca competencia:\n>>> ")
                if competencia_elegida in list(map(lambda x: x["from"]["options"]["item"]["name"], competencia)):
                    competencia_valida = True
            competencias_habilidades.append(competencia_elegida)




def recoger_info_clase(info):
    hit_die = info["hit_die"]
    competencias_de_comienzo = info["proficiencies"] ##Array de json. Cada elemento tiene index, name, url
    tiradas_de_salvacion = info["saving_throws"] ##Array de json. Cada elemento tiene index, name, url
    equipamiento_de_comienzo = info["starting_equipment"] ## {"equipment": {index, name, url}}


root.mainloop()