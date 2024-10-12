from engine import *

class CRUD_usuario:
    def __init__(self, Session):
        self.session = Session

    # Crear usuario
    def crear_usuario(self, usuario, contrasena):
        if self.obtener_usuario(usuario) is None:
            nuevo_usuario = Vendedor(usuario=usuario, contrasena=contrasena)
            self.session.add(nuevo_usuario)
            self.session.commit()
            return nuevo_usuario
        else:
            print("Ese nombre de usuario ya esta en uso")

    # Leer usuario (buscar por nombre)
    def obtener_usuario(self, usuario):
        try:
            usuario = self.session.query(Vendedor).filter_by(usuario=usuario).one()
            return usuario
        except NoResultFound:
            return None

    # Actualizar contraseña del usuario
    def actualizar_contrasena(self, usuario, nueva_contrasena):
        usuario = self.obtener_usuario(usuario)
        if usuario is not None:
            usuario.contrasena = nueva_contrasena
            self.session.commit()
            return usuario
        return None

    # Eliminar usuario
    def eliminar_usuario(self, usuario):
        usuario = self.obtener_usuario(usuario)
        if usuario is not None:
            self.session.delete(usuario)
            self.session.commit()
            return True
        return False

    # Verificar contraseña
    def verificar_contrasena(self, usuario, contrasena):
        usuario = self.obtener_usuario(usuario)
        if usuario is not None:
            return usuario.contrasena == contrasena
        return False



#CON ESTO CREAMOS UNA SESION. 
#Session() es una "fabrica de sesiones", aqui nos esta creando una sesion llamada session
session = Session()
# Instanciamos un objeto crud_usuario, perteneciente a la clase CRUD_usuario y le pasamos la sesion que creamos antes
crud_usuario = CRUD_usuario(session)
# Llamamos al metodo que queremos utilizar
crud_usuario.crear_usuario("Victor", 1234)

#INVESTIGAR Y AGREGAR HASING A LAS CONTRASEÑAS