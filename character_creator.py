import json
import random as r
from asyncio.windows_events import NULL
from stat import FILE_ATTRIBUTE_ARCHIVE

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

import requests

'''!!! No vamos a meter ni multiclases ni subclases !!!'''

<<<<<<< master
root = Tk()
frm = ttk.Frame(root, padding=30)
frm.place(relx=0.5, rely=0.2, anchor="center")
contenedor_competencias = ttk.Frame(frm)
contenedor_competencias.grid(column=0, row=4, columnspan=2, pady=10)

BASE_URL = "https://www.dnd5eapi.co/api/2014/"

root.title("DnD")
root.geometry("800x500")
root.update()

ancho = 800
alto = 500

x = (root.winfo_screenwidth() // 2) - (ancho // 2)
y = (root.winfo_screenheight() // 2) - (alto // 2)

root.geometry(f"{ancho}x{alto}+{x}+{y}")

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
nombre_entry.grid(column=0, row=1)
=======
"""Funciones"""
>>>>>>> master

def set_nombre():
    ##Lo mismo pero con el nombre
    global nombre
    print(nombre_entry.get())
    nombre = nombre_entry.get()
    print(nombre)




def set_races():
    global all_razas
    razas = []
    all_razas = requests.get(BASE_URL + "races").json()["results"]
    for raza in all_razas:
        razas.append(raza["name"])
    print(razas)

def set_proficiencias(): ##función que recoge las  proficiencias de cada clase.
    global clase,competencias_armas
    clase = clase_combobox.get()

    competencias = []
    competencias_armas = requests.get(BASE_URL + "classes/" + clase.lower()).json()["proficiencies"]
    for competencia in competencias_armas:
        competencias.append(competencia["name"])
    print(competencias)

def set_clase(): ##funcion a la que llamar al pulsar el botón
    ##Recoger clase escogida en Tkinter y meterla en la variable clase
    global clase, info_clase
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
    set_races()

def set_proficiencias(): ##función que recoge las  proficiencias de cada clase.
    global clase,competencias_armas

    competencias = []
    competencias_armas = requests.get(BASE_URL + "classes/" + clase.lower()).json()["proficiencies"]
    for competencia in competencias_armas:
        competencias.append(competencia["name"])
    competencias.pop()
    competencias.pop()
    print(competencias)


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



root = Tk()
frm = ttk.Frame(root, padding=30)
frm.grid()
contenedor_competencias = ttk.LabelFrame(root, text="Competencias", padding="10")
contenedor_competencias.grid(column=0, row=3, columnspan=2, pady=10)
contenedor_equipamiento = ttk.LabelFrame(root, text="Equipamiento Inicial", padding="10")
contenedor_equipamiento.grid(column=0, row=4, padx=10, pady=10)

contenedor_stats = ttk.LabelFrame(root, text="Stats", padding="10")
contenedor_stats.grid(column=0, row=6, pady=10)

BASE_URL = "https://www.dnd5eapi.co/api/2014/"

root.title("DnD")
root.geometry("800x500")

nombre = None
clase = None
info_clase = None
competencias_armas = []
competencias_habilidades = []
competencias_herramientas = []
hit_die = None
tiradas_de_salvacion = []
equipamiento_de_comienzo = []

# Hay que cambiar cosas para que se manejen
# los inputs en Tkinter

opciones_clases =[] ##Usarlo en el campo de opciones de clase para que aparezcan en un menú desplegable y poner un botón de confirmar al lado.
ttk.Label(frm, text="Introduce nombre:").grid(column=0, row=0)
nombre_entry = ttk.Entry(frm, width=30)
nombre_entry.insert(0, "Nombre")
nombre_entry.grid(column=0, row=1)

opciones = requests.get(BASE_URL + "classes/").json()["results"]
print("Clases disponibles:\n")
for opcion in opciones:
    opciones_clases.append(opcion["name"])

ttk.Label(frm, text="Elige clase:").grid(column=0, row=2, pady=(15, 0))

clase_combobox=Combobox(frm, values=opciones_clases, state="readonly")
clase_combobox.current(0)
clase_combobox.grid(column=0, row=3)

clase_verificar = ttk.Button(frm, text="Verificar Clase", command=set_clase)
clase_verificar.grid(column=1, row=3)

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

root.update()

x = (root.winfo_screenwidth() // 2) - (800 // 2)
y = (root.winfo_screenheight() // 2) - (500 // 2)

root.geometry(f"800x500+{x}+{y}")
root.mainloop()