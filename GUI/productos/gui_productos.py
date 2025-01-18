import customtkinter as ctk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_producto import CRUD_producto
from data.crud.crud_categoria import CRUD_categoria
from gui.util.generic import centrar_ventana, destruir
from models.models.modelo_producto import ModeloProducto
from models.models.modelo_categoria import ModeloCategoria

class ProductosApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title('Listado de Productos')#
        centrar_ventana(self.ventana, 1200, 600)
        self.ventana.resizable(width=0, height=0)

        self.ventana.configure(bg="#1C2124")
        self.frame_principal = ctk.CTkFrame(self.ventana, width=850, height=750, fg_color="#1C2124")
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)
        
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
            command=lambda: self.ir_a("vender"),
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
            text="Usuarios",
            command=lambda: self.proxima("Usuarios"),
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
            command=lambda: self.ir_a("libro_ventas"),
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
            text="Gestor de Productos y Categorias",
            fg_color="#1C2124",
            font=("Helvetica", 30, "bold"),  # Tamaño del texto reducido para mayor ajuste
            text_color="#F3920F",
            height=40,
        )
        self.label_titulo.place(x=900, y=10, anchor="n")

        # Estilos del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2C353A",
                        fieldbackground="#2C353A",
                        foreground="white",
                        rowheight=25,
                        borderwidth=2,
                        font=("Roboto", 14),
                        relief="solid")
        style.configure("Treeview.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 20, 'bold'))
        style.map("Treeview", background=[('selected', '#F3920F')])

        self.tree = ttk.Treeview(self.frame_principal, columns=("ID", "Categoria", "Nombre", "Precio", "Stock", "Costo", "CodBar"), show="headings", style="Treeview", height=15)
        self.tree.heading("ID", text="ID", command=lambda: self.ordenar_columna("ID"))
        self.tree.heading("Categoria", text="Categoria", command=lambda: self.ordenar_columna("Categoria"))
        self.tree.heading("Nombre", text="Nombre", command=lambda: self.ordenar_columna("Nombre"))
        self.tree.heading("Precio", text="Precio", command=lambda: self.ordenar_columna("Precio"))
        self.tree.heading("Stock", text="Stock", command=lambda: self.ordenar_columna("Stock"))
        self.tree.heading("Costo", text="Costo", command=lambda: self.ordenar_columna("Costo"))
        self.tree.heading("CodBar", text="CodBar", command=lambda: self.ordenar_columna("CodBar"))
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        
        self.tree.column("ID", anchor="center", width=25, minwidth=25)  # Columna "ID" más pequeña
        self.tree.column("Categoria", width=120, minwidth=100)  # Columna "Categoria" más ancha
        self.tree.column("Nombre", width=150, minwidth=100)
        self.tree.column("Precio", width=40, minwidth=40)
        self.tree.column("Stock", width=40, minwidth=40)
        self.tree.column("Costo", width=40, minwidth=40)
        self.tree.column("CodBar", width=100, minwidth=90)

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
        self.crud_producto = CRUD_producto(Session())
        self.datos = self.cargar_datos()

        # Botón Crear Producto
        self.crear_producto_button = ctk.CTkButton(self.botones_frame, text="Crear Producto", command=self.crear_producto, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.crear_producto_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        # Botones Eliminar Producto
        self.eliminar_producto_button = ctk.CTkButton(self.botones_frame, text="Eliminar Producto", command=self.eliminar_producto, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.eliminar_producto_button.grid(row=2, column=1, padx=20, sticky="e")

        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.ventana.mainloop()

    def proxima(self, nombre):
        if nombre=="Usuarios":
            from gui.usuarios.gui_usuarios import UsuariosApp
            destruir(self.ventana, UsuariosApp)


    def cargar_datos(self):
        productos = self.crud_producto.obtener_todos_productos()
        for row in self.tree.get_children():
            self.tree.delete(row)
        datos = []
        
          # Si no hay productos, mostrar mensaje en la primera fila
        if not productos:
            self.tree.insert("", "end", values=("No hay productos cargados", "", "", "", "", "", ""), tags=("empty",))
            return datos
        
        for index, (producto, categoria_nombre) in enumerate(productos):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(producto.productoID, categoria_nombre, producto.nombre, producto.precio,
                                                producto.stock, producto.costo, producto.codigo_barra), tags=(tag,))
            datos.append((producto.productoID, producto.categoriaID, producto.nombre, producto.precio,
                                                producto.stock, producto.costo, producto.codigo_barra))
        return datos
    

    def ordenar_columna(self, columna):
        col_index = ["ID", "Categoria", "Nombre", "Precio", "Stock", "Costo", "CodBar"].index(columna)
        orden_inverso = getattr(self, "orden_inverso", False)
        self.datos.sort(key=lambda x: x[col_index], reverse=orden_inverso)
        self.orden_inverso = not orden_inverso
        for row in self.tree.get_children():
            self.tree.delete(row)
        for index, dato in enumerate(self.datos):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=dato, tags=(tag,))

    def crear_producto(self):
        # usuario = self.usuario_entry.get()
        # contrasena = self.contrasena_entry.get()
        # try:
        #     modelo_usuario = ModeloUsuario(usuario, contrasena)
        #     if not modelo_usuario.es_completo():
        #         raise ValueError("Faltan campos por completar")
        #     resultado, error = self.crud_usuario.crear_usuario(usuario, contrasena)
        #     if error:
        #         self.error_label.configure(text=error, text_color="#FF0000")  # Mensaje de error en rojo
        #         return
        #     self.usuario_entry.delete(0, "end")
        #     self.contrasena_entry.delete(0, "end")
        #     self.datos = self.cargar_usuarios()
        #     self.error_label.configure(text="Usuario creado con éxito.", text_color="#00FF00")  # Mensaje de éxito
        # except ValueError as e:
        #     self.error_label.configure(text=str(e), text_color="#FF0000")
        # except Exception as e:
        #     self.error_label.configure(text=f"Error inesperado: {str(e)}", text_color="#FF0000")
        pass


    def eliminar_producto(self):
        # selected_item = self.tree.selection()
        # if not selected_item:
        #     self.error_label.configure(text="Por favor, selecciona un usuario.", text_color="#FF0000")
        #     return
        # nombre_usuario = self.tree.item(selected_item)["values"][1]
        
        # if nombre_usuario.lower() == "admin":
        #     self.error_label.configure(text="No puede eliminar al usuario administrador.", text_color="#FF0000")
        #     return
        
        # try:
        #     self.crud_usuario.eliminar_usuario(nombre_usuario)
        #     self.datos = self.cargar_usuarios()
        #     self.error_label.configure(text="Usuario eliminado con éxito.", text_color="#00FF00")  # Mensaje de éxito
        # except Exception as e:
        #     self.error_label.configure(text=f"Error al eliminar el usuario: {str(e)}", text_color="#FF0000")
        pass
    
    
# ProductosApp()
