import customtkinter as ctk
from tkinter.font import BOLD
from gui.util.generic import centrar_ventana, configurar_boton_elegante


class MasterPanel:
    def __init__(self):
        ctk.set_appearance_mode("light")  # Asegura consistencia en colores
        ctk.set_default_color_theme("blue")  # Tema por defecto

        self.ventana = ctk.CTk()  # Crea la ventana principal
        self.ventana.title('TuAlmaZen')
        centrar_ventana(self.ventana, 1300, 700)
        self.ventana.resizable(width=1, height=1)
        self.ventana.attributes("-topmost", True)  # Mantener siempre en la parte superior

        # Crear un efecto degradado con Frames apilados
        colores_degradado = ["#FFA500", "#F39C12", "#E67E22", "#D35400", "#4F4F4F"]  # Tonos ajustados
        for i, color in enumerate(colores_degradado):
            frame = ctk.CTkFrame(self.ventana, fg_color=color)
            frame.place(relx=0, rely=i * 0.2, relwidth=1, relheight=0.2)  # Apila frames al 20% cada uno

        # Título en el frame principal con fondo del mismo color que el primer frame
        self.titulo = ctk.CTkLabel(self.ventana, text="━━━━ Tu Alma Zen ━━━━", font=("Arial", 52, BOLD),
                                   text_color="#2C2F33", bg_color=colores_degradado[0])  # Fondo igual al primer frame
        self.titulo.place(relx=0.5, rely=0.05, anchor='center')

        # Frame secundario (marco)
        self.marco = ctk.CTkFrame(self.ventana, height=500, corner_radius=15, fg_color="#2C2F33")
        self.marco.place(relx=0.5, rely=0.5, relwidth=0.95, anchor='center')

        # Configurar botones en una distribución 2x2
        boton_ancho = 300
        boton_alto = 120

        # Primera columna
        self.boton_vender = ctk.CTkButton(self.marco, text="Vender", width=boton_ancho, height=boton_alto, 
                                         font=("Arial", 24, BOLD), fg_color="#1E90FF", text_color="white",
                                         corner_radius=10)
        configurar_boton_elegante(self.boton_vender, border_color="#005c9e")
        self.boton_vender.place(relx=0.25, rely=0.3, anchor='center')

        self.boton_usuarios = ctk.CTkButton(self.marco, text="Usuarios", width=boton_ancho, height=boton_alto, 
                                           font=("Arial", 24, BOLD), fg_color="#FFD700", text_color="black",
                                           corner_radius=10)
        configurar_boton_elegante(self.boton_usuarios, border_color="#b8860b")
        self.boton_usuarios.place(relx=0.25, rely=0.7, anchor='center')

        # Segunda columna
        self.boton_productos = ctk.CTkButton(self.marco, text="Productos", width=boton_ancho, height=boton_alto, 
                                            font=("Arial", 24, BOLD), fg_color="#32CD32", text_color="white",
                                            corner_radius=10)
        configurar_boton_elegante(self.boton_productos, border_color="#228b22")
        self.boton_productos.place(relx=0.75, rely=0.3, anchor='center')

        self.boton_libro_ventas = ctk.CTkButton(self.marco, text="Libro de Ventas", width=boton_ancho, height=boton_alto, 
                                               font=("Arial", 24, BOLD), fg_color="#FF6347", text_color="white",
                                               corner_radius=10)
        configurar_boton_elegante(self.boton_libro_ventas, border_color="#b22222")
        self.boton_libro_ventas.place(relx=0.75, rely=0.7, anchor='center')

        self.ventana.mainloop()


MasterPanel()
