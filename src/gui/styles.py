from tkinter import ttk

def configure_styles(root):
    """Configura los estilos de la aplicación."""
    # Colores y fuentes
    bg_color = "#f8f9fa"
    text_color = "#212529"
    
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("Main.TFrame", background=bg_color)
    style.configure("Card.TFrame", background=bg_color)
    
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background=bg_color, foreground="#343a40")
    style.configure("Body.TLabel", font=("Segoe UI", 10), background=bg_color, foreground=text_color)
    style.configure("Small.TLabel", font=("Segoe UI", 8), background=bg_color, foreground="#6c757d")
    
    style.configure("StatusStopped.TLabel", font=("Segoe UI", 10, "bold"), background=bg_color, foreground="#dc3545")
    style.configure("StatusRunning.TLabel", font=("Segoe UI", 10, "bold"), background=bg_color, foreground="#28a745")
    
    style.configure("TButton", font=("Segoe UI", 10), padding=5)
    
    root.configure(bg=bg_color)
