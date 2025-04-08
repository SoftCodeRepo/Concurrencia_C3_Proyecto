import random

class Nivel1:
    def __init__(self):
        self.colores = {
            "Rojo": "#f44336",
            "Verde": "#4caf50",
            "Azul": "#2196f3",
            "Amarillo": "#ffeb3b",
            "Morado": "#9c27b0",
            "Naranja": "#ff9800",
            "Rosa": "#e91e63",
            "Café": "#795548",
            "Gris": "#9e9e9e",
            "Negro": "#000000",
            "Celeste": "#00bcd4"
        }


    def generar_pregunta(self):
        color_nombre, color_hex = random.choice(list(self.colores.items()))
        distractores = random.sample([c for c in self.colores if c != color_nombre], 2)
        opciones = [color_nombre] + distractores
        random.shuffle(opciones)
        return color_hex, color_nombre, opciones
