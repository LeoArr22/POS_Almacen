from PIL import Image



#Funcion que lee una imagen de una ruta (path) y redimensiona segun tupla (size).
#Esto es convertido por ImageTk.PhotoImage en una objeto para ser usado por Tkinter
import customtkinter as ctk
from PIL import Image

def leer_imagen(path, size):
    return ctk.CTkImage(light_image=Image.open(path).resize(size, Image.LANCZOS),
                        size=size)



#ventana.geometry("ancho x alto + posicion_x + posicion_y")
#Define tamañano de la ventana y luego la posicion respecto al borde izquierdo y al borde superior
#Con nuestra funcion centrar_ventana  indicamos el tamaño de la pantalla
#y logramos que se ubique en el centro de la pantalla del usuario, esto gracias
#al calculo realizado en x e y
def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho/2) - (aplicacion_ancho/2))
    y = int((pantalla_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

#Recibe una ventana, la destruye y pasa a la siguiente
def destruir(ventana_actual, proxima_ventana):
        ventana_actual.destroy()  # Cierra la ventana actual
        proxima_ventana()
    