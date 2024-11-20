from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..schemas.proyecto_schema import ProyectoSchema
from ..services.proyecto_service import insertar_datos_proyecto
from ..database import get_db
from ..services.calculos_proyecto_service import CalculosProyectoService
from ..models.hito_db import HitoDB
from ..models.tarea_db import TareaDB

router = APIRouter()

# Endpoint para crear un proyecto
@router.post("/rutaCritica/proyectos")
async def crear_proyecto(proyecto: ProyectoSchema, db: AsyncSession = Depends(get_db)):
    try:
        nuevo_proyecto = await insertar_datos_proyecto(
            db,
            nombre=proyecto.nombre,
            descripcion=proyecto.descripcion,
            hitos_data=proyecto.hitos
        )
        return {"message": f"Proyecto '{nuevo_proyecto.nombre}' creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear el proyecto: {str(e)}")

# Endpoint para obtener cálculos totales
@router.get("/rutaCritica/calculos")
async def obtener_calculos_totales(db: AsyncSession = Depends(get_db)):
    try:
        # Consulta los hitos, tareas y subtareas utilizando joinedload
        resultado = await db.execute(
            select(HitoDB)
            .options(
                joinedload(HitoDB.tareas)  # Cargar tareas asociadas al hito
                .joinedload(TareaDB.subtareas)  # Cargar subtareas asociadas a las tareas
            )
        )

        # Obtener los hitos cargados con tareas y subtareas
        hitos_list = resultado.scalars().unique().all()

        # Instancia el servicio de cálculos de proyecto con los hitos
        calculos_servicio = CalculosProyectoService(hitos=hitos_list)

        # Ejecuta los cálculos
        calculos_totales = calculos_servicio.ejecutar_calculos()

        return calculos_totales
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener cálculos: {str(e)}")