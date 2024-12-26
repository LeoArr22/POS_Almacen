import customtkinter as ctk
from tkinter.font import BOLD
from gui.util.generic import centrar_ventana, leer_imagen
from datetime import datetime


class MasterPanel:
    def __init__(self):
        self.ventana = ctk.CTk()  # Crea la ventana principal
        self.ventana.title('TuAlmaZen')
        centrar_ventana(self.ventana, 720, 670)
        self.ventana.resizable(width=0, height=0)
        self.ventana.attributes("-topmost", True)  # Mantener siempre en la parte superior

        fondo_color = "#110D0C"  # Color de fondo para botones y frame
        boton_borde = "#B56C3D"

        self.frame_fondo = ctk.CTkFrame(self.ventana, width=720, height=670, fg_color=fondo_color)
        self.frame_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Coloca la imagen de fondo en el Frame
        self.fondo = leer_imagen("./gui/master/fondo.png", (720, 670))
        self.fondo_label = ctk.CTkLabel(self.frame_fondo, image=self.fondo, text="")
        self.fondo_label.place(relwidth=1, relheight=1)

        # Label de título
        self.label_titulo = ctk.CTkLabel(
            self.frame_fondo, 
            text="Panel de Administración", 
            font=("Arial", 28, BOLD), 
            text_color="#B56C3D"
        )
        self.label_titulo.place(relx=0.5, rely=0.48, anchor="center")

        # Configurar botones en una distribución 2x2
        boton_ancho = 200
        boton_alto = 100

        # Primera columna
        self.boton_vender = ctk.CTkButton(
            self.frame_fondo, 
            text="Vender", 
            width=boton_ancho, 
            height=boton_alto, 
            font=("Arial", 24, BOLD), 
            fg_color=fondo_color, 
            bg_color=fondo_color, 
            text_color="#FFFFFF", 
            corner_radius=20, 
            border_width=2, 
            border_color=boton_borde
        )
        self.boton_vender.place(relx=0.3, rely=0.6, anchor='center')

        self.boton_usuarios = ctk.CTkButton(
            self.frame_fondo, 
            text="Usuarios", 
            width=boton_ancho, 
            height=boton_alto, 
            font=("Arial", 24, BOLD), 
            fg_color=fondo_color, 
            bg_color=fondo_color, 
            text_color="#FFFFFF", 
            corner_radius=20, 
            border_width=2, 
            border_color=boton_borde
        )
        self.boton_usuarios.place(relx=0.3, rely=0.8, anchor='center')

        # Segunda columna
        self.boton_productos = ctk.CTkButton(
            self.frame_fondo, 
            text="Productos", 
            width=boton_ancho, 
            height=boton_alto, 
            font=("Arial", 24, BOLD), 
            fg_color=fondo_color, 
            bg_color=fondo_color, 
            text_color="#FFFFFF", 
            corner_radius=20, 
            border_width=2, 
            border_color=boton_borde
        )
        self.boton_productos.place(relx=0.7, rely=0.6, anchor='center')

        self.boton_libro_ventas = ctk.CTkButton(
            self.frame_fondo, 
            text="Libro de Ventas", 
            width=boton_ancho, 
            height=boton_alto, 
            font=("Arial", 20, BOLD), 
            fg_color=fondo_color, 
            bg_color=fondo_color, 
            text_color="#FFFFFF", 
            corner_radius=20, 
            border_width=2, 
            border_color=boton_borde
        )
        self.boton_libro_ventas.place(relx=0.7, rely=0.8, anchor='center')

        # Label de fecha y hora
        self.label_fecha_hora = ctk.CTkLabel(
            self.frame_fondo, 
            font=("Arial", 18), 
            text_color="#B56C3D"
        )
        self.label_fecha_hora.place(relx=0.5, rely=0.95, anchor="center")
        self.actualizar_fecha_hora()

        self.ventana.mainloop()

    def actualizar_fecha_hora(self):
        """Actualiza la fecha y hora en el label cada minuto."""
        fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.label_fecha_hora.configure(text=fecha_hora_actual)
        self.ventana.after(60000, self.actualizar_fecha_hora)  # Actualizar cada minuto
