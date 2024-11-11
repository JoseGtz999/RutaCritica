from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import List, Dict
from app.models.proyecto_db import ProyectoDB
from app.models.hito_db import HitoDB
from app.models.tarea_db import TareaDB
from app.models.subtarea_db import SubtareaDB
from app.models.subtarea_db import SubtareaDB
from sqlalchemy import select


async def insertar_datos_proyecto(
    db: AsyncSession,
    nombre_proyecto: str,
    descripcion: str,
    datos: List[Dict[str, str]]  # Lista de diccionarios con los datos validados del CSV
):
    try:
        # Crear un nuevo proyecto en la base de datos
        nuevo_proyecto = ProyectoDB(nombre=nombre_proyecto, descripcion=descripcion)
        db.add(nuevo_proyecto)
        await db.commit()
        await db.refresh(nuevo_proyecto)

        # Crear hitos, tareas y subtareas basados en los datos validados del CSV
        for fila in datos:
            # Crear el hito si no existe en el proyecto actual
            hito_obj = HitoDB(
                nombre=fila["hito"],  # Nombre del hito desde el CSV
                proyecto_id=nuevo_proyecto.id
            )
            db.add(hito_obj)
            await db.commit()
            await db.refresh(hito_obj)

            # Crear la tarea
            tarea_obj = TareaDB(
                nombre=fila["tarea"],  # Nombre de la tarea desde el CSV
                hito_id=hito_obj.id
            )
            db.add(tarea_obj)
            await db.commit()
            await db.refresh(tarea_obj)

            # Verificar si "dependencia" es un nombre de otra subtarea
            dependencia_obj = None
            if fila.get("dependencia"):
                dependencia_obj = await db.execute(
                    select(SubtareaDB).filter(SubtareaDB.nombre == fila["dependencia"])
                )
                dependencia_obj = dependencia_obj.scalar_one_or_none()

            # Crear la subtarea
            subtarea_obj = SubtareaDB(
                nombre=fila["subtarea"],  # Nombre de la subtarea desde el CSV
                dependencia=dependencia_obj,  # Dependencia como objeto
                tiempo_esperado=float(fila.get("tiempo esperado", 0)),  # Tiempo esperado desde el CSV
                tarea_id=tarea_obj.id
            )
            db.add(subtarea_obj)
            await db.commit()

        return {"message": f"Proyecto '{nuevo_proyecto.nombre}' creado exitosamente"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar datos en la base de datos: {str(e)}")
