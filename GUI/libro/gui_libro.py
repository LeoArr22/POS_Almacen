import os

import customtkinter as ctk
from tkinter import ttk

from gui.util.generic import centrar_ventana
from gui.util.nav import navegacion, boton_productos, boton_ventas, boton_usuarios, titulo, menu_label

from data.sql.engine import Session
from data.crud.crud_venta import CRUD_venta
from data.crud.crud_detalle import CRUD_detalle

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle


class LibroApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title('Listado de Ventas')
        centrar_ventana(self.ventana, 1200, 650)
        self.ventana.resizable(width=0, height=0)

        self.ventana.configure(bg="#1C2124")
        self.frame_principal = ctk.CTkFrame(self.ventana, width=850, height=750, fg_color="#1C2124")
        self.frame_principal.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.page_size = 15
        self.current_page = 0
        
        
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.rowconfigure(0, weight=0) #Nav Bar
        self.frame_principal.rowconfigure(1, weight=2) #Botones superiores
        self.frame_principal.rowconfigure(2, weight=1) #Error label
        self.frame_principal.rowconfigure(3, weight=3) #Treeview
        self.frame_principal.rowconfigure(4, weight=1) #Botones inferiores


        
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
                        rowheight=20,
                        borderwidth=2,
                        font=("Roboto", 14),
                        relief="solid")
        style.configure("Treeview.Heading", background="#1C2124", foreground="#F3920F", font=('Helvetica', 13, 'bold'))
        style.map("Treeview", background=[('selected', '#F3920F')])

        self.tree = ttk.Treeview(self.frame_principal, columns=("ID", "Fecha", "Total Venta", "Ganancia Total", "Vendedor Nombre", "Vendedor ID" ), show="headings", style="Treeview", height=15)

        self.tree.tag_configure('evenrow', background='#2C353A')
        self.tree.tag_configure('oddrow', background='#1C2124')

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

        # Label para mensajes de error
        self.error_label = ctk.CTkLabel(self.frame_principal, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Frame para campos y botones superiores
        self.botones_frame = ctk.CTkFrame(self.frame_principal, height=50, fg_color="#1C2124")
        self.botones_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.botones_frame.grid_rowconfigure(5, weight=1)
        self.botones_frame.grid_columnconfigure(7, weight=1)
        
        # Frame para campos y botones inferiores
        self.botones_frame_inferior = ctk.CTkFrame(self.frame_principal, height=50, fg_color="#1C2124")
        self.botones_frame_inferior.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.botones_frame_inferior.grid_rowconfigure(2, weight=1)
        self.botones_frame_inferior.grid_columnconfigure(0, weight=3)
        self.botones_frame_inferior.grid_columnconfigure(1, weight=1)
        self.botones_frame_inferior.grid_columnconfigure(2, weight=2)
        self.botones_frame_inferior.grid_columnconfigure(3, weight=1)
        self.botones_frame_inferior.grid_columnconfigure(4, weight=1)
        
        # CRUD
        self.crud_venta = CRUD_venta(Session)
        self.crud_detalle = CRUD_detalle(Session)


        #BOTONES FRAME SUPERIOR
        # Botones y campos
        
        # Campo y botón para buscar por fecha POR RANGO
        self.fecha_inicio_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Fecha (YYYY-MM-DD)", width=200)
        self.fecha_inicio_entry.grid(row=1, column=0, padx=10, sticky="ew")
        self.fecha_fin_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Fecha (YYYY-MM-DD)", width=200)
        self.fecha_fin_entry.grid(row=2, column=0, padx=10, sticky="ew")

        self.fecha_por_rango_button = ctk.CTkButton(
            self.botones_frame, text="Buscar por Rango de Fechas", command=self.buscar_por_rango_fechas,
            border_width=2, fg_color="#1C2124", text_color="white",
            font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F"
        )
        self.fecha_por_rango_button.grid(row=3, column=0, padx=10, sticky="ew")
        
        # Campo y boton para buscar por vendedor
        self.buscar_vendedor_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Nombre Vendedor", width=200)
        self.buscar_vendedor_entry.grid(row=2, column=2, padx=10, sticky="ew")
        
        self.buscar_vendedor_button = ctk.CTkButton(
            self.botones_frame, text="Buscar por Vendedor", command=self.buscar_por_nombre_vendedor,
            border_width=2, fg_color="#1C2124", text_color="white",
            font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F"
        )
        self.buscar_vendedor_button.grid(row=3, column=2, padx=10, sticky="ew")
        
        # boton para buscar por vendedor y fechas
        self.buscar_vendedor_button = ctk.CTkButton(
            self.botones_frame, text="Buscar por Vendedor y Fecha", command=self.buscar_por_rango_fechas_y_nombre_vendedor,
            border_width=2, fg_color="#1C2124", text_color="white",
            font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F"
        )
        self.buscar_vendedor_button.grid(row=3, column=3, padx=10, sticky="ew")

        # Botón Ver borrar lista
        self.borrar_lista_button = ctk.CTkButton(self.botones_frame, text="Borrar Listado", command=self.cargar_datos, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.borrar_lista_button.grid(row=3, column=4, padx=10, sticky="ew")
        
        # Botón Ver Detalle
        self.ver_detalle_button = ctk.CTkButton(self.botones_frame, text="Ver Detalle", command=self.ver_detalle, border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.ver_detalle_button.grid(row=3, column=5, padx=10, sticky="ew")
        
        # Botón y campo Generar Reporte
        self.exportar_entry = ctk.CTkEntry(self.botones_frame, placeholder_text="Nombrar Archivo", width=200)
        self.exportar_entry.grid(row=2, column=6, padx=10, sticky="ew")
        
        self.exportar_button = ctk.CTkButton(self.botones_frame, text="Generar Reporte", 
                                            command=lambda: self.exportar_ventas_pandas_pdf(self.datos),
                                            border_width=2, 
                                            fg_color="#1C2124", 
                                            text_color="white", 
                                            font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.exportar_button.grid(row=3, column=6, padx=10, sticky="ew")
        
        
        #BOTONES FRAME INFERIOR
        #Totales
        self.total_vendido_label = ctk.CTkLabel(self.botones_frame_inferior, text="Venta Total: $0", fg_color="#1C2124", font=("Helvetica", 25, "bold"), text_color="#F3920F")
        self.total_vendido_label.grid(row=0, column=0, padx=10, sticky="w")

        self.total_ganancias_label = ctk.CTkLabel(self.botones_frame_inferior, text="Ganancia Total: $0", fg_color="#1C2124", font=("Helvetica", 25, "bold"), text_color="#F3920F")
        self.total_ganancias_label.grid(row=1, column=0, padx=10, sticky="w")

       # Columna vacía para separación
        self.empty_label = ctk.CTkLabel(self.botones_frame_inferior, text="", fg_color="#1C2124")
        self.empty_label.grid(row=0, column=1, rowspan=2, sticky="w")
        # Botones de navegación
        self.prev_button = ctk.CTkButton(self.botones_frame_inferior, text="🢀", 
                                        command=self.prev_page, 
                                        border_width=2, 
                                        fg_color="#1C2124", 
                                        text_color="white", 
                                        font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.prev_button.grid(row=0, column=4, padx=(0, 1), sticky="e")

        self.next_button = ctk.CTkButton(self.botones_frame_inferior, text="🢂", 
                                        command=self.next_page, 
                                        border_width=2, 
                                        fg_color="#1C2124",
                                        text_color="white",
                                        font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.next_button.grid(row=0, column=5, padx=(0, 10), sticky="e")


        self.cargar_datos()
        self.ventana.mainloop()

    def cargar_datos(self, ventas=None):    
        total_vendido = 0
        total_ganancia = 0    
        # Limpiar el Treeview antes de cargar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        self.datos = []
        
        # Si no hay ventas, mostrar mensaje en la primera fila
        if not ventas:
            self.tree.insert("", "end", values=("POR FAVOR", "      APLIQUE UN", "      FILTRO", "      PARA VER", "        LAS VENTAS", ""), tags=("empty",))
            self.actualizar_totales(total_vendido, total_ganancia)
            return self.datos
        
        for index, venta in enumerate(ventas):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            
            self.datos.append((venta.ventaID, venta.fecha, venta.total_venta, venta.ganancia_total, venta.nombre_vendedor, venta.vendedorID))
            total_vendido += venta.total_venta
            total_ganancia += venta.ganancia_total
        
        self.update_treeview()
        self.actualizar_totales(total_vendido, total_ganancia)
        self.error_label.configure(text="", text_color="#FF0000")
        return self.datos

    def update_treeview(self):
        # Limpiar el Treeview antes de cargar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size
        page_data = self.datos[start_index:end_index]
        
        for index, dato in enumerate(page_data):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=dato, tags=(tag,))

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.datos):
            self.current_page += 1
            self.update_treeview()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_treeview()

    def actualizar_totales(self, total_vendido, total_ganancia):
        self.total_vendido_label.configure(text=f"Venta Total: ${total_vendido}")
        self.total_ganancias_label.configure(text=f"Ganancia Total: ${total_ganancia}")

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

        self.update_treeview()


    def buscar_por_rango_fechas(self):
        fecha_inicio = self.fecha_inicio_entry.get().strip()
        fecha_fin = self.fecha_fin_entry.get().strip() or None
        
        if not fecha_inicio:
            self.error_label.configure(text="Debe ingresar al menos, la fecha de inicio", text_color="#FF0000")
            return

        if fecha_fin is None:
            fecha_fin = fecha_inicio

        ventas = self.crud_venta.obtener_ventas_por_rango_fechas(fecha_inicio, fecha_fin)

        if not ventas:
            self.error_label.configure(text="No se encontraron ventas en el rango especificado", text_color="#FF0000")
            return

        self.cargar_datos(ventas)

    def buscar_por_nombre_vendedor(self):
        vendedor_nombre = self.buscar_vendedor_entry.get().strip()
        
        if not vendedor_nombre:
            self.error_label.configure(text="Ingrese un nombre de vendedor para buscar", text_color="#FF0000")
            return
        
        ventas = self.crud_venta.obtener_ventas_por_nombre_vendedor(vendedor_nombre)
        
        if not ventas:
            self.error_label.configure(text="No se encontraron ventas para el vendedor especificado", text_color="#FF0000")
            return
        
        self.cargar_datos(ventas)
        
    def buscar_por_rango_fechas_y_nombre_vendedor(self):
        fecha_inicio = self.fecha_inicio_entry.get().strip()
        fecha_fin = self.fecha_fin_entry.get().strip() or None
        vendedor_nombre = self.buscar_vendedor_entry.get().strip()
            
        if not fecha_inicio or not vendedor_nombre:
            self.error_label.configure(text="Debe ingresar al menos, la fecha de inicio y el nombre del vendedor", text_color="#FF0000")
            return
         
        if fecha_fin is None:
            fecha_fin = fecha_inicio
        
        ventas = self.crud_venta.obtener_ventas_por_rango_fechas_y_nombre_vendedor(vendedor_nombre, fecha_inicio, fecha_fin)
        
        if not ventas:
            self.error_label.configure(text="No se encontraron ventas para el vendedor en el rango especificado", text_color="#FF0000")
            return
            
        self.cargar_datos(ventas)    
        
        
        
    #DETALLES    

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
        self.popup_detalle.resizable(width=0, height=0)
        self.popup_detalle.grab_set()
        centrar_ventana(self.popup_detalle, 650, 400)

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



    #REPORTES

    def obtener_ruta_escritorio(self):
        """Obtiene la ruta del escritorio del usuario."""
        return os.path.join(os.path.expanduser("~"), "Desktop")

    def obtener_nombre_disponible(self, nombre_base):
        """Genera un nombre de archivo único en la carpeta 'Reportes' del escritorio."""
        escritorio = self.obtener_ruta_escritorio()
        directorio = os.path.join(escritorio, "Reportes")

        # Crear la carpeta si no existe
        if not os.path.exists(directorio):
            os.makedirs(directorio)

        contador = 1
        nombre_archivo = os.path.join(directorio, f"{nombre_base}.pdf")

        while os.path.exists(nombre_archivo):
            nombre_archivo = os.path.join(directorio, f"{nombre_base}_{contador}.pdf")
            contador += 1

        return nombre_archivo

    def exportar_ventas_pandas_pdf(self, ventas):
        """Exporta las ventas a un archivo PDF en formato de tabla."""
        if not ventas:
            self.error_label.configure(text="No hay ventas para exportar", text_color="#FF0000")
            return

        nombre_base = self.exportar_entry.get().strip() or "Reporte"

        # Convertir ventas a DataFrame de pandas
        df = pd.DataFrame([{
            "ID": venta[0],
            "Fecha": venta[1],
            "Total Venta": venta[2],
            "Ganancia de la Venta": venta[3],
            "Vendedor": venta[4]
        } for venta in ventas])

        # Obtener un nombre de archivo único
        nombre_archivo = self.obtener_nombre_disponible(nombre_base)

        # Crear documento PDF
        doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
        elementos = []

        # **Crear la tabla**
        data = [df.columns.tolist()] + df.values.tolist()  # Encabezado + datos
        tabla = Table(data)

        # **Estilo de la tabla**
        estilo = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.orange),  # Fondo de encabezado
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),   # Texto blanco en encabezado
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Centrar texto
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Bordes negros
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Fuente en encabezado
            ("FONTSIZE", (0, 0), (-1, -1), 12),  # Tamaño de letra más grande
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Fondo de celdas
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),  # Espaciado en encabezado
            ("TOPPADDING", (0, 0), (-1, -1), 5),  # Espaciado entre filas
        ])
        tabla.setStyle(estilo)

        elementos.append(tabla)
        # **Obtener los valores de facturación y ganancia desde los labels**
        total_vendido = self.total_vendido_label.cget("text").replace("Venta Total: $", "").strip()
        total_ganancia = self.total_ganancias_label.cget("text").replace("Ganancia Total: $", "").strip()

        # **Agregar un espacio antes de los totales**
        elementos.append(Spacer(1, 12))

        # **Crear el resumen de totales**
        estilo_texto = ParagraphStyle(name="Normal", fontSize=14, textColor=colors.black)

        texto_facturacion = Paragraph(f"<b>Venta Total:</b> ${total_vendido}", estilo_texto)
        texto_ganancia = Paragraph(f"<b>Ganancia Total:</b> ${total_ganancia}", estilo_texto)

        elementos.append(texto_facturacion)
        elementos.append(texto_ganancia)        

        doc.build(elementos)

        self.error_label.configure(text=f"Reporte generado en: {nombre_archivo}", text_color="#00FF00")