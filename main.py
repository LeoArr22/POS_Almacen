from models.models.modelo_producto import ModeloProducto
# from data.crud.crud_producto import *


try:
    producto=ModeloProducto("Manaos", "2")
    # valor=producto.es_completo()
    print(producto.codigo_barra)
    # with Session() as session:
    #     crud_producto=CRUD_producto(session)
    #     crud_producto.crear_producto(producto.nombre, producto.precio, producto.stock, producto.costo, producto.codigo_barra, 1)
except ValueError as e:
    print(e)

