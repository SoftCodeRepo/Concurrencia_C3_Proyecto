import tkinter as tk
import threading
from fabrica import FabricaDeNiveles
from observador import Logger, Temporizador
from narrador import Narrador
from tkinter import messagebox

class ControladorAlfabetizador:
    def __init__(self, ventana):
        self.ventana = ventana
        self.nivel_numero = 1
        self.nivel_actual = FabricaDeNiveles.crear_nivel(self.nivel_numero)

        self.puntos = 0
        self.puntos_nivel2 = 10
        self.puntos_nivel3 = 20

        self.nivel_cambiado = False

        self.configurar_interfaz()

        self.observadores = []
        self.logger = Logger()
        self.temporizador = Temporizador(10, self.tiempo_agotado, self)
        self.observadores += [self.logger, self.temporizador]

        self.narrador = Narrador()

        self.correcta = ""
        self.semaforo = threading.Semaphore(1)
        self.condicion = threading.Condition()

        self.siguiente_pregunta()

    def configurar_interfaz(self):
        panel_superior = tk.Frame(self.ventana, bg="white")
        panel_superior.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.label_nivel = tk.Label(panel_superior, text="Nivel 1", font=("Comic Sans MS", 14), bg="white", fg="#0d47a1")
        self.label_nivel.pack(side=tk.LEFT, padx=10)

        self.label_puntos = tk.Label(panel_superior, text="Puntos: 0", font=("Comic Sans MS", 14), bg="white", fg="#0d47a1")
        self.label_puntos.pack(side=tk.LEFT, padx=10)

        self.label_tiempo = tk.Label(panel_superior, text="Tiempo: 10", font=("Comic Sans MS", 14), bg="white", fg="#0d47a1")
        self.label_tiempo.pack(side=tk.RIGHT, padx=10)

        self.label = tk.Label(self.ventana, text="", font=("Comic Sans MS", 18), bg="white", fg="#0d47a1", wraplength=500, justify="center")
        self.label.pack(pady=15)

        self.botones = []
        for i in range(3):
            btn = tk.Button(self.ventana, text="", width=25, height=2, font=("Arial", 14), command=lambda i=i: self.verificar(i), bg="#bbdefb")
            btn.pack(pady=6)
            self.botones.append(btn)

    def notificar_observadores(self, evento, data=""):
        for obs in self.observadores:
            try:
                obs.notificar(evento, data)
            except Exception as e:
                print(f"Error al notificar observador: {e}")

    def cambiar_nivel(self, nuevo_nivel):
        self.temporizador.cancelar()

        self.nivel_actual = FabricaDeNiveles.crear_nivel(nuevo_nivel)
        self.nivel_numero = nuevo_nivel
        self.label_nivel.config(text=f"Nivel {self.nivel_numero}")
        messagebox.showinfo("¡Nivel Nuevo!", f"¡Has avanzado al nivel {self.nivel_numero}!.")
        
        self.nivel_cambiado = True

    def verificar_progresion_nivel(self):
        if self.nivel_numero == 1 and self.puntos >= self.puntos_nivel2:
            self.cambiar_nivel(2)
            return True
        elif self.nivel_numero == 2 and self.puntos >= self.puntos_nivel3:
            self.cambiar_nivel(3)
            return True
        return False

    def siguiente_pregunta(self):
        def tarea():
            with self.semaforo:
                pregunta = self.nivel_actual.generar_pregunta()

                if self.nivel_numero == 1:
                    color_hex, self.correcta, opciones = pregunta
                    pregunta_texto = "¿De qué color es este?"
                    self.label.config(text=pregunta_texto, bg=color_hex, fg="white")
                elif self.nivel_numero == 2:
                    enunciado, self.correcta, opciones = pregunta
                    pregunta_texto = f"¿Qué sílaba falta en la palabra?\n{enunciado}"
                    self.label.config(text=pregunta_texto, bg="white", fg="#0d47a1")
                elif self.nivel_numero == 3:
                    enunciado, self.correcta, opciones = pregunta
                    pregunta_texto = f"¿Qué palabra completa la oración?\n{enunciado}"
                    self.label.config(text=pregunta_texto, bg="white", fg="#0d47a1")

                if len(opciones) != 3:
                    opciones = opciones[:2] + [self.correcta]

                for i in range(3):
                    self.botones[i].config(text=opciones[i], bg="#bbdefb", state=tk.NORMAL)

                self.temporizador.cancelar()
                self.temporizador.iniciar()
                self.notificar_observadores("nueva_pregunta", str(self.correcta))

                texto_a_narrar = self.label.cget("text")
                self.narrador.hablar(texto_a_narrar)

        threading.Thread(target=tarea).start()

    def verificar(self, indice):
        seleccion = self.botones[indice].cget("text")
        self.notificar_observadores("respuesta", seleccion)

        def tarea():
            with self.condicion:
                if seleccion == self.correcta:
                    self.botones[indice].config(bg="lightgreen")
                    puntos_ganados = self.nivel_numero
                    self.puntos += puntos_ganados
                    self.label_puntos.config(text=f"Puntos: {self.puntos}")
                    messagebox.showinfo("¡Correcto!", f"¡Bien hecho! Era '{self.correcta}'.\n+{puntos_ganados} punto(s)")
                    cambio_de_nivel = self.verificar_progresion_nivel()
                    
                    self.nivel_cambiado = False
                    
                    if not cambio_de_nivel:
                        self.temporizador.cancelar()
                        self.ventana.after(1000, self.siguiente_pregunta)
                    else:
                        self.ventana.after(1000, self.siguiente_pregunta)
                else:
                    self.botones[indice].config(bg="salmon")
                    messagebox.showerror("Incorrecto", f"No era '{seleccion}', era '{self.correcta}'.")
                    self.temporizador.cancelar()
                    self.ventana.after(1000, self.siguiente_pregunta)

        threading.Thread(target=tarea).start()

    def tiempo_agotado(self):
        messagebox.showwarning("Tiempo agotado", "Se acabó el tiempo. Vamos a la siguiente.")
        self.notificar_observadores("respuesta", "sin respuesta")
        self.siguiente_pregunta()

    def actualizar_tiempo(self, tiempo_restante):
        self.label_tiempo.config(text=f"Tiempo: {tiempo_restante}")