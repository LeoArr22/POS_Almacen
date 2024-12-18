from PIL import Image, ImageDraw, ImageTk

def crear_degradado(ancho, alto, color1, color2):
    """
    Genera un degradado vertical entre dos colores.
    """
    img = Image.new("RGBA", (ancho, alto), color=color1)
    draw = ImageDraw.Draw(img)
    for i in range(alto):
        ratio = i / alto
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, i), (ancho, i)], fill=(r, g, b))
    return img


def configurar_boton_elegante(boton, border_color="#000000", border_width=4):
    """
    Configura un botón con sombras y bordes elegantes.
    """
    boton.configure(border_width=border_width, border_color=border_color)

#Funcion que lee una imagen de una ruta (path) y redimensiona segun tupla (size).
#Esto es convertido por ImageTk.PhotoImage en una objeto para ser usado por Tkinter
def leer_imagen (path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))


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