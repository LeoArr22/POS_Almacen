import customtkinter as ctk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_usuarios import CRUD_usuario
from gui.util.generic import centrar_ventana
from gui.util.nav import navegacion, boton_libro, boton_ventas, boton_productos, titulo, menu_label
from models.models.modelo_usuario import ModeloUsuario

class UsuariosApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title('Listado de Usuarios')
        centrar_ventana(self.ventana, 900, 600)
        self.ventana.resizable(width=0, height=0)

        self.ventana.configure(bg="#1C2124")
        self.frame_principal = ctk.CTkFrame(self.ventana, width=700, height=600, fg_color="#1C2124")
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)

                
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=1)  # Barra de navegación
        self.frame_principal.grid_rowconfigure(1, weight=3)  # Treeview 
        self.frame_principal.grid_rowconfigure(2, weight=1)  # Label de error
        self.frame_principal.grid_rowconfigure(3, weight=2)  # Botones/campos busqueda productos

        navegacion(self)
        menu_label(self)
        boton_libro(self, 1)
        boton_productos(self, 2)
        boton_ventas(self, 3)        
        titulo(self, "Gestor de Usuarios", 4)

        self.mostrar_contrasenas = False
        # Estilos del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2C353A",
                        fieldbackground="#2C353A",
                        foreground="white",
                        rowheight=30,
                        font=("Roboto", 18),
                        borderwidth=2,
                        relief="solid")
        style.configure("Treeview.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 14, 'bold'))
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
        self.botones_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=10)
        self.botones_frame.columnconfigure(4, weight=1)

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
        self.modificar_contrasena_button = ctk.CTkButton(self.botones_frame, text="Modificar Contraseña", command=self.modificar_contrasena, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.modificar_contrasena_button.grid(row=2, column=1, padx=50, sticky="w")
        
        # Campos para modificar nombre (solo nombre)
        self.modificar_nombre_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Nuevo Nombre", width=200)
        self.modificar_nombre_entry.grid(row=1, column=2, padx=20,  pady=5, sticky="w")

        # Botón Modificar Nombre
        self.modificar_nombre_button = ctk.CTkButton(self.botones_frame, text="Modificar Nombre", command=self.modificar_nombre, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.modificar_nombre_button.grid(row=2, column=2, padx=50, sticky="w")

        # Botones Eliminar Usuario
        self.eliminar_usuario_button = ctk.CTkButton(self.botones_frame, text="Eliminar Usuario", command=self.eliminar_usuario, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.eliminar_usuario_button.grid(row=2, column=3, padx=20, sticky="e")

        # Boton Ver contraseña
        self.ver_contrasena_button = ctk.CTkButton(self.botones_frame, text="Mostrar / Ocultar Contraseña", command=self.mostrar_ocultar_contrasenas, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.ver_contrasena_button.grid(row=0, column=3, sticky="e")

        self.toggle_password_button = ctk.CTkButton(
            self.botones_frame,
            text="Mostrar Contraseña",
            command=self.mostrar_ocultar_contrasenas,
            border_width=2,
            fg_color="#1C2124",
            text_color="white",
            font=("Helvetica", 12, "bold"),
            hover_color="#F3920F",
            border_color="#F3920F"
        )
        self.toggle_password_button.grid(row=0, column=4, padx=20, sticky="e")

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
            contrasena_oculta = dato[2] if self.mostrar_contrasenas else "****"
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(dato[0], dato[1], contrasena_oculta), tags=(tag,))

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

            usuario_actualizado, error = self.crud_usuario.actualizar_contrasena(nombre_usuario, contrasena_nueva)

            if usuario_actualizado:
                self.modificar_contrasena_entry.delete(0, "end")
                self.datos = self.cargar_usuarios()
                self.error_label.configure(text="Contraseña actualizada con éxito.", text_color="#00FF00")  # Mensaje de éxito
            else:
                self.error_label.configure(text=error, text_color="#FF0000")  # Mensaje de error del CRUD

        except ValueError as e:
            self.error_label.configure(text=str(e), text_color="#FF0000")
        except Exception as e:
            self.error_label.configure(text=f"Error inesperado: {str(e)}", text_color="#FF0000")
            
    def modificar_nombre(self):
        nombre_nuevo = self.modificar_nombre_entry.get()
        selected_item = self.tree.selection()

        if not selected_item:
            self.error_label.configure(text="Por favor, selecciona un usuario.", text_color="#FF0000")
            return

        nombre_usuario = self.tree.item(selected_item)["values"][1]

        try:
            usuario_actualizado, error = self.crud_usuario.actualizar_nombre(nombre_usuario, nombre_nuevo)

            if usuario_actualizado:
                self.modificar_nombre_entry.delete(0, "end")
                self.datos = self.cargar_usuarios()
                self.error_label.configure(text="Nombre actualizado con éxito.", text_color="#00FF00")  # Mensaje de éxito
            else:
                self.error_label.configure(text=error, text_color="#FF0000")  # Mensaje de error del CRUD

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

    def mostrar_ocultar_contrasenas(self):
        self.mostrar_contrasenas = not self.mostrar_contrasenas
        self.datos = self.cargar_usuarios()
        texto = "Ocultar Contraseña" if self.mostrar_contrasenas else "Mostrar Contraseña"
        self.toggle_password_button.configure(text=texto)


