import customtkinter as ctk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_venta import CRUD_venta
from data.crud.crud_detalle import CRUD_detalle
from gui.util.generic import centrar_ventana
from gui.util.nav import navegacion, boton_productos, boton_ventas, boton_usuarios, titulo, menu_label

class LibroApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title('Listado de Ventas')
        centrar_ventana(self.ventana, 1200, 650)
        self.ventana.resizable(width=0, height=0)

        self.ventana.configure(bg="#1C2124")
        self.frame_principal = ctk.CTkFrame(self.ventana, width=850, height=750, fg_color="#1C2124")
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.rowconfigure(0, weight=0)
        self.frame_principal.rowconfigure(1, weight=1)

        
        navegacion(self)
        menu_label(self)
        boton_productos(self, 1)
        boton_usuarios(self, 2)
        boton_ventas(self, 3)        
        titulo(self, "Libro de Ventas", 4)

        # Treeview para mostrar las ventas
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

        self.tree = ttk.Treeview(self.frame_principal, columns=("ID", "Fecha", "Total Venta", "Ganancia Total", "Vendedor Nombre", "Vendedor ID" ), show="headings", style="Treeview", height=15)

        self.tree.heading("ID", text="ID", command=lambda: self.ordenar_columna("ID"))
        self.tree.heading("Fecha", text="Fecha", command=lambda: self.ordenar_columna("Fecha"))
        self.tree.heading("Total Venta", text="Total Venta", command=lambda: self.ordenar_columna("Total Venta"))
        self.tree.heading("Ganancia Total", text="Ganancia Total", command=lambda: self.ordenar_columna("Ganancia Total"))
        self.tree.heading("Vendedor Nombre", text="Vendedor Nombre", command=lambda: self.ordenar_columna("Vendedor Nombre"))
        self.tree.heading("Vendedor ID", text="Vendedor ID", command=lambda: self.ordenar_columna("Vendedor ID"))

        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.tree.column("ID", anchor="center", width=10)
        self.tree.column("Fecha", width=100, minwidth=100)
        self.tree.column("Total Venta", width=100)
        self.tree.column("Ganancia Total", width=100)
        self.tree.column("Vendedor Nombre", width=100)
        self.tree.column("Vendedor ID", width=100)

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.frame_principal, orientation="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=3, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Label para mensajes de error
        self.error_label = ctk.CTkLabel(self.frame_principal, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Frame para campos y botones
        self.botones_frame = ctk.CTkFrame(self.frame_principal, height=50, fg_color="#1C2124")
        self.botones_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.botones_frame.grid_rowconfigure(5, weight=1)
        self.botones_frame.grid_columnconfigure(7, weight=1)

        # CRUD
        self.crud_venta = CRUD_venta(Session)
        self.crud_detalle = CRUD_detalle(Session)
        self.cargar_datos()

        # Botones y campos
        # Campo y botón para buscar por fecha
        self.buscar_fecha_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Fecha (YYYY-MM-DD)", width=200)
        self.buscar_fecha_entry.grid(row=2, column=1, padx=10, sticky="ew")

        self.buscar_fecha_button = ctk.CTkButton(
            self.botones_frame, text="Buscar por Fecha", command=self.buscar_por_fecha,
            border_width=2, fg_color="#1C2124", text_color="white",
            font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F"
        )
        self.buscar_fecha_button.grid(row=3, column=1, padx=10, sticky="ew")
        
        # Campo y botón para buscar por fecha POR RANGO
        self.fecha_inicio_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Fecha (YYYY-MM-DD)", width=200)
        self.fecha_inicio_entry.grid(row=1, column=2, padx=10, sticky="ew")
        self.fecha_fin_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Fecha (YYYY-MM-DD)", width=200)
        self.fecha_fin_entry.grid(row=2, column=2, padx=10, sticky="ew")

        self.fecha_por_rango_button = ctk.CTkButton(
            self.botones_frame, text="Buscar por Rango de Fechas", command=self.buscar_por_rango_fechas,
            border_width=2, fg_color="#1C2124", text_color="white",
            font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F"
        )
        self.fecha_por_rango_button.grid(row=3, column=2, padx=10, sticky="ew")

        # Botón Ver Todas las Ventas
        self.ver_todas_button = ctk.CTkButton(self.botones_frame, text="Ver Todas Las Ventas", command=self.cargar_datos, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.ver_todas_button.grid(row=1, column=3, padx=10, sticky="ew")
        
        # Botón Ver Detalle
        self.ver_detalle_button = ctk.CTkButton(self.botones_frame, text="Ver Detalle", command=self.ver_detalle, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.ver_detalle_button.grid(row=3, column=3, padx=10, sticky="ew")
        
        self.total_vendido_label = ctk.CTkLabel(self.botones_frame, text="Venta Total: $0.00", fg_color="#1C2124", font=("Helvetica", 25, "bold"), text_color="#F3920F")
        self.total_vendido_label.grid(row=1, column=4, padx=10, sticky="ew")
        
        self.total_ganancias_label = ctk.CTkLabel(self.botones_frame, text="Ganancia Total: $0.00", fg_color="#1C2124", font=("Helvetica", 25, "bold"), text_color="#F3920F")
        self.total_ganancias_label.grid(row=3, column=4, padx=10, sticky="ew")


        self.ventana.mainloop()

    def cargar_datos(self):
        ventas = self.crud_venta.obtener_todas_las_ventas()
        
        # Limpiar el Treeview antes de cargar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        self.datos = []
        
        # Si no hay ventas, mostrar mensaje en la primera fila
        if not ventas:
            self.tree.insert("", "end", values=("NO", "HAY VENTAS", "CARGADAS", "", "", ""), tags=("empty",))
            return self.datos
        
        for index, venta in enumerate(ventas):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            
            self.tree.insert(
                "", "end",
                values=(
                    venta.ventaID, venta.fecha, venta.total_venta,
                    venta.ganancia_total, venta.nombre_vendedor, venta.vendedorID
                ),
                tags=(tag,)
            )
            
            # Guardar datos para ordenamiento
            self.datos.append((venta.ventaID, venta.fecha, venta.total_venta, venta.ganancia_total, venta.nombre_vendedor, venta.vendedorID))
        
        return self.datos

    def ordenar_columna(self, columna):
        col_index = ["ID", "Fecha", "Total Venta", "Ganancia Total", "Vendedor Nombre""Vendedor ID"].index(columna)
        orden_inverso = getattr(self, "orden_inverso", False)
        
        self.datos.sort(key=lambda x: x[col_index], reverse=orden_inverso)
        
        self.orden_inverso = not orden_inverso
        
        # Limpiar y volver a cargar los datos ordenados
        for row in self.tree.get_children():
            self.tree.delete(row)
        for index, dato in enumerate(self.datos):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=dato, tags=(tag,))

    def buscar_por_fecha(self):
        fecha = self.buscar_fecha_entry.get().strip()
        
        if not fecha:
            self.error_label.configure(text="Ingrese una fecha para buscar", text_color="#FF0000")
            return

        ventas = self.crud_venta.obtener_ventas_por_fecha(fecha)
        
        if not ventas:
            self.error_label.configure(text="No se encontraron ventas para la fecha especificada", text_color="#FF0000")
            return
        
        # Limpiar Treeview y mostrar solo las ventas encontradas
        self.tree.delete(*self.tree.get_children())
        for venta in ventas:
            self.tree.insert("", "end", values=(venta.ventaID, venta.fecha, venta.total_venta, venta.ganancia_total, venta.nombre_vendedor, venta.vendedorID))

    def buscar_por_rango_fechas(self):
        fecha_inicio = self.fecha_inicio_entry.get().strip()
        fecha_fin = self.fecha_fin_entry.get().strip()

        if not fecha_inicio or not fecha_fin:
            self.error_label.configure(text="Ingrese ambas fechas para buscar", text_color="#FF0000")
            return

        ventas = self.crud_venta.obtener_ventas_por_rango_fechas(fecha_inicio, fecha_fin)

        if not ventas:
            self.error_label.configure(text="No se encontraron ventas en el rango especificado", text_color="#FF0000")
            return

        # Limpiar Treeview y mostrar solo las ventas encontradas
        self.tree.delete(*self.tree.get_children())
        for venta in ventas:
            self.tree.insert("", "end", values=(venta.ventaID, venta.fecha, venta.total_venta, venta.ganancia_total, venta.nombre_vendedor, venta.vendedorID))


    def ver_detalle(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.error_label.configure(text="Por favor, selecciona una venta.", text_color="#FF0000")
            return
        venta_id = self.tree.item(selected_item)["values"][0]
        
        # Crear ventana emergente para mostrar el detalle de la venta
        self.popup_detalle = ctk.CTkToplevel(self.ventana)
        self.popup_detalle.title("Detalle de Venta")
        self.popup_detalle.transient(self.ventana)
        self.popup_detalle.grab_set()
        centrar_ventana(self.popup_detalle, 600, 400)

        self.popup_detalle.configure(bg="#1C2124", fg_color="#1C2124")
        self.popup_detalle.grid_columnconfigure(0, weight=1)
        self.popup_detalle.grid_columnconfigure(1, weight=1)

        # Obtener detalles de la venta
        detalles = self.crud_detalle.obtener_detalles_por_venta(venta_id)
        
        # Mostrar detalles en un Treeview
        self.tree_popup = ttk.Treeview(self.popup_detalle, columns=("Producto", "Cantidad", "Total"), show="headings")
        self.tree_popup.heading("Producto", text="Producto")
        self.tree_popup.heading("Cantidad", text="Cantidad")
        self.tree_popup.heading("Total", text="Total")
        self.tree_popup.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Scrollbar
        self.scrollbar_popup = ctk.CTkScrollbar(self.popup_detalle, orientation="vertical", command=self.tree_popup.yview)
        self.scrollbar_popup.grid(row=1, column=3, sticky="ns")
        self.tree_popup.configure(yscrollcommand=self.scrollbar_popup.set)

        # Cargar detalles en el Treeview
        for detalle in detalles:
            self.tree_popup.insert("", "end", values=(detalle.producto_nombre, detalle.cantidad, detalle.total_prod))

        # Botón para cerrar la ventana de detalle
        self.cerrar_button = ctk.CTkButton(self.popup_detalle, text="Cerrar", command=self.popup_detalle.destroy, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.cerrar_button.grid(row=2, column=0, columnspan=3, pady=10)

