from data.sql.engine import *

class CRUD_producto():
    def __init__(self, Session):
        self.session = Session

    def crear_producto(self, nombre, precio, stock, costo, codigo_barra, categoria_id):
        if self.obtener_producto(nombre) is None:
            nuevo_producto = Producto(nombre=nombre, precio=precio, stock=stock, costo=costo, codigo_barra=codigo_barra, categoriaID=categoria_id)
            self.session.add(nuevo_producto)
            self.session.commit()
            return nuevo_producto, None
        else:
            return None, "Ese producto ya está registrado"

    def obtener_producto(self, nombre):
        try:
            producto = self.session.query(Producto).filter_by(nombre=nombre).one()
            return producto
        except NoResultFound:
            return None
        
    def obtener_todos_productos(self):
        try:
            productos = self.session.query(Producto, Categoria.nombre).join(Categoria, Producto.categoriaID == Categoria.categoriaID).all()

            return productos
        except Exception as e:
            return None    
        
         
        

    def actualizar_producto(self, nombre, nuevo_nombre=None, nuevo_precio=None, nuevo_stock=None, nuevo_costo=None):
        producto = self.obtener_producto(nombre)
        if producto is not None:
            if nuevo_nombre is not None:
                producto.nombre = nuevo_nombre
            if nuevo_precio is not None:
                producto.precio = nuevo_precio
            if nuevo_stock is not None:
                producto.stock = nuevo_stock
            if nuevo_costo is not None:
                producto.costo = nuevo_costo
            self.session.commit()
            return producto
        return None, "Producto no encontrado para actualizar"

    def eliminar_producto(self, nombre):
        producto = self.obtener_producto(nombre)
        if producto is not None:
            self.session.delete(producto)
            self.session.commit()
            return True
        return False, "Producto no encontrado para eliminar"
