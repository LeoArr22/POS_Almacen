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

