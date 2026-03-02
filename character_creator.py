import random as r
from textwrap import wrap

import openpyxl

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

import pygame
from playsound3 import playsound
from PIL import Image, ImageTk
import pygame

import requests

from tkinter.scrolledtext import ScrolledText
"""Funciones"""

def set_nombre():
    ##Lo mismo pero con el nombre
    global nombre
    nombre = nombre_entry.get()

def get_races():
    info_razas = requests.get(BASE_URL + "races").json()["results"]
    razas = []
    for opcion_raza in info_razas:
        razas.append(opcion_raza["name"])
    return razas

def set_races():
    global raza
    raza = raza_combobox.get()
    mostrar_info_raza()
    mostrar_stats()

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

def mostrar_info_raza():
    global tipos_stats, info_raza
    for widget in contenedor_info_raza.winfo_children():
        widget.destroy()
    for widget in contenedor_stats.winfo_children():
        widget.destroy()

    info_raza = requests.get(BASE_URL + "races/" + raza.lower()).json()

    tipos_stats = []

    for i, nombre in enumerate(nombre_stats):
        ttk.Label(contenedor_stats, text=nombre).grid(column=i, row=0, padx=3)

        entry = ttk.Entry(contenedor_stats, width=5, state="readonly", justify="center")
        entry.grid(column=i, row=1, padx=3)

        tipos_stats.append(entry)

    ttk.Label(contenedor_info_raza, text="Speed: " + str(info_raza["speed"])).grid(column=0, row=0, pady=5, sticky="w")
    ttk.Label(contenedor_info_raza, text="Size: " + info_raza["size_description"], wraplength=400).grid(column=0, row=1, pady=5, sticky="w")
    languages = [language["name"] for language in info_raza["languages"]]
    languages_str = ", ".join(languages)
    ttk.Label(contenedor_info_raza, text="Languages: " + languages_str).grid(column=0, row=2, pady=5, sticky="w")
    alignment = info_raza["alignment"]
    ttk.Label(contenedor_info_raza, wraplength=400, text="Alignment: " + alignment).grid(column=0, row=3, pady=5, sticky="w")

    info_caracteristicas = info_raza["traits"]
    for i in range (len(info_caracteristicas)):
        info_caracteristica = requests.get(BASE_URL + "traits/" + info_caracteristicas[i]["index"]).json()
        ttk.Label(contenedor_info_raza, wraplength=500, text=f"{info_caracteristica['name']}: {info_caracteristica['desc']}").grid(column=0, row=4+i, pady=5, sticky="w")

    generate_stats()

def generate_stats():
    global tipos_stats, clase
    minimo_requerido = True
    while minimo_requerido:
        stats = [r.randint(3, 18) for _ in range(6)]
        if sum(stats) >= 72:
            minimo_requerido = False

    stats.sort(reverse=True)

    orden_stats = ["intelligence", "strength", "dexterity", "wisdom", "constitution", "charisma"]

    prioridad = prioridad_stats.get(clase, orden_stats)

    asignacion = {}
    for i in range(6):
        asignacion[prioridad[i]] = stats[i]
    global tipos_stats
    minimo_requerido = False
    stats = []
    while not minimo_requerido:
        sum_stats = 0
        for i in range(6):
            stat = r.randint(3, 18)
            stats.append([tipos_stats_nombres[i], stat])
            sum_stats += stat
        if sum_stats >= 72:
            minimo_requerido = True

    stat_bonuses = get_stat_bonus()
    for stat in stat_bonuses:
        posicion_stat = tipos_stats_nombres.index(stat[0])
        stats[posicion_stat][1] += stat[1]


    for i in range(len(tipos_stats)):
        tipos_stats[i].config(state="normal")
        tipos_stats[i].delete(0, END)
        tipos_stats[i].insert(0, str(stats[i][1]))
        tipos_stats[i].config(state="readonly")
    print(f"Suma total conseguida: {sum_stats}")
    for i, widget in enumerate(tipos_stats):
        stat = orden_stats[i]
        valor = asignacion[stat]

        widget.config(state="normal")
        widget.delete(0, END)
        widget.insert(0, str(valor))
        widget.config(state="readonly")

def get_stat_bonus():
    stats_bonuses = []
    stats_bonuses_json = requests.get(BASE_URL + "races/" + raza.lower()).json()["ability_bonuses"]
    for stat in stats_bonuses_json:
        stats_bonuses.append((stat["ability_score"]["name"], stat["bonus"]))
    return stats_bonuses

def mostrar_stats():
    btn_generate = ttk.Button(contenedor_stats, text="Generate", command=generate_stats)
    btn_generate.grid(column=6, row=1, padx=10)

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

def mostrar_datos():
    set_nombre()
    print(nombre)
    print(clase)
    print(raza)
    print(competencias_habilidades)
    print(competencias_armas)
    print(competencias_herramientas)

root = Tk()
root.title("DnD")
root.geometry("850x850")

style = ttk.Style()
style.theme_use("clam")  # mejor para personalizar


pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("musica.mp3")
sound.set_volume(0.05)
sound.play()

main_container = Frame(root)
main_container.pack(fill='both', expand=True)

canvas = Canvas(main_container, highlightthickness=0, background="white")
scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side='right', fill='y')
canvas.pack(side='left', fill='both', expand=True)

frm = ttk.Frame(canvas, padding=30)
'''fondo_pil = Image.open("./fondo.jpg")
fondo_tk = ImageTk.PhotoImage(fondo_pil)
fondo_id = canvas.create_image(0, 0, image=fondo_tk, anchor="nw")
canvas.imagen_fondo = fondo_tk '''

canvas_frame = canvas.create_window((0, 0), window=frm, anchor="nw")
canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_frame, width=e.width)) ##Hace que el canvas ocpe la pantalla entera entonces se centaran las cosas
frm.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) ##Hace que el frame ocupe el canvas entero jaja
frm.columnconfigure(0, weight=1)
frm.columnconfigure(1, weight=1)

def mover_rueda(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all("<MouseWheel>", mover_rueda)

BASE_URL = "https://www.dnd5eapi.co/api/2014/"

prioridad_stats = {
    "Barbarian": ["strength", "constitution", "dexterity", "wisdom", "charisma", "intelligence"],
    "Fighter": ["strength", "constitution", "dexterity", "wisdom", "charisma", "intelligence"],
    "Paladin": ["strength", "charisma", "constitution", "wisdom", "dexterity", "intelligence"],
    "Rogue": ["dexterity", "intelligence", "charisma", "wisdom", "constitution", "strength"],
    "Wizard": ["intelligence", "constitution", "dexterity", "wisdom", "charisma", "strength"],
    "Cleric": ["wisdom", "constitution", "strength", "charisma", "dexterity", "intelligence"],
    "Ranger": ["dexterity", "wisdom", "constitution", "strength", "intelligence", "charisma"],
    "Sorcerer": ["charisma", "constitution", "dexterity", "wisdom", "intelligence", "strength"],
    "Warlock": ["charisma", "constitution", "dexterity", "wisdom", "intelligence", "strength"],
    "Monk": ["dexterity", "wisdom", "constitution", "strength", "charisma", "intelligence"],
    "Druid": ["wisdom", "constitution", "dexterity", "intelligence", "charisma", "strength"],
    "Bard": ["charisma", "dexterity", "constitution", "wisdom", "intelligence", "strength"]
}
nombre_stats = ["INT", "STR", "DEX", "WIS", "CON", "CHA"]

nombre = ""
clase = ""
raza = ""
info_clase = {}
info_raza = {}
competencias_armas = []
competencias_habilidades = []
competencias_herramientas = []
hit_die = None
tiradas_de_salvacion = []
equipamiento_de_comienzo = []
tipos_stats = []

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
clase_verificar = ttk.Button(frm, text="Verify", command=set_clase)
clase_verificar.grid(column=1, row=5, padx=5, sticky="w")

ttk.Label(frm, text="Select race:").grid(column=0, row=4, pady=(15, 0), columnspan=2)
raza_combobox = Combobox(frm, values=get_races(), state="readonly")
raza_combobox.current(0)
raza_combobox.grid(column=0, row=5, padx=5, sticky="e")

# raza_verificar = ttk.Button(frm, text="Verify race", command=set_races)
# raza_verificar.grid(column=1, row=5, padx=5, sticky="w")

contenedor_competencias = ttk.LabelFrame(frm, text="Competencias", padding="10")
contenedor_competencias.grid(column=0, row=6, columnspan=2, pady=10, sticky="nsew")

contenedor_equipamiento = ttk.LabelFrame(frm, text="Equipamiento Inicial", padding="10")
contenedor_equipamiento.grid(column=0, row=7, columnspan=2, pady=10, sticky="nsew")

contenedor_info_raza = ttk.LabelFrame(frm, text="Info " + raza, padding="10")
contenedor_info_raza.grid(column=0, row=9,columnspan=2, padx=10, sticky="nsew")

contenedor_stats = ttk.LabelFrame(frm, text="Stats", padding="10")
contenedor_stats.grid(column=0, row=8, columnspan=2, pady=10)

contenedor_story = ttk.LabelFrame(frm, text="Tell your story:")
contenedor_story.grid(column=0, row=10, columnspan=2, pady=(10, 0), sticky="nsew")

backstory = ScrolledText(contenedor_story, width=60, height=10)
backstory.pack(padx=10, pady=10)
tipos_stats_nombres = ["INT", "STR", "DEX", "WIS", "CON", "CHA"]

guardar = ttk.Button(frm, text="Guardar personaje", command=mostrar_datos)
guardar.grid(column=0, row=11, columnspan=2, padx=5, sticky="w")
# EXCEL
root_characters = "character.csv"
nombre_personaje = nombre_entry.get()

root.mainloop()