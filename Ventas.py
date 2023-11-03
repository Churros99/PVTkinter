from tkinter import *
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import sqlite3


class Ventana (tb.Window):
    
    def __init__(self) :
        super().__init__()
        self.Ventana_login()
        
    def Ventana_login(self):
        self.frame_login= Frame(self)
        self.frame_login.pack()
        
        self.lblframe_login = ttk.LabelFrame(self.frame_login,text='Acceso')
        self.lblframe_login.pack(padx=10, pady=10)
        
        lbltitulo = ttk.Label(self.lblframe_login, text='Inicio de Sesion', font=('Arial',22))
        lbltitulo.pack(padx=10, pady=35)
        
        self.txt_usuario = ttk.Entry(self.lblframe_login, width=40, justify=CENTER)
        self.txt_usuario.pack(padx=10, pady=10)
        self.txt_clave = ttk.Entry(self.lblframe_login, width=40, justify=CENTER)
        self.txt_clave.pack(padx=10, pady=10)
        self.txt_clave.config(show='*')
        self.btn_acceso = ttk.Button(self.lblframe_login, text='Ingresar',width=38, command=self.logueo)
        self.btn_acceso.pack(padx=10, pady=10)
    
    def Ventana_menu(self):
        self.frame_left = Frame(self, width=200)
        self.frame_left.grid(row=0, column=0, sticky=NSEW)
         
        self.frame_center = Frame(self)
        self.frame_center.grid(row=0, column=1, sticky=NSEW)
         
        self.frame_right = Frame(self, width=400)
        self.frame_right.grid(row=0, column=2, sticky=NSEW)
         
        btn_productos = ttk.Button(self.frame_left, text='Productos', width=15)
        btn_productos.grid(row=0, column=0, padx=10, pady=10)
        btn_ventas = ttk.Button(self.frame_left, text='Ventas', width=15)
        btn_ventas.grid(row=1, column=0, padx=10, pady=10)
        btn_clientes = ttk.Button(self.frame_left, text='Clientes', width=15)
        btn_clientes.grid(row=2, column=0, padx=10, pady=10)
        btn_Compras = ttk.Button(self.frame_left, text='Compras', width=15)
        btn_Compras.grid(row=3, column=0, padx=10, pady=10)
        btn_usuarios = ttk.Button(self.frame_left, text='Usuarios', width=15, command=self.Ventana_lista_usuarios)
        btn_usuarios.grid(row=4, column=0, padx=10, pady=10)
        btn_reportes = ttk.Button(self.frame_left, text='Reportes', width=15)
        btn_reportes.grid(row=5, column=0, padx=10, pady=10)
        btn_backup = ttk.Button(self.frame_left, text='Backup', width=15)
        btn_backup.grid(row=6, column=0, padx=10, pady=10)
        btn_restaurarbd = ttk.Button(self.frame_left, text='Restaurar DB', width=15)
        btn_restaurarbd.grid(row=7, column=0, padx=10, pady=10)
        
        lbl2 = Label(self.frame_center, text='Aqui pondremos las ventanas que creemos')
        lbl2.grid(row=0,column=0, padx=10, pady=10)
        
        lbl1 = Label(self.frame_right, text='Aqui pondremos las busquedas para la venta')
        lbl1.grid(row=0,column=0, padx=10, pady=10)
        
    def Ventana_lista_usuarios(self):
        self.frame_lista_usuarios = Frame(self.frame_center)
        self.frame_lista_usuarios.grid(row=0,column=0,columnspan=2, sticky=NSEW)
        
        self.lblframe_botones_listusu = LabelFrame(self.frame_lista_usuarios)
        self.lblframe_botones_listusu.grid(row=0,column=0, padx=10, pady=10, sticky=NSEW)
        
        btn_nuevo_usuario = tb.Button(self.lblframe_botones_listusu, text='Nuevo', width=15, bootstyle="success")
        btn_nuevo_usuario.grid(row=0, column=0, padx=5, pady=5)
        btn_modificar_usuario = tb.Button(self.lblframe_botones_listusu, text='Modificar', width=15, bootstyle="warning")
        btn_modificar_usuario.grid(row=0, column=1, padx=5, pady=5)
        btn_eliminar_usuario = tb.Button(self.lblframe_botones_listusu, text='Eliminar', width=15, bootstyle="danger")
        btn_eliminar_usuario.grid(row=0, column=2, padx=5, pady=5)
        
        self.lblframe_busqueda_listusu = LabelFrame(self.frame_lista_usuarios, width=50)
        self.lblframe_busqueda_listusu.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
        
        txt_busqueda_usuarios = ttk.Entry(self.lblframe_busqueda_listusu, width=100)
        txt_busqueda_usuarios.grid(row=0,column=0, padx=5, pady=5)
        
        #=========================== treeview ===================================#
        self.lblframe_tree_listusu = LabelFrame(self.frame_lista_usuarios)
        self.lblframe_tree_listusu.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        columnas = ("codigo","nombre", "clave", "rol")
        self.tree_lista_usuarios = tb.Treeview(self.lblframe_tree_listusu, columns= columnas, height=17, show='headings', bootstyle='dark')
        self.tree_lista_usuarios.grid(row=0, column=0)
        
        self.tree_lista_usuarios.heading("codigo", text="Codigo", anchor='w')
        self.tree_lista_usuarios.heading("nombre", text="Nombre", anchor='w')
        self.tree_lista_usuarios.heading("clave", text="Clave", anchor='w')
        self.tree_lista_usuarios.heading("rol", text="Rol", anchor='w')
        self.tree_lista_usuarios['displaycolumns'] = ("codigo","nombre", "rol")
        
        # Crea el scrollbar
        tree_scroll_listausu= tb.Scrollbar(self.frame_lista_usuarios, bootstyle='round-success')
        tree_scroll_listausu.grid(row=2, column=1)
        
        # Cnfigurar el scrollbar
        tree_scroll_listausu.config(command=self.tree_lista_usuarios.yview)
        
        self.mostrar_usuarios()
        
    def mostrar_usuarios(self):
        try:
            miConexion = sqlite3.connect("ventas.db")
            miCursor = miConexion.cursor()
            registros = self.tree_lista_usuarios.get_children()
            for elemento in registros:
                self.tree_lista_usuarios.delete(elemento)
            miCursor.execute("select * from Usuarios")
            datos = miCursor.fetchall()
            
            for row in datos:
                self.tree_lista_usuarios.insert("",0,text=row[0],values=(row[0], row[1], row[2], row[3]))
            
            miConexion.commit()
            miConexion.close()
            
        except:
            
            messagebox.showerror("Lista de usuarios","ocurrio un error al mostrar la lista de usuario")
        
    def logueo(self):
        self.frame_login.pack_forget() # Aqui ocultamos la ventana Login
        self.Ventana_menu() # Aqui abrimos nuestra ventana menu
          
def main():
    app = Ventana()
    app.title('Sistema de Ventas')
    app.state('zoomed')
    tb.Style('superhero')
    app.mainloop()
        
    
if __name__ == '__main__':
    main()