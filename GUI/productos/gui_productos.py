import customtkinter as ctk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_producto import CRUD_producto
from data.crud.crud_categoria import CRUD_categoria
from gui.util.generic import centrar_ventana
from gui.util.nav import navegacion, boton_libro, boton_ventas, boton_usuarios, titulo, menu_label
from models.models.modelo_producto import ModeloProducto
from models.models.modelo_categoria import ModeloCategoria


class ProductosApp:
### INIT - CONFIGURACION VENTANA ###
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title('Listado de Productos')
        centrar_ventana(self.ventana, 1200, 650)
        self.ventana.resizable(width=0, height=0)

        self.ventana.configure(bg="#1C2124")
        self.frame_principal = ctk.CTkFrame(self.ventana, width=850, height=750, fg_color="#1C2124")
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.frame_principal.columnconfigure(0, weight=1)  # Expandir en el ancho
        self.frame_principal.rowconfigure(0, weight=0)  # Fila para el frame superior
        self.frame_principal.rowconfigure(1, weight=1)  # Fila para el contenido principal

        navegacion(self)
        menu_label(self)
        boton_libro(self, 1)
        boton_usuarios(self, 2)
        boton_ventas(self, 3)        
        titulo(self, "Gestor de Productos y Categorias", 4)


### TREEVIEW VENTANA PRINCIPAL ###
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
        style.configure("Treeview.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 13, 'bold'))
        style.map("Treeview", background=[('selected', '#F3920F')])

        self.tree = ttk.Treeview(self.frame_principal, columns=("ID", "Categoria", "Nombre", "Precio", "Stock", "Costo", "Ganancia Unitaria", "Ganancia Acumulada", "CodBar"), show="headings", style="Treeview", height=15)

        self.tree.heading("ID", text="ID", command=lambda: self.ordenar_columna("ID"))
        self.tree.heading("Categoria", text="Categoria", command=lambda: self.ordenar_columna("Categoria"))
        self.tree.heading("Nombre", text="Nombre", command=lambda: self.ordenar_columna("Nombre"))
        self.tree.heading("Precio", text="Precio", command=lambda: self.ordenar_columna("Precio"))
        self.tree.heading("Stock", text="Stock", command=lambda: self.ordenar_columna("Stock"))
        self.tree.heading("Costo", text="Costo", command=lambda: self.ordenar_columna("Costo"))
        self.tree.heading("Ganancia Unitaria", text="Ganancia", command=lambda: self.ordenar_columna("Ganancia Unitaria")) 
        self.tree.heading("Ganancia Acumulada", text="GananAcumu", command=lambda: self.ordenar_columna("Ganancia Acumulada"))
        self.tree.heading("CodBar", text="CodBar", command=lambda: self.ordenar_columna("CodBar"))


        # Agregamos el Treeview al grid
        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Ajustar tamaños de columnas
        self.tree.column("ID", anchor="center", width=10)  
        self.tree.column("Categoria", width=100, minwidth=100)  
        self.tree.column("Nombre", width=100)
        self.tree.column("Precio", width=40)
        self.tree.column("Stock", width=30)
        self.tree.column("Costo", width=40)
        self.tree.column("Ganancia Unitaria", width=80, minwidth=70)  
        self.tree.column("Ganancia Acumulada", width=90, minwidth=80)  
        self.tree.column("CodBar", width=100, minwidth=90)



### SCROLLBAR ###
        self.scrollbar = ctk.CTkScrollbar(self.frame_principal, orientation="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=3, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

### LABEL PARA MENSAJES DE ERROR ###
        self.error_label = ctk.CTkLabel(self.frame_principal, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

### FRAME PARA CAMPOS Y BOTONES ####
        self.botones_frame = ctk.CTkFrame(self.frame_principal, height=50, fg_color="#1C2124")
        self.botones_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.botones_frame.grid_rowconfigure(5, weight=1)
        self.botones_frame.grid_columnconfigure(7, weight=1)


### CRUD ###
        self.crud_producto = CRUD_producto(Session)
        self.crud_categoria = CRUD_categoria(Session)
        self.cargar_datos()

### BOTONES Y CAMPOS ###
        # Botón Crear Producto
        self.crear_producto_button = ctk.CTkButton(self.botones_frame, text="Crear Producto", command=self.crear_producto, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.crear_producto_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Botón Crear Producto
        self.modificar_producto_button = ctk.CTkButton(self.botones_frame, text="Modificar Producto", command=self.modificar_producto, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.modificar_producto_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Campo y botón para buscar por nombre
        self.buscar_nombre_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Nombre del producto", width=200)
        self.buscar_nombre_entry.grid(row=2, column=1, padx=10, sticky="ew")

        self.buscar_nombre_button = ctk.CTkButton(
            self.botones_frame, text="Buscar por Nombre", command=self.buscar_por_nombre,
            border_width=2, fg_color="#1C2124", text_color="white",
            font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F"
        )
        self.buscar_nombre_button.grid(row=3, column=1, padx=10, sticky="ew")

        # Campo y botón para buscar por código de barra
        self.buscar_codigo_barra_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Código de Barra", width=200)
        self.buscar_codigo_barra_entry.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        self.buscar_cb_button = ctk.CTkButton(
            self.botones_frame, text="Buscar por Código de Barra", command=self.buscar_por_codigo_barra,
            border_width=2, fg_color="#1C2124", text_color="white",
            font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F"
        )
        self.buscar_cb_button.grid(row=3, column=3, padx=10, sticky="ew")


        # Botones Eliminar Producto
        self.eliminar_producto_button = ctk.CTkButton(self.botones_frame, text="Eliminar Producto", command=self.eliminar_producto, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.eliminar_producto_button.grid(row=3, column=4, padx=10, sticky="ew")
        
        # Botones Ver Todos los Producto
        self.ver_todos_button = ctk.CTkButton(self.botones_frame, text="Ver Todos Los Productos", command=self.cargar_datos, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.ver_todos_button.grid(row=2, column=4, padx=10, sticky="ew")
        
        # Campos para crear categoria
        self.categoria_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Nombre de categoria", width=200)
        self.categoria_entry.grid(row=2, column=5, padx=10, pady=5, sticky="ew")
        
        # Boton Crear Categoria
        self.crear_categoria_button = ctk.CTkButton(self.botones_frame, text="Crear Categoria", command=self.crear_categoria,  border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.crear_categoria_button.grid(row=3, column=5, padx=10, sticky="ew")
        
        # Boton Modificar Categorias
        self.crear_categoria_button = ctk.CTkButton(self.botones_frame, text="Modificar Categorias", command=self.modificar_categoria,  border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.crear_categoria_button.grid(row=3, column=6, padx=10, sticky="ew")

        self.ventana.mainloop()

                                                            ### METODOS ###


### TREE VIEW METODOS ###
    def cargar_datos(self):
        productos = self.crud_producto.obtener_todos_productos()
        
        # Limpiar el Treeview antes de cargar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        self.datos = []
        
        # Si no hay productos, mostrar mensaje en la primera fila
        if not productos:
            self.tree.insert("", "end", values=("NO", "HAY PRODUCTOS", "CARGADOS", "", "", "", "", "", ""), tags=("empty",))
            return self.datos
        
        for index, (productoID, nombre, precio, stock, costo, codigo_barra, ganancia_acumulada, ganancia_unidad, categoria_nombre) in enumerate(productos):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            
            self.tree.insert(
                "", "end",
                values=(
                    productoID, categoria_nombre, nombre, int(precio),
                    stock, int(costo), int(ganancia_unidad), int(ganancia_acumulada), codigo_barra  # 🔥 Se agrega la ganancia unitaria y acumulada
                ),
                tags=(tag,)
            )
            
            # Guardar datos para ordenamiento
            self.datos.append((
                productoID, categoria_nombre, nombre, precio,
                stock, costo, ganancia_unidad, ganancia_acumulada, codigo_barra
            ))
        
        return self.datos


    def ordenar_columna(self, columna):
        col_index = ["ID", "Categoria", "Nombre", "Precio", "Stock", "Costo", "CodBar"].index(columna)
        orden_inverso = getattr(self, "orden_inverso", False)
        
        # Ordenar por nombre de la categoría si es la columna "Categoria"
        if columna == "Categoria":
            self.datos.sort(key=lambda x: x[1], reverse=orden_inverso)
        else:
            self.datos.sort(key=lambda x: x[col_index], reverse=orden_inverso)
        
        self.orden_inverso = not orden_inverso
        
        # Limpiar y volver a cargar los datos ordenados
        for row in self.tree.get_children():
            self.tree.delete(row)
        for index, dato in enumerate(self.datos):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=dato, tags=(tag,))
            
            
    def buscar_por_nombre(self):
        """Busca un producto por nombre y lo muestra en el Treeview."""
        nombre = self.buscar_nombre_entry.get().strip()
        
        if not nombre:
            self.error_label.configure(text="Ingrese un nombre para buscar", text_color="#FF0000")
            return

        producto, error = self.crud_producto.obtener_producto_por_nombre(nombre)
        
        if error:
            self.error_label.configure(text=error, text_color="#FF0000")
            return
        
        # Limpiar Treeview y mostrar solo el producto encontrado
        self.tree.delete(*self.tree.get_children())  # Borra los datos actuales
        self.tree.insert("", "end", values=(
            producto.productoID, self.categoria_nombre, producto.nombre,
            int(producto.precio), producto.stock, int(producto.costo),
            producto.codigo_barra
        ))

    def buscar_por_codigo_barra(self):
        """Busca un producto por código de barra y lo muestra en el Treeview."""
        codigo_barra = self.buscar_codigo_barra_entry.get().strip()
        
        if not codigo_barra:
            self.error_label.configure(text="Ingrese un código de barra para buscar", text_color="#FF0000")
            return

        producto, error = self.crud_producto.obtener_producto_por_cb(codigo_barra)
        
        if error:
            self.error_label.configure(text=error, text_color="#FF0000")
            return
        
        # Limpiar Treeview y mostrar solo el producto encontrado
        self.tree.delete(*self.tree.get_children())  
        self.tree.insert("", "end", values=(
            producto.productoID, self.categoria_nombre, producto.nombre,
            int(producto.precio), producto.stock, int(producto.costo),
            producto.codigo_barra
        ))
            

    def aceptar(self):
        """Valida y guarda el producto."""
        try:
            # Validación de los datos del producto
            modelo_producto = ModeloProducto(
                nombre=self.nombre_var.get(),
                precio=self.precio_var.get(),
                stock=self.stock_var.get(),
                costo=self.costo_var.get(),
                codigo_barra=self.codigo_barra_var.get(),
            )
            if not modelo_producto.es_completo():
                raise ValueError("Faltan campos por completar")

            # Obtener el ID de la categoría seleccionada
            self.categoria_nombre = self.categoria_var.get()  # Nombre de la categoría seleccionada
            categoria_id = self.categorias_dict.get(self.categoria_nombre)  # ID correspondiente

            if not categoria_id:
                raise ValueError("Categoría no válida seleccionada")

            # Crear producto en la base de datos
            resultado, error = self.crud_producto.crear_producto(
                modelo_producto.nombre,
                modelo_producto.precio,
                modelo_producto.stock,
                modelo_producto.costo,
                modelo_producto.codigo_barra,
                categoria_id
            )
            if error:
                self.mensaje_label.configure(text=error, text_color="#FF0000")
                return

            self.cargar_datos()
            
            # Mostrar éxito y limpiar campos
            self.mensaje_label.configure(text="Producto creado con éxito", text_color="#00FF00")
            self.nombre_var.set("")
            self.precio_var.set("")
            self.stock_var.set("")
            self.costo_var.set("")
            self.codigo_barra_var.set("")
            self.categoria_var.set("")
            self.nombre_entry.focus()

        except ValueError as ve:
            # Errores de validación controlados
            self.mensaje_label.configure(text=str(ve), text_color="#FF0000")
        except Exception as e:
            # Errores inesperados
            self.mensaje_label.configure(text=f"Error inesperado: {str(e)}", text_color="#FF0000")


    def crear_producto(self):
        """Abre una ventana emergente para crear un producto."""
        # Crear ventana emergente
        self.popup_crear = ctk.CTkToplevel(self.ventana)
        self.popup_crear.title("Crear Producto")
        self.popup_crear.transient(self.ventana)  # Marcar como ventana hija
        self.popup_crear.grab_set()  # Bloquear interacción con la ventana principal
        centrar_ventana(self.popup_crear, 600, 400)  # Centrar la ventana

        # Configurar diseño de la ventana emergente
        
        self.popup_crear.configure(bg="#1C2124", fg_color="#1C2124")
        self.popup_crear.grid_columnconfigure(0, weight=1)
        self.popup_crear.grid_columnconfigure(1, weight=1)

        # Variables de entrada
        self.nombre_var = ctk.StringVar()
        self.precio_var = ctk.StringVar()
        self.stock_var = ctk.StringVar()
        self.costo_var = ctk.StringVar()
        self.codigo_barra_var = ctk.StringVar()
        self.categoria_var = ctk.StringVar()

        # Etiquetas y entradas
        ctk.CTkLabel(
            self.popup_crear, text="Nombre:", font=("Helvetica", 16, "bold"),
            text_color="#F3920F", fg_color="#1C2124"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.nombre_entry = ctk.CTkEntry(
            self.popup_crear, textvariable=self.nombre_var, width=250,
            fg_color="#2C353A", text_color="#FFFFFF"
        )
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            self.popup_crear, text="Precio:", font=("Helvetica", 16, "bold"),
            text_color="#F3920F", fg_color="#1C2124"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="e")

        ctk.CTkEntry(
            self.popup_crear, textvariable=self.precio_var, width=250,
            fg_color="#2C353A", text_color="#FFFFFF"
        ).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            self.popup_crear, text="Stock:", font=("Helvetica", 16, "bold"),
            text_color="#F3920F", fg_color="#1C2124"
        ).grid(row=2, column=0, padx=10, pady=5, sticky="e")

        ctk.CTkEntry(
            self.popup_crear, textvariable=self.stock_var, width=250,
            fg_color="#2C353A", text_color="#FFFFFF"
        ).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            self.popup_crear, text="Costo:", font=("Helvetica", 16, "bold"),
            text_color="#F3920F", fg_color="#1C2124"
        ).grid(row=3, column=0, padx=10, pady=5, sticky="e")

        ctk.CTkEntry(
            self.popup_crear, textvariable=self.costo_var, width=250,
            fg_color="#2C353A", text_color="#FFFFFF"
        ).grid(row=3, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            self.popup_crear, text="Código de Barra:", font=("Helvetica", 16, "bold"),
            text_color="#F3920F", fg_color="#1C2124"
        ).grid(row=4, column=0, padx=10, pady=5, sticky="e")

        ctk.CTkEntry(
            self.popup_crear, textvariable=self.codigo_barra_var, width=250,
            fg_color="#2C353A", text_color="#FFFFFF"
        ).grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Listado de categorías
        categorias = self.crud_categoria.obtener_categorias()
        if isinstance(categorias, tuple):
            categorias, error = categorias
            if error:
                self.mensaje_label.configure(text=error, text_color="#FF0000")
                return

        # Crear un diccionario para mapear nombres a IDs
        self.categorias_dict = {nombre: id_ for id_, nombre in categorias}

        # Desplegable de categorías
        ctk.CTkLabel(
            self.popup_crear, text="Categoría:", font=("Helvetica", 16, "bold"),
            text_color="#F3920F", fg_color="#1C2124"
        ).grid(row=5, column=0, padx=10, pady=5, sticky="e")

        categoria_dropdown = ctk.CTkOptionMenu(
            self.popup_crear, variable=self.categoria_var, values=list(self.categorias_dict.keys()),
            fg_color="#2C353A", text_color="#FFFFFF", dropdown_hover_color="#2C353A"
        )
        categoria_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Mensaje de error/success
        self.mensaje_label = ctk.CTkLabel(
            self.popup_crear, text="", font=("Helvetica", 14, "bold"),
            text_color="#FF0000", fg_color="#1C2124"
        )
        self.mensaje_label.grid(row=6, column=0, columnspan=2, pady=10)

        # Botón para aceptar
        ctk.CTkButton(
            self.popup_crear, text="Aceptar", command=self.aceptar,
            border_width=2, fg_color="#1C2124", text_color="#F3920F",
            font=("Helvetica", 16, "bold"), hover_color="#2C353A",
            border_color="#F3920F", width=150, height=50
        ).grid(row=7, column=0, columnspan=2, pady=15)
        
        
    def modificar_producto(self):
        """Abre una ventana emergente para modificar un producto seleccionado en el Treeview."""
        
        # Obtener producto seleccionado
        item = self.tree.focus()
        if not item:
            self.error_label.configure(text="Seleccione un producto para modificar", text_color="#000000")
            return

        self.valores = self.tree.item(item, "values")
        if not self.valores:
            self.error_label.configure(text="Error al obtener datos del producto", text_color="#FF0000")
            return

        # Crear ventana emergente
        self.popup_modificar = ctk.CTkToplevel(self.ventana)
        self.popup_modificar.title("Modificar Producto")
        self.popup_modificar.transient(self.ventana)  # Marcar como ventana hija
        self.popup_modificar.grab_set()  # Bloquear interacción con la ventana principal
        centrar_ventana(self.popup_modificar, 600, 400)  # Centrar la ventana

        self.popup_modificar.configure(bg="#1C2124", fg_color="#1C2124")
        self.popup_modificar.grid_columnconfigure(0, weight=1)
        self.popup_modificar.grid_columnconfigure(1, weight=1)

        # Variables de entrada
        self.nombre_var_mod = ctk.StringVar(value=self.valores[2])
        self.precio_var_mod = ctk.StringVar(value=self.valores[3])
        self.stock_var_mod = ctk.StringVar(value=self.valores[4])
        self.costo_var_mod = ctk.StringVar(value=self.valores[5])
        self.codigo_barra_var_mod = ctk.StringVar(value=self.valores[8])
        self.categoria_var_mod = ctk.StringVar(value=self.valores[1])

        # Etiquetas y entradas
        labels = ["Nombre:", "Precio:", "Stock:", "Costo:", "Código de Barra:", "Categoría:"]
        variables = [self.nombre_var_mod, self.precio_var_mod, self.stock_var_mod, self.costo_var_mod, self.codigo_barra_var_mod]

        for i, (label, var) in enumerate(zip(labels, variables)):
            ctk.CTkLabel(self.popup_modificar, text=label, font=("Helvetica", 16, "bold"),
                        text_color="#F3920F", fg_color="#1C2124").grid(row=i, column=0, padx=10, pady=5, sticky="e")

            ctk.CTkEntry(self.popup_modificar, textvariable=var, width=250,
                        fg_color="#2C353A", text_color="#FFFFFF").grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # Obtener categorías
        categorias = self.crud_categoria.obtener_categorias()
        if isinstance(categorias, tuple):
            categorias, error = categorias
            if error:
                self.mensaje_label.configure(text=error, text_color="#FF0000")
                return

        self.categorias_dict = {nombre: id_ for id_, nombre in categorias}

        # Desplegable de categorías
        ctk.CTkLabel(self.popup_modificar, text="Categoría:", font=("Helvetica", 16, "bold"),
                    text_color="#F3920F", fg_color="#1C2124").grid(row=5, column=0, padx=10, pady=5, sticky="e")

        categoria_dropdown = ctk.CTkOptionMenu(self.popup_modificar, variable=self.categoria_var_mod, 
                                            values=list(self.categorias_dict.keys()),
                                            fg_color="#2C353A", text_color="#FFFFFF", dropdown_hover_color="#2C353A")
        categoria_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Mensaje de error/success
        self.mensaje_label = ctk.CTkLabel(self.popup_modificar, text="", font=("Helvetica", 14, "bold"),
                                        text_color="#FF0000", fg_color="#1C2124")
        self.mensaje_label.grid(row=6, column=0, columnspan=2, pady=10)

        # Botón para aceptar cambios
        ctk.CTkButton(self.popup_modificar, text="Guardar Cambios", command=self.guardar_cambios_producto,
                    border_width=2, fg_color="#1C2124", text_color="#F3920F",
                    font=("Helvetica", 16, "bold"), hover_color="#2C353A",
                    border_color="#F3920F", width=150, height=50).grid(row=7, column=0, columnspan=2, pady=15)
        

    def guardar_cambios_producto(self):
        """Valida y guarda el producto."""
        try:
            # Validación de los datos del producto
            modelo_producto_mod = ModeloProducto(
                nombre=self.nombre_var_mod.get(),
                precio=self.precio_var_mod.get(),
                stock=self.stock_var_mod.get(),
                costo=self.costo_var_mod.get(),
                codigo_barra=self.codigo_barra_var_mod.get(),
            )
            if not modelo_producto_mod.es_completo():
                raise ValueError("Faltan campos por completar")

            # Obtener el ID de la categoría seleccionada
            self.categoria_nombre = self.categoria_var_mod.get()  # Nombre de la categoría seleccionada
            categoria_id = self.categorias_dict.get(self.categoria_nombre)  # ID correspondiente

            if not categoria_id:
                raise ValueError("Categoría no válida seleccionada")

            # Crear producto en la base de datos
            resultado, error = self.crud_producto.actualizar_producto(
                self.valores[2],
                modelo_producto_mod.nombre,
                modelo_producto_mod.precio,
                modelo_producto_mod.stock,
                modelo_producto_mod.costo,
                modelo_producto_mod.codigo_barra,
                categoria_id
            )
            if error:
                self.mensaje_label.configure(text=error, text_color="#FF0000")
                return

            self.cargar_datos()
            
            # Mostrar éxito 
            self.mensaje_label.configure(text="Producto modificado con éxito", text_color="#00FF00")

        except ValueError as ve:
            # Errores de validación controlados
            self.mensaje_label.configure(text=str(ve), text_color="#FF0000")
        except Exception as e:
            # Errores inesperados
            self.mensaje_label.configure(text=f"Error inesperado: {str(e)}", text_color="#FF0000")
                

    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.error_label.configure(text="Por favor, selecciona un producto.", text_color="#FF0000")
            return
        nombre_producto = self.tree.item(selected_item)["values"][2]
        
        try:
            self.crud_producto.eliminar_producto(nombre_producto)
            self.datos = self.cargar_datos()
            self.error_label.configure(text="Producto eliminado con éxito.", text_color="#00FF00")  # Mensaje de éxito
        except Exception as e:
            self.error_label.configure(text=f"Error al eliminar el producto: {str(e)}", text_color="#FF0000")
        
    def crear_categoria(self):
        categoria = self.categoria_entry.get()
        try:
            modelo_categoria = ModeloCategoria(categoria)
            resultado, error = self.crud_categoria.crear_categoria(categoria)
            if error:
                self.error_label.configure(text=error, text_color="#FF0000")  # Mensaje de error en rojo
                return
            self.categoria_entry.delete(0, "end")
            self.error_label.configure(text="Categoria creada con éxito.", text_color="#00FF00")  # Mensaje de éxito
        except ValueError as e:
            self.error_label.configure(text=str(e), text_color="#FF0000")
        except Exception as e:
            self.error_label.configure(text=f"Error inesperado: {str(e)}", text_color="#FF0000")    
            
            
    def modificar_categoria(self):
        """Abre una ventana emergente para crear un producto."""
        # Crear ventana emergente
        self.popup_modifica_cat = ctk.CTkToplevel(self.ventana)
        self.popup_modifica_cat.title("Modificar/Eliminar Categorias")
        self.popup_modifica_cat.transient(self.ventana)  # Marcar como ventana hija
        self.popup_modifica_cat.grab_set()  # Bloquear interacción con la ventana principal
        centrar_ventana(self.popup_modifica_cat, 600, 450)  # Centrar la ventana

        # Configurar diseño de la ventana emergente
        
        self.popup_modifica_cat.configure(bg="#1C2124", fg_color="#1C2124")
        self.popup_modifica_cat.grid_columnconfigure(0, weight=1)
        self.popup_modifica_cat.grid_columnconfigure(1, weight=1)
                
        # Estilos del Treeview
        style_popup = ttk.Style()
        style_popup.theme_use("clam")
        style_popup.configure("Treeview_popup",
                        background="#2C353A",
                        fieldbackground="#2C353A",
                        foreground="white",
                        rowheight=30,
                        borderwidth=2,
                        relief="solid")
        style_popup.configure("Treeview_popup.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 12, 'bold'))
        style_popup.map("Treeview_popup", background=[('selected', '#F3920F')])

        self.tree_popup = ttk.Treeview(self.popup_modifica_cat, columns=("Categoria"), show="headings", style="Treeview")
        self.tree_popup.heading("Categoria", text="Categoria")
        self.tree_popup.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Scrollbar
        self.scrollbar_popup = ctk.CTkScrollbar(self.popup_modifica_cat, orientation="vertical", command=self.tree_popup.yview)
        self.scrollbar_popup.grid(row=1, column=3, sticky="ns")
        self.tree_popup.configure(yscrollcommand=self.scrollbar_popup.set)

        # Label para mensajes de error
        self.error_label_popup = ctk.CTkLabel(self.popup_modifica_cat, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label_popup.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Frame para campos y botones
        self.botones_frame_popup = ctk.CTkFrame(self.popup_modifica_cat, height=40, fg_color="#1C2124")
        self.botones_frame_popup.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.botones_frame_popup.grid_rowconfigure(0, weight=1)
        
        self.cargar_categorias()
        
        # Campo para modificar nombre categoria
        self.modificar_nombre_entry_popup = ctk.CTkEntry(self.botones_frame_popup, placeholder_text="Nueva Nombre", width=200)
        self.modificar_nombre_entry_popup.grid(row=1, column=1, padx=50,  pady=5, sticky="w")
        
        # Botón Modificar nombre categoria
        self.modificar_nombre_button_popup = ctk.CTkButton(self.botones_frame_popup, text="Modificar Categoria", border_width=2, command=self.modificar_nombre, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.modificar_nombre_button_popup.grid(row=2, column=1, padx=80, sticky="w")

        # Boton Eliminar Categoria
        self.eliminar_categoria_button_popup = ctk.CTkButton(self.botones_frame_popup, text="Eliminar Categoria", border_width=2, command=self.eliminar_categoria, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.eliminar_categoria_button_popup.grid(row=2, column=2, padx=30, sticky="e")
        
        
    def cargar_categorias(self):
        categorias, error = self.crud_categoria.obtener_categorias()
        if error:
            print(error)
            return []

        # Limpiar el árbol actual
        for row in self.tree_popup.get_children():
            self.tree_popup.delete(row)
            
        datos = []
        for _, nombre in categorias:  # Ignorar el ID
            self.tree_popup.insert("", "end", values=(nombre,))
            datos.append(nombre)
        return datos  
    
    
    def modificar_nombre(self):
        nombre_nuevo = self.modificar_nombre_entry_popup.get()
        selected_item = self.tree_popup.selection()

        if not selected_item:
            self.error_label_popup.configure(text="Por favor, selecciona una categoria.", text_color="#FF0000")
            return

        nombre_categoria = self.tree_popup.item(selected_item)["values"][0]

        if nombre_categoria == "Sin Categoria":
            self.error_label_popup.configure(text="No puede modificar la categoria auxiliar: Sin Categoria")
            return

        try:
            modelo_categoria = ModeloCategoria(nombre_nuevo)
            resultado, error = self.crud_categoria.actualizar_categoria(nombre_categoria, nombre_nuevo)

            if error:  # Verificar si hay un error
                self.error_label_popup.configure(text=error, text_color="#FF0000")
            else:
                self.modificar_nombre_entry_popup.delete(0, "end")
                self.cargar_categorias()
                self.cargar_datos()
                self.error_label_popup.configure(text="Categoría actualizada con éxito.", text_color="#00FF00")  # Mensaje de éxito
        except ValueError as e:
            self.error_label_popup.configure(text=str(e), text_color="#FF0000")
        except Exception as e:
            self.error_label_popup.configure(text=f"Error inesperado: {str(e)}", text_color="#FF0000")
    

    def eliminar_categoria(self):
        selected_item = self.tree_popup.selection()
        if not selected_item:
            self.error_label_popup.configure(text="Por favor, selecciona una categoria.", text_color="#FF0000")
            return
        nombre_categoria = self.tree_popup.item(selected_item)["values"][0]
        
        if nombre_categoria == "Sin Categoria":
            self.error_label_popup.configure(text="No puede eliminar la categoria auxiliar: Sin Categoria", text_color="#FF0000")
            return
        
        try:
            self.crud_categoria.eliminar_categoria(nombre_categoria)
            self.cargar_categorias()
            self.error_label_popup.configure(text="Categoria eliminada con éxito.", text_color="#00FF00")  # Mensaje de éxito
            self.datos = self.cargar_datos()
        except Exception as e:
            self.error_label_popup.configure(text=f"Error al eliminar la categoria: {str(e)}", text_color="#FF0000")
            
    
    # ProductosApp()
