import sys
import os

# Obtiene el directorio actual del script en ejecución
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtiene el directorio raíz de POS_Almacen
pos_almacen_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Agrega la subcarpeta 'DATA' al path
data_dir = os.path.join(pos_almacen_dir, "GUI")
sys.path.append(data_dir)


import customtkinter as ctk
from tkinter.font import BOLD
from util.generic import centrar_ventana



class MasterPanel:
    def __init__(self):
        self.ventana = ctk.CTk()  #Crea la ventana principal
        self.ventana.title('TuAlmaZen')
        centrar_ventana(self.ventana, 1250, 700)
        self.ventana.resizable(width=1, height=1)
        self.ventana.attributes("-topmost", True)  # Mantener siempre en la parte superior
        
        self.frame=ctk.CTkFrame(self.ventana, width=1000, height=600, fg_color="#F3920F")
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        
        
        self.ventana.mainloop()
        
        
        
MasterPanel()