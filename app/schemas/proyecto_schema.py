from pydantic import BaseModel
from typing import List, Optional
from .hito_schema import HitoSchema

class ProyectoSchema(BaseModel):
    nombre: str
    descripcion: str = ""
    hitos: Optional[List[HitoSchema]] = None  

    # Nuevos campos para tiempos calculados
    tiempo_optimista_total: Optional[float] = None
    tiempo_pesimista_total: Optional[float] = None
    tiempo_esperado_total: Optional[float] = None
    desviacion_estandar_total: Optional[float] = None

    class Config:
        from_attributes = True  # Permite que el esquema funcione con ORMs
