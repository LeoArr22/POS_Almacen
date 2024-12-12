from models.util.validadores import longitud_palabra, recorre_validadores, es_completo


class ModeloCategoria():
    def __init__(self, nombre=None):
        self.nombre=nombre
             
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre is not None:
            validadores = [
                lambda palabra: longitud_palabra(palabra, 3, 20)
            ]

            recorre_validadores(validadores, nuevo_nombre)
            self.__nombre = nuevo_nombre   
            
    def completo(self):
        es_completo("Nombre")
        
        

    
            
            
