from tkinter import *
from tkinter import ttk
from connection import *

TABLA_HITOS = "hitos"
TABLA_REGISTRO_RECORRIDO = "registro_recorrido"

ventana = Tk()
ventana.title("Hitos Lugares")
ventana.geometry("400x550")

db=Database()
modificar=False
fecha=StringVar()
observacion=StringVar()
lugaresID = {} #Dictionary

def seleccionar(event):
    id= tvHitos.selection()[0]
    if int(id)>0:
        observacion.set(tvHitos.item(id,"values")[1])
        fecha.set(tvHitos.item(id,"values")[2])

def obtenerLugares():
    sql= "select * from "+TABLA_REGISTRO_RECORRIDO
    db.cursor.execute(sql)
    filas=db.cursor.fetchall()
    for fila in filas:
        key=fila[1]
        value=fila[0]
        lugaresID[key]=value

def option_selected(event):
    llenarTabla()

marco = LabelFrame(ventana, text="Formulario de Gestion de Hitos")
marco.place(x=50,y=50, width=300, height=450)

#Entradas
obtenerLugares()

lblLugares=Label(marco, text="Lugar: ").grid(column=0, row=0,padx=5, pady=5)
valuesFormLugares=list(lugaresID.keys())
txtLugares=ttk.Combobox(marco, values= valuesFormLugares)
txtLugares.grid(column=1, row=0)
txtLugares.current(0)
txtLugares.bind("<<ComboboxSelected>>", option_selected)

lblObservacion=Label(marco, text="Observacion: ").grid(column=0, row=2,padx=5, pady=5)
txtObservacion=Entry(marco, textvariable=observacion)
txtObservacion.grid(column=1, row=2)

lblFecha=Label(marco, text="Fecha: ").grid(column=0, row=3,padx=5, pady=5)
txtFecha=Entry(marco, textvariable=fecha)
txtFecha.grid(column=1, row=3)

txtMensaje=Label(marco, text="", fg="green")
txtMensaje.grid(column=0, row= 4,columnspan=4)

#Mostrar

tvHitos= ttk.Treeview(marco,selectmode= NONE)
tvHitos.grid(column=0,row=1,columnspan=4,padx=4, pady=5)
tvHitos["columns"] = ("ID","OBSERVACION", "FECHA")
tvHitos.column("#0", width=0, stretch=NO )
tvHitos.column("ID", width=50, anchor=CENTER )
tvHitos.column("OBSERVACION", width=150, anchor=CENTER )
tvHitos.column("FECHA", width=75, anchor=CENTER )

tvHitos.heading("#0", text="")
tvHitos.heading("ID", text="ID", anchor=CENTER )
tvHitos.heading("OBSERVACION", text="OBSERVACION", anchor=CENTER )
tvHitos.heading("FECHA", text="FECHA", anchor=CENTER )
tvHitos.bind("<<TreeviewSelect>>", seleccionar)

#Buttons
btnEliminar= Button(marco, text="Eliminar",command=lambda:eliminar())
btnEliminar.grid(column=0,row=6,padx=5,pady=5)
btnNuevo= Button(marco, text="Guardar",command=lambda:agregar())
btnNuevo.grid(column=1,row=6,padx=5,pady=5)
btnModificar= Button(marco, text="Seleccionar",command=lambda:editar())
btnModificar.grid(column=0,row=7,padx=5,pady=5)
btnVolver= Button(marco, text="Volver",command=lambda:volver())
btnVolver.grid(column=1,row=7,padx=5,pady=5)

#Funciones

def modificarFalse():
    global modificar
    modificar=False
    tvHitos.config(selectmode= NONE)
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)

def modificarTrue():
    global modificar
    modificar=True
    tvHitos.config(selectmode= BROWSE)
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)

def validar():
    return len(observacion.get())>0 and len(fecha.get())>0

def limpiar():
    observacion.set("")
    fecha.set("")

def vaciarTabla():
    filas=tvHitos.get_children()
    for fila in filas:
        tvHitos.delete(fila)

def llenarTabla():
    vaciarTabla()
    sql= "select * from "+TABLA_HITOS+" where id_lugar_hito = "+str(lugaresID[txtLugares.get()])
    db.cursor.execute(sql)
    filas=db.cursor.fetchall()
    for fila in filas:
        id=fila[0]
        tvHitos.insert("", END, id, text=id, values=fila)

def eliminar():
    id=tvHitos.selection()[0]
    if int(id)>0:
        sql="delete from "+TABLA_HITOS+" where id_hito="+id
        db.cursor.execute(sql)
        db.connection.commit()
        tvHitos.delete(id)
        txtMensaje.config(text="Se ha eliminado el registro correctamente")
        limpiar()
    else:
        txtMensaje.config(text="Seleccione un registro para eliminar")


def agregar():
    if modificar==False:
        if validar():
            val= (observacion.get(), fecha.get())
            print(lugaresID[txtLugares.get()])
            sql= "insert into "+TABLA_HITOS+" (observacion,fecha,id_lugar_hito) values (%s,%s,"+ str(lugaresID[txtLugares.get()]) +")"
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
            val= (observacion.get(), fecha.get())
            id=tvHitos.selection()[0]
            sql= "update "+TABLA_HITOS+" set observacion=%s, fecha=%s where id_hito="+id
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