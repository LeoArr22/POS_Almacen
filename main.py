from models.models.modelo_producto import ModeloProducto
from data.crud.crud_producto import CRUD_producto
from data.sql.engine import Session
# from data.crud.crud_producto import *


try:
    producto=ModeloProducto("Cocuchasss", "5", "7", "10", "1234321234565")
    valor=producto.es_completo()
    with Session() as session:
        crud_producto=CRUD_producto(session)
        crud_producto.crear_producto(producto.nombre, producto.precio, producto.stock, producto.costo, producto.codigo_barra, 1)
except ValueError as e:
    print(e)

