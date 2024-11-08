# app/services/calculos_totales.py
import math
from typing import List
from ..models.hito_db import HitoDB

class CalculosTotales:
    def __init__(self, hitos: List[HitoDB]):
        self.hitos = hitos

    def calcular_totales(self):
        suma_varianzas = sum(hito.calcular_varianza() for hito in self.hitos)
        desviacion_estandar_total = math.sqrt(suma_varianzas)
        pert_total = sum(hito.calcular_tiempos()["esperado"] for hito in self.hitos)
        return {
            "desviacion_estandar_total": desviacion_estandar_total,
            "pert_total": pert_total
        }