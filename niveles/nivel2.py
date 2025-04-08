import random

class Nivel2:
    def __init__(self):
        self.palabras = [
            ("_sa", "ca"), ("ca_", "sa"), ("ma_", "no"), ("_no", "ma"),
            ("pa_", "to"), ("_to", "pa"), ("_l", "so"), ("so_", "le"),
            ("_cha", "le"), ("le_", "che"), ("ca_", "llo"), ("_llo", "ca"),
            ("pi_", "eza"), ("_eza", "pi"), ("bo_", "ta"), ("_ta", "bo")
        ]
        # Set de palabras válidas que no pueden ser opciones
        self.palabras_validas = set(pair[1] for pair in self.palabras)

    def generar_pregunta(self):
        incompleta, correcta = random.choice(self.palabras)
        distractores = ["me", "ri", "ta", "la", "ro", "mi", "pa", "to", "lo", "so"]
        
        # Filtrar distractores para evitar que sean combinaciones válidas
        opciones = []
        while len(opciones) < 3:
            distractor = random.choice(distractores)
            if distractor not in self.palabras_validas and distractor not in opciones:
                opciones.append(distractor)
        
        # Asegurarse de que la respuesta correcta esté en las opciones
        opciones.append(correcta)
        random.shuffle(opciones)
        
        return incompleta, correcta, opciones
