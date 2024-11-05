# app/models/proyecto.py
from pydantic import BaseModel
from typing import List
from .hito import Hito

class Hito(BaseModel):
    nombre: str
    hitos: List[Hito]

    def calcular_tiempos(self) -> dict:
        suma_optimista = sum(hito.calcular_tiempos()["optimista"] for tarea in self.hitos)
        suma_pesimista = sum(tarea.calcular_tiempos()["pesimista"] for tarea in self.hitos)
        return {"optimista": suma_optimista, "pesimista": suma_pesimista}

    def __str__(self):
        tareas_str = "\n".join(str(tarea) for tarea in self.tareas)
        return f"Hito: {self.nombre}\n{tareas_str}"