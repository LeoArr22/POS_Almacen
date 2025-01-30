from data.sql.engine import *
from sqlalchemy import func  # Importar funciones SQLAlchemy

class CRUD_producto():
    def __init__(self, Session):
        self.session = Session

    def crear_producto(self, nombre, precio, stock, costo, codigo_barra, categoria_id):
        producto_nom, error = self.obtener_producto_por_nombre(nombre)
        if producto_nom is None:
            producto_cb, error = self.obtener_producto_por_cb(codigo_barra)
            if producto_cb is None:
                nuevo_producto = Producto(nombre=nombre, precio=precio, stock=stock, costo=costo, codigo_barra=codigo_barra, categoriaID=categoria_id)
                self.session.add(nuevo_producto)
                self.session.commit()
                return nuevo_producto, None
            else:
               return None, "Ya existe un producto con ese codigo de barra"
        else:
            return None, "Ya existe un producto con ese nombre"


    def obtener_producto_por_nombre(self, nombre):
        try:
            producto = self.session.query(Producto).filter(func.lower(Producto.nombre) == nombre.lower()).one()
            return producto, ""
        except NoResultFound:
            return None, "No se encontró ningún producto con ese nombre"

    def obtener_producto_por_cb(self, codigo_barra):
        try:
            producto = self.session.query(Producto).filter_by(codigo_barra=codigo_barra).one()
            return producto, ""
        except NoResultFound:
            return None, "No se encontró ningún producto con ese código de barra"

        
    def obtener_todos_productos(self):
        try:
            productos = self.session.query(Producto, Categoria.nombre).join(Categoria, Producto.categoriaID == Categoria.categoriaID).all()

            return productos
        except Exception as e:
            return None    
        
         
        

    def actualizar_producto(self, nombre, nuevo_nombre=None, nuevo_precio=None, nuevo_stock=None, nuevo_costo=None, nuevo_cb=None, nueva_categoria=None):
        producto, error = self.obtener_producto_por_nombre(nombre)
        if producto is not None:
            if nuevo_nombre is not None:
                producto.nombre = nuevo_nombre
            if nuevo_precio is not None:
                producto.precio = nuevo_precio
            if nuevo_stock is not None:
                producto.stock = nuevo_stock
            if nuevo_costo is not None:
                producto.costo = nuevo_costo
            if nuevo_cb is not None:
                producto.codigo_barra = nuevo_cb
            if nueva_categoria is not None:
                producto.categoriaID = nueva_categoria       
            self.session.commit()
            return producto, None
        return None, error

    def eliminar_producto(self, nombre):
        producto = self.obtener_producto_por_nombre(nombre)
        if producto is not None:
            self.session.delete(producto)
            self.session.commit()
            return True
        return False, "Producto no encontrado para eliminar"
