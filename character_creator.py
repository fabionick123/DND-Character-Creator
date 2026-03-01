import json
from stat import FILE_ATTRIBUTE_ARCHIVE

import requests

'''!!! No vamos a meter ni multiclases ni subclases !!!'''

BASE_URL = "https://www.dnd5eapi.co/api/2014/"

nombre = None
clase = None
competencias_habilidades = []
competencias_herramientas = []

# Hay que cambiar cosas para que se manejen
# los inputs en Tkinter

opciones_clases =[] ##Usarlo en el campo de opciones de clase y poner un botón de confirmar al lado.
opciones = requests.get(BASE_URL + "classes/").json()["results"]
print("Clases disponibles:\n")
for opcion in opciones:
    opciones_clases.append(opcion["name"])

def set_clase(): ##funcion a la que llamar al pulsar el botón
    ##Recoger clase escogida en Tkinter y meterla en la variable clase
    pass

def set_nombre():
    ##Lo mismo pero con el nombre
    pass



'''ENCIMA LO QUE SE USA PARA TKINTER'''
def elegir_clase():
    clase_valida = False
    info_clase = None
    clases = requests.get(BASE_URL + "classes/").json()["results"]
    print("Clases disponibles:\n")
    for clase in clases:
        print(clase["name"])

    clase_elegida = input("Introduzca clase:\n>>> ").lower()

    while not clase_valida:
        try:
            info_clase = requests.get(BASE_URL + "classes/" + clase_elegida).json()
            clase_valida = True
        except requests.exceptions.RequestException as e:
            print("Clase inválida. Introdúzcala de nuevo:")
            clase_elegida = input(">>> ").lower()
    return info_clase

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


elegir_competencias(elegir_clase())