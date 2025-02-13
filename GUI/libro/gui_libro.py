import customtkinter as ctk
from tkinter import ttk
from data.sql.engine import Session
from data.crud.crud_producto import CRUD_producto
from data.crud.crud_categoria import CRUD_categoria
from gui.util.generic import centrar_ventana, proxima
from models.models.modelo_producto import ModeloProducto
from models.models.modelo_categoria import ModeloCategoria

class LibroApp:
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
        self.frame_principal.rowconfigure(2, weight=1)

        # Frame superior (primera fila)
        self.frame_superior = ctk.CTkFrame(self.frame_principal, fg_color="#2E3B4E")
        self.frame_superior.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        ### FRAME PARA CAMPOS Y BOTONES ####
        self.botones_frame = ctk.CTkFrame(self.frame_principal, fg_color="#1C2124")
        self.botones_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        self.botones_frame.grid_rowconfigure(1, weight=1)
        self.botones_frame.grid_columnconfigure(3, weight=1)
       

        ### BARRA DE NAVEGACIÓN ###
        self.frame_superior.columnconfigure(0, weight=3)  # Más espacio para el título
        self.frame_superior.columnconfigure(1, weight=1)  # Menos espacio para los botones
        self.frame_superior.columnconfigure(2, weight=1)
        self.frame_superior.columnconfigure(3, weight=1)
        self.frame_superior.columnconfigure(4, weight=3)
        self.frame_superior.rowconfigure(0, weight=1)

        self.label_nav = ctk.CTkLabel(
            self.frame_superior,
            text="Menú de Navegación →",
            fg_color="transparent",
            font=("Helvetica", 20, "bold"),
            text_color="#F3920F",
            height=40
        )
        self.label_nav.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Botón "Vender"
        self.vender_button = ctk.CTkButton(
            self.frame_superior,
            text="Vender",
            command=lambda: proxima(self.ventana, "Vender"),
            border_width=2,
            fg_color="#1C2124",
            text_color="#F3920F",
            font=("Helvetica", 16, "bold"),
            hover_color="#2C353A",
            border_color="#F3920F",
            width=100,
            height=40
        )
        self.vender_button.grid(row=0, column=1, padx=10, pady=5)

        # Botón "Usuarios"
        self.usuarios_button = ctk.CTkButton(
            self.frame_superior,
            text="Usuarios",
            command=lambda: proxima(self.ventana, "Usuarios"),
            border_width=2,
            fg_color="#1C2124",
            text_color="#F3920F",
            font=("Helvetica", 16, "bold"),
            hover_color="#2C353A",
            border_color="#F3920F",
            width=100,
            height=40
        )
        self.usuarios_button.grid(row=0, column=2, padx=10, pady=5)

        # Botón "Libro de Ventas"
        self.libro_ventas_button = ctk.CTkButton(
            self.frame_superior,
            text="Libro de Ventas",
            command=lambda: proxima(self.ventana, "libro_ventas"),
            border_width=2,
            fg_color="#1C2124",
            text_color="#F3920F",
            font=("Helvetica", 16, "bold"),
            hover_color="#2C353A",
            border_color="#F3920F",
            width=130,
            height=40
        )
        self.libro_ventas_button.grid(row=0, column=3, padx=10, pady=5)

### TITULO ###
        # Label para el título, ajustado más cerca del listado
        self.label_titulo = ctk.CTkLabel(
            self.frame_superior,
            text="Gestor de Productos y Categorias",
            fg_color="transparent",
            font=("Helvetica", 30, "bold"),  # Tamaño del texto reducido para mayor ajuste
            text_color="#F3920F",
            height=40,
        )
        self.label_titulo.grid(row=0 ,column=4, padx=10, pady=5)


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
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

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
        self.scrollbar.grid(row=1, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

### LABEL PARA MENSAJES DE ERROR ###
        self.error_label = ctk.CTkLabel(self.frame_principal, text="", fg_color="#F3920F", font=("Helvetica", 14, "bold"), text_color="white", width=700, height=30)
        self.error_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")



### BOTONES Y CAMPOS ###
        # Botón Crear Producto
        self.crear_producto_button = ctk.CTkButton(self.botones_frame, text="Crear Producto", border_width=2, fg_color="#1C2124", text_color="white", font=("Helvetica", 12, "bold"), hover_color="#F3920F", border_color="#F3920F")
        self.crear_producto_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        
        self.ventana.mainloop()
