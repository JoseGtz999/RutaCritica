import math

class CalculosEstadisticos:
    def __init__(self, hito):
        self.hito = hito

    def calcular_desviacion_y_varianza(self):
        tiempos = self.hito.calcular_tiempos()
        desviacion_estandar = (tiempos["pesimista"] - tiempos["optimista"]) / 6
        varianza = desviacion_estandar ** 2
        return tiempos["optimista"], tiempos["pesimista"], desviacion_estandar, varianza
