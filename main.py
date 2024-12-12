from models.models.modelo_producto import ModeloProducto

try:
    producto=ModeloProducto("Fiambre")
    print(producto.nombre)
    producto.completo
except ValueError as e:
    print(e)

