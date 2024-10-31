from DATA.SQL.engine import *
from UTIL.validadores import valida_categoria

class CRUD_categoria():
    def __init__(self, Session):
        self.session = Session

    @valida_categoria  
    def crear_categoria(self, nombre):
        if self.obtener_categoria(nombre) is None:
            nueva_categoria = Categoria(nombre=nombre)
            self.session.add(nueva_categoria)
            self.session.commit()
            return nueva_categoria
        else:
            print("Esa categoría ya está registrada")

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
        return None

    def eliminar_categoria(self, nombre):
        categoria = self.obtener_categoria(nombre)
        if categoria is not None:
            self.session.delete(categoria)
            self.session.commit()
            return True
        return False

with Session() as session:
    crud_categoria=CRUD_categoria(session)
    crud_categoria.crear_categoria("Almacennnn")