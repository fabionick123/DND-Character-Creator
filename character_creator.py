import json
import random as r
from asyncio.windows_events import NULL
from stat import FILE_ATTRIBUTE_ARCHIVE

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

import requests

'''!!! No vamos a meter ni multiclases ni subclases !!!'''

root = Tk()
frm = ttk.Frame(root, padding=30)
frm.grid()
contenedor_competencias = ttk.Frame(frm)
contenedor_competencias.grid(column=0, row=4, columnspan=2, pady=10)
contenedor_stats = ttk.Frame(frm)
contenedor_stats.grid(column=0, row=5, columnspan=2, pady=10)

BASE_URL = "https://www.dnd5eapi.co/api/2014/"

root.title("DnD")
root.geometry("800x500")

nombre = None
clase = None
info_clase = None
competencias_armas = []
competencias_habilidades = []
competencias_herramientas = []

# Hay que cambiar cosas para que se manejen
# los inputs en Tkinter

opciones_clases =[] ##Usarlo en el campo de opciones de clase para que aparezcan en un menú desplegable y poner un botón de confirmar al lado.
ttk.Label(frm, text="Introduce nombre:").grid(column=0, row=0)
nombre_entry = ttk.Entry(frm, width=30)
nombre_entry.insert(0, "Nombre")
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
    competencias_armas = requests.get(BASE_URL + "classes/monk").json()["proficiencies"]
    for competencia in competencias_armas:
        competencias.append(competencia["name"])
    print(competencias)

ttk.Label(frm, text="Elige clase:").grid(column=0, row=2, pady=(15, 0))
clase_combobox=Combobox(frm, values=opciones_clases, state="readonly")
clase_combobox.current(0)
clase_combobox.grid(column=0, row=3)

def set_clase(): ##funcion a la que llamar al pulsar el botón
    ##Recoger clase escogida en Tkinter y meterla en la variable clase
    global clase, info_clase
    clase = clase_combobox.get()

    info_clase = requests.get(BASE_URL + "classes/" + clase.lower()).json()
    mostrar_competencias()
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
            combo.current(i)
            combo.grid(column=0, row=fila_interna, pady=2)
            fila_interna += 1

def generate_stats():
    stats_tipos = [intelligence, strength, dexterity, wisdom, constitution, charisma]
    minimo_requerido = False
    while not minimo_requerido:
        sum_stats = 0
        stats = []
        for i in range(6):
            stat = r.randint(3, 18)
            stats.append(stat)
            sum_stats += stat
        if sum_stats >= 72:
            minimo_requerido = True

    for i in range(len(stats_tipos)):
        stats_tipos[i].config(state="normal")
        stats_tipos[i].delete(0, END)
        stats_tipos[i].insert(0, str(stats[i]))
        stats_tipos[i].config(state="readonly")
    print(f"Suma total conseguida: {sum_stats}")

contenedor_stats.config(cursor="target")

ttk.Label(contenedor_stats, text="INT", width=5).grid(column=1, row=3, pady=3)
intelligence = ttk.Entry(contenedor_stats, width=5)
intelligence.grid(column=1, row=4, padx=3)

ttk.Label(contenedor_stats, text="STR", width=5).grid(column=2, row=3, pady=3)
strength = ttk.Entry(contenedor_stats, width=5)
strength.grid(column=2, row=4, padx=3)

ttk.Label(contenedor_stats, text="DEX", width=5).grid(column=3, row=3, pady=3)
dexterity = ttk.Entry(contenedor_stats, width=5)
dexterity.grid(column=3, row=4, padx=3)

ttk.Label(contenedor_stats, text="WIS", width=5).grid(column=4, row=3, pady=3)
wisdom = ttk.Entry(contenedor_stats, width=5)
wisdom.grid(column=4, row=4, padx=3)

ttk.Label(contenedor_stats, text="CON", width=5).grid(column=5, row=3, pady=3)
constitution = ttk.Entry(contenedor_stats, width=5)
constitution.grid(column=5, row=4, padx=3)

ttk.Label(contenedor_stats, text="CHA", width=5).grid(column=6, row=3, pady=3)
charisma = ttk.Entry(contenedor_stats, width=5)
charisma.grid(column=6, row=4, padx=3)

ttk.Button(contenedor_stats, text="Generate", command=generate_stats).grid(column=7, row=4, padx=5, pady=5)


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