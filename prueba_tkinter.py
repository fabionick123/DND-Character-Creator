from tkinter import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=20)
frm.grid()

root.title("prueba")
root.geometry("800x500")

ttk.Label(frm, text="Hello World!").grid(column=0, row=0)

texto = ttk.Entry(frm, width=30)
texto.grid(column=0, row=1)

def al_hacer_click():
    print("Se presionó el botón")
    print("Contenido del Entry:", texto.get())

boton = ttk.Button(frm, text="Click me!", command=al_hacer_click)
boton.grid(column=1, row=0)

ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=1)

root.mainloop()