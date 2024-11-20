# app/schemas/subtarea_schema.py
from pydantic import BaseModel

class SubtareaSchema(BaseModel):
    nombre: str
    PERT: float

    # Opcionalmente, puedes definir los tiempos esperados si los necesitas en la respuesta
    tiempo_optimista: float = None
    tiempo_pesimista: float = None
    tiempo_probable: float = None

    class Config:
        from_attributes = True  # Habilita compatibilidad con ORMs para interactuar con modelos
