from data.sql.engine import *
from util.validadores import valida_producto

class CRUD_producto():
    def __init__(self, Session):
        self.session = Session

    @valida_producto
    def crear_producto(self, nombre, precio, stock, costo, codigo_barra, categoria_id):
        if self.obtener_producto(nombre) is None:
            nuevo_producto = Producto(nombre=nombre, precio=precio, stock=stock, costo=costo, codigo_barra=codigo_barra, categoriaID=categoria_id)
            self.session.add(nuevo_producto)
            self.session.commit()
            return nuevo_producto
        else:
            print("Ese producto ya está registrado")

    def obtener_producto(self, nombre):
        try:
            producto = self.session.query(Producto).filter_by(nombre=nombre).one()
            return producto
        except NoResultFound:
            return None

    def actualizar_producto(self, nombre, nuevo_precio=None, nuevo_stock=None, nuevo_costo=None):
        producto = self.obtener_producto(nombre)
        if producto is not None:
            if nuevo_precio is not None:
                producto.precio = nuevo_precio
            if nuevo_stock is not None:
                producto.stock = nuevo_stock
            if nuevo_costo is not None:
                producto.costo = nuevo_costo
            self.session.commit()
            return producto
        return None

    def eliminar_producto(self, nombre):
        producto = self.obtener_producto(nombre)
        if producto is not None:
            self.session.delete(producto)
            self.session.commit()
            return True
        return False

with Session() as session:
    crud_producto=CRUD_producto(session)
    nuevo=crud_producto.crear_producto("Coca-Cola", 3000, 10, 2000, 123456712876, 1)
    