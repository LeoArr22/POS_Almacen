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
            return [(categoria.categoriaID, categoria.nombre) for categoria in categorias]  # Usa categoriaID
        except Exception as e:
            return [], f"Error al obtener las categorías: {str(e)}"


    def obtener_categoria(self, nombre):
        try:
            categoria = self.session.query(Categoria).filter_by(nombre=nombre).first()
            return categoria
        except NoResultFound:
            return None

    def actualizar_categoria(self, nombre, nuevo_nombre):
        categoria = self.obtener_categoria(nombre)
        if categoria is not None:
            categoria.nombre = nuevo_nombre
            self.session.commit()
            return categoria
        return None, "Categoría no encontrada para actualizar"

    def eliminar_categoria(self, nombre):
        categoria = self.obtener_categoria(nombre)
        if categoria is not None:
            self.session.delete(categoria)
            self.session.commit()
            return True
        return False, "Categoría no encontrada para eliminar"

# with Session() as session:
#     crud_categoria = CRUD_categoria(session)
#     crud_categoria.crear_categoria("Puchos")
