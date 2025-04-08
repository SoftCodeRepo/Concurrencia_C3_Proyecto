import threading
log_lock = threading.RLock()

class Observador:
    def notificar(self):
        pass

class Logger(Observador):
    def notificar(self, evento, data):
        def log():
            with log_lock:
                with open("registro.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{evento.upper()}] {data}\n")
        threading.Thread(target=log).start()

class Temporizador(Observador):
    def __init__(self, timeout, callback, controlador):
        self.timeout = timeout
        self.callback = callback
        self.controlador = controlador
        self.hilo = None
        self.cancelar_evento = threading.Event()

    def iniciar(self):
        self.cancelar()
        self.cancelar_evento.clear()
        
        def esperar():
            for tiempo in range(self.timeout, 0, -1):
                self.controlador.ventana.after(0, self.controlador.actualizar_tiempo, tiempo)
                if self.cancelar_evento.wait(1):
                    return
            
            if not self.cancelar_evento.is_set():
                self.controlador.ventana.after(0, self.callback)

        self.hilo = threading.Thread(target=esperar)
        self.hilo.daemon = True
        self.hilo.start()

    def cancelar(self):
        self.cancelar_evento.set()
        
        if self.hilo and self.hilo.is_alive():
            self.hilo.join(0.1)

    def notificar(self, evento, data):
        if evento == "nueva_pregunta":
            self.iniciar()
        elif evento == "respuesta":
            self.cancelar()