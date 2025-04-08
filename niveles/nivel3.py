import random

class Nivel3:
    def __init__(self):
        self.frases = [
            ("El perro _ rápido.", "corre"),
            ("La niña _ agua.", "bebe"),
            ("Mi mamá cocina _.", "sopa"),
            ("El sol está _.", "brillando"),
            ("Yo leo un _.", "libro"),
            ("La casa es _.", "grande"),
            ("El gato _ leche.", "toma"),
            ("Papá lee el _.", "periódico"),
            ("El niño juega con la _.", "pelota"),
            ("La flor es muy _.", "bonita"),
            ("Me gusta comer _.", "fruta"),
            ("El tren va muy _.", "rápido")
        ]       


    def generar_pregunta(self):
        oracion, correcta = random.choice(self.frases)
        distractores = ["lápiz", "salta", "juega", "tele", "mesa", "rojo"]
        opciones = random.sample(distractores, 3)
        if correcta not in opciones:
            opciones[random.randint(0, 1)] = correcta
        else:
            opciones.append(correcta)
        random.shuffle(opciones)
        return oracion, correcta, opciones
