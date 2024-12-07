from models.util.validadores import *

class ModeloUsuario:
    def __init__(self, usuario=None, contrasena=None):
        self.usuario = usuario
        self.contrasena = contrasena
        
#USUARIO
    @property
    def usuario(self):
        return self.__usuario 

    @usuario.setter
    def usuario(self, nuevo_usuario):
        if nuevo_usuario is not None:
            validadores = [
                lambda palabra: longitud_palabra(palabra, 1, 10),
                lambda palabra: solo_letras(palabra)
            ]

            recorre_validadores(validadores, nuevo_usuario)
            self.__usuario = nuevo_usuario

#CONTRASENA 
    @property
    def contrasena(self):
        return self.__contrasena  
    
    @contrasena.setter
    def contrasena(self, nueva_contrasena):
        if nueva_contrasena is not None:
            validadores = [
                lambda numero: longitud_numero(numero, 4, 4),
                lambda numero: solo_numero(numero)
            ]
            recorre_validadores(validadores, nueva_contrasena)
            self.__contrasena = nueva_contrasena
                  