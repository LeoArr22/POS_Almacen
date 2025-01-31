import customtkinter as ctk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_producto import CRUD_producto
from gui.util.generic import centrar_ventana, destruir
from models.models.modelo_producto import ModeloProducto

class DetallesApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title('Gestor de Detalles de Venta')
        centrar_ventana(self.ventana, 1200, 650)
        self.ventana.resizable(width=0, height=0)

        self.ventana.configure(bg="#1C2124")
        self.frame_principal = ctk.CTkFrame(self.ventana, width=850, height=750, fg_color="#1C2124")
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)

        # Treeview que ocupa toda la pantalla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2C353A", fieldbackground="#2C353A", foreground="white", rowheight=25, borderwidth=2, font=("Roboto", 14), relief="solid")
        style.configure("Treeview.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 20, 'bold'))
        style.map("Treeview", background=[('selected', '#F3920F')])

        self.tree = ttk.Treeview(self.frame_principal, columns=("ID", "Nombre", "Precio", "Cantidad", "Total"), show="headings", style="Treeview", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Total", text="Total")
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.tree.column("ID", anchor="center", width=50, minwidth=50)
        self.tree.column("Nombre", width=150, minwidth=100)
        self.tree.column("Precio", width=100, minwidth=100)
        self.tree.column("Cantidad", width=80, minwidth=60)
        self.tree.column("Total", width=100, minwidth=100)

        self.scrollbar = ctk.CTkScrollbar(self.frame_principal, orientation="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Campo de entrada para el código de barras
        self.codigo_barra_entry = ctk.CTkEntry(self.frame_principal, placeholder_text="Código de Barra", width=200)
        self.codigo_barra_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Mensaje de error
        self.error_label = ctk.CTkLabel(self.frame_principal, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")

        # Total de la venta
        self.total_label = ctk.CTkLabel(self.frame_principal, text="Total: $0.00", fg_color="#1C2124", font=("Helvetica", 20, "bold"), text_color="#F3920F")
        self.total_label.grid(row=3, column=0, columnspan=3, pady=20)

        self.crud_producto = CRUD_producto(Session)
        self.cargar_datos()

        self.codigo_barra_entry.bind("<KeyRelease>", self.on_codigo_barra_change)

        # Evento para modificar la cantidad
        self.tree.bind('<Double-1>', self.on_treeview_item_edit)
        
        self.ventana.mainloop()

    def on_codigo_barra_change(self, event):
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

    def cargar_producto_en_treeview(self, producto):
        # Comprobar si el producto ya está cargado
        item_existente = None
        for item in self.tree.get_children():
            if self.tree.item(item)["values"][0] == producto.productoID:  # Compara el ID del producto
                item_existente = item
                break

        if item_existente:
            # Si el producto ya está, aumentar la cantidad y actualizar el total
            cantidad_actual = int(self.tree.item(item_existente)["values"][3])
            nuevo_total = producto.precio * (cantidad_actual + 1)
            self.tree.item(item_existente, values=(producto.productoID, producto.nombre, producto.precio, cantidad_actual + 1, nuevo_total))
        else:
            # Si el producto no está, agregarlo
            total_prod = producto.precio  # Inicializamos la cantidad en 1
            self.tree.insert("", "end", values=(producto.productoID, producto.nombre, producto.precio, 1, total_prod))

        self.actualizar_total_venta()

    def on_treeview_item_edit(self, event):
        item_id = self.tree.identify_row(event.y)  # Obtener el item que se ha clickeado
        col = self.tree.identify_column(event.x)  # Obtener la columna que se ha clickeado
        if col == '#4':  # Columna de la cantidad
            old_value = self.tree.item(item_id)["values"][3]
            new_value = self.prompt_for_quantity(old_value)
            if new_value:
                producto_id = self.tree.item(item_id)["values"][0]
                producto, error = self.crud_producto.obtener_producto_por_id(producto_id)
                if producto:
                    stock_disponible = producto.stock
                    if new_value <= stock_disponible:
                        new_total = producto.precio * new_value
                        self.tree.item(item_id, values=(producto.productoID, producto.nombre, producto.precio, new_value, new_total))
                        self.actualizar_total_venta()
                    else:
                        self.error_label.configure(text=f"Cantidad excede el stock disponible ({stock_disponible})")
                else:
                    self.error_label.configure(text="Producto no encontrado.")
                
    def prompt_for_quantity(self, current_quantity):
        """Muestra una ventana emergente para editar la cantidad."""
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

        confirm_button = ctk.CTkButton(top, text="Confirmar", command=on_confirm)
        confirm_button.pack(pady=10)

        top.mainloop()
    
    def actualizar_total_venta(self):
        total = 0
        for item in self.tree.get_children():
            total += float(self.tree.item(item)["values"][4])  # Total está en la 5ta columna
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def cargar_datos(self):
        # Aquí puedes cargar todos los productos si es necesario
        pass
