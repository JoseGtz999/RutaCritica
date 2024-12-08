from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.subtarea_db import SubtareaDB
from typing import List

async def obtener_datos_ruta_critica(db: AsyncSession) -> List[dict]:
    """
    Obtiene los datos relevantes de las subtareas para la ruta crítica.
    
    :param db: La sesión de base de datos.
    :return: Lista de diccionarios con la información de las subtareas.
    """
    try:
        # Consulta de todas las subtareas
        result = await db.execute(select(SubtareaDB))
        subtareas = result.scalars().all()

        # Seleccionar solo los campos que necesitamos
        subtareas_data = [
            {
                "nombre": subtarea.nombre,
                "tiempo_probable": subtarea.tiempo_probable,
                "dependencia_id": subtarea.dependencia_id,
                "subtarea_id_csv": subtarea.subtarea_id_csv
            }
            for subtarea in subtareas
        ]
        return subtareas_data

    except Exception as e:
        raise Exception(f"Error al obtener datos de la ruta crítica: {str(e)}")
