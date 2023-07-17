from tkinter import *
from tkinter import ttk
from connection import *

TABLA_MEDICAMENTOS = "medicamentos"

ventana = Tk()
ventana.title("Crud Medicamentos")
ventana.geometry("420x515")

db=Database()
modificar=False
nombre=StringVar()
precio=StringVar()

def seleccionar(event):
    id= tvMedicamentos.selection()[0]
    if int(id)>0:
        nombre.set(tvMedicamentos.item(id,"values")[1])
        precio.set(tvMedicamentos.item(id,"values")[2])

marco = LabelFrame(ventana, text="Formulario de Gestion de Medicamentos")
marco.place(x=50,y=50, width=320, height=415)

#Entradas

lblNombre=Label(marco, text="Nombre: ").grid(column=0, row=0,padx=5, pady=5)
txtNombre=Entry(marco, textvariable=nombre)
txtNombre.grid(column=1, row=0)

lblPrecio=Label(marco, text="Precio: ").grid(column=0, row=1,padx=5, pady=5)
txtPrecio=Entry(marco, textvariable=precio)
txtPrecio.grid(column=1, row=1)


txtMensaje=Label(marco, text="", fg="green")
txtMensaje.grid(column=0, row= 2,columnspan=4)

#Mostrar

tvMedicamentos= ttk.Treeview(marco,selectmode= NONE)
tvMedicamentos.grid(column=0,row=3,columnspan=4,padx=4, pady=5)
tvMedicamentos["columns"] = ("ID","NOMBRE", "PRECIO")
tvMedicamentos.column("#0", width=0, stretch=NO )
tvMedicamentos.column("ID", width=50, anchor=CENTER )
tvMedicamentos.column("NOMBRE", width=150, anchor=CENTER )
tvMedicamentos.column("PRECIO", width=60, anchor=CENTER )

tvMedicamentos.heading("#0", text="")
tvMedicamentos.heading("ID", text="ID", anchor=CENTER )
tvMedicamentos.heading("NOMBRE", text="NOMBRE", anchor=CENTER )
tvMedicamentos.heading("PRECIO", text="PRECIO", anchor=CENTER )
tvMedicamentos.bind("<<TreeviewSelect>>", seleccionar)

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
    tvMedicamentos.config(selectmode= NONE)
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)

def modificarTrue():
    global modificar
    modificar=True
    tvMedicamentos.config(selectmode= BROWSE)
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)

def validar():
    return len(nombre.get())>0 and len(precio.get())>0

def limpiar():
    nombre.set("")
    precio.set("")

def vaciarTabla():
    filas=tvMedicamentos.get_children()
    for fila in filas:
        tvMedicamentos.delete(fila)

def llenarTabla():
    vaciarTabla()
    sql= "select * from "+TABLA_MEDICAMENTOS
    db.cursor.execute(sql)
    filas=db.cursor.fetchall()
    for fila in filas:
        id=fila[0]
        tvMedicamentos.insert("", END, id, text=id, values=fila)

def eliminar():
    id=tvMedicamentos.selection()[0]
    if int(id)>0:
        sql="delete from "+TABLA_MEDICAMENTOS+" where id="+id
        db.cursor.execute(sql)
        db.connection.commit()
        tvMedicamentos.delete(id)
        txtMensaje.config(text="Se ha eliminado el registro correctamente")
        limpiar()
    else:
        txtMensaje.config(text="Seleccione un registro para eliminar")


def agregar():
    if modificar==False:
        if validar():
            val= (nombre.get(), precio.get())
            sql= "insert into "+TABLA_MEDICAMENTOS+" (nombre, precio) values (%s,%s)"
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
            val= (nombre.get(), precio.get())
            id=tvMedicamentos.selection()[0]
            sql= "update "+TABLA_MEDICAMENTOS+" set nombre=%s, precio=%s where id="+id
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