from models.util.validadores import recorre_validadores, longitud_palabra, solo_numero, longitud_numero, positivo

class ModeloProducto:
    def __init__(self, nombre=None, precio=None, stock=None, costo=None, codigo_barra=None):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.costo = costo
        self.codigo_barra = codigo_barra

#SE USARA PARA EL CREATE. VALIDA QUE TODOS LOS CAMPOS TENGAS DATOS
    def es_completo(self):
        atributos_requeridos = ["nombre", "precio", "stock", "costo", "codigo_barra"]
        for atributo in atributos_requeridos:
            if getattr(self, atributo) is None: #getattr: obtiene el valor de cada atributo. Si alguno es None
                raise ValueError(f"El campo '{atributo}' está incompleto") #significa que nuestro modelo aun 
                                                                           #no esta completo y nos devuelve False
        return True
        
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre is not None:
            validadores = [
                lambda palabra: longitud_palabra(palabra, 1, 20)
            ]
            recorre_validadores(validadores, nuevo_nombre)
        self.__nombre = nuevo_nombre

    @property
    def precio(self):
        return self.__precio
    
    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio is not None:
            validadores = [
                lambda numero: solo_numero(numero),
                lambda numero: longitud_numero(numero, 1, 10),
                lambda numero: positivo(numero)
            ]
            recorre_validadores(validadores, nuevo_precio)
            nuevo_precio = int(nuevo_precio)
        self.__precio = nuevo_precio

    @property
    def stock(self):
        return self.__stock
    
    @stock.setter
    def stock(self, nuevo_stock):
        if nuevo_stock is not None:
            validadores = [
                lambda numero: solo_numero(numero),
                lambda numero: longitud_numero(numero, 1, 10)
            ]
            recorre_validadores(validadores, nuevo_stock)
            nuevo_stock = int(nuevo_stock)
        self.__stock = nuevo_stock

    @property
    def costo(self):
        return self.__costo
    
    @costo.setter
    def costo(self, nuevo_costo):
        if nuevo_costo is not None:
            validadores = [
                lambda numero: solo_numero(numero),
                lambda numero: longitud_numero(numero, 1, 999999),
                lambda numero: positivo(numero)
            ]
            recorre_validadores(validadores, nuevo_costo)
            nuevo_costo = int(nuevo_costo)
        self.__costo = nuevo_costo

    @property
    def codigo_barra(self):
        return self.__codigo_barra
    
    @codigo_barra.setter
    def codigo_barra(self, nuevo_codigo):
        if nuevo_codigo is not None:
            validadores = [
                lambda numero: solo_numero(numero),
                lambda numero: longitud_numero(numero, 13, 13),
                lambda numero: positivo(numero)
            ]
            recorre_validadores(validadores, nuevo_codigo)
            nuevo_codigo = int(nuevo_codigo)
        self.__codigo_barra = nuevo_codigo
