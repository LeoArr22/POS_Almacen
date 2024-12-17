from models.models.modelo_producto import ModeloProducto
from data.crud.crud_producto import CRUD_producto
from data.sql.engine import Session
# from data.crud.crud_producto import *


try:
    # producto=ModeloProducto("Cocuchasss", "s", "7", "10", "1234321234565")
    # valor=producto.es_completo()
    with Session() as session:
        crud_producto=CRUD_producto(session)
        crud_producto.actualizar_producto("Cocuchasss", nuevo_precio=200)
except ValueError as e:
    print(e)

