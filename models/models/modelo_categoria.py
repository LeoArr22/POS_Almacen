from models.util.validadores import longitud_palabra, recorre_validadores, solo_letras

class ModeloCategoria:
    def __init__(self, nombre=None, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion
     
        
#NOMBRE    
    @property #Convertimos el metodo en un getter
    def nombre (self):
        return self.__nombre
    
    @nombre.setter #convertimos el metodo en un setter, usamos notacion de punto categoria.nombre="Nuevo_nombre"
    def nombre(self, nuevo_nombre):
        if nuevo_nombre is not None:
        # Lista de validadores con sus parametros
            validadores = [
                lambda palabra: longitud_palabra(palabra, 2, 20), #Usamos funciones anonimas para validar cada validador
                lambda palabra: solo_letras(palabra) #todas nos van a devolver una tupla de dos valores
                         ]
    #La tupla obtenida puede ser (False, "mensaje de error") o (True, "")
    #"valido" guarda al booleano, "mensaje" al string
    #en caso de ser falso se activa el if y devuelve como mensaje de error al try para su impresion
            resultado = recorre_validadores(validadores, nuevo_nombre)
            if resultado is not None:
                return resultado    
        self.__nombre = nuevo_nombre 

#DESCRIPCION
    @property
    def descripcion(self):
        return self.__descripcion
    
    @descripcion.setter
    def descripcion(self, nueva_descripcion):
        if nueva_descripcion is not None and nueva_descripcion.strip() != "":
            validadores = [
                lambda palabra: longitud_palabra(palabra, 0, 40)
            ]
            resultado = recorre_validadores(validadores, nueva_descripcion)
            if resultado is not None:
                return resultado
        self.__descripcion = nueva_descripcion

    
  
        
        

    
            
            
