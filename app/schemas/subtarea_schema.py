# app/schemas/subtarea_schema.py
from pydantic import BaseModel

class SubtareaSchema(BaseModel):
    nombre: str
    tiempo_probable: float

    # Opcionalmente, puedes definir los tiempos esperados si los necesitas en la respuesta
    tiempo_optimista: float = None
    tiempo_pesimista: float = None
    tiempo_esperado: float = None

    class Config:
        from_attributes = True  # Habilita compatibilidad con ORMs para interactuar con modelos
