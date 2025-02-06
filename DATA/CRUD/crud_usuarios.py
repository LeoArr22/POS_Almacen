from data.sql.engine import *
from sqlalchemy.exc import NoResultFound

class CRUD_usuario():
    def __init__(self, Session):
        self.Session = Session

    def crear_usuario(self, usuario, contrasena):
        with self.Session() as session:
            if self.obtener_usuario(usuario, session) is None:
                nuevo_usuario = Vendedor(usuario=usuario, contrasena=contrasena)
                session.add(nuevo_usuario)
                session.commit()
                return nuevo_usuario, None
            return None, "Ese nombre de usuario ya está en uso"

    def modificar_usuario(self, usuario, usuario_nuevo, contrasena_nueva):
        with self.Session() as session:
            usuario_obj = self.obtener_usuario(usuario, session)
            
            if usuario_obj is None:
                return None, "Usuario no encontrado"

            if usuario_obj.usuario == 'admin' and usuario_nuevo != usuario_obj.usuario:
                return None, "El usuario 'admin' no puede cambiar su nombre."

            if usuario_nuevo:
                usuario_obj.usuario = usuario_nuevo
            if contrasena_nueva:
                usuario_obj.contrasena = contrasena_nueva

            session.commit()
            return usuario_obj, None 

    def obtener_usuario(self, usuario, session=None):
        close_session = False
        if session is None:
            session = self.Session()
            close_session = True
        try:
            usuario_obj = session.query(Vendedor).filter_by(usuario=usuario).one()
            return usuario_obj
        except NoResultFound:
            return None
        finally:
            if close_session:
                session.close()

    def obtener_todos_usuarios(self):
        with self.Session() as session:
            return session.query(Vendedor).all()

    def actualizar_contrasena(self, usuario, nueva_contrasena):
        with self.Session() as session:
            usuario_obj = self.obtener_usuario(usuario, session)
            if usuario_obj is not None:
                usuario_obj.contrasena = nueva_contrasena
                session.commit()
                return usuario_obj
            return None

    def eliminar_usuario(self, usuario):
        with self.Session() as session:
            usuario_obj = self.obtener_usuario(usuario, session)
            if usuario_obj is not None:
                session.delete(usuario_obj)
                session.commit()
                return True
            return False

    def verificar_contrasena(self, usuario, contrasena):
        with self.Session() as session:
            usuario_obj = self.obtener_usuario(usuario, session)
            if usuario_obj is not None:
                if int(usuario_obj.contrasena) == contrasena:  
                    return usuario_obj
            return False
