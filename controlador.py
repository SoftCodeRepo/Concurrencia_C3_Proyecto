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
        self.puntos_nivel2 = 1
        self.puntos_nivel3 = 3
        self.puntos_finales = 5
        self.intentos_fallidos = 0

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

        self.mostrar_pantalla_inicio()

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

    def mostrar_pantalla_inicio(self):
        mensaje = (
            "\u00a1Bienvenido a AlfabeTIC - Aprende Jugando!\n\n"
            "Este juego educativo te ayudar\u00e1 a mejorar tu lectura y escritura.\n"
            "Responde preguntas de colores, s\u00edlabas y oraciones para avanzar de nivel.\n"
            "\u00a1Buena suerte y divi\u00e9rtete!"
        )
        self.narrador.hablar(mensaje)
        messagebox.showinfo("Bienvenida", mensaje)
        self.siguiente_pregunta()

    def mostrar_pantalla_final(self):
        mensaje = (
            "\u00a1Felicidades! Has completado el juego.\n\n"
            f"Obtuviste un total de {self.puntos} puntos.\n"
            "Gracias por jugar con AlfabeTIC - Aprende Jugando."
        )
        messagebox.showinfo("\u00a1Juego Completado!", mensaje)
        self.narrador.hablar(mensaje)
        self.ventana.quit()

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

        def mostrar_nivel_nuevo():
            mensaje = f"\u00a1Has avanzado al nivel {self.nivel_numero}!"
            self.narrador.hablar(mensaje)
            messagebox.showinfo("\u00a1Nivel Nuevo!", mensaje)
            self.nivel_cambiado = True
            self.siguiente_pregunta()

        self.ventana.after(100, mostrar_nivel_nuevo)

    def verificar_progresion_nivel(self):
        if self.puntos >= self.puntos_finales:
            self.mostrar_pantalla_final()
            return True
        elif self.nivel_numero == 1 and self.puntos >= self.puntos_nivel2:
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
                    pregunta_texto = "\u00bfDe qu\u00e9 color es este?"
                    self.label.config(text=pregunta_texto, bg=color_hex, fg="white")
                elif self.nivel_numero == 2:
                    enunciado, self.correcta, opciones = pregunta
                    pregunta_texto = f"\u00bfQu\u00e9 s\u00edlaba falta en la palabra?\n{enunciado}"
                    self.label.config(text=pregunta_texto, bg="white", fg="#0d47a1")
                elif self.nivel_numero == 3:
                    enunciado, self.correcta, opciones = pregunta
                    pregunta_texto = f"\u00bfQu\u00e9 palabra completa la oraci\u00f3n?\n{enunciado}"
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
                    self.intentos_fallidos = 0
                    self.label_puntos.config(text=f"Puntos: {self.puntos}")
                    mensaje = f"\u00a1Bien hecho! Era '{self.correcta}'.\n+{puntos_ganados} punto(s)"
                    messagebox.showinfo("\u00a1Correcto!",mensaje)
                    self.narrador.hablar(mensaje)
                    cambio_de_nivel = self.verificar_progresion_nivel()

                    self.nivel_cambiado = False

                    if not cambio_de_nivel:
                        self.temporizador.cancelar()
                        self.ventana.after(1000, self.siguiente_pregunta)
                else:
                    self.botones[indice].config(bg="salmon")
                    self.intentos_fallidos += 1

                    if self.intentos_fallidos >= 3:
                        self.puntos = max(0, self.puntos - 1)
                        self.label_puntos.config(text=f"Puntos: {self.puntos}")
                        self.narrador.hablar("\u00a13 errores seguidos! Pierdes 1 punto.")
                        messagebox.showwarning("Penalizaci\u00f3n", "\u00a13 errores seguidos! Pierdes 1 punto.")
                        self.intentos_fallidos = 0

                    messagebox.showerror("Incorrecto", f"No era '{seleccion}', era '{self.correcta}'.")
                    self.temporizador.cancelar()
                    self.ventana.after(1000, self.siguiente_pregunta)

        threading.Thread(target=tarea).start()

    def tiempo_agotado(self):
        messagebox.showwarning("Tiempo agotado", "Se acab\u00f3 el tiempo. Vamos a la siguiente.")
        self.narrador.hablar("Se acab\u00f3 el tiempo. Vamos a la siguiente.")
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= 3:
            self.puntos = max(0, self.puntos - 1)
            self.label_puntos.config(text=f"Puntos: {self.puntos}")
            messagebox.showwarning("Penalizaci\u00f3n", "\u00a13 errores seguidos! Pierdes 1 punto.")
            self.narrador.hablar("\u00a13 errores seguidos! Pierdes 1 punto.")
            self.intentos_fallidos = 0

        self.notificar_observadores("respuesta", "sin respuesta")
        self.siguiente_pregunta()

    def actualizar_tiempo(self, tiempo_restante):
        self.label_tiempo.config(text=f"Tiempo: {tiempo_restante}")
