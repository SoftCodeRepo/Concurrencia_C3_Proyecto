import random

class Nivel2:
    def __init__(self):
        self.palabras = [
            ("_sa", "ca"), ("ca_", "sa"), ("ma_", "no"), ("_no", "ma"),
            ("pa_", "to"), ("_to", "pa"), ("_l", "so"), ("so_", "le"),
            ("_cha", "le"), ("le_", "che"), ("ca_", "llo"), ("_llo", "ca"),
            ("pi_", "eza"), ("_eza", "pi"), ("bo_", "ta"), ("_ta", "bo")
        ]


    def generar_pregunta(self):
        incompleta, correcta = random.choice(self.palabras)
        distractores = ["me", "ri", "ta", "la", "ro", "mi"]
        opciones = random.sample(distractores, 3)
        if correcta not in opciones:
            opciones[random.randint(0, 1)] = correcta
        else:
            opciones.append(correcta)
        random.shuffle(opciones)
        return incompleta, correcta, opciones
