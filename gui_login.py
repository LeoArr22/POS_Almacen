import customtkinter as ctk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")  # Tamaño de la ventana
        self.root.title("Login de Usuario")  # Título de la ventana
        self.root.configure(fg_color="#1A1A40")  # Fondo azul oscuro
        self.root.resizable(False, False)  # Evitar que se redimensione la ventana

        # Etiqueta de bienvenida
        self.welcome_label = ctk.CTkLabel(self.root, text="Bienvenido", text_color="white", font=("Arial", 24))
        self.welcome_label.pack(pady=20)

        # Campo de entrada para el nombre de usuario
        self.username_entry = ctk.CTkEntry(self.root, placeholder_text="Usuario", width=300, height=40, corner_radius=10)
        self.username_entry.pack(pady=10)

        # Campo de entrada para la contraseña
        self.password_entry = ctk.CTkEntry(self.root, placeholder_text="Contraseña", show="*", width=300, height=40, corner_radius=10)
        self.password_entry.pack(pady=10)

        # Botón de inicio de sesión
        self.login_button = ctk.CTkButton(self.root, text="Iniciar Sesión", width=150, height=40, corner_radius=10, fg_color="#3A3A69", command=self.iniciar_sesion)
        self.login_button.pack(pady=20)

    def iniciar_sesion(self):
        # Aquí puedes agregar la lógica de validación del login
        usuario = self.username_entry.get()
        contrasena = self.password_entry.get()
        print(f"Usuario: {usuario}, Contraseña: {contrasena}")

# Inicializar la app
if __name__ == "__main__":
    root = ctk.CTk()  # Crear la ventana principal
    app = LoginApp(root)  # Instanciar la clase del login
    root.mainloop()  # Iniciar el bucle principal de la ventana
