import http.server
import socketserver

class SilentHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Manejador HTTP que silencia los errores de conexión rotos."""
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass
    
    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass
    
    def log_message(self, format, *args):
        pass  # Silenciar logs en consola para limpiar

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Servidor HTTP multihilo."""
    daemon_threads = True
    allow_reuse_address = True
