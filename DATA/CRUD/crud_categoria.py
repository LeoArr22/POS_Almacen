from data.sql.engine import *
from sqlalchemy import func

class CRUD_categoria():
    def __init__(self, Session):
        self.Session = Session  # Guardamos la clase Session, no una sesión abierta

    def crear_categoria(self, nombre):
        with self.Session() as session:  # Manejo de la sesión dentro del CRUD
            try:
                categoria_nom, _ = self.obtener_categoria_por_nombre(nombre, session)
                if categoria_nom is None:
                    nueva_categoria = Categoria(nombre=nombre)
                    session.add(nueva_categoria)
                    session.commit()
                    return nueva_categoria, None
                else:
                    return None, "Esa categoría ya está registrada"
            except Exception as e:
                session.rollback()
                return None, f"Error al crear la categoría: {str(e)}"

    def obtener_categoria_por_nombre(self, nombre, session=None):
        close_session = False  # Bandera para saber si debemos cerrar la sesión
        if session is None:
            session = self.Session()  # Creamos una nueva sesión si no se pasó una
            close_session = True  # Indicamos que la sesión debe cerrarse después
        
        try:
            categoria = session.query(Categoria).filter(func.lower(Categoria.nombre) == nombre.lower()).one_or_none()
            return categoria, ""
        except NoResultFound:
            return None, "No se encontró ninguna categoría con ese nombre"
        finally:
            if close_session:
                session.close()  # Cerramos la sesión solo si la creamos aquí

    def obtener_categorias(self):
        with self.Session() as session:  # Manejo de la sesión dentro del CRUD
            try:
                categorias = session.query(Categoria).all()  # Obtiene todas las categorías
                return [(categoria.categoriaID, categoria.nombre) for categoria in categorias], None  # Usa categoriaID
            except Exception as e:
                return [], f"Error al obtener las categorías: {str(e)}"

    def actualizar_categoria(self, nombre, nuevo_nombre):
        with self.Session() as session:  # Manejo de la sesión dentro del CRUD
            try:
                categoria, error = self.obtener_categoria_por_nombre(nombre, session)
                if categoria is not None:
                    categoria_existente, _ = self.obtener_categoria_por_nombre(nuevo_nombre, session)
                    if categoria_existente is not None:
                        return None, "Esa categoría ya está registrada"
                    categoria.nombre = nuevo_nombre
                    session.commit()
                    return categoria, None
                return None, "Categoría no encontrada para actualizar"
            except Exception as e:
                session.rollback()
                return None, f"Error al actualizar la categoría: {str(e)}"

    def eliminar_categoria(self, nombre_categoria):
        with self.Session() as session:  # Manejo de la sesión dentro del CRUD
            try:
                categoria = session.query(Categoria).filter(func.lower(Categoria.nombre) == nombre_categoria.lower()).one_or_none()
                if not categoria:
                    return None, "La categoría no existe."

                sin_categoria = session.query(Categoria).filter(func.lower(Categoria.nombre) == "sin categoria").one_or_none()
                if not sin_categoria:
                    sin_categoria = Categoria(nombre="Sin Categoria")
                    session.add(sin_categoria)
                    session.commit()

                productos_asociados = session.query(Producto).filter_by(categoriaID=categoria.categoriaID).all()
                for producto in productos_asociados:
                    producto.categoriaID = sin_categoria.categoriaID
                session.commit()

                session.delete(categoria)
                session.commit()
                return True, None
            except Exception as e:
                session.rollback()
                return None, f"Error al eliminar la categoría: {str(e)}"
