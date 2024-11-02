# suma_optimista.py
class SumaOptimista:
    def __init__(self, hito):
        self.hito = hito

    def calcular(self):
        return self.hito.calcular_tiempos()["optimista"]
