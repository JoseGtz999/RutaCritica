import math
from .calculos_estadisticos import CalculosEstadisticos
from .suma_optimista import SumaOptimista
from .suma_pesimista import SumaPesimista


class CalculosTotales:
    def __init__(self, hitos):
        self.hitos = hitos

    def calcular_totales(self):
        suma_varianzas = sum(CalculosEstadisticos(hito).calcular_desviacion_y_varianza()[3] for hito in self.hitos)
        desviacion_estandar_total = math.sqrt(suma_varianzas)

        pert_total = sum(
            tarea.calcular_tiempos()["esperado"]
            for hito in self.hitos
            for tarea in hito.tareas
        )

        suma_pesimista = sum(SumaPesimista(hito).calcular() for hito in self.hitos)
        tiempo_pesimista_total = suma_pesimista + 2 * desviacion_estandar_total

        suma_optimista = sum(SumaOptimista(hito).calcular() for hito in self.hitos)
        tiempo_optimista_total = suma_optimista - 2 * desviacion_estandar_total

        return {
            "desviacion_estandar_total": desviacion_estandar_total,
            "pert_total": pert_total,
            "tiempo_pesimista_total": tiempo_pesimista_total,
            "tiempo_optimista_total": tiempo_optimista_total
        }
