from tkinter import *
from tkinter import ttk
from connection import *

TABLA_ANIMALES = "animal"

ventana = Tk()
ventana.title("Crud Animales")
ventana.geometry("350x515")

db=Database()
modificar=False
especie=StringVar()
peso=StringVar()

def seleccionar(event):
    id= tvAnimales.selection()[0]
    if int(id)>0:
        especie.set(tvAnimales.item(id,"values")[1])
        peso.set(tvAnimales.item(id,"values")[2])

marco = LabelFrame(ventana, text="Formulario de Gestion de Animales")
marco.place(x=50,y=50, width=250, height=415)

#Entradas

lblEspecie=Label(marco, text="Especie: ").grid(column=0, row=0,padx=5, pady=5)
txtEspecie=Entry(marco, textvariable=especie)
txtEspecie.grid(column=1, row=0)

lblPeso=Label(marco, text="Peso: ").grid(column=0, row=1,padx=5, pady=5)
txtPeso=Entry(marco, textvariable=peso)
txtPeso.grid(column=1, row=1)


txtMensaje=Label(marco, text="", fg="green")
txtMensaje.grid(column=0, row= 2,columnspan=4)

#Mostrar

tvAnimales= ttk.Treeview(marco,selectmode= NONE)
tvAnimales.grid(column=0,row=3,columnspan=4,padx=4, pady=5)
tvAnimales["columns"] = ("ID","ESPECIE", "PESO")
tvAnimales.column("#0", width=0, stretch=NO )
tvAnimales.column("ID", width=50, anchor=CENTER )
tvAnimales.column("ESPECIE", width=80, anchor=CENTER )
tvAnimales.column("PESO", width=60, anchor=CENTER )

tvAnimales.heading("#0", text="")
tvAnimales.heading("ID", text="ID", anchor=CENTER )
tvAnimales.heading("ESPECIE", text="ESPECIE", anchor=CENTER )
tvAnimales.heading("PESO", text="PESO", anchor=CENTER )
tvAnimales.bind("<<TreeviewSelect>>", seleccionar)

#Buttons
btnEliminar= Button(marco, text="Eliminar",command=lambda:eliminar())
btnEliminar.grid(column=0,row=4,padx=5, pady=5)
btnNuevo= Button(marco, text="Guardar",command=lambda:agregar())
btnNuevo.grid(column=1,row=4,padx=5, pady=5)
btnModificar= Button(marco, text="Seleccionar",command=lambda:editar())
btnModificar.grid(column=0,row=5,padx=5, pady=5)
btnVolver= Button(marco, text="Volver",command=lambda:volver())
btnVolver.grid(column=1,row=5,padx=5, pady=5)
#Funciones

def modificarFalse():
    global modificar
    modificar=False
    tvAnimales.config(selectmode= NONE)
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)

def modificarTrue():
    global modificar
    modificar=True
    tvAnimales.config(selectmode= BROWSE)
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)

def validar():
    return len(especie.get())>0 and len(peso.get())>0

def limpiar():
    especie.set("")
    peso.set("")

def vaciarTabla():
    filas=tvAnimales.get_children()
    for fila in filas:
        tvAnimales.delete(fila)

def llenarTabla():
    vaciarTabla()
    sql= "select * from "+TABLA_ANIMALES
    db.cursor.execute(sql)
    filas=db.cursor.fetchall()
    for fila in filas:
        id=fila[0]
        tvAnimales.insert("", END, id, text=id, values=fila)

def eliminar():
    id=tvAnimales.selection()[0]
    if int(id)>0:
        sql="delete from "+TABLA_ANIMALES+" where id="+id
        db.cursor.execute(sql)
        db.connection.commit()
        tvAnimales.delete(id)
        txtMensaje.config(text="Se ha eliminado el registro correctamente")
        limpiar()
    else:
        txtMensaje.config(text="Seleccione un registro para eliminar")


def agregar():
    if modificar==False:
        if validar():
            val= (especie.get(), peso.get())
            sql= "insert into "+TABLA_ANIMALES+" (especie, peso) values (%s,%s)"
            db.cursor.execute(sql,val)
            db.connection.commit()
            txtMensaje.config(text="Registro guardado correctamente", fg="green")
            llenarTabla()
            limpiar()
        else:
            txtMensaje.config(text="Los campos no deben estar vacios", fg="red")
    else:
        modificarFalse()


def editar():
    if modificar==True:
        if validar():
            val= (especie.get(), peso.get())
            id=tvAnimales.selection()[0]
            sql= "update "+TABLA_ANIMALES+" set especie=%s, peso=%s where id="+id
            db.cursor.execute(sql,val)
            db.connection.commit()
            txtMensaje.config(text="Registro actualizado correctamente", fg="green")
            llenarTabla()
            limpiar()
        else:
            txtMensaje.config(text="Los campos no deben estar vacios", fg="red")
    else:
        modificarTrue()
def volver():
    ventana.destroy()

llenarTabla()
ventana.mainloop()