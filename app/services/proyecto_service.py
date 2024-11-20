from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import List, Dict
from app.models.proyecto_db import ProyectoDB
from app.models.hito_db import HitoDB
from app.models.tarea_db import TareaDB
from app.models.subtarea_db import SubtareaDB
from sqlalchemy import select, delete


async def limpiar_datos(db: AsyncSession):
    try:
        # Borrar todas las subtareas
        await db.execute(delete(SubtareaDB))
        # Borrar todas las tareas
        await db.execute(delete(TareaDB))
        # Borrar todos los hitos
        await db.execute(delete(HitoDB))
        # Borrar todos los proyectos
        await db.execute(delete(ProyectoDB))
        await db.commit()  # Confirmar los cambios
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al limpiar la base de datos: {str(e)}")


async def insertar_datos_proyecto(
    db: AsyncSession,
    nombre_proyecto: str,
    descripcion: str,
    datos: List[Dict[str, str]]  # Lista de diccionarios con los datos validados del CSV
):
    try:
        # Limpiar la base de datos antes de la inserción
        await limpiar_datos(db)

        # Crear un nuevo proyecto en la base de datos
        nuevo_proyecto = ProyectoDB(nombre=nombre_proyecto, descripcion=descripcion)
        db.add(nuevo_proyecto)
        await db.commit()
        await db.refresh(nuevo_proyecto)

        # Crear hitos, tareas y subtareas basados en los datos validados del CSV
        subtarea_id_map = {}  # Para mapear subtareaID con sus objetos SubtareaDB

        for fila in datos:
            # Verificar si el hito ya existe en el proyecto actual
            hito_obj = await db.execute(
                select(HitoDB).filter(HitoDB.nombre == fila["hito"], HitoDB.proyecto_id == nuevo_proyecto.id)
            )
            hito_obj = hito_obj.scalar_one_or_none()

            if not hito_obj:
                # Si no existe el hito, lo creamos
                hito_obj = HitoDB(
                    nombre=fila["hito"],  # Nombre del hito desde el CSV
                    proyecto_id=nuevo_proyecto.id
                )
                db.add(hito_obj)
                await db.commit()
                await db.refresh(hito_obj)

            # Verificar si la tarea ya existe en el hito actual
            tarea_obj = await db.execute(
                select(TareaDB).filter(TareaDB.nombre == fila["tarea"], TareaDB.hito_id == hito_obj.id)
            )
            tarea_obj = tarea_obj.scalar_one_or_none()

            if not tarea_obj:
                # Si no existe la tarea, la creamos
                tarea_obj = TareaDB(
                    nombre=fila["tarea"],  # Nombre de la tarea desde el CSV
                    hito_id=hito_obj.id
                )
                db.add(tarea_obj)
                await db.commit()
                await db.refresh(tarea_obj)

            # Verificar el valor de tiempo_probable
            tiempo_probable = fila.get("tiempo probable")
            try:
                tiempo_probable = float(tiempo_probable) if tiempo_probable else 0.0
            except ValueError:
                raise HTTPException(status_code=400, detail=f"El valor de 'tiempo probable' no es válido en la fila: {fila}")

            # Verificar si "subtareaID" está presente en el CSV
            subtarea_id_csv = fila["subtareaID"] if fila["subtareaID"] else None


            # Procesar dependencia si existe
            dependencia_ids = []
            if fila.get("dependencia"):
                dependencias = fila["dependencia"].split(",")  # Manejar múltiples dependencias separadas por comas
                for dep_id in dependencias:
                    dep_id = dep_id.strip()  # Mantener el formato "x.x.x" como cadena
                    # Validar que la dependencia es un identificador válido
                    if not dep_id.replace(".", "").isdigit():
                        raise HTTPException(
                            status_code=400,
                            detail=f"El valor de dependencia '{dep_id}' en la fila: {fila} no es un ID válido.",
                        )
                    dependencia_ids.append(dep_id)  # Guardar el valor como cadena


            # Crear la subtarea
            subtarea_obj = SubtareaDB(
                nombre=fila["subtarea"],
                tiempo_probable=tiempo_probable,
                tarea_id=tarea_obj.id,
                subtarea_id_csv=subtarea_id_csv,  # El subtarea_id_csv del CSV
                dependencia_id=dependencia_ids,  # Lista de IDs de subtareas dependientes (formato x.x.x)
            )
            db.add(subtarea_obj)
            await db.commit()
            await db.refresh(subtarea_obj)

            # Mapear subtareaID con el objeto creado
            subtarea_id_map[subtarea_id_csv] = subtarea_obj

        return {"message": f"Proyecto '{nuevo_proyecto.nombre}' creado exitosamente"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar datos en la base de datos: {str(e)}")
