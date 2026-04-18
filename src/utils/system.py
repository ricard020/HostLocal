def setup_app_id(app_id: str):
    """Configura el AppUserModelID para que el icono se muestre correctamente en la barra de tareas."""
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass
