import pyttsx3
import threading
import queue

class Narrador:
    def __init__(self):
        self.motor = pyttsx3.init()
        self.motor.setProperty('rate', 160)
        self.motor.setProperty('voice', self.get_voz_espanol())
        
        self.cola = queue.Queue()
        self.hilo = threading.Thread(target=self.procesar_cola)
        self.hilo.daemon = True
        self.hilo.start()

        self.lock = threading.Lock()

    def get_voz_espanol(self):
        for voz in self.motor.getProperty('voices'):
            if 'spanish' in voz.name.lower() or 'español1' in voz.id.lower():
                return voz.id
        return self.motor.getProperty('voices')[0].id

    def hablar(self, texto):
        self.cola.put(texto)

    def procesar_cola(self):
        while True:
            texto = self.cola.get()
            try:
                with self.lock:
                    self.motor.say(texto)
                    self.motor.runAndWait()
            except RuntimeError as e:
                print(f"[Narrador] Error: {e}")
            self.cola.task_done()
