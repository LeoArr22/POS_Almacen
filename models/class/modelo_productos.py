from models.util.validadores import *

class ModeloProducto:
    def __init__(self, nombre=None, precio=None, stock=None, costo=None, codigo_barra=None, categoriaID=None):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.costo = costo
        self.codigo_barra = codigo_barra
        self.categoriaID = categoriaID

    # NOMBRE
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre is not None:
            validadores = [
                lambda palabra: longitud_palabra(palabra, 1, 30)
            ]
            recorre_validadores(validadores, nuevo_nombre)
            self.__nombre = nuevo_nombre

    # PRECIO
    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio is not None:
            validadores = [
                lambda numero: longitud_numero(float(numero), 1, 8),
                lambda numero: solo_numero(numero),
                lambda numero: positivo(numero)
            ]
            recorre_validadores(validadores, nuevo_precio)
            self.__precio = nuevo_precio

    # STOCK
    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, nuevo_stock):
        if nuevo_stock is not None:
            validadores = [
                lambda numero: numero_entero_positivo(numero)
            ]
            recorre_validadores(validadores, nuevo_stock)
            self.__stock = nuevo_stock

    # COSTO
    @property
    def costo(self):
        return self.__costo

    @costo.setter
    def costo(self, nuevo_costo):
        if nuevo_costo is not None:
            validadores = [
                lambda numero: longitud_numero(float(numero), 1, 8),
                lambda numero: numero_positivo(float(numero))
            ]
            recorre_validadores(validadores, nuevo_costo)
            self.__costo = nuevo_costo

    # CÓDIGO DE BARRA
    @property
    def codigo_barra(self):
        return self.__codigo_barra

    @codigo_barra.setter
    def codigo_barra(self, nuevo_codigo_barra):
        if nuevo_codigo_barra is not None:
            validadores = [
                lambda codigo: longitud_numero(codigo, 13, 13),
                lambda codigo: solo_numero(codigo)
            ]
            recorre_validadores(validadores, nuevo_codigo_barra)
            self.__codigo_barra = nuevo_codigo_barra