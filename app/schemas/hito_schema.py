# app/schemas/hito_schema.py
from pydantic import BaseModel
from typing import List
from .tarea_schema import TareaSchema

class HitoSchema(BaseModel):
    nombre: str
    tareas: List[TareaSchema]  # Lista de tareas

    # Totales de tiempo para el hito completo
    tiempo_optimista: float = None
    tiempo_pesimista: float = None
    tiempo_esperado: float = None

    class Config:
        from_attributes = True
