from data.sql.engine import *

#Nuestra clase CRUD recibe como parametro en su constructor la session
class CRUD_usuario():
    def __init__(self, Session):
        self.session = Session

    # Crear usuario
    
    def crear_usuario(self, usuario, contrasena):
        if self.obtener_usuario(usuario) is None:
            nuevo_usuario = Vendedor(usuario=usuario, contrasena=contrasena)
            self.session.add(nuevo_usuario)
            self.session.commit()
            return nuevo_usuario, None  # Retorna el nuevo usuario y None para indicar éxito
        else:
            return None, "Ese nombre de usuario ya está en uso"  # Retorna None y el mensaje de error

    def modificar_usuario(self, usuario, usuario_nuevo, contrasena_nueva):
        print(usuario)
        usuario_obj = self.obtener_usuario(usuario)
        
        if usuario_obj is None:
            return None, "Usuario no encontrado"
        
        # Verificar que no se cambie el nombre de 'admin'
        if usuario_obj.usuario == 'admin' and usuario_nuevo != usuario_obj.usuario:
            return None, "El usuario 'admin' no puede cambiar su nombre."
        
        # Modificar el nombre de usuario si es proporcionado
        if usuario_nuevo:
            usuario_obj.usuario = usuario_nuevo
        
        # Modificar la contraseña si es proporcionada
        if contrasena_nueva:
            usuario_obj.contrasena = contrasena_nueva
        
        # Guardar los cambios en la base de datos
        self.session.commit()
        return usuario_obj, None 


    # Leer usuario (buscar por nombre) En caso de no encontrarlo devuelve None
    def obtener_usuario(self, usuario):
        try:
            usuario = self.session.query(Vendedor).filter_by(usuario=usuario).one()
            return usuario
        except NoResultFound:
            return None
 
    def obtener_todos_usuarios(self):
        usuarios = self.session.query(Vendedor).all()
        return usuarios

    # Actualizar contraseña del usuario. Primero busca el usuario con el metodo obtener_usuario, 
    # si este es igual a None, no realiza ningun cambio y devuelve None 
    
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

    def verificar_contrasena(self, usuario, contrasena):
        usuario_obj = self.obtener_usuario(usuario)
        if usuario_obj is not None:
            print(f"Contraseña en BD: {usuario_obj.contrasena}, Contraseña ingresada: {contrasena}")
            print(f"Tipo en BD: {type(usuario_obj.contrasena)}, Tipo ingresado: {type(contrasena)}")
            if (int(usuario_obj.contrasena) == contrasena):
                return usuario_obj
        return False




# #CON ESTO CREAMOS UNA SESION. 
# # Session() es una "fabrica de sesiones", aqui nos esta creando una sesion llamada session
# session=Session()
# # De todas formas vamos a usar with para que cierre sesion automaticamente una vez termine de aplicar la funcionalidad
# with Session() as session:
#     # Instanciamos un objeto crud_usuario, perteneciente a la clase CRUD_usuario y le pasamos la sesion que creamos antes
#     crud_usuario = CRUD_usuario(session)
#     # Llamamos al metodo que queremos utilizar
#     crud_usuario.crear_usuario("Angieeee", "1234")
# # INVESTIGAR Y AGREGAR HASING A LAS CONTRASEÑAS