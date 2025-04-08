from niveles.nivel1 import Nivel1
from niveles.nivel2 import Nivel2
from niveles.nivel3 import Nivel3

class FabricaDeNiveles:
    @staticmethod
    def crear_nivel(numero):
        if numero == 1:
            return Nivel1()
        elif numero == 2:
            return Nivel2()
        elif numero == 3:
            return Nivel3()
        else:
            raise ValueError(f"Nivel {numero} no válido")
