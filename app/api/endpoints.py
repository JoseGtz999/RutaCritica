# app/api/endpoints.py
from fastapi import APIRouter
from ..schemas.hito_schema import HitoSchema
from ..models.hito import Hito
from ..models.tarea import Tarea  # Importa el modelo Tarea
from ..models.subtarea import Subtarea  # Importa el modelo Subtarea
from ..services.calculos_totales import CalculosTotales

router = APIRouter()

# Endpoint para crear un hito
@router.post("/rutaCritica/hitos")
async def crear_hito(hito: HitoSchema):
    nuevo_hito = Hito(nombre=hito.nombre, tareas=[])

    # Añadimos las tareas y subtareas del hito
    for tarea_data in hito.tareas:
        tarea = Tarea(nombre=tarea_data.nombre, subtareas=[])
        for subtarea_data in tarea_data.subtareas:
            subtarea = Subtarea(
                nombre=subtarea_data.nombre,
                tiempo_probable=subtarea_data.tiempo_probable
            )
            tarea.agregar(subtarea)  # Agrega la subtarea a la tarea
        nuevo_hito.tareas.append(tarea)  # Agrega la tarea al hito

    # Devuelve un mensaje de éxito al crear el hito
    return {"message": f"Hito '{nuevo_hito.nombre}' creado exitosamente"}

# Endpoint para obtener cálculos totales
@router.get("/rutaCritica/calculos")
async def obtener_calculos_totales():
    calculos_totales = CalculosTotales(hitos).calcular_totales()
    return calculos_totales

