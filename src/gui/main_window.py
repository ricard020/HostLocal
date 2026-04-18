import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from src.logic.http_server import ThreadedHTTPServer, SilentHTTPHandler
from src.utils.network import get_local_ip
from src.gui.styles import configure_styles

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HostLocal | Servidor local para archivos")
        self.root.resizable(False, False)
        
        # --- Ruta por defecto: Desktop ---
        self.default_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        try:
            os.chdir(self.default_dir)
        except Exception:
            pass # Si falla, usa directorio actual
        
        # Configuración de estilo
        configure_styles(self.root)
        
        self.httpd = None
        self.server_thread = None
        self.is_running = False
        self.local_ip = get_local_ip()
        
        self.create_widgets()

    def create_widgets(self):
        # Marco Principal
        main_frame = ttk.Frame(self.root, padding="20", style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Servidor HTTP Local", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Area de Configuración
        config_frame = ttk.Frame(main_frame, style="Card.TFrame")
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Input Puerto
        port_frame = ttk.Frame(config_frame, style="Card.TFrame")
        port_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(port_frame, text="Puerto:", style="Body.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        
        self.port_var = tk.StringVar(value="8080")
        vcmd = (self.root.register(self.validate_port_input), '%P')
        self.port_entry = ttk.Entry(port_frame, textvariable=self.port_var, width=10, font=("Segoe UI", 10), validate="key", validatecommand=vcmd)
        self.port_entry.pack(side=tk.LEFT)
        
        # Area de IP y Copiar
        ip_frame = ttk.Frame(main_frame, style="Card.TFrame")
        ip_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.ip_display_var = tk.StringVar(value=f"Esperando iniciar...")
        self.ip_entry = ttk.Entry(ip_frame, textvariable=self.ip_display_var, state="readonly", font=("Segoe UI", 11, "bold"), justify="center")
        self.ip_entry.pack(fill=tk.X, pady=(0, 10), ipady=5)
        
        # Copiar Dirección IP
        self.copy_btn = ttk.Button(ip_frame, text="Copiar Dirección IP", command=self.copy_to_clipboard, state="disabled", takefocus=False)
        self.copy_btn.pack(fill=tk.X)
        
        # Estado
        self.status_var = tk.StringVar(value="Estado: Detenido")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, style="StatusStopped.TLabel")
        self.status_label.pack(pady=(0, 20))
        
        # Botones de Control
        control_frame = ttk.Frame(main_frame, style="Main.TFrame")
        control_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = tk.Button(control_frame, text="Iniciar Servidor", command=self.start_server, 
                                 bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), 
                                 relief="flat", pady=8, cursor="hand2", activebackground="#218838", activeforeground="white",
                                 takefocus=False)
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.stop_btn = tk.Button(control_frame, text="Detener Servidor", command=self.stop_server, 
                                state="disabled", bg="#6c757d", fg="white", font=("Segoe UI", 10, "bold"), 
                                relief="flat", pady=8, cursor="arrow", activebackground="#5a6268", activeforeground="white",
                                takefocus=False)
        self.stop_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Info pequeña
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        if cwd.startswith(home):
            display_path = cwd.replace(home, "~", 1)
        else:
            display_path = cwd
            
        info_label = ttk.Label(main_frame, text=f"Directorio: {display_path}", style="Small.TLabel")
        info_label.pack(side=tk.BOTTOM, anchor="w")

    def validate_port_input(self, P):
        if P == "":
            return True
        return P.isdigit()

    def start_server(self):
        # Actualizar IP local al iniciar por si hubo cambios de red
        self.local_ip = get_local_ip()

        port_str = self.port_var.get()
        if not port_str.isdigit():
            messagebox.showerror("Error", "El puerto debe ser un número valido.")
            return
            
        port = int(port_str)
        if port < 1024 or port > 65535:
            # Permitimos puertos bajos pero no hacemos nada especial
            pass

        try:
            # Crear servidor
            self.httpd = ThreadedHTTPServer(("0.0.0.0", port), SilentHTTPHandler)
            
            # Actualizar GUI
            self.is_running = True
            
            self.start_btn.config(state="disabled", bg="#6c757d", cursor="arrow")
            self.stop_btn.config(state="normal", bg="#dc3545", cursor="hand2")
            self.port_entry.config(state="disabled")
            self.copy_btn.state(["!disabled"])
            
            addr_str = f"{self.local_ip}:{port}"
            self.ip_display_var.set(addr_str)
            
            self.status_var.set(f"Estado: Ejecutando en puerto {port}")
            self.status_label.configure(style="StatusRunning.TLabel")
            
            # Iniciar hilo
            self.server_thread = threading.Thread(target=self.httpd.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
        except OSError as e:
            messagebox.showerror("Error al iniciar", f"No se pudo iniciar en el puerto {port}.\nEs probable que este ocupado.\n\nDetalle: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def stop_server(self):
        if self.httpd:
            threading.Thread(target=self.httpd.shutdown).start()
        
        self.is_running = False
        self.start_btn.config(state="normal", bg="#28a745", cursor="hand2")
        self.stop_btn.config(state="disabled", bg="#6c757d", cursor="arrow")
        self.port_entry.config(state="normal")
        self.copy_btn.state(["disabled"])
        
        self.ip_display_var.set("Esperando iniciar...")
        self.status_var.set("Estado: Detenido")
        self.status_label.configure(style="StatusStopped.TLabel")

    def copy_to_clipboard(self):
        content = self.ip_display_var.get()
        if content and content != "Esperando iniciar...":
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()
            # Feedback visual
            original_text = self.copy_btn.cget("text")
            self.copy_btn.configure(text="Copiado!")
            self.root.after(1500, lambda: self.copy_btn.configure(text=original_text))
