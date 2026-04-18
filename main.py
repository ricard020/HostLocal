import tkinter as tk
import os
import sys

# Ensure src can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.gui.main_window import ServerGUI
from src.utils.system import setup_app_id

def main():
    root = tk.Tk()
    
    # Configurar AppUserModelID
    setup_app_id('com.python.localserver.gui.1.0')

    # Establecer icono
    try:
        # Busca el icono en la carpeta 'assets/logo' relativa al script principal
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo", "logo-ico.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass

    # Centrar ventana
    window_width = 500
    window_height = 380
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = ServerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
