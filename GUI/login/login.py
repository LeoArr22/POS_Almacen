import json
from data.sql.engine import *
from data.crud.crud_usuarios import CRUD_usuario
from gui.util.generic import leer_imagen, centrar_ventana
from gui.master.master import MasterPanel

import customtkinter as ctk
from tkinter.font import BOLD

class LoginApp:
    def __init__(self):
        self.ventana = ctk.CTk()  # Crea la ventana principal
        self.ventana.title('Login')
        centrar_ventana(self.ventana, 700, 500)
        self.ventana.resizable(width=0, height=0)
        self.etiqueta_error_login = None

        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.ventana, width=700, height=500)
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)

        # Revisar si mostrar mensaje inicial
        if not self.verificar_mensaje_mostrado():
            self.crear_usuario_admin()
            self.mostrar_mensaje_inicial()
        else:
            self.mostrar_login()

        # Ejecutar la ventana
        self.ventana.mainloop()

    def verificar_mensaje_mostrado(self):
        """Verifica si el mensaje inicial ya fue mostrado."""
        try:
            with open("config.json", "r") as archivo:
                config = json.load(archivo)
            return config.get("mensaje_mostrado", False)
        except FileNotFoundError:
            return False

    def registrar_mensaje_mostrado(self):
        """Registra que el mensaje inicial ya fue mostrado."""
        with open("config.json", "w") as archivo:
            json.dump({"mensaje_mostrado": True}, archivo)

    def crear_usuario_admin(self):
        """Crea el usuario administrador por defecto."""
        with Session() as session:
            crud_usuario = CRUD_usuario(session)
            crud_usuario.crear_usuario("admin", 1234)

    def mostrar_mensaje_inicial(self):
        # Fondo
        fondo = leer_imagen("./gui/login/dibujo-monje.png", (700, 500))
        fondo_label = ctk.CTkLabel(self.frame_principal, image=fondo, text="")
        fondo_label.image = fondo  # Retener referencia
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        mensajes = [
            "Gracias por instalar TuAlmaZen!",
            "Se ha creado el usuario: admin",
            "La contraseña por defecto es: 1234",
            "Este usuario da acceso al",
            "panel de administración.",
            "Puede cambiar la contraseña",
            "en la sección de usuarios,",
            "dentro del panel de administración"
    ]

        posicionesy = [0.1, 0.25, 0.30, 0.45, 0.50, 0.60, 0.65, 0.70]  # Posiciones relativas en Y
        for i, texto in enumerate(mensajes):
            etiqueta = ctk.CTkLabel(
                self.frame_principal,
                text=texto,
                width=300,
                text_color="#F3920F",
                fg_color="#1C2124",
                font=('Carlito', 20, BOLD),
                justify="left",
            )
            etiqueta.place(relx=0.54, rely=posicionesy[i])  # Posiciona cada línea de forma independiente

        # Botón de entendido
        btn_entendido = ctk.CTkButton(
            self.frame_principal,
            text="Entendido!",
            font=('Helvetica', 20, BOLD),
            text_color="#F3920F",
            bg_color='#1C2124',
            fg_color='#1C2124',
            hover_color="#D5D0D4",
            border_width=2,
            border_color="#F3920F",
            command=self.iniciar_login
        )
        btn_entendido.place(relx=0.65, rely=0.8)  # Alineado con el mensaje

    def iniciar_login(self):
        """Registra el mensaje mostrado y pasa al login."""
        self.registrar_mensaje_mostrado()
        self.mostrar_login()

    def mostrar_login(self):
        # Eliminar contenido del frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Fondo
        fondo = leer_imagen("./gui/login/dibujo-monje.png", (700, 500))
        fondo_label = ctk.CTkLabel(self.frame_principal, image=fondo, text="")
        fondo_label.image = fondo  # Retener referencia
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Formulario de inicio de sesión
        etiqueta_bienvenida = ctk.CTkLabel(self.frame_principal, text="BIENVENIDO", text_color="#F3920F",
                                           fg_color="#1C2124", font=('Carlito', 50, BOLD))
        etiqueta_bienvenida.place(relx=0.57, rely=0.1)

        etiqueta_usuario = ctk.CTkLabel(self.frame_principal, text="Usuario", text_color="#F3920F",
                                         fg_color="#1C2124", bg_color="#1C2124", font=('Helvetica', 20))
        etiqueta_usuario.place(relx=0.71, rely=0.3)

        self.var_usuario = ctk.StringVar()
        self.usuario = ctk.CTkEntry(self.frame_principal, textvariable=self.var_usuario, width=300, font=('Helvetica', 20),
                                    bg_color="#1C2124", fg_color='#1C2124', text_color="#D5D0D4", 
                                    border_width=1, border_color="#F3920F", corner_radius=20)
        self.usuario.place(relx=0.55, rely=0.355)

        etiqueta_contrasena = ctk.CTkLabel(self.frame_principal, text="Contraseña", text_color="#F3920F",
                                         fg_color="#1C2124", bg_color="#1C2124", font=('Helvetica', 20))
        etiqueta_contrasena.place(relx=0.69, rely=0.455)

        self.var_contrasena = ctk.StringVar()
        self.contrasena = ctk.CTkEntry(self.frame_principal, textvariable=self.var_contrasena, width=300, font=('Helvetica', 20),
                                    bg_color="#1C2124", fg_color='#1C2124', text_color="#D5D0D4", show="*",
                                    border_width=1, border_color="#F3920F", corner_radius=20)
        self.contrasena.place(relx=0.55, rely=0.510)

        btn_login = ctk.CTkButton(self.frame_principal, command=self.logear, font=('Helvetica', 20, BOLD), text="Iniciar Sesión", 
                                  text_color="#F3920F", bg_color='#1C2124', fg_color='#1C2124', hover_color="#D5D0D4",
                                  border_width=2, border_color="#F3920F")
        btn_login.place(relx=0.65, rely=0.7)

    def logear(self):
        usuario = self.var_usuario.get().strip()
        contrasena = self.var_contrasena.get().strip()

        if not usuario or not contrasena:
            self.mostrar_error("  Complete los campos")
            return
        
        try:
            contrasena = int(contrasena)
        except ValueError:
            self.mostrar_error("La contraseña debe ser \n numérica")
            return
        
        if self.etiqueta_error_login:
            self.etiqueta_error_login.place_forget()

        with Session() as session:
            crud_usuario = CRUD_usuario(session)
            usuario_obj = crud_usuario.verificar_contrasena(usuario, contrasena)
            if usuario_obj:
                if usuario == "admin":
                    self.ventana.destroy()
                    MasterPanel()
                else:
                    self.ventana.destroy()
            else:
                self.mostrar_error("Credenciales Incorrectas")

    def mostrar_error(self, mensaje):
        if self.etiqueta_error_login:
            self.etiqueta_error_login.place_forget()
        self.etiqueta_error_login = ctk.CTkLabel(
            self.frame_principal,
            text=mensaje,
            font=('Helvetica', 20, BOLD),
            text_color="#D40000",
            bg_color="#1C2124",
            fg_color="#1C2124"
        )
        self.etiqueta_error_login.place(relx=0.59, rely=0.8)
