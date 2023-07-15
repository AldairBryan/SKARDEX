from tkinter import *
from tkinter import ttk
from connection import *

TABLA_REGISTRO_RECORRIDO = "registro_recorrido"

ventana = Tk()
ventana.title("Crud Registro Recorrido")
ventana.geometry("700x500")

db=Database()
modificar=False
lugares=StringVar()
orden=StringVar()
tiempo=StringVar()
categoria=StringVar()
precio=StringVar()

def seleccionar(event):
    id= tvLugares.selection()[0]
    if int(id)>0:
        lugares.set(tvLugares.item(id,"values")[1])
        orden.set(tvLugares.item(id,"values")[2])
        tiempo.set(tvLugares.item(id,"values")[3])
        categoria.set(tvLugares.item(id,"values")[4])
        precio.set(tvLugares.item(id,"values")[5])

marco = LabelFrame(ventana, text="Formulario de Gestion de Registro Recorrido")
marco.place(x=50,y=50, width=600, height=400)

#Entradas

lblLugares=Label(marco, text="Lugar: ").grid(column=0, row=0,padx=5, pady=5)
txtLugares=Entry(marco, textvariable=lugares)
txtLugares.grid(column=1, row=0)

lblOrden=Label(marco, text="Orden: ").grid(column=0, row=1,padx=5, pady=5)
txtOrden=Entry(marco, textvariable=orden)
txtOrden.grid(column=1, row=1)

lblTiempo=Label(marco, text="Tiempo: ").grid(column=2, row=0,padx=5, pady=5)
txtTiempo=Entry(marco, textvariable=tiempo)
txtTiempo.grid(column=3, row=0)

lblCategoria=Label(marco, text="Categoria: ").grid(column=2, row=1,padx=5, pady=5)
txtCategoria=Entry(marco, textvariable=categoria)
txtCategoria.grid(column=3, row=1)

lblPrecio=Label(marco, text="Precio: ").grid(column=4, row=0,padx=5, pady=5)
txtPrecio=Entry(marco, textvariable=precio)
txtPrecio.grid(column=5, row=0)

txtMensaje=Label(marco, text="a", fg="green")
txtMensaje.grid(column=0, row= 2,columnspan=4)

#Mostrar

tvLugares= ttk.Treeview(marco,selectmode= NONE)
tvLugares.grid(column=0,row=3,columnspan=4,padx=4, pady=5)
tvLugares["columns"] = ("ID","LUGARES", "ORDEN", "TIEMPO", "CATEGORIA", "PRECIO")
tvLugares.column("#0", width=0, stretch=NO )
tvLugares.column("ID", width=50, anchor=CENTER )
tvLugares.column("LUGARES", width=80, anchor=CENTER )
tvLugares.column("ORDEN", width=60, anchor=CENTER )
tvLugares.column("TIEMPO", width=60, anchor=CENTER )
tvLugares.column("CATEGORIA", width=100, anchor=CENTER )
tvLugares.column("PRECIO", width=70, anchor=CENTER )

tvLugares.heading("#0", text="")
tvLugares.heading("ID", text="ID", anchor=CENTER )
tvLugares.heading("LUGARES", text="LUGARES", anchor=CENTER )
tvLugares.heading("ORDEN", text="ORDEN", anchor=CENTER )
tvLugares.heading("TIEMPO", text="TIEMPO", anchor=CENTER )
tvLugares.heading("CATEGORIA", text="CATEGORIA", anchor=CENTER )
tvLugares.heading("PRECIO", text="PRECIO", anchor=CENTER )
tvLugares.bind("<<TreeviewSelect>>", seleccionar)

#Buttons
btnEliminar= Button(marco, text="Eliminar",command=lambda:eliminar())
btnEliminar.grid(column=1,row=6)
btnNuevo= Button(marco, text="Guardar",command=lambda:agregar())
btnNuevo.grid(column=2,row=6)
btnModificar= Button(marco, text="Seleccionar",command=lambda:editar())
btnModificar.grid(column=3,row=6)

#Funciones

def modificarFalse():
    global modificar
    modificar=False
    tvLugares.config(selectmode= NONE)
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)

def modificarTrue():
    global modificar
    modificar=True
    tvLugares.config(selectmode= BROWSE)
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)

def validar():
    return len(lugares.get())>0 and len(orden.get())>0 and len(tiempo.get())>0 and len(categoria.get())>0 and len(precio.get())>0

def limpiar():
    lugares.set("")
    orden.set("")
    tiempo.set("")
    categoria.set("")
    precio.set("")

def vaciarTabla():
    filas=tvLugares.get_children()
    for fila in filas:
        tvLugares.delete(fila)

def llenarTabla():
    vaciarTabla()
    sql= "select * from "+TABLA_REGISTRO_RECORRIDO
    db.cursor.execute(sql)
    filas=db.cursor.fetchall()
    for fila in filas:
        id=fila[0]
        tvLugares.insert("", END, id, text=id, values=fila)

def eliminar():
    id=tvLugares.selection()[0]
    if int(id)>0:
        sql="delete from "+TABLA_REGISTRO_RECORRIDO+" where id_registro_recorrido="+id
        db.cursor.execute(sql)
        db.connection.commit()
        tvLugares.delete(id)
        txtMensaje.config(text="Se ha eliminado el registro correctamente")
        limpiar()
    else:
        txtMensaje.config(text="Seleccione un registro para eliminar")


def agregar():
    if modificar==False:
        if validar():
            val= (lugares.get(), orden.get(), tiempo.get(), categoria.get(), precio.get())
            sql= "insert into "+TABLA_REGISTRO_RECORRIDO+" (lugar, orden, tiempo, categoria, precio) values (%s,%s,%s,%s,%s)"
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
            val= (lugares.get(), orden.get(), tiempo.get(), categoria.get(), precio.get())
            id=tvLugares.selection()[0]
            sql= "update "+TABLA_REGISTRO_RECORRIDO+" set lugar=%s, orden=%s, tiempo=%s, categoria=%s, precio=%s where id_registro_recorrido="+id
            db.cursor.execute(sql,val)
            db.connection.commit()
            txtMensaje.config(text="Registro actualizado correctamente", fg="green")
            llenarTabla()
            limpiar()
        else:
            txtMensaje.config(text="Los campos no deben estar vacios", fg="red")
    else:
        modificarTrue()

llenarTabla()
ventana.mainloop()
