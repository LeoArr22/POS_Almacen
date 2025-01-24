from data.sql.engine import *

class CRUD_categoria():
    def __init__(self, Session):
        self.session = Session

    def crear_categoria(self, nombre):
        if self.obtener_categoria(nombre) is None:
            nueva_categoria = Categoria(nombre=nombre)
            self.session.add(nueva_categoria)
            self.session.commit()
            return nueva_categoria, None
        else:
            return None, "Esa categoría ya está registrada"

    def obtener_categorias(self):
        """Obtiene todas las categorías disponibles desde el CRUD."""
        try:
            categorias = self.session.query(Categoria).all()  # Obtiene todas las categorías
            return [(categoria.categoriaID, categoria.nombre) for categoria in categorias], None  # Usa categoriaID
        except Exception as e:
            return [], f"Error al obtener las categorías: {str(e)}"


    def obtener_categoria(self, nombre):
        try:
            categoria = self.session.query(Categoria).filter_by(nombre=nombre).first()
            return categoria
        except NoResultFound:
            return None

    def actualizar_categoria(self, nombre, nuevo_nombre):
        categoria = self.obtener_categoria(nuevo_nombre)
        if categoria is not None:
            return None, "Esa categoría ya está registrada"

        categoria = self.obtener_categoria(nombre)
        if categoria is not None:
            categoria.nombre = nuevo_nombre
            self.session.commit()
            return categoria, None
        return None, "Categoría no encontrada para actualizar"

    def eliminar_categoria(self, nombre_categoria):
        """Elimina una categoría y reasigna productos asociados a 'Sin Categoría'."""
        try:
            # Verificar si existe la categoría a eliminar
            categoria = self.obtener_categoria(nombre_categoria)
            if not categoria:
                return None, "La categoría no existe."

            # Verificar si existe la categoría 'Sin Categoría'
            sin_categoria = self.obtener_categoria("Sin Categoria")
            if not sin_categoria:
                # Crear la categoría 'Sin Categoría' si no existe
                sin_categoria = Categoria(nombre="Sin Categoria")
                self.session.add(sin_categoria)
                self.session.commit()

            # Actualizar los productos asociados para usar 'Sin Categoría'
            productos_asociados = self.session.query(Producto).filter_by(categoriaID=categoria.categoriaID).all()
            for producto in productos_asociados:
                producto.categoriaID = sin_categoria.categoriaID
            self.session.commit()

            # Eliminar la categoría
            self.session.delete(categoria)
            self.session.commit()
            return True, None
        except Exception as e:
            self.session.rollback()
            return None, f"Error al eliminar la categoría: {str(e)}"


# with Session() as session:
#     crud_categoria = CRUD_categoria(session)
#     crud_categoria.crear_categoria("Puchos")
