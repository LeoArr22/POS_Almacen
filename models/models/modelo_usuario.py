from util.validadores import recorre_validadores, solo_letras, longitud_palabra, solo_numero, longitud_numero

class ModeloUsuario:
    def __init__(self, usuario, contrasena ):
        self.usuario = usuario,
        self.contrasena = contrasena

    @property
    def usuario(self):
        return self.__usuario
    
    @usuario.setter
    def usuario(self, nuevo_usuario):
        if nuevo_usuario is not None:
            validadores = [
                lambda palabra: solo_letras(palabra),
                lambda palabra: longitud_palabra(palabra,1, 20)
            ]
            recorre_validadores(validadores, nuevo_usuario)
            self.__usuario = nuevo_usuario
            
    @property
    def contrasena(self):
       return self.__contrasena
   
    @contrasena.setter
    def contrasena(self, nueva_contrasena):
        if nueva_contrasena is not None:
            validadores = [
                lambda numero: solo_numero(numero),
                lambda numero: longitud_numero(numero, 4, 4)
            ]  
            recorre_validadores(validadores, nueva_contrasena)
            nueva_contrasena=int(nueva_contrasena)
            self.__contrasena = nueva_contrasena