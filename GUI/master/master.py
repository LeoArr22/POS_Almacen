import customtkinter as ctk
from tkinter.font import BOLD
from gui.util.generic import centrar_ventana, configurar_boton_elegante, leer_imagen


class MasterPanel:
    def __init__(self):
        self.ventana = ctk.CTk()  # Crea la ventana principal
        self.ventana.title('TuAlmaZen')
        centrar_ventana(self.ventana, 720, 671)
        self.ventana.resizable(width=1, height=1)
        self.ventana.attributes("-topmost", True)  # Mantener siempre en la parte superior

        
        self.frame_fondo = ctk.CTkFrame(self.ventana, width=720, height=671)
        self.frame_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        #Coloca la imagen de fondo en el Frame
        self.fondo = leer_imagen("./gui/master/fondo.png", (720, 671))
        self.fondo_label = ctk.CTkLabel(self.frame_fondo, image=self.fondo, text="")
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Configurar botones en una distribución 2x2
        boton_ancho = 200
        boton_alto = 100

        # Primera columna
        self.boton_vender = ctk.CTkButton(self.frame_fondo, text="Vender", width=boton_ancho, height=boton_alto, 
                                         font=("Arial", 24, BOLD), fg_color="#484D4D", text_color="#090A0A",
                                         corner_radius=20)
        configurar_boton_elegante(self.boton_vender, border_color="#FFFFFF")
        self.boton_vender.place(relx=0.3, rely=0.6, anchor='center')

        self.boton_usuarios = ctk.CTkButton(self.frame_fondo, text="Usuarios", width=boton_ancho, height=boton_alto, 
                                         font=("Arial", 24, BOLD), fg_color="#484D4D", text_color="#090A0A",
                                         corner_radius=20)
        configurar_boton_elegante(self.boton_usuarios, border_color="#484D4D")
        self.boton_usuarios.place(relx=0.3, rely=0.8, anchor='center')

        # Segunda columna
        self.boton_productos = ctk.CTkButton(self.frame_fondo, text="Productos", width=boton_ancho, height=boton_alto, 
                                         font=("Arial", 24, BOLD), fg_color="#484D4D", text_color="#090A0A",
                                         corner_radius=20)
        configurar_boton_elegante(self.boton_productos, border_color="#FFFFFF")
        self.boton_productos.place(relx=0.7, rely=0.6, anchor='center')

        self.boton_libro_ventas = ctk.CTkButton(self.frame_fondo, text="Libro de Ventas", width=boton_ancho, height=boton_alto, 
                                         font=("Arial", 20, BOLD), fg_color="#484D4D", text_color="#090A0A",
                                         corner_radius=20)
        configurar_boton_elegante(self.boton_libro_ventas, border_color="#FFFFFF")
        self.boton_libro_ventas.place(relx=0.7, rely=0.8, anchor='center')

        self.ventana.mainloop()
