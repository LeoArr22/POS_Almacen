from gui.util.generic import proxima
import customtkinter as ctk


def navegacion(self):
    # Frame superior
    self.frame_superior = ctk.CTkFrame(self.frame_principal, fg_color="#2E3B4E")
    self.frame_superior.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Barra de navegación
    self.frame_superior.columnconfigure(0, weight=3)
    self.frame_superior.columnconfigure(1, weight=1)
    self.frame_superior.columnconfigure(2, weight=1)
    self.frame_superior.columnconfigure(3, weight=1)
    self.frame_superior.columnconfigure(4, weight=3)
    self.frame_superior.rowconfigure(0, weight=1)


def menu_label(self):
    self.label_nav = ctk.CTkLabel(
            self.frame_superior,
            text="Menú de Navegación →",
            fg_color="transparent",
            font=("Helvetica", 20, "bold"),
            text_color="#F3920F",
            height=40
        )
    self.label_nav.grid(row=0, column=0, padx=10, pady=5, sticky="w")

def crear_boton(self, texto, comando, columna):
    boton = ctk.CTkButton(
        self.frame_superior,
        text=texto,
        command=comando,
        border_width=2, 
        fg_color="#1C2124",
        text_color="#F3920F",
        font=("Helvetica", 16, "bold"),
        hover_color="#2C353A",
        border_color="#F3920F",
        width=100,
        height=40
    )
    boton.grid(row=0, column=columna, padx=10, pady=5)

def boton_productos(self, columna):
    crear_boton(self, "Productos", lambda: proxima(self.ventana, "Productos"), columna)

def boton_usuarios(self, columna):
    crear_boton(self, "Usuarios", lambda: proxima(self.ventana, "Usuarios"), columna)

def boton_libro(self, columna):
    crear_boton(self, "Libro de Ventas", lambda: proxima(self.ventana, "Libro de Ventas"), columna)  

def boton_ventas(self, columna):
    crear_boton(self, "Vender", lambda: proxima(self.ventana, "Vender"), columna)  


def titulo(self, texto, columna):
    self.label_titulo = ctk.CTkLabel(
            self.frame_superior,
            text=texto,
            fg_color="transparent",
            font=("Helvetica", 20, "bold"),
            text_color="#F3920F",
            height=40,
        )
    self.label_titulo.grid(row=0, column=columna, padx=10, pady=5)

    
    