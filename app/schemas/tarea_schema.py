# app/schemas/tarea_schema.py
from pydantic import BaseModel
from typing import List
from .subtarea_schema import SubtareaSchema

class TareaSchema(BaseModel):
    nombre: str
    subtareas: List[SubtareaSchema]  # Lista de subtareas

    # Totales de tiempo para la tarea completa (opcional en la respuesta)
    tiempo_optimista: float = None
    tiempo_pesimista: float = None
    tiempo_esperado: float = None

    class Config:
        orm_mode = True
