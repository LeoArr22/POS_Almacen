import customtkinter as ctk
from tkinter.font import BOLD
from util.generic import centrar_ventana, leer_imagen

class LoginApp:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.ventana = ctk.CTk()  # Crear la ventana principal
        self.ventana.title('Login')
        centrar_ventana(self.ventana, 750, 600)
        self.ventana.resizable(width=0, height=0)

        # Frame para el logo
        frame_logo = ctk.CTkFrame(self.ventana, fg_color='#FBF1E7', width=250)
        frame_logo.pack(side="left", expand=ctk.YES, fill=ctk.BOTH)
        frame_logo.pack_propagate(False)

        # Colocar el logo en el frame izquierdo
        logo = leer_imagen("./POS_Almacen/GUI/login/logo.PNG", (300, 200))  # Ajusta el tamaño según sea necesario
        label_logo = ctk.CTkLabel(frame_logo, image=logo, text="")
        label_logo.pack(expand=True)  # Usar pack para expandir el label dentro del frame

        # Frame para el formulario de login
        frame_login = ctk.CTkFrame(self.ventana, fg_color='#2C3E50', width=500)
        frame_login.pack(side="right", expand=ctk.YES, fill=ctk.BOTH)
        frame_login.pack_propagate(False)

        # Divisor entre el logo y el formulario
        divisor = ctk.CTkFrame(self.ventana, width=18, fg_color="#ECF0F1")
        divisor.pack(side="right", fill=ctk.Y)

        # Etiqueta de bienvenida
        etiqueta_bienvenida = ctk.CTkLabel(frame_login, text="Bienvenid@", font=('Helvetica', 60, BOLD), text_color="#ECF0F1")
        etiqueta_bienvenida.grid(row=0, column=0, pady=(40, 120), sticky='nsew')  # Ajuste de posición

        # Etiqueta de usuario
        etiqueta_usuario = ctk.CTkLabel(frame_login, text="Usuario", font=('Helvetica', 20, BOLD), text_color="#ECF0F1")
        etiqueta_usuario.grid(row=1, column=0, pady=(0, 5), sticky='nsew')  # Ajuste de posición

        # Variable para el campo de entrada de usuario
        self.usuario_var = ctk.StringVar()

        # Campo de entrada para el usuario
        self.usuario = ctk.CTkEntry(frame_login, font=('Helvetica', 16), textvariable=self.usuario_var, fg_color='#ECF0F1', text_color="#34495E", border_width=2)
        self.usuario.grid(row=2, column=0, pady=(0, 30), padx=20, sticky='ew')  # Rellena horizontalmente

        # Etiqueta de contraseña
        etiqueta_password = ctk.CTkLabel(frame_login, text="Contraseña", font=('Helvetica', 20, BOLD), text_color="#ECF0F1")
        etiqueta_password.grid(row=3, column=0, pady=(0, 5), sticky='nsew')  # Ajuste de posición

        # Variable para el campo de entrada de contraseña
        self.password_var = ctk.StringVar()

        # Campo de entrada para la contraseña
        self.password = ctk.CTkEntry(frame_login, font=('Helvetica', 16), textvariable=self.password_var, show="*", fg_color='#ECF0F1', text_color="#34495E", border_width=2)
        self.password.grid(row=4, column=0, pady=(0, 10), padx=20, sticky='ew')  # Rellena horizontalmente

        # Botón de login
        btn_login = ctk.CTkButton(frame_login, text="Iniciar Sesión", font=('Helvetica', 16, BOLD), fg_color='#E74C3C', text_color='white')
        btn_login.grid(row=5, column=0, pady=(30, 20), ipadx=10, ipady=10)  # Ajusta el margen vertical

        # Ajuste de columnas para que se expandan
        frame_login.columnconfigure(0, weight=1)  # Permite que la columna 0 se expanda

        # Ejecutar la ventana
        self.ventana.mainloop()


# Inicializar la aplicación
LoginApp()
