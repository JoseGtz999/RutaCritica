from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..schemas.proyecto_schema import ProyectoSchema
from ..services.proyecto_service import insertar_datos_proyecto
from ..database import get_db
from ..services.calculos_proyecto_service import CalculosProyectoService
from ..services.cpm_service import obtener_datos_ruta_critica

from ..models.hito_db import HitoDB
from ..models.tarea_db import TareaDB
from app.models.subtarea_db import SubtareaDB

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
    

@router.get("/rutaCritica/subtareas")
async def obtener_subtareas(db: AsyncSession = Depends(get_db)):
    """
    Endpoint para obtener subtareas con su tiempo estimado y tiempo real.
    """
    try:
        from ..services.subtarea_service import obtener_datos_subtareas  # Importa el servicio
        subtareas = await obtener_datos_subtareas(db)  # Llama al servicio
        return {"estado": "exito", "subtareas": subtareas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener subtareas: {str(e)}")

@router.put("/subtarea/{subtarea_id}")
async def actualizar_tiempo_real(
    subtarea_id: str,  # ID de la subtarea a actualizar
    tiempo_real: float,  # Nuevo valor para el tiempo real
    db: AsyncSession = Depends(get_db)
):
    """
    Actualiza el tiempo_real de una subtarea específica por ID.
    """
    try:
        # Buscar la subtarea por su ID
        subtarea_obj = await db.execute(
            select(SubtareaDB).filter(SubtareaDB.subtarea_id_csv == subtarea_id)
        )
        subtarea_obj = subtarea_obj.scalar_one_or_none()

        if not subtarea_obj:
            raise HTTPException(status_code=404, detail=f"Subtarea con ID '{subtarea_id}' no encontrada.")

        # Validar el valor de tiempo_real (debe ser un número positivo)
        if tiempo_real < 0:
            raise HTTPException(status_code=400, detail="El valor de 'tiempo_real' no puede ser negativo.")

        # Actualizar el tiempo_real de la subtarea
        subtarea_obj.tiempo_real = tiempo_real
        await db.commit()
        await db.refresh(subtarea_obj)

        return {"estado": "exito", "mensaje": f"Tiempo real de la subtarea con ID '{subtarea_id}' actualizado exitosamente."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el tiempo real de la subtarea: {str(e)}")

@router.get("/rutaCritica/subtareasCPM")
async def obtener_subtareas_ruta_critica(db: AsyncSession = Depends(get_db)):
    """
    Endpoint para obtener la información de las subtareas necesarias para calcular la ruta crítica.
    Incluye nombre, tiempo probable, dependencia_id y subtarea_id_csv.
    """
    try:
        # Llamamos al servicio que obtiene los datos de las subtareas para la ruta crítica
        subtareas = await obtener_datos_ruta_critica(db)

        # Retornamos la lista de subtareas con la información deseada
        return {"estado": "exito", "subtareas": subtareas}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las subtareas: {str(e)}")
