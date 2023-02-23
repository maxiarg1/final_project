import re
import sqlite3
from tkinter import messagebox
from tkinter.messagebox import showerror
from peewee import *
import tkinter as tk
from my_observer import Subject


db = SqliteDatabase("mydb.db")


class BaseModel(Model):
    class Meta:
        database = db



class Formulario(BaseModel):
    fecha = DateField(unique=False)
    nombre = CharField()
    apellido = CharField()


db.connect()
db.create_tables([Formulario])


class Crud(Subject):
    def __init__(
        self,
    ):
        pass

    def confirmacion_consulta(func):
        def wrapper(*args, **kwargs):
            if messagebox.askokcancel("Confirmación", "¿Está seguro de que desea realizar la consulta?"):
                return func(*args, **kwargs)
        return wrapper
#-----------------------------------------alta registro-----------------------------------------
    def alta(self, fecha_1, nombre_1, apellido_1, tree):
        if messagebox.askyesno(
            message="Usted esta por cargar un nuevo registro, desea continuar?",
            title="Advertencia",
        ):
            nombre_cadena = nombre_1.get()
            apellido_cadena = apellido_1.get()
            patron = "^[A-Za-z0-9áéíóúñÑ,! \.]*$"  
            if re.match(patron, nombre_cadena) and re.match(patron, apellido_cadena):
                formularios = Formulario()
                formularios.fecha = fecha_1.get()
                formularios.nombre = nombre_cadena
                formularios.apellido = apellido_cadena
                formularios.save()
                self.actualizar_treeview(tree)
                self.delete_fields(nombre_1, apellido_1)
                messagebox.showinfo(
                    "Operación exitosa", "Usted ha cargado un nuevo registro"
                )
            else:
                showerror(
                    "Error en Carga del registro ",
                    "Solo se permite en ´Descripción del registro´ la carga de caracteres:\n alfanuméricos (incluida la 'ñ') \n '.' (punto)\n ',' (coma)\n ' '(espacio en blanco)\n ",
                )
                self.delete_fields(nombre_1, apellido_1)
        else:
            self.delete_fields(nombre_1, apellido_1)
#-----------------------------------------consulta-----------------------------------------
    @confirmacion_consulta
    def consultar_pantalla(self, date_val, name_val, lname_val, tree):
        records = tree.get_children()
        for element in records:
            tree.delete(element)
        for fila in Formulario.select():
            tree.insert("", 0, text=fila.id, values=(fila.fecha, fila.nombre, fila.apellido))

#-----------------------------------------modificar registro-----------------------------------------
   
    def modificar(self, fecha_1, nombre_1, apellido_1, tree):
        if messagebox.askyesno(
            message="El registro seleccionado será modificado definitivamente, desea continuar?",
            title="Advertencia",
        ):
            cadena = nombre_1.get()
            patron = "^[A-Za-z0-9áéíóúñÑ,! \.]*$"
            if re.match(patron, cadena):
                valor = tree.selection()
                item = tree.item(valor)
                actualizar = Formulario.update(
                    fecha=fecha_1.get(),
                    nombre=nombre_1.get(),
                    apellido=apellido_1.get(),
                ).where(Formulario.id == item["text"])
                actualizar.execute()
                self.actualizar_treeview(tree)
                self.delete_fields(nombre_1, apellido_1)
                messagebox.showinfo("Operación exitosa", "Usted ha modificado el registro")
            else:
                showerror(
                    "Error en la modificación del registro",
                    "Solo se permite en ´Descripción de registro la carga de caracteres:\n alfanuméricos (incluida la 'ñ') \n '.' (punto)\n ',' (coma)\n ' '(espacio en blanco)\n ",
                )
                self.delete_fields(nombre_1)
                self.delete_fields(apellido_1)
        else:
            self.delete_fields(nombre_1)
            self.delete_fields(apellido_1)

#-------------------------------------borrar---------------------------------------------------------

    def borrar(self, tree):
        if messagebox.askyesno(
            message="El registro se perderá definitivamente, desea continuar?",
            title="Advertencia",
        ):
            valor = tree.selection()
            item = tree.item(valor)
            borrar = Formulario.get(Formulario.id == item["text"])
            borrar.delete_instance()
            tree.delete(valor)
            messagebox.showinfo("Operación exitosa", "Usted ha eliminado el registro")
        else:
            pass

#-----------------------------actualizar treeview------------------------------
    def actualizar_treeview(self, mytreeview):
        records = mytreeview.get_children()
        for element in records:
            mytreeview.delete(element)
        for fila in Formulario.select():
            mytreeview.insert(
                "", 0, text=fila.id, values=(fila.fecha, fila.nombre, fila.apellido)
            )

    #borrar campos cada vez que ocurre una modificacion
    def delete_fields(self, nombre_1, apellido_1):
        nombre_1.set("")
        apellido_1.set("")

    def limiter(self, c_val):
        if len(c_val.get()) > 0:
            c_val.set(c_val.get()[:125])



