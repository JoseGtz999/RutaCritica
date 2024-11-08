# app/services/proyecto_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.proyecto_db import ProyectoDB
from app.models.hito_db import HitoDB
from app.models.tarea_db import TareaDB
from app.models.subtarea_db import SubtareaDB

async def insertar_proyecto(db: AsyncSession, nombre: str, descripcion: str, hitos_data: list):
    # Crear una instancia de ProyectoDB
    proyecto = ProyectoDB(nombre=nombre, descripcion=descripcion)

    # Iterar sobre los datos de los hitos
    for hito_data in hitos_data:
        # Accede a los atributos de hito_data correctamente
        hito = HitoDB(
            nombre=hito_data.nombre,  # Acceder como atributo, no como índice
            tiempo_optimista=hito_data.tiempo_optimista,  # Acceder como atributo
            tiempo_pesimista=hito_data.tiempo_pesimista,
            tiempo_esperado=hito_data.tiempo_esperado,
            proyecto=proyecto
        )

        # Crear tareas y subtareas
        for tarea_data in hito_data.tareas:  # Acceder a tareas como atributo
            tarea = TareaDB(nombre=tarea_data.nombre, hito=hito)
            for subtarea_data in tarea_data.subtareas:  # Acceder como atributo
                subtarea = SubtareaDB(
                    nombre=subtarea_data.nombre,
                    tiempo_probable=subtarea_data.tiempo_probable,
                    tiempo_optimista=subtarea_data.tiempo_optimista,
                    tiempo_pesimista=subtarea_data.tiempo_pesimista,
                    tiempo_esperado=subtarea_data.tiempo_esperado,
                    tarea=tarea
                )
                db.add(subtarea)

            db.add(tarea)
        
        db.add(hito)

    db.add(proyecto)
    await db.commit()  # Guardar los cambios de forma asincrónica
    await db.refresh(proyecto)  # Actualizar la instancia del proyecto
    return proyecto