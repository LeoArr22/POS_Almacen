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

def boton_productos(self, columna):
    self.productos_button = ctk.CTkButton(
        self.frame_superior,
        text="Productos",
        command=lambda: proxima(self.ventana, "Productos"),
        border_width=2,
        fg_color="#1C2124",
        text_color="#F3920F",
        font=("Helvetica", 16, "bold"),
        hover_color="#2C353A",
        border_color="#F3920F",
        width=100,
        height=40
    )
    self.productos_button.grid(row=0, column=columna, padx=10, pady=5)
        
def boton_usuarios(self, columna):
    self.usuarios_button = ctk.CTkButton(
        self.frame_superior,
        text="Usuarios",
        command=lambda: proxima(self.ventana, "Usuarios"),
        border_width=2,
        fg_color="#1C2124",
        text_color="#F3920F",
        font=("Helvetica", 16, "bold"),
        hover_color="#2C353A",
        border_color="#F3920F",
        width=100,
        height=40
    )
    self.usuarios_button.grid(row=0, column=columna, padx=10, pady=5)
    
def boton_ventas(self, columna):
    self.vender_button = ctk.CTkButton(
            self.frame_superior,
            text="Vender",
            command=lambda: proxima(self.ventana, "Vender"),
            border_width=2,
            fg_color="#1C2124",
            text_color="#F3920F",
            font=("Helvetica", 16, "bold"),
            hover_color="#2C353A",
            border_color="#F3920F",
            width=100,
            height=40
        )
    self.vender_button.grid(row=0, column=columna, padx=10, pady=5)
    
def boton_libro(self, columna):
    self.libro_ventas_button = ctk.CTkButton(
            self.frame_superior,
            text="Libro de Ventas",
            command=lambda: proxima(self.ventana, "Libro de Ventas"),
            border_width=2,
            fg_color="#1C2124",
            text_color="#F3920F",
            font=("Helvetica", 16, "bold"),
            hover_color="#2C353A",
            border_color="#F3920F",
            width=130,
            height=40
        )
    self.libro_ventas_button.grid(row=0, column=columna, padx=10, pady=5)    
    

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
    
    
    