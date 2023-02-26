from textwrap import fill
from tkinter import W
from tkinter import CENTER
from tkinter import Label
from tkinter import StringVar
from tkinter import Entry
from tkinter import Button
from tkinter import ttk
import tkinter as tk
from model import Crud
from tkcalendar import DateEntry
from tkinter import messagebox



class MyView:
    def __init__(self, ventana) -> None:
        self.root = ventana
        self.root.title("Formulario")
        self.root.config(bg="#F5EDF7")
        self.root.geometry("1200x600")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.resizable(0, 0)
        self.obj = Crud()

        self.fecha_1 = Label(self.root, text="Fecha:", font=("Roboto", 9))
        self.fecha_1.grid(
            row=1, 
            column=1, 
            sticky="", 
            padx=1, 
            pady=2)

        self.nombre = Label(self.root, text="Nombre:", font=("Roboto", 9))
        self.nombre.grid(
            row=2,
            column=1,
            sticky="",
            padx=1,
            pady=2,
        )

        self.apellido = Label(self.root, text="Apellido:", font=("Roboto", 9))
        self.apellido.grid(
            row=3,
            column=1,
            sticky="",
            padx=1,
            pady=2,
        )

        #---------------------Defino variables---------------------

        self.date_val, self.name_val, self.lname_val = StringVar(), StringVar(), StringVar()

        self.name_val.trace("w", lambda *args: self.obj.limiter(self.name_val))

        self.lname_val.trace("w", lambda *args: self.obj.limiter(self.lname_val))

        self.entrada1 = DateEntry(
            self.root,
            textvariable=self.date_val,
            width=20,
            font=("Roboto", 9),
            date_pattern="dd/mm/yyyy",
            arrowcolor="white",
            firstweekday="sunday",
            weekendbackground="pink",
            justify="center",
        )

        self.entrada1.grid(row=1, 
        column=2, 
        sticky=W, 
        padx=1, 
        pady=2,
        ipady=4)

        self.entrada2 = Entry(self.root, textvariable=self.name_val, width=115)
        self.entrada2.grid(
            row=2, 
            column=2, 
            columnspan=4, 
            sticky=W, 
            padx=1, 
            pady=22, 
            ipady=4
        )

        self.entrada3 = Entry(self.root, textvariable=self.lname_val, width=115)
        self.entrada3.grid(
            row=3, 
            column=2, 
            columnspan=4, 
            sticky=W, 
            padx=1, 
            pady=22, 
            ipady=4
        )
        
        #---------------------Asignacion de botones---------------------
        #boton para crear registro
        self.create_button = Button(
            self.root,
            text="Crear",
            command=lambda: self.obj.alta(
                self.date_val, self.name_val, self.lname_val, self.tree
            ),
            font=("Roboto", 9),
            width=25,
            activebackground="#F2EDFF",
            activeforeground="#4CD269",
        )
        self.create_button.grid(row=6, column=1, padx=10, pady=5, sticky="")
        #-------------------------------------------------------------
        #boton para consultar la db; si esta vacia la consulta trae toda la db sino busca lo seleccionado

        self.read_button = Button(
            self.root,
            text="Buscar",
            command=lambda: self.obj.consultar_pantalla(
                self.date_val, self.name_val, self.lname_val, self.tree
            ),
            font=("Roboto", 10),
            width=22,
            activebackground="#F2EDFF",
            activeforeground="#4CD269",
        )
        self.read_button.grid(row=7, column=1, padx=10, pady=5, sticky="")
        #-------------------------------------------------------------
        #boton para modificar registro en la db
        self.update_button = Button(
            self.root,
            text="Modificar",
            command=lambda: self.obj.modificar(
            self.date_val, self.name_val, self.lname_val, self.tree
        ) if self.tree.selection() else messagebox.showinfo("Error", "Primero deberá seleccionar un elemento para modificar"),
            font=("Roboto", 9),
            width=25,
            activebackground="#F2EDFF",
            activeforeground="#DBCB1A",
        )
        self.update_button.grid(row=8, column=1, padx=10, pady=5, sticky="")

        #--------------------------------------------------------------
        #Boton para borrar registro.
        self.delete_button = Button(
            self.root,
            text="Borrar",
            command=lambda: self.obj.borrar(self.tree),
            font=("Roboto", 9),
            width=25,
            activebackground="#F2EDFF",
            activeforeground="#B30600",
        )
        self.delete_button.grid(row=9, column=1, padx=10, pady=5, sticky="") 
        

        #---------------------Treeview---------------------
        self.tree = ttk.Treeview(self.root)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        self.tree["columns"] = ("col1", "col2", "col3")
        self.tree.column("#0", width=50, minwidth=50, anchor=W)
        self.tree.column("col1", width=90, minwidth=80, anchor=CENTER)
        self.tree.column("col2", width=400, minwidth=80, anchor=CENTER)
        self.tree.column("col3", width=400, minwidth=80, anchor=CENTER)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Fecha")
        self.tree.heading("col2", text="Nombre")
        self.tree.heading("col3", text="Apellido")
        self.tree["show"] = "headings"
        self.tree.grid(row=6, column=2, columnspan=4, rowspan=4, sticky=W, padx=1, pady=5, ipady=4)

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=6, column=4, sticky="ns")

        self.tree.configure(yscrollcommand=scrollbar.set)

    def on_tree_select(self, event):
        try:
            # Obtener el elemento seleccionado del treeview
            item = self.tree.selection()[0]
            
            # Obtener los valores de las columnas del elemento seleccionado
            values = self.tree.item(item, "values")
            
            # Establecer el valor del entry
            self.entrada1.delete(0, tk.END)
            self.entrada2.delete(0, tk.END)
            self.entrada3.delete(0, tk.END)
            self.entrada1.insert(0, values[0])
            self.entrada2.insert(0, values[1])
            self.entrada3.insert(0, values[2])
        except:
            pass
