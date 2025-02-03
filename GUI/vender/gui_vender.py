import customtkinter as ctk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_producto import CRUD_producto
from gui.util.generic import centrar_ventana, destruir
from models.models.modelo_producto import ModeloProducto

class DetallesApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title('Listado de Productos')
        centrar_ventana(self.ventana, 1200, 650)
        self.ventana.resizable(width=0, height=0)

        self.ventana.configure(bg="#1C2124")
        self.frame_principal = ctk.CTkFrame(self.ventana, width=850, height=750, fg_color="#1C2124")
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=1)  # Barra de navegación
        self.frame_principal.grid_rowconfigure(1, weight=1)  # Treeview 
        self.frame_principal.grid_rowconfigure(2, weight=1)  # Label de error
        self.frame_principal.grid_rowconfigure(3, weight=1)  # Botones/campos busqueda productos
        self.frame_principal.grid_rowconfigure(4, weight=1)  # Total y boton finalizar
        
        
        ### BARRA DE NAVEGACION ###
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
            text="Productos",
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
        self.productos_button.place(x=367, y=10)

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

### TITULO ###
        # Label para el título, ajustado más cerca del listado
        self.label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestor de Ventas\nUsuario Logeado: Pepito",
            fg_color="#1C2124",
            font=("Helvetica", 30, "bold"),  # Tamaño del texto reducido para mayor ajuste
            text_color="#F3920F",
            height=40,
        )
        self.label_titulo.place(x=900, y=10, anchor="n")

        
        

        # Treeview que ocupa toda la pantalla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2C353A",
                        fieldbackground="#2C353A",
                        foreground="white",
                        rowheight=20,
                        borderwidth=2,
                        font=("Roboto", 14),
                        relief="solid")
        style.configure("Treeview.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 20, 'bold'))
        style.map("Treeview", background=[('selected', '#F3920F')])

        self.tree = ttk.Treeview(self.frame_principal, columns=("ID", "Nombre", "Precio", "Cantidad", "Stock", "Total"), show="headings", style="Treeview", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Stock", text="Stock")  
        self.tree.heading("Total", text="Total")

        self.tree.column("ID", anchor="center", width=50, minwidth=50)
        self.tree.column("Nombre", width=150, minwidth=100)
        self.tree.column("Precio", width=100, minwidth=100)
        self.tree.column("Cantidad", width=80, minwidth=60)
        self.tree.column("Stock", width=120, minwidth=100)
        self.tree.column("Total", width=100, minwidth=100)

        self.tree.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)


        self.scrollbar = ctk.CTkScrollbar(self.frame_principal, orientation="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=2, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Mensaje de error
        self.error_label = ctk.CTkLabel(self.frame_principal, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label.grid(row=3, column=0, columnspan=3, padx=10, sticky="ew")

        ### FRAME PARA CAMPOS Y BOTONES ####
        self.botones_frame = ctk.CTkFrame(self.frame_principal, height=50, fg_color="#1C2124")
        self.botones_frame.grid(row=4, column=0, columnspan=3, sticky="w", padx=5)
        self.botones_frame.grid_rowconfigure(5, weight=1)
        self.botones_frame.grid_columnconfigure(7, weight=1)

        # Label de entrada de codigo de barras
        self.label_cb = ctk.CTkLabel(self.botones_frame, text="Por Codigo de Barra", fg_color="#1C2124", font=("Helvetica", 16, "bold"), text_color="#F3920F")
        self.label_cb.grid(row=0, column=0, sticky="ew")

        # Campo de entrada para el código de barras
        self.codigo_barra_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Código de Barra", width=150)
        self.codigo_barra_entry.grid(row=1, column=0, padx=5, sticky="ew")
        
        # Label de entrada de nombre
        self.label_nombre = ctk.CTkLabel(self.botones_frame, text="Por Nombre", fg_color="#1C2124", font=("Helvetica", 17, "bold"), text_color="#F3920F")
        self.label_nombre.grid(row=0, column=1, sticky="ew")

        # Campo de entrada para el nombre
        self.nombre_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Nombre", width=150)
        self.nombre_entry.grid(row=1, column=1, padx=5, sticky="ew")
        
        # Boton Busqueda por Nombre
        self.boton_busqueda_por_nombre = ctk.CTkButton(self.botones_frame, text="Buscar por Nombre", border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.boton_busqueda_por_nombre.grid(row=2, column=1, padx=5, pady=5)
        
        # Label de entrada de ID
        self.label_id = ctk.CTkLabel(self.botones_frame, text="Por Identificador", fg_color="#1C2124", font=("Helvetica", 17, "bold"), text_color="#F3920F")
        self.label_id.grid(row=0, column=2, sticky="ew")

        # Campo de entrada para el ID
        self.id_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="ID", width=150)
        self.id_entry.grid(row=1, column=2, padx=5, sticky="ew")
        
        # Boton Busqueda por ID
        self.boton_busqueda_por_id = ctk.CTkButton(self.botones_frame, text="Buscar por ID", border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.boton_busqueda_por_id.grid(row=2, column=2, padx=5, pady=5)
        
        # Label de cantidad
        self.label_cantidad = ctk.CTkLabel(self.botones_frame, text="Cambiar Cantidad", fg_color="#1C2124", font=("Helvetica", 17, "bold"), text_color="#F3920F")
        self.label_cantidad.grid(row=0, column=3, sticky="ew")
        
        # Campo de entrada cantidad
        self.cantidad_entry = ctk.CTkEntry(self.botones_frame, width=150, placeholder_text="Cantidad")
        self.cantidad_entry.grid(row=1, column=3, padx=10)

        # Boton confirmar
        self.boton_modificar = ctk.CTkButton(self.botones_frame, text="Modificar Cantidad", command=self.modificar_cantidad, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.boton_modificar.grid(row=2, column=3, padx=10, pady=5)
        
        # Label de eliminar producto
        self.label_eliminar = ctk.CTkLabel(self.botones_frame, text="Eliminar Producto", fg_color="#1C2124", font=("Helvetica", 17, "bold"), text_color="#F3920F")
        self.label_eliminar.grid(row=1, column=4, sticky="ew")
        
        # Boton eliminar producto
        self.boton_eliminar = ctk.CTkButton(self.botones_frame, text="Eliminar", border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.boton_eliminar.grid(row=2, column=4, padx=30, pady=5)
        
        # Total de la venta
        self.total_label = ctk.CTkLabel(self.botones_frame, text="Total: $0", fg_color="#1C2124", font=("Helvetica", 30, "bold"), text_color="#F3920F")
        self.total_label.grid(row=0, column=5, padx=40)
        
        # Boton finalizar venta
        self.boton_eliminar = ctk.CTkButton(self.botones_frame, text="Finalizar Venta", border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.boton_eliminar.grid(row=2, column=5, padx=40, pady=5)

        self.crud_producto = CRUD_producto(Session)
        self.cargar_datos()

        self.codigo_barra_entry.bind("<KeyRelease>", self.buscar_por_codigo_de_barra)
    
        self.ventana.mainloop()
        
    #CARGAR POR CODIGO DE BARRA
    def buscar_por_codigo_de_barra(self, event):
        codigo_barra = self.codigo_barra_entry.get()

        # Solo procesar si el código de barra tiene 13 dígitos
        if len(codigo_barra) == 13:
            producto, error = self.crud_producto.obtener_producto_por_cb(codigo_barra)

            if producto:
                self.cargar_producto_en_treeview(producto)
                self.codigo_barra_entry.delete(0, 'end')  # Limpiar entrada para el siguiente código de barra
                self.error_label.configure(text="")
            else:
                self.error_label.configure(text="Producto no encontrado. Intenta de nuevo.")

    def buscar_por_nombre(self):
        """Busca un producto por nombre y lo muestra en el Treeview."""
        nombre = self.nombre_entry.get().strip()
        
        if not nombre:
            self.error_label.configure(text="Ingrese un nombre para buscar", text_color="#FF0000")
            return

        producto, error = self.crud_producto.obtener_producto_por_nombre(nombre)
        
        if error:
            self.error_label.configure(text=error, text_color="#FF0000")
            return


    def cargar_producto_en_treeview(self, producto):
        # Comprobar si el producto ya está en la lista
        item_existente = None
        for item in self.tree.get_children():
            if self.tree.item(item)["values"][0] == producto.productoID:
                item_existente = item
                break

        if item_existente:
            # Aumentar la cantidad solo si hay stock disponible
            cantidad_actual = int(self.tree.item(item_existente)["values"][3])  # Columna de cantidad
            if cantidad_actual + 1 <= producto.stock:  # Verificar stock
                nuevo_total = producto.precio * (cantidad_actual + 1)
                self.tree.item(item_existente, values=(producto.productoID, producto.nombre, producto.precio, cantidad_actual + 1, producto.stock, nuevo_total ))
            else:
                self.error_label.configure(text="No hay suficiente stock disponible.")
        else:
            # Agregar el producto con cantidad = 1 si hay stock disponible
            if producto.stock > 0:
                total_prod = producto.precio
                self.tree.insert("", "end", values=(producto.productoID, producto.nombre, producto.precio, 1, producto.stock, total_prod))
            else:
                self.error_label.configure(text="Producto sin stock disponible.")

        self.actualizar_total_venta()

    def modificar_cantidad(self):
        """Modifica la cantidad de un producto seleccionado en el Treeview basado en el campo de entrada."""
        selected_item = self.tree.selection()

        if not selected_item:
            self.error_label.configure(text="Seleccione un producto para modificar la cantidad.")
            return

        item_id = selected_item[0]
        values = self.tree.item(item_id)["values"]
        producto_id, nombre, precio, cantidad_actual, stock_disponible, total_actual,  = values

        try:
            nueva_cantidad = int(self.cantidad_entry.get())
            if nueva_cantidad > stock_disponible:
                self.error_label.configure(text=f"Cantidad excede el stock disponible ({stock_disponible}).")
            else:
                new_total = precio * nueva_cantidad
                self.tree.item(item_id, values=(producto_id, nombre, precio, nueva_cantidad, stock_disponible, new_total))
                self.actualizar_total_venta()
                self.error_label.configure(text="")  # Limpiar mensaje de error
                self.cantidad_entry.delete(0, "end")  # Limpiar campo de entrada después de actualizar
        except ValueError:
            self.error_label.configure(text="Ingrese un número válido.")
    
    def actualizar_total_venta(self):
        total = 0
        for item in self.tree.get_children():
            total+= (self.tree.item(item)["values"][5])  # Total está en la 5ta columna
        self.total_label.configure(text=f"Total: ${total}")

    def cargar_datos(self):
        # Aquí puedes cargar todos los productos si es necesario
        pass


