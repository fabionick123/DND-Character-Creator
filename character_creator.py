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
contenedor_competencias = ttk.LabelFrame(root, text="Competencias", padding="10")
contenedor_competencias.grid(column=0, row=3, columnspan=2, pady=10)

contenedor_equipamiento = ttk.LabelFrame(root, text="Equipamiento Inicial", padding="10")
contenedor_equipamiento.grid(column=0, row=4, padx=10, pady=10)

BASE_URL = "https://www.dnd5eapi.co/api/2014/"

root.title("DnD")
root.geometry("800x500")

nombre = None
clase = None
info_clase = None
hit_die = None
tiradas_de_salvacion = []
equipamiento_de_comienzo = []
competencias_armas = []
competencias_habilidades = []
# Hay que cambiar cosas para que se manejen
# los inputs en Tkinter

opciones_clases =[] ##Usarlo en el campo de opciones de clase para que aparezcan en un menú desplegable y poner un botón de confirmar al lado.
ttk.Label(frm, text="Introduce nombre:").grid(column=0, row=0)
nombre_entry = ttk.Entry(frm, width=30)
nombre_entry.grid(column=0, row=1)

def set_nombre():
    ##Lo mismo pero con el nombre
    global nombre
    print(nombre_entry.get())
    nombre = nombre_entry.get()
    print(nombre)

opciones_clases =[] ##Usarlo en el campo de opciones de clase y poner un botón de confirmar al lado.
opciones = requests.get(BASE_URL + "classes/").json()["results"]
print("Clases disponibles:\n")
for opcion in opciones:
    opciones_clases.append(opcion["name"])

def set_proficiencias(): ##función que recoge las  proficiencias de cada clase.
    global clase,competencias_armas
    clase = clase_combobox.get()

    competencias = []
    competencias_armas = requests.get(BASE_URL + "classes/" + clase.lower()).json()["proficiencies"]
    for competencia in competencias_armas:
        competencias.append(competencia["name"])
    print(competencias)

clase_combobox=Combobox(frm, values=opciones_clases, state="readonly")
clase_combobox.current(0)
clase_combobox.grid(column=0, row=3, padx=10, pady=20)

def set_clase(): ##funcion a la que llamar al pulsar el botón
    ##Recoger clase escogida en Tkinter y meterla en la variable clase
    global clase, info_clase, hit_die, tiradas_de_salvacion, equipamiento_de_comienzo
    clase = clase_combobox.get()

    info_clase = requests.get(BASE_URL + "classes/" + clase.lower()).json()
    hit_die = info_clase["hit_die"]
    tiradas_de_salvacion_json = info_clase["saving_throws"]

    for tirada in tiradas_de_salvacion_json:
        tiradas_de_salvacion.append(tirada["name"])

    equipamiento_de_comienzo_json = info_clase["starting_equipment"]
    for equipamiento in equipamiento_de_comienzo_json:
        equipamiento_de_comienzo.append((equipamiento["equipment"]["name"], equipamiento["quantity"]))
    print(equipamiento_de_comienzo)

    mostrar_competencias()
    mostrar_equipamiento()
    set_proficiencias()

clase_verificar = ttk.Button(frm, text="Verificar Clase", command=set_clase)
clase_verificar.grid(column=1, row=3)

def mostrar_competencias():
    for widget in contenedor_competencias.winfo_children():
        widget.destroy()
    fila_interna = 0
    for bloque in info_clase["proficiency_choices"]:
        ttk.Label(contenedor_competencias, text=bloque["desc"]).grid(column=0, row=fila_interna, pady=5)
        fila_interna += 1
        opciones_limpias = []

        for opcion_competencia in bloque["from"]["options"]:
            if "item" in opcion_competencia:
                opciones_limpias.append(opcion_competencia["item"]["name"])

            elif "choice" in opcion_competencia:
                sub_lista_competencias = opcion_competencia["choice"]["from"]["options"]
                for sub_opcion in sub_lista_competencias:
                    if "item" in sub_opcion:
                        opciones_limpias.append(sub_opcion["item"]["name"])

        for i in range(bloque["choose"]):
            combo = ttk.Combobox(contenedor_competencias, values=opciones_limpias, state="readonly", width=50)
            combo.grid(column=0, row=fila_interna, pady=2)
            fila_interna += 1

def get_items_from_category(url_categoria):
    data = requests.get("https://www.dnd5eapi.co" + url_categoria).json()
    return [item["name"] for item in data["equipment"]]


def mostrar_equipamiento():
    for widget in contenedor_equipamiento.winfo_children():
        widget.destroy()

    fila = 0
    for bloque in info_clase["starting_equipment_options"]:
        ttk.Label(contenedor_equipamiento, text=bloque["desc"]).grid(column=0, row=fila, pady=(10, 2))
        fila += 1

        opciones_finales = []

        for opcion_equipamiento in bloque["from"]["options"]:
            if opcion_equipamiento["option_type"] == "counted_reference":
                nombre_equipamiento = f"{opcion_equipamiento['count']} {opcion_equipamiento['of']['name']}"
                opciones_finales.append(nombre_equipamiento)

            elif opcion_equipamiento["option_type"] == "choice":
                sub_opcion = opcion_equipamiento["choice"]

                if sub_opcion["from"]["option_set_type"] == "equipment_category":
                    url_opcion = sub_opcion["from"]["equipment_category"]["url"]
                    lista_items = get_items_from_category(url_opcion)
                    for item in lista_items:
                        opciones_finales.append(item)

                elif sub_opcion["from"]["option_set_type"] == "options_array":
                    for sub_opcion_segunda in sub_opcion["from"]["options"]:
                        if "item" in sub_opcion_segunda:
                            opciones_finales.append(sub_opcion_segunda["item"]["name"])
                        elif "of" in sub_opcion_segunda:
                            opciones_finales.append(f"{sub_opcion_segunda['count']} {sub_opcion_segunda['of']['name']}")

        for i in range(bloque["choose"]):
            combo = ttk.Combobox(contenedor_equipamiento, values=opciones_finales, state="readonly", width=60)
            combo.grid(column=0, row=fila, pady=2)
            fila += 1


'''ENCIMA LO QUE SE USA PARA TKINTER'''


root.mainloop()