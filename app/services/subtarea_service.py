from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.subtarea_db import SubtareaDB

async def obtener_datos_subtareas(db: AsyncSession):
    """
    Servicio para obtener los datos de las subtareas.
    Devuelve id, nombre, tiempo_probable y tiempo_real de cada subtarea.
    """
    try:
        # Consultar las subtareas de la base de datos
        resultado = await db.execute(
            select(SubtareaDB.id, SubtareaDB.nombre, SubtareaDB.tiempo_probable, SubtareaDB.tiempoReal)
        )
        subtareas = resultado.all()

        # Formatear los resultados en una lista de diccionarios
        subtareas_formateadas = [
            {
                "id": subtarea[0],
                "nombre": subtarea[1],
                "tiempo_estimado": subtarea[2],
                "tiempo_real": subtarea[3] if subtarea[3] is not None else "null"
            }
            for subtarea in subtareas
        ]

        return subtareas_formateadas
    except Exception as e:
        raise Exception(f"Error al obtener los datos de las subtareas: {str(e)}")

