def valida_usuario(func):
    def wrapper (self, *args, **kwargs):
        usuario=args[0]
        contrasena=args[1]
        if len(usuario)>10:
            raise ValueError("El nombre de usuario no puede ser mayor a 10 caracteres")
        if len(contrasena)==4:
            try:
                contrasena=int(contrasena)
            except ValueError:
                raise ValueError("La contraseña debe ser numerica")
        else:
            raise ValueError("La contraseña debe ser de 4 caracteres")
        
        return func(self, usuario, contrasena)
    return wrapper


def valida_producto(func):
    def wrapper(self, *args, **kwargs):
        nombre = args[0]
        precio = args[1]
        stock = args[2]
        costo = args[3]
        
        if len(nombre) > 30:
            raise ValueError("El nombre del producto no puede ser mayor a 30 caracteres")
        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio debe ser un número positivo")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("El stock debe ser un número entero no negativo")
        if not isinstance(costo, (int, float)) or costo <= 0:
            raise ValueError("El costo debe ser un número positivo")

        return func(self, *args, **kwargs)
    return wrapper

    
def valida_categoria(func):
    def wrapper(self, *args, **kwargs):
        nombre = args[0]
        if len(nombre) == 0:
            raise ValueError("El nombre de la categoría no puede estar vacío")
        if len(nombre) > 30:
            raise ValueError("El nombre de la categoría no puede ser mayor a 30 caracteres")
        
        return func(self, *args, **kwargs)
    return wrapper
#validar todo en columna detalle
def validar_cantidad(cantidad):
    """Valida que la cantidad sea un entero positivo."""
    if isinstance(cantidad, int) and cantidad > 0:
        return True
    else:
        print("Cantidad inválida: debe ser un entero positivo.")
        return False

def validar_total_prod(total_prod):
    """Valida que el total del producto sea un número decimal positivo."""
    if isinstance(total_prod, (int, float)) and total_prod >= 0:
        return True
    else:
        print("Total del producto inválido: debe ser un número positivo.")
        return False

def validar_ids(producto_id, venta_id):
    """Valida que los IDs sean enteros positivos."""
    if isinstance(producto_id, int) and producto_id > 0 and isinstance(venta_id, int) and venta_id > 0:
        return True
    else:
        print("IDs inválidos: deben ser enteros positivos.")
        return False
