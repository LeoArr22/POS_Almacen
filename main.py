# from gui.master.master import MasterPanel

# # main.py
# from auth import verificar_o_crear_vendedor  # Importas la función desde auth.py

# if __name__ == "__main__":
#     verificar_o_crear_vendedor()  # Llamas a la función para verificar o crear un vendedor

from gui.login.login import LoginApp
from gui.productos.gui_productos import ProductosApp

# from models.models.modelo_producto import ModeloProducto
# from data.crud.crud_producto import CRUD_producto
# from data.sql.engine import Session
# # from data.crud.crud_producto import *


# try:
#     # producto=ModeloProducto("Cocuchasss", "s", "7", "10", "1234321234565")
#     # valor=producto.es_completo()
#     with Session() as session:
#         crud_producto=CRUD_producto(session)
#         crud_producto.actualizar_producto("Cocuchasss", nuevo_precio=200)
# except ValueError as e:
#     print(e)

if __name__ == "__main__":
    ProductosApp()
    # LoginApp

