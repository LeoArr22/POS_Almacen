import sys
import os

# Obtiene el directorio actual del script en ejecución
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtiene el directorio raíz de POS_Almacen
pos_almacen_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Agrega la subcarpeta 'DATA' al path
data_dir = os.path.join(pos_almacen_dir, "DATA")
sys.path.append(data_dir)



import customtkinter as ctk
from tkinter.font import BOLD
from GUI.util.generic import centrar_ventana, leer_imagen
from DATA.CRUD.crud_usuarios import CRUD_usuario
from DATA.SQL.engine import *


class LoginApp:
    def __init__(self):
        self.ventana = ctk.CTk()  #Crea la ventana principal
        self.ventana.title('Login')
        centrar_ventana(self.ventana, 700, 500)
        self.ventana.resizable(width=0, height=0)
        
        self.frame_fondo = ctk.CTkFrame(self.ventana, width=700, height=500)
        self.frame_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        #Coloca la imagen de fondo en el Frame
        self.fondo = leer_imagen("./POS_Almacen/GUI/login/dibujo-monje.png", (700, 500))
        self.fondo_label = ctk.CTkLabel(self.frame_fondo, image=self.fondo, text="")
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        #Etiqueta de bienvenida
        etiqueta_bienvenida = ctk.CTkLabel(self.frame_fondo, text="BIENVENIDO", text_color="#F3920F",
                                           fg_color="#1C2124", font=('Carlito', 50, BOLD))
        etiqueta_bienvenida.place(relx=0.57, rely=0.1)  # Ajuste de posición

        #Etiqueta de usuario
        etiqueta_usuario = ctk.CTkLabel(self.frame_fondo, text="Usuario", text_color="#F3920F",
                                         fg_color="#1C2124", bg_color="#1C2124", font=('Helvetica', 20))
        etiqueta_usuario.place(relx=0.71, rely=0.3)  # Ajuste de posición

        # Variable para el usuario
        self.var_usuario = ctk.StringVar()

        #Campo de entrada para el usuario
        self.usuario = ctk.CTkEntry(self.frame_fondo, textvariable=self.var_usuario, width=300, font=('Helvetica', 20),
                                    bg_color="#1C2124", fg_color='#1C2124', text_color="#D5D0D4", 
                                    border_width=1, border_color="#F3920F", corner_radius=20)
        self.usuario.place(relx=0.55, rely=0.355)
        
        #Etiqueta de contraseña
        etiqueta_contrasena = ctk.CTkLabel(self.frame_fondo, text="Contraseña", text_color="#F3920F",
                                         fg_color="#1C2124", bg_color="#1C2124", font=('Helvetica', 20))
        etiqueta_contrasena.place(relx=0.69, rely=0.455)  # Ajuste de posición

        #Variable para el campo de entrada de usuario
        self.var_contrasena = ctk.StringVar()

        #Campo de entrada para la contraseña
        self.contrasena = ctk.CTkEntry(self.frame_fondo, textvariable=self.var_contrasena, width=300, font=('Helvetica', 20),
                                    bg_color="#1C2124", fg_color='#1C2124', text_color="#D5D0D4", show="*",
                                    border_width=1, border_color="#F3920F", corner_radius=20)
        self.contrasena.place(relx=0.55, rely=0.510)

        #Boton de login
        btn_login = ctk.CTkButton(self.frame_fondo, command=self.logear, font=('Helvetica', 20, BOLD), text="Iniciar Sesión", 
                                  text_color="#F3920F", bg_color='#1C2124', fg_color='#1C2124', hover_color="#D5D0D4",
                                  border_width=2, border_color="#F3920F")
        btn_login.place(relx=0.65, rely=0.7) 
        
        # Ejecutar la ventana
        self.ventana.mainloop()
        
    def logear(self):
        usuario = self.var_usuario.get()
        contrasena = int(self.var_contrasena.get())
        
        with Session() as session:
            crud_usuario=CRUD_usuario(session)
            
            if crud_usuario.verificar_contrasena(usuario, contrasena):
                print("LOGEADO")
            else:
                etiqueta_error_login = ctk.CTkLabel(self.frame_fondo, text="Credenciales Incorrectas", font=('Helvetica', 20, BOLD),
                                                    text_color="#D40000", bg_color="#1C2124", fg_color="#1C2124")
                etiqueta_error_login.place(relx=0.59, rely=0.8)
                


# Inicializar la aplicación
LoginApp()
