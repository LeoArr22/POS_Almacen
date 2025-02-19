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

    def actualizar_nombre(self, usuario, usuario_nuevo):
        with self.Session() as session:
            usuario_obj = self.obtener_usuario(usuario, session)
            nuevo_nombre = self.obtener_usuario(usuario_nuevo, session)
            
            if usuario_obj is None:
                return None, "Usuario no encontrado"
            
            if nuevo_nombre is not None:
                return None, "Ya existe un usuario con ese nombre"

            if usuario_obj.usuario == 'admin':
                return None, "El usuario 'admin' no puede cambiar su nombre."

            usuario_obj.usuario = usuario_nuevo

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
                return usuario_obj, ""
            return None, "Usuario no encontrado"

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
