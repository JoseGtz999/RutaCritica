# app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.proyecto_schema import ProyectoSchema  # Esquema de Proyecto
from ..services.proyecto_service import insertar_proyecto  # Servicio de inserción de proyecto
from ..database import get_db  # Dependencia de sesión DB
from ..services.calculos_totales import CalculosTotales

router = APIRouter()

# Endpoint para crear un proyecto
@router.post("/rutaCritica/proyectos")
async def crear_proyecto(proyecto: ProyectoSchema, db: AsyncSession = Depends(get_db)):
    try:
        # Llama a la función asincrónica `insertar_proyecto` para guardar el proyecto en la BD
        nuevo_proyecto = await insertar_proyecto(
            db,
            nombre=proyecto.nombre,
            descripcion=proyecto.descripcion,
            hitos_data=proyecto.hitos
        )
        # Devuelve un mensaje de éxito al crear el proyecto
        return {"message": f"Proyecto '{nuevo_proyecto.nombre}' creado exitosamente"}
    except Exception as e:
        # Manejo de errores y devolución de una respuesta HTTP de error
        raise HTTPException(status_code=400, detail=f"Error al crear el proyecto: {str(e)}")

# Endpoint para obtener cálculos totales
@router.get("/rutaCritica/calculos")
async def obtener_calculos_totales():
    try:
        # Llama a la función calcular_totales para obtener cálculos
        calculos_totales = CalculosTotales().calcular_totales()
        return calculos_totales
    except Exception as e:
        # Manejo de errores y devolución de una respuesta HTTP de error
        raise HTTPException(status_code=400, detail=f"Error al obtener cálculos: {str(e)}")
