import tkinter as tk
from tkinter.font import BOLD
from generic import centrar_ventana


class MasterPanel:
    
                                      
    def __init__(self):        
        self.ventana = tk.Tk()                             
        self.ventana.title('Master panel')
        centrar_ventana(self.ventana, 500, 500)
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)            
        
        self.ventana.mainloop()
        
