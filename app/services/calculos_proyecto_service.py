# app/services/calculos_proyecto_service.py

import math
from typing import List
from ..models.hito_db import HitoDB
from ..models.subtarea_db import SubtareaDB

class CalculosProyectoService:
    def __init__(self, hitos: List[HitoDB]):
        self.hitos = hitos

    # 1. Cálculos para cada Subtarea
    @staticmethod
    def calcular_tiempos_subtarea(subtarea: SubtareaDB):
        """
        Calcula los tiempos optimista, pesimista y la duración PERT para una subtarea.
        """
        tiempo_optimista = subtarea.tiempo_probable - 1
        tiempo_pesimista = subtarea.tiempo_probable + 2
        duracion_pert = (tiempo_optimista + subtarea.tiempo_probable *4+ tiempo_pesimista) / 6
        return {
            "tiempo_optimista": tiempo_optimista,
            "tiempo_pesimista": tiempo_pesimista,
            "duracion_pert": duracion_pert
        }

    # 2. Cálculos para cada Hito
    def calcular_tiempos_hito(self, hito: HitoDB):
        """
        Calcula los tiempos totales optimista, pesimista, desviación estándar y varianza para un hito.
        """
        tiempo_optimista_total = 0
        tiempo_pesimista_total = 0

        # Iteramos sobre las tareas del hito
        for tarea in hito.tareas:
            for subtarea in tarea.subtareas:
                tiempos_subtarea = self.calcular_tiempos_subtarea(subtarea)
                tiempo_optimista_total += tiempos_subtarea["tiempo_optimista"]
                tiempo_pesimista_total += tiempos_subtarea["tiempo_pesimista"]

        # Desviación estándar y varianza
        desviacion_estandar = (tiempo_pesimista_total - tiempo_optimista_total) / 6
        varianza = math.pow(desviacion_estandar, 2)

        return {
            "tiempo_optimista_total": tiempo_optimista_total,
            "tiempo_pesimista_total": tiempo_pesimista_total,
            "desviacion_estandar": desviacion_estandar,
            "varianza": varianza
        }

    # 3. Cálculos a Nivel de Proyecto
    def calcular_tiempos_proyecto(self):
        """
        Calcula la desviación estándar total, el PERT total, y los tiempos más optimista y pesimista para el proyecto.
        """
        # Suma de varianzas y cálculo de desviación estándar total
        suma_varianzas = sum(self.calcular_tiempos_hito(hito)["varianza"] for hito in self.hitos)
        desviacion_estandar_total = math.sqrt(suma_varianzas)

        # Cálculo de PERT total (suma de duraciones PERT de todas las subtareas en el proyecto)
        pert_total = sum(
            self.calcular_tiempos_subtarea(subtarea)["duracion_pert"]
            for hito in self.hitos
            for tarea in hito.tareas
            for subtarea in tarea.subtareas
        )

        # Cálculo de tiempos más optimista y más pesimista para el proyecto
        tiempo_optimista_proyecto = pert_total - 2 * desviacion_estandar_total
        tiempo_pesimista_proyecto = pert_total + 2 * desviacion_estandar_total

        return {
            "desviacion_estandar_total": desviacion_estandar_total,
            "pert_total": pert_total,
            "tiempo_optimista_proyecto": tiempo_optimista_proyecto,
            "tiempo_pesimista_proyecto": tiempo_pesimista_proyecto
        }


    # 4. Método principal para ejecutar todos los cálculos
    def ejecutar_calculos(self):
        """
        Ejecuta los cálculos para cada subtarea, hito y el proyecto en general.
        """
        resultados_hitos = []

        for hito in self.hitos:
            # Calcular tiempos para cada subtarea dentro del hito
            resultados_subtareas = []
            for tarea in hito.tareas:
                for subtarea in tarea.subtareas:
                    tiempos_subtarea = self.calcular_tiempos_subtarea(subtarea)
                    subtarea.tiempo_optimista = tiempos_subtarea["tiempo_optimista"]
                    subtarea.tiempo_pesimista = tiempos_subtarea["tiempo_pesimista"]
                    subtarea.duracion_pert = tiempos_subtarea["duracion_pert"]

                    resultados_subtareas.append({
                        "nombre": subtarea.nombre,
                        "tiempo_optimista": subtarea.tiempo_optimista,
                        "tiempo_pesimista": subtarea.tiempo_pesimista,
                        "duracion_pert": subtarea.duracion_pert
                    })

            # Calcular tiempos agregados para el hito
            tiempos_hito = self.calcular_tiempos_hito(hito)
            hito.tiempo_optimista_total = tiempos_hito["tiempo_optimista_total"]
            hito.tiempo_pesimista_total = tiempos_hito["tiempo_pesimista_total"]
            hito.desviacion_estandar = tiempos_hito["desviacion_estandar"]
            hito.varianza = tiempos_hito["varianza"]

            resultados_hitos.append({
                "nombre": hito.nombre,
                "tiempo_optimista_total": hito.tiempo_optimista_total,
                "tiempo_pesimista_total": hito.tiempo_pesimista_total,
                "desviacion_estandar": hito.desviacion_estandar,
                "varianza": hito.varianza,
                "subtareas": resultados_subtareas
            })

        # Calcular tiempos a nivel de proyecto
        tiempos_proyecto = self.calcular_tiempos_proyecto()

        return {
            "hitos": resultados_hitos,
            "proyecto": {
                "tiempo_optimista_proyecto": tiempos_proyecto["tiempo_optimista_proyecto"],
                "tiempo_pesimista_proyecto": tiempos_proyecto["tiempo_pesimista_proyecto"],
                "desviacion_estandar_total": tiempos_proyecto["desviacion_estandar_total"],
                "pert_total": tiempos_proyecto["pert_total"]
            }
        }
