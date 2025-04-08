import tkinter as tk
from controlador import ControladorAlfabetizador

def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("AlfabeTIC - Aprende Jugando")
    ventana.geometry("600x500")
    ventana.configure(bg="#e1f5fe")

    titulo = tk.Label(ventana, text="🧠 AlfabeTIC 🧠", font=("Comic Sans MS", 26, "bold"), bg="#e1f5fe", fg="#0277bd")
    titulo.pack(pady=10)

    marco = tk.Frame(ventana, bg="white", bd=2, relief=tk.GROOVE)
    marco.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)

    app = ControladorAlfabetizador(marco)

    creditos = tk.Label(ventana, text="Hecho por Christian Jesús", font=("Arial", 10), bg="#e1f5fe", fg="#0288d1")
    creditos.pack(pady=5)

    ventana.mainloop()
