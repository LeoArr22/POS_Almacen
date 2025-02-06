from data.sql.engine import *
from sqlalchemy import func  # Importar funciones SQLAlchemy

class CRUD_producto():
    def __init__(self, Session):
        self.Session = Session  # Almacenamos la clase Session, no la sesión abierta

    def crear_producto(self, nombre, precio, stock, costo, codigo_barra, categoria_id):
        with self.Session() as session:  # Usamos el bloque 'with' para manejar la sesión
            producto_nom, error = self.obtener_producto_por_nombre(nombre, session)
            if producto_nom is None:
                producto_cb, error = self.obtener_producto_por_cb(codigo_barra, session)
                if producto_cb is None:
                    nuevo_producto = Producto(
                        nombre=nombre, precio=precio, stock=stock, costo=costo, ganancia_acumulada=0,
                        codigo_barra=codigo_barra, categoriaID=categoria_id
                    )
                    session.add(nuevo_producto)
                    session.commit()
                    return nuevo_producto, None
                else:
                    return None, "Ya existe un producto con ese código de barra"
            else:
                return None, "Ya existe un producto con ese nombre"
            
    def obtener_producto_por_id(self, id, session=None):
        close_session = False
        if session is None:
            session = self.Session()
            close_session = True
        try:
            producto = session.query(Producto).filter(Producto.productoID==id).one()
            return producto, ""
        except NoResultFound:
            return None, "No se encontro ningun producto con ese ID"
        finally:
            if close_session:
                session.close()

    def obtener_producto_por_nombre(self, nombre, session=None):
        close_session = False
        if session is None:
            session = self.Session()
            close_session = True
        try:
            producto = session.query(Producto).filter(func.lower(Producto.nombre) == nombre.lower()).one()
            return producto, ""
        except NoResultFound:
            return None, "No se encontró ningún producto con ese nombre"
        finally:
            if close_session:
                session.close()
                
    def obtener_productos_por_nombre(self, nombre, session=None):
        close_session = False
        if session is None:
            session = self.Session()
            close_session = True
        try:
            productos = session.query(Producto).filter(Producto.nombre.ilike(f"%{nombre}%")).all()
            
            if not productos:
                return None, "No se encontró ningún producto con ese nombre"
            
            return productos, ""
        finally:
            if close_session:
                session.close()            

    def obtener_producto_por_cb(self, codigo_barra, session=None):
        close_session = False
        if session is None:
            session = self.Session()
            close_session = True    
        try:
            producto = session.query(Producto).filter_by(codigo_barra=codigo_barra).one()
            return producto, ""
        except NoResultFound:
            return None, "No se encontró ningún producto con ese código de barra"
        finally:
            if close_session:
                session.close()
                
                
    def obtener_todos_productos(self):
        with self.Session() as session:
            productos = (
                session.query(
                    Producto.productoID,
                    Producto.nombre,
                    Producto.precio,
                    Producto.stock,
                    Producto.costo,
                    Producto.codigo_barra,
                    Producto.ganancia_acumulada,
                    (Producto.precio - Producto.costo).label("ganancia_unidad"),
                    Categoria.nombre.label("categoria_nombre")
                )
                .join(Categoria, Producto.categoriaID == Categoria.categoriaID)
                .all()
            )
            return productos


    def actualizar_producto(self, nombre, nuevo_nombre=None, nuevo_precio=None, nuevo_stock=None, nuevo_costo=None, nuevo_cb=None, nueva_categoria=None):
        with self.Session() as session:
            producto, error = self.obtener_producto_por_nombre(nombre, session)
            existe, error = self.obtener_producto_por_nombre(nuevo_nombre, session)
            if producto is not None:
                if existe is None or nuevo_nombre==producto.nombre:
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
                    session.commit()
                    return producto, None
                return None, "Ya existe un producto con ese nombre"
            return None, "No se pudo encontrar el producto"

    def eliminar_producto(self, nombre):
        with self.Session() as session:
            producto, error = self.obtener_producto_por_nombre(nombre, session)
            if producto is not None:
                session.delete(producto)
                session.commit()
                return True, None
            return False, error
