# app/models/tarea.py

from pydantic import BaseModel
from typing import List
from .subtarea import Subtarea

class Tarea(BaseModel):
    nombre: str
    subtareas: List[Subtarea] = []  # Inicializa la lista de subtareas

    def agregar(self, subtarea: Subtarea):
        self.subtareas.append(subtarea)  # Agrega una subtarea a la lista de subtareas

    def calcular_tiempos(self) -> dict:
        suma_optimista = sum(subtarea.calcular_optimista() for subtarea in self.subtareas)
        suma_pesimista = sum(subtarea.calcular_pesimista() for subtarea in self.subtareas)
        suma_esperado = sum(subtarea.calcular_esperado() for subtarea in self.subtareas)
        return {"optimista": suma_optimista, "pesimista": suma_pesimista, "esperado": suma_esperado}

    def __str__(self):
        subtareas_str = "\n".join(str(subtarea) for subtarea in self.subtareas)
        return f"  Tarea: {self.nombre}\n{subtareas_str}"
