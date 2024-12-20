# auth.py
from data.sql.engine import *

# Crear la sesión con el engine existente
Session = sessionmaker(bind=engine)

def verificar_o_crear_vendedor():
    """Verifica si existe un vendedor. Si no, solicita crear uno."""
    session = Session()  # Crear la sesión dentro de la función para evitar conflictos
    try:
        # Verificar si ya existe un vendedor
        vendedor_existente = session.query(Vendedor).first()
        if vendedor_existente:
            print("Ya existe al menos un vendedor. Continuando...")
        else:
            print("No se encontró ningún vendedor. Creando uno nuevo...")
            usuario = input("Ingrese el nombre de usuario: ")
            contrasena = input("Ingrese la contraseña (numérica): ")
            nuevo_vendedor = Vendedor(usuario=usuario, contrasena=int(contrasena))
            session.add(nuevo_vendedor)
            session.commit()
            print(f"Vendedor {usuario} creado con éxito.")
    except Exception as e:
        print(f"Error al verificar o crear un vendedor: {e}")
        session.rollback()
    finally:
        session.close()
