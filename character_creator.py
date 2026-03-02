import random as r

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

import requests

"""Funciones"""

def set_nombre():
    ##Lo mismo pero con el nombre
    global nombre
    print(nombre_entry.get())
    nombre = nombre_entry.get()
    print(nombre)

def get_races():
    info_razas = requests.get(BASE_URL + "races").json()["results"]
    razas = []
    for opcion_raza in info_razas:
        razas.append(opcion_raza["name"])
    return razas

def set_races():
    global raza
    raza = raza_combobox.get()
    mostrar_stats()
    mostrar_info_raza()

def mostrar_info_raza():
    for widget in contenedor_info_raza.winfo_children():
        widget.destroy()
    info_raza = requests.get(BASE_URL + "races/" + raza.lower()).json()
    ttk.Label(contenedor_info_raza, text="Velocidad: " + str(info_raza["speed"])).grid(column=0, row=0, pady=5, sticky="w")

def set_clase():
    global clase, info_clase
    clase = clase_combobox.get()

    info_clase = requests.get(BASE_URL + "classes/" + clase.lower()).json()
    mostrar_competencias()
    mostrar_equipamiento()
    set_proficiencias()
    set_races()

def set_proficiencias():
    global clase, competencias_armas
    competencias = []
    competencias_armas = requests.get(BASE_URL + "classes/" + clase.lower()).json()["proficiencies"]
    for competencia in competencias_armas:
        competencias.append(competencia["name"])
    if len(competencias) >= 2:
        competencias.pop()
        competencias.pop()
    print(competencias)

def generate_stats(tipos):
    global stats, sum_stats
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

    for i in range(len(tipos)):
        tipos[i].config(state="normal")
        tipos[i].delete(0, END)
        tipos[i].insert(0, str(stats[i]))
        tipos[i].config(state="readonly")
    print(f"Suma total conseguida: {sum_stats}")

def mostrar_stats():

    contenedor_stats = ttk.LabelFrame(frm, text="Stats", padding="10")
    contenedor_stats.grid(column=0, row=8, columnspan=2, pady=10)

    intelligence = ttk.Entry(contenedor_stats, width=5, state="readonly", justify="center")
    intelligence.grid(column=0, row=1, padx=3)

    strength = ttk.Entry(contenedor_stats, width=5, state="readonly", justify="center")
    strength.grid(column=1, row=1, padx=3)

    dexterity = ttk.Entry(contenedor_stats, width=5, state="readonly", justify="center")
    dexterity.grid(column=2, row=1, padx=3)

    wisdom = ttk.Entry(contenedor_stats, width=5, state="readonly", justify="center")
    wisdom.grid(column=3, row=1, padx=3)

    constitution = ttk.Entry(contenedor_stats, width=5, state="readonly", justify="center")
    constitution.grid(column=4, row=1, padx=3)

    charisma = ttk.Entry(contenedor_stats, width=5, state="readonly", justify="center")
    charisma.grid(column=5, row=1, padx=3)

    btn_generate = ttk.Button(contenedor_stats, text="Generate", command=generate_stats)
    btn_generate.grid(column=6, row=1, padx=10)

    stats_tipos = [intelligence, strength, dexterity, wisdom, constitution, charisma]
    generate_stats(stats_tipos)

def mostrar_competencias():
    for widget in contenedor_competencias.winfo_children():
        widget.destroy()
    fila_interna = 0
    for bloque in info_clase["proficiency_choices"]:
        ttk.Label(contenedor_competencias, text=bloque["desc"]).grid(column=0, row=fila_interna, pady=5, sticky="w")
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
            combo.current(0)
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
        ttk.Label(contenedor_equipamiento, text=bloque["desc"]).grid(column=0, row=fila, pady=(10, 2), sticky="w")
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
            combo.current(0)
            combo.grid(column=0, row=fila, pady=2)
            fila += 1



root = Tk()
root.title("DnD")
root.geometry("850x850")

frm = ttk.Frame(root, padding=30)
frm.pack(expand=True)
frm.columnconfigure(0, weight=1)
frm.columnconfigure(1, weight=1)

BASE_URL = "https://www.dnd5eapi.co/api/2014/"


nombre = None
clase = ""
raza = ""
info_clase = None
competencias_armas = []
competencias_habilidades = []
competencias_herramientas = []
hit_die = None
tiradas_de_salvacion = []
equipamiento_de_comienzo = []

ttk.Label(frm, text="Introduce nombre:").grid(column=0, row=0,columnspan=2)
nombre_entry = ttk.Entry(frm, width=30)
nombre_entry.insert(0, "name")
nombre_entry.grid(column=0, row=1, columnspan=2, pady=5)


opciones_clases =[] ##Usarlo en el campo de opciones de clase y poner un botón de confirmar al lado.
opciones = requests.get(BASE_URL + "classes/").json()["results"]
# print("Clases disponibles:\n")
for opcion in opciones:
    opciones_clases.append(opcion["name"])

ttk.Label(frm, text="Select class:").grid(column=0, row=2, pady=(15, 0), columnspan=2)
clase_combobox = Combobox(frm, values=opciones_clases, state="readonly")
clase_combobox.current(0)
clase_combobox.grid(column=0, row=3, padx=5, sticky="e")
clase_verificar = ttk.Button(frm, text="Verify Class", command=set_clase)
clase_verificar.grid(column=1, row=3, padx=5, sticky="w")

ttk.Label(frm, text="Select race:").grid(column=0, row=4, pady=(15, 0), columnspan=2)
raza_combobox = Combobox(frm, values=get_races(), state="readonly")
raza_combobox.current(0)
raza_combobox.grid(column=0, row=5, padx=5, sticky="e")

raza_verificar = ttk.Button(frm, text="Verify race", command=set_races)
raza_verificar.grid(column=1, row=5, padx=5, sticky="w")

contenedor_competencias = ttk.LabelFrame(frm, text="Competencias", padding="10")
contenedor_competencias.grid(column=0, row=6, columnspan=2, pady=10, sticky="nsew")

contenedor_equipamiento = ttk.LabelFrame(frm, text="Equipamiento Inicial", padding="10")
contenedor_equipamiento.grid(column=0, row=7, columnspan=2, pady=10, sticky="nsew")

contenedor_info_raza = ttk.LabelFrame(frm, text="Info " + raza, padding="10")
contenedor_info_raza.grid(column=0, row=9,columnspan=2, padx=10, sticky="nsew")

root.mainloop()