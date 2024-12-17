import re #Importamos modulo re para trabajar con expresiones regulares
from datetime import datetime



#RECORRE LA LISTA DE VALIDADORES CORRESPONDIENTES
def recorre_validadores(validadores, valor):
        for validador in validadores:
            valido, mensaje = validador(valor)
            if not valido:
                raise ValueError(mensaje) 



#VALIDADORES DE STRING

def longitud_palabra(palabra, min, max):
    if len(palabra) > max:
        return (False, f"Superó la longitud máxima de {max} caracteres")
    elif len(palabra) < min:
        return (False, f"No alcanzó la longitud mínima de {min} caracteres")
    else:
        return (True, "") 

def solo_letras(palabra):
    # La siguiente es una expresion regular. 
    # fullmatch controla si en cualquier momento de la cadena se cumple con la condicion de 
    # a-zA-Z (todas las letras minus y mayus) y \s (los espacios)
    # la r inicial indica que se trata de una cadena sin procesar para evitar problemas con el guion invertido
    # El + indica uno o mas del conjunto anterior
    if re.fullmatch(r"[a-zA-ZñÑ\s]+", palabra):
        return (True, "")
    else:
        return (False, "Solo se permiten letras y espacios")
            
            
#VALIDADORES DE INT

def longitud_numero(numero, min, max):
    if not (min <= len(numero) <= max):
        if (min != max): 
            return False, f"Debe tener entre {min} y {max} dígitos."
        else:
            return False, f"Debe tener exactamente {min} digitos" 
    return True, ""

def solo_numero(numero):
    try:
        numero = int(numero)
        return True, ""
    except:
        return False, "El valor debe ser un número entero."
    
def positivo(numero):
    numero=int(numero)
    if numero > 0:
        return True, ""
    else:
        return False, "El valor debe ser mayor a 0"        
    
    
# VALIDADOR DE FECHA

def valida_fecha(fecha, formato=r"%Y-%m-%d"):
    try:
        datetime.strptime(fecha, formato)
        return (True, "")
    except:
        return (False, "Fecha no valida (YYYY-MM-DD)")
