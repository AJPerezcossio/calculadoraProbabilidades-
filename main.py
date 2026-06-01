import tkinter as tk
from interfaz import ProbCalcApp

def main():
    # 1. Creamos la raíz de la aplicación Tkinter
    root = tk.Tk()
    
    # 2. Inicializamos nuestra interfaz pasándole la raíz
    app = ProbCalcApp(root)
    
    # 3. Encendemos el bucle infinito para que la ventana escuche clics y teclazos
    root.mainloop()

# Buenas prácticas de Ingeniería en Sistemas:
# Asegura que el archivo solo se ejecute si se le da "Play" directo a él
if __name__ == "__main__":
    main()
