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

