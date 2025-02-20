import customtkinter as ctk
from tkinter.font import BOLD
from gui.util.generic import centrar_ventana, leer_imagen, proxima
from gui.usuarios.gui_usuarios import UsuariosApp
from gui.productos.gui_productos import ProductosApp
from datetime import datetime


class MasterPanel:
    def __init__(self, ventana, frame):
        fondo_color = "#1C2124"  # Fondo de botones y frame
        texto_color = "#FFFFFF"
        boton_borde = "#B56C3D"
        hover_color = boton_borde  # Color al pasar el mouse

        # Centrar ventana
        centrar_ventana(ventana, 700, 500)

        self.frame_fondo = frame  # Usa el frame pasado como argumento

        # Fondo con imagen
        self.fondo = leer_imagen("./gui/login/dibujo-monje.png", (700, 500))
        self.fondo_label = ctk.CTkLabel(self.frame_fondo, image=self.fondo, text="")
        self.fondo_label.image = self.fondo  # Retener referencia
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Label de título
        self.label_titulo = ctk.CTkLabel(
            self.frame_fondo,
            text="Panel de Administración",
            font=("Arial", 18, BOLD),
            text_color=texto_color,
            bg_color=fondo_color,
        )
        self.label_titulo.place(relx=0.75, rely=0.05, anchor="center")  # Mover a la izquierda

        # Configurar botones
        boton_ancho = 150
        boton_alto = 70

        self.boton_vender = ctk.CTkButton(
            self.frame_fondo,
            text="Vender",
            width=boton_ancho,
            height=boton_alto,
            font=("Arial", 16, BOLD),
            fg_color=fondo_color,
            bg_color=fondo_color,
            text_color=texto_color,
            hover_color=hover_color,
            corner_radius=20,
            border_width=2,
            border_color=boton_borde,
            command=lambda: proxima(ventana, "Vender")
        )
        self.boton_vender.place(relx=0.75, rely=0.2, anchor="center")

        self.boton_usuarios = ctk.CTkButton(
            self.frame_fondo,
            text="Usuarios",
            width=boton_ancho,
            height=boton_alto,
            font=("Arial", 16, BOLD),
            fg_color=fondo_color,
            bg_color=fondo_color,
            text_color=texto_color,
            hover_color=hover_color,
            corner_radius=20,
            border_width=2,
            border_color=boton_borde,
            command=lambda: proxima(ventana, "Usuarios")
        )
        self.boton_usuarios.place(relx=0.75, rely=0.4, anchor="center")

        self.boton_productos = ctk.CTkButton(
            self.frame_fondo,
            text="Productos",
            width=boton_ancho,
            height=boton_alto,
            font=("Arial", 16, BOLD),
            fg_color=fondo_color,
            bg_color=fondo_color,
            text_color=texto_color,
            hover_color=hover_color,
            corner_radius=20,
            border_width=2,
            border_color=boton_borde,
            command=lambda: proxima(ventana, "Productos")
        )
        self.boton_productos.place(relx=0.75, rely=0.6, anchor="center")

        self.boton_libro_ventas = ctk.CTkButton(
            self.frame_fondo,
            text="Libro de Ventas",
            width=boton_ancho,
            height=boton_alto,
            font=("Arial", 14, BOLD),
            fg_color=fondo_color,
            bg_color=fondo_color,
            text_color=texto_color,
            hover_color=hover_color,
            corner_radius=20,
            border_width=2,
            border_color=boton_borde,
            command=lambda: proxima(ventana, "Libro de Ventas")
        )
        self.boton_libro_ventas.place(relx=0.75, rely=0.8, anchor="center")

        # Label de fecha y hora
        self.label_fecha_hora = ctk.CTkLabel(
            self.frame_fondo,
            font=("Arial", 18),
            text_color=texto_color,
            bg_color=fondo_color,
        )
        self.label_fecha_hora.place(relx=0.75, rely=0.95, anchor="center")  # Mover a la izquierda
        self.actualizar_fecha_hora()

    def actualizar_fecha_hora(self):
        """Actualiza la fecha y hora en el label cada minuto."""
        fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.label_fecha_hora.configure(text=fecha_hora_actual)
        self.frame_fondo.after(60000, self.actualizar_fecha_hora)  # Actualizar cada minuto
