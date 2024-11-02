# suma_pesimista.py
class SumaPesimista:
    def __init__(self, hito):
        self.hito = hito

    def calcular(self):
        return self.hito.calcular_tiempos()["pesimista"]
