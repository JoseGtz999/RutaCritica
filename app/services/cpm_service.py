from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.subtarea_db import SubtareaDB
from typing import List

async def obtener_datos_ruta_critica(db: AsyncSession) -> List[dict]:
    """
    Obtiene los datos relevantes de las subtareas para la ruta crítica.
    """
    try:
        result = await db.execute(select(SubtareaDB))
        subtareas = result.scalars().all()

        subtareas_data = [
            {
                "nombre": subtarea.nombre or "Sin nombre",  # Nombre por defecto
                "tiempo_probable": subtarea.tiempo_probable or 0,  # Tiempo probable por defecto
                "dependencia_id": subtarea.dependencia_id or [],  # Lista vacía si es nulo
                "subtarea_id_csv": subtarea.subtarea_id_csv or "0"  # ID por defecto
            }
            for subtarea in subtareas
        ]
        return subtareas_data
    except Exception as e:
        raise Exception(f"Error al obtener datos de la ruta crítica: {str(e)}")
