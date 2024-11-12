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

            # Verificar si "dependencia" es un nombre de otra subtarea
            dependencia_obj = None
            if fila.get("dependencia"):
                # Buscar la subtarea que se menciona como dependencia
                print(f"Buscando dependencia para subtarea '{fila['subtarea']}' con nombre '{fila['dependencia']}'")
                dependencia_obj = await db.execute(
                    select(SubtareaDB).filter(SubtareaDB.nombre == fila["dependencia"])
                )
                dependencia_obj = dependencia_obj.scalar_one_or_none()

                # Depuración: Si se encuentra o no la dependencia
                if dependencia_obj:
                    print(f"Dependencia encontrada: {dependencia_obj.id} para '{fila['dependencia']}'")
                else:
                    print(f"No se encontró dependencia para subtarea '{fila['subtarea']}'")

            # Verificar el valor de tiempo_esperado
            tiempo_esperado = fila.get("tiempo esperado")
            
            # Intentar convertir el valor de tiempo_esperado en un float
            try:
                tiempo_esperado = float(tiempo_esperado) if tiempo_esperado else 0.0
            except ValueError:
                print(f"Error: el valor de 'tiempo esperado' no es válido para '{fila['subtarea']}'")
                tiempo_esperado = 0.0

            # Imprimir el valor para verificar
            print(f"Tiempo esperado para subtarea '{fila['subtarea']}': {tiempo_esperado}")

            # Verificar si "subtareaID" está presente en el CSV y convertirlo a entero
            subtarea_id_csv = int(fila["subtareaID"]) if fila["subtareaID"] else None

            # Verificar si la subtarea ya existe en la tarea basada en el subtarea_id_csv
            subtarea_obj = await db.execute(
                select(SubtareaDB).filter(SubtareaDB.subtarea_id_csv == subtarea_id_csv, SubtareaDB.tarea_id == tarea_obj.id)
            )
            subtarea_obj = subtarea_obj.scalar_one_or_none()

            if not subtarea_obj:
                # Si no existe la subtarea, la creamos
                subtarea_obj = SubtareaDB(
                    nombre=fila["subtarea"],
                    dependencia_id=dependencia_obj.id if dependencia_obj else None,  # Aquí cambiamos 'dependencia' por 'dependencia_id'
                    tiempo_esperado=tiempo_esperado,
                    tarea_id=tarea_obj.id,
                    subtarea_id_csv=subtarea_id_csv  # Aquí aseguramos que se pase como entero
                )
                db.add(subtarea_obj)
                await db.commit()  # Guardar en la base de datos
                await db.refresh(subtarea_obj)  # Refrescar el objeto para verificar que se guardó correctamente

                # Verificar que se guardó correctamente
                print(f"Subtarea '{subtarea_obj.nombre}' guardada con tiempo_esperado: {subtarea_obj.tiempo_esperado}")
            else:
                print(f"Subtarea '{subtarea_obj.nombre}' ya existe y no se vuelve a insertar.")

        return {"message": f"Proyecto '{nuevo_proyecto.nombre}' creado exitosamente"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar datos en la base de datos: {str(e)}")
