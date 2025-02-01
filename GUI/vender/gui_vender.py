import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_producto import CRUD_producto
from gui.util.generic import centrar_ventana, destruir
from models.models.modelo_producto import ModeloProducto

class DetallesApp:
   ### INIT - CONFIGURACION VENTANA ###
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
        self.frame_principal.grid_rowconfigure(1, weight=2)  # Treeview 
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
            text="Vender",
            fg_color="#1C2124",
            font=("Helvetica", 30, "bold"),  # Tamaño del texto reducido para mayor ajuste
            text_color="#F3920F",
            height=40,
        )
        self.label_titulo.place(x=900, y=10, anchor="n")

### TREEVIEW VENTANA PRINCIPAL ###
        # Estilos del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2C353A",
                        fieldbackground="#2C353A",
                        foreground="white",
                        rowheight=15,
                        borderwidth=2,
                        font=("Roboto", 14),
                        relief="solid")
        style.configure("Treeview.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 20, 'bold'))
        style.map("Treeview", background=[('selected', '#F3920F')])

        self.tree = ttk.Treeview(self.frame_principal, columns=("VentaID", "ProdID", "Nombre", "Categoria", "Stock", "Cant","Precio","PrecioxCantidad"), show="headings", style="Treeview", height=15)
        self.tree.heading("VentaID", text="VentaID")
        self.tree.heading("ProdID", text="ProdID")
        self.tree.heading("Categoria", text="Categoria",)
        self.tree.heading("Nombre", text="Nombre",)
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Cant", text="Cant")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("PrecioxCantidad", text="PrecioxCantidad")

        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=0)
        
        self.tree.column("VentaID", anchor="center", width=150, minwidth=150, stretch=False)
        self.tree.column("ProdID", width=150, minwidth=150)
        self.tree.column("Categoria", width=370, minwidth=370)
        self.tree.column("Nombre", width=370, minwidth=370)
        self.tree.column("Stock", width=150, minwidth=150)
        self.tree.column("Cant", width=150, minwidth=150)
        self.tree.column("Precio", width=150, minwidth=150)
        self.tree.column("PrecioxCantidad", width=270, minwidth=270)


### SCROLLBAR ###
        self.scrollbar = ctk.CTkScrollbar(self.frame_principal, orientation="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

### LABEL PARA MENSAJES DE ERROR ###
        self.error_label = ctk.CTkLabel(self.frame_principal, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label.grid(row=2, column=0, columnspan=3, padx=10, pady=0, sticky="ew")



### CRUD ###
        self.crud_producto = CRUD_producto(Session)

        self.ventana.mainloop()

    def on_codigo_barra_change(self, event):
        codigo_barra = self.codigo_barra_entry.get()
        if len(codigo_barra) == 13:
            producto, error = self.crud_producto.obtener_producto_por_cb(codigo_barra)
            if producto:
                self.cargar_producto_en_treeview(producto)
                self.codigo_barra_entry.delete(0, 'end')
                self.error_label.configure(text="")
            else:
                self.error_label.configure(text="Producto no encontrado. Intenta de nuevo.")

    def cargar_producto_en_treeview(self, producto):
        item_existente = None
        for item in self.tree.get_children():
            if self.tree.item(item)["values"][0] == producto.productoID:
                item_existente = item
                break

        if item_existente:
            cantidad_actual = int(self.tree.item(item_existente)["values"][3])
            nuevo_total = producto.precio * (cantidad_actual + 1)
            self.tree.item(item_existente, values=(producto.productoID, producto.nombre, 
                                                   producto.precio, cantidad_actual + 1, nuevo_total))
        else:
            total_prod = producto.precio
            self.tree.insert("", "end", values=(producto.productoID, producto.nombre, 
                                                 producto.precio, 1, total_prod))

        self.actualizar_total_venta()

    def on_treeview_item_edit(self, event):
        item_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if col == '#4':
            old_value = self.tree.item(item_id)["values"][3]
            new_value = self.prompt_for_quantity(old_value)
            if new_value:
                producto_id = self.tree.item(item_id)["values"][0]
                producto, error = self.crud_producto.obtener_producto_por_id(producto_id)
                if producto:
                    if new_value <= producto.stock:
                        new_total = producto.precio * new_value
                        self.tree.item(item_id, values=(producto.productoID, producto.nombre, 
                                                         producto.precio, new_value, new_total))
                        self.actualizar_total_venta()
                    else:
                        self.error_label.configure(text=f"Cantidad excede el stock disponible ({producto.stock})")

    def prompt_for_quantity(self, current_quantity):
        top = ctk.CTkToplevel(self.ventana)
        top.title("Modificar Cantidad")
        top.geometry("300x150")
        top.configure(bg="#1C2124")

        label = ctk.CTkLabel(top, text="Ingrese la nueva cantidad", fg_color="#1C2124", font=("Helvetica", 14), text_color="white")
        label.pack(pady=10)

        quantity_entry = ctk.CTkEntry(top, width=200)
        quantity_entry.insert(0, current_quantity)
        quantity_entry.pack(pady=5)

        def on_confirm():
            new_quantity = int(quantity_entry.get())
            top.destroy()
            return new_quantity

        ctk.CTkButton(top, text="Confirmar", command=on_confirm).pack(pady=10)
        top.mainloop()

    def actualizar_total_venta(self):
        total = sum(float(self.tree.item(item)["values"][4]) for item in self.tree.get_children())
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def cargar_datos(self):
        pass
