import customtkinter as ctk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_usuarios import CRUD_usuario
from gui.util.generic import centrar_ventana, proxima
from models.models.modelo_usuario import ModeloUsuario

class UsuariosApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title('Listado de Usuarios')
        centrar_ventana(self.ventana, 700, 600)
        self.ventana.resizable(width=0, height=0)

        self.ventana.configure(bg="#1C2124")
        self.frame_principal = ctk.CTkFrame(self.ventana, width=700, height=600, fg_color="#1C2124")
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)

        self.mostrar_contrasenas = False

        
        self.label_nav = ctk.CTkLabel(
            self.frame_principal,
            text="Menú de Navegación →",
            fg_color="#1C2124",
            font=("Helvetica", 20, "bold"),  # Tamaño del texto reducido para mayor ajuste
            text_color="#F3920F",
            height=40,
        )
        self.label_nav.place(x=10, y=10)

        # Botones superiores para navegación
        self.vender_button = ctk.CTkButton(
            self.frame_principal,
            text="Vender",
            command=lambda: proxima(self.ventana,"Vender"),
            border_width=2,
            fg_color="#1C2124",
            text_color="#F3920F",
            font=("Helvetica", 16, "bold"),
            hover_color="#2C353A",
            border_color="#F3920F",
            width=40,
            height=40
        )
        self.vender_button.place(x=250, y=10)

        self.productos_button = ctk.CTkButton(
            self.frame_principal,
            text="Productos",
            command=lambda: proxima(self.ventana, "Productos"),
            border_width=2,
            fg_color="#1C2124",
            text_color="#F3920F",
            font=("Helvetica", 16, "bold"),
            hover_color="#2C353A",
            border_color="#F3920F",
            width=40,
            height=40
        )
        self.productos_button.place(x=350, y=10)

        self.libro_ventas_button = ctk.CTkButton(
            self.frame_principal,
            text="Libro de Ventas",
            command=lambda: proxima(self.ventana, "Libro de Ventas"),
            border_width=2,
            fg_color="#1C2124",
            text_color="#F3920F",
            font=("Helvetica", 16, "bold"),
            hover_color="#2C353A",
            border_color="#F3920F",
            width=40,
            height=40
        )
        self.libro_ventas_button.place(x=475, y=10)

        # Label para el título, ajustado más cerca del listado
        self.label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestor de Usuarios",
            fg_color="#1C2124",
            font=("Helvetica", 30, "bold"),  # Tamaño del texto reducido para mayor ajuste
            text_color="#F3920F",
            height=40,
        )
        self.label_titulo.place(relx=0.5, y=80, anchor="n")

        # Estilos del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2C353A",
                        fieldbackground="#2C353A",
                        foreground="white",
                        rowheight=25,
                        borderwidth=2,
                        relief="solid")
        style.configure("Treeview.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 12, 'bold'))
        style.map("Treeview", background=[('selected', '#F3920F')])

        self.tree = ttk.Treeview(self.frame_principal, columns=("ID", "Usuario", "Contraseña"), show="headings", style="Treeview")
        self.tree.heading("ID", text="ID", command=lambda: self.ordenar_columna("ID"))
        self.tree.heading("Usuario", text="Usuario", command=lambda: self.ordenar_columna("Usuario"))
        self.tree.heading("Contraseña", text="Contraseña", command=lambda: self.ordenar_columna("Contraseña"))
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.frame_principal, orientation="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Label para mensajes de error
        self.error_label = ctk.CTkLabel(self.frame_principal, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Frame para campos y botones
        self.botones_frame = ctk.CTkFrame(self.frame_principal, height=50, fg_color="#1C2124")
        self.botones_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.botones_frame.grid_rowconfigure(0, weight=1)

        # CRUD
        self.crud_usuario = CRUD_usuario(Session)
        self.datos = self.cargar_usuarios()

        # Campos para crear usuario
        self.usuario_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Nombre de usuario", width=200)
        self.usuario_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.contrasena_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Contraseña", width=200, show="*")
        self.contrasena_entry.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Botón Crear Usuario
        self.crear_usuario_button = ctk.CTkButton(self.botones_frame, text="Crear Usuario", command=self.crear_usuario, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.crear_usuario_button.grid(row=2, column=0, padx=40, pady=10, sticky="w")

        # Campos para modificar contraseña (solo contraseña)
        self.modificar_contrasena_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Nueva Contraseña", width=200, show="*")
        self.modificar_contrasena_entry.grid(row=1, column=1, padx=20,  pady=5, sticky="w")

        # Botón Modificar Contraseña
        self.modificar_usuario_button = ctk.CTkButton(self.botones_frame, text="Modificar Contraseña", command=self.modificar_contrasena, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.modificar_usuario_button.grid(row=2, column=1, padx=50, sticky="w")

        # Botones Eliminar Usuario
        self.eliminar_usuario_button = ctk.CTkButton(self.botones_frame, text="Eliminar Usuario", command=self.eliminar_usuario, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.eliminar_usuario_button.grid(row=2, column=2, padx=20, sticky="e")

        self.toggle_password_button = ctk.CTkButton(
            self.botones_frame,
            text="Mostrar Contraseña",
            command=self.toggle_contrasenas,
            border_width=2,
            fg_color="#1C2124",
            text_color="white",
            font=("Helvetica", 12, "bold"),
            hover_color="#F3920F",
            border_color="#F3920F"
        )
        self.toggle_password_button.grid(row=0, column=2, padx=20, sticky="ew")

        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.ventana.mainloop()


 

    def cargar_usuarios(self):
        usuarios = self.crud_usuario.obtener_todos_usuarios()
        for row in self.tree.get_children():
            self.tree.delete(row)
        datos = []
        for index, usuario in enumerate(usuarios):
            contrasena = usuario.contrasena if self.mostrar_contrasenas else "****"
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(usuario.vendedorID, usuario.usuario, contrasena), tags=(tag,))
            datos.append((usuario.vendedorID, usuario.usuario, usuario.contrasena))
        return datos

    def ordenar_columna(self, columna):
        col_index = ["ID", "Usuario", "Contraseña"].index(columna)
        orden_inverso = getattr(self, "orden_inverso", False)
        self.datos.sort(key=lambda x: x[col_index], reverse=orden_inverso)
        self.orden_inverso = not orden_inverso
        for row in self.tree.get_children():
            self.tree.delete(row)
        for index, dato in enumerate(self.datos):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=dato, tags=(tag,))

    def crear_usuario(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        try:
            modelo_usuario = ModeloUsuario(usuario, contrasena)
            if not modelo_usuario.es_completo():
                raise ValueError("Faltan campos por completar")
            resultado, error = self.crud_usuario.crear_usuario(usuario, contrasena)
            if error:
                self.error_label.configure(text=error, text_color="#FF0000")  # Mensaje de error en rojo
                return
            self.usuario_entry.delete(0, "end")
            self.contrasena_entry.delete(0, "end")
            self.datos = self.cargar_usuarios()
            self.error_label.configure(text="Usuario creado con éxito.", text_color="#00FF00")  # Mensaje de éxito
        except ValueError as e:
            self.error_label.configure(text=str(e), text_color="#FF0000")
        except Exception as e:
            self.error_label.configure(text=f"Error inesperado: {str(e)}", text_color="#FF0000")


    def modificar_contrasena(self):
        contrasena_nueva = self.modificar_contrasena_entry.get()
        selected_item = self.tree.selection()

        if not selected_item:
            self.error_label.configure(text="Por favor, selecciona un usuario.", text_color="#FF0000")
            return

        nombre_usuario = self.tree.item(selected_item)["values"][1]

        try:
            modelo_usuario = ModeloUsuario(nombre_usuario, contrasena_nueva)

            if not modelo_usuario.es_completo():
                raise ValueError("La contraseña no es válida.")

            error = self.crud_usuario.actualizar_contrasena(nombre_usuario, contrasena_nueva)

            self.modificar_contrasena_entry.delete(0, "end")
            self.datos = self.cargar_usuarios()
            self.error_label.configure(text="Contraseña actualizada con éxito.", text_color="#00FF00")  # Mensaje de éxito
        except ValueError as e:
            self.error_label.configure(text=str(e), text_color="#FF0000")
        except Exception as e:
            self.error_label.configure(text=f"Error inesperado: {str(e)}", text_color="#FF0000")


    def eliminar_usuario(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.error_label.configure(text="Por favor, selecciona un usuario.", text_color="#FF0000")
            return
        nombre_usuario = self.tree.item(selected_item)["values"][1]
        
        if nombre_usuario.lower() == "admin":
            self.error_label.configure(text="No puede eliminar al usuario administrador.", text_color="#FF0000")
            return
        
        try:
            self.crud_usuario.eliminar_usuario(nombre_usuario)
            self.datos = self.cargar_usuarios()
            self.error_label.configure(text="Usuario eliminado con éxito.", text_color="#00FF00")  # Mensaje de éxito
        except Exception as e:
            self.error_label.configure(text=f"Error al eliminar el usuario: {str(e)}", text_color="#FF0000")

    def toggle_contrasenas(self):
        self.mostrar_contrasenas = not self.mostrar_contrasenas
        self.datos = self.cargar_usuarios()
        texto = "Ocultar Contraseña" if self.mostrar_contrasenas else "Mostrar Contraseña"
        self.toggle_password_button.configure(text=texto)


